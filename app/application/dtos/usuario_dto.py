from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class _UsuarioBaseDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9\-_]+$")
    nombres: str = Field(min_length=2, max_length=100)
    apellidos: str = Field(min_length=2, max_length=100)
    correo: Optional[str] = Field(default=None, max_length=150)
    url_imagen: Optional[str] = Field(default=None, max_length=500)
    activo: bool = True
    rol_id: int = Field(gt=0)

    @field_validator("username", mode="before")
    @classmethod
    def normalizar_username(cls, valor):
        return valor.strip().lower() if isinstance(valor, str) else valor

    @field_validator("correo")
    @classmethod
    def validar_correo(cls, valor: Optional[str]) -> Optional[str]:
        if valor and "@" not in valor:
            raise ValueError("El correo no tiene un formato válido.")
        return valor.lower() if valor else valor

    @field_validator("url_imagen")
    @classmethod
    def validar_url_imagen(cls, valor: Optional[str]) -> Optional[str]:
        if valor and not valor.startswith(("http://", "https://")):
            raise ValueError("La URL de la imagen debe empezar con http:// o https://.")
        return valor


class CrearUsuarioDTO(_UsuarioBaseDTO):
    password: str = Field(min_length=8, max_length=100)


class ActualizarUsuarioDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    username: Optional[str] = Field(default=None, min_length=3, max_length=50, pattern=r"^[A-Za-z0-9\-_]+$")
    nombres: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellidos: Optional[str] = Field(default=None, min_length=2, max_length=100)
    correo: Optional[str] = Field(default=None, max_length=150)
    password: Optional[str] = Field(default=None, min_length=8, max_length=100)
    url_imagen: Optional[str] = Field(default=None, max_length=500)
    activo: Optional[bool] = None
    rol_id: Optional[int] = Field(default=None, gt=0)

    @field_validator("username", mode="before")
    @classmethod
    def normalizar_username(cls, valor):
        return valor.strip().lower() if isinstance(valor, str) else valor

    @field_validator("url_imagen")
    @classmethod
    def validar_url_imagen(cls, valor: Optional[str]) -> Optional[str]:
        if valor and not valor.startswith(("http://", "https://")):
            raise ValueError("La URL de la imagen debe empezar con http:// o https://.")
        return valor


class UsuarioDTO(_UsuarioBaseDTO):
    id: int
    creado_en: datetime
    actualizado_en: datetime
