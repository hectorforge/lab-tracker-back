from datetime import date, time, datetime
from typing import List, Optional
from pydantic import BaseModel, field_validator, model_validator
from sqlmodel import SQLModel, Field

from app.models import (
    EstadoLaboratorio,
    EstadoWorkstation,
    CategoriaTipoEquipo,
    EstadoEquipo,
    EstadoTipoEquipo,
    Moneda,
    TipoLicencia,
    EstadoLicencia,
    TipoDocumento,
    EstadoAlumno,
    EstadoMatricula,
    EstadoHorario,
    PrioridadIncidente,
    EstadoIncidente,
)


class LaboratorioBase(SQLModel):
    codigo: str = Field(min_length=2, max_length=20)
    nombre: str = Field(min_length=2, max_length=100)
    ubicacion: str = Field(min_length=2, max_length=100)
    capacidad_workstations: int = Field(gt=0)
    estado: EstadoLaboratorio = EstadoLaboratorio.DISPONIBLE


class LaboratorioCreate(LaboratorioBase):
    pass


class LaboratorioUpdate(SQLModel):
    codigo: Optional[str] = Field(default=None, min_length=2, max_length=20)
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    ubicacion: Optional[str] = Field(default=None, min_length=2, max_length=100)
    capacidad_workstations: Optional[int] = Field(default=None, gt=0)
    estado: Optional[EstadoLaboratorio] = None


class LaboratorioRead(LaboratorioBase):
    id: int


class WorkstationBase(SQLModel):
    codigo: str = Field(min_length=2, max_length=30)
    ubicacion_interna: str = Field(min_length=2, max_length=100)
    estado: EstadoWorkstation = EstadoWorkstation.DISPONIBLE
    laboratorio_id: int


class WorkstationCreate(WorkstationBase):
    pass


class WorkstationUpdate(SQLModel):
    codigo: Optional[str] = Field(default=None, min_length=2, max_length=30)
    ubicacion_interna: Optional[str] = Field(default=None, min_length=2, max_length=100)
    estado: Optional[EstadoWorkstation] = None
    laboratorio_id: Optional[int] = None


class WorkstationRead(WorkstationBase):
    id: int


class EquipoBase(SQLModel):
    codigo_patrimonial: str = Field(min_length=2, max_length=50)
    categoria: CategoriaTipoEquipo
    marca: str = Field(min_length=2, max_length=60)
    modelo: str = Field(min_length=1, max_length=80)
    numero_serie: Optional[str] = Field(default=None, max_length=80)
    caracteristicas: str = Field(min_length=2, max_length=500)
    estado: EstadoEquipo = EstadoEquipo.OPERATIVO
    laboratorio_id: int
    workstation_id: Optional[int] = None
    tipo_equipo_id: Optional[int] = None
    costo_estimado: Optional[float] = Field(default=None, ge=0)
    costo_adquisicion: Optional[float] = Field(default=None, ge=0)
    moneda: Moneda = Moneda.PEN
    fecha_adquisicion: Optional[date] = None
    proveedor: Optional[str] = Field(default=None, max_length=120)
    garantia_hasta: Optional[date] = None
    observaciones: Optional[str] = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def validar_costos_y_garantia(self):
        if (
            self.costo_estimado is not None
            and self.costo_adquisicion is not None
            and self.costo_adquisicion > self.costo_estimado * 2
        ):
            raise ValueError("El costo de adquisición difiere demasiado del estimado.")
        if (
            self.garantia_hasta
            and self.fecha_adquisicion
            and self.garantia_hasta < self.fecha_adquisicion
        ):
            raise ValueError("La garantía no puede vencer antes de la adquisición.")
        return self


class EquipoCreate(EquipoBase):
    pass


class EquipoUpdate(SQLModel):
    codigo_patrimonial: Optional[str] = Field(default=None, min_length=2, max_length=50)
    categoria: Optional[CategoriaTipoEquipo] = None
    marca: Optional[str] = Field(default=None, min_length=2, max_length=60)
    modelo: Optional[str] = Field(default=None, min_length=1, max_length=80)
    numero_serie: Optional[str] = Field(default=None, max_length=80)
    caracteristicas: Optional[str] = Field(default=None, min_length=2, max_length=500)
    estado: Optional[EstadoEquipo] = None
    laboratorio_id: Optional[int] = None
    workstation_id: Optional[int] = None
    tipo_equipo_id: Optional[int] = None
    costo_estimado: Optional[float] = Field(default=None, ge=0)
    costo_adquisicion: Optional[float] = Field(default=None, ge=0)
    moneda: Optional[Moneda] = None
    fecha_adquisicion: Optional[date] = None
    proveedor: Optional[str] = Field(default=None, max_length=120)
    garantia_hasta: Optional[date] = None
    observaciones: Optional[str] = Field(default=None, max_length=500)


class EquipoRead(EquipoBase):
    id: int


class HorarioBase(SQLModel):
    laboratorio_id: int
    nombre_turno: str = Field(min_length=3, max_length=120)
    docente_responsable: str = Field(min_length=3, max_length=100)
    fecha: date
    hora_inicio: time
    hora_fin: time

    @model_validator(mode="after")
    def validar_rango_horario(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio.")
        return self


class HorarioCreate(HorarioBase):
    pass


class HorarioRead(HorarioBase):
    id: int
    estado: EstadoHorario


class AsignacionCreate(SQLModel):
    workstation_id: int
    codigo_alumno: str = Field(min_length=3, max_length=30)
    observaciones: Optional[str] = Field(default=None, max_length=250)


class AsignacionRead(SQLModel):
    id: int
    horario_id: int
    workstation_id: int
    codigo_alumno: str
    observaciones: Optional[str]
    fecha_asignacion: datetime


class IncidenteBase(SQLModel):
    workstation_id: Optional[int] = None
    equipo_id: Optional[int] = None
    reportado_por: str = Field(min_length=2, max_length=100)
    descripcion: str = Field(min_length=5, max_length=500)
    prioridad: PrioridadIncidente = PrioridadIncidente.MEDIA

    @model_validator(mode="after")
    def validar_objetivo_incidente(self):
        if self.workstation_id is None and self.equipo_id is None:
            raise ValueError(
                "Debe especificar al menos un workstation_id o un equipo_id."
            )
        return self


class IncidenteCreate(IncidenteBase):
    pass


class IncidenteUpdateEstado(SQLModel):
    estado: EstadoIncidente


class IncidenteRead(IncidenteBase):
    id: int
    estado: EstadoIncidente
    fecha_reporte: datetime
    fecha_resolucion: Optional[datetime]


# ---------------------------------------------------------------------------
# Catalogo de tipos de equipo
# ---------------------------------------------------------------------------


class TipoEquipoBase(SQLModel):
    codigo: str = Field(min_length=2, max_length=20)
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: str = Field(min_length=2, max_length=500)
    categoria: CategoriaTipoEquipo
    especificaciones_minimas: Optional[str] = Field(default=None, max_length=500)
    vida_util_meses: Optional[int] = Field(default=None, ge=1, le=600)
    requiere_mantenimiento: bool = False
    requiere_licencia: bool = False
    costo_referencial: Optional[float] = Field(default=None, ge=0)
    moneda: Moneda = Moneda.PEN
    estado: EstadoTipoEquipo = EstadoTipoEquipo.ACTIVO

    @field_validator("codigo")
    @classmethod
    def normalizar_codigo(cls, valor: str) -> str:
        return valor.strip().upper()


class TipoEquipoCreate(TipoEquipoBase):
    pass


class TipoEquipoUpdate(SQLModel):
    codigo: Optional[str] = Field(default=None, min_length=2, max_length=20)
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(default=None, min_length=2, max_length=500)
    categoria: Optional[CategoriaTipoEquipo] = None
    especificaciones_minimas: Optional[str] = Field(default=None, max_length=500)
    vida_util_meses: Optional[int] = Field(default=None, ge=1, le=600)
    requiere_mantenimiento: Optional[bool] = None
    requiere_licencia: Optional[bool] = None
    costo_referencial: Optional[float] = Field(default=None, ge=0)
    moneda: Optional[Moneda] = None
    estado: Optional[EstadoTipoEquipo] = None


class TipoEquipoRead(TipoEquipoBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime


# ---------------------------------------------------------------------------
# Alumnos
# ---------------------------------------------------------------------------

CORREO_INSTITUCIONAL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class AlumnoBase(SQLModel):
    codigo: str = Field(min_length=3, max_length=30)
    nombres: str = Field(min_length=2, max_length=100)
    apellidos: str = Field(min_length=2, max_length=100)
    tipo_documento: TipoDocumento = TipoDocumento.DNI
    numero_documento: Optional[str] = Field(default=None, max_length=20)
    correo_institucional: str = Field(max_length=150)
    correo_personal: Optional[str] = Field(default=None, max_length=150)
    telefono: Optional[str] = Field(default=None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    carrera: str = Field(min_length=2, max_length=120)
    semestre: Optional[int] = Field(default=None, ge=1, le=20)
    grupo: Optional[str] = Field(default=None, max_length=20)
    estado: EstadoAlumno = EstadoAlumno.ACTIVO
    fecha_ingreso: date = Field(default_factory=date.today)
    observaciones: Optional[str] = Field(default=None, max_length=500)

    @field_validator("codigo")
    @classmethod
    def normalizar_codigo(cls, valor: str) -> str:
        return valor.strip().upper()

    @field_validator("correo_institucional")
    @classmethod
    def validar_correo_institucional(cls, valor: str) -> str:
        import re

        correo = valor.strip().lower()
        if not re.match(CORREO_INSTITUCIONAL_PATTERN, correo):
            raise ValueError("El correo institucional no tiene un formato valido.")
        return correo


class AlumnoCreate(AlumnoBase):
    pass


class AlumnoUpdate(SQLModel):
    codigo: Optional[str] = Field(default=None, min_length=3, max_length=30)
    nombres: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellidos: Optional[str] = Field(default=None, min_length=2, max_length=100)
    tipo_documento: Optional[TipoDocumento] = None
    numero_documento: Optional[str] = Field(default=None, max_length=20)
    correo_institucional: Optional[str] = Field(default=None, max_length=150)
    correo_personal: Optional[str] = Field(default=None, max_length=150)
    telefono: Optional[str] = Field(default=None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    carrera: Optional[str] = Field(default=None, min_length=2, max_length=120)
    semestre: Optional[int] = Field(default=None, ge=1, le=20)
    grupo: Optional[str] = Field(default=None, max_length=20)
    estado: Optional[EstadoAlumno] = None
    fecha_ingreso: Optional[date] = None
    observaciones: Optional[str] = Field(default=None, max_length=500)


class AlumnoRead(AlumnoBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime


# ---------------------------------------------------------------------------
# Matriculas (Alumno <-> Horario)
# ---------------------------------------------------------------------------


class MatriculaCreate(SQLModel):
    alumno_id: int
    horario_id: int
    observaciones: Optional[str] = Field(default=None, max_length=250)


class MatriculaRead(SQLModel):
    id: int
    alumno_id: int
    horario_id: int
    fecha_matricula: datetime
    estado: EstadoMatricula
    observaciones: Optional[str]


class MatriculaDetalleRead(MatriculaRead):
    alumno: AlumnoRead


# ---------------------------------------------------------------------------
# Reporte de carga masiva desde Excel
# ---------------------------------------------------------------------------


class ErrorFilaExcel(BaseModel):
    fila: int
    codigo: Optional[str] = None
    campo: str
    mensaje: str


class ResultadoCargaMatricula(BaseModel):
    horario_id: int
    total_filas_leidas: int
    filas_validas: int
    alumnos_creados: int
    alumnos_reutilizados: int
    registros_insertados: int
    filas_con_error: int
    errores: List[ErrorFilaExcel]
    modo: str
    mensaje: str


class ColumnaPlantilla(BaseModel):
    nombre: str
    requerida: bool
    descripcion: str


# ---------------------------------------------------------------------------
# Licencias de software por equipo
# ---------------------------------------------------------------------------


class LicenciaBase(SQLModel):
    codigo: str = Field(min_length=2, max_length=50)
    nombre: str = Field(min_length=2, max_length=120)
    tipo: TipoLicencia = TipoLicencia.PERPETUA
    clave_producto: Optional[str] = Field(default=None, max_length=120)
    fabricante: Optional[str] = Field(default=None, max_length=100)
    cantidad_usuarios: int = Field(default=1, ge=1)
    fecha_adquisicion: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    costo: Optional[float] = Field(default=None, ge=0)
    moneda: Moneda = Moneda.PEN
    estado: EstadoLicencia = EstadoLicencia.ACTIVA
    equipo_id: Optional[int] = None
    tipo_equipo_id: Optional[int] = None
    observaciones: Optional[str] = Field(default=None, max_length=500)

    @field_validator("codigo")
    @classmethod
    def normalizar_codigo(cls, valor: str) -> str:
        return valor.strip().upper()

    @model_validator(mode="after")
    def validar_licencia(self):
        if (
            self.fecha_vencimiento
            and self.fecha_adquisicion
            and self.fecha_vencimiento < self.fecha_adquisicion
        ):
            raise ValueError("La licencia no puede vencer antes de su adquisición.")
        if (
            self.estado == EstadoLicencia.ACTIVA
            and self.fecha_vencimiento
            and self.fecha_vencimiento < date.today()
        ):
            raise ValueError("Una licencia vencida no puede permanecer activa.")
        return self


class LicenciaCreate(LicenciaBase):
    pass


class LicenciaUpdate(SQLModel):
    codigo: Optional[str] = Field(default=None, min_length=2, max_length=50)
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=120)
    tipo: Optional[TipoLicencia] = None
    clave_producto: Optional[str] = Field(default=None, max_length=120)
    fabricante: Optional[str] = Field(default=None, max_length=100)
    cantidad_usuarios: Optional[int] = Field(default=None, ge=1)
    fecha_adquisicion: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    costo: Optional[float] = Field(default=None, ge=0)
    moneda: Optional[Moneda] = None
    estado: Optional[EstadoLicencia] = None
    equipo_id: Optional[int] = None
    tipo_equipo_id: Optional[int] = None
    observaciones: Optional[str] = Field(default=None, max_length=500)


class LicenciaRead(LicenciaBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime