from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.api.security import requiere_admin, requiere_lectura
from app.api.api_response import ApiResponse
from app.infrastructure.database.database import get_session
from app.api.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.application.dtos import ActualizarTipoEquipoDTO, CrearTipoEquipoDTO, TipoEquipoDTO
from app.domain.entities import CategoriaTipoEquipo, Usuario
from app.infrastructure.repositories import TipoEquipoRepository
from app.application.services import TipoEquipoService
from app.application.interfaces import AbstractTipoEquipoService

router = APIRouter(prefix="/tipos-equipo", tags=["Catálogo de Tipos de Equipo"])


def get_tipo_equipo_service(
    session: Session = Depends(get_session),
) -> AbstractTipoEquipoService:
    return TipoEquipoService(tipo_equipo_repo=TipoEquipoRepository(session))


@router.post(
    "/", response_model=ApiResponse[TipoEquipoDTO], status_code=status.HTTP_201_CREATED
)
def crear_tipo_equipo(
    data: CrearTipoEquipoDTO,
    service: AbstractTipoEquipoService = Depends(get_tipo_equipo_service),
    _: Usuario = Depends(requiere_admin),
):
    return ApiResponse.ok(
        service.crear_tipo_equipo(data),
        message="Tipo de equipo registrado correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=ApiResponse[Pagina[TipoEquipoDTO]])
def listar_tipos_equipo(
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    solo_activos: bool = Query(default=False),
    categoria: Optional[CategoriaTipoEquipo] = Query(default=None),
    service: AbstractTipoEquipoService = Depends(get_tipo_equipo_service),
    _: Usuario = Depends(requiere_lectura),
):
    return ApiResponse.ok(
        service.listar_tipos_equipo(paginacion, solo_activos, categoria),
        message="Catálogo de tipos de equipo obtenido correctamente.",
    )


@router.get("/{tipo_equipo_id}", response_model=ApiResponse[TipoEquipoDTO])
def obtener_tipo_equipo(
    tipo_equipo_id: int,
    service: AbstractTipoEquipoService = Depends(get_tipo_equipo_service),
    _: Usuario = Depends(requiere_lectura),
):
    return ApiResponse.ok(
        service.obtener_tipo_equipo(tipo_equipo_id),
        message="Tipo de equipo obtenido correctamente.",
    )


@router.put("/{tipo_equipo_id}", response_model=ApiResponse[TipoEquipoDTO])
def actualizar_tipo_equipo(
    tipo_equipo_id: int,
    data: ActualizarTipoEquipoDTO,
    service: AbstractTipoEquipoService = Depends(get_tipo_equipo_service),
    _: Usuario = Depends(requiere_admin),
):
    return ApiResponse.ok(
        service.actualizar_tipo_equipo(
            tipo_equipo_id, data
        ),
        message="Tipo de equipo actualizado correctamente.",
    )


@router.delete("/{tipo_equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tipo_equipo(
    tipo_equipo_id: int,
    service: AbstractTipoEquipoService = Depends(get_tipo_equipo_service),
    _: Usuario = Depends(requiere_admin),
):
    service.eliminar_tipo_equipo(tipo_equipo_id)
