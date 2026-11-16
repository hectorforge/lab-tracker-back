from datetime import date, time, datetime
from typing import Optional
from pydantic import model_validator
from sqlmodel import SQLModel, Field

from app.models.lab_models import (
    EstadoLaboratorio,
    EstadoWorkstation,
    TipoEquipo,
    EstadoEquipo,
    EstadoHorario,
    PrioridadIncidente,
    EstadoIncidente,
)


class LaboratorioBase(SQLModel):
    codigo: str = Field(min_length=2, max_length=20)
    nombre: str = Field(min_length=2, max_length=100)
    ubicacion: str = Field(min_length=2, max_length=100)
    capacidad_workstations: int = Field(gt=0)
    estado: EstadoLaboratorio = EstadoLaboratorio.DISPONIBLE


class LaboratorioCreate(LaboratorioBase):
    pass


class LaboratorioUpdate(SQLModel):
    codigo: Optional[str] = Field(default=None, min_length=2, max_length=20)
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    ubicacion: Optional[str] = Field(default=None, min_length=2, max_length=100)
    capacidad_workstations: Optional[int] = Field(default=None, gt=0)
    estado: Optional[EstadoLaboratorio] = None


class LaboratorioRead(LaboratorioBase):
    id: int


class WorkstationBase(SQLModel):
    codigo: str = Field(min_length=2, max_length=30)
    ubicacion_interna: str = Field(min_length=2, max_length=100)
    estado: EstadoWorkstation = EstadoWorkstation.DISPONIBLE
    laboratorio_id: int


class WorkstationCreate(WorkstationBase):
    pass


class WorkstationUpdate(SQLModel):
    codigo: Optional[str] = Field(default=None, min_length=2, max_length=30)
    ubicacion_interna: Optional[str] = Field(default=None, min_length=2, max_length=100)
    estado: Optional[EstadoWorkstation] = None
    laboratorio_id: Optional[int] = None


class WorkstationRead(WorkstationBase):
    id: int


class EquipoBase(SQLModel):
    codigo_patrimonial: str = Field(min_length=2, max_length=50)
    tipo: TipoEquipo
    marca: str = Field(min_length=2, max_length=60)
    modelo: str = Field(min_length=1, max_length=80)
    numero_serie: Optional[str] = Field(default=None, max_length=80)
    caracteristicas: str = Field(min_length=2, max_length=500)
    estado: EstadoEquipo = EstadoEquipo.OPERATIVO
    laboratorio_id: int
    workstation_id: Optional[int] = None


class EquipoCreate(EquipoBase):
    pass


class EquipoUpdate(SQLModel):
    codigo_patrimonial: Optional[str] = Field(default=None, min_length=2, max_length=50)
    tipo: Optional[TipoEquipo] = None
    marca: Optional[str] = Field(default=None, min_length=2, max_length=60)
    modelo: Optional[str] = Field(default=None, min_length=1, max_length=80)
    numero_serie: Optional[str] = Field(default=None, max_length=80)
    caracteristicas: Optional[str] = Field(default=None, min_length=2, max_length=500)
    estado: Optional[EstadoEquipo] = None
    laboratorio_id: Optional[int] = None
    workstation_id: Optional[int] = None


class EquipoRead(EquipoBase):
    id: int


class HorarioBase(SQLModel):
    laboratorio_id: int
    nombre_turno: str = Field(min_length=3, max_length=120)
    docente_responsable: str = Field(min_length=3, max_length=100)
    fecha: date
    hora_inicio: time
    hora_fin: time

    @model_validator(mode="after")
    def validar_rango_horario(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio.")
        return self


class HorarioCreate(HorarioBase):
    pass


class HorarioRead(HorarioBase):
    id: int
    estado: EstadoHorario


class AsignacionCreate(SQLModel):
    workstation_id: int
    codigo_alumno: str = Field(min_length=3, max_length=30)
    observaciones: Optional[str] = Field(default=None, max_length=250)


class AsignacionRead(SQLModel):
    id: int
    horario_id: int
    workstation_id: int
    codigo_alumno: str
    observaciones: Optional[str]
    fecha_asignacion: datetime


class IncidenteBase(SQLModel):
    workstation_id: Optional[int] = None
    equipo_id: Optional[int] = None
    reportado_por: str = Field(min_length=2, max_length=100)
    descripcion: str = Field(min_length=5, max_length=500)
    prioridad: PrioridadIncidente = PrioridadIncidente.MEDIA

    @model_validator(mode="after")
    def validar_objetivo_incidente(self):
        if self.workstation_id is None and self.equipo_id is None:
            raise ValueError(
                "Debe especificar al menos un workstation_id o un equipo_id."
            )
        return self


class IncidenteCreate(IncidenteBase):
    pass


class IncidenteUpdateEstado(SQLModel):
    estado: EstadoIncidente


class IncidenteRead(IncidenteBase):
    id: int
    estado: EstadoIncidente
    fecha_reporte: datetime
    fecha_resolucion: Optional[datetime]