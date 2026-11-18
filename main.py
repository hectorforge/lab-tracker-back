from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import registrar_manejadores_excepciones
from app.api.endpoints import (
    alumno_router,
    equipo_router,
    horario_router,
    incidente_router,
    laboratorio_router,
    licencia_router,
    matricula_router,
    tipo_equipo_router,
    workstation_router,
)
from app.infrastructure.database import create_db_and_tables, settings
import app.domain.entities  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

registrar_manejadores_excepciones(app)

for router in (
    laboratorio_router,
    workstation_router,
    equipo_router,
    tipo_equipo_router,
    alumno_router,
    matricula_router,
    licencia_router,
    horario_router,
    incidente_router,
):
    app.include_router(router)


@app.get("/", tags=["Inicio"])
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
    }
