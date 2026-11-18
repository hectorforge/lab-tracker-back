"""Contrato de persistencia para la entidad :class:`Equipo`."""

from abc import ABC, abstractmethod
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import CategoriaTipoEquipo, Equipo


class AbstractEquipoRepository(ABC):
    """Puerto de salida para el inventario físico de equipos tecnológicos."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Equipo]:
        """Recupera un equipo por su clave primaria.

        Args:
            id (int): Identificador único de la fila en ``equipos``.

        Returns:
            Optional[Equipo]: Entidad encontrada o ``None`` si no existe.
        """
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        laboratorio_id: Optional[int] = None,
        workstation_id: Optional[int] = None,
        categoria: Optional[CategoriaTipoEquipo] = None,
    ) -> Pagina[Equipo]:
        """Lista equipos paginados aplicando filtros opcionales en la consulta.

        Args:
            paginacion (ParametrosPaginacion): Página, tamaño y cálculo de totales.
            laboratorio_id (Optional[int]): Filtra por laboratorio propietario.
            workstation_id (Optional[int]): Filtra por puesto de trabajo asignado.
            categoria (Optional[CategoriaTipoEquipo]): Filtra por categoría
                genérica (hardware, software, redes, etc.).

        Returns:
            Pagina[Equipo]: Página de equipos con metadata de paginación.
        """
        pass

    @abstractmethod
    def create(self, obj: Equipo) -> Equipo:
        """Persiste un equipo nuevo en el inventario.

        Args:
            obj (Equipo): Entidad validada por la capa de aplicación.

        Returns:
            Equipo: Entidad creada con su ``id`` asignado.
        """
        pass

    @abstractmethod
    def update(self, obj: Equipo) -> Equipo:
        """Actualiza un equipo existente.

        Args:
            obj (Equipo): Entidad modificada a persistir.

        Returns:
            Equipo: Entidad actualizada y refrescada.
        """
        pass

    @abstractmethod
    def delete(self, obj: Equipo) -> None:
        """Elimina un equipo del inventario.

        Args:
            obj (Equipo): Entidad a eliminar.

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_by_codigo_patrimonial(self, codigo_patrimonial: str) -> Optional[Equipo]:
        """Busca un equipo por su código patrimonial único.

        Args:
            codigo_patrimonial (str): Código de inventario de la institución.

        Returns:
            Optional[Equipo]: Equipo coincidente o ``None``.

        Note:
            Se utiliza para garantizar la unicidad antes de registrar un equipo.
        """
        pass
