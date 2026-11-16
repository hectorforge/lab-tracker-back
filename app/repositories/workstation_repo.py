from typing import Optional, List
from sqlmodel import Session, select
from app.models.lab_models import Workstation
from app.repositories.base_repository import BaseRepository
from app.repositories.interfaces import AbstractWorkstationRepository


class WorkstationRepository(BaseRepository[Workstation], AbstractWorkstationRepository):
    def __init__(self, session: Session):
        super().__init__(Workstation, session)

    def get_by_laboratorio(self, laboratorio_id: int) -> List[Workstation]:
        statement = select(Workstation).where(
            Workstation.laboratorio_id == laboratorio_id
        )
        return list(self.session.exec(statement).all())

    def get_by_codigo_y_laboratorio(
        self, codigo: str, laboratorio_id: int
    ) -> Optional[Workstation]:
        statement = select(Workstation).where(
            Workstation.codigo == codigo,
            Workstation.laboratorio_id == laboratorio_id,
        )
        return self.session.exec(statement).first()