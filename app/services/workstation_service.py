from typing import List
from fastapi import HTTPException, status
from app.models.lab_models import Workstation
from app.schemas.lab_schemas import WorkstationCreate, WorkstationUpdate
from app.repositories.interfaces import (
    AbstractWorkstationRepository,
    AbstractLaboratorioRepository,
)
from app.services.interfaces import AbstractWorkstationService


class WorkstationService(AbstractWorkstationService):
    def __init__(
        self,
        ws_repo: AbstractWorkstationRepository,
        lab_repo: AbstractLaboratorioRepository,
    ):
        self.ws_repo = ws_repo
        self.lab_repo = lab_repo

    def crear_workstation(self, data: WorkstationCreate) -> Workstation:
        lab = self.lab_repo.get_by_id(data.laboratorio_id)
        if not lab:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Laboratorio {data.laboratorio_id} no encontrado.",
            )

        if self.ws_repo.get_by_codigo_y_laboratorio(data.codigo, data.laboratorio_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe la workstation '{data.codigo}' en este laboratorio.",
            )

        actuales = self.ws_repo.get_by_laboratorio(data.laboratorio_id)
        if len(actuales) >= lab.capacidad_workstations:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El laboratorio '{lab.nombre}' alcanzó su capacidad máxima de {lab.capacidad_workstations} workstations.",
            )

        nueva_ws = Workstation(**data.model_dump())
        return self.ws_repo.create(nueva_ws)

    def listar_por_laboratorio(self, lab_id: int) -> List[Workstation]:
        if not self.lab_repo.get_by_id(lab_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Laboratorio {lab_id} no encontrado.",
            )
        return self.ws_repo.get_by_laboratorio(lab_id)

    def obtener_workstation(self, workstation_id: int) -> Workstation:
        ws = self.ws_repo.get_by_id(workstation_id)
        if not ws:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workstation {workstation_id} no encontrada.",
            )
        return ws

    def actualizar_workstation(
        self, workstation_id: int, data: WorkstationUpdate
    ) -> Workstation:
        ws = self.obtener_workstation(workstation_id)
        datos = data.model_dump(exclude_unset=True)

        nuevo_lab_id = datos.get("laboratorio_id", ws.laboratorio_id)
        nuevo_codigo = datos.get("codigo", ws.codigo)

        if nuevo_lab_id != ws.laboratorio_id:
            nuevo_lab = self.lab_repo.get_by_id(nuevo_lab_id)
            if not nuevo_lab:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Laboratorio destino {nuevo_lab_id} no encontrado.",
                )
            if len(self.ws_repo.get_by_laboratorio(nuevo_lab_id)) >= nuevo_lab.capacidad_workstations:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El laboratorio destino no tiene capacidad disponible.",
                )

        if nuevo_codigo != ws.codigo or nuevo_lab_id != ws.laboratorio_id:
            if self.ws_repo.get_by_codigo_y_laboratorio(nuevo_codigo, nuevo_lab_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe el código '{nuevo_codigo}' en el laboratorio destino.",
                )

        for campo, valor in datos.items():
            setattr(ws, campo, valor)

        return self.ws_repo.update(ws)

    def eliminar_workstation(self, workstation_id: int) -> None:
        ws = self.obtener_workstation(workstation_id)
        self.ws_repo.delete(ws)