"""Contrato de persistencia para la entidad :class:`Incidente`."""

from abc import ABC, abstractmethod
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import Incidente


class AbstractIncidenteRepository(ABC):
    """Puerto de salida para incidentes y mantenimiento de laboratorios."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Incidente]:
        """Recupera un incidente por su clave primaria.

        Args:
            id (int): Identificador único de la fila en ``incidentes``.

        Returns:
            Optional[Incidente]: Entidad encontrada o ``None`` si no existe.
        """
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        solo_pendientes: bool = False,
        equipo_id: Optional[int] = None,
        workstation_id: Optional[int] = None,
    ) -> Pagina[Incidente]:
        """Lista incidentes paginados con filtros opcionales.

        Args:
            paginacion (ParametrosPaginacion): Página, tamaño y cálculo de totales.
            solo_pendientes (bool): Si es ``True``, incluye únicamente estados
                ``pendiente`` y ``en_proceso``.
            equipo_id (Optional[int]): Filtra por equipo afectado.
            workstation_id (Optional[int]): Filtra por workstation afectada.

        Returns:
            Pagina[Incidente]: Página de incidentes con metadata de paginación.
        """
        pass

    @abstractmethod
    def create(self, obj: Incidente) -> Incidente:
        """Persiste un incidente nuevo.

        Args:
            obj (Incidente): Entidad validada por la capa de aplicación.

        Returns:
            Incidente: Entidad creada con su ``id`` asignado.
        """
        pass

    @abstractmethod
    def update(self, obj: Incidente) -> Incidente:
        """Actualiza un incidente existente (estado, resolución, imágenes).

        Args:
            obj (Incidente): Entidad modificada a persistir.

        Returns:
            Incidente: Entidad actualizada y refrescada.
        """
        pass

    @abstractmethod
    def count_abiertos_por_equipo(self, equipo_id: int) -> int:
        """Cuenta los incidentes abiertos de un equipo.

        Args:
            equipo_id (int): Identificador del equipo.

        Returns:
            int: Cantidad de incidentes en estado ``pendiente`` o ``en_proceso``.

        Note:
            Se usa para decidir si un equipo puede volver a ``operativo``.
        """
        pass

    @abstractmethod
    def count_abiertos_por_workstation(self, workstation_id: int) -> int:
        """Cuenta los incidentes abiertos de una workstation.

        Args:
            workstation_id (int): Identificador de la workstation.

        Returns:
            int: Cantidad de incidentes en estado ``pendiente`` o ``en_proceso``.
        """
        pass
