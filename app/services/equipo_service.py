from typing import List, Optional
from fastapi import HTTPException, status
from app.models.lab_models import Equipo, TipoEquipo
from app.schemas.lab_schemas import EquipoCreate, EquipoUpdate
from app.repositories.interfaces import (
    AbstractEquipoRepository,
    AbstractLaboratorioRepository,
    AbstractWorkstationRepository,
)
from app.services.interfaces import AbstractEquipoService


class EquipoService(AbstractEquipoService):
    def __init__(
        self,
        equipo_repo: AbstractEquipoRepository,
        lab_repo: AbstractLaboratorioRepository,
        ws_repo: AbstractWorkstationRepository,
    ):
        self.equipo_repo = equipo_repo
        self.lab_repo = lab_repo
        self.ws_repo = ws_repo

    def registrar_equipo(self, data: EquipoCreate) -> Equipo:
        if not self.lab_repo.get_by_id(data.laboratorio_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Laboratorio {data.laboratorio_id} no encontrado.",
            )

        if self.equipo_repo.get_by_codigo_patrimonial(data.codigo_patrimonial):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El código patrimonial '{data.codigo_patrimonial}' ya está registrado.",
            )

        if data.workstation_id is not None:
            ws = self.ws_repo.get_by_id(data.workstation_id)
            if not ws:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Workstation {data.workstation_id} no encontrada.",
                )
            if ws.laboratorio_id != data.laboratorio_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La workstation no pertenece al laboratorio indicado.",
                )

        nuevo_equipo = Equipo(**data.model_dump())
        return self.equipo_repo.create(nuevo_equipo)

    def listar_equipos(self) -> List[Equipo]:
        return self.equipo_repo.get_all()

    def listar_por_laboratorio(
        self, lab_id: int, tipo: Optional[TipoEquipo] = None
    ) -> List[Equipo]:
        if not self.lab_repo.get_by_id(lab_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Laboratorio {lab_id} no encontrado.",
            )
        return self.equipo_repo.get_by_laboratorio(lab_id, tipo)

    def listar_por_workstation(self, workstation_id: int) -> List[Equipo]:
        if not self.ws_repo.get_by_id(workstation_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workstation {workstation_id} no encontrada.",
            )
        return self.equipo_repo.get_by_workstation(workstation_id)

    def obtener_equipo(self, equipo_id: int) -> Equipo:
        equipo = self.equipo_repo.get_by_id(equipo_id)
        if not equipo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipo {equipo_id} no encontrado.",
            )
        return equipo

    def actualizar_equipo(self, equipo_id: int, data: EquipoUpdate) -> Equipo:
        equipo = self.obtener_equipo(equipo_id)
        datos = data.model_dump(exclude_unset=True)

        if (
            "codigo_patrimonial" in datos
            and datos["codigo_patrimonial"] != equipo.codigo_patrimonial
        ):
            if self.equipo_repo.get_by_codigo_patrimonial(datos["codigo_patrimonial"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El código patrimonial ya pertenece a otro equipo.",
                )

        lab_id_final = datos.get("laboratorio_id", equipo.laboratorio_id)
        if not self.lab_repo.get_by_id(lab_id_final):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Laboratorio {lab_id_final} no encontrado.",
            )

        ws_id_final = (
            datos["workstation_id"]
            if "workstation_id" in datos
            else equipo.workstation_id
        )
        if ws_id_final is not None:
            ws = self.ws_repo.get_by_id(ws_id_final)
            if not ws:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Workstation {ws_id_final} no encontrada.",
                )
            if ws.laboratorio_id != lab_id_final:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La workstation asignada no pertenece al laboratorio del equipo.",
                )

        for campo, valor in datos.items():
            setattr(equipo, campo, valor)

        return self.equipo_repo.update(equipo)

    def eliminar_equipo(self, equipo_id: int) -> None:
        equipo = self.obtener_equipo(equipo_id)
        self.equipo_repo.delete(equipo)