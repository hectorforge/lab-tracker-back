from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.domain.entities import EstadoIncidente, PrioridadIncidente


class _IncidenteBaseDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    workstation_id: Optional[int] = Field(default=None, gt=0)
    equipo_id: Optional[int] = Field(default=None, gt=0)
    reportado_por: str = Field(min_length=2, max_length=100)
    descripcion: str = Field(min_length=5, max_length=500)
    prioridad: PrioridadIncidente = PrioridadIncidente.MEDIA
    url_imagenes: Optional[List[str]] = Field(default=None)

    @field_validator("url_imagenes")
    @classmethod
    def validar_urls_imagenes(cls, valor: Optional[List[str]]) -> Optional[List[str]]:
        if valor:
            for url in valor:
                if not url.startswith(("http://", "https://")):
                    raise ValueError(
                        "Cada URL de imagen debe empezar con http:// o https://."
                    )
        return valor

    @model_validator(mode="after")
    def validar_objetivo(self):
        if self.workstation_id is None and self.equipo_id is None:
            raise ValueError("Debe especificar workstation_id o equipo_id.")
        return self


class CrearIncidenteDTO(_IncidenteBaseDTO):
    """DTO de entrada para reportar incidentes."""


class ActualizarEstadoIncidenteDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, from_attributes=True)

    estado: EstadoIncidente
    url_imagenes: Optional[List[str]] = Field(default=None)

    @field_validator("url_imagenes")
    @classmethod
    def validar_urls_imagenes(cls, valor: Optional[List[str]]) -> Optional[List[str]]:
        if valor:
            for url in valor:
                if not url.startswith(("http://", "https://")):
                    raise ValueError(
                        "Cada URL de imagen debe empezar con http:// o https://."
                    )
        return valor


class IncidenteDTO(_IncidenteBaseDTO):
    id: int
    estado: EstadoIncidente
    fecha_reporte: datetime
    fecha_resolucion: Optional[datetime] = None
