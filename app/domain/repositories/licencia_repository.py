"""Contrato de persistencia para la entidad :class:`Licencia`."""

from abc import ABC, abstractmethod
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import EstadoLicencia, Licencia


class AbstractLicenciaRepository(ABC):
    """Puerto de salida para licencias de software de los laboratorios."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Licencia]:
        """Recupera una licencia por su clave primaria.

        Args:
            id (int): Identificador único de la fila en ``licencias``.

        Returns:
            Optional[Licencia]: Entidad encontrada o ``None`` si no existe.
        """
        pass

    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[Licencia]:
        """Busca una licencia por su código único.

        Args:
            codigo (str): Código de la licencia; se normaliza a mayúsculas.

        Returns:
            Optional[Licencia]: Licencia coincidente o ``None``.
        """
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        equipo_id: Optional[int] = None,
        estado: Optional[EstadoLicencia] = None,
    ) -> Pagina[Licencia]:
        """Lista licencias paginadas con filtros opcionales.

        Args:
            paginacion (ParametrosPaginacion): Página, tamaño y cálculo de totales.
            equipo_id (Optional[int]): Filtra licencias asignadas a un equipo.
            estado (Optional[EstadoLicencia]): Filtra por estado de vigencia.

        Returns:
            Pagina[Licencia]: Página de licencias con metadata de paginación.
        """
        pass

    @abstractmethod
    def create(self, obj: Licencia) -> Licencia:
        """Persiste una licencia nueva.

        Args:
            obj (Licencia): Entidad validada por la capa de aplicación.

        Returns:
            Licencia: Entidad creada con su ``id`` asignado.
        """
        pass

    @abstractmethod
    def update(self, obj: Licencia) -> Licencia:
        """Actualiza una licencia existente.

        Args:
            obj (Licencia): Entidad modificada a persistir.

        Returns:
            Licencia: Entidad actualizada y refrescada.
        """
        pass

    @abstractmethod
    def delete(self, obj: Licencia) -> None:
        """Elimina una licencia del sistema.

        Args:
            obj (Licencia): Entidad a eliminar.

        Returns:
            None
        """
        pass
