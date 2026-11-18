from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.core.api_response import ApiResponse
from app.core.database import get_session
from app.core.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.dtos import ActualizarAlumnoDTO, CrearAlumnoDTO
from app.models import EstadoAlumno
from app.repositories.implementaciones import AlumnoRepository
from app.schemas.lab_schemas import AlumnoCreate, AlumnoRead, AlumnoUpdate
from app.services.implementaciones import AlumnoService
from app.services.interfaces import AbstractAlumnoService
from sqlmodel import Session

router = APIRouter(prefix="/alumnos", tags=["Gestión de Alumnos"])


def get_alumno_service(
    session: Session = Depends(get_session),
) -> AbstractAlumnoService:
    return AlumnoService(alumno_repo=AlumnoRepository(session))


@router.post(
    "/", response_model=ApiResponse[AlumnoRead], status_code=status.HTTP_201_CREATED
)
def crear_alumno(
    data: AlumnoCreate,
    service: AbstractAlumnoService = Depends(get_alumno_service),
):
    return ApiResponse.ok(
        service.crear_alumno(CrearAlumnoDTO.model_validate(data)),
        message="Alumno registrado correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=ApiResponse[Pagina[AlumnoRead]])
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


@router.get("/{alumno_id}", response_model=ApiResponse[AlumnoRead])
def obtener_alumno(
    alumno_id: int,
    service: AbstractAlumnoService = Depends(get_alumno_service),
):
    return ApiResponse.ok(
        service.obtener_alumno(alumno_id), message="Alumno obtenido correctamente."
    )


@router.put("/{alumno_id}", response_model=ApiResponse[AlumnoRead])
def actualizar_alumno(
    alumno_id: int,
    data: AlumnoUpdate,
    service: AbstractAlumnoService = Depends(get_alumno_service),
):
    return ApiResponse.ok(
        service.actualizar_alumno(
            alumno_id, ActualizarAlumnoDTO.model_validate(data)
        ),
        message="Alumno actualizado correctamente.",
    )


@router.delete("/{alumno_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_alumno(
    alumno_id: int,
    service: AbstractAlumnoService = Depends(get_alumno_service),
):
    service.eliminar_alumno(alumno_id)
