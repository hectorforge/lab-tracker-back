import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.api_response import ApiResponse
from app.domain.exceptions import AppException

logger = logging.getLogger(__name__)


def _serializar(response: ApiResponse) -> dict:
    return response.model_dump(mode="json")


def registrar_manejadores_excepciones(app: FastAPI) -> None:
    """Centraliza la conversión de cualquier excepción a ApiResponse."""

    @app.exception_handler(AppException)
    async def manejar_app_exception(request: Request, exc: AppException):
        errores = [{"codigo": exc.code, "mensaje": exc.message}]
        errores.extend(exc.errors)
        return JSONResponse(
            status_code=exc.status_code,
            content=_serializar(
                ApiResponse.fail(
                    message=exc.message,
                    status=exc.status_code,
                    details=exc.details,
                    errors=errores,
                    path=request.url.path,
                )
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def manejar_validacion(request: Request, exc: RequestValidationError):
        errores = []
        for error in exc.errors():
            campo = ".".join(str(p) for p in error.get("loc", [])[1:]) or None
            errores.append(
                {
                    "codigo": str(error.get("type", "validation_error")).upper(),
                    "mensaje": str(error.get("msg", "Dato inválido.")),
                    "campo": campo,
                }
            )
        return JSONResponse(
            status_code=422,
            content=_serializar(
                ApiResponse.fail(
                    message="La solicitud no pasó la validación de esquema.",
                    status=422,
                    errors=errores,
                    path=request.url.path,
                )
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def manejar_http_exception(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=_serializar(
                ApiResponse.fail(
                    message=str(exc.detail),
                    status=exc.status_code,
                    errors=[
                        {
                            "codigo": f"HTTP_{exc.status_code}",
                            "mensaje": str(exc.detail),
                        }
                    ],
                    path=request.url.path,
                )
            ),
        )

    @app.exception_handler(Exception)
    async def manejar_exception_no_controlada(request: Request, exc: Exception):
        logger.exception("Error no controlado en %s", request.url.path, exc_info=exc)
        return JSONResponse(
            status_code=500,
            content=_serializar(
                ApiResponse.fail(
                    message="Ocurrió un error inesperado. Contacte al administrador.",
                    status=500,
                    errors=[
                        {
                            "codigo": "INTERNAL_ERROR",
                            "mensaje": "Error no controlado.",
                        }
                    ],
                    path=request.url.path,
                )
            ),
        )
