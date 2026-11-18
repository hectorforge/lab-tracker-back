from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.domain.entities import EstadoAlumno, TipoDocumento

PATRON_CODIGO = r"^[A-Z0-9\-_]+$"
PATRON_CORREO = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class _AlumnoBaseDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    codigo: str = Field(min_length=3, max_length=30, pattern=PATRON_CODIGO)
    nombres: str = Field(min_length=2, max_length=100)
    apellidos: str = Field(min_length=2, max_length=100)
    tipo_documento: TipoDocumento = TipoDocumento.DNI
    numero_documento: Optional[str] = Field(default=None, max_length=20)
    correo_institucional: str = Field(max_length=150, pattern=PATRON_CORREO)
    correo_personal: Optional[str] = Field(default=None, max_length=150)
    telefono: Optional[str] = Field(default=None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    carrera: str = Field(min_length=2, max_length=120)
    semestre: Optional[int] = Field(default=None, ge=1, le=20)
    grupo: Optional[str] = Field(default=None, max_length=20)
    estado: EstadoAlumno = EstadoAlumno.ACTIVO
    fecha_ingreso: date = Field(default_factory=date.today)
    observaciones: Optional[str] = Field(default=None, max_length=500)

    @field_validator("codigo", mode="before")
    @classmethod
    def normalizar_codigo(cls, valor):
        return valor.strip().upper() if isinstance(valor, str) else valor

    @field_validator("correo_institucional", "correo_personal", mode="before")
    @classmethod
    def normalizar_correo(cls, valor):
        return valor.strip().lower() if isinstance(valor, str) else valor if isinstance(valor, str) else valor

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_nacimiento and self.fecha_nacimiento > date.today():
            raise ValueError("La fecha de nacimiento no puede ser futura.")
        return self


class CrearAlumnoDTO(_AlumnoBaseDTO):
    """DTO de entrada para crear alumnos."""


class ActualizarAlumnoDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    codigo: Optional[str] = Field(default=None, min_length=3, max_length=30, pattern=PATRON_CODIGO)
    nombres: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellidos: Optional[str] = Field(default=None, min_length=2, max_length=100)
    tipo_documento: Optional[TipoDocumento] = None
    numero_documento: Optional[str] = Field(default=None, max_length=20)
    correo_institucional: Optional[str] = Field(default=None, max_length=150, pattern=PATRON_CORREO)
    correo_personal: Optional[str] = Field(default=None, max_length=150)
    telefono: Optional[str] = Field(default=None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    carrera: Optional[str] = Field(default=None, min_length=2, max_length=120)
    semestre: Optional[int] = Field(default=None, ge=1, le=20)
    grupo: Optional[str] = Field(default=None, max_length=20)
    estado: Optional[EstadoAlumno] = None
    fecha_ingreso: Optional[date] = None
    observaciones: Optional[str] = Field(default=None, max_length=500)

    @field_validator("codigo", mode="before")
    @classmethod
    def normalizar_codigo(cls, valor):
        return valor.strip().upper() if isinstance(valor, str) else valor if isinstance(valor, str) else valor

    @field_validator("correo_institucional", "correo_personal", mode="before")
    @classmethod
    def normalizar_correo(cls, valor):
        return valor.strip().lower() if isinstance(valor, str) else valor if isinstance(valor, str) else valor


class AlumnoDTO(_AlumnoBaseDTO):
    id: int
    creado_en: datetime
    actualizado_en: datetime
