from abc import ABC, abstractmethod
from typing import Optional

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import EstadoLicencia, Licencia


class AbstractLicenciaRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Licencia]:
        pass

    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[Licencia]:
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        equipo_id: Optional[int] = None,
        estado: Optional[EstadoLicencia] = None,
    ) -> Pagina[Licencia]:
        """Lista licencias paginadas desde el repositorio."""
        pass

    @abstractmethod
    def create(self, obj: Licencia) -> Licencia:
        pass

    @abstractmethod
    def update(self, obj: Licencia) -> Licencia:
        pass

    @abstractmethod
    def delete(self, obj: Licencia) -> None:
        pass
