from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.api.api_response import ApiResponse
from app.infrastructure.database.database import get_session
from app.api.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.infrastructure.repositories import (
    EquipoRepository,
    IncidenteRepository,
    WorkstationRepository,
)
from app.application.dtos import (
    ActualizarEstadoIncidenteDTO,
    CrearIncidenteDTO,
    IncidenteDTO,
)
from app.application.services import IncidenteService
from app.application.interfaces import AbstractIncidenteService

router = APIRouter(prefix="/incidentes", tags=["Incidentes y Mantenimiento"])


def get_incidente_service(
    session: Session = Depends(get_session),
) -> AbstractIncidenteService:
    return IncidenteService(
        incidente_repo=IncidenteRepository(session),
        equipo_repo=EquipoRepository(session),
        ws_repo=WorkstationRepository(session),
    )


@router.post(
    "/", response_model=ApiResponse[IncidenteDTO], status_code=status.HTTP_201_CREATED
)
def reportar_incidente(
    data: CrearIncidenteDTO,
    service: AbstractIncidenteService = Depends(get_incidente_service),
):
    return ApiResponse.ok(
        service.reportar_incidente(data),
        message="Incidente reportado correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=ApiResponse[Pagina[IncidenteDTO]])
def listar_incidentes(
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    solo_pendientes: bool = False,
    service: AbstractIncidenteService = Depends(get_incidente_service),
):
    return ApiResponse.ok(
        service.listar_incidentes(paginacion, solo_pendientes),
        message="Lista de incidentes obtenida correctamente.",
    )


@router.get("/equipo/{equipo_id}", response_model=ApiResponse[Pagina[IncidenteDTO]])
def listar_incidentes_por_equipo(
    equipo_id: int,
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    service: AbstractIncidenteService = Depends(get_incidente_service),
):
    return ApiResponse.ok(
        service.listar_por_equipo(paginacion, equipo_id),
        message="Incidentes del equipo obtenidos correctamente.",
    )


@router.get(
    "/workstation/{workstation_id}", response_model=ApiResponse[Pagina[IncidenteDTO]]
)
def listar_incidentes_por_workstation(
    workstation_id: int,
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    service: AbstractIncidenteService = Depends(get_incidente_service),
):
    return ApiResponse.ok(
        service.listar_por_workstation(paginacion, workstation_id),
        message="Incidentes de la workstation obtenidos correctamente.",
    )


@router.patch("/{incidente_id}/estado", response_model=ApiResponse[IncidenteDTO])
def actualizar_estado_incidente(
    incidente_id: int,
    data: ActualizarEstadoIncidenteDTO,
    service: AbstractIncidenteService = Depends(get_incidente_service),
):
    return ApiResponse.ok(
        service.actualizar_estado(incidente_id, data),
        message="Estado del incidente actualizado correctamente.",
    )
