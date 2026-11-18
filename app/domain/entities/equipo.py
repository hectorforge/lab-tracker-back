from datetime import date
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.domain.entities.enums import (
    CategoriaTipoEquipo,
    EstadoEquipo,
    Moneda,
)


if TYPE_CHECKING:
    from app.domain.entities.laboratorio import Laboratorio
    from app.domain.entities.workstation import Workstation
    from app.domain.entities.tipo_equipo import TipoEquipo
    from app.domain.entities.incidente import Incidente
    from app.domain.entities.licencia import Licencia


class Equipo(SQLModel, table=True):
    __tablename__ = "equipos"

    id: Optional[int] = Field(default=None, primary_key=True)
    codigo_patrimonial: str = Field(
        max_length=50, unique=True, index=True, nullable=False
    )
    categoria: CategoriaTipoEquipo = Field(index=True, nullable=False)
    marca: str = Field(max_length=60, nullable=False)
    modelo: str = Field(max_length=80, nullable=False)
    numero_serie: Optional[str] = Field(default=None, max_length=80)
    caracteristicas: str = Field(max_length=500, nullable=False)
    estado: EstadoEquipo = Field(default=EstadoEquipo.OPERATIVO, nullable=False)
    laboratorio_id: int = Field(foreign_key="laboratorios.id", nullable=False)
    workstation_id: Optional[int] = Field(
        default=None, foreign_key="workstations.id", nullable=True
    )
    tipo_equipo_id: Optional[int] = Field(
        default=None, foreign_key="tipos_equipo.id", nullable=True
    )
    costo_estimado: Optional[float] = Field(default=None, ge=0)
    costo_adquisicion: Optional[float] = Field(default=None, ge=0)
    moneda: Moneda = Field(default=Moneda.PEN, nullable=False)
    fecha_adquisicion: Optional[date] = Field(default=None)
    proveedor: Optional[str] = Field(default=None, max_length=120)
    garantia_hasta: Optional[date] = Field(default=None)
    observaciones: Optional[str] = Field(default=None, max_length=500)
    url_imagen: Optional[str] = Field(default=None, max_length=500)

    laboratorio: Optional["Laboratorio"] = Relationship(back_populates="equipos")
    workstation: Optional["Workstation"] = Relationship(back_populates="equipos")
    tipo_equipo: Optional["TipoEquipo"] = Relationship(back_populates="equipos")
    incidentes: List["Incidente"] = Relationship(back_populates="equipo")
    licencias: List["Licencia"] = Relationship(
        back_populates="equipo",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    def validar(self) -> None:
        if self.costo_estimado is not None and self.costo_estimado < 0:
            raise ValueError("El costo estimado no puede ser negativo.")
        if self.costo_adquisicion is not None and self.costo_adquisicion < 0:
            raise ValueError("El costo de adquisición no puede ser negativo.")
        if (
            self.garantia_hasta
            and self.fecha_adquisicion
            and self.garantia_hasta < self.fecha_adquisicion
        ):
            raise ValueError("La garantía no puede vencer antes de la adquisición.")
