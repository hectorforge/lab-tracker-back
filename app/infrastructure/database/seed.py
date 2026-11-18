"""Datos iniciales del sistema interno (roles y administrador)."""

from sqlmodel import Session

from app.domain.entities import Rol, RolNombre, Usuario
from app.domain.security import hash_password
from app.infrastructure.database.config import settings
from app.infrastructure.database.database import engine
from app.infrastructure.repositories import RolRepository, UsuarioRepository

ROLES_INICIALES = {
    RolNombre.ADMINISTRADOR: "Acceso total a todas las areas del sistema.",
    RolNombre.GESTION_LABORATORIOS: (
        "Consulta de laboratorios, equipos, alumnos matriculados e incidentes."
    ),
    RolNombre.DOCENTE: (
        "Consulta de horarios, matriculas y asignaciones; puede reportar incidentes."
    ),
}


def sembrar_datos_base() -> None:
    """Crea los roles por defecto y el usuario administrador si no existen."""
    with Session(engine) as session:
        rol_repo = RolRepository(session)
        usuario_repo = UsuarioRepository(session)

        for nombre, descripcion in ROLES_INICIALES.items():
            if not rol_repo.get_by_nombre(nombre):
                rol_repo.create(
                    Rol(nombre=nombre.value, descripcion=descripcion, es_activo=True)
                )

        admin_rol = rol_repo.get_by_nombre(RolNombre.ADMINISTRADOR)
        if admin_rol and not usuario_repo.get_by_username(settings.ADMIN_USERNAME):
            usuario_repo.create(
                Usuario(
                    username=settings.ADMIN_USERNAME,
                    nombres="Administrador",
                    apellidos="del Sistema",
                    correo="admin@universidad.edu.pe",
                    password_hash=hash_password(settings.ADMIN_PASSWORD),
                    url_imagen=None,
                    activo=True,
                    rol_id=admin_rol.id,
                )
            )
