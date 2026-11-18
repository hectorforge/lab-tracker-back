from datetime import datetime, timezone
from typing import Optional

from app.core.exceptions import BadRequestException, ConflictException, NotFoundException
from app.core.pagination import (
    mapear_pagina,
    Pagina,
    ParametrosPaginacion,
)
from app.dtos import (
    ActualizarTipoEquipoDTO,
    CrearTipoEquipoDTO,
    TipoEquipoDTO,
)
from app.models import CategoriaTipoEquipo, TipoEquipo
from app.repositories.interfaces import AbstractTipoEquipoRepository
from app.services.interfaces import AbstractTipoEquipoService


class TipoEquipoService(AbstractTipoEquipoService):
    def __init__(self, tipo_equipo_repo: AbstractTipoEquipoRepository):
        self.tipo_equipo_repo = tipo_equipo_repo

    def crear_tipo_equipo(self, data: CrearTipoEquipoDTO) -> TipoEquipoDTO:
        if self.tipo_equipo_repo.get_by_codigo(data.codigo):
            raise BadRequestException(f"El código de tipo de equipo '{data.codigo}' ya está registrado.")
        entidad = self.tipo_equipo_repo.create(TipoEquipo(**data.model_dump()))
        return TipoEquipoDTO.model_validate(entidad)

    def listar_tipos_equipo(
        self,
        paginacion: ParametrosPaginacion,
        solo_activos: bool = False,
        categoria: Optional[CategoriaTipoEquipo] = None,
    ) -> Pagina[TipoEquipoDTO]:
        pagina = self.tipo_equipo_repo.listar(paginacion, solo_activos, categoria)
        return mapear_pagina(pagina, TipoEquipoDTO.model_validate)

    def obtener_tipo_equipo(self, tipo_equipo_id: int) -> TipoEquipoDTO:
        entidad = self.tipo_equipo_repo.get_by_id(tipo_equipo_id)
        if not entidad:
            raise NotFoundException(f"Tipo de equipo {tipo_equipo_id} no encontrado.")
        return TipoEquipoDTO.model_validate(entidad)

    def actualizar_tipo_equipo(
        self, tipo_equipo_id: int, data: ActualizarTipoEquipoDTO
    ) -> TipoEquipoDTO:
        entidad = self.tipo_equipo_repo.get_by_id(tipo_equipo_id)
        if not entidad:
            raise NotFoundException(f"Tipo de equipo {tipo_equipo_id} no encontrado.")

        datos = data.model_dump(exclude_unset=True)
        if "codigo" in datos and datos["codigo"]:
            existente = self.tipo_equipo_repo.get_by_codigo(datos["codigo"])
            if existente and existente.id != tipo_equipo_id:
                raise BadRequestException("El código de tipo de equipo ya pertenece a otro registro.")

        for campo, valor in datos.items():
            setattr(entidad, campo, valor)
        entidad.actualizado_en = datetime.now(timezone.utc)
        actualizado = self.tipo_equipo_repo.update(entidad)
        return TipoEquipoDTO.model_validate(actualizado)

    def eliminar_tipo_equipo(self, tipo_equipo_id: int) -> None:
        entidad = self.tipo_equipo_repo.get_by_id(tipo_equipo_id)
        if not entidad:
            raise NotFoundException(f"Tipo de equipo {tipo_equipo_id} no encontrado.")
        if entidad.equipos:
            raise ConflictException("No se puede eliminar un tipo de equipo que tiene equipos asociados.")
        self.tipo_equipo_repo.delete(entidad)
