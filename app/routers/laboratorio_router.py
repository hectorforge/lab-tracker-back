from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.lab_schemas import (
    LaboratorioCreate,
    LaboratorioUpdate,
    LaboratorioRead,
)
from app.repositories.laboratorio_repo import LaboratorioRepository
from app.repositories.workstation_repo import WorkstationRepository
from app.services.interfaces import AbstractLaboratorioService
from app.services.laboratorio_service import LaboratorioService

router = APIRouter(prefix="/laboratorios", tags=["Laboratorios"])


def get_laboratorio_service(
    session: Session = Depends(get_session),
) -> AbstractLaboratorioService:
    return LaboratorioService(
        lab_repo=LaboratorioRepository(session),
        ws_repo=WorkstationRepository(session),
    )


@router.post("/", response_model=LaboratorioRead, status_code=status.HTTP_201_CREATED)
def crear_laboratorio(
    data: LaboratorioCreate,
    service: AbstractLaboratorioService = Depends(get_laboratorio_service),
):
    return service.crear_laboratorio(data)


@router.get("/", response_model=List[LaboratorioRead])
def listar_laboratorios(
    solo_disponibles: bool = False,
    service: AbstractLaboratorioService = Depends(get_laboratorio_service),
):
    return service.listar_laboratorios(solo_disponibles)


@router.get("/{lab_id}", response_model=LaboratorioRead)
def obtener_laboratorio(
    lab_id: int,
    service: AbstractLaboratorioService = Depends(get_laboratorio_service),
):
    return service.obtener_laboratorio(lab_id)


@router.put("/{lab_id}", response_model=LaboratorioRead)
def actualizar_laboratorio(
    lab_id: int,
    data: LaboratorioUpdate,
    service: AbstractLaboratorioService = Depends(get_laboratorio_service),
):
    return service.actualizar_laboratorio(lab_id, data)


@router.delete("/{lab_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_laboratorio(
    lab_id: int,
    service: AbstractLaboratorioService = Depends(get_laboratorio_service),
):
    service.eliminar_laboratorio(lab_id)