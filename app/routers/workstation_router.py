from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.lab_schemas import (
    WorkstationCreate,
    WorkstationUpdate,
    WorkstationRead,
)
from app.repositories.workstation_repo import WorkstationRepository
from app.repositories.laboratorio_repo import LaboratorioRepository
from app.services.interfaces import AbstractWorkstationService
from app.services.workstation_service import WorkstationService

router = APIRouter(prefix="/workstations", tags=["Workstations"])


def get_workstation_service(
    session: Session = Depends(get_session),
) -> AbstractWorkstationService:
    return WorkstationService(
        ws_repo=WorkstationRepository(session),
        lab_repo=LaboratorioRepository(session),
    )


@router.post("/", response_model=WorkstationRead, status_code=status.HTTP_201_CREATED)
def crear_workstation(
    data: WorkstationCreate,
    service: AbstractWorkstationService = Depends(get_workstation_service),
):
    return service.crear_workstation(data)


@router.get("/laboratorio/{lab_id}", response_model=List[WorkstationRead])
def listar_workstations_por_laboratorio(
    lab_id: int,
    service: AbstractWorkstationService = Depends(get_workstation_service),
):
    return service.listar_por_laboratorio(lab_id)


@router.get("/{workstation_id}", response_model=WorkstationRead)
def obtener_workstation(
    workstation_id: int,
    service: AbstractWorkstationService = Depends(get_workstation_service),
):
    return service.obtener_workstation(workstation_id)


@router.put("/{workstation_id}", response_model=WorkstationRead)
def actualizar_workstation(
    workstation_id: int,
    data: WorkstationUpdate,
    service: AbstractWorkstationService = Depends(get_workstation_service),
):
    return service.actualizar_workstation(workstation_id, data)


@router.delete("/{workstation_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_workstation(
    workstation_id: int,
    service: AbstractWorkstationService = Depends(get_workstation_service),
):
    service.eliminar_workstation(workstation_id)