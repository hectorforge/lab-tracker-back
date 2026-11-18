"""Contrato de la capa de aplicación para la gestión de roles."""

from abc import ABC, abstractmethod

from app.api.pagination import Pagina, ParametrosPaginacion
from app.application.dtos import ActualizarRolDTO, CrearRolDTO, RolDTO


class AbstractRolService(ABC):
    """Operaciones de negocio sobre los perfiles de permisos."""

    @abstractmethod
    def crear_rol(self, data: CrearRolDTO) -> RolDTO:
        """Registra un rol validando que su nombre no esté duplicado.

        Args:
            data (CrearRolDTO): Nombre del catálogo, descripción y estado.

        Returns:
            RolDTO: Rol creado.

        Raises:
            BadRequestException: Si el nombre ya existe.
        """
        pass

    @abstractmethod
    def listar_roles(
        self, paginacion: ParametrosPaginacion, solo_activos: bool = False
    ) -> Pagina[RolDTO]:
        """Lista roles paginados.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            solo_activos (bool): Excluye roles desactivados.

        Returns:
            Pagina[RolDTO]: Página de roles.
        """
        pass

    @abstractmethod
    def obtener_rol(self, rol_id: int) -> RolDTO:
        """Obtiene un rol por su identificador.

        Args:
            rol_id (int): Identificador del rol.

        Returns:
            RolDTO: Rol encontrado.

        Raises:
            NotFoundException: Si el rol no existe.
        """
        pass

    @abstractmethod
    def actualizar_rol(self, rol_id: int, data: ActualizarRolDTO) -> RolDTO:
        """Actualiza un rol existente.

        Args:
            rol_id (int): Identificador del rol a modificar.
            data (ActualizarRolDTO): Campos a actualizar.

        Returns:
            RolDTO: Rol actualizado.

        Raises:
            NotFoundException: Si el rol no existe.
            BadRequestException: Si el nuevo nombre ya está en uso.
        """
        pass

    @abstractmethod
    def eliminar_rol(self, rol_id: int) -> None:
        """Elimina un rol sin usuarios asignados.

        Args:
            rol_id (int): Identificador del rol a eliminar.

        Returns:
            None

        Raises:
            NotFoundException: Si el rol no existe.
            ConflictException: Si aún hay usuarios con ese rol.
        """
        pass
