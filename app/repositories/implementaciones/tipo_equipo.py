from typing import Optional

from sqlmodel import Session, select

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import CategoriaTipoEquipo, EstadoTipoEquipo, TipoEquipo
from app.repositories.base_repository import BaseRepository
from app.repositories.interfaces import AbstractTipoEquipoRepository


class TipoEquipoRepository(BaseRepository[TipoEquipo], AbstractTipoEquipoRepository):
    def __init__(self, session: Session):
        super().__init__(TipoEquipo, session)

    def get_by_codigo(self, codigo: str) -> Optional[TipoEquipo]:
        statement = select(TipoEquipo).where(
            TipoEquipo.codigo == codigo.strip().upper()
        )
        return self.session.exec(statement).first()

    def listar(
        self,
        paginacion: ParametrosPaginacion,
        solo_activos: bool = False,
        categoria: Optional[CategoriaTipoEquipo] = None,
    ) -> Pagina[TipoEquipo]:
        statement = select(TipoEquipo)
        if solo_activos:
            statement = statement.where(
                TipoEquipo.estado == EstadoTipoEquipo.ACTIVO
            )
        if categoria is not None:
            statement = statement.where(TipoEquipo.categoria == categoria)
        return self.paginar(statement.order_by(TipoEquipo.nombre.asc()), paginacion)
