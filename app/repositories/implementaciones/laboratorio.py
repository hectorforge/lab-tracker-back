from typing import Optional

from sqlmodel import Session, select

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import EstadoLaboratorio, Laboratorio
from app.repositories.base_repository import BaseRepository
from app.repositories.interfaces import AbstractLaboratorioRepository


class LaboratorioRepository(BaseRepository[Laboratorio], AbstractLaboratorioRepository):
    def __init__(self, session: Session):
        super().__init__(Laboratorio, session)

    def get_by_codigo(self, codigo: str) -> Optional[Laboratorio]:
        statement = select(Laboratorio).where(Laboratorio.codigo == codigo.strip().upper())
        return self.session.exec(statement).first()

    def listar(
        self, paginacion: ParametrosPaginacion, solo_disponibles: bool = False
    ) -> Pagina[Laboratorio]:
        statement = select(Laboratorio)
        if solo_disponibles:
            statement = statement.where(
                Laboratorio.estado == EstadoLaboratorio.DISPONIBLE
            )
        return self.paginar(statement, paginacion)
