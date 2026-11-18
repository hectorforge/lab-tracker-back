from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.api.api_response import ApiResponse
from app.infrastructure.database.database import get_session
from app.api.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.domain.entities import EstadoHorario
from app.infrastructure.repositories import (
    HorarioRepository,
    LaboratorioRepository,
    WorkstationRepository,
)
from app.application.dtos import (
    AsignacionDTO,
    CrearAsignacionDTO,
    CrearHorarioDTO,
    HorarioDTO,
)
from app.application.services import HorarioService
from app.application.interfaces import AbstractHorarioService

router = APIRouter(prefix="/horarios", tags=["Horarios y Responsabilidad"])


def get_horario_service(
    session: Session = Depends(get_session),
) -> AbstractHorarioService:
    return HorarioService(
        horario_repo=HorarioRepository(session),
        lab_repo=LaboratorioRepository(session),
        ws_repo=WorkstationRepository(session),
    )


@router.post(
    "/", response_model=ApiResponse[HorarioDTO], status_code=status.HTTP_201_CREATED
)
def crear_horario(
    data: CrearHorarioDTO,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return ApiResponse.ok(
        service.crear_horario(data),
        message="Horario registrado correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=ApiResponse[Pagina[HorarioDTO]])
def listar_horarios(
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    laboratorio_id: Optional[int] = None,
    fecha: Optional[date] = None,
    estado: Optional[EstadoHorario] = None,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return ApiResponse.ok(
        service.listar_horarios(paginacion, laboratorio_id, fecha, estado),
        message="Lista de horarios obtenida correctamente.",
    )


@router.get("/{horario_id}", response_model=ApiResponse[HorarioDTO])
def obtener_horario(
    horario_id: int,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return ApiResponse.ok(
        service.obtener_horario(horario_id), message="Horario obtenido correctamente."
    )


@router.patch("/{horario_id}/iniciar", response_model=ApiResponse[HorarioDTO])
def iniciar_turno(
    horario_id: int,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return ApiResponse.ok(
        service.iniciar_turno(horario_id), message="Turno iniciado correctamente."
    )


@router.patch("/{horario_id}/finalizar", response_model=ApiResponse[HorarioDTO])
def finalizar_turno(
    horario_id: int,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return ApiResponse.ok(
        service.finalizar_turno(horario_id),
        message="Turno finalizado correctamente.",
    )


@router.patch("/{horario_id}/cancelar", response_model=ApiResponse[HorarioDTO])
def cancelar_turno(
    horario_id: int,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return ApiResponse.ok(
        service.cancelar_turno(horario_id), message="Turno cancelado correctamente."
    )


@router.post(
    "/{horario_id}/asignaciones",
    response_model=ApiResponse[AsignacionDTO],
    status_code=status.HTTP_201_CREATED,
)
def asignar_workstation_en_turno(
    horario_id: int,
    data: CrearAsignacionDTO,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return ApiResponse.ok(
        service.asignar_workstation(horario_id, data),
        message="Workstation asignada correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get(
    "/{horario_id}/asignaciones", response_model=ApiResponse[Pagina[AsignacionDTO]]
)
def listar_asignaciones_turno(
    horario_id: int,
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return ApiResponse.ok(
        service.listar_asignaciones_turno(paginacion, horario_id),
        message="Asignaciones del turno obtenidas correctamente.",
    )


@router.get(
    "/alumnos/{codigo_alumno}/historial",
    response_model=ApiResponse[Pagina[AsignacionDTO]],
)
def historial_responsabilidad_alumno(
    codigo_alumno: str,
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return ApiResponse.ok(
        service.consultar_historial_alumno(paginacion, codigo_alumno),
        message="Historial del alumno obtenido correctamente.",
    )
