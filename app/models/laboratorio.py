from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.enums import (
    EstadoLaboratorio,
)


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
