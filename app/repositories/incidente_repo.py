from typing import List
from sqlmodel import Session, select, func
from app.models.lab_models import Incidente, EstadoIncidente
from app.repositories.base_repository import BaseRepository
from app.repositories.interfaces import AbstractIncidenteRepository


class IncidenteRepository(BaseRepository[Incidente], AbstractIncidenteRepository):
    def __init__(self, session: Session):
        super().__init__(Incidente, session)

    def get_pendientes(self) -> List[Incidente]:
        statement = (
            select(Incidente)
            .where(Incidente.estado != EstadoIncidente.RESUELTO)
            .order_by(Incidente.fecha_reporte.asc())
        )
        return list(self.session.exec(statement).all())

    def get_by_equipo(self, equipo_id: int) -> List[Incidente]:
        statement = (
            select(Incidente)
            .where(Incidente.equipo_id == equipo_id)
            .order_by(Incidente.fecha_reporte.desc())
        )
        return list(self.session.exec(statement).all())

    def get_by_workstation(self, workstation_id: int) -> List[Incidente]:
        statement = (
            select(Incidente)
            .where(Incidente.workstation_id == workstation_id)
            .order_by(Incidente.fecha_reporte.desc())
        )
        return list(self.session.exec(statement).all())

    def count_abiertos_por_equipo(self, equipo_id: int) -> int:
        statement = select(func.count(Incidente.id)).where(
            Incidente.equipo_id == equipo_id,
            Incidente.estado != EstadoIncidente.RESUELTO,
        )
        return int(self.session.exec(statement).one())

    def count_abiertos_por_workstation(self, workstation_id: int) -> int:
        statement = select(func.count(Incidente.id)).where(
            Incidente.workstation_id == workstation_id,
            Incidente.estado != EstadoIncidente.RESUELTO,
        )
        return int(self.session.exec(statement).one())