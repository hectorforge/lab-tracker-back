from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.api.api_response import ApiResponse
from app.infrastructure.database.database import get_session
from app.api.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.application.dtos import ActualizarEquipoDTO, CrearEquipoDTO, EquipoDTO
from app.domain.entities import CategoriaTipoEquipo
from app.infrastructure.repositories import (
    EquipoRepository,
    LaboratorioRepository,
    TipoEquipoRepository,
    WorkstationRepository,
)
from app.application.services import EquipoService
from app.application.interfaces import AbstractEquipoService

router = APIRouter(prefix="/equipos", tags=["Inventario de Equipos"])


def get_equipo_service(
    session: Session = Depends(get_session),
) -> AbstractEquipoService:
    return EquipoService(
        equipo_repo=EquipoRepository(session),
        lab_repo=LaboratorioRepository(session),
        ws_repo=WorkstationRepository(session),
        tipo_equipo_repo=TipoEquipoRepository(session),
    )


@router.post(
    "/", response_model=ApiResponse[EquipoDTO], status_code=status.HTTP_201_CREATED
)
def registrar_equipo(
    data: CrearEquipoDTO,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return ApiResponse.ok(
        service.registrar_equipo(data),
        message="Equipo registrado correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=ApiResponse[Pagina[EquipoDTO]])
def listar_equipos(
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return ApiResponse.ok(
        service.listar_equipos(paginacion),
        message="Lista de equipos obtenida correctamente.",
    )


@router.get("/laboratorio/{lab_id}", response_model=ApiResponse[Pagina[EquipoDTO]])
def listar_equipos_por_laboratorio(
    lab_id: int,
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    categoria: Optional[CategoriaTipoEquipo] = None,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return ApiResponse.ok(
        service.listar_por_laboratorio(paginacion, lab_id, categoria),
        message="Equipos del laboratorio obtenidos correctamente.",
    )


@router.get(
    "/workstation/{workstation_id}", response_model=ApiResponse[Pagina[EquipoDTO]]
)
def listar_equipos_por_workstation(
    workstation_id: int,
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return ApiResponse.ok(
        service.listar_por_workstation(paginacion, workstation_id),
        message="Equipos de la workstation obtenidos correctamente.",
    )


@router.get("/{equipo_id}", response_model=ApiResponse[EquipoDTO])
def obtener_equipo(
    equipo_id: int,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return ApiResponse.ok(
        service.obtener_equipo(equipo_id), message="Equipo obtenido correctamente."
    )


@router.put("/{equipo_id}", response_model=ApiResponse[EquipoDTO])
def actualizar_equipo(
    equipo_id: int,
    data: ActualizarEquipoDTO,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return ApiResponse.ok(
        service.actualizar_equipo(
            equipo_id, data
        ),
        message="Equipo actualizado correctamente.",
    )


@router.delete("/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_equipo(
    equipo_id: int,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    service.eliminar_equipo(equipo_id)
