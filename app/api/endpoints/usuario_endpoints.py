from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.api import ApiResponse
from app.api.pagination import Pagina, ParametrosPaginacion, get_paginacion
from app.api.security import requiere_admin
from app.application.dtos import (
    ActualizarUsuarioDTO,
    CrearUsuarioDTO,
    UsuarioDTO,
)
from app.application.interfaces import AbstractUsuarioService
from app.application.services import UsuarioService
from app.domain.entities import Usuario
from app.infrastructure.database import get_session
from app.infrastructure.repositories import RolRepository, UsuarioRepository

router = APIRouter(prefix="/usuarios", tags=["Usuarios del Sistema"])


def get_usuario_service(
    session: Session = Depends(get_session),
) -> AbstractUsuarioService:
    return UsuarioService(
        usuario_repo=UsuarioRepository(session),
        rol_repo=RolRepository(session),
    )


@router.post(
    "/", response_model=ApiResponse[UsuarioDTO], status_code=status.HTTP_201_CREATED
)
def crear_usuario(
    data: CrearUsuarioDTO,
    _: Usuario = Depends(requiere_admin),
    service: AbstractUsuarioService = Depends(get_usuario_service),
):
    return ApiResponse.ok(
        service.crear_usuario(data),
        message="Usuario registrado correctamente.",
        status=status.HTTP_201_CREATED,
    )


@router.get("/", response_model=ApiResponse[Pagina[UsuarioDTO]])
def listar_usuarios(
    paginacion: ParametrosPaginacion = Depends(get_paginacion),
    rol_id: Optional[int] = None,
    solo_activos: bool = False,
    busqueda: Optional[str] = None,
    _: Usuario = Depends(requiere_admin),
    service: AbstractUsuarioService = Depends(get_usuario_service),
):
    return ApiResponse.ok(
        service.listar_usuarios(paginacion, rol_id, solo_activos, busqueda),
        message="Lista de usuarios obtenida correctamente.",
    )


@router.get("/{usuario_id}", response_model=ApiResponse[UsuarioDTO])
def obtener_usuario(
    usuario_id: int,
    _: Usuario = Depends(requiere_admin),
    service: AbstractUsuarioService = Depends(get_usuario_service),
):
    return ApiResponse.ok(
        service.obtener_usuario(usuario_id),
        message="Usuario obtenido correctamente.",
    )


@router.put("/{usuario_id}", response_model=ApiResponse[UsuarioDTO])
def actualizar_usuario(
    usuario_id: int,
    data: ActualizarUsuarioDTO,
    _: Usuario = Depends(requiere_admin),
    service: AbstractUsuarioService = Depends(get_usuario_service),
):
    return ApiResponse.ok(
        service.actualizar_usuario(usuario_id, data),
        message="Usuario actualizado correctamente.",
    )


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    usuario_id: int,
    _: Usuario = Depends(requiere_admin),
    service: AbstractUsuarioService = Depends(get_usuario_service),
):
    service.eliminar_usuario(usuario_id)
