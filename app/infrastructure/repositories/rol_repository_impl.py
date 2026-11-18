from typing import Optional

from sqlmodel import Session, select

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import Rol, RolNombre
from app.domain.repositories import AbstractRolRepository
from app.infrastructure.repositories.base_repository import BaseRepository


class RolRepository(BaseRepository[Rol], AbstractRolRepository):
    def __init__(self, session: Session):
        super().__init__(Rol, session)

    def get_by_nombre(self, nombre: str | RolNombre) -> Optional[Rol]:
        valor = nombre.value if isinstance(nombre, RolNombre) else nombre
        statement = select(Rol).where(Rol.nombre == valor.strip().lower())
        return self.session.exec(statement).first()

    def listar(
        self, paginacion: ParametrosPaginacion, solo_activos: bool = False
    ) -> Pagina[Rol]:
        statement = select(Rol)
        if solo_activos:
            statement = statement.where(Rol.es_activo.is_(True))
        return self.paginar(statement, paginacion)
