from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.domain.entities import EstadoLicencia, Moneda, TipoLicencia

PATRON_CODIGO = r"^[A-Z0-9\-_]+$"


class _LicenciaBaseDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    codigo: str = Field(min_length=2, max_length=50, pattern=PATRON_CODIGO)
    nombre: str = Field(min_length=2, max_length=120)
    tipo: TipoLicencia = TipoLicencia.PERPETUA
    clave_producto: Optional[str] = Field(default=None, max_length=120)
    fabricante: Optional[str] = Field(default=None, max_length=100)
    cantidad_usuarios: int = Field(default=1, ge=1)
    fecha_adquisicion: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    costo: Optional[float] = Field(default=None, ge=0)
    moneda: Moneda = Moneda.PEN
    estado: EstadoLicencia = EstadoLicencia.ACTIVA
    equipo_id: Optional[int] = Field(default=None, gt=0)
    tipo_equipo_id: Optional[int] = Field(default=None, gt=0)
    observaciones: Optional[str] = Field(default=None, max_length=500)

    @field_validator("codigo", mode="before")
    @classmethod
    def normalizar_codigo(cls, valor):
        return valor.strip().upper() if isinstance(valor, str) else valor

    @model_validator(mode="after")
    def validar_vigencia(self):
        if (
            self.fecha_vencimiento
            and self.fecha_adquisicion
            and self.fecha_vencimiento < self.fecha_adquisicion
        ):
            raise ValueError("La licencia no puede vencer antes de su adquisición.")
        if (
            self.estado == EstadoLicencia.ACTIVA
            and self.fecha_vencimiento
            and self.fecha_vencimiento < date.today()
        ):
            raise ValueError("Una licencia vencida no puede permanecer activa.")
        return self


class CrearLicenciaDTO(_LicenciaBaseDTO):
    """DTO de entrada para crear licencias."""


class ActualizarLicenciaDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    codigo: Optional[str] = Field(default=None, min_length=2, max_length=50, pattern=PATRON_CODIGO)
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=120)
    tipo: Optional[TipoLicencia] = None
    clave_producto: Optional[str] = Field(default=None, max_length=120)
    fabricante: Optional[str] = Field(default=None, max_length=100)
    cantidad_usuarios: Optional[int] = Field(default=None, ge=1)
    fecha_adquisicion: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    costo: Optional[float] = Field(default=None, ge=0)
    moneda: Optional[Moneda] = None
    estado: Optional[EstadoLicencia] = None
    equipo_id: Optional[int] = Field(default=None, gt=0)
    tipo_equipo_id: Optional[int] = Field(default=None, gt=0)
    observaciones: Optional[str] = Field(default=None, max_length=500)

    @field_validator("codigo", mode="before")
    @classmethod
    def normalizar_codigo(cls, valor):
        return valor.strip().upper() if isinstance(valor, str) else valor if isinstance(valor, str) else valor


class LicenciaDTO(_LicenciaBaseDTO):
    id: int
    creado_en: datetime
    actualizado_en: datetime
