from typing import List
from datetime import date, time
from sqlalchemy.orm import Session
from app.models.lab_models import Reserva, EstadoReserva
from app.repositories.base_repository import BaseRepository


class ReservaRepository(BaseRepository[Reserva]):
    def __init__(self, db: Session):
        super().__init__(Reserva, db)

    def get_conflictos(
        self,
        laboratorio_id: int,
        fecha: date,
        hora_inicio: time,
        hora_fin: time,
    ) -> List[Reserva]:
        return (
            self.db.query(Reserva)
            .filter(
                Reserva.laboratorio_id == laboratorio_id,
                Reserva.fecha == fecha,
                Reserva.estado == EstadoReserva.ACTIVA,
                Reserva.hora_inicio < hora_fin,
                Reserva.hora_fin > hora_inicio,
            )
            .all()
        )

    def get_by_laboratorio(self, laboratorio_id: int) -> List[Reserva]:
        return (
            self.db.query(Reserva)
            .filter(Reserva.laboratorio_id == laboratorio_id)
            .order_by(Reserva.fecha.desc(), Reserva.hora_inicio.asc())
            .all()
        )

    def get_by_fecha(self, fecha: date) -> List[Reserva]:
        return (
            self.db.query(Reserva)
            .filter(Reserva.fecha == fecha)
            .order_by(Reserva.hora_inicio.asc())
            .all()
        )