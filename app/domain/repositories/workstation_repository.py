"""Contrato de persistencia para la entidad :class:`Workstation`."""

from abc import ABC, abstractmethod
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import Workstation


class AbstractWorkstationRepository(ABC):
    """Puerto de salida para puestos de trabajo de laboratorio."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Workstation]:
        """Recupera una workstation por su clave primaria.

        Args:
            id (int): Identificador único de la fila en ``workstations``.

        Returns:
            Optional[Workstation]: Entidad encontrada o ``None`` si no existe.
        """
        pass

    @abstractmethod
    def listar(
        self,
        paginacion: ParametrosPaginacion,
        laboratorio_id: Optional[int] = None,
    ) -> Pagina[Workstation]:
        """Lista workstations paginadas, opcionalmente por laboratorio.

        Args:
            paginacion (ParametrosPaginacion): Configuración de página, tamaño
                y cálculo de totales.
            laboratorio_id (Optional[int]): Si se indica, filtra los puestos
                pertenecientes a ese laboratorio.

        Returns:
            Pagina[Workstation]: Página de resultados con metadata de paginación.
        """
        pass

    @abstractmethod
    def create(self, obj: Workstation) -> Workstation:
        """Persiste una workstation nueva.

        Args:
            obj (Workstation): Entidad validada por la capa de aplicación.

        Returns:
            Workstation: Entidad creada con su ``id`` asignado.

        Raises:
            ValueError: Si la entidad no cumple sus invariantes.
        """
        pass

    @abstractmethod
    def update(self, obj: Workstation) -> Workstation:
        """Actualiza una workstation existente.

        Args:
            obj (Workstation): Entidad modificada a persistir.

        Returns:
            Workstation: Entidad actualizada y refrescada.
        """
        pass

    @abstractmethod
    def delete(self, obj: Workstation) -> None:
        """Elimina una workstation y sus relaciones dependientes.

        Args:
            obj (Workstation): Entidad a eliminar.

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_by_codigo_y_laboratorio(
        self, codigo: str, laboratorio_id: int
    ) -> Optional[Workstation]:
        """Busca una workstation por código dentro de un laboratorio.

        Args:
            codigo (str): Código interno del puesto (por ejemplo ``WS-01``).
            laboratorio_id (int): Laboratorio propietario del puesto.

        Returns:
            Optional[Workstation]: Workstation coincidente o ``None``.

        Note:
            Permite validar la unicidad del código por laboratorio antes de
            crear o mover un puesto a otro laboratorio.
        """
        pass
