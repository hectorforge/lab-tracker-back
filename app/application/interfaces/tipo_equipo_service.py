"""Contrato de la capa de aplicación para el catálogo de tipos de equipo."""

from abc import ABC, abstractmethod
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.application.dtos import (
    ActualizarTipoEquipoDTO,
    CrearTipoEquipoDTO,
    TipoEquipoDTO,
)
from app.domain.entities import CategoriaTipoEquipo


class AbstractTipoEquipoService(ABC):
    """Operaciones de negocio sobre el catálogo institucional de equipos."""

    @abstractmethod
    def crear_tipo_equipo(self, data: CrearTipoEquipoDTO) -> TipoEquipoDTO:
        """Registra un tipo de equipo validando la unicidad de su código.

        Args:
            data (CrearTipoEquipoDTO): Categoría genérica, descripción, vida
                útil, costos y requisitos de licencia/mantenimiento.

        Returns:
            TipoEquipoDTO: Tipo creado con sus fechas de auditoría.

        Raises:
            BadRequestException: Si el código del catálogo ya existe.
        """
        pass

    @abstractmethod
    def listar_tipos_equipo(
        self,
        paginacion: ParametrosPaginacion,
        solo_activos: bool = False,
        categoria: Optional[CategoriaTipoEquipo] = None,
    ) -> Pagina[TipoEquipoDTO]:
        """Lista el catálogo paginado con filtros opcionales.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            solo_activos (bool): Excluye tipos inactivos o descontinuados.
            categoria (Optional[CategoriaTipoEquipo]): Filtra por etiqueta genérica.

        Returns:
            Pagina[TipoEquipoDTO]: Página de tipos de equipo.
        """
        pass

    @abstractmethod
    def obtener_tipo_equipo(self, tipo_equipo_id: int) -> TipoEquipoDTO:
        """Obtiene un tipo de equipo por su identificador.

        Args:
            tipo_equipo_id (int): Identificador del tipo de equipo.

        Returns:
            TipoEquipoDTO: Tipo encontrado.

        Raises:
            NotFoundException: Si el tipo no existe.
        """
        pass

    @abstractmethod
    def actualizar_tipo_equipo(
        self, tipo_equipo_id: int, data: ActualizarTipoEquipoDTO
    ) -> TipoEquipoDTO:
        """Actualiza un tipo de equipo del catálogo.

        Args:
            tipo_equipo_id (int): Identificador del tipo a modificar.
            data (ActualizarTipoEquipoDTO): Campos a actualizar.

        Returns:
            TipoEquipoDTO: Tipo actualizado.

        Raises:
            NotFoundException: Si el tipo no existe.
            BadRequestException: Si el nuevo código ya pertenece a otro tipo.
        """
        pass

    @abstractmethod
    def eliminar_tipo_equipo(self, tipo_equipo_id: int) -> None:
        """Elimina un tipo de equipo sin equipos físicos asociados.

        Args:
            tipo_equipo_id (int): Identificador del tipo a eliminar.

        Returns:
            None

        Raises:
            NotFoundException: Si el tipo no existe.
            ConflictException: Si todavía hay equipos que referencian el tipo.
        """
        pass
