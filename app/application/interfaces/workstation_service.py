"""Contrato de la capa de aplicación para la gestión de workstations."""

from abc import ABC, abstractmethod

from app.api.pagination import Pagina, ParametrosPaginacion
from app.application.dtos import (
    ActualizarWorkstationDTO,
    CrearWorkstationDTO,
    WorkstationDTO,
)


class AbstractWorkstationService(ABC):
    """Operaciones de negocio sobre puestos de trabajo."""

    @abstractmethod
    def crear_workstation(self, data: CrearWorkstationDTO) -> WorkstationDTO:
        """Registra una workstation respetando la capacidad del laboratorio.

        Args:
            data (CrearWorkstationDTO): Datos del puesto y su laboratorio.

        Returns:
            WorkstationDTO: Workstation creada.

        Raises:
            NotFoundException: Si el laboratorio indicado no existe.
            BadRequestException: Si el código ya existe en el laboratorio o
                si se alcanzó la capacidad máxima de puestos.
        """
        pass

    @abstractmethod
    def listar_por_laboratorio(
        self, paginacion: ParametrosPaginacion, lab_id: int
    ) -> Pagina[WorkstationDTO]:
        """Lista las workstations de un laboratorio, paginadas.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            lab_id (int): Identificador del laboratorio propietario.

        Returns:
            Pagina[WorkstationDTO]: Página de puestos de trabajo.

        Raises:
            NotFoundException: Si el laboratorio no existe.
        """
        pass

    @abstractmethod
    def obtener_workstation(self, workstation_id: int) -> WorkstationDTO:
        """Obtiene una workstation por su identificador.

        Args:
            workstation_id (int): Identificador del puesto.

        Returns:
            WorkstationDTO: Workstation encontrada.

        Raises:
            NotFoundException: Si el puesto no existe.
        """
        pass

    @abstractmethod
    def actualizar_workstation(
        self, workstation_id: int, data: ActualizarWorkstationDTO
    ) -> WorkstationDTO:
        """Actualiza una workstation y valida un posible cambio de laboratorio.

        Args:
            workstation_id (int): Identificador del puesto a modificar.
            data (ActualizarWorkstationDTO): Campos a actualizar.

        Returns:
            WorkstationDTO: Workstation actualizada.

        Raises:
            NotFoundException: Si la workstation o el laboratorio destino
                no existen.
            BadRequestException: Si el código se repite en el laboratorio
                destino o no hay capacidad disponible.
        """
        pass

    @abstractmethod
    def eliminar_workstation(self, workstation_id: int) -> None:
        """Elimina una workstation del laboratorio.

        Args:
            workstation_id (int): Identificador del puesto a eliminar.

        Returns:
            None

        Raises:
            NotFoundException: Si el puesto no existe.
        """
        pass
