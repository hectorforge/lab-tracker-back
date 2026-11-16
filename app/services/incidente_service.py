from datetime import datetime
from typing import List
from fastapi import HTTPException, status
from app.models.lab_models import (
    Incidente,
    EstadoIncidente,
    EstadoEquipo,
    EstadoWorkstation,
)
from app.schemas.lab_schemas import IncidenteCreate, IncidenteUpdateEstado
from app.repositories.interfaces import (
    AbstractIncidenteRepository,
    AbstractEquipoRepository,
    AbstractWorkstationRepository,
)
from app.services.interfaces import AbstractIncidenteService


class IncidenteService(AbstractIncidenteService):
    def __init__(
        self,
        incidente_repo: AbstractIncidenteRepository,
        equipo_repo: AbstractEquipoRepository,
        ws_repo: AbstractWorkstationRepository,
    ):
        self.incidente_repo = incidente_repo
        self.equipo_repo = equipo_repo
        self.ws_repo = ws_repo

    def reportar_incidente(self, data: IncidenteCreate) -> Incidente:
        equipo = None
        ws = None

        if data.equipo_id is not None:
            equipo = self.equipo_repo.get_by_id(data.equipo_id)
            if not equipo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Equipo {data.equipo_id} no encontrado.",
                )

        if data.workstation_id is not None:
            ws = self.ws_repo.get_by_id(data.workstation_id)
            if not ws:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Workstation {data.workstation_id} no encontrada.",
                )

        if equipo and ws and equipo.workstation_id != ws.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El equipo indicado no pertenece a la workstation especificada.",
            )

        incidente = Incidente(**data.model_dump())
        creado = self.incidente_repo.create(incidente)

        if equipo and equipo.estado == EstadoEquipo.OPERATIVO:
            equipo.estado = EstadoEquipo.CON_FALLA
            self.equipo_repo.update(equipo)

        if ws and ws.estado == EstadoWorkstation.DISPONIBLE:
            ws.estado = EstadoWorkstation.CON_FALLA
            self.ws_repo.update(ws)

        return creado

    def listar_incidentes(self, solo_pendientes: bool = False) -> List[Incidente]:
        if solo_pendientes:
            return self.incidente_repo.get_pendientes()
        return self.incidente_repo.get_all()

    def listar_por_equipo(self, equipo_id: int) -> List[Incidente]:
        return self.incidente_repo.get_by_equipo(equipo_id)

    def listar_por_workstation(self, workstation_id: int) -> List[Incidente]:
        return self.incidente_repo.get_by_workstation(workstation_id)

    def actualizar_estado(
        self, incidente_id: int, data: IncidenteUpdateEstado
    ) -> Incidente:
        incidente = self.incidente_repo.get_by_id(incidente_id)
        if not incidente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Incidente {incidente_id} no encontrado.",
            )

        incidente.estado = data.estado
        equipo = (
            self.equipo_repo.get_by_id(incidente.equipo_id)
            if incidente.equipo_id is not None
            else None
        )
        ws = (
            self.ws_repo.get_by_id(incidente.workstation_id)
            if incidente.workstation_id is not None
            else None
        )

        if data.estado == EstadoIncidente.EN_PROCESO:
            incidente.fecha_resolucion = None
            if equipo and equipo.estado != EstadoEquipo.DE_BAJA:
                equipo.estado = EstadoEquipo.EN_MANTENIMIENTO
                self.equipo_repo.update(equipo)
            if ws and ws.estado != EstadoWorkstation.INHABILITADA:
                ws.estado = EstadoWorkstation.EN_MANTENIMIENTO
                self.ws_repo.update(ws)
            return self.incidente_repo.update(incidente)

        if data.estado == EstadoIncidente.RESUELTO:
            incidente.fecha_resolucion = datetime.now()
            actualizado = self.incidente_repo.update(incidente)

            if (
                equipo
                and equipo.estado != EstadoEquipo.DE_BAJA
                and self.incidente_repo.count_abiertos_por_equipo(equipo.id) == 0
            ):
                equipo.estado = EstadoEquipo.OPERATIVO
                self.equipo_repo.update(equipo)

            if (
                ws
                and ws.estado != EstadoWorkstation.INHABILITADA
                and self.incidente_repo.count_abiertos_por_workstation(ws.id) == 0
            ):
                ws.estado = EstadoWorkstation.DISPONIBLE
                self.ws_repo.update(ws)

            return actualizado

        incidente.fecha_resolucion = None
        return self.incidente_repo.update(incidente)