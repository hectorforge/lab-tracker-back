from abc import ABC, abstractmethod

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import Workstation
from app.schemas.lab_schemas import WorkstationCreate, WorkstationUpdate


class AbstractWorkstationService(ABC):
    @abstractmethod
    def crear_workstation(self, data: WorkstationCreate) -> Workstation:
        pass

    @abstractmethod
    def listar_por_laboratorio(
        self, paginacion: ParametrosPaginacion, lab_id: int
    ) -> Pagina[Workstation]:
        pass

    @abstractmethod
    def obtener_workstation(self, workstation_id: int) -> Workstation:
        pass

    @abstractmethod
    def actualizar_workstation(
        self, workstation_id: int, data: WorkstationUpdate
    ) -> Workstation:
        pass

    @abstractmethod
    def eliminar_workstation(self, workstation_id: int) -> None:
        pass
