from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models import (
    CategoriaTipoEquipo,
    EstadoEquipo,
    Moneda,
)

PATRON_PATRIMONIAL = r"^[A-Z0-9\-_]+$"


class _EquipoBaseDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    codigo_patrimonial: str = Field(min_length=2, max_length=50, pattern=PATRON_PATRIMONIAL)
    categoria: CategoriaTipoEquipo
    marca: str = Field(min_length=2, max_length=60)
    modelo: str = Field(min_length=1, max_length=80)
    numero_serie: Optional[str] = Field(default=None, max_length=80)
    caracteristicas: str = Field(min_length=2, max_length=500)
    estado: EstadoEquipo = EstadoEquipo.OPERATIVO
    laboratorio_id: int = Field(gt=0)
    workstation_id: Optional[int] = Field(default=None, gt=0)
    tipo_equipo_id: Optional[int] = Field(default=None, gt=0)
    costo_estimado: Optional[float] = Field(default=None, ge=0)
    costo_adquisicion: Optional[float] = Field(default=None, ge=0)
    moneda: Moneda = Moneda.PEN
    fecha_adquisicion: Optional[date] = None
    proveedor: Optional[str] = Field(default=None, max_length=120)
    garantia_hasta: Optional[date] = None
    observaciones: Optional[str] = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def validar_costos(self):
        if (
            self.garantia_hasta
            and self.fecha_adquisicion
            and self.garantia_hasta < self.fecha_adquisicion
        ):
            raise ValueError("La garantía no puede vencer antes de la adquisición.")
        return self


class CrearEquipoDTO(_EquipoBaseDTO):
    """DTO de entrada para registrar equipos."""


class ActualizarEquipoDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    codigo_patrimonial: Optional[str] = Field(default=None, min_length=2, max_length=50, pattern=PATRON_PATRIMONIAL)
    categoria: Optional[CategoriaTipoEquipo] = None
    marca: Optional[str] = Field(default=None, min_length=2, max_length=60)
    modelo: Optional[str] = Field(default=None, min_length=1, max_length=80)
    numero_serie: Optional[str] = Field(default=None, max_length=80)
    caracteristicas: Optional[str] = Field(default=None, min_length=2, max_length=500)
    estado: Optional[EstadoEquipo] = None
    laboratorio_id: Optional[int] = Field(default=None, gt=0)
    workstation_id: Optional[int] = Field(default=None, gt=0)
    tipo_equipo_id: Optional[int] = Field(default=None, gt=0)
    costo_estimado: Optional[float] = Field(default=None, ge=0)
    costo_adquisicion: Optional[float] = Field(default=None, ge=0)
    moneda: Optional[Moneda] = None
    fecha_adquisicion: Optional[date] = None
    proveedor: Optional[str] = Field(default=None, max_length=120)
    garantia_hasta: Optional[date] = None
    observaciones: Optional[str] = Field(default=None, max_length=500)


class EquipoDTO(_EquipoBaseDTO):
    id: int
