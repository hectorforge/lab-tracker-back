from app.api.pagination import mapear_pagina, Pagina, ParametrosPaginacion
from app.application.interfaces import AbstractLaboratorioService
from app.domain.exceptions import BadRequestException, NotFoundException
from app.domain.repositories import (
    AbstractLaboratorioRepository,
    AbstractWorkstationRepository,
)
from app.application.dtos import (
    ActualizarLaboratorioDTO,
    CrearLaboratorioDTO,
    LaboratorioDTO,
)
from app.domain.entities import Laboratorio


class LaboratorioService(AbstractLaboratorioService):
    def __init__(
        self,
        lab_repo: AbstractLaboratorioRepository,
        ws_repo: AbstractWorkstationRepository,
    ):
        self.lab_repo = lab_repo
        self.ws_repo = ws_repo

    def crear_laboratorio(self, data: CrearLaboratorioDTO) -> LaboratorioDTO:
        if self.lab_repo.get_by_codigo(data.codigo):
            raise BadRequestException(
                f"Ya existe un laboratorio con el código '{data.codigo}'."
            )
        entidad = self.lab_repo.create(Laboratorio(**data.model_dump()))
        return LaboratorioDTO.model_validate(entidad)

    def listar_laboratorios(
        self,
        paginacion: ParametrosPaginacion,
        solo_disponibles: bool = False,
    ) -> Pagina[LaboratorioDTO]:
        pagina = self.lab_repo.listar(paginacion, solo_disponibles)
        return mapear_pagina(pagina, LaboratorioDTO.model_validate)

    def obtener_laboratorio(self, lab_id: int) -> LaboratorioDTO:
        return LaboratorioDTO.model_validate(self._obtener_entidad(lab_id))

    def actualizar_laboratorio(
        self, lab_id: int, data: ActualizarLaboratorioDTO
    ) -> LaboratorioDTO:
        lab = self._obtener_entidad(lab_id)
        datos = data.model_dump(exclude_unset=True)

        if datos.get("codigo") and datos["codigo"] != lab.codigo:
            if self.lab_repo.get_by_codigo(datos["codigo"]):
                raise BadRequestException(
                    f"El código '{datos['codigo']}' ya está en uso."
                )

        if "capacidad_workstations" in datos:
            parametros = ParametrosPaginacion(pagina=1, tamano_pagina=1)
            cantidad_actual = self.ws_repo.listar(
                parametros, laboratorio_id=lab_id
            ).total
            if datos["capacidad_workstations"] < cantidad_actual:
                raise BadRequestException(
                    "La capacidad no puede ser menor a las "
                    f"{cantidad_actual} workstations ya registradas."
                )

        for campo, valor in datos.items():
            setattr(lab, campo, valor)
        return LaboratorioDTO.model_validate(self.lab_repo.update(lab))

    def eliminar_laboratorio(self, lab_id: int) -> None:
        self.lab_repo.delete(self._obtener_entidad(lab_id))

    def _obtener_entidad(self, lab_id: int) -> Laboratorio:
        lab = self.lab_repo.get_by_id(lab_id)
        if not lab:
            raise NotFoundException(f"Laboratorio con ID {lab_id} no encontrado.")
        return lab
