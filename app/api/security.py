"""Dependencias de autenticación y autorización para los endpoints."""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.application.security import decodificar_token
from app.domain.entities import RolNombre, Usuario
from app.domain.exceptions import ForbiddenException, UnauthorizedException
from app.infrastructure.database import get_session
from app.infrastructure.repositories import UsuarioRepository

_esquema = HTTPBearer(
    scheme_name="Bearer", description="Token JWT obtenido en POST /auth/login", auto_error=False
)


def get_usuario_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(_esquema),
    session=Depends(get_session),
) -> Usuario:
    """Resuelve el usuario autenticado a partir del token Bearer.

    Args:
        credenciales: Credenciales HTTP del header ``Authorization``.
        session: Sesión de base de datos inyectada.

    Returns:
        Usuario: Usuario autenticado con su rol cargado.

    Raises:
        UnauthorizedException: Si falta el token, es inválido o la cuenta
            está desactivada.
    """
    if credenciales is None:
        raise UnauthorizedException("Se requiere un token de acceso Bearer.")

    payload = decodificar_token(credenciales.credentials)
    username = payload.get("sub")
    if not username:
        raise UnauthorizedException("El token no contiene un usuario válido.")

    usuario = UsuarioRepository(session).get_by_username(username)
    if not usuario or not usuario.activo:
        raise UnauthorizedException("La cuenta de usuario no existe o está inactiva.")
    return usuario


def requiere_roles(*roles: RolNombre):
    """Fábrica de dependencias que restringe el acceso a ciertos roles.

    Args:
        *roles: Roles autorizados a ejecutar el endpoint.

    Returns:
        Callable: Dependencia que devuelve el usuario autenticado o lanza
        ``ForbiddenException`` si su rol no está autorizado.
    """
    permitidos = {rol.value for rol in roles}

    def _verificar(usuario: Usuario = Depends(get_usuario_actual)) -> Usuario:
        if usuario.rol is None or usuario.rol.nombre not in permitidos:
            raise ForbiddenException(
                "Su rol no tiene permisos para realizar esta operación."
            )
        return usuario

    return _verificar


requiere_admin = requiere_roles(RolNombre.ADMINISTRADOR)
requiere_lectura = requiere_roles(
    RolNombre.ADMINISTRADOR,
    RolNombre.GESTION_LABORATORIOS,
    RolNombre.DOCENTE,
)
requiere_admin_o_gestion = requiere_roles(
    RolNombre.ADMINISTRADOR, RolNombre.GESTION_LABORATORIOS
)
requiere_admin_o_docente = requiere_roles(
    RolNombre.ADMINISTRADOR, RolNombre.DOCENTE
)
