"""Contrato de persistencia para la entidad :class:`Alumno`."""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Set

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import Alumno, EstadoAlumno


class AbstractAlumnoRepository(ABC):
    """Puerto de salida para datos personales y académicos de estudiantes."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Alumno]:
        """Recupera un alumno por su clave primaria.

        Args:
            id (int): Identificador único de la fila en ``alumnos``.

        Returns:
            Optional[Alumno]: Entidad encontrada o ``None`` si no existe.
        """
        pass

    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[Alumno]:
        """Busca un alumno por su código institucional único.

        Args:
            codigo (str): Código del estudiante; se normaliza a mayúsculas.

        Returns:
            Optional[Alumno]: Alumno coincidente o ``None``.
        """
        pass

    @abstractmethod
    def get_by_correo(self, correo: str) -> Optional[Alumno]:
        """Busca un alumno por su correo institucional.

        Args:
            correo (str): Correo a buscar; se normaliza a minúsculas.

        Returns:
            Optional[Alumno]: Alumno coincidente o ``None``.

        Note:
            Permite validar unicidad antes de crear o actualizar un alumno.
        """
        pass

    @abstractmethod
    def get_by_codigos(self, codigos: Set[str]) -> Dict[str, Alumno]:
        """Obtiene varios alumnos en una sola consulta por sus códigos.

        Args:
            codigos (Set[str]): Conjunto de códigos institucionales. Si está
                vacío, el resultado es un diccionario vacío sin acceder a la BD.

        Returns:
            Dict[str, Alumno]: Mapa ``codigo -> Alumno`` de los registros
            existentes. Los códigos inexistentes no aparecen en el mapa.

        Note:
            Se emplea en la carga masiva para reutilizar alumnos ya registrados.
        """
        pass

    @abstractmethod
    def get_by_correos(self, correos: Set[str]) -> Set[str]:
        """Determina qué correos ya están registrados en la base de datos.

        Args:
            correos (Set[str]): Conjunto de correos institucionales a verificar.

        Returns:
            Set[str]: Subconjunto de correos que ya pertenecen a algún alumno.
        """
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        carrera: Optional[str] = None,
        estado: Optional[EstadoAlumno] = None,
        busqueda: Optional[str] = None,
    ) -> Pagina[Alumno]:
        """Lista alumnos paginados aplicando filtros en la consulta.

        Args:
            paginacion (ParametrosPaginacion): Página, tamaño y cálculo de totales.
            carrera (Optional[str]): Filtro parcial por programa académico.
            estado (Optional[EstadoAlumno]): Filtro por estado del alumno.
            busqueda (Optional[str]): Término libre que se aplica sobre nombres,
                apellidos, código y correo institucional.

        Returns:
            Pagina[Alumno]: Página de alumnos ordenada por apellidos y nombres.
        """
        pass

    @abstractmethod
    def create(self, obj: Alumno) -> Alumno:
        """Persiste un alumno nuevo.

        Args:
            obj (Alumno): Entidad validada por la capa de aplicación.

        Returns:
            Alumno: Entidad creada con su ``id`` asignado.
        """
        pass

    @abstractmethod
    def update(self, obj: Alumno) -> Alumno:
        """Actualiza un alumno existente.

        Args:
            obj (Alumno): Entidad modificada a persistir.

        Returns:
            Alumno: Entidad actualizada y refrescada.
        """
        pass

    @abstractmethod
    def delete(self, obj: Alumno) -> None:
        """Elimina un alumno sin matrículas asociadas.

        Args:
            obj (Alumno): Entidad a eliminar. La capa de aplicación valida
                previamente que no tenga matrículas registradas.

        Returns:
            None
        """
        pass
