from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.comun import _ahora
from app.models.enums import (
    PrioridadIncidente,
    EstadoIncidente,
)


class Incidente(SQLModel, table=True):
    __tablename__ = "incidentes"

    id: Optional[int] = Field(default=None, primary_key=True)
    workstation_id: Optional[int] = Field(
        default=None, foreign_key="workstations.id", nullable=True
    )
    equipo_id: Optional[int] = Field(
        default=None, foreign_key="equipos.id", nullable=True
    )
    reportado_por: str = Field(max_length=100, nullable=False)
    descripcion: str = Field(max_length=500, nullable=False)
    prioridad: PrioridadIncidente = Field(
        default=PrioridadIncidente.MEDIA, nullable=False
    )
    estado: EstadoIncidente = Field(
        default=EstadoIncidente.PENDIENTE, nullable=False
    )
    fecha_reporte: datetime = Field(default_factory=_ahora, nullable=False)
    fecha_resolucion: Optional[datetime] = Field(default=None, nullable=True)

    workstation: Optional[Workstation] = Relationship(back_populates="incidentes")
    equipo: Optional[Equipo] = Relationship(back_populates="incidentes")
