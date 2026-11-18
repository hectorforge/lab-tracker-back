from abc import ABC, abstractmethod
from typing import Dict, Optional, Set

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import Alumno, EstadoAlumno


class AbstractAlumnoRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Alumno]:
        pass

    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[Alumno]:
        pass

    @abstractmethod
    def get_by_correo(self, correo: str) -> Optional[Alumno]:
        pass

    @abstractmethod
    def get_by_codigos(self, codigos: Set[str]) -> Dict[str, Alumno]:
        pass

    @abstractmethod
    def get_by_correos(self, correos: Set[str]) -> Set[str]:
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        carrera: Optional[str] = None,
        estado: Optional[EstadoAlumno] = None,
        busqueda: Optional[str] = None,
    ) -> Pagina[Alumno]:
        """Lista alumnos paginados y filtrados en la consulta."""
        pass

    @abstractmethod
    def create(self, obj: Alumno) -> Alumno:
        pass

    @abstractmethod
    def update(self, obj: Alumno) -> Alumno:
        pass

    @abstractmethod
    def delete(self, obj: Alumno) -> None:
        pass
