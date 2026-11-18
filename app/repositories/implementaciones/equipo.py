from typing import Optional

from sqlmodel import Session, select

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import CategoriaTipoEquipo, Equipo
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

    def listar(
        self,
        paginacion: ParametrosPaginacion,
        laboratorio_id: Optional[int] = None,
        workstation_id: Optional[int] = None,
        categoria: Optional[CategoriaTipoEquipo] = None,
    ) -> Pagina[Equipo]:
        statement = select(Equipo)
        if laboratorio_id is not None:
            statement = statement.where(Equipo.laboratorio_id == laboratorio_id)
        if workstation_id is not None:
            statement = statement.where(Equipo.workstation_id == workstation_id)
        if categoria is not None:
            statement = statement.where(Equipo.categoria == categoria)
        return self.paginar(statement, paginacion)
