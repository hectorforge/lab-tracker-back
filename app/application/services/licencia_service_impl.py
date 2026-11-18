from typing import Optional

from app.domain.exceptions import BadRequestException, NotFoundException
from app.api.pagination import mapear_pagina, Pagina, ParametrosPaginacion
from app.application.dtos import (
    ActualizarLicenciaDTO,
    CrearLicenciaDTO,
    LicenciaDTO,
)
from app.domain.entities import EstadoLicencia, Licencia
from app.domain.repositories import (
    AbstractEquipoRepository,
    AbstractLicenciaRepository,
    AbstractTipoEquipoRepository,
)
from app.application.interfaces import AbstractLicenciaService


class LicenciaService(AbstractLicenciaService):
    def __init__(
        self,
        licencia_repo: AbstractLicenciaRepository,
        equipo_repo: AbstractEquipoRepository,
        tipo_equipo_repo: AbstractTipoEquipoRepository,
    ):
        self.licencia_repo = licencia_repo
        self.equipo_repo = equipo_repo
        self.tipo_equipo_repo = tipo_equipo_repo

    def crear_licencia(self, data: CrearLicenciaDTO) -> LicenciaDTO:
        if self.licencia_repo.get_by_codigo(data.codigo):
            raise BadRequestException(f"El código de licencia '{data.codigo}' ya está registrado.")
        self._validar_asociaciones(data.equipo_id, data.tipo_equipo_id)
        entidad = self.licencia_repo.create(Licencia(**data.model_dump()))
        return LicenciaDTO.model_validate(entidad)

    def listar_licencias(
        self,
        paginacion: ParametrosPaginacion,
        equipo_id: Optional[int] = None,
        estado: Optional[EstadoLicencia] = None,
    ) -> Pagina[LicenciaDTO]:
        pagina = self.licencia_repo.listar(paginacion, equipo_id, estado)
        return mapear_pagina(pagina, LicenciaDTO.model_validate)

    def obtener_licencia(self, licencia_id: int) -> LicenciaDTO:
        entidad = self.licencia_repo.get_by_id(licencia_id)
        if not entidad:
            raise NotFoundException(f"Licencia {licencia_id} no encontrada.")
        return LicenciaDTO.model_validate(entidad)

    def actualizar_licencia(
        self, licencia_id: int, data: ActualizarLicenciaDTO
    ) -> LicenciaDTO:
        entidad = self.licencia_repo.get_by_id(licencia_id)
        if not entidad:
            raise NotFoundException(f"Licencia {licencia_id} no encontrada.")

        datos = data.model_dump(exclude_unset=True)
        if datos.get("codigo"):
            existente = self.licencia_repo.get_by_codigo(datos["codigo"])
            if existente and existente.id != licencia_id:
                raise BadRequestException("El código de licencia ya pertenece a otro registro.")

        self._validar_asociaciones(
            datos.get("equipo_id", entidad.equipo_id),
            datos.get("tipo_equipo_id", entidad.tipo_equipo_id),
        )

        for campo, valor in datos.items():
            setattr(entidad, campo, valor)
        actualizada = self.licencia_repo.update(entidad)
        return LicenciaDTO.model_validate(actualizada)

    def eliminar_licencia(self, licencia_id: int) -> None:
        entidad = self.licencia_repo.get_by_id(licencia_id)
        if not entidad:
            raise NotFoundException(f"Licencia {licencia_id} no encontrada.")
        self.licencia_repo.delete(entidad)

    def _validar_asociaciones(
        self, equipo_id: Optional[int], tipo_equipo_id: Optional[int]
    ) -> None:
        if equipo_id is not None:
            equipo = self.equipo_repo.get_by_id(equipo_id)
            if not equipo:
                raise NotFoundException(f"Equipo {equipo_id} no encontrado.")
            if (
                tipo_equipo_id is not None
                and equipo.tipo_equipo_id is not None
                and equipo.tipo_equipo_id != tipo_equipo_id
            ):
                raise BadRequestException("El tipo de equipo de la licencia no coincide con el "
                        "tipo de equipo asignado al equipo.")
        if tipo_equipo_id is not None and not self.tipo_equipo_repo.get_by_id(
            tipo_equipo_id
        ):
            raise NotFoundException(f"Tipo de equipo {tipo_equipo_id} no encontrado.")
