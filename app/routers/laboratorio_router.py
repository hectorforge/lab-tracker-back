from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.api_response import ApiResponse
from app.core.database import get_session
from app.core.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.repositories.implementaciones import (
    LaboratorioRepository,
    WorkstationRepository,
)
from app.schemas.lab_schemas import LaboratorioCreate, LaboratorioRead, LaboratorioUpdate
from app.services.implementaciones import LaboratorioService
from app.services.interfaces import AbstractLaboratorioService

router = APIRouter(prefix="/laboratorios", tags=["Laboratorios"])


def get_laboratorio_service(
    session: Session = Depends(get_session),
) -> AbstractLaboratorioService:
    return LaboratorioService(
        lab_repo=LaboratorioRepository(session),
        ws_repo=WorkstationRepository(session),
    )


@router.post(
    "/", response_model=ApiResponse[LaboratorioRead], status_code=status.HTTP_201_CREATED
)
def crear_laboratorio(
    data: LaboratorioCreate,
    service: AbstractLaboratorioService = Depends(get_laboratorio_service),
):
    return ApiResponse.ok(
        service.crear_laboratorio(data),
        message="Laboratorio registrado correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=ApiResponse[Pagina[LaboratorioRead]])
def listar_laboratorios(
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    solo_disponibles: bool = False,
    service: AbstractLaboratorioService = Depends(get_laboratorio_service),
):
    return ApiResponse.ok(
        service.listar_laboratorios(paginacion, solo_disponibles),
        message="Lista de laboratorios obtenida correctamente.",
    )


@router.get("/{lab_id}", response_model=ApiResponse[LaboratorioRead])
def obtener_laboratorio(
    lab_id: int,
    service: AbstractLaboratorioService = Depends(get_laboratorio_service),
):
    return ApiResponse.ok(
        service.obtener_laboratorio(lab_id),
        message="Laboratorio obtenido correctamente.",
    )


@router.put("/{lab_id}", response_model=ApiResponse[LaboratorioRead])
def actualizar_laboratorio(
    lab_id: int,
    data: LaboratorioUpdate,
    service: AbstractLaboratorioService = Depends(get_laboratorio_service),
):
    return ApiResponse.ok(
        service.actualizar_laboratorio(lab_id, data),
        message="Laboratorio actualizado correctamente.",
    )


@router.delete("/{lab_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_laboratorio(
    lab_id: int,
    service: AbstractLaboratorioService = Depends(get_laboratorio_service),
):
    service.eliminar_laboratorio(lab_id)
