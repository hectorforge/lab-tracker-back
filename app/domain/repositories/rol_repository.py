"""Contrato de persistencia para la entidad :class:`Rol`."""

from abc import ABC, abstractmethod
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import Rol, RolNombre


class AbstractRolRepository(ABC):
    """Puerto de salida para los perfiles de permisos del sistema."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Rol]:
        """Recupera un rol por su clave primaria.

        Args:
            id (int): Identificador único de la fila en ``roles``.

        Returns:
            Optional[Rol]: Entidad encontrada o ``None`` si no existe.
        """
        pass

    @abstractmethod
    def get_by_nombre(self, nombre: str | RolNombre) -> Optional[Rol]:
        """Busca un rol por su nombre normalizado.

        Args:
            nombre (str | RolNombre): Nombre del rol (acepta enum o cadena).

        Returns:
            Optional[Rol]: Rol coincidente o ``None``.
        """
        pass

    @abstractmethod
    def listar(
        self, paginacion: ParametrosPaginacion, solo_activos: bool = False
    ) -> Pagina[Rol]:
        """Lista roles paginados.

        Args:
            paginacion (ParametrosPaginacion): Página, tamaño y totales.
            solo_activos (bool): Excluye roles desactivados.

        Returns:
            Pagina[Rol]: Página de roles.
        """
        pass

    @abstractmethod
    def create(self, obj: Rol) -> Rol:
        """Persiste un rol nuevo.

        Args:
            obj (Rol): Entidad validada por la capa de aplicación.

        Returns:
            Rol: Rol creado con su ``id`` asignado.
        """
        pass

    @abstractmethod
    def update(self, obj: Rol) -> Rol:
        """Actualiza un rol existente.

        Args:
            obj (Rol): Entidad modificada a persistir.

        Returns:
            Rol: Rol actualizado y refrescado.
        """
        pass

    @abstractmethod
    def delete(self, obj: Rol) -> None:
        """Elimina un rol del sistema.

        Args:
            obj (Rol): Entidad a eliminar. La capa de aplicación valida que
                no tenga usuarios asignados.

        Returns:
            None
        """
        pass
