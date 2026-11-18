from abc import ABC, abstractmethod

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import Incidente
from app.schemas.lab_schemas import IncidenteCreate, IncidenteUpdateEstado


class AbstractIncidenteService(ABC):
    @abstractmethod
    def reportar_incidente(self, data: IncidenteCreate) -> Incidente:
        pass

    @abstractmethod
    def listar_incidentes(
        self, paginacion: ParametrosPaginacion, solo_pendientes: bool = False
    ) -> Pagina[Incidente]:
        pass

    @abstractmethod
    def listar_por_equipo(
        self, paginacion: ParametrosPaginacion, equipo_id: int
    ) -> Pagina[Incidente]:
        pass

    @abstractmethod
    def listar_por_workstation(
        self, paginacion: ParametrosPaginacion, workstation_id: int
    ) -> Pagina[Incidente]:
        pass

    @abstractmethod
    def actualizar_estado(
        self, incidente_id: int, data: IncidenteUpdateEstado
    ) -> Incidente:
        pass
