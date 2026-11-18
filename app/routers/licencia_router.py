from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.api_response import ApiResponse
from app.core.database import get_session
from app.core.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.dtos import ActualizarLicenciaDTO, CrearLicenciaDTO
from app.models import EstadoLicencia
from app.repositories.implementaciones import (
    EquipoRepository,
    LicenciaRepository,
    TipoEquipoRepository,
)
from app.schemas.lab_schemas import LicenciaCreate, LicenciaRead, LicenciaUpdate
from app.services.implementaciones import LicenciaService
from app.services.interfaces import AbstractLicenciaService

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
    "/", response_model=ApiResponse[LicenciaRead], status_code=status.HTTP_201_CREATED
)
def crear_licencia(
    data: LicenciaCreate,
    service: AbstractLicenciaService = Depends(get_licencia_service),
):
    return ApiResponse.ok(
        service.crear_licencia(CrearLicenciaDTO.model_validate(data)),
        message="Licencia registrada correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=ApiResponse[Pagina[LicenciaRead]])
def listar_licencias(
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    equipo_id: Optional[int] = Query(default=None),
    estado: Optional[EstadoLicencia] = Query(default=None),
    service: AbstractLicenciaService = Depends(get_licencia_service),
):
    return ApiResponse.ok(
        service.listar_licencias(paginacion, equipo_id, estado),
        message="Lista de licencias obtenida correctamente.",
    )


@router.get("/{licencia_id}", response_model=ApiResponse[LicenciaRead])
def obtener_licencia(
    licencia_id: int,
    service: AbstractLicenciaService = Depends(get_licencia_service),
):
    return ApiResponse.ok(
        service.obtener_licencia(licencia_id),
        message="Licencia obtenida correctamente.",
    )


@router.put("/{licencia_id}", response_model=ApiResponse[LicenciaRead])
def actualizar_licencia(
    licencia_id: int,
    data: LicenciaUpdate,
    service: AbstractLicenciaService = Depends(get_licencia_service),
):
    return ApiResponse.ok(
        service.actualizar_licencia(
            licencia_id, ActualizarLicenciaDTO.model_validate(data)
        ),
        message="Licencia actualizada correctamente.",
    )


@router.delete("/{licencia_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_licencia(
    licencia_id: int,
    service: AbstractLicenciaService = Depends(get_licencia_service),
):
    service.eliminar_licencia(licencia_id)
