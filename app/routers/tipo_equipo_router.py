from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.api_response import ApiResponse
from app.core.database import get_session
from app.core.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.dtos import ActualizarTipoEquipoDTO, CrearTipoEquipoDTO
from app.models import CategoriaTipoEquipo
from app.repositories.implementaciones import TipoEquipoRepository
from app.schemas.lab_schemas import TipoEquipoCreate, TipoEquipoRead, TipoEquipoUpdate
from app.services.implementaciones import TipoEquipoService
from app.services.interfaces import AbstractTipoEquipoService

router = APIRouter(prefix="/tipos-equipo", tags=["Catálogo de Tipos de Equipo"])


def get_tipo_equipo_service(
    session: Session = Depends(get_session),
) -> AbstractTipoEquipoService:
    return TipoEquipoService(tipo_equipo_repo=TipoEquipoRepository(session))


@router.post(
    "/", response_model=ApiResponse[TipoEquipoRead], status_code=status.HTTP_201_CREATED
)
def crear_tipo_equipo(
    data: TipoEquipoCreate,
    service: AbstractTipoEquipoService = Depends(get_tipo_equipo_service),
):
    return ApiResponse.ok(
        service.crear_tipo_equipo(CrearTipoEquipoDTO.model_validate(data)),
        message="Tipo de equipo registrado correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=ApiResponse[Pagina[TipoEquipoRead]])
def listar_tipos_equipo(
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    solo_activos: bool = Query(default=False),
    categoria: Optional[CategoriaTipoEquipo] = Query(default=None),
    service: AbstractTipoEquipoService = Depends(get_tipo_equipo_service),
):
    return ApiResponse.ok(
        service.listar_tipos_equipo(paginacion, solo_activos, categoria),
        message="Catálogo de tipos de equipo obtenido correctamente.",
    )


@router.get("/{tipo_equipo_id}", response_model=ApiResponse[TipoEquipoRead])
def obtener_tipo_equipo(
    tipo_equipo_id: int,
    service: AbstractTipoEquipoService = Depends(get_tipo_equipo_service),
):
    return ApiResponse.ok(
        service.obtener_tipo_equipo(tipo_equipo_id),
        message="Tipo de equipo obtenido correctamente.",
    )


@router.put("/{tipo_equipo_id}", response_model=ApiResponse[TipoEquipoRead])
def actualizar_tipo_equipo(
    tipo_equipo_id: int,
    data: TipoEquipoUpdate,
    service: AbstractTipoEquipoService = Depends(get_tipo_equipo_service),
):
    return ApiResponse.ok(
        service.actualizar_tipo_equipo(
            tipo_equipo_id, ActualizarTipoEquipoDTO.model_validate(data)
        ),
        message="Tipo de equipo actualizado correctamente.",
    )


@router.delete("/{tipo_equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tipo_equipo(
    tipo_equipo_id: int,
    service: AbstractTipoEquipoService = Depends(get_tipo_equipo_service),
):
    service.eliminar_tipo_equipo(tipo_equipo_id)
