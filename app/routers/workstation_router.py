from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.api_response import ApiResponse
from app.core.database import get_session
from app.core.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.repositories.implementaciones import (
    LaboratorioRepository,
    WorkstationRepository,
)
from app.schemas.lab_schemas import WorkstationCreate, WorkstationRead, WorkstationUpdate
from app.services.implementaciones import WorkstationService
from app.services.interfaces import AbstractWorkstationService

router = APIRouter(prefix="/workstations", tags=["Workstations"])


def get_workstation_service(
    session: Session = Depends(get_session),
) -> AbstractWorkstationService:
    return WorkstationService(
        ws_repo=WorkstationRepository(session),
        lab_repo=LaboratorioRepository(session),
    )


@router.post(
    "/", response_model=ApiResponse[WorkstationRead], status_code=status.HTTP_201_CREATED
)
def crear_workstation(
    data: WorkstationCreate,
    service: AbstractWorkstationService = Depends(get_workstation_service),
):
    return ApiResponse.ok(
        service.crear_workstation(data),
        message="Workstation registrada correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/laboratorio/{lab_id}", response_model=ApiResponse[Pagina[WorkstationRead]])
def listar_workstations_por_laboratorio(
    lab_id: int,
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    service: AbstractWorkstationService = Depends(get_workstation_service),
):
    return ApiResponse.ok(
        service.listar_por_laboratorio(paginacion, lab_id),
        message="Workstations del laboratorio obtenidas correctamente.",
    )


@router.get("/{workstation_id}", response_model=ApiResponse[WorkstationRead])
def obtener_workstation(
    workstation_id: int,
    service: AbstractWorkstationService = Depends(get_workstation_service),
):
    return ApiResponse.ok(
        service.obtener_workstation(workstation_id),
        message="Workstation obtenida correctamente.",
    )


@router.put("/{workstation_id}", response_model=ApiResponse[WorkstationRead])
def actualizar_workstation(
    workstation_id: int,
    data: WorkstationUpdate,
    service: AbstractWorkstationService = Depends(get_workstation_service),
):
    return ApiResponse.ok(
        service.actualizar_workstation(workstation_id, data),
        message="Workstation actualizada correctamente.",
    )


@router.delete("/{workstation_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_workstation(
    workstation_id: int,
    service: AbstractWorkstationService = Depends(get_workstation_service),
):
    service.eliminar_workstation(workstation_id)
