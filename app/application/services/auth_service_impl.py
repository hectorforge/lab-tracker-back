from app.application.dtos import LoginDTO, TokenDTO, UsuarioDTO
from app.application.interfaces import AbstractAuthService
from app.application.security import crear_token
from app.domain.exceptions import UnauthorizedException
from app.domain.repositories import AbstractUsuarioRepository
from app.domain.security import verify_password


class AuthService(AbstractAuthService):
    def __init__(self, usuario_repo: AbstractUsuarioRepository):
        self.usuario_repo = usuario_repo

    def login(self, data: LoginDTO) -> TokenDTO:
        usuario = self.usuario_repo.get_by_username(data.username)
        if not usuario or not verify_password(data.password, usuario.password_hash):
            raise UnauthorizedException("Usuario o contraseña incorrectos.")
        if not usuario.activo:
            raise UnauthorizedException("La cuenta de usuario está desactivada.")
        if not usuario.rol or not usuario.rol.es_activo:
            raise UnauthorizedException("El rol asignado no está activo.")

        token, expira = crear_token(usuario.username, usuario.rol.nombre)
        return TokenDTO(
            access_token=token,
            token_type="bearer",
            expires_in=expira,
            username=usuario.username,
            rol=usuario.rol.nombre,
        )

    def obtener_usuario_actual(self, username: str) -> UsuarioDTO:
        usuario = self.usuario_repo.get_by_username(username)
        if not usuario or not usuario.activo:
            raise UnauthorizedException("El usuario autenticado ya no está activo.")
        return UsuarioDTO.model_validate(usuario)
