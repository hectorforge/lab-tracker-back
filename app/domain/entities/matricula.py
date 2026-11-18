from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship
from app.domain.entities.comun import _ahora
from app.domain.entities.enums import (
    EstadoMatricula,
)


if TYPE_CHECKING:
    from app.domain.entities.alumno import Alumno
    from app.domain.entities.horario import Horario


class Matricula(SQLModel, table=True):
    """Tabla intermedia Alumno <-> Horario: matrícula en un turno de laboratorio."""

    __tablename__ = "matriculas"
    __table_args__ = (
        UniqueConstraint(
            "alumno_id", "horario_id", name="uq_matricula_alumno_horario"
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    alumno_id: int = Field(foreign_key="alumnos.id", nullable=False)
    horario_id: int = Field(foreign_key="horarios.id", nullable=False)
    fecha_matricula: datetime = Field(default_factory=_ahora, nullable=False)
    estado: EstadoMatricula = Field(default=EstadoMatricula.MATRICULADO, nullable=False)
    observaciones: Optional[str] = Field(default=None, max_length=250)

    alumno: Optional["Alumno"] = Relationship(back_populates="matriculas")
    horario: Optional["Horario"] = Relationship(back_populates="matriculas")

    def validar(self) -> None:
        if self.alumno_id <= 0 or self.horario_id <= 0:
            raise ValueError("La matrícula requiere un alumno y un horario válidos.")
