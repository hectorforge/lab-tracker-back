from datetime import date
from typing import Optional

from app.api.pagination import mapear_pagina, Pagina, ParametrosPaginacion
from app.application.interfaces import AbstractHorarioService
from app.domain.exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from app.domain.repositories import (
    AbstractHorarioRepository,
    AbstractLaboratorioRepository,
    AbstractWorkstationRepository,
)
from app.application.dtos import (
    AsignacionDTO,
    CrearAsignacionDTO,
    CrearHorarioDTO,
    HorarioDTO,
)
from app.domain.entities import (
    AsignacionWorkstation,
    EstadoHorario,
    EstadoLaboratorio,
    EstadoWorkstation,
    Horario,
)


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

    def crear_horario(self, data: CrearHorarioDTO) -> HorarioDTO:
        lab = self.lab_repo.get_by_id(data.laboratorio_id)
        if not lab:
            raise NotFoundException(f"Laboratorio {data.laboratorio_id} no encontrado.")
        if lab.estado != EstadoLaboratorio.DISPONIBLE:
            raise BadRequestException(
                f"El laboratorio '{lab.nombre}' no está disponible."
            )
        if self.horario_repo.get_conflictos(
            data.laboratorio_id, data.fecha, data.hora_inicio, data.hora_fin
        ):
            raise ConflictException(
                "Ya existe un horario activo que se cruza con el rango solicitado."
            )
        entidad = self.horario_repo.create(Horario(**data.model_dump()))
        return HorarioDTO.model_validate(entidad)

    def listar_horarios(
        self,
        paginacion: ParametrosPaginacion,
        laboratorio_id: Optional[int] = None,
        fecha: Optional[date] = None,
        estado: Optional[EstadoHorario] = None,
    ) -> Pagina[HorarioDTO]:
        pagina = self.horario_repo.listar(paginacion, laboratorio_id, fecha, estado)
        return mapear_pagina(pagina, HorarioDTO.model_validate)

    def obtener_horario(self, horario_id: int) -> HorarioDTO:
        return HorarioDTO.model_validate(self._obtener_entidad(horario_id))

    def iniciar_turno(self, horario_id: int) -> HorarioDTO:
        horario = self._obtener_entidad(horario_id)
        if horario.estado != EstadoHorario.PROGRAMADO:
            raise BadRequestException(
                "Solo se puede iniciar un turno que se encuentre programado."
            )
        horario.estado = EstadoHorario.EN_CURSO
        return HorarioDTO.model_validate(self.horario_repo.update(horario))

    def finalizar_turno(self, horario_id: int) -> HorarioDTO:
        horario = self._obtener_entidad(horario_id)
        if horario.estado not in (EstadoHorario.PROGRAMADO, EstadoHorario.EN_CURSO):
            raise BadRequestException(
                "Solo se pueden finalizar turnos programados o en curso."
            )
        horario.estado = EstadoHorario.FINALIZADO
        return HorarioDTO.model_validate(self.horario_repo.update(horario))

    def cancelar_turno(self, horario_id: int) -> HorarioDTO:
        horario = self._obtener_entidad(horario_id)
        if horario.estado != EstadoHorario.PROGRAMADO:
            raise BadRequestException(
                "Solo se pueden cancelar turnos que aún estén programados."
            )
        horario.estado = EstadoHorario.CANCELADO
        return HorarioDTO.model_validate(self.horario_repo.update(horario))

    def asignar_workstation(
        self, horario_id: int, data: CrearAsignacionDTO
    ) -> AsignacionDTO:
        horario = self._obtener_entidad(horario_id)
        if horario.estado not in (EstadoHorario.PROGRAMADO, EstadoHorario.EN_CURSO):
            raise BadRequestException(
                "No se pueden asignar puestos en un turno finalizado o cancelado."
            )

        ws = self.ws_repo.get_by_id(data.workstation_id)
        if not ws:
            raise NotFoundException(
                f"Workstation {data.workstation_id} no encontrada."
            )
        if ws.laboratorio_id != horario.laboratorio_id:
            raise BadRequestException(
                "La workstation no pertenece al laboratorio de este turno."
            )
        if ws.estado != EstadoWorkstation.DISPONIBLE:
            raise BadRequestException(
                f"La workstation '{ws.codigo}' no está disponible."
            )
        if self.horario_repo.get_asignacion_por_horario_y_workstation(
            horario_id, data.workstation_id
        ):
            raise ConflictException(
                f"La workstation '{ws.codigo}' ya tiene un responsable en este turno."
            )
        if self.horario_repo.get_asignacion_por_horario_y_alumno(
            horario_id, data.codigo_alumno
        ):
            raise ConflictException(
                f"El alumno '{data.codigo_alumno}' ya tiene otra workstation en este turno."
            )

        entidad = self.horario_repo.create_asignacion(
            AsignacionWorkstation(
                horario_id=horario_id,
                workstation_id=data.workstation_id,
                codigo_alumno=data.codigo_alumno,
                observaciones=data.observaciones,
            )
        )
        return AsignacionDTO.model_validate(entidad)

    def listar_asignaciones_turno(
        self, paginacion: ParametrosPaginacion, horario_id: int
    ) -> Pagina[AsignacionDTO]:
        self._obtener_entidad(horario_id)
        pagina = self.horario_repo.listar_asignaciones(paginacion, horario_id=horario_id)
        return mapear_pagina(pagina, AsignacionDTO.model_validate)

    def consultar_historial_alumno(
        self, paginacion: ParametrosPaginacion, codigo_alumno: str
    ) -> Pagina[AsignacionDTO]:
        pagina = self.horario_repo.listar_historial_alumno(paginacion, codigo_alumno)
        return mapear_pagina(pagina, AsignacionDTO.model_validate)

    def _obtener_entidad(self, horario_id: int) -> Horario:
        horario = self.horario_repo.get_by_id(horario_id)
        if not horario:
            raise NotFoundException(f"Horario {horario_id} no encontrado.")
        return horario
