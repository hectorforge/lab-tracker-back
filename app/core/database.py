from typing import Generator
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=connect_args,
)


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
        },
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
    # Importar los modelos garantiza que estén registrados en el metadata.
    import app.models  # noqa: F401

    SQLModel.metadata.create_all(engine)
    if settings.DATABASE_URL.startswith("sqlite"):
        _migrar_columnas_sqlite()


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session