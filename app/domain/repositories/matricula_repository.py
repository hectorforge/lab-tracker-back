"""Contrato de persistencia para la tabla intermedia :class:`Matricula`.

Representa la relación ``Alumno <-> Horario`` y la consulta de alumnos
matriculados por turno.
"""

from abc import ABC, abstractmethod
from typing import Optional, Set

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import Matricula


class AbstractMatriculaRepository(ABC):
    """Puerto de salida para matrículas de laboratorio."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Matricula]:
        """Recupera una matrícula por su clave primaria.

        Args:
            id (int): Identificador único de la fila en ``matriculas``.

        Returns:
            Optional[Matricula]: Entidad encontrada o ``None`` si no existe.
        """
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        horario_id: Optional[int] = None,
    ) -> Pagina[Matricula]:
        """Lista matrículas paginadas con el alumno precargado.

        Args:
            paginacion (ParametrosPaginacion): Página, tamaño y cálculo de totales.
            horario_id (Optional[int]): Si se indica, limita el resultado a un
                turno concreto.

        Returns:
            Pagina[Matricula]: Página de matrículas con la relación ``alumno``
            cargada para evitar consultas N+1.
        """
        pass

    @abstractmethod
    def get_codigos_matriculados(
        self, horario_id: int, codigos: Set[str]
    ) -> Set[str]:
        """Verifica qué alumnos ya están matriculados en un turno.

        Args:
            horario_id (int): Turno sobre el que se realiza la comprobación.
            codigos (Set[str]): Códigos institucionales a verificar.

        Returns:
            Set[str]: Subconjunto de códigos que ya poseen matrícula en el
            horario indicado.

        Note:
            Es la validación clave de la carga masiva para impedir duplicados.
        """
        pass

    @abstractmethod
    def get_por_alumno_y_horario(
        self, alumno_id: int, horario_id: int
    ) -> Optional[Matricula]:
        """Busca la matrícula de un alumno en un horario concreto.

        Args:
            alumno_id (int): Identificador del alumno.
            horario_id (int): Identificador del turno.

        Returns:
            Optional[Matricula]: Matrícula existente o ``None``.

        Note:
            Refleja la restricción de unicidad ``(alumno_id, horario_id)``.
        """
        pass

    @abstractmethod
    def create(self, obj: Matricula) -> Matricula:
        """Persiste una matrícula nueva.

        Args:
            obj (Matricula): Entidad validada por la capa de aplicación.

        Returns:
            Matricula: Entidad creada con su ``id`` asignado.
        """
        pass

    @abstractmethod
    def update(self, obj: Matricula) -> Matricula:
        """Actualiza una matrícula existente.

        Args:
            obj (Matricula): Entidad modificada a persistir.

        Returns:
            Matricula: Entidad actualizada y refrescada.
        """
        pass

    @abstractmethod
    def delete(self, obj: Matricula) -> None:
        """Elimina una matrícula (da de baja al alumno del turno).

        Args:
            obj (Matricula): Entidad a eliminar.

        Returns:
            None
        """
        pass
