from typing import Optional

from app.domain.exceptions import BadRequestException, NotFoundException
from app.api.pagination import mapear_pagina, Pagina, ParametrosPaginacion
from app.application.dtos import (
    ActualizarEquipoDTO,
    CrearEquipoDTO,
    EquipoDTO,
)
from app.domain.entities import (
    CategoriaTipoEquipo,
    EstadoTipoEquipo,
    Equipo,
    TipoEquipo,
)
from app.domain.repositories import (
    AbstractEquipoRepository,
    AbstractLaboratorioRepository,
    AbstractTipoEquipoRepository,
    AbstractWorkstationRepository,
)
from app.application.interfaces import AbstractEquipoService


class EquipoService(AbstractEquipoService):
    def __init__(
        self,
        equipo_repo: AbstractEquipoRepository,
        lab_repo: AbstractLaboratorioRepository,
        ws_repo: AbstractWorkstationRepository,
        tipo_equipo_repo: AbstractTipoEquipoRepository,
    ):
        self.equipo_repo = equipo_repo
        self.lab_repo = lab_repo
        self.ws_repo = ws_repo
        self.tipo_equipo_repo = tipo_equipo_repo

    def registrar_equipo(self, data: CrearEquipoDTO) -> EquipoDTO:
        if not self.lab_repo.get_by_id(data.laboratorio_id):
            raise NotFoundException(f"Laboratorio {data.laboratorio_id} no encontrado.")
        if self.equipo_repo.get_by_codigo_patrimonial(data.codigo_patrimonial):
            raise BadRequestException(f"El código patrimonial '{data.codigo_patrimonial}' ya está registrado.")
        if data.workstation_id is not None:
            ws = self.ws_repo.get_by_id(data.workstation_id)
            if not ws:
                raise NotFoundException(f"Workstation {data.workstation_id} no encontrada.")
            if ws.laboratorio_id != data.laboratorio_id:
                raise BadRequestException("La workstation no pertenece al laboratorio indicado.")
        if data.tipo_equipo_id is not None:
            self._validar_tipo_equipo(data.tipo_equipo_id, data.categoria)

        entidad = self.equipo_repo.create(Equipo(**data.model_dump()))
        return EquipoDTO.model_validate(entidad)

    def listar_equipos(self, paginacion: ParametrosPaginacion) -> Pagina[EquipoDTO]:
        pagina = self.equipo_repo.listar(paginacion)
        return mapear_pagina(pagina, EquipoDTO.model_validate)

    def listar_por_laboratorio(
        self,
        paginacion: ParametrosPaginacion,
        lab_id: int,
        categoria: Optional[CategoriaTipoEquipo] = None,
    ) -> Pagina[EquipoDTO]:
        if not self.lab_repo.get_by_id(lab_id):
            raise NotFoundException(f"Laboratorio {lab_id} no encontrado.")
        pagina = self.equipo_repo.listar(
            paginacion, laboratorio_id=lab_id, categoria=categoria
        )
        return mapear_pagina(pagina, EquipoDTO.model_validate)

    def listar_por_workstation(
        self, paginacion: ParametrosPaginacion, workstation_id: int
    ) -> Pagina[EquipoDTO]:
        if not self.ws_repo.get_by_id(workstation_id):
            raise NotFoundException(f"Workstation {workstation_id} no encontrada.")
        pagina = self.equipo_repo.listar(
            paginacion, workstation_id=workstation_id
        )
        return mapear_pagina(pagina, EquipoDTO.model_validate)

    def obtener_equipo(self, equipo_id: int) -> EquipoDTO:
        entidad = self.equipo_repo.get_by_id(equipo_id)
        if not entidad:
            raise NotFoundException(f"Equipo {equipo_id} no encontrado.")
        return EquipoDTO.model_validate(entidad)

    def actualizar_equipo(self, equipo_id: int, data: ActualizarEquipoDTO) -> EquipoDTO:
        entidad = self.equipo_repo.get_by_id(equipo_id)
        if not entidad:
            raise NotFoundException(f"Equipo {equipo_id} no encontrado.")

        datos = data.model_dump(exclude_unset=True)
        if (
            datos.get("codigo_patrimonial")
            and datos["codigo_patrimonial"] != entidad.codigo_patrimonial
            and self.equipo_repo.get_by_codigo_patrimonial(datos["codigo_patrimonial"])
        ):
            raise BadRequestException("El código patrimonial ya pertenece a otro equipo.")

        lab_id_final = datos.get("laboratorio_id", entidad.laboratorio_id)
        if not self.lab_repo.get_by_id(lab_id_final):
            raise NotFoundException(f"Laboratorio {lab_id_final} no encontrado.")

        ws_id_final = datos.get("workstation_id", entidad.workstation_id)
        if ws_id_final is not None:
            ws = self.ws_repo.get_by_id(ws_id_final)
            if not ws:
                raise NotFoundException(f"Workstation {ws_id_final} no encontrada.")
            if ws.laboratorio_id != lab_id_final:
                raise BadRequestException("La workstation asignada no pertenece al laboratorio del equipo.")

        if datos.get("tipo_equipo_id") is not None:
            categoria_final = datos.get("categoria", entidad.categoria)
            self._validar_tipo_equipo(datos["tipo_equipo_id"], categoria_final)

        for campo, valor in datos.items():
            setattr(entidad, campo, valor)
        actualizado = self.equipo_repo.update(entidad)
        return EquipoDTO.model_validate(actualizado)

    def eliminar_equipo(self, equipo_id: int) -> None:
        entidad = self.equipo_repo.get_by_id(equipo_id)
        if not entidad:
            raise NotFoundException(f"Equipo {equipo_id} no encontrado.")
        self.equipo_repo.delete(entidad)

    def _validar_tipo_equipo(
        self, tipo_equipo_id: int, categoria: CategoriaTipoEquipo
    ) -> TipoEquipo:
        tipo = self.tipo_equipo_repo.get_by_id(tipo_equipo_id)
        if not tipo:
            raise NotFoundException(f"Tipo de equipo {tipo_equipo_id} no encontrado.")
        if tipo.estado != EstadoTipoEquipo.ACTIVO:
            raise BadRequestException("El tipo de equipo seleccionado no está activo.")
        if tipo.categoria != categoria:
            raise BadRequestException("La categoría del tipo de equipo no coincide con la categoría "
                    "indicada para el equipo.")
        return tipo
