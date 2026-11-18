from datetime import date
from typing import Optional

from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import (
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
            raise NotFoundException(f"Laboratorio {data.laboratorio_id} no encontrado.")

        if lab.estado != EstadoLaboratorio.DISPONIBLE:
            raise BadRequestException(f"El laboratorio '{lab.nombre}' no está disponible (estado: {lab.estado.value}).")

        conflictos = self.horario_repo.get_conflictos(
            laboratorio_id=data.laboratorio_id,
            fecha=data.fecha,
            hora_inicio=data.hora_inicio,
            hora_fin=data.hora_fin,
        )
        if conflictos:
            raise ConflictException("Ya existe un horario activo que se cruza con el rango solicitado.")

        nuevo_horario = Horario(**data.model_dump())
        return self.horario_repo.create(nuevo_horario)

    def listar_horarios(
        self,
        paginacion: ParametrosPaginacion,
        laboratorio_id: Optional[int] = None,
        fecha: Optional[date] = None,
        estado: Optional[EstadoHorario] = None,
    ) -> Pagina[Horario]:
        return self.horario_repo.listar(paginacion, laboratorio_id, fecha, estado)

    def obtener_horario(self, horario_id: int) -> Horario:
        horario = self.horario_repo.get_by_id(horario_id)
        if not horario:
            raise NotFoundException(f"Horario {horario_id} no encontrado.")
        return horario

    def iniciar_turno(self, horario_id: int) -> Horario:
        horario = self.obtener_horario(horario_id)
        if horario.estado != EstadoHorario.PROGRAMADO:
            raise BadRequestException("Solo se puede iniciar un turno que se encuentre programado.")
        horario.estado = EstadoHorario.EN_CURSO
        return self.horario_repo.update(horario)

    def finalizar_turno(self, horario_id: int) -> Horario:
        horario = self.obtener_horario(horario_id)
        if horario.estado not in (EstadoHorario.PROGRAMADO, EstadoHorario.EN_CURSO):
            raise BadRequestException("Solo se pueden finalizar turnos programados o en curso.")
        horario.estado = EstadoHorario.FINALIZADO
        return self.horario_repo.update(horario)

    def cancelar_turno(self, horario_id: int) -> Horario:
        horario = self.obtener_horario(horario_id)
        if horario.estado != EstadoHorario.PROGRAMADO:
            raise BadRequestException("Solo se pueden cancelar turnos que aún estén programados.")
        horario.estado = EstadoHorario.CANCELADO
        return self.horario_repo.update(horario)

    def asignar_workstation(
        self, horario_id: int, data: AsignacionCreate
    ) -> AsignacionWorkstation:
        horario = self.obtener_horario(horario_id)
        if horario.estado not in (EstadoHorario.PROGRAMADO, EstadoHorario.EN_CURSO):
            raise BadRequestException("No se pueden asignar puestos en un turno finalizado o cancelado.")

        ws = self.ws_repo.get_by_id(data.workstation_id)
        if not ws:
            raise NotFoundException(f"Workstation {data.workstation_id} no encontrada.")

        if ws.laboratorio_id != horario.laboratorio_id:
            raise BadRequestException("La workstation no pertenece al laboratorio asignado a este turno.")

        if ws.estado != EstadoWorkstation.DISPONIBLE:
            raise BadRequestException(f"La workstation '{ws.codigo}' no está disponible (estado: {ws.estado.value}).")

        if self.horario_repo.get_asignacion_por_horario_y_workstation(
            horario_id, data.workstation_id
        ):
            raise ConflictException(f"La workstation '{ws.codigo}' ya tiene un alumno responsable en este turno.")

        if self.horario_repo.get_asignacion_por_horario_y_alumno(
            horario_id, data.codigo_alumno
        ):
            raise ConflictException(f"El alumno '{data.codigo_alumno}' ya tiene asignada otra workstation en este turno.")

        asignacion = AsignacionWorkstation(
            horario_id=horario_id,
            workstation_id=data.workstation_id,
            codigo_alumno=data.codigo_alumno,
            observaciones=data.observaciones,
        )
        return self.horario_repo.create_asignacion(asignacion)

    def listar_asignaciones_turno(
        self, paginacion: ParametrosPaginacion, horario_id: int
    ) -> Pagina[AsignacionWorkstation]:
        self.obtener_horario(horario_id)
        return self.horario_repo.listar_asignaciones(paginacion, horario_id=horario_id)

    def consultar_historial_alumno(
        self, paginacion: ParametrosPaginacion, codigo_alumno: str
    ) -> Pagina[AsignacionWorkstation]:
        return self.horario_repo.listar_historial_alumno(paginacion, codigo_alumno)
