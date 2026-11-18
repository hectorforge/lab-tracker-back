from abc import ABC, abstractmethod
from datetime import date, time
from typing import Optional

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import (
    AsignacionWorkstation,
    EstadoHorario,
    Horario,
)


class AbstractHorarioRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Horario]:
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        laboratorio_id: Optional[int] = None,
        fecha: Optional[date] = None,
        estado: Optional[EstadoHorario] = None,
    ) -> Pagina[Horario]:
        """Lista horarios paginados desde el repositorio."""
        pass

    @abstractmethod
    def create(self, obj: Horario) -> Horario:
        pass

    @abstractmethod
    def update(self, obj: Horario) -> Horario:
        pass

    @abstractmethod
    def get_conflictos(
        self, laboratorio_id: int, fecha: date, hora_inicio: time, hora_fin: time
    ) -> list:
        """Consulta interna (no paginada) de horarios que se solapan."""
        pass

    @abstractmethod
    def create_asignacion(
        self, asignacion: AsignacionWorkstation
    ) -> AsignacionWorkstation:
        pass

    @abstractmethod
    def get_asignacion_por_horario_y_workstation(
        self, horario_id: int, workstation_id: int
    ) -> Optional[AsignacionWorkstation]:
        pass

    @abstractmethod
    def get_asignacion_por_horario_y_alumno(
        self, horario_id: int, codigo_alumno: str
    ) -> Optional[AsignacionWorkstation]:
        pass

    @abstractmethod
    def listar_asignaciones(
        self,
        paginacion: ParametrosPaginacion,
        horario_id: Optional[int] = None,
        codigo_alumno: Optional[str] = None,
    ) -> Pagina[AsignacionWorkstation]:
        """Lista asignaciones paginadas."""
        pass

    @abstractmethod
    def listar_historial_alumno(
        self, paginacion: ParametrosPaginacion, codigo_alumno: str
    ) -> Pagina[AsignacionWorkstation]:
        """Historial paginado de asignaciones de un alumno."""
        pass
