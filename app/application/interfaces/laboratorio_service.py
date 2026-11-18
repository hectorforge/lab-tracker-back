"""Contrato de la capa de aplicación para la gestión de laboratorios."""

from abc import ABC, abstractmethod

from app.api.pagination import Pagina, ParametrosPaginacion
from app.application.dtos import (
    ActualizarLaboratorioDTO,
    CrearLaboratorioDTO,
    LaboratorioDTO,
)


class AbstractLaboratorioService(ABC):
    """Operaciones de negocio sobre laboratorios.

    Todas las validaciones (unicidad de código, capacidad mínima, etc.) se
    resuelven aquí; los endpoints solo traducen HTTP a DTOs.
    """

    @abstractmethod
    def crear_laboratorio(self, data: CrearLaboratorioDTO) -> LaboratorioDTO:
        """Registra un laboratorio validando que su código no esté duplicado.

        Args:
            data (CrearLaboratorioDTO): Datos validados del nuevo laboratorio.

        Returns:
            LaboratorioDTO: Laboratorio creado, ya mapeado a DTO de salida.

        Raises:
            BadRequestException: Si el código institucional ya existe.
        """
        pass

    @abstractmethod
    def listar_laboratorios(
        self, paginacion: ParametrosPaginacion, solo_disponibles: bool = False
    ) -> Pagina[LaboratorioDTO]:
        """Lista laboratorios con paginación aplicada en el repositorio.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            solo_disponibles (bool): Filtra únicamente laboratorios disponibles.

        Returns:
            Pagina[LaboratorioDTO]: Página de DTOs con metadata de paginación.
        """
        pass

    @abstractmethod
    def obtener_laboratorio(self, lab_id: int) -> LaboratorioDTO:
        """Obtiene un laboratorio por su identificador.

        Args:
            lab_id (int): Identificador del laboratorio.

        Returns:
            LaboratorioDTO: Laboratorio encontrado.

        Raises:
            NotFoundException: Si no existe un laboratorio con ese ID.
        """
        pass

    @abstractmethod
    def actualizar_laboratorio(
        self, lab_id: int, data: ActualizarLaboratorioDTO
    ) -> LaboratorioDTO:
        """Actualiza un laboratorio validando unicidad y capacidad.

        Args:
            lab_id (int): Identificador del laboratorio a modificar.
            data (ActualizarLaboratorioDTO): Campos a actualizar; los no
                enviados se omiten.

        Returns:
            LaboratorioDTO: Laboratorio actualizado.

        Raises:
            NotFoundException: Si el laboratorio no existe.
            BadRequestException: Si el código ya está en uso o la nueva
                capacidad es menor que el número de workstations registradas.
        """
        pass

    @abstractmethod
    def eliminar_laboratorio(self, lab_id: int) -> None:
        """Elimina un laboratorio del sistema.

        Args:
            lab_id (int): Identificador del laboratorio a eliminar.

        Returns:
            None

        Raises:
            NotFoundException: Si el laboratorio no existe.
        """
        pass
