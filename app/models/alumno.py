from datetime import date, datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.comun import _ahora, PATRON_CODIGO, PATRON_CORREO
from app.models.enums import (
    TipoDocumento,
    EstadoAlumno,
)


class Alumno(SQLModel, table=True):
    """Datos personales y académicos de un estudiante de la institución."""

    __tablename__ = "alumnos"

    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str = Field(max_length=30, unique=True, index=True, nullable=False)
    nombres: str = Field(max_length=100, nullable=False)
    apellidos: str = Field(max_length=100, nullable=False)
    tipo_documento: TipoDocumento = Field(default=TipoDocumento.DNI, nullable=False)
    numero_documento: Optional[str] = Field(default=None, max_length=20, index=True)
    correo_institucional: str = Field(
        max_length=150, unique=True, index=True, nullable=False
    )
    correo_personal: Optional[str] = Field(default=None, max_length=150)
    telefono: Optional[str] = Field(default=None, max_length=20)
    fecha_nacimiento: Optional[date] = Field(default=None)
    carrera: str = Field(max_length=120, nullable=False)
    semestre: Optional[int] = Field(default=None, ge=1, le=20)
    grupo: Optional[str] = Field(default=None, max_length=20)
    estado: EstadoAlumno = Field(default=EstadoAlumno.ACTIVO, nullable=False)
    fecha_ingreso: date = Field(default_factory=date.today, nullable=False)
    observaciones: Optional[str] = Field(default=None, max_length=500)
    creado_en: datetime = Field(default_factory=_ahora, nullable=False)
    actualizado_en: datetime = Field(default_factory=_ahora, nullable=False)

    matriculas: List["Matricula"] = Relationship(
        back_populates="alumno",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    asignaciones: List["AsignacionWorkstation"] = Relationship(
        back_populates="alumno"
    )

    def validar(self) -> None:
        if not PATRON_CODIGO.match(self.codigo.strip().upper()):
            raise ValueError("El código de alumno contiene caracteres inválidos.")
        if not PATRON_CORREO.match(self.correo_institucional.strip().lower()):
            raise ValueError("El correo institucional no tiene un formato válido.")
        if self.semestre is not None and not 1 <= self.semestre <= 20:
            raise ValueError("El semestre debe estar entre 1 y 20.")
        if (
            self.fecha_nacimiento
            and self.fecha_nacimiento > date.today()
        ):
            raise ValueError("La fecha de nacimiento no puede ser futura.")
