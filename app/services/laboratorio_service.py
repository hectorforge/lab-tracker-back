from typing import List
from fastapi import HTTPException, status
from app.models.lab_models import Laboratorio
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un laboratorio con el código '{data.codigo}'.",
            )
        nuevo_lab = Laboratorio(**data.model_dump())
        return self.lab_repo.create(nuevo_lab)

    def listar_laboratorios(self, solo_disponibles: bool = False) -> List[Laboratorio]:
        if solo_disponibles:
            return self.lab_repo.get_disponibles()
        return self.lab_repo.get_all()

    def obtener_laboratorio(self, lab_id: int) -> Laboratorio:
        lab = self.lab_repo.get_by_id(lab_id)
        if not lab:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Laboratorio con ID {lab_id} no encontrado.",
            )
        return lab

    def actualizar_laboratorio(
        self, lab_id: int, data: LaboratorioUpdate
    ) -> Laboratorio:
        lab = self.obtener_laboratorio(lab_id)
        datos = data.model_dump(exclude_unset=True)

        if "codigo" in datos and datos["codigo"] != lab.codigo:
            if self.lab_repo.get_by_codigo(datos["codigo"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El código '{datos['codigo']}' ya está en uso.",
                )

        if "capacidad_workstations" in datos:
            cantidad_actual = len(self.ws_repo.get_by_laboratorio(lab_id))
            if datos["capacidad_workstations"] < cantidad_actual:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"La capacidad no puede ser menor a las {cantidad_actual} workstations ya registradas.",
                )

        for campo, valor in datos.items():
            setattr(lab, campo, valor)

        return self.lab_repo.update(lab)

    def eliminar_laboratorio(self, lab_id: int) -> None:
        lab = self.obtener_laboratorio(lab_id)
        self.lab_repo.delete(lab)