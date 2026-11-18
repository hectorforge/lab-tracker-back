from typing import Generic, List, TypeVar

from fastapi import Query
from pydantic import BaseModel, Field

T = TypeVar("T")


class ParametrosPaginacion(BaseModel):
    """Parámetros de paginación que el router entrega al repositorio."""

    pagina: int = Field(default=1, ge=1)
    tamano_pagina: int = Field(default=10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.pagina - 1) * self.tamano_pagina

    @property
    def limit(self) -> int:
        return self.tamano_pagina


class Pagina(BaseModel, Generic[T]):
    """Resultado paginado devuelto por los repositorios."""

    items: List[T]
    total: int
    pagina: int
    tamano_pagina: int
    total_paginas: int

    @classmethod
    def crear(cls, items: List[T], total: int, params: ParametrosPaginacion):
        total_paginas = (total + params.tamano_pagina - 1) // params.tamano_pagina
        return cls(
            items=items,
            total=total,
            pagina=params.pagina,
            tamano_pagina=params.tamano_pagina,
            total_paginas=total_paginas,
        )


def mapear_pagina(pagina: Pagina, transformar) -> Pagina:
    """Convierte los items de una página aplicando una función (p. ej. DTO)."""
    params = ParametrosPaginacion(
        pagina=pagina.pagina, tamano_pagina=pagina.tamano_pagina
    )
    return Pagina.crear([transformar(item) for item in pagina.items], pagina.total, params)


def get_paginacion(
    pagina: int = Query(default=1, ge=1, description="Número de página"),
    tamano_pagina: int = Query(
        default=10, ge=1, le=100, description="Registros por página"
    ),
) -> ParametrosPaginacion:
    """Dependencia de FastAPI para construir los parámetros de paginación."""
    return ParametrosPaginacion(pagina=pagina, tamano_pagina=tamano_pagina)
