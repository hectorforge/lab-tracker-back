from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.domain.entities.enums import (
    EstadoLaboratorio,
)


if TYPE_CHECKING:
    from app.domain.entities.workstation import Workstation
    from app.domain.entities.equipo import Equipo
    from app.domain.entities.horario import Horario


class Laboratorio(SQLModel, table=True):
    __tablename__ = "laboratorios"

    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str = Field(max_length=20, unique=True, index=True, nullable=False)
    nombre: str = Field(max_length=100, nullable=False)
    ubicacion: str = Field(max_length=100, nullable=False)
    capacidad_workstations: int = Field(gt=0, nullable=False)
    estado: EstadoLaboratorio = Field(
        default=EstadoLaboratorio.DISPONIBLE, nullable=False
    )
    url_imagen: Optional[str] = Field(default=None, max_length=500)

    workstations: List["Workstation"] = Relationship(
        back_populates="laboratorio",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    equipos: List["Equipo"] = Relationship(
        back_populates="laboratorio",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    horarios: List["Horario"] = Relationship(
        back_populates="laboratorio",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
