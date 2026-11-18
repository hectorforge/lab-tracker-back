from .laboratorio import LaboratorioRepository
from .workstation import WorkstationRepository
from .equipo import EquipoRepository
from .tipo_equipo import TipoEquipoRepository
from .alumno import AlumnoRepository
from .matricula import MatriculaRepository
from .horario import HorarioRepository
from .incidente import IncidenteRepository
from .licencia import LicenciaRepository

__all__ = [
    "LaboratorioRepository",
    "WorkstationRepository",
    "EquipoRepository",
    "TipoEquipoRepository",
    "AlumnoRepository",
    "MatriculaRepository",
    "HorarioRepository",
    "IncidenteRepository",
    "LicenciaRepository",
]
