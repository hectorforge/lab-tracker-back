from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import JSON, Column
from sqlmodel import SQLModel, Field, Relationship
from app.domain.entities.comun import _ahora
from app.domain.entities.enums import (
    PrioridadIncidente,
    EstadoIncidente,
)


if TYPE_CHECKING:
    from app.domain.entities.workstation import Workstation
    from app.domain.entities.equipo import Equipo


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
    # Enlaces a las fotos del incidente (adjuntos) almacenados como JSON.
    url_imagenes: Optional[List[str]] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )

    workstation: Optional["Workstation"] = Relationship(back_populates="incidentes")
    equipo: Optional["Equipo"] = Relationship(back_populates="incidentes")
