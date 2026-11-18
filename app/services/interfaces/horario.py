from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import AsignacionWorkstation, EstadoHorario, Horario
from app.schemas.lab_schemas import AsignacionCreate, HorarioCreate


class AbstractHorarioService(ABC):
    @abstractmethod
    def crear_horario(self, data: HorarioCreate) -> Horario:
        pass

    @abstractmethod
    def listar_horarios(
        self,
        paginacion: ParametrosPaginacion,
        laboratorio_id: Optional[int] = None,
        fecha: Optional[date] = None,
        estado: Optional[EstadoHorario] = None,
    ) -> Pagina[Horario]:
        pass

    @abstractmethod
    def obtener_horario(self, horario_id: int) -> Horario:
        pass

    @abstractmethod
    def iniciar_turno(self, horario_id: int) -> Horario:
        pass

    @abstractmethod
    def finalizar_turno(self, horario_id: int) -> Horario:
        pass

    @abstractmethod
    def cancelar_turno(self, horario_id: int) -> Horario:
        pass

    @abstractmethod
    def asignar_workstation(self, horario_id: int, data: AsignacionCreate):
        pass

    @abstractmethod
    def listar_asignaciones_turno(
        self, paginacion: ParametrosPaginacion, horario_id: int
    ) -> Pagina[AsignacionWorkstation]:
        pass

    @abstractmethod
    def consultar_historial_alumno(
        self, paginacion: ParametrosPaginacion, codigo_alumno: str
    ) -> Pagina[AsignacionWorkstation]:
        pass
