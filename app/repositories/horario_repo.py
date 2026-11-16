from datetime import date, time
from typing import Optional, List
from sqlmodel import Session, select
from app.models.lab_models import Horario, EstadoHorario, AsignacionWorkstation
from app.repositories.base_repository import BaseRepository
from app.repositories.interfaces import AbstractHorarioRepository


class HorarioRepository(BaseRepository[Horario], AbstractHorarioRepository):
    def __init__(self, session: Session):
        super().__init__(Horario, session)

    def get_conflictos(
        self, laboratorio_id: int, fecha: date, hora_inicio: time, hora_fin: time
    ) -> List[Horario]:
        statement = select(Horario).where(
            Horario.laboratorio_id == laboratorio_id,
            Horario.fecha == fecha,
            Horario.estado.in_([EstadoHorario.PROGRAMADO, EstadoHorario.EN_CURSO]),
            Horario.hora_inicio < hora_fin,
            Horario.hora_fin > hora_inicio,
        )
        return list(self.session.exec(statement).all())

    def get_by_laboratorio_y_fecha(
        self, laboratorio_id: int, fecha: Optional[date] = None
    ) -> List[Horario]:
        statement = select(Horario).where(Horario.laboratorio_id == laboratorio_id)
        if fecha is not None:
            statement = statement.where(Horario.fecha == fecha)
        statement = statement.order_by(Horario.fecha.desc(), Horario.hora_inicio.asc())
        return list(self.session.exec(statement).all())

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

    def get_asignaciones_por_horario(
        self, horario_id: int
    ) -> List[AsignacionWorkstation]:
        statement = select(AsignacionWorkstation).where(
            AsignacionWorkstation.horario_id == horario_id
        )
        return list(self.session.exec(statement).all())

    def get_historial_alumno(self, codigo_alumno: str) -> List[AsignacionWorkstation]:
        statement = (
            select(AsignacionWorkstation)
            .where(AsignacionWorkstation.codigo_alumno == codigo_alumno)
            .order_by(AsignacionWorkstation.fecha_asignacion.desc())
        )
        return list(self.session.exec(statement).all())