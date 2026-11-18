from app.api.pagination import mapear_pagina, Pagina, ParametrosPaginacion
from app.application.dtos import ActualizarRolDTO, CrearRolDTO, RolDTO
from app.application.interfaces import AbstractRolService
from app.domain.entities import Rol
from app.domain.exceptions import BadRequestException, ConflictException, NotFoundException
from app.domain.repositories import AbstractRolRepository


class RolService(AbstractRolService):
    def __init__(self, rol_repo: AbstractRolRepository):
        self.rol_repo = rol_repo

    def crear_rol(self, data: CrearRolDTO) -> RolDTO:
        if self.rol_repo.get_by_nombre(data.nombre):
            raise BadRequestException(f"El rol '{data.nombre}' ya está registrado.")
        entidad = self.rol_repo.create(Rol(**data.model_dump()))
        return RolDTO.model_validate(entidad)

    def listar_roles(
        self, paginacion: ParametrosPaginacion, solo_activos: bool = False
    ) -> Pagina[RolDTO]:
        pagina = self.rol_repo.listar(paginacion, solo_activos)
        return mapear_pagina(pagina, RolDTO.model_validate)

    def obtener_rol(self, rol_id: int) -> RolDTO:
        return RolDTO.model_validate(self._obtener_entidad(rol_id))

    def actualizar_rol(self, rol_id: int, data: ActualizarRolDTO) -> RolDTO:
        rol = self._obtener_entidad(rol_id)
        datos = data.model_dump(exclude_unset=True)
        if datos.get("nombre"):
            existente = self.rol_repo.get_by_nombre(datos["nombre"])
            if existente and existente.id != rol_id:
                raise BadRequestException("El nombre del rol ya está en uso.")
        for campo, valor in datos.items():
            setattr(rol, campo, valor)
        return RolDTO.model_validate(self.rol_repo.update(rol))

    def eliminar_rol(self, rol_id: int) -> None:
        rol = self._obtener_entidad(rol_id)
        if rol.usuarios:
            raise ConflictException(
                "No se puede eliminar un rol que tiene usuarios asignados."
            )
        self.rol_repo.delete(rol)

    def _obtener_entidad(self, rol_id: int) -> Rol:
        rol = self.rol_repo.get_by_id(rol_id)
        if not rol:
            raise NotFoundException(f"Rol {rol_id} no encontrado.")
        return rol
