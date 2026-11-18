"""Utilidades criptográficas de dominio para credenciales."""

import bcrypt


def hash_password(password: str) -> str:
    """Genera un hash bcrypt de la contraseña indicada.

    Args:
        password (str): Contraseña en texto plano.

    Returns:
        str: Hash listo para almacenar en ``usuarios.password_hash``.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Compara una contraseña con su hash almacenado.

    Args:
        password (str): Contraseña recibida en el login.
        password_hash (str): Hash guardado en la base de datos.

    Returns:
        bool: ``True`` si coinciden, ``False`` en caso contrario.
    """
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"), password_hash.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False
