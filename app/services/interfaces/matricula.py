from abc import ABC, abstractmethod
from typing import BinaryIO, List

from app.core.pagination import Pagina, ParametrosPaginacion
from app.dtos import (
    ColumnaPlantillaDTO,
    MatriculaDTO,
    ResultadoCargaMatriculaDTO,
)


class AbstractMatriculaService(ABC):
    @abstractmethod
    def cargar_matriculas_desde_excel(
        self,
        horario_id: int,
        archivo: BinaryIO,
        nombre_archivo: str,
        permitir_parciales: bool = False,
    ) -> ResultadoCargaMatriculaDTO:
        """
        Procesa un .xlsx y matricula alumnos únicamente en el horario indicado.

        Los DTOs validan la estructura de cada fila; el servicio aplica las
        reglas de negocio y devuelve un reporte detallado con rollback atómico
        por defecto.
        """
        pass

    @abstractmethod
    def listar_matriculas_por_horario(
        self, paginacion: ParametrosPaginacion, horario_id: int
    ) -> Pagina[MatriculaDTO]:
        """Lista paginadamente los alumnos matriculados en un turno."""
        pass

    @abstractmethod
    def eliminar_matricula(self, matricula_id: int) -> None:
        """Da de baja una matrícula existente."""
        pass

    @abstractmethod
    def columnas_plantilla(self) -> List[ColumnaPlantillaDTO]:
        """Describe las columnas requeridas y opcionales del Excel."""
        pass
