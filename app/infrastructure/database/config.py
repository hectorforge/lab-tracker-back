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

    # Seguridad (JWT)
    JWT_SECRET_KEY: str = "cambiar-este-secreto-en-produccion-labtracker-2026"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    # Usuario administrador creado al arrancar si no existe.
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"

    # Limitacion de peticiones (ventana de 60 segundos)
    RATE_LIMIT_PER_MINUTE: int = 100
    LOGIN_RATE_LIMIT_PER_MINUTE: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
