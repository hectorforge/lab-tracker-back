from typing import Dict, Optional, Set

from sqlmodel import Session, select

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import Alumno, EstadoAlumno
from app.repositories.base_repository import BaseRepository
from app.repositories.interfaces import AbstractAlumnoRepository


class AlumnoRepository(BaseRepository[Alumno], AbstractAlumnoRepository):
    def __init__(self, session: Session):
        super().__init__(Alumno, session)

    def get_by_codigo(self, codigo: str) -> Optional[Alumno]:
        statement = select(Alumno).where(Alumno.codigo == codigo.strip().upper())
        return self.session.exec(statement).first()

    def get_by_correo(self, correo: str) -> Optional[Alumno]:
        statement = select(Alumno).where(
            Alumno.correo_institucional == correo.strip().lower()
        )
        return self.session.exec(statement).first()

    def get_by_codigos(self, codigos: Set[str]) -> Dict[str, Alumno]:
        if not codigos:
            return {}
        normalizados = {c.strip().upper() for c in codigos}
        statement = select(Alumno).where(Alumno.codigo.in_(normalizados))
        return {alumno.codigo: alumno for alumno in self.session.exec(statement).all()}

    def get_by_correos(self, correos: Set[str]) -> Set[str]:
        if not correos:
            return set()
        normalizados = {c.strip().lower() for c in correos}
        statement = select(Alumno.correo_institucional).where(
            Alumno.correo_institucional.in_(normalizados)
        )
        return set(self.session.exec(statement).all())

    def listar(
        self,
        paginacion: ParametrosPaginacion,
        carrera: Optional[str] = None,
        estado: Optional[EstadoAlumno] = None,
        busqueda: Optional[str] = None,
    ) -> Pagina[Alumno]:
        statement = select(Alumno)
        if carrera:
            statement = statement.where(Alumno.carrera.ilike(f"%{carrera.strip()}%"))
        if estado is not None:
            statement = statement.where(Alumno.estado == estado)
        if busqueda:
            termino = f"%{busqueda.strip()}%"
            statement = statement.where(
                Alumno.nombres.ilike(termino)
                | Alumno.apellidos.ilike(termino)
                | Alumno.codigo.ilike(termino)
                | Alumno.correo_institucional.ilike(termino)
            )
        ordenado = statement.order_by(Alumno.apellidos.asc(), Alumno.nombres.asc())
        return self.paginar(ordenado, paginacion)
