"""Contrato de la capa de aplicación para licencias de software."""

from abc import ABC, abstractmethod
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.application.dtos import (
    ActualizarLicenciaDTO,
    CrearLicenciaDTO,
    LicenciaDTO,
)
from app.domain.entities import EstadoLicencia


class AbstractLicenciaService(ABC):
    """Operaciones de negocio sobre licencias por equipo o tipo de equipo."""

    @abstractmethod
    def crear_licencia(self, data: CrearLicenciaDTO) -> LicenciaDTO:
        """Registra una licencia validando equipo, catálogo y unicidad.

        Args:
            data (CrearLicenciaDTO): Código, tipo, vigencia, costo y
                asociaciones opcionales con equipo/tipo de equipo.

        Returns:
            LicenciaDTO: Licencia creada con sus fechas de auditoría.

        Raises:
            BadRequestException: Si el código ya existe, la categoría del
                tipo no coincide con la del equipo o la licencia vencida se
                declara activa.
            NotFoundException: Si el equipo o el tipo de equipo no existen.
        """
        pass

    @abstractmethod
    def listar_licencias(
        self,
        paginacion: ParametrosPaginacion,
        equipo_id: Optional[int] = None,
        estado: Optional[EstadoLicencia] = None,
    ) -> Pagina[LicenciaDTO]:
        """Lista licencias paginadas con filtros opcionales.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            equipo_id (Optional[int]): Filtra por equipo licenciado.
            estado (Optional[EstadoLicencia]): Filtra por estado de vigencia.

        Returns:
            Pagina[LicenciaDTO]: Página de licencias.
        """
        pass

    @abstractmethod
    def obtener_licencia(self, licencia_id: int) -> LicenciaDTO:
        """Obtiene una licencia por su identificador.

        Args:
            licencia_id (int): Identificador de la licencia.

        Returns:
            LicenciaDTO: Licencia encontrada.

        Raises:
            NotFoundException: Si la licencia no existe.
        """
        pass

    @abstractmethod
    def actualizar_licencia(
        self, licencia_id: int, data: ActualizarLicenciaDTO
    ) -> LicenciaDTO:
        """Actualiza una licencia existente.

        Args:
            licencia_id (int): Identificador de la licencia a modificar.
            data (ActualizarLicenciaDTO): Campos a actualizar.

        Returns:
            LicenciaDTO: Licencia actualizada.

        Raises:
            NotFoundException: Si la licencia, el equipo o el tipo no existen.
            BadRequestException: Si el código ya pertenece a otra licencia o
                las asociaciones son incoherentes.
        """
        pass

    @abstractmethod
    def eliminar_licencia(self, licencia_id: int) -> None:
        """Elimina una licencia del sistema.

        Args:
            licencia_id (int): Identificador de la licencia a eliminar.

        Returns:
            None

        Raises:
            NotFoundException: Si la licencia no existe.
        """
        pass
