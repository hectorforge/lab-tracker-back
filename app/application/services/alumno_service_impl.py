from datetime import datetime, timezone
from typing import Optional

from app.domain.exceptions import BadRequestException, ConflictException, NotFoundException
from app.api.pagination import mapear_pagina, Pagina, ParametrosPaginacion
from app.application.dtos import AlumnoDTO, ActualizarAlumnoDTO, CrearAlumnoDTO
from app.domain.entities import Alumno, EstadoAlumno
from app.domain.repositories import AbstractAlumnoRepository
from app.application.interfaces import AbstractAlumnoService


class AlumnoService(AbstractAlumnoService):
    def __init__(self, alumno_repo: AbstractAlumnoRepository):
        self.alumno_repo = alumno_repo

    def crear_alumno(self, data: CrearAlumnoDTO) -> AlumnoDTO:
        if self.alumno_repo.get_by_codigo(data.codigo):
            raise BadRequestException(f"El código de alumno '{data.codigo}' ya está registrado.")
        if self.alumno_repo.get_by_correo(data.correo_institucional):
            raise BadRequestException(f"El correo institucional '{data.correo_institucional}' "
                    "ya pertenece a otro alumno.")
        entidad = self.alumno_repo.create(Alumno(**data.model_dump()))
        return AlumnoDTO.model_validate(entidad)

    def listar_alumnos(
        self,
        paginacion: ParametrosPaginacion,
        carrera: Optional[str] = None,
        estado: Optional[EstadoAlumno] = None,
        busqueda: Optional[str] = None,
    ) -> Pagina[AlumnoDTO]:
        pagina = self.alumno_repo.listar(paginacion, carrera, estado, busqueda)
        return mapear_pagina(pagina, AlumnoDTO.model_validate)

    def obtener_alumno(self, alumno_id: int) -> AlumnoDTO:
        entidad = self.alumno_repo.get_by_id(alumno_id)
        if not entidad:
            raise NotFoundException(f"Alumno {alumno_id} no encontrado.")
        return AlumnoDTO.model_validate(entidad)

    def actualizar_alumno(self, alumno_id: int, data: ActualizarAlumnoDTO) -> AlumnoDTO:
        entidad = self.alumno_repo.get_by_id(alumno_id)
        if not entidad:
            raise NotFoundException(f"Alumno {alumno_id} no encontrado.")

        datos = data.model_dump(exclude_unset=True)
        if datos.get("codigo"):
            existente = self.alumno_repo.get_by_codigo(datos["codigo"])
            if existente and existente.id != alumno_id:
                raise BadRequestException("El código de alumno ya pertenece a otro registro.")
        if datos.get("correo_institucional"):
            otro = self.alumno_repo.get_by_correo(datos["correo_institucional"])
            if otro and otro.id != alumno_id:
                raise BadRequestException("El correo institucional ya pertenece a otro alumno.")

        for campo, valor in datos.items():
            setattr(entidad, campo, valor)
        entidad.actualizado_en = datetime.now(timezone.utc)
        actualizado = self.alumno_repo.update(entidad)
        return AlumnoDTO.model_validate(actualizado)

    def eliminar_alumno(self, alumno_id: int) -> None:
        entidad = self.alumno_repo.get_by_id(alumno_id)
        if not entidad:
            raise NotFoundException(f"Alumno {alumno_id} no encontrado.")
        if entidad.matriculas:
            raise ConflictException("No se puede eliminar un alumno con matrículas registradas.")
        self.alumno_repo.delete(entidad)
