from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.domain.entities.comun import _ahora

if TYPE_CHECKING:
    from app.domain.entities.usuario import Usuario


class Rol(SQLModel, table=True):
    """Perfil de permisos asignado a los usuarios del sistema."""

    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, unique=True, index=True, nullable=False)
    descripcion: str = Field(max_length=250, nullable=False)
    es_activo: bool = Field(default=True, nullable=False)
    creado_en: datetime = Field(default_factory=_ahora, nullable=False)

    usuarios: List["Usuario"] = Relationship(back_populates="rol")

    def validar(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del rol es obligatorio.")
