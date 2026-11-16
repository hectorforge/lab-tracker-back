import enum
from datetime import date, time, datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class EstadoLaboratorio(str, enum.Enum):
    DISPONIBLE = "disponible"
    MANTENIMIENTO = "mantenimiento"
    CERRADO = "cerrado"


class EstadoWorkstation(str, enum.Enum):
    DISPONIBLE = "disponible"
    CON_FALLA = "con_falla"
    EN_MANTENIMIENTO = "en_mantenimiento"
    INHABILITADA = "inhabilitada"


class TipoEquipo(str, enum.Enum):
    CPU = "cpu"
    MONITOR = "monitor"
    ESTABILIZADOR = "estabilizador"
    TECLADO = "teclado"
    MOUSE = "mouse"


class EstadoEquipo(str, enum.Enum):
    OPERATIVO = "operativo"
    CON_FALLA = "con_falla"
    EN_MANTENIMIENTO = "en_mantenimiento"
    DE_BAJA = "de_baja"


class EstadoHorario(str, enum.Enum):
    PROGRAMADO = "programado"
    EN_CURSO = "en_curso"
    FINALIZADO = "finalizado"
    CANCELADO = "cancelado"


class PrioridadIncidente(str, enum.Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class EstadoIncidente(str, enum.Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    RESUELTO = "resuelto"


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


class Workstation(SQLModel, table=True):
    __tablename__ = "workstations"

    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str = Field(max_length=30, index=True, nullable=False)
    ubicacion_interna: str = Field(max_length=100, nullable=False)
    estado: EstadoWorkstation = Field(
        default=EstadoWorkstation.DISPONIBLE, nullable=False
    )
    laboratorio_id: int = Field(foreign_key="laboratorios.id", nullable=False)

    laboratorio: Optional[Laboratorio] = Relationship(back_populates="workstations")
    equipos: List["Equipo"] = Relationship(back_populates="workstation")
    asignaciones: List["AsignacionWorkstation"] = Relationship(
        back_populates="workstation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    incidentes: List["Incidente"] = Relationship(back_populates="workstation")


class Equipo(SQLModel, table=True):
    __tablename__ = "equipos"

    id: Optional[int] = Field(default=None, primary_key=True)
    codigo_patrimonial: str = Field(
        max_length=50, unique=True, index=True, nullable=False
    )
    tipo: TipoEquipo = Field(index=True, nullable=False)
    marca: str = Field(max_length=60, nullable=False)
    modelo: str = Field(max_length=80, nullable=False)
    numero_serie: Optional[str] = Field(default=None, max_length=80)
    caracteristicas: str = Field(max_length=500, nullable=False)
    estado: EstadoEquipo = Field(default=EstadoEquipo.OPERATIVO, nullable=False)
    laboratorio_id: int = Field(foreign_key="laboratorios.id", nullable=False)
    workstation_id: Optional[int] = Field(
        default=None, foreign_key="workstations.id", nullable=True
    )

    laboratorio: Optional[Laboratorio] = Relationship(back_populates="equipos")
    workstation: Optional[Workstation] = Relationship(back_populates="equipos")
    incidentes: List["Incidente"] = Relationship(back_populates="equipo")


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

    laboratorio: Optional[Laboratorio] = Relationship(back_populates="horarios")
    asignaciones: List["AsignacionWorkstation"] = Relationship(
        back_populates="horario",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class AsignacionWorkstation(SQLModel, table=True):
    __tablename__ = "asignaciones_workstation"

    id: Optional[int] = Field(default=None, primary_key=True)
    horario_id: int = Field(foreign_key="horarios.id", nullable=False)
    workstation_id: int = Field(foreign_key="workstations.id", nullable=False)
    codigo_alumno: str = Field(max_length=30, index=True, nullable=False)
    observaciones: Optional[str] = Field(default=None, max_length=250)
    fecha_asignacion: datetime = Field(default_factory=datetime.now, nullable=False)

    horario: Optional[Horario] = Relationship(back_populates="asignaciones")
    workstation: Optional[Workstation] = Relationship(back_populates="asignaciones")


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
    fecha_reporte: datetime = Field(default_factory=datetime.now, nullable=False)
    fecha_resolucion: Optional[datetime] = Field(default=None, nullable=True)

    workstation: Optional[Workstation] = Relationship(back_populates="incidentes")
    equipo: Optional[Equipo] = Relationship(back_populates="incidentes")