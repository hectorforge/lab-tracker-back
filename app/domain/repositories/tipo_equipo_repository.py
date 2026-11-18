"""Contrato de persistencia para el catálogo :class:`TipoEquipo`."""

from abc import ABC, abstractmethod
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import CategoriaTipoEquipo, TipoEquipo


class AbstractTipoEquipoRepository(ABC):
    """Puerto de salida para el catálogo institucional de tipos de equipo."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[TipoEquipo]:
        """Recupera un tipo de equipo por su clave primaria.

        Args:
            id (int): Identificador único de la fila en ``tipos_equipo``.

        Returns:
            Optional[TipoEquipo]: Entidad encontrada o ``None`` si no existe.
        """
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        solo_activos: bool = False,
        categoria: Optional[CategoriaTipoEquipo] = None,
    ) -> Pagina[TipoEquipo]:
        """Lista el catálogo paginado con filtros opcionales.

        Args:
            paginacion (ParametrosPaginacion): Página, tamaño y cálculo de totales.
            solo_activos (bool): Si es ``True``, excluye tipos inactivos o
                descontinuados.
            categoria (Optional[CategoriaTipoEquipo]): Filtra por etiqueta genérica.

        Returns:
            Pagina[TipoEquipo]: Página de tipos de equipo ordenada por nombre.
        """
        pass

    @abstractmethod
    def create(self, obj: TipoEquipo) -> TipoEquipo:
        """Persiste un tipo de equipo nuevo en el catálogo.

        Args:
            obj (TipoEquipo): Entidad validada por la capa de aplicación.

        Returns:
            TipoEquipo: Entidad creada con su ``id`` asignado.
        """
        pass

    @abstractmethod
    def update(self, obj: TipoEquipo) -> TipoEquipo:
        """Actualiza un tipo de equipo existente.

        Args:
            obj (TipoEquipo): Entidad modificada a persistir.

        Returns:
            TipoEquipo: Entidad actualizada y refrescada.
        """
        pass

    @abstractmethod
    def delete(self, obj: TipoEquipo) -> None:
        """Elimina un tipo de equipo del catálogo.

        Args:
            obj (TipoEquipo): Entidad a eliminar. La capa de aplicación debe
                verificar previamente que no tenga equipos asociados.

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[TipoEquipo]:
        """Busca un tipo de equipo por su código único.

        Args:
            codigo (str): Código del catálogo; se normaliza a mayúsculas.

        Returns:
            Optional[TipoEquipo]: Tipo encontrado o ``None``.
        """
        pass
