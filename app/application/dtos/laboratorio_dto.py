from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.entities import EstadoLaboratorio


class _LaboratorioBaseDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    codigo: str = Field(min_length=2, max_length=20)
    nombre: str = Field(min_length=2, max_length=100)
    ubicacion: str = Field(min_length=2, max_length=100)
    capacidad_workstations: int = Field(gt=0)
    estado: EstadoLaboratorio = EstadoLaboratorio.DISPONIBLE
    url_imagen: str | None = Field(default=None, max_length=500)

    @field_validator("url_imagen")
    @classmethod
    def validar_url_imagen(cls, valor: str | None) -> str | None:
        if valor and not valor.startswith(("http://", "https://")):
            raise ValueError("La URL de la imagen debe empezar con http:// o https://.")
        return valor

    @field_validator("codigo", mode="before")
    @classmethod
    def normalizar_codigo(cls, valor):
        return valor.strip().upper() if isinstance(valor, str) else valor


class CrearLaboratorioDTO(_LaboratorioBaseDTO):
    """DTO de entrada para registrar laboratorios."""


class ActualizarLaboratorioDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    codigo: str | None = Field(default=None, min_length=2, max_length=20)
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    ubicacion: str | None = Field(default=None, min_length=2, max_length=100)
    capacidad_workstations: int | None = Field(default=None, gt=0)
    estado: EstadoLaboratorio | None = None
    url_imagen: str | None = Field(default=None, max_length=500)

    @field_validator("url_imagen")
    @classmethod
    def validar_url_imagen(cls, valor: str | None) -> str | None:
        if valor and not valor.startswith(("http://", "https://")):
            raise ValueError("La URL de la imagen debe empezar con http:// o https://.")
        return valor

    @field_validator("codigo", mode="before")
    @classmethod
    def normalizar_codigo(cls, valor):
        return valor.strip().upper() if isinstance(valor, str) else valor if isinstance(valor, str) else valor


class LaboratorioDTO(_LaboratorioBaseDTO):
    id: int
