from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.entities import EstadoWorkstation


class _WorkstationBaseDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    codigo: str = Field(min_length=2, max_length=30)
    ubicacion_interna: str = Field(min_length=2, max_length=100)
    estado: EstadoWorkstation = EstadoWorkstation.DISPONIBLE
    laboratorio_id: int = Field(gt=0)

    @field_validator("codigo", mode="before")
    @classmethod
    def normalizar_codigo(cls, valor):
        return valor.strip().upper() if isinstance(valor, str) else valor


class CrearWorkstationDTO(_WorkstationBaseDTO):
    """DTO de entrada para registrar workstations."""


class ActualizarWorkstationDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    codigo: str | None = Field(default=None, min_length=2, max_length=30)
    ubicacion_interna: str | None = Field(default=None, min_length=2, max_length=100)
    estado: EstadoWorkstation | None = None
    laboratorio_id: int | None = Field(default=None, gt=0)

    @field_validator("codigo", mode="before")
    @classmethod
    def normalizar_codigo(cls, valor):
        return valor.strip().upper() if isinstance(valor, str) else valor if isinstance(valor, str) else valor


class WorkstationDTO(_WorkstationBaseDTO):
    id: int
