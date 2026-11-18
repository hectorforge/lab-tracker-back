from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import Usuario
from app.domain.repositories import AbstractUsuarioRepository
from app.infrastructure.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Usuario], AbstractUsuarioRepository):
    def __init__(self, session: Session):
        super().__init__(Usuario, session)

    def get_by_username(self, username: str) -> Optional[Usuario]:
        statement = (
            select(Usuario)
            .where(Usuario.username == username.strip().lower())
            .options(selectinload(Usuario.rol))
        )
        return self.session.exec(statement).first()

    def get_by_correo(self, correo: str) -> Optional[Usuario]:
        statement = select(Usuario).where(
            Usuario.correo == correo.strip().lower()
        )
        return self.session.exec(statement).first()

    def get_by_id(self, id: int) -> Optional[Usuario]:
        statement = (
            select(Usuario)
            .where(Usuario.id == id)
            .options(selectinload(Usuario.rol))
        )
        return self.session.exec(statement).first()

    def listar(
        self,
        paginacion: ParametrosPaginacion,
        rol_id: Optional[int] = None,
        solo_activos: bool = False,
        busqueda: Optional[str] = None,
    ) -> Pagina[Usuario]:
        statement = select(Usuario)
        if rol_id is not None:
            statement = statement.where(Usuario.rol_id == rol_id)
        if solo_activos:
            statement = statement.where(Usuario.activo.is_(True))
        if busqueda:
            termino = f"%{busqueda.strip()}%"
            statement = statement.where(
                Usuario.username.ilike(termino)
                | Usuario.nombres.ilike(termino)
                | Usuario.apellidos.ilike(termino)
            )
        return self.paginar(statement, paginacion)
