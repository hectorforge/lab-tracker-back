from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.lab_schemas import (
    IncidenteCreate,
    IncidenteUpdateEstado,
    IncidenteRead,
)
from app.repositories.incidente_repo import IncidenteRepository
from app.repositories.equipo_repo import EquipoRepository
from app.repositories.workstation_repo import WorkstationRepository
from app.services.interfaces import AbstractIncidenteService
from app.services.incidente_service import IncidenteService

router = APIRouter(prefix="/incidentes", tags=["Incidentes y Mantenimiento"])


def get_incidente_service(
    session: Session = Depends(get_session),
) -> AbstractIncidenteService:
    return IncidenteService(
        incidente_repo=IncidenteRepository(session),
        equipo_repo=EquipoRepository(session),
        ws_repo=WorkstationRepository(session),
    )


@router.post("/", response_model=IncidenteRead, status_code=status.HTTP_201_CREATED)
def reportar_incidente(
    data: IncidenteCreate,
    service: AbstractIncidenteService = Depends(get_incidente_service),
):
    return service.reportar_incidente(data)


@router.get("/", response_model=List[IncidenteRead])
def listar_incidentes(
    solo_pendientes: bool = False,
    service: AbstractIncidenteService = Depends(get_incidente_service),
):
    return service.listar_incidentes(solo_pendientes)


@router.get("/equipo/{equipo_id}", response_model=List[IncidenteRead])
def listar_incidentes_por_equipo(
    equipo_id: int,
    service: AbstractIncidenteService = Depends(get_incidente_service),
):
    return service.listar_por_equipo(equipo_id)


@router.get("/workstation/{workstation_id}", response_model=List[IncidenteRead])
def listar_incidentes_por_workstation(
    workstation_id: int,
    service: AbstractIncidenteService = Depends(get_incidente_service),
):
    return service.listar_por_workstation(workstation_id)


@router.patch("/{incidente_id}/estado", response_model=IncidenteRead)
def actualizar_estado_incidente(
    incidente_id: int,
    data: IncidenteUpdateEstado,
    service: AbstractIncidenteService = Depends(get_incidente_service),
):
    return service.actualizar_estado(incidente_id, data)