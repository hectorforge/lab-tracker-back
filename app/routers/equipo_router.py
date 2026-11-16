from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.core.database import get_session
from app.models.lab_models import TipoEquipo
from app.schemas.lab_schemas import EquipoCreate, EquipoUpdate, EquipoRead
from app.repositories.equipo_repo import EquipoRepository
from app.repositories.laboratorio_repo import LaboratorioRepository
from app.repositories.workstation_repo import WorkstationRepository
from app.services.interfaces import AbstractEquipoService
from app.services.equipo_service import EquipoService

router = APIRouter(prefix="/equipos", tags=["Inventario de Equipos"])


def get_equipo_service(
    session: Session = Depends(get_session),
) -> AbstractEquipoService:
    return EquipoService(
        equipo_repo=EquipoRepository(session),
        lab_repo=LaboratorioRepository(session),
        ws_repo=WorkstationRepository(session),
    )


@router.post("/", response_model=EquipoRead, status_code=status.HTTP_201_CREATED)
def registrar_equipo(
    data: EquipoCreate,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return service.registrar_equipo(data)


@router.get("/", response_model=List[EquipoRead])
def listar_equipos(
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return service.listar_equipos()


@router.get("/laboratorio/{lab_id}", response_model=List[EquipoRead])
def listar_equipos_por_laboratorio(
    lab_id: int,
    tipo: Optional[TipoEquipo] = None,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return service.listar_por_laboratorio(lab_id, tipo)


@router.get("/workstation/{workstation_id}", response_model=List[EquipoRead])
def listar_equipos_por_workstation(
    workstation_id: int,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return service.listar_por_workstation(workstation_id)


@router.get("/{equipo_id}", response_model=EquipoRead)
def obtener_equipo(
    equipo_id: int,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return service.obtener_equipo(equipo_id)


@router.put("/{equipo_id}", response_model=EquipoRead)
def actualizar_equipo(
    equipo_id: int,
    data: EquipoUpdate,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    return service.actualizar_equipo(equipo_id, data)


@router.delete("/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_equipo(
    equipo_id: int,
    service: AbstractEquipoService = Depends(get_equipo_service),
):
    service.eliminar_equipo(equipo_id)