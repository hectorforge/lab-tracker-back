"""Capa HTTP: endpoints, respuestas estándar y manejo centralizado de errores."""

from .api_response import ApiResponse, DetalleError
from .exception_handlers import registrar_manejadores_excepciones
from .pagination import (
    get_paginacion,
    mapear_pagina,
    Pagina,
    ParametrosPaginacion,
)
