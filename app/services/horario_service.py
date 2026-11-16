from datetime import date
from typing import List, Optional
from fastapi import HTTPException, status
from app.models.lab_models import (
    Horario,
    AsignacionWorkstation,
    EstadoLaboratorio,
    EstadoWorkstation,
    EstadoHorario,
)
from app.schemas.lab_schemas import HorarioCreate, AsignacionCreate
from app.repositories.interfaces import (
    AbstractHorarioRepository,
    AbstractLaboratorioRepository,
    AbstractWorkstationRepository,
)
from app.services.interfaces import AbstractHorarioService


class HorarioService(AbstractHorarioService):
    def __init__(
        self,
        horario_repo: AbstractHorarioRepository,
        lab_repo: AbstractLaboratorioRepository,
        ws_repo: AbstractWorkstationRepository,
    ):
        self.horario_repo = horario_repo
        self.lab_repo = lab_repo
        self.ws_repo = ws_repo

    def crear_horario(self, data: HorarioCreate) -> Horario:
        lab = self.lab_repo.get_by_id(data.laboratorio_id)
        if not lab:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Laboratorio {data.laboratorio_id} no encontrado.",
            )

        if lab.estado != EstadoLaboratorio.DISPONIBLE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El laboratorio '{lab.nombre}' no está disponible (estado: {lab.estado.value}).",
            )

        conflictos = self.horario_repo.get_conflictos(
            laboratorio_id=data.laboratorio_id,
            fecha=data.fecha,
            hora_inicio=data.hora_inicio,
            hora_fin=data.hora_fin,
        )
        if conflictos:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un horario activo que se cruza con el rango solicitado.",
            )

        nuevo_horario = Horario(**data.model_dump())
        return self.horario_repo.create(nuevo_horario)

    def listar_horarios(
        self, laboratorio_id: Optional[int] = None, fecha: Optional[date] = None
    ) -> List[Horario]:
        if laboratorio_id is not None:
            return self.horario_repo.get_by_laboratorio_y_fecha(laboratorio_id, fecha)
        return self.horario_repo.get_all()

    def obtener_horario(self, horario_id: int) -> Horario:
        horario = self.horario_repo.get_by_id(horario_id)
        if not horario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Horario {horario_id} no encontrado.",
            )
        return horario

    def iniciar_turno(self, horario_id: int) -> Horario:
        horario = self.obtener_horario(horario_id)
        if horario.estado != EstadoHorario.PROGRAMADO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se puede iniciar un turno que se encuentre programado.",
            )
        horario.estado = EstadoHorario.EN_CURSO
        return self.horario_repo.update(horario)

    def finalizar_turno(self, horario_id: int) -> Horario:
        horario = self.obtener_horario(horario_id)
        if horario.estado not in (EstadoHorario.PROGRAMADO, EstadoHorario.EN_CURSO):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden finalizar turnos programados o en curso.",
            )
        horario.estado = EstadoHorario.FINALIZADO
        return self.horario_repo.update(horario)

    def cancelar_turno(self, horario_id: int) -> Horario:
        horario = self.obtener_horario(horario_id)
        if horario.estado != EstadoHorario.PROGRAMADO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden cancelar turnos que aún estén programados.",
            )
        horario.estado = EstadoHorario.CANCELADO
        return self.horario_repo.update(horario)

    def asignar_workstation(
        self, horario_id: int, data: AsignacionCreate
    ) -> AsignacionWorkstation:
        horario = self.obtener_horario(horario_id)
        if horario.estado not in (EstadoHorario.PROGRAMADO, EstadoHorario.EN_CURSO):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pueden asignar puestos en un turno finalizado o cancelado.",
            )

        ws = self.ws_repo.get_by_id(data.workstation_id)
        if not ws:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workstation {data.workstation_id} no encontrada.",
            )

        if ws.laboratorio_id != horario.laboratorio_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La workstation no pertenece al laboratorio asignado a este turno.",
            )

        if ws.estado != EstadoWorkstation.DISPONIBLE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La workstation '{ws.codigo}' no está disponible (estado: {ws.estado.value}).",
            )

        if self.horario_repo.get_asignacion_por_horario_y_workstation(
            horario_id, data.workstation_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"La workstation '{ws.codigo}' ya tiene un alumno responsable en este turno.",
            )

        if self.horario_repo.get_asignacion_por_horario_y_alumno(
            horario_id, data.codigo_alumno
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El alumno '{data.codigo_alumno}' ya tiene asignada otra workstation en este turno.",
            )

        asignacion = AsignacionWorkstation(
            horario_id=horario_id,
            workstation_id=data.workstation_id,
            codigo_alumno=data.codigo_alumno,
            observaciones=data.observaciones,
        )
        return self.horario_repo.create_asignacion(asignacion)

    def listar_asignaciones_turno(
        self, horario_id: int
    ) -> List[AsignacionWorkstation]:
        self.obtener_horario(horario_id)
        return self.horario_repo.get_asignaciones_por_horario(horario_id)

    def consultar_historial_alumno(
        self, codigo_alumno: str
    ) -> List[AsignacionWorkstation]:
        return self.horario_repo.get_historial_alumno(codigo_alumno)