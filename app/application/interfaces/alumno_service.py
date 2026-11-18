"""Contrato de la capa de aplicación para la gestión de alumnos."""

from abc import ABC, abstractmethod
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.application.dtos import (
    ActualizarAlumnoDTO,
    AlumnoDTO,
    CrearAlumnoDTO,
)
from app.domain.entities import EstadoAlumno


class AbstractAlumnoService(ABC):
    """Operaciones de negocio sobre datos personales y académicos."""

    @abstractmethod
    def crear_alumno(self, data: CrearAlumnoDTO) -> AlumnoDTO:
        """Registra un alumno validando código y correo institucional únicos.

        Args:
            data (CrearAlumnoDTO): Datos personales, de contacto y académicos.

        Returns:
            AlumnoDTO: Alumno creado con sus fechas de auditoría.

        Raises:
            BadRequestException: Si el código o el correo ya están registrados.
        """
        pass

    @abstractmethod
    def listar_alumnos(
        self,
        paginacion: ParametrosPaginacion,
        carrera: Optional[str] = None,
        estado: Optional[EstadoAlumno] = None,
        busqueda: Optional[str] = None,
    ) -> Pagina[AlumnoDTO]:
        """Lista alumnos paginados aplicando filtros de negocio.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            carrera (Optional[str]): Filtro parcial por programa académico.
            estado (Optional[EstadoAlumno]): Filtro por estado del alumno.
            busqueda (Optional[str]): Búsqueda libre sobre nombres, apellidos,
                código o correo.

        Returns:
            Pagina[AlumnoDTO]: Página de alumnos con metadata de paginación.
        """
        pass

    @abstractmethod
    def obtener_alumno(self, alumno_id: int) -> AlumnoDTO:
        """Obtiene un alumno por su identificador.

        Args:
            alumno_id (int): Identificador del alumno.

        Returns:
            AlumnoDTO: Alumno encontrado.

        Raises:
            NotFoundException: Si el alumno no existe.
        """
        pass

    @abstractmethod
    def actualizar_alumno(
        self, alumno_id: int, data: ActualizarAlumnoDTO
    ) -> AlumnoDTO:
        """Actualiza un alumno existente.

        Args:
            alumno_id (int): Identificador del alumno a modificar.
            data (ActualizarAlumnoDTO): Campos a actualizar.

        Returns:
            AlumnoDTO: Alumno actualizado.

        Raises:
            NotFoundException: Si el alumno no existe.
            BadRequestException: Si el código o correo ya pertenecen a otro alumno.
        """
        pass

    @abstractmethod
    def eliminar_alumno(self, alumno_id: int) -> None:
        """Elimina un alumno que no tenga matrículas registradas.

        Args:
            alumno_id (int): Identificador del alumno a eliminar.

        Returns:
            None

        Raises:
            NotFoundException: Si el alumno no existe.
            ConflictException: Si el alumno posee matrículas asociadas.
        """
        pass
