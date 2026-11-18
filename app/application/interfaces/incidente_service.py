"""Contrato de la capa de aplicación para incidentes y mantenimiento."""

from abc import ABC, abstractmethod

from app.api.pagination import Pagina, ParametrosPaginacion
from app.application.dtos import (
    ActualizarEstadoIncidenteDTO,
    CrearIncidenteDTO,
    IncidenteDTO,
)


class AbstractIncidenteService(ABC):
    """Operaciones de negocio sobre fallas reportadas y su resolución."""

    @abstractmethod
    def reportar_incidente(self, data: CrearIncidenteDTO) -> IncidenteDTO:
        """Registra un incidente y marca el equipo/puesto como con falla.

        Args:
            data (CrearIncidenteDTO): Equipo o workstation afectada,
                descripción, prioridad y enlaces a fotos del fallo.

        Returns:
            IncidenteDTO: Incidente creado en estado ``pendiente``.

        Raises:
            NotFoundException: Si el equipo o la workstation indicados
                no existen.
            BadRequestException: Si el equipo no pertenece a la workstation.
        """
        pass

    @abstractmethod
    def listar_incidentes(
        self, paginacion: ParametrosPaginacion, solo_pendientes: bool = False
    ) -> Pagina[IncidenteDTO]:
        """Lista incidentes paginados.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            solo_pendientes (bool): Si es ``True``, limita a estados
                ``pendiente`` y ``en_proceso``.

        Returns:
            Pagina[IncidenteDTO]: Página de incidentes.
        """
        pass

    @abstractmethod
    def listar_por_equipo(
        self, paginacion: ParametrosPaginacion, equipo_id: int
    ) -> Pagina[IncidenteDTO]:
        """Lista el historial paginado de incidentes de un equipo.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            equipo_id (int): Identificador del equipo.

        Returns:
            Pagina[IncidenteDTO]: Incidentes del equipo.
        """
        pass

    @abstractmethod
    def listar_por_workstation(
        self, paginacion: ParametrosPaginacion, workstation_id: int
    ) -> Pagina[IncidenteDTO]:
        """Lista el historial paginado de incidentes de una workstation.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            workstation_id (int): Identificador del puesto de trabajo.

        Returns:
            Pagina[IncidenteDTO]: Incidentes del puesto.
        """
        pass

    @abstractmethod
    def actualizar_estado(
        self, incidente_id: int, data: ActualizarEstadoIncidenteDTO
    ) -> IncidenteDTO:
        """Cambia el estado del incidente y sincroniza el equipo/workstation.

        Al resolver, agrega las imágenes de reparación y devuelve los recursos
        a ``operativo``/``disponible`` solo si no quedan incidentes abiertos.

        Args:
            incidente_id (int): Identificador del incidente.
            data (ActualizarEstadoIncidenteDTO): Nuevo estado y, opcionalmente,
                enlaces a fotos de la reparación.

        Returns:
            IncidenteDTO: Incidente actualizado con el historial de imágenes.

        Raises:
            NotFoundException: Si el incidente no existe.
        """
        pass
