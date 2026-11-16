from typing import Optional, List
from sqlmodel import Session, select
from app.models.lab_models import Laboratorio, EstadoLaboratorio
from app.repositories.base_repository import BaseRepository
from app.repositories.interfaces import AbstractLaboratorioRepository


class LaboratorioRepository(BaseRepository[Laboratorio], AbstractLaboratorioRepository):
    def __init__(self, session: Session):
        super().__init__(Laboratorio, session)

    def get_by_codigo(self, codigo: str) -> Optional[Laboratorio]:
        statement = select(Laboratorio).where(Laboratorio.codigo == codigo)
        return self.session.exec(statement).first()

    def get_disponibles(self) -> List[Laboratorio]:
        statement = select(Laboratorio).where(
            Laboratorio.estado == EstadoLaboratorio.DISPONIBLE
        )
        return list(self.session.exec(statement).all())