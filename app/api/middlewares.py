"""Middlewares HTTP: limitación de peticiones y cabeceras de seguridad."""

import threading
import time
from collections import defaultdict, deque

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.api_response import ApiResponse
from app.infrastructure.database.config import settings

VENTANA_SEGUNDOS = 60


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Limita peticiones por IP en una ventana deslizante de 60 segundos.

    El endpoint de login usa un límite más estricto para mitigar fuerza bruta.
    El estado se mantiene en memoria; en despliegues con varias réplicas se
    debe sustituir por un backend compartido (por ejemplo Redis).
    """

    def __init__(self, app):
        super().__init__(app)
        self._solicitudes: dict[tuple[str, str], deque] = defaultdict(deque)
        self._bloqueo = threading.Lock()

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host if request.client else "desconocida"
        es_login = request.url.path.startswith("/auth/login")
        clave = (ip, "login" if es_login else "general")
        limite = (
            settings.LOGIN_RATE_LIMIT_PER_MINUTE
            if es_login
            else settings.RATE_LIMIT_PER_MINUTE
        )
        ahora = time.monotonic()

        with self._bloqueo:
            cola = self._solicitudes[clave]
            while cola and ahora - cola[0] >= VENTANA_SEGUNDOS:
                cola.popleft()

            if len(cola) >= limite:
                reintentar = max(1, int(VENTANA_SEGUNDOS - (ahora - cola[0])) + 1)
                cuerpo = ApiResponse.fail(
                    message="Demasiadas peticiones. Intente nuevamente en unos segundos.",
                    status=429,
                    errors=[
                        {
                            "codigo": "RATE_LIMIT_EXCEEDED",
                            "mensaje": f"Máximo {limite} peticiones por minuto.",
                        }
                    ],
                    path=request.url.path,
                ).model_dump(mode="json")
                return JSONResponse(
                    status_code=429,
                    content=cuerpo,
                    headers={"Retry-After": str(reintentar)},
                )

            cola.append(ahora)
            restantes = limite - len(cola)

        respuesta = await call_next(request)
        respuesta.headers["X-RateLimit-Limit"] = str(limite)
        respuesta.headers["X-RateLimit-Remaining"] = str(restantes)
        return respuesta


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Añade cabeceras HTTP de protección básica a todas las respuestas."""

    async def dispatch(self, request: Request, call_next):
        respuesta = await call_next(request)
        respuesta.headers["X-Content-Type-Options"] = "nosniff"
        respuesta.headers["X-Frame-Options"] = "DENY"
        respuesta.headers["Referrer-Policy"] = "no-referrer"
        respuesta.headers["X-XSS-Protection"] = "1; mode=block"
        return respuesta
