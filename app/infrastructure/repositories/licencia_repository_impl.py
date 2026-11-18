from datetime import date
from typing import Optional

from sqlmodel import Session, select

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import EstadoLicencia, Licencia
from app.infrastructure.repositories.base_repository import BaseRepository
from app.domain.repositories import AbstractLicenciaRepository


class LicenciaRepository(BaseRepository[Licencia], AbstractLicenciaRepository):
    def __init__(self, session: Session):
        super().__init__(Licencia, session)

    def get_by_codigo(self, codigo: str) -> Optional[Licencia]:
        statement = select(Licencia).where(Licencia.codigo == codigo.strip().upper())
        return self.session.exec(statement).first()

    def listar(
        self,
        paginacion: ParametrosPaginacion,
        equipo_id: Optional[int] = None,
        estado: Optional[EstadoLicencia] = None,
    ) -> Pagina[Licencia]:
        statement = select(Licencia)
        if equipo_id is not None:
            statement = statement.where(Licencia.equipo_id == equipo_id)
        if estado is not None:
            statement = statement.where(Licencia.estado == estado)
        return self.paginar(statement, paginacion)

    def get_vigentes(self) -> list:
        statement = select(Licencia).where(
            Licencia.estado == EstadoLicencia.ACTIVA,
            (Licencia.fecha_vencimiento.is_(None))
            | (Licencia.fecha_vencimiento >= date.today()),
        )
        return list(self.session.exec(statement).all())
