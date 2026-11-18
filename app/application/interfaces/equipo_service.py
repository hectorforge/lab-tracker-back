"""Contrato de la capa de aplicación para el inventario de equipos."""

from abc import ABC, abstractmethod
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.application.dtos import (
    ActualizarEquipoDTO,
    CrearEquipoDTO,
    EquipoDTO,
)
from app.domain.entities import CategoriaTipoEquipo


class AbstractEquipoService(ABC):
    """Operaciones de negocio sobre equipos físicos y su catálogo."""

    @abstractmethod
    def registrar_equipo(self, data: CrearEquipoDTO) -> EquipoDTO:
        """Registra un equipo validando laboratorio, puesto y catálogo.

        Args:
            data (CrearEquipoDTO): Datos patrimoniales, económicos y de imagen.

        Returns:
            EquipoDTO: Equipo creado con su ``id`` y ``url_imagen``.

        Raises:
            NotFoundException: Si el laboratorio, la workstation o el tipo
                de equipo indicados no existen.
            BadRequestException: Si el código patrimonial ya está registrado,
                la workstation pertenece a otro laboratorio, el tipo no está
                activo o su categoría no coincide.
        """
        pass

    @abstractmethod
    def listar_equipos(self, paginacion: ParametrosPaginacion) -> Pagina[EquipoDTO]:
        """Lista todo el inventario paginado.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.

        Returns:
            Pagina[EquipoDTO]: Página de equipos con metadata de paginación.
        """
        pass

    @abstractmethod
    def listar_por_laboratorio(
        self,
        paginacion: ParametrosPaginacion,
        lab_id: int,
        categoria: Optional[CategoriaTipoEquipo] = None,
    ) -> Pagina[EquipoDTO]:
        """Lista los equipos de un laboratorio filtrando por categoría.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            lab_id (int): Laboratorio propietario de los equipos.
            categoria (Optional[CategoriaTipoEquipo]): Categoría genérica opcional.

        Returns:
            Pagina[EquipoDTO]: Página de equipos del laboratorio.

        Raises:
            NotFoundException: Si el laboratorio no existe.
        """
        pass

    @abstractmethod
    def listar_por_workstation(
        self, paginacion: ParametrosPaginacion, workstation_id: int
    ) -> Pagina[EquipoDTO]:
        """Lista los equipos asignados a una workstation.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            workstation_id (int): Identificador del puesto de trabajo.

        Returns:
            Pagina[EquipoDTO]: Página de equipos del puesto.

        Raises:
            NotFoundException: Si la workstation no existe.
        """
        pass

    @abstractmethod
    def obtener_equipo(self, equipo_id: int) -> EquipoDTO:
        """Obtiene un equipo por su identificador.

        Args:
            equipo_id (int): Identificador del equipo.

        Returns:
            EquipoDTO: Equipo encontrado.

        Raises:
            NotFoundException: Si el equipo no existe.
        """
        pass

    @abstractmethod
    def actualizar_equipo(
        self, equipo_id: int, data: ActualizarEquipoDTO
    ) -> EquipoDTO:
        """Actualiza un equipo existente.

        Args:
            equipo_id (int): Identificador del equipo a modificar.
            data (ActualizarEquipoDTO): Campos a actualizar, incluida
                ``url_imagen`` y los costos.

        Returns:
            EquipoDTO: Equipo actualizado.

        Raises:
            NotFoundException: Si el equipo, laboratorio, workstation o tipo
                indicados no existen.
            BadRequestException: Si el código patrimonial está duplicado o
                el tipo/categoría no son coherentes.
        """
        pass

    @abstractmethod
    def eliminar_equipo(self, equipo_id: int) -> None:
        """Elimina un equipo del inventario.

        Args:
            equipo_id (int): Identificador del equipo a eliminar.

        Returns:
            None

        Raises:
            NotFoundException: Si el equipo no existe.
        """
        pass
