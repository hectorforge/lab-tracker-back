from .laboratorio import AbstractLaboratorioRepository
from .workstation import AbstractWorkstationRepository
from .equipo import AbstractEquipoRepository
from .horario import AbstractHorarioRepository
from .incidente import AbstractIncidenteRepository
from .tipo_equipo import AbstractTipoEquipoRepository
from .alumno import AbstractAlumnoRepository
from .matricula import AbstractMatriculaRepository
from .licencia import AbstractLicenciaRepository

__all__ = [
    "AbstractLaboratorioRepository",
    "AbstractWorkstationRepository",
    "AbstractEquipoRepository",
    "AbstractHorarioRepository",
    "AbstractIncidenteRepository",
    "AbstractTipoEquipoRepository",
    "AbstractAlumnoRepository",
    "AbstractMatriculaRepository",
    "AbstractLicenciaRepository",
]
