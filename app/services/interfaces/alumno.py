from abc import ABC, abstractmethod
from typing import Optional

from app.core.pagination import Pagina, ParametrosPaginacion
from app.dtos import ActualizarAlumnoDTO, AlumnoDTO, CrearAlumnoDTO
from app.models import EstadoAlumno


class AbstractAlumnoService(ABC):
    @abstractmethod
    def crear_alumno(self, data: CrearAlumnoDTO) -> AlumnoDTO:
        pass

    @abstractmethod
    def listar_alumnos(
        self,
        paginacion: ParametrosPaginacion,
        carrera: Optional[str] = None,
        estado: Optional[EstadoAlumno] = None,
        busqueda: Optional[str] = None,
    ) -> Pagina[AlumnoDTO]:
        pass

    @abstractmethod
    def obtener_alumno(self, alumno_id: int) -> AlumnoDTO:
        pass

    @abstractmethod
    def actualizar_alumno(self, alumno_id: int, data: ActualizarAlumnoDTO) -> AlumnoDTO:
        pass

    @abstractmethod
    def eliminar_alumno(self, alumno_id: int) -> None:
        pass
