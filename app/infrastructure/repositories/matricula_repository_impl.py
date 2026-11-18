from typing import Optional, Set

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import Alumno, Matricula
from app.infrastructure.repositories.base_repository import BaseRepository
from app.domain.repositories import AbstractMatriculaRepository


class MatriculaRepository(BaseRepository[Matricula], AbstractMatriculaRepository):
    def __init__(self, session: Session):
        super().__init__(Matricula, session)

    def listar(
        self,
        paginacion: ParametrosPaginacion,
        horario_id: Optional[int] = None,
    ) -> Pagina[Matricula]:
        statement = select(Matricula)
        if horario_id is not None:
            statement = statement.where(Matricula.horario_id == horario_id)
        statement = statement.options(selectinload(Matricula.alumno))
        return self.paginar(statement, paginacion)

    def get_codigos_matriculados(
        self, horario_id: int, codigos: Set[str]
    ) -> Set[str]:
        if not codigos:
            return set()
        normalizados = {c.strip().upper() for c in codigos}
        statement = (
            select(Alumno.codigo)
            .join(Matricula, Matricula.alumno_id == Alumno.id)
            .where(
                Matricula.horario_id == horario_id,
                Alumno.codigo.in_(normalizados),
            )
        )
        return set(self.session.exec(statement).all())

    def get_por_alumno_y_horario(
        self, alumno_id: int, horario_id: int
    ) -> Optional[Matricula]:
        statement = select(Matricula).where(
            Matricula.alumno_id == alumno_id,
            Matricula.horario_id == horario_id,
        )
        return self.session.exec(statement).first()
