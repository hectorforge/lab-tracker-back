from typing import Generator
from sqlmodel import SQLModel, Session, create_engine
from app.infrastructure.database.config import settings

ES_SQLITE = settings.DATABASE_URL.startswith("sqlite")

_opciones_engine = {"echo": settings.DEBUG}
if ES_SQLITE:
    _opciones_engine["connect_args"] = {"check_same_thread": False}
else:
    _opciones_engine.update(pool_pre_ping=True, pool_size=5, max_overflow=10)

engine = create_engine(settings.DATABASE_URL, **_opciones_engine)


def _migrar_columnas_sqlite() -> None:
    """
    Agrega columnas nuevas a tablas ya existentes en SQLite.

    ``create_all`` crea las tablas nuevas pero no altera las anteriores; sin este
    paso, una base de datos creada con versiones anteriores del modelo fallaría
    al consultar ``equipos`` o ``asignaciones_workstation``.
    """
    columnas_por_tabla = {
        "equipos": {
            "tipo_equipo_id": "INTEGER",
            "categoria": "TEXT DEFAULT 'hardware'",
            "costo_estimado": "REAL",
            "costo_adquisicion": "REAL",
            "moneda": "TEXT DEFAULT 'pen'",
            "fecha_adquisicion": "DATE",
            "proveedor": "VARCHAR(120)",
            "garantia_hasta": "DATE",
            "observaciones": "VARCHAR(500)",
            "url_imagen": "VARCHAR(500)",
        },
        "laboratorios": {"url_imagen": "VARCHAR(500)"},
        "incidentes": {"url_imagenes": "JSON"},
        "asignaciones_workstation": {"alumno_id": "INTEGER"},
    }

    with engine.begin() as connection:
        for tabla, columnas in columnas_por_tabla.items():
            existentes = {
                fila[1]
                for fila in connection.exec_driver_sql(
                    f"PRAGMA table_info({tabla})"
                ).all()
            }
            for columna, tipo in columnas.items():
                if columna not in existentes:
                    connection.exec_driver_sql(
                        f"ALTER TABLE {tabla} ADD COLUMN {columna} {tipo}"
                    )


def create_db_and_tables() -> None:
    """Crea el esquema en el motor configurado.

    En PostgreSQL ``create_all`` genera las tablas que aún no existan; los
    cambios de esquema posteriores se gestionan con migraciones (Alembic).
    En SQLite se aplica además la migración ligera de columnas para bases
    de desarrollo ya creadas.
    """
    # Importar los modelos garantiza que estén registrados en el metadata.
    import app.domain.entities  # noqa: F401

    SQLModel.metadata.create_all(engine)
    if ES_SQLITE:
        _migrar_columnas_sqlite()

    from app.infrastructure.database.seed import sembrar_datos_base

    sembrar_datos_base()


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session