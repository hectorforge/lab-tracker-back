import re
from datetime import date, datetime, timezone


def _ahora() -> datetime:
    """Fecha actual con zona horaria (requerida por SQLModel/SQLAlchemy 2.x)."""
    return datetime.now(timezone.utc)


PATRON_CODIGO = re.compile(r"^[A-Z0-9\-_]+$")
PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
