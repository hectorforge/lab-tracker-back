from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.api import ApiResponse
from app.api.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.api.security import requiere_admin
from app.application.dtos import ActualizarRolDTO, CrearRolDTO, RolDTO
from app.application.interfaces import AbstractRolService
from app.application.services import RolService
from app.domain.entities import Usuario
from app.infrastructure.database import get_session
from app.infrastructure.repositories import RolRepository

router = APIRouter(prefix="/roles", tags=["Roles y Permisos"])


def get_rol_service(session: Session = Depends(get_session)) -> AbstractRolService:
    return RolService(rol_repo=RolRepository(session))


@router.post(
    "/", response_model=ApiResponse[RolDTO], status_code=status.HTTP_201_CREATED
)
def crear_rol(
    data: CrearRolDTO,
    _: Usuario = Depends(requiere_admin),
    service: AbstractRolService = Depends(get_rol_service),
):
    return ApiResponse.ok(
        service.crear_rol(data),
        message="Rol registrado correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=ApiResponse[Pagina[RolDTO]])
def listar_roles(
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    solo_activos: bool = False,
    _: Usuario = Depends(requiere_admin),
    service: AbstractRolService = Depends(get_rol_service),
):
    return ApiResponse.ok(
        service.listar_roles(paginacion, solo_activos),
        message="Lista de roles obtenida correctamente.",
    )


@router.get("/{rol_id}", response_model=ApiResponse[RolDTO])
def obtener_rol(
    rol_id: int,
    _: Usuario = Depends(requiere_admin),
    service: AbstractRolService = Depends(get_rol_service),
):
    return ApiResponse.ok(
        service.obtener_rol(rol_id), message="Rol obtenido correctamente."
    )


@router.put("/{rol_id}", response_model=ApiResponse[RolDTO])
def actualizar_rol(
    rol_id: int,
    data: ActualizarRolDTO,
    _: Usuario = Depends(requiere_admin),
    service: AbstractRolService = Depends(get_rol_service),
):
    return ApiResponse.ok(
        service.actualizar_rol(rol_id, data),
        message="Rol actualizado correctamente.",
    )


@router.delete("/{rol_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_rol(
    rol_id: int,
    _: Usuario = Depends(requiere_admin),
    service: AbstractRolService = Depends(get_rol_service),
):
    service.eliminar_rol(rol_id)
