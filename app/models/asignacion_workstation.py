from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.comun import _ahora


class AsignacionWorkstation(SQLModel, table=True):
    __tablename__ = "asignaciones_workstation"

    id: Optional[int] = Field(default=None, primary_key=True)
    horario_id: int = Field(foreign_key="horarios.id", nullable=False)
    workstation_id: int = Field(foreign_key="workstations.id", nullable=False)
    codigo_alumno: str = Field(max_length=30, index=True, nullable=False)
    alumno_id: Optional[int] = Field(
        default=None, foreign_key="alumnos.id", nullable=True
    )
    observaciones: Optional[str] = Field(default=None, max_length=250)
    fecha_asignacion: datetime = Field(default_factory=_ahora, nullable=False)

    horario: Optional[Horario] = Relationship(back_populates="asignaciones")
    workstation: Optional[Workstation] = Relationship(back_populates="asignaciones")
    alumno: Optional[Alumno] = Relationship(back_populates="asignaciones")
