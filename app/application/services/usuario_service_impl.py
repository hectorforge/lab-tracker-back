from datetime import datetime, timezone

from app.api.pagination import mapear_pagina, Pagina, ParametrosPaginacion
from app.application.dtos import (
    ActualizarUsuarioDTO,
    CrearUsuarioDTO,
    UsuarioDTO,
)
from app.application.interfaces import AbstractUsuarioService
from app.domain.entities import Usuario
from app.domain.exceptions import BadRequestException, NotFoundException
from app.domain.repositories import (
    AbstractRolRepository,
    AbstractUsuarioRepository,
)
from app.domain.security import hash_password


class UsuarioService(AbstractUsuarioService):
    def __init__(
        self,
        usuario_repo: AbstractUsuarioRepository,
        rol_repo: AbstractRolRepository,
    ):
        self.usuario_repo = usuario_repo
        self.rol_repo = rol_repo

    def crear_usuario(self, data: CrearUsuarioDTO) -> UsuarioDTO:
        if self.usuario_repo.get_by_username(data.username):
            raise BadRequestException(
                f"El username '{data.username}' ya está registrado."
            )
        if not self.rol_repo.get_by_id(data.rol_id):
            raise NotFoundException(f"Rol {data.rol_id} no encontrado.")
        if data.correo and self._correo_en_uso(data.correo):
            raise BadRequestException("El correo ya pertenece a otro usuario.")

        datos = data.model_dump(exclude={"password"})
        datos["password_hash"] = hash_password(data.password)
        entidad = self.usuario_repo.create(Usuario(**datos))
        return UsuarioDTO.model_validate(entidad)

    def listar_usuarios(
        self,
        paginacion: ParametrosPaginacion,
        rol_id: int | None = None,
        solo_activos: bool = False,
        busqueda: str | None = None,
    ) -> Pagina[UsuarioDTO]:
        pagina = self.usuario_repo.listar(
            paginacion, rol_id, solo_activos, busqueda
        )
        return mapear_pagina(pagina, UsuarioDTO.model_validate)

    def obtener_usuario(self, usuario_id: int) -> UsuarioDTO:
        return UsuarioDTO.model_validate(self._obtener_entidad(usuario_id))

    def actualizar_usuario(
        self, usuario_id: int, data: ActualizarUsuarioDTO
    ) -> UsuarioDTO:
        usuario = self._obtener_entidad(usuario_id)
        datos = data.model_dump(exclude_unset=True, exclude={"password"})

        if datos.get("username"):
            existente = self.usuario_repo.get_by_username(datos["username"])
            if existente and existente.id != usuario_id:
                raise BadRequestException("El username ya pertenece a otro usuario.")
        if datos.get("correo") and self._correo_en_uso(datos["correo"], usuario_id):
            raise BadRequestException("El correo ya pertenece a otro usuario.")
        if datos.get("rol_id") and not self.rol_repo.get_by_id(datos["rol_id"]):
            raise NotFoundException(f"Rol {datos['rol_id']} no encontrado.")

        for campo, valor in datos.items():
            setattr(usuario, campo, valor)
        if data.password:
            usuario.password_hash = hash_password(data.password)
        usuario.actualizado_en = datetime.now(timezone.utc)

        return UsuarioDTO.model_validate(self.usuario_repo.update(usuario))

    def eliminar_usuario(self, usuario_id: int) -> None:
        self.usuario_repo.delete(self._obtener_entidad(usuario_id))

    def _obtener_entidad(self, usuario_id: int) -> Usuario:
        usuario = self.usuario_repo.get_by_id(usuario_id)
        if not usuario:
            raise NotFoundException(f"Usuario {usuario_id} no encontrado.")
        return usuario

    def _correo_en_uso(self, correo: str, excluir_id: int | None = None) -> bool:
        usuario = self.usuario_repo.get_by_correo(correo)
        return bool(usuario and usuario.id != excluir_id)
