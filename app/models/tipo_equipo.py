from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.comun import _ahora, PATRON_CODIGO
from app.models.enums import (
    CategoriaTipoEquipo,
    EstadoTipoEquipo,
    Moneda,
)


class TipoEquipo(SQLModel, table=True):
    """Catálogo institucional: define etiquetas/categorías de equipos tecnológicos."""

    __tablename__ = "tipos_equipo"

    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str = Field(max_length=20, unique=True, index=True, nullable=False)
    nombre: str = Field(max_length=100, nullable=False)
    descripcion: str = Field(max_length=500, nullable=False)
    categoria: CategoriaTipoEquipo = Field(index=True, nullable=False)
    especificaciones_minimas: Optional[str] = Field(default=None, max_length=500)
    vida_util_meses: Optional[int] = Field(default=None, ge=1, le=600)
    requiere_mantenimiento: bool = Field(default=False, nullable=False)
    requiere_licencia: bool = Field(default=False, nullable=False)
    costo_referencial: Optional[float] = Field(default=None, ge=0)
    moneda: Moneda = Field(default=Moneda.PEN, nullable=False)
    estado: EstadoTipoEquipo = Field(default=EstadoTipoEquipo.ACTIVO, nullable=False)
    creado_en: datetime = Field(default_factory=_ahora, nullable=False)
    actualizado_en: datetime = Field(default_factory=_ahora, nullable=False)

    equipos: List["Equipo"] = Relationship(back_populates="tipo_equipo")
    licencias: List["Licencia"] = Relationship(
        back_populates="tipo_equipo",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    def validar(self) -> None:
        """Validación de integridad a nivel de modelo (se ejecuta en el repositorio)."""
        if not PATRON_CODIGO.match(self.codigo.strip().upper()):
            raise ValueError("El código del tipo de equipo contiene caracteres inválidos.")
        if self.costo_referencial is not None and self.costo_referencial < 0:
            raise ValueError("El costo referencial no puede ser negativo.")
        if self.vida_util_meses is not None and not 1 <= self.vida_util_meses <= 600:
            raise ValueError("La vida útil debe estar entre 1 y 600 meses.")
