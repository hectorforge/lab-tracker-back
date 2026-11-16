from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.lab_schemas import (
    HorarioCreate,
    HorarioRead,
    AsignacionCreate,
    AsignacionRead,
)
from app.repositories.horario_repo import HorarioRepository
from app.repositories.laboratorio_repo import LaboratorioRepository
from app.repositories.workstation_repo import WorkstationRepository
from app.services.interfaces import AbstractHorarioService
from app.services.horario_service import HorarioService

router = APIRouter(prefix="/horarios", tags=["Horarios y Responsabilidad"])


def get_horario_service(
    session: Session = Depends(get_session),
) -> AbstractHorarioService:
    return HorarioService(
        horario_repo=HorarioRepository(session),
        lab_repo=LaboratorioRepository(session),
        ws_repo=WorkstationRepository(session),
    )


@router.post("/", response_model=HorarioRead, status_code=status.HTTP_201_CREATED)
def crear_horario(
    data: HorarioCreate,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return service.crear_horario(data)


@router.get("/", response_model=List[HorarioRead])
def listar_horarios(
    laboratorio_id: Optional[int] = None,
    fecha: Optional[date] = None,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return service.listar_horarios(laboratorio_id, fecha)


@router.get("/{horario_id}", response_model=HorarioRead)
def obtener_horario(
    horario_id: int,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return service.obtener_horario(horario_id)


@router.patch("/{horario_id}/iniciar", response_model=HorarioRead)
def iniciar_turno(
    horario_id: int,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return service.iniciar_turno(horario_id)


@router.patch("/{horario_id}/finalizar", response_model=HorarioRead)
def finalizar_turno(
    horario_id: int,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return service.finalizar_turno(horario_id)


@router.patch("/{horario_id}/cancelar", response_model=HorarioRead)
def cancelar_turno(
    horario_id: int,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return service.cancelar_turno(horario_id)


@router.post(
    "/{horario_id}/asignaciones",
    response_model=AsignacionRead,
    status_code=status.HTTP_201_CREATED,
)
def asignar_workstation_en_turno(
    horario_id: int,
    data: AsignacionCreate,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return service.asignar_workstation(horario_id, data)


@router.get("/{horario_id}/asignaciones", response_model=List[AsignacionRead])
def listar_asignaciones_turno(
    horario_id: int,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return service.listar_asignaciones_turno(horario_id)


@router.get("/alumnos/{codigo_alumno}/historial", response_model=List[AsignacionRead])
def historial_responsabilidad_alumno(
    codigo_alumno: str,
    service: AbstractHorarioService = Depends(get_horario_service),
):
    return service.consultar_historial_alumno(codigo_alumno)