from typing import Generic, TypeVar, Type, Optional, List

from sqlalchemy import func
from sqlmodel import Session, select

from app.api.pagination import Pagina, ParametrosPaginacion

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, id: int) -> Optional[ModelType]:
        statement = select(self.model).where(self.model.id == id)
        return self.session.exec(statement).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        statement = select(self.model).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def paginar(
        self, statement, paginacion: ParametrosPaginacion
    ) -> Pagina[ModelType]:
        """Aplica offset/limit y calcula totales en la propia consulta."""
        consulta_conteo = select(func.count()).select_from(self.model)
        if statement.whereclause is not None:
            consulta_conteo = consulta_conteo.where(statement.whereclause)
        total = self.session.exec(consulta_conteo).one()
        consulta = statement.offset(paginacion.offset).limit(paginacion.limit)
        items = list(self.session.exec(consulta).all())
        return Pagina.crear(items, total, paginacion)

    def create(self, obj: ModelType) -> ModelType:
        validar = getattr(obj, "validar", None)
        if callable(validar):
            validar()
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, obj: ModelType) -> ModelType:
        validar = getattr(obj, "validar", None)
        if callable(validar):
            validar()
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.session.delete(obj)
        self.session.commit()
