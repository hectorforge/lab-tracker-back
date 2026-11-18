from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from app.api.security import requiere_admin, requiere_lectura
from app.domain.entities import Usuario
from app.api.api_response import ApiResponse
from app.infrastructure.database.database import get_session
from app.api.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.application.dtos import (
    ColumnaPlantillaDTO,
    MatriculaDTO,
    ResultadoCargaMatriculaDTO,
)
from app.infrastructure.repositories import (
    AlumnoRepository,
    HorarioRepository,
    MatriculaRepository,
)
from app.application.services import MatriculaService
from app.application.interfaces import AbstractMatriculaService
from sqlmodel import Session

router = APIRouter(prefix="/matriculas", tags=["Matrículas y Carga Masiva"])


def get_matricula_service(
    session: Session = Depends(get_session),
) -> AbstractMatriculaService:
    return MatriculaService(
        session=session,
        horario_repo=HorarioRepository(session),
        alumno_repo=AlumnoRepository(session),
        matricula_repo=MatriculaRepository(session),
    )


@router.post("/carga-excel", response_model=ApiResponse[ResultadoCargaMatriculaDTO])
def cargar_matriculas_desde_excel(
    horario_id: int = Form(..., description="ID del horario/turno destino"),
    permitir_parciales: bool = Form(
        False,
        description=(
            "Si es false (por defecto), cualquier fila con error cancela toda la carga. "
            "Si es true, se insertan solo las filas válidas y se reportan los errores."
        ),
    ),
    archivo: UploadFile = File(..., description="Archivo .xlsx con los matriculados"),
    service: AbstractMatriculaService = Depends(get_matricula_service),
    _: Usuario = Depends(requiere_admin),
):
    return ApiResponse.ok(
        service.cargar_matriculas_desde_excel(
            horario_id=horario_id,
            archivo=archivo.file,
            nombre_archivo=archivo.filename or "",
            permitir_parciales=permitir_parciales,
        ),
        message="Procesamiento del archivo finalizado.",
    )


@router.get("/plantilla", response_model=ApiResponse[list[ColumnaPlantillaDTO]])
def columnas_plantilla(
    service: AbstractMatriculaService = Depends(get_matricula_service),
    _: Usuario = Depends(requiere_lectura),
):
    return ApiResponse.ok(
        service.columnas_plantilla(),
        message="Plantilla de columnas obtenida correctamente.",
    )


@router.get("/horario/{horario_id}", response_model=ApiResponse[Pagina[MatriculaDTO]])
def listar_matriculas_por_horario(
    horario_id: int,
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    service: AbstractMatriculaService = Depends(get_matricula_service),
    _: Usuario = Depends(requiere_lectura),
):
    return ApiResponse.ok(
        service.listar_matriculas_por_horario(paginacion, horario_id),
        message="Matrículas del horario obtenidas correctamente.",
    )


@router.delete("/{matricula_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_matricula(
    matricula_id: int,
    service: AbstractMatriculaService = Depends(get_matricula_service),
    _: Usuario = Depends(requiere_admin),
):
    service.eliminar_matricula(matricula_id)
