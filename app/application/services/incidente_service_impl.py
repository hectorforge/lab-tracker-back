from datetime import datetime, timezone

from app.api.pagination import mapear_pagina, Pagina, ParametrosPaginacion
from app.application.interfaces import AbstractIncidenteService
from app.domain.exceptions import BadRequestException, NotFoundException
from app.domain.repositories import (
    AbstractEquipoRepository,
    AbstractIncidenteRepository,
    AbstractWorkstationRepository,
)
from app.application.dtos import (
    ActualizarEstadoIncidenteDTO,
    CrearIncidenteDTO,
    IncidenteDTO,
)
from app.domain.entities import (
    EstadoEquipo,
    EstadoIncidente,
    EstadoWorkstation,
    Incidente,
)


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

    def reportar_incidente(self, data: CrearIncidenteDTO) -> IncidenteDTO:
        equipo = None
        ws = None
        if data.equipo_id is not None:
            equipo = self.equipo_repo.get_by_id(data.equipo_id)
            if not equipo:
                raise NotFoundException(f"Equipo {data.equipo_id} no encontrado.")
        if data.workstation_id is not None:
            ws = self.ws_repo.get_by_id(data.workstation_id)
            if not ws:
                raise NotFoundException(
                    f"Workstation {data.workstation_id} no encontrada."
                )
        if equipo and ws and equipo.workstation_id != ws.id:
            raise BadRequestException(
                "El equipo indicado no pertenece a la workstation especificada."
            )

        creado = self.incidente_repo.create(Incidente(**data.model_dump()))
        if equipo and equipo.estado == EstadoEquipo.OPERATIVO:
            equipo.estado = EstadoEquipo.CON_FALLA
            self.equipo_repo.update(equipo)
        if ws and ws.estado == EstadoWorkstation.DISPONIBLE:
            ws.estado = EstadoWorkstation.CON_FALLA
            self.ws_repo.update(ws)
        return IncidenteDTO.model_validate(creado)

    def listar_incidentes(
        self, paginacion: ParametrosPaginacion, solo_pendientes: bool = False
    ) -> Pagina[IncidenteDTO]:
        pagina = self.incidente_repo.listar(paginacion, solo_pendientes)
        return mapear_pagina(pagina, IncidenteDTO.model_validate)

    def listar_por_equipo(
        self, paginacion: ParametrosPaginacion, equipo_id: int
    ) -> Pagina[IncidenteDTO]:
        pagina = self.incidente_repo.listar(paginacion, equipo_id=equipo_id)
        return mapear_pagina(pagina, IncidenteDTO.model_validate)

    def listar_por_workstation(
        self, paginacion: ParametrosPaginacion, workstation_id: int
    ) -> Pagina[IncidenteDTO]:
        pagina = self.incidente_repo.listar(paginacion, workstation_id=workstation_id)
        return mapear_pagina(pagina, IncidenteDTO.model_validate)

    def actualizar_estado(
        self, incidente_id: int, data: ActualizarEstadoIncidenteDTO
    ) -> IncidenteDTO:
        incidente = self.incidente_repo.get_by_id(incidente_id)
        if not incidente:
            raise NotFoundException(f"Incidente {incidente_id} no encontrado.")

        incidente.estado = data.estado
        if data.url_imagenes:
            incidente.url_imagenes = list(
                dict.fromkeys(
                    (incidente.url_imagenes or []) + data.url_imagenes
                )
            )
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
            return IncidenteDTO.model_validate(self.incidente_repo.update(incidente))

        if data.estado == EstadoIncidente.RESUELTO:
            incidente.fecha_resolucion = datetime.now(timezone.utc)
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
            return IncidenteDTO.model_validate(actualizado)

        incidente.fecha_resolucion = None
        return IncidenteDTO.model_validate(self.incidente_repo.update(incidente))
