from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.api.security import requiere_admin, requiere_lectura
from app.api.api_response import ApiResponse
from app.infrastructure.database.database import get_session
from app.api.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.application.dtos import ActualizarLicenciaDTO, CrearLicenciaDTO, LicenciaDTO
from app.domain.entities import EstadoLicencia, Usuario
from app.infrastructure.repositories import (
    EquipoRepository,
    LicenciaRepository,
    TipoEquipoRepository,
)
from app.application.services import LicenciaService
from app.application.interfaces import AbstractLicenciaService

router = APIRouter(prefix="/licencias", tags=["Licencias de Software"])


def get_licencia_service(
    session: Session = Depends(get_session),
) -> AbstractLicenciaService:
    return LicenciaService(
        licencia_repo=LicenciaRepository(session),
        equipo_repo=EquipoRepository(session),
        tipo_equipo_repo=TipoEquipoRepository(session),
    )


@router.post(
    "/", response_model=ApiResponse[LicenciaDTO], status_code=status.HTTP_201_CREATED
)
def crear_licencia(
    data: CrearLicenciaDTO,
    service: AbstractLicenciaService = Depends(get_licencia_service),
    _: Usuario = Depends(requiere_admin),
):
    return ApiResponse.ok(
        service.crear_licencia(data),
        message="Licencia registrada correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=ApiResponse[Pagina[LicenciaDTO]])
def listar_licencias(
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    equipo_id: Optional[int] = Query(default=None),
    estado: Optional[EstadoLicencia] = Query(default=None),
    service: AbstractLicenciaService = Depends(get_licencia_service),
    _: Usuario = Depends(requiere_lectura),
):
    return ApiResponse.ok(
        service.listar_licencias(paginacion, equipo_id, estado),
        message="Lista de licencias obtenida correctamente.",
    )


@router.get("/{licencia_id}", response_model=ApiResponse[LicenciaDTO])
def obtener_licencia(
    licencia_id: int,
    service: AbstractLicenciaService = Depends(get_licencia_service),
    _: Usuario = Depends(requiere_lectura),
):
    return ApiResponse.ok(
        service.obtener_licencia(licencia_id),
        message="Licencia obtenida correctamente.",
    )


@router.put("/{licencia_id}", response_model=ApiResponse[LicenciaDTO])
def actualizar_licencia(
    licencia_id: int,
    data: ActualizarLicenciaDTO,
    service: AbstractLicenciaService = Depends(get_licencia_service),
    _: Usuario = Depends(requiere_admin),
):
    return ApiResponse.ok(
        service.actualizar_licencia(
            licencia_id, data
        ),
        message="Licencia actualizada correctamente.",
    )


@router.delete("/{licencia_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_licencia(
    licencia_id: int,
    service: AbstractLicenciaService = Depends(get_licencia_service),
    _: Usuario = Depends(requiere_admin),
):
    service.eliminar_licencia(licencia_id)
