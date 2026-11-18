from abc import ABC, abstractmethod
from typing import Optional

from app.core.pagination import Pagina, ParametrosPaginacion
from app.dtos import (
    ActualizarTipoEquipoDTO,
    CrearTipoEquipoDTO,
    TipoEquipoDTO,
)
from app.models import CategoriaTipoEquipo


class AbstractTipoEquipoService(ABC):
    @abstractmethod
    def crear_tipo_equipo(self, data: CrearTipoEquipoDTO) -> TipoEquipoDTO:
        pass

    @abstractmethod
    def listar_tipos_equipo(
        self,
        paginacion: ParametrosPaginacion,
        solo_activos: bool = False,
        categoria: Optional[CategoriaTipoEquipo] = None,
    ) -> Pagina[TipoEquipoDTO]:
        pass

    @abstractmethod
    def obtener_tipo_equipo(self, tipo_equipo_id: int) -> TipoEquipoDTO:
        pass

    @abstractmethod
    def actualizar_tipo_equipo(
        self, tipo_equipo_id: int, data: ActualizarTipoEquipoDTO
    ) -> TipoEquipoDTO:
        pass

    @abstractmethod
    def eliminar_tipo_equipo(self, tipo_equipo_id: int) -> None:
        pass
