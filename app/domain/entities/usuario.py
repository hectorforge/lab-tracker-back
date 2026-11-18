from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.domain.entities.comun import PATRON_CORREO, PATRON_CODIGO, _ahora

if TYPE_CHECKING:
    from app.domain.entities.rol import Rol


class Usuario(SQLModel, table=True):
    """Cuenta interna con la que se autentica el personal del laboratorio."""

    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, index=True, nullable=False)
    nombres: str = Field(max_length=100, nullable=False)
    apellidos: str = Field(max_length=100, nullable=False)
    correo: Optional[str] = Field(default=None, max_length=150, index=True)
    password_hash: str = Field(max_length=255, nullable=False)
    url_imagen: Optional[str] = Field(default=None, max_length=500)
    activo: bool = Field(default=True, nullable=False)
    rol_id: int = Field(foreign_key="roles.id", nullable=False)
    creado_en: datetime = Field(default_factory=_ahora, nullable=False)
    actualizado_en: datetime = Field(default_factory=_ahora, nullable=False)

    rol: Optional["Rol"] = Relationship(back_populates="usuarios")

    def validar(self) -> None:
        if not PATRON_CODIGO.match(self.username.strip().upper()):
            raise ValueError("El username solo admite letras, números, - y _.")
        if self.correo and not PATRON_CORREO.match(self.correo.strip().lower()):
            raise ValueError("El correo no tiene un formato válido.")
