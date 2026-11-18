from datetime import date, time
from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.api.pagination import Pagina, ParametrosPaginacion
from app.domain.entities import AsignacionWorkstation, EstadoHorario, Horario
from app.infrastructure.repositories.base_repository import BaseRepository
from app.domain.repositories import AbstractHorarioRepository


class HorarioRepository(BaseRepository[Horario], AbstractHorarioRepository):
    def __init__(self, session: Session):
        super().__init__(Horario, session)

    def get_conflictos(
        self, laboratorio_id: int, fecha: date, hora_inicio: time, hora_fin: time
    ) -> list:
        statement = select(Horario).where(
            Horario.laboratorio_id == laboratorio_id,
            Horario.fecha == fecha,
            Horario.estado.in_([EstadoHorario.PROGRAMADO, EstadoHorario.EN_CURSO]),
            Horario.hora_inicio < hora_fin,
            Horario.hora_fin > hora_inicio,
        )
        return list(self.session.exec(statement).all())

    def listar(
        self,
        paginacion: ParametrosPaginacion,
        laboratorio_id: Optional[int] = None,
        fecha: Optional[date] = None,
        estado: Optional[EstadoHorario] = None,
    ) -> Pagina[Horario]:
        statement = select(Horario)
        if laboratorio_id is not None:
            statement = statement.where(Horario.laboratorio_id == laboratorio_id)
        if fecha is not None:
            statement = statement.where(Horario.fecha == fecha)
        if estado is not None:
            statement = statement.where(Horario.estado == estado)
        ordenado = statement.order_by(Horario.fecha.desc(), Horario.hora_inicio.asc())
        return self.paginar(ordenado, paginacion)

    def create_asignacion(
        self, asignacion: AsignacionWorkstation
    ) -> AsignacionWorkstation:
        self.session.add(asignacion)
        self.session.commit()
        self.session.refresh(asignacion)
        return asignacion

    def get_asignacion_por_horario_y_workstation(
        self, horario_id: int, workstation_id: int
    ) -> Optional[AsignacionWorkstation]:
        statement = select(AsignacionWorkstation).where(
            AsignacionWorkstation.horario_id == horario_id,
            AsignacionWorkstation.workstation_id == workstation_id,
        )
        return self.session.exec(statement).first()

    def get_asignacion_por_horario_y_alumno(
        self, horario_id: int, codigo_alumno: str
    ) -> Optional[AsignacionWorkstation]:
        statement = select(AsignacionWorkstation).where(
            AsignacionWorkstation.horario_id == horario_id,
            AsignacionWorkstation.codigo_alumno == codigo_alumno,
        )
        return self.session.exec(statement).first()

    def listar_asignaciones(
        self,
        paginacion: ParametrosPaginacion,
        horario_id: Optional[int] = None,
        codigo_alumno: Optional[str] = None,
    ) -> Pagina[AsignacionWorkstation]:
        statement = select(AsignacionWorkstation)
        if horario_id is not None:
            statement = statement.where(
                AsignacionWorkstation.horario_id == horario_id
            )
        if codigo_alumno is not None:
            statement = statement.where(
                AsignacionWorkstation.codigo_alumno == codigo_alumno
            )
        return self.paginar(statement, paginacion)

    def listar_historial_alumno(
        self, paginacion: ParametrosPaginacion, codigo_alumno: str
    ) -> Pagina[AsignacionWorkstation]:
        statement = (
            select(AsignacionWorkstation)
            .where(AsignacionWorkstation.codigo_alumno == codigo_alumno)
            .order_by(AsignacionWorkstation.fecha_asignacion.desc())
        )
        return self.paginar(statement, paginacion)
