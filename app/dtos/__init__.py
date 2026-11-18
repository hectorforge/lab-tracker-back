"""DTOs de capa de servicio.

Los servicios reciben y devuelven estos objetos, nunca entidades ORM. Cada DTO
valida su propia estructura (Pydantic) y luego el repositorio hace el mapeo a
la tabla correspondiente.
"""

from .alumno_dto import (
    AlumnoDTO,
    CrearAlumnoDTO,
    ActualizarAlumnoDTO,
)
from .tipo_equipo_dto import (
    TipoEquipoDTO,
    CrearTipoEquipoDTO,
    ActualizarTipoEquipoDTO,
)
from .equipo_dto import EquipoDTO, CrearEquipoDTO, ActualizarEquipoDTO
from .licencia_dto import (
    LicenciaDTO,
    CrearLicenciaDTO,
    ActualizarLicenciaDTO,
)
from .matricula_dto import (
    MatriculaDTO,
    CrearMatriculaDTO,
    FilaMatriculaDTO,
    ErrorFilaExcelDTO,
    ResultadoCargaMatriculaDTO,
    ColumnaPlantillaDTO,
)

__all__ = [
    "AlumnoDTO",
    "CrearAlumnoDTO",
    "ActualizarAlumnoDTO",
    "TipoEquipoDTO",
    "CrearTipoEquipoDTO",
    "ActualizarTipoEquipoDTO",
    "EquipoDTO",
    "CrearEquipoDTO",
    "ActualizarEquipoDTO",
    "LicenciaDTO",
    "CrearLicenciaDTO",
    "ActualizarLicenciaDTO",
    "MatriculaDTO",
    "CrearMatriculaDTO",
    "FilaMatriculaDTO",
    "ErrorFilaExcelDTO",
    "ResultadoCargaMatriculaDTO",
    "ColumnaPlantillaDTO",
]
