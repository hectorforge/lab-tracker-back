from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models import EstadoAlumno, EstadoMatricula, TipoDocumento
from app.dtos.alumno_dto import AlumnoDTO

PATRON_CODIGO = r"^[A-Z0-9\-_]+$"
PATRON_CORREO = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class FilaMatriculaDTO(BaseModel):
    """Fila ya saneada del Excel: es el objeto que consume el servicio."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    fila: int = Field(gt=1)
    codigo: str = Field(min_length=3, max_length=30, pattern=PATRON_CODIGO)
    nombres: str = Field(min_length=2, max_length=100)
    apellidos: str = Field(min_length=2, max_length=100)
    tipo_documento: TipoDocumento = TipoDocumento.DNI
    numero_documento: Optional[str] = Field(default=None, max_length=20)
    correo_institucional: str = Field(max_length=150, pattern=PATRON_CORREO)
    correo_personal: Optional[str] = Field(default=None, max_length=150)
    telefono: Optional[str] = Field(default=None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    carrera: str = Field(min_length=2, max_length=120)
    semestre: Optional[int] = Field(default=None, ge=1, le=20)
    grupo: Optional[str] = Field(default=None, max_length=20)
    estado: EstadoAlumno = EstadoAlumno.ACTIVO
    observaciones: Optional[str] = Field(default=None, max_length=250)

    @field_validator("codigo")
    @classmethod
    def normalizar_codigo(cls, valor: str) -> str:
        return valor.strip().upper()

    @field_validator("correo_institucional", "correo_personal")
    @classmethod
    def normalizar_correo(cls, valor: Optional[str]) -> Optional[str]:
        return valor.strip().lower() if valor else valor


class CrearMatriculaDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    alumno_id: int = Field(gt=0)
    horario_id: int = Field(gt=0)
    observaciones: Optional[str] = Field(default=None, max_length=250)


class ErrorFilaExcelDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    fila: int
    codigo: Optional[str] = None
    campo: str
    mensaje: str


class ResultadoCargaMatriculaDTO(BaseModel):
    horario_id: int
    total_filas_leidas: int
    filas_validas: int
    alumnos_creados: int
    alumnos_reutilizados: int
    registros_insertados: int
    filas_con_error: int
    errores: List[ErrorFilaExcelDTO]
    modo: str
    mensaje: str


class ColumnaPlantillaDTO(BaseModel):
    nombre: str
    requerida: bool
    descripcion: str


class MatriculaDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    alumno_id: int
    horario_id: int
    fecha_matricula: datetime
    estado: EstadoMatricula
    observaciones: Optional[str] = None
    alumno: Optional[AlumnoDTO] = None
