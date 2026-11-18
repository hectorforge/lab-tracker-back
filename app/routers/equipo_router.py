from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.api_response import ApiResponse
from app.core.database import get_session
from app.core.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.dtos import ActualizarEquipoDTO, CrearEquipoDTO
from app.models import CategoriaTipoEquipo
from app.repositories.implementaciones import (
    EquipoRepository,
    LaboratorioRepository,
    TipoEquipoRepository,
    WorkstationRepository,
)
from app.schemas.lab_schemas import EquipoCreate, EquipoRead, EquipoUpdate
from app.services.implementaciones import EquipoService
from app.services.interfaces import AbstractEquipoService

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
    "/", response_model=ApiResponse[EquipoRead], status_code=status.HTTP_201_CREATED
)
def registrar_equipo(
    data: EquipoCreate,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return ApiResponse.ok(
        service.registrar_equipo(CrearEquipoDTO.model_validate(data)),
        message="Equipo registrado correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=ApiResponse[Pagina[EquipoRead]])
def listar_equipos(
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return ApiResponse.ok(
        service.listar_equipos(paginacion),
        message="Lista de equipos obtenida correctamente.",
    )


@router.get("/laboratorio/{lab_id}", response_model=ApiResponse[Pagina[EquipoRead]])
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
    "/workstation/{workstation_id}", response_model=ApiResponse[Pagina[EquipoRead]]
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


@router.get("/{equipo_id}", response_model=ApiResponse[EquipoRead])
def obtener_equipo(
    equipo_id: int,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return ApiResponse.ok(
        service.obtener_equipo(equipo_id), message="Equipo obtenido correctamente."
    )


@router.put("/{equipo_id}", response_model=ApiResponse[EquipoRead])
def actualizar_equipo(
    equipo_id: int,
    data: EquipoUpdate,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return ApiResponse.ok(
        service.actualizar_equipo(
            equipo_id, ActualizarEquipoDTO.model_validate(data)
        ),
        message="Equipo actualizado correctamente.",
    )


@router.delete("/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_equipo(
    equipo_id: int,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    service.eliminar_equipo(equipo_id)
