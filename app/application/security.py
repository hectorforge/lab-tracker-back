"""Generación y validación de tokens JWT (capa de aplicación)."""

from datetime import datetime, timedelta, timezone

import jwt

from app.domain.exceptions import UnauthorizedException
from app.infrastructure.database.config import settings


def crear_token(username: str, rol: str) -> tuple[str, int]:
    """Genera un token JWT para el usuario autenticado.

    Args:
        username (str): Identificador del usuario (claim ``sub``).
        rol (str): Nombre del rol (claim ``rol``).

    Returns:
        tuple[str, int]: Token codificado y segundos de vigencia.
    """
    vigencia = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    ahora = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "rol": rol,
        "iat": ahora,
        "exp": ahora + vigencia,
    }
    token = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return token, int(vigencia.total_seconds())


def decodificar_token(token: str) -> dict:
    """Valida firma y vigencia de un token.

    Args:
        token (str): Token JWT recibido en el header ``Authorization``.

    Returns:
        dict: Payload decodificado.

    Raises:
        UnauthorizedException: Si el token es inválido o está expirado.
    """
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        raise UnauthorizedException("Token de acceso inválido o expirado.")
