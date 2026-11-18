"""Contrato de la capa de aplicación para matrículas y carga masiva."""

from abc import ABC, abstractmethod
from typing import BinaryIO, List

from app.api.pagination import Pagina, ParametrosPaginacion
from app.application.dtos import (
    ColumnaPlantillaDTO,
    MatriculaDTO,
    ResultadoCargaMatriculaDTO,
)


class AbstractMatriculaService(ABC):
    """Operaciones de negocio sobre la matrícula en turnos de laboratorio."""

    @abstractmethod
    def cargar_matriculas_desde_excel(
        self,
        horario_id: int,
        archivo: BinaryIO,
        nombre_archivo: str,
        permitir_parciales: bool = False,
    ) -> ResultadoCargaMatriculaDTO:
        """Procesa un ``.xlsx`` y matricula alumnos en un único horario.

        El servicio valida que el horario exista y esté activo, el formato y
        columnas del archivo, la integridad de cada fila mediante
        :class:`FilaMatriculaDTO`, los duplicados internos y las matrículas
        previas. Por defecto la operación es atómica: si hay errores por fila
        no se persiste nada y se devuelve el reporte.

        Args:
            horario_id (int): Turno destino; debe estar ``programado`` o
                ``en_curso``.
            archivo (BinaryIO): Flujo binario del archivo Excel subido.
            nombre_archivo (str): Nombre original, usado para validar la
                extensión ``.xlsx``.
            permitir_parciales (bool): Si es ``True``, se insertan únicamente
                las filas válidas y se reportan las inválidas.

        Returns:
            ResultadoCargaMatriculaDTO: Reporte con totales, filas con error
            y detalle de cada incidencia.

        Raises:
            NotFoundException: Si el horario indicado no existe.
            BusinessRuleException: Si el horario no está activo.
            FileValidationException: Si el archivo, la extensión o las
                columnas requeridas no son válidos.
            DatabaseException: Si ocurre un error crítico de persistencia;
                se realiza rollback completo antes de propagarlo.
        """
        pass

    @abstractmethod
    def listar_matriculas_por_horario(
        self, paginacion: ParametrosPaginacion, horario_id: int
    ) -> Pagina[MatriculaDTO]:
        """Lista paginadamente los alumnos matriculados en un turno.

        Args:
            paginacion (ParametrosPaginacion): Página y tamaño solicitados.
            horario_id (int): Turno cuyas matrículas se consultan.

        Returns:
            Pagina[MatriculaDTO]: Página de matrículas con el alumno anidado.

        Raises:
            NotFoundException: Si el horario no existe.
        """
        pass

    @abstractmethod
    def eliminar_matricula(self, matricula_id: int) -> None:
        """Da de baja una matrícula existente.

        Args:
            matricula_id (int): Identificador de la matrícula a eliminar.

        Returns:
            None

        Raises:
            NotFoundException: Si la matrícula no existe.
        """
        pass

    @abstractmethod
    def columnas_plantilla(self) -> List[ColumnaPlantillaDTO]:
        """Describe el formato esperado del archivo Excel.

        Returns:
            List[ColumnaPlantillaDTO]: Columnas requeridas y opcionales con
            su descripción, para que el cliente pueda generar la plantilla.
        """
        pass
