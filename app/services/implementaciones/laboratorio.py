from app.core.exceptions import BadRequestException, NotFoundException
from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import Laboratorio
from app.schemas.lab_schemas import LaboratorioCreate, LaboratorioUpdate
from app.repositories.interfaces import (
    AbstractLaboratorioRepository,
    AbstractWorkstationRepository,
)
from app.services.interfaces import AbstractLaboratorioService


class LaboratorioService(AbstractLaboratorioService):
    def __init__(
        self,
        lab_repo: AbstractLaboratorioRepository,
        ws_repo: AbstractWorkstationRepository,
    ):
        self.lab_repo = lab_repo
        self.ws_repo = ws_repo

    def crear_laboratorio(self, data: LaboratorioCreate) -> Laboratorio:
        if self.lab_repo.get_by_codigo(data.codigo):
            raise BadRequestException(f"Ya existe un laboratorio con el código '{data.codigo}'.")
        nuevo_lab = Laboratorio(**data.model_dump())
        return self.lab_repo.create(nuevo_lab)

    def listar_laboratorios(
        self,
        paginacion: ParametrosPaginacion,
        solo_disponibles: bool = False,
    ) -> Pagina[Laboratorio]:
        return self.lab_repo.listar(paginacion, solo_disponibles)

    def obtener_laboratorio(self, lab_id: int) -> Laboratorio:
        lab = self.lab_repo.get_by_id(lab_id)
        if not lab:
            raise NotFoundException(f"Laboratorio con ID {lab_id} no encontrado.")
        return lab

    def actualizar_laboratorio(
        self, lab_id: int, data: LaboratorioUpdate
    ) -> Laboratorio:
        lab = self.obtener_laboratorio(lab_id)
        datos = data.model_dump(exclude_unset=True)

        if "codigo" in datos and datos["codigo"] != lab.codigo:
            if self.lab_repo.get_by_codigo(datos["codigo"]):
                raise BadRequestException(f"El código '{datos['codigo']}' ya está en uso.")

        if "capacidad_workstations" in datos:
            parametros = ParametrosPaginacion(pagina=1, tamano_pagina=1)
            cantidad_actual = self.ws_repo.listar(
                parametros, laboratorio_id=lab_id
            ).total
            if datos["capacidad_workstations"] < cantidad_actual:
                raise BadRequestException(f"La capacidad no puede ser menor a las {cantidad_actual} workstations ya registradas.")

        for campo, valor in datos.items():
            setattr(lab, campo, valor)

        return self.lab_repo.update(lab)

    def eliminar_laboratorio(self, lab_id: int) -> None:
        lab = self.obtener_laboratorio(lab_id)
        self.lab_repo.delete(lab)
