from typing import Optional

from sqlmodel import Session, select

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import Workstation
from app.repositories.base_repository import BaseRepository
from app.repositories.interfaces import AbstractWorkstationRepository


class WorkstationRepository(BaseRepository[Workstation], AbstractWorkstationRepository):
    def __init__(self, session: Session):
        super().__init__(Workstation, session)

    def get_by_codigo_y_laboratorio(
        self, codigo: str, laboratorio_id: int
    ) -> Optional[Workstation]:
        statement = select(Workstation).where(
            Workstation.codigo == codigo.strip().upper(),
            Workstation.laboratorio_id == laboratorio_id,
        )
        return self.session.exec(statement).first()

    def listar(
        self,
        paginacion: ParametrosPaginacion,
        laboratorio_id: Optional[int] = None,
    ) -> Pagina[Workstation]:
        statement = select(Workstation)
        if laboratorio_id is not None:
            statement = statement.where(Workstation.laboratorio_id == laboratorio_id)
        return self.paginar(statement, paginacion)
