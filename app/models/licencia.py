from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.comun import _ahora, PATRON_CODIGO
from app.models.enums import (
    Moneda,
    TipoLicencia,
    EstadoLicencia,
)


class Licencia(SQLModel, table=True):
    """Licencia de software asociada a un equipo (o al catálogo de forma genérica)."""

    __tablename__ = "licencias"

    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str = Field(max_length=50, unique=True, index=True, nullable=False)
    nombre: str = Field(max_length=120, nullable=False)
    tipo: TipoLicencia = Field(default=TipoLicencia.PERPETUA, nullable=False)
    clave_producto: Optional[str] = Field(default=None, max_length=120)
    fabricante: Optional[str] = Field(default=None, max_length=100)
    cantidad_usuarios: int = Field(default=1, ge=1, nullable=False)
    fecha_adquisicion: Optional[date] = Field(default=None)
    fecha_vencimiento: Optional[date] = Field(default=None)
    costo: Optional[float] = Field(default=None, ge=0)
    moneda: Moneda = Field(default=Moneda.PEN, nullable=False)
    estado: EstadoLicencia = Field(default=EstadoLicencia.ACTIVA, nullable=False)
    equipo_id: Optional[int] = Field(
        default=None, foreign_key="equipos.id", nullable=True
    )
    tipo_equipo_id: Optional[int] = Field(
        default=None, foreign_key="tipos_equipo.id", nullable=True
    )
    observaciones: Optional[str] = Field(default=None, max_length=500)
    creado_en: datetime = Field(default_factory=_ahora, nullable=False)
    actualizado_en: datetime = Field(default_factory=_ahora, nullable=False)

    equipo: Optional[Equipo] = Relationship(back_populates="licencias")
    tipo_equipo: Optional[TipoEquipo] = Relationship(back_populates="licencias")

    def validar(self) -> None:
        if not PATRON_CODIGO.match(self.codigo.strip().upper()):
            raise ValueError("El código de licencia contiene caracteres inválidos.")
        if self.costo is not None and self.costo < 0:
            raise ValueError("El costo de la licencia no puede ser negativo.")
        if (
            self.fecha_vencimiento
            and self.fecha_adquisicion
            and self.fecha_vencimiento < self.fecha_adquisicion
        ):
            raise ValueError("La licencia no puede vencer antes de su adquisición.")
        if (
            self.estado == EstadoLicencia.ACTIVA
            and self.fecha_vencimiento
            and self.fecha_vencimiento < date.today()
        ):
            raise ValueError("Una licencia vencida no puede permanecer activa.")
