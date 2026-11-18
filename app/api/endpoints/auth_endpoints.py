from fastapi import APIRouter, Depends, status

from app.api import ApiResponse
from app.api.security import get_usuario_actual
from app.application.dtos import LoginDTO, TokenDTO, UsuarioDTO
from app.application.interfaces import AbstractAuthService
from app.application.services import AuthService
from app.domain.entities import Usuario
from app.infrastructure.database import get_session
from app.infrastructure.repositories import UsuarioRepository
from sqlmodel import Session

router = APIRouter(prefix="/auth", tags=["Autenticación"])


def get_auth_service(session: Session = Depends(get_session)) -> AbstractAuthService:
    return AuthService(usuario_repo=UsuarioRepository(session))


@router.post("/login", response_model=ApiResponse[TokenDTO])
def login(
    data: LoginDTO,
    service: AbstractAuthService = Depends(get_auth_service),
):
    return ApiResponse.ok(
        service.login(data), message="Inicio de sesión correcto."
    )


@router.get("/me", response_model=ApiResponse[UsuarioDTO])
def usuario_actual(
    usuario: Usuario = Depends(get_usuario_actual),
    service: AbstractAuthService = Depends(get_auth_service),
):
    return ApiResponse.ok(
        service.obtener_usuario_actual(usuario.username),
        message="Usuario autenticado obtenido correctamente.",
    )
