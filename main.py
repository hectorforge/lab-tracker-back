from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.core.exception_handlers import registrar_manejadores_excepciones
import app.models  # noqa: F401
from app.routers import (
    laboratorio_router,
    workstation_router,
    equipo_router,
    tipo_equipo_router,
    alumno_router,
    matricula_router,
    licencia_router,
    horario_router,
    incidente_router,
)


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

app.include_router(laboratorio_router.router)
app.include_router(workstation_router.router)
app.include_router(equipo_router.router)
app.include_router(tipo_equipo_router.router)
app.include_router(alumno_router.router)
app.include_router(matricula_router.router)
app.include_router(licencia_router.router)
app.include_router(horario_router.router)
app.include_router(incidente_router.router)


@app.get("/", tags=["Inicio"])
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
    }