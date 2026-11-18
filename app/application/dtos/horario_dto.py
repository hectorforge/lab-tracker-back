from datetime import date, time, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.entities import EstadoHorario


class _HorarioBaseDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    laboratorio_id: int = Field(gt=0)
    nombre_turno: str = Field(min_length=3, max_length=120)
    docente_responsable: str = Field(min_length=3, max_length=100)
    fecha: date
    hora_inicio: time
    hora_fin: time

    @model_validator(mode="after")
    def validar_rango(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio.")
        return self


class CrearHorarioDTO(_HorarioBaseDTO):
    """DTO de entrada para programar horarios."""


class HorarioDTO(_HorarioBaseDTO):
    id: int
    estado: EstadoHorario


class _AsignacionBaseDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    workstation_id: int = Field(gt=0)
    codigo_alumno: str = Field(min_length=3, max_length=30)
    observaciones: Optional[str] = Field(default=None, max_length=250)

    @model_validator(mode="after")
    def normalizar_codigo(self):
        object.__setattr__(self, "codigo_alumno", self.codigo_alumno.strip().upper())
        return self


class CrearAsignacionDTO(_AsignacionBaseDTO):
    """DTO de entrada para asignar workstations."""


class AsignacionDTO(_AsignacionBaseDTO):
    id: int
    horario_id: int
    alumno_id: Optional[int] = None
    fecha_asignacion: datetime
