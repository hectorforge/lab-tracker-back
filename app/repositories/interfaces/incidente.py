from abc import ABC, abstractmethod
from typing import Optional

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import Incidente


class AbstractIncidenteRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Incidente]:
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        solo_pendientes: bool = False,
        equipo_id: Optional[int] = None,
        workstation_id: Optional[int] = None,
    ) -> Pagina[Incidente]:
        """Lista incidentes paginados y filtrados."""
        pass

    @abstractmethod
    def create(self, obj: Incidente) -> Incidente:
        pass

    @abstractmethod
    def update(self, obj: Incidente) -> Incidente:
        pass

    @abstractmethod
    def count_abiertos_por_equipo(self, equipo_id: int) -> int:
        pass

    @abstractmethod
    def count_abiertos_por_workstation(self, workstation_id: int) -> int:
        pass
