"""Contrato de persistencia para :class:`Horario` y sus asignaciones.

Además de los horarios/turnos, expone las consultas de asignación de
workstations responsables y del historial por alumno.
"""

from abc import ABC, abstractmethod
from datetime import date, time
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import AsignacionWorkstation, EstadoHorario, Horario


class AbstractHorarioRepository(ABC):
    """Puerto de salida para horarios de laboratorio y asignaciones."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Horario]:
        """Recupera un horario por su clave primaria.

        Args:
            id (int): Identificador único de la fila en ``horarios``.

        Returns:
            Optional[Horario]: Entidad encontrada o ``None`` si no existe.
        """
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        laboratorio_id: Optional[int] = None,
        fecha: Optional[date] = None,
        estado: Optional[EstadoHorario] = None,
    ) -> Pagina[Horario]:
        """Lista horarios paginados con filtros opcionales.

        Args:
            paginacion (ParametrosPaginacion): Página, tamaño y cálculo de totales.
            laboratorio_id (Optional[int]): Filtra por laboratorio.
            fecha (Optional[date]): Filtra por día del turno.
            estado (Optional[EstadoHorario]): Filtra por estado del turno.

        Returns:
            Pagina[Horario]: Página ordenada por fecha descendente y hora de inicio.
        """
        pass

    @abstractmethod
    def create(self, obj: Horario) -> Horario:
        """Persiste un horario nuevo.

        Args:
            obj (Horario): Entidad validada por la capa de aplicación.

        Returns:
            Horario: Entidad creada con su ``id`` asignado.
        """
        pass

    @abstractmethod
    def update(self, obj: Horario) -> Horario:
        """Actualiza un horario existente (por ejemplo, su estado).

        Args:
            obj (Horario): Entidad modificada a persistir.

        Returns:
            Horario: Entidad actualizada y refrescada.
        """
        pass

    @abstractmethod
    def get_conflictos(
        self, laboratorio_id: int, fecha: date, hora_inicio: time, hora_fin: time
    ) -> list:
        """Detecta turnos activos que se solapan con un rango solicitado.

        Args:
            laboratorio_id (int): Laboratorio donde se programa el turno.
            fecha (date): Fecha del turno propuesto.
            hora_inicio (time): Hora de inicio propuesta.
            hora_fin (time): Hora de fin propuesta.

        Returns:
            list: Horarios en estado ``programado`` o ``en_curso`` que
            intersectan el rango. Lista vacía si no hay conflicto.

        Note:
            Consulta interna de apoyo a la validación de negocio; no está
            paginada porque no se expone directamente como listado.
        """
        pass

    @abstractmethod
    def create_asignacion(
        self, asignacion: AsignacionWorkstation
    ) -> AsignacionWorkstation:
        """Persiste la asignación de una workstation a un alumno en un turno.

        Args:
            asignacion (AsignacionWorkstation): Entidad de asignación validada.

        Returns:
            AsignacionWorkstation: Asignación creada con su ``id`` asignado.
        """
        pass

    @abstractmethod
    def get_asignacion_por_horario_y_workstation(
        self, horario_id: int, workstation_id: int
    ) -> Optional[AsignacionWorkstation]:
        """Verifica si una workstation ya tiene responsable en un turno.

        Args:
            horario_id (int): Turno a consultar.
            workstation_id (int): Puesto de trabajo a verificar.

        Returns:
            Optional[AsignacionWorkstation]: Asignación existente o ``None``.
        """
        pass

    @abstractmethod
    def get_asignacion_por_horario_y_alumno(
        self, horario_id: int, codigo_alumno: str
    ) -> Optional[AsignacionWorkstation]:
        """Verifica si un alumno ya tiene asignada una workstation en el turno.

        Args:
            horario_id (int): Turno a consultar.
            codigo_alumno (str): Código institucional del alumno.

        Returns:
            Optional[AsignacionWorkstation]: Asignación existente o ``None``.
        """
        pass

    @abstractmethod
    def listar_asignaciones(
        self,
        paginacion: ParametrosPaginacion,
        horario_id: Optional[int] = None,
        codigo_alumno: Optional[str] = None,
    ) -> Pagina[AsignacionWorkstation]:
        """Lista asignaciones paginadas con filtros opcionales.

        Args:
            paginacion (ParametrosPaginacion): Página, tamaño y cálculo de totales.
            horario_id (Optional[int]): Filtra por turno.
            codigo_alumno (Optional[str]): Filtra por alumno responsable.

        Returns:
            Pagina[AsignacionWorkstation]: Página de asignaciones.
        """
        pass

    @abstractmethod
    def listar_historial_alumno(
        self, paginacion: ParametrosPaginacion, codigo_alumno: str
    ) -> Pagina[AsignacionWorkstation]:
        """Obtiene el historial paginado de puestos asignados a un alumno.

        Args:
            paginacion (ParametrosPaginacion): Página, tamaño y cálculo de totales.
            codigo_alumno (str): Código institucional del alumno.

        Returns:
            Pagina[AsignacionWorkstation]: Asignaciones ordenadas por fecha de
            asignación descendente.
        """
        pass
