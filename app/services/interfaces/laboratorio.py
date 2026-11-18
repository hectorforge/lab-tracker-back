from abc import ABC, abstractmethod

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import Laboratorio
from app.schemas.lab_schemas import LaboratorioCreate, LaboratorioUpdate


class AbstractLaboratorioService(ABC):
    @abstractmethod
    def crear_laboratorio(self, data: LaboratorioCreate) -> Laboratorio:
        pass

    @abstractmethod
    def listar_laboratorios(
        self, paginacion: ParametrosPaginacion, solo_disponibles: bool = False
    ) -> Pagina[Laboratorio]:
        """Lista laboratorios paginados desde el repositorio."""
        pass

    @abstractmethod
    def obtener_laboratorio(self, lab_id: int) -> Laboratorio:
        pass

    @abstractmethod
    def actualizar_laboratorio(
        self, lab_id: int, data: LaboratorioUpdate
    ) -> Laboratorio:
        pass

    @abstractmethod
    def eliminar_laboratorio(self, lab_id: int) -> None:
        pass
