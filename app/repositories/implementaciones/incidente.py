from typing import Optional

from sqlmodel import Session, select

from app.core.pagination import Pagina, ParametrosPaginacion
from app.models import EstadoIncidente, Incidente
from app.repositories.base_repository import BaseRepository
from app.repositories.interfaces import AbstractIncidenteRepository


class IncidenteRepository(BaseRepository[Incidente], AbstractIncidenteRepository):
    def __init__(self, session: Session):
        super().__init__(Incidente, session)

    def listar(
        self,
        paginacion: ParametrosPaginacion,
        solo_pendientes: bool = False,
        equipo_id: Optional[int] = None,
        workstation_id: Optional[int] = None,
    ) -> Pagina[Incidente]:
        statement = select(Incidente)
        if solo_pendientes:
            statement = statement.where(
                Incidente.estado.in_(
                    [EstadoIncidente.PENDIENTE, EstadoIncidente.EN_PROCESO]
                )
            )
        if equipo_id is not None:
            statement = statement.where(Incidente.equipo_id == equipo_id)
        if workstation_id is not None:
            statement = statement.where(Incidente.workstation_id == workstation_id)
        return self.paginar(statement, paginacion)

    def count_abiertos_por_equipo(self, equipo_id: int) -> int:
        statement = select(Incidente).where(
            Incidente.equipo_id == equipo_id,
            Incidente.estado.in_(
                [EstadoIncidente.PENDIENTE, EstadoIncidente.EN_PROCESO]
            ),
        )
        return len(self.session.exec(statement).all())

    def count_abiertos_por_workstation(self, workstation_id: int) -> int:
        statement = select(Incidente).where(
            Incidente.workstation_id == workstation_id,
            Incidente.estado.in_(
                [EstadoIncidente.PENDIENTE, EstadoIncidente.EN_PROCESO]
            ),
        )
        return len(self.session.exec(statement).all())
