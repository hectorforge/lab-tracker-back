from abc import ABC, abstractmethod
from typing import Optional

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import CategoriaTipoEquipo, Equipo


class AbstractEquipoRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Equipo]:
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        laboratorio_id: Optional[int] = None,
        workstation_id: Optional[int] = None,
        categoria: Optional[CategoriaTipoEquipo] = None,
    ) -> Pagina[Equipo]:
        """Lista equipos paginados aplicando filtros opcionales."""
        pass

    @abstractmethod
    def create(self, obj: Equipo) -> Equipo:
        pass

    @abstractmethod
    def update(self, obj: Equipo) -> Equipo:
        pass

    @abstractmethod
    def delete(self, obj: Equipo) -> None:
        pass

    @abstractmethod
    def get_by_codigo_patrimonial(self, codigo_patrimonial: str) -> Optional[Equipo]:
        pass
