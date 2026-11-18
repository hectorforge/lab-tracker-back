from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.entities import RolNombre


class _RolBaseDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    nombre: str = Field(min_length=3, max_length=50)
    descripcion: str = Field(min_length=3, max_length=250)
    es_activo: bool = True

    @field_validator("nombre", mode="before")
    @classmethod
    def normalizar_nombre(cls, valor):
        return valor.strip().lower() if isinstance(valor, str) else valor

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor: str) -> str:
        nombres_validos = {rol.value for rol in RolNombre}
        if valor not in nombres_validos:
            raise ValueError(
                "El rol debe ser uno de: " + ", ".join(sorted(nombres_validos))
            )
        return valor


class CrearRolDTO(_RolBaseDTO):
    """DTO de entrada para crear un rol."""


class ActualizarRolDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    nombre: Optional[str] = Field(default=None, min_length=3, max_length=50)
    descripcion: Optional[str] = Field(default=None, min_length=3, max_length=250)
    es_activo: Optional[bool] = None

    @field_validator("nombre", mode="before")
    @classmethod
    def normalizar_nombre(cls, valor):
        return valor.strip().lower() if isinstance(valor, str) else valor


class RolDTO(_RolBaseDTO):
    id: int
    creado_en: datetime
