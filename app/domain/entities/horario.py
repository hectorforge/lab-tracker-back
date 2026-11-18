from datetime import date, time
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.domain.entities.enums import (
    EstadoHorario,
)


if TYPE_CHECKING:
    from app.domain.entities.laboratorio import Laboratorio
    from app.domain.entities.asignacion_workstation import AsignacionWorkstation
    from app.domain.entities.matricula import Matricula


class Horario(SQLModel, table=True):
    __tablename__ = "horarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    laboratorio_id: int = Field(foreign_key="laboratorios.id", nullable=False)
    nombre_turno: str = Field(max_length=120, nullable=False)
    docente_responsable: str = Field(max_length=100, nullable=False)
    fecha: date = Field(index=True, nullable=False)
    hora_inicio: time = Field(nullable=False)
    hora_fin: time = Field(nullable=False)
    estado: EstadoHorario = Field(default=EstadoHorario.PROGRAMADO, nullable=False)

    laboratorio: Optional["Laboratorio"] = Relationship(back_populates="horarios")
    asignaciones: List["AsignacionWorkstation"] = Relationship(
        back_populates="horario",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    matriculas: List["Matricula"] = Relationship(
        back_populates="horario",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    def validar(self) -> None:
        if self.hora_fin <= self.hora_inicio:
            raise ValueError("La hora de fin debe ser posterior a la de inicio.")
