from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.entities import (
    CategoriaTipoEquipo,
    EstadoTipoEquipo,
    Moneda,
)

PATRON_CODIGO = r"^[A-Z0-9\-_]+$"


class _TipoEquipoBaseDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    codigo: str = Field(min_length=2, max_length=20, pattern=PATRON_CODIGO)
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: str = Field(min_length=2, max_length=500)
    categoria: CategoriaTipoEquipo
    especificaciones_minimas: Optional[str] = Field(default=None, max_length=500)
    vida_util_meses: Optional[int] = Field(default=None, ge=1, le=600)
    requiere_mantenimiento: bool = False
    requiere_licencia: bool = False
    costo_referencial: Optional[float] = Field(default=None, ge=0)
    moneda: Moneda = Moneda.PEN
    estado: EstadoTipoEquipo = EstadoTipoEquipo.ACTIVO

    @field_validator("codigo", mode="before")
    @classmethod
    def normalizar_codigo(cls, valor):
        return valor.strip().upper() if isinstance(valor, str) else valor


class CrearTipoEquipoDTO(_TipoEquipoBaseDTO):
    """DTO de entrada para crear tipos de equipo."""


class ActualizarTipoEquipoDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    codigo: Optional[str] = Field(default=None, min_length=2, max_length=20, pattern=PATRON_CODIGO)
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(default=None, min_length=2, max_length=500)
    categoria: Optional[CategoriaTipoEquipo] = None
    especificaciones_minimas: Optional[str] = Field(default=None, max_length=500)
    vida_util_meses: Optional[int] = Field(default=None, ge=1, le=600)
    requiere_mantenimiento: Optional[bool] = None
    requiere_licencia: Optional[bool] = None
    costo_referencial: Optional[float] = Field(default=None, ge=0)
    moneda: Optional[Moneda] = None
    estado: Optional[EstadoTipoEquipo] = None

    @field_validator("codigo", mode="before")
    @classmethod
    def normalizar_codigo(cls, valor):
        return valor.strip().upper() if isinstance(valor, str) else valor if isinstance(valor, str) else valor


class TipoEquipoDTO(_TipoEquipoBaseDTO):
    id: int
    creado_en: datetime
    actualizado_en: datetime
