"""Contrato de persistencia para la entidad :class:`Usuario`."""

from abc import ABC, abstractmethod
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import Usuario


class AbstractUsuarioRepository(ABC):
    """Puerto de salida para cuentas de acceso al sistema interno."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Usuario]:
        """Recupera un usuario por su clave primaria.

        Args:
            id (int): Identificador único de la fila en ``usuarios``.

        Returns:
            Optional[Usuario]: Entidad encontrada o ``None`` si no existe.
        """
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[Usuario]:
        """Busca un usuario por su nombre de acceso (login).

        Args:
            username (str): Nombre de usuario; se normaliza a minúsculas.

        Returns:
            Optional[Usuario]: Usuario encontrado o ``None``.
        """
        pass

    @abstractmethod
    def get_by_correo(self, correo: str) -> Optional[Usuario]:
        """Busca un usuario por su correo institucional.

        Args:
            correo (str): Correo a buscar; se normaliza a minúsculas.

        Returns:
            Optional[Usuario]: Usuario coincidente o ``None``.
        """
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        rol_id: Optional[int] = None,
        solo_activos: bool = False,
        busqueda: Optional[str] = None,
    ) -> Pagina[Usuario]:
        """Lista usuarios paginados con filtros opcionales.

        Args:
            paginacion (ParametrosPaginacion): Página, tamaño y totales.
            rol_id (Optional[int]): Filtra por rol asignado.
            solo_activos (bool): Excluye cuentas desactivadas.
            busqueda (Optional[str]): Búsqueda libre sobre username, nombres
                y apellidos.

        Returns:
            Pagina[Usuario]: Página de usuarios.
        """
        pass

    @abstractmethod
    def create(self, obj: Usuario) -> Usuario:
        """Persiste un usuario nuevo.

        Args:
            obj (Usuario): Entidad con ``password_hash`` ya calculado.

        Returns:
            Usuario: Usuario creado con su ``id`` asignado.
        """
        pass

    @abstractmethod
    def update(self, obj: Usuario) -> Usuario:
        """Actualiza un usuario existente.

        Args:
            obj (Usuario): Entidad modificada a persistir.

        Returns:
            Usuario: Usuario actualizado y refrescado.
        """
        pass

    @abstractmethod
    def delete(self, obj: Usuario) -> None:
        """Elimina un usuario del sistema.

        Args:
            obj (Usuario): Entidad a eliminar.

        Returns:
            None
        """
        pass
