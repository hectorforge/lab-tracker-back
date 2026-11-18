"""DTOs de aplicación: validan la estructura de entrada y salida de los servicios."""

from .alumno_dto import AlumnoDTO, CrearAlumnoDTO, ActualizarAlumnoDTO
from .tipo_equipo_dto import (
    TipoEquipoDTO,
    CrearTipoEquipoDTO,
    ActualizarTipoEquipoDTO,
)
from .equipo_dto import EquipoDTO, CrearEquipoDTO, ActualizarEquipoDTO
from .licencia_dto import LicenciaDTO, CrearLicenciaDTO, ActualizarLicenciaDTO
from .laboratorio_dto import (
    LaboratorioDTO,
    CrearLaboratorioDTO,
    ActualizarLaboratorioDTO,
)
from .workstation_dto import (
    WorkstationDTO,
    CrearWorkstationDTO,
    ActualizarWorkstationDTO,
)
from .horario_dto import (
    HorarioDTO,
    CrearHorarioDTO,
    AsignacionDTO,
    CrearAsignacionDTO,
)
from .incidente_dto import (
    IncidenteDTO,
    CrearIncidenteDTO,
    ActualizarEstadoIncidenteDTO,
)
from .matricula_dto import (
    MatriculaDTO,
    CrearMatriculaDTO,
    FilaMatriculaDTO,
    ErrorFilaExcelDTO,
    ResultadoCargaMatriculaDTO,
    ColumnaPlantillaDTO,
)
from .rol_dto import RolDTO, CrearRolDTO, ActualizarRolDTO
from .usuario_dto import (
    UsuarioDTO,
    CrearUsuarioDTO,
    ActualizarUsuarioDTO,
)
from .auth_dto import LoginDTO, TokenDTO

__all__ = [
    "AlumnoDTO", "CrearAlumnoDTO", "ActualizarAlumnoDTO",
    "TipoEquipoDTO", "CrearTipoEquipoDTO", "ActualizarTipoEquipoDTO",
    "EquipoDTO", "CrearEquipoDTO", "ActualizarEquipoDTO",
    "LicenciaDTO", "CrearLicenciaDTO", "ActualizarLicenciaDTO",
    "LaboratorioDTO", "CrearLaboratorioDTO", "ActualizarLaboratorioDTO",
    "WorkstationDTO", "CrearWorkstationDTO", "ActualizarWorkstationDTO",
    "HorarioDTO", "CrearHorarioDTO", "AsignacionDTO", "CrearAsignacionDTO",
    "IncidenteDTO", "CrearIncidenteDTO", "ActualizarEstadoIncidenteDTO",
    "MatriculaDTO", "CrearMatriculaDTO", "FilaMatriculaDTO",
    "ErrorFilaExcelDTO", "ResultadoCargaMatriculaDTO", "ColumnaPlantillaDTO",
    "RolDTO", "CrearRolDTO", "ActualizarRolDTO",
    "UsuarioDTO", "CrearUsuarioDTO", "ActualizarUsuarioDTO",
    "LoginDTO", "TokenDTO",
]
