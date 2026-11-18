from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación, sobreescribible mediante variables de entorno."""

    APP_NAME: str = "Sistema de Inventario y Gestión de Laboratorios"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Driver psycopg 3 (SQLAlchemy: postgresql+psycopg://).
    DATABASE_URL: str = (
        "postgresql+psycopg://labtracker:labtracker@localhost:5432/labtracker"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
