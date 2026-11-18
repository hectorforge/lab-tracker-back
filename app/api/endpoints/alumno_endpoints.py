from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.api.api_response import ApiResponse
from app.infrastructure.database.database import get_session
from app.api.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.application.dtos import ActualizarAlumnoDTO, CrearAlumnoDTO, AlumnoDTO
from app.domain.entities import EstadoAlumno
from app.infrastructure.repositories import AlumnoRepository
from app.application.services import AlumnoService
from app.application.interfaces import AbstractAlumnoService
from sqlmodel import Session

router = APIRouter(prefix="/alumnos", tags=["Gestión de Alumnos"])


def get_alumno_service(
    session: Session = Depends(get_session),
) -> AbstractAlumnoService:
    return AlumnoService(alumno_repo=AlumnoRepository(session))


@router.post(
    "/", response_model=ApiResponse[AlumnoDTO], status_code=status.HTTP_201_CREATED
)
def crear_alumno(
    data: CrearAlumnoDTO,
    service: AbstractAlumnoService = Depends(get_alumno_service),
):
    return ApiResponse.ok(
        service.crear_alumno(data),
        message="Alumno registrado correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=ApiResponse[Pagina[AlumnoDTO]])
def listar_alumnos(
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    carrera: Optional[str] = Query(default=None),
    estado: Optional[EstadoAlumno] = Query(default=None),
    busqueda: Optional[str] = Query(default=None),
    service: AbstractAlumnoService = Depends(get_alumno_service),
):
    return ApiResponse.ok(
        service.listar_alumnos(paginacion, carrera, estado, busqueda),
        message="Lista de alumnos obtenida correctamente.",
    )


@router.get("/{alumno_id}", response_model=ApiResponse[AlumnoDTO])
def obtener_alumno(
    alumno_id: int,
    service: AbstractAlumnoService = Depends(get_alumno_service),
):
    return ApiResponse.ok(
        service.obtener_alumno(alumno_id), message="Alumno obtenido correctamente."
    )


@router.put("/{alumno_id}", response_model=ApiResponse[AlumnoDTO])
def actualizar_alumno(
    alumno_id: int,
    data: ActualizarAlumnoDTO,
    service: AbstractAlumnoService = Depends(get_alumno_service),
):
    return ApiResponse.ok(
        service.actualizar_alumno(
            alumno_id, data
        ),
        message="Alumno actualizado correctamente.",
    )


@router.delete("/{alumno_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_alumno(
    alumno_id: int,
    service: AbstractAlumnoService = Depends(get_alumno_service),
):
    service.eliminar_alumno(alumno_id)
