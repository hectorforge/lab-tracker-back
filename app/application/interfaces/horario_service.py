"""Contrato de la capa de aplicación para horarios y responsables de puesto."""

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.application.dtos import (
    AsignacionDTO,
    CrearAsignacionDTO,
    CrearHorarioDTO,
    HorarioDTO,
)
from app.domain.entities import EstadoHorario


class AbstractHorarioService(ABC):
    """Operaciones de negocio sobre turnos de laboratorio."""

    @abstractmethod
    def crear_horario(self, data: CrearHorarioDTO) -> HorarioDTO:
        """Programa un turno validando disponibilidad y ausencia de cruces.

        Args:
            data (CrearHorarioDTO): Laboratorio, fecha, rango horario y
                docente responsable.

        Returns:
            HorarioDTO: Horario creado en estado ``programado``.

        Raises:
            NotFoundException: Si el laboratorio no existe.
            BadRequestException: Si el laboratorio no está disponible.
            ConflictException: Si existe otro turno activo que se solapa.
        """
        pass

    @abstractmethod
    def listar_horarios(
        self,
        paginacion: ParametrosPaginacion,
        laboratorio_id: Optional[int] = None,
        fecha: Optional[date] = None,
        estado: Optional[EstadoHorario] = None,
    ) -> Pagina[HorarioDTO]:
        """Lista horarios paginados con filtros opcionales.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            laboratorio_id (Optional[int]): Filtra por laboratorio.
            fecha (Optional[date]): Filtra por día del turno.
            estado (Optional[EstadoHorario]): Filtra por estado del turno.

        Returns:
            Pagina[HorarioDTO]: Página de horarios ordenada cronológicamente.
        """
        pass

    @abstractmethod
    def obtener_horario(self, horario_id: int) -> HorarioDTO:
        """Obtiene un horario por su identificador.

        Args:
            horario_id (int): Identificador del turno.

        Returns:
            HorarioDTO: Horario encontrado.

        Raises:
            NotFoundException: Si el horario no existe.
        """
        pass

    @abstractmethod
    def iniciar_turno(self, horario_id: int) -> HorarioDTO:
        """Cambia un turno programado a ``en_curso``.

        Args:
            horario_id (int): Identificador del turno a iniciar.

        Returns:
            HorarioDTO: Turno actualizado.

        Raises:
            NotFoundException: Si el horario no existe.
            BadRequestException: Si el turno no estaba programado.
        """
        pass

    @abstractmethod
    def finalizar_turno(self, horario_id: int) -> HorarioDTO:
        """Cambia un turno programado o en curso a ``finalizado``.

        Args:
            horario_id (int): Identificador del turno a finalizar.

        Returns:
            HorarioDTO: Turno actualizado.

        Raises:
            NotFoundException: Si el horario no existe.
            BadRequestException: Si el turno estaba cancelado o ya finalizado.
        """
        pass

    @abstractmethod
    def cancelar_turno(self, horario_id: int) -> HorarioDTO:
        """Cancela un turno que aún estaba programado.

        Args:
            horario_id (int): Identificador del turno a cancelar.

        Returns:
            HorarioDTO: Turno cancelado.

        Raises:
            NotFoundException: Si el horario no existe.
            BadRequestException: Si el turno ya inició o estaba cancelado.
        """
        pass

    @abstractmethod
    def asignar_workstation(
        self, horario_id: int, data: CrearAsignacionDTO
    ) -> AsignacionDTO:
        """Asigna un alumno responsable a una workstation del turno.

        Args:
            horario_id (int): Turno en el que se realiza la asignación.
            data (CrearAsignacionDTO): Workstation, código de alumno y
                observaciones opcionales.

        Returns:
            AsignacionDTO: Asignación creada.

        Raises:
            NotFoundException: Si el turno o la workstation no existen.
            BadRequestException: Si el turno no está activo, la workstation
                pertenece a otro laboratorio o no está disponible.
            ConflictException: Si la workstation o el alumno ya tienen una
                asignación en el mismo turno.
        """
        pass

    @abstractmethod
    def listar_asignaciones_turno(
        self, paginacion: ParametrosPaginacion, horario_id: int
    ) -> Pagina[AsignacionDTO]:
        """Lista paginadamente las asignaciones registradas en un turno.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            horario_id (int): Turno a consultar.

        Returns:
            Pagina[AsignacionDTO]: Página de asignaciones.

        Raises:
            NotFoundException: Si el turno no existe.
        """
        pass

    @abstractmethod
    def consultar_historial_alumno(
        self, paginacion: ParametrosPaginacion, codigo_alumno: str
    ) -> Pagina[AsignacionDTO]:
        """Consulta el historial paginado de puestos de un alumno.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            codigo_alumno (str): Código institucional del alumno.

        Returns:
            Pagina[AsignacionDTO]: Asignaciones ordenadas por fecha reciente.
        """
        pass
