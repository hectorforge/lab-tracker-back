from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.api.security import requiere_admin, requiere_lectura
from app.domain.entities import Usuario
from app.api.api_response import ApiResponse
from app.infrastructure.database.database import get_session
from app.api.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.infrastructure.repositories import (
    LaboratorioRepository,
    WorkstationRepository,
)
from app.application.dtos import CrearWorkstationDTO, WorkstationDTO, ActualizarWorkstationDTO
from app.application.services import WorkstationService
from app.application.interfaces import AbstractWorkstationService

router = APIRouter(prefix="/workstations", tags=["Workstations"])


def get_workstation_service(
    session: Session = Depends(get_session),
) -> AbstractWorkstationService:
    return WorkstationService(
        ws_repo=WorkstationRepository(session),
        lab_repo=LaboratorioRepository(session),
    )


@router.post(
    "/", response_model=ApiResponse[WorkstationDTO], status_code=status.HTTP_201_CREATED
)
def crear_workstation(
    data: CrearWorkstationDTO,
    service: AbstractWorkstationService = Depends(get_workstation_service),
    _: Usuario = Depends(requiere_admin),
):
    return ApiResponse.ok(
        service.crear_workstation(data),
        message="Workstation registrada correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/laboratorio/{lab_id}", response_model=ApiResponse[Pagina[WorkstationDTO]])
def listar_workstations_por_laboratorio(
    lab_id: int,
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    service: AbstractWorkstationService = Depends(get_workstation_service),
    _: Usuario = Depends(requiere_lectura),
):
    return ApiResponse.ok(
        service.listar_por_laboratorio(paginacion, lab_id),
        message="Workstations del laboratorio obtenidas correctamente.",
    )


@router.get("/{workstation_id}", response_model=ApiResponse[WorkstationDTO])
def obtener_workstation(
    workstation_id: int,
    service: AbstractWorkstationService = Depends(get_workstation_service),
    _: Usuario = Depends(requiere_lectura),
):
    return ApiResponse.ok(
        service.obtener_workstation(workstation_id),
        message="Workstation obtenida correctamente.",
    )


@router.put("/{workstation_id}", response_model=ApiResponse[WorkstationDTO])
def actualizar_workstation(
    workstation_id: int,
    data: ActualizarWorkstationDTO,
    service: AbstractWorkstationService = Depends(get_workstation_service),
    _: Usuario = Depends(requiere_admin),
):
    return ApiResponse.ok(
        service.actualizar_workstation(workstation_id, data),
        message="Workstation actualizada correctamente.",
    )


@router.delete("/{workstation_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_workstation(
    workstation_id: int,
    service: AbstractWorkstationService = Depends(get_workstation_service),
    _: Usuario = Depends(requiere_admin),
):
    service.eliminar_workstation(workstation_id)
