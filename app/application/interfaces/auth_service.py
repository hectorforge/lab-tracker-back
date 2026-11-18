"""Contrato de la capa de aplicación para autenticación."""

from abc import ABC, abstractmethod

from app.application.dtos import LoginDTO, TokenDTO, UsuarioDTO


class AbstractAuthService(ABC):
    """Operaciones de login y consulta del usuario autenticado."""

    @abstractmethod
    def login(self, data: LoginDTO) -> TokenDTO:
        """Valida credenciales y emite un token JWT.

        Args:
            data (LoginDTO): Username y contraseña en texto plano.

        Returns:
            TokenDTO: Token de acceso, tipo, vigencia, usuario y rol.

        Raises:
            UnauthorizedException: Si el usuario no existe, la contraseña
                es incorrecta o la cuenta está desactivada.
        """
        pass

    @abstractmethod
    def obtener_usuario_actual(self, username: str) -> UsuarioDTO:
        """Devuelve los datos del usuario dueño del token.

        Args:
            username (str): Nombre de usuario extraído del token JWT.

        Returns:
            UsuarioDTO: Usuario autenticado.

        Raises:
            UnauthorizedException: Si la cuenta ya no existe o está inactiva.
        """
        pass
