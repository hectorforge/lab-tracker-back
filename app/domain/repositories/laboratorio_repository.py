"""Contrato de persistencia para la entidad :class:`Laboratorio`.

Define las operaciones de acceso a datos sin acoplar la capa de dominio a
SQLAlchemy ni a FastAPI. Las implementaciones concretas residen en
``infrastructure/repositories``.
"""

from abc import ABC, abstractmethod
from typing import Optional

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import EstadoLaboratorio, Laboratorio


class AbstractLaboratorioRepository(ABC):
    """Puerto de salida para consultar y persistir laboratorios."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Laboratorio]:
        """Recupera un laboratorio por su clave primaria.

        Args:
            id (int): Identificador único de la fila en ``laboratorios``.

        Returns:
            Optional[Laboratorio]: Entidad encontrada o ``None`` si el
            identificador no existe.

        Note:
            Este contrato no lanza errores de negocio; la decisión de
            traducir ``None`` en un error 404 corresponde a la capa de aplicación.
        """
        pass

    @abstractmethod
    def listar(
        self, paginacion: ParametrosPaginacion, solo_disponibles: bool = False
    ) -> Pagina[Laboratorio]:
        """Lista laboratorios aplicando paginación y filtros en la consulta.

        Args:
            paginacion (ParametrosPaginacion): Número de página y tamaño de
                página; el repositorio calcula ``offset``, ``limit`` y totales.
            solo_disponibles (bool): Si es ``True``, restringe los resultados
                a laboratorios con estado ``DISPONIBLE``.

        Returns:
            Pagina[Laboratorio]: Página con los elementos, el total de
            registros y el número total de páginas.
        """
        pass

    @abstractmethod
    def create(self, obj: Laboratorio) -> Laboratorio:
        """Persiste un laboratorio nuevo y confirma la transacción.

        Args:
            obj (Laboratorio): Entidad validada por la capa de aplicación.

        Returns:
            Laboratorio: Entidad persistida con su ``id`` asignado y refrescada
            desde la base de datos.

        Raises:
            ValueError: Si la validación de integridad de la entidad falla.
        """
        pass

    @abstractmethod
    def update(self, obj: Laboratorio) -> Laboratorio:
        """Guarda los cambios de un laboratorio existente.

        Args:
            obj (Laboratorio): Entidad modificada, normalmente obtenida
                previamente con :meth:`get_by_id`.

        Returns:
            Laboratorio: Entidad actualizada y refrescada.

        Raises:
            ValueError: Si la entidad deja de cumplir sus invariantes.
        """
        pass

    @abstractmethod
    def delete(self, obj: Laboratorio) -> None:
        """Elimina físicamente un laboratorio.

        Args:
            obj (Laboratorio): Entidad a eliminar. Las relaciones dependientes
                se gestionan mediante ``cascade`` en el modelo.

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[Laboratorio]:
        """Busca un laboratorio por su código institucional único.

        Args:
            codigo (str): Código a buscar; se normaliza a mayúsculas.

        Returns:
            Optional[Laboratorio]: Laboratorio coincidente o ``None``.
        """
        pass
