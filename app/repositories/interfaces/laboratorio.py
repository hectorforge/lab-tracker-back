from abc import ABC, abstractmethod
from typing import Optional

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import Laboratorio


class AbstractLaboratorioRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Laboratorio]:
        """Obtiene un laboratorio por su identificador."""
        pass

    @abstractmethod
    def listar(
        self, paginacion: ParametrosPaginacion, solo_disponibles: bool = False
    ) -> Pagina[Laboratorio]:
        """Lista laboratorios paginados en el repositorio."""
        pass

    @abstractmethod
    def create(self, obj: Laboratorio) -> Laboratorio:
        pass

    @abstractmethod
    def update(self, obj: Laboratorio) -> Laboratorio:
        pass

    @abstractmethod
    def delete(self, obj: Laboratorio) -> None:
        pass

    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[Laboratorio]:
        pass
