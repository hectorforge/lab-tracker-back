from typing import Optional, List
from sqlmodel import Session, select
from app.models.lab_models import Equipo, TipoEquipo
from app.repositories.base_repository import BaseRepository
from app.repositories.interfaces import AbstractEquipoRepository


class EquipoRepository(BaseRepository[Equipo], AbstractEquipoRepository):
    def __init__(self, session: Session):
        super().__init__(Equipo, session)

    def get_by_codigo_patrimonial(self, codigo_patrimonial: str) -> Optional[Equipo]:
        statement = select(Equipo).where(
            Equipo.codigo_patrimonial == codigo_patrimonial
        )
        return self.session.exec(statement).first()

    def get_by_laboratorio(
        self, laboratorio_id: int, tipo: Optional[TipoEquipo] = None
    ) -> List[Equipo]:
        statement = select(Equipo).where(Equipo.laboratorio_id == laboratorio_id)
        if tipo is not None:
            statement = statement.where(Equipo.tipo == tipo)
        return list(self.session.exec(statement).all())

    def get_by_workstation(self, workstation_id: int) -> List[Equipo]:
        statement = select(Equipo).where(Equipo.workstation_id == workstation_id)
        return list(self.session.exec(statement).all())