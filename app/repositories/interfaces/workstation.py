from abc import ABC, abstractmethod
from typing import Optional

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import Workstation


class AbstractWorkstationRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Workstation]:
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        laboratorio_id: Optional[int] = None,
    ) -> Pagina[Workstation]:
        """Lista workstations paginadas, opcionalmente por laboratorio."""
        pass

    @abstractmethod
    def create(self, obj: Workstation) -> Workstation:
        pass

    @abstractmethod
    def update(self, obj: Workstation) -> Workstation:
        pass

    @abstractmethod
    def delete(self, obj: Workstation) -> None:
        pass

    @abstractmethod
    def get_by_codigo_y_laboratorio(
        self, codigo: str, laboratorio_id: int
    ) -> Optional[Workstation]:
        pass
