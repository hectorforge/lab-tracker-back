from abc import ABC, abstractmethod
from typing import Optional

from app.core.pagination import Pagina, ParametrosPaginacion
from app.dtos import ActualizarEquipoDTO, CrearEquipoDTO, EquipoDTO
from app.models import CategoriaTipoEquipo


class AbstractEquipoService(ABC):
    @abstractmethod
    def registrar_equipo(self, data: CrearEquipoDTO) -> EquipoDTO:
        pass

    @abstractmethod
    def listar_equipos(self, paginacion: ParametrosPaginacion) -> Pagina[EquipoDTO]:
        pass

    @abstractmethod
    def listar_por_laboratorio(
        self,
        paginacion: ParametrosPaginacion,
        lab_id: int,
        categoria: Optional[CategoriaTipoEquipo] = None,
    ) -> Pagina[EquipoDTO]:
        pass

    @abstractmethod
    def listar_por_workstation(
        self, paginacion: ParametrosPaginacion, workstation_id: int
    ) -> Pagina[EquipoDTO]:
        pass

    @abstractmethod
    def obtener_equipo(self, equipo_id: int) -> EquipoDTO:
        pass

    @abstractmethod
    def actualizar_equipo(self, equipo_id: int, data: ActualizarEquipoDTO) -> EquipoDTO:
        pass

    @abstractmethod
    def eliminar_equipo(self, equipo_id: int) -> None:
        pass
