"""Contrato de la capa de aplicación para la gestión de usuarios internos."""

from abc import ABC, abstractmethod
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.application.dtos import (
    ActualizarUsuarioDTO,
    CrearUsuarioDTO,
    UsuarioDTO,
)


class AbstractUsuarioService(ABC):
    """Operaciones de negocio sobre cuentas y credenciales."""

    @abstractmethod
    def crear_usuario(self, data: CrearUsuarioDTO) -> UsuarioDTO:
        """Registra un usuario con contraseña hasheada.

        Args:
            data (CrearUsuarioDTO): Credenciales, datos personales, foto y rol.

        Returns:
            UsuarioDTO: Usuario creado (sin exponer el hash).

        Raises:
            NotFoundException: Si el rol indicado no existe.
            BadRequestException: Si el username o el correo ya están en uso.
        """
        pass

    @abstractmethod
    def listar_usuarios(
        self,
        paginacion: ParametrosPaginacion,
        rol_id: Optional[int] = None,
        solo_activos: bool = False,
        busqueda: Optional[str] = None,
    ) -> Pagina[UsuarioDTO]:
        """Lista usuarios paginados con filtros opcionales.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            rol_id (Optional[int]): Filtra por rol.
            solo_activos (bool): Excluye cuentas desactivadas.
            busqueda (Optional[str]): Búsqueda libre por username o nombre.

        Returns:
            Pagina[UsuarioDTO]: Página de usuarios.
        """
        pass

    @abstractmethod
    def obtener_usuario(self, usuario_id: int) -> UsuarioDTO:
        """Obtiene un usuario por su identificador.

        Args:
            usuario_id (int): Identificador del usuario.

        Returns:
            UsuarioDTO: Usuario encontrado.

        Raises:
            NotFoundException: Si el usuario no existe.
        """
        pass

    @abstractmethod
    def actualizar_usuario(
        self, usuario_id: int, data: ActualizarUsuarioDTO
    ) -> UsuarioDTO:
        """Actualiza un usuario, su foto y opcionalmente su contraseña.

        Args:
            usuario_id (int): Identificador del usuario a modificar.
            data (ActualizarUsuarioDTO): Campos a actualizar.

        Returns:
            UsuarioDTO: Usuario actualizado.

        Raises:
            NotFoundException: Si el usuario o el rol indicado no existen.
            BadRequestException: Si el username o correo pertenecen a otro usuario.
        """
        pass

    @abstractmethod
    def eliminar_usuario(self, usuario_id: int) -> None:
        """Elimina un usuario del sistema.

        Args:
            usuario_id (int): Identificador del usuario a eliminar.

        Returns:
            None

        Raises:
            NotFoundException: Si el usuario no existe.
        """
        pass
