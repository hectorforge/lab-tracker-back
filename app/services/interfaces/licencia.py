from abc import ABC, abstractmethod
from typing import Optional

from app.core.pagination import Pagina, ParametrosPaginacion
from app.dtos import ActualizarLicenciaDTO, CrearLicenciaDTO, LicenciaDTO
from app.models import EstadoLicencia


class AbstractLicenciaService(ABC):
    @abstractmethod
    def crear_licencia(self, data: CrearLicenciaDTO) -> LicenciaDTO:
        pass

    @abstractmethod
    def listar_licencias(
        self,
        paginacion: ParametrosPaginacion,
        equipo_id: Optional[int] = None,
        estado: Optional[EstadoLicencia] = None,
    ) -> Pagina[LicenciaDTO]:
        pass

    @abstractmethod
    def obtener_licencia(self, licencia_id: int) -> LicenciaDTO:
        pass

    @abstractmethod
    def actualizar_licencia(
        self, licencia_id: int, data: ActualizarLicenciaDTO
    ) -> LicenciaDTO:
        pass

    @abstractmethod
    def eliminar_licencia(self, licencia_id: int) -> None:
        pass
