"""Caso de uso: cargar matriculados desde un archivo Excel.

Coordina al servicio de aplicación dejando un punto único para futuras
extensiones (auditoría, notificaciones, almacenamiento del archivo, etc.).
"""

from typing import BinaryIO

from app.application.interfaces import AbstractMatriculaService
from app.application.dtos import ResultadoCargaMatriculaDTO


class CargarMatriculasUseCase:
    def __init__(self, service: AbstractMatriculaService):
        self.service = service

    def ejecutar(
        self,
        horario_id: int,
        archivo: BinaryIO,
        nombre_archivo: str,
        permitir_parciales: bool = False,
    ) -> ResultadoCargaMatriculaDTO:
        if horario_id <= 0:
            raise ValueError("El horario_id debe ser un entero positivo.")
        return self.service.cargar_matriculas_desde_excel(
            horario_id=horario_id,
            archivo=archivo,
            nombre_archivo=nombre_archivo,
            permitir_parciales=permitir_parciales,
        )
