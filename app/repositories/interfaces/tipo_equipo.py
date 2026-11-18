from abc import ABC, abstractmethod
from typing import Optional

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import CategoriaTipoEquipo, TipoEquipo


class AbstractTipoEquipoRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[TipoEquipo]:
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        solo_activos: bool = False,
        categoria: Optional[CategoriaTipoEquipo] = None,
    ) -> Pagina[TipoEquipo]:
        """Lista el catálogo paginado desde el repositorio."""
        pass

    @abstractmethod
    def create(self, obj: TipoEquipo) -> TipoEquipo:
        pass

    @abstractmethod
    def update(self, obj: TipoEquipo) -> TipoEquipo:
        pass

    @abstractmethod
    def delete(self, obj: TipoEquipo) -> None:
        pass

    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[TipoEquipo]:
        pass
