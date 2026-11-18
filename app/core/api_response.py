from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar
from uuid import uuid4

from pydantic import BaseModel, Field

from app.models.comun import _ahora

T = TypeVar("T")


class DetalleError(BaseModel):
    codigo: str
    mensaje: str
    campo: Optional[str] = None


class ApiResponse(BaseModel, Generic[T]):
    """Envoltorio estándar para todas las respuestas del backend."""

    isSuccess: bool
    status: int
    message: str
    details: Optional[T] = None
    errors: List[DetalleError] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=_ahora)
    traceId: str = Field(default_factory=lambda: str(uuid4()))
    path: Optional[str] = None

    @classmethod
    def ok(
        cls,
        data: Any = None,
        message: str = "Operación completada correctamente.",
        status: int = 200,
        path: Optional[str] = None,
    ) -> "ApiResponse[T]":
        return cls(
            isSuccess=True,
            status=status,
            message=message,
            details=data,
            path=path,
        )

    @classmethod
    def fail(
        cls,
        message: str,
        status: int = 400,
        errors: Optional[List[dict]] = None,
        details: Any = None,
        path: Optional[str] = None,
    ) -> "ApiResponse[T]":
        return cls(
            isSuccess=False,
            status=status,
            message=message,
            details=details,
            errors=[DetalleError(**e) for e in (errors or [])],
            path=path,
        )
