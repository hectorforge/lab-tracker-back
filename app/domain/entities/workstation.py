from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.domain.entities.enums import (
    EstadoWorkstation,
)


if TYPE_CHECKING:
    from app.domain.entities.laboratorio import Laboratorio
    from app.domain.entities.equipo import Equipo
    from app.domain.entities.asignacion_workstation import AsignacionWorkstation
    from app.domain.entities.incidente import Incidente


class Workstation(SQLModel, table=True):
    __tablename__ = "workstations"

    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str = Field(max_length=30, index=True, nullable=False)
    ubicacion_interna: str = Field(max_length=100, nullable=False)
    estado: EstadoWorkstation = Field(
        default=EstadoWorkstation.DISPONIBLE, nullable=False
    )
    laboratorio_id: int = Field(foreign_key="laboratorios.id", nullable=False)

    laboratorio: Optional["Laboratorio"] = Relationship(back_populates="workstations")
    equipos: List["Equipo"] = Relationship(back_populates="workstation")
    asignaciones: List["AsignacionWorkstation"] = Relationship(
        back_populates="workstation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    incidentes: List["Incidente"] = Relationship(back_populates="workstation")
