from abc import ABC, abstractmethod
from typing import Optional, Set

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import Matricula


class AbstractMatriculaRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Matricula]:
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        horario_id: Optional[int] = None,
    ) -> Pagina[Matricula]:
        """Lista matrículas paginadas con los datos del alumno cargados."""
        pass

    @abstractmethod
    def get_codigos_matriculados(
        self, horario_id: int, codigos: Set[str]
    ) -> Set[str]:
        pass

    @abstractmethod
    def get_por_alumno_y_horario(
        self, alumno_id: int, horario_id: int
    ) -> Optional[Matricula]:
        pass

    @abstractmethod
    def create(self, obj: Matricula) -> Matricula:
        pass

    @abstractmethod
    def update(self, obj: Matricula) -> Matricula:
        pass

    @abstractmethod
    def delete(self, obj: Matricula) -> None:
        pass
