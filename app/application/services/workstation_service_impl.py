from app.api.pagination import mapear_pagina, Pagina, ParametrosPaginacion
from app.application.interfaces import AbstractWorkstationService
from app.domain.exceptions import BadRequestException, NotFoundException
from app.domain.repositories import (
    AbstractLaboratorioRepository,
    AbstractWorkstationRepository,
)
from app.application.dtos import (
    ActualizarWorkstationDTO,
    CrearWorkstationDTO,
    WorkstationDTO,
)
from app.domain.entities import Workstation


class WorkstationService(AbstractWorkstationService):
    def __init__(
        self,
        ws_repo: AbstractWorkstationRepository,
        lab_repo: AbstractLaboratorioRepository,
    ):
        self.ws_repo = ws_repo
        self.lab_repo = lab_repo

    def crear_workstation(self, data: CrearWorkstationDTO) -> WorkstationDTO:
        lab = self.lab_repo.get_by_id(data.laboratorio_id)
        if not lab:
            raise NotFoundException(f"Laboratorio {data.laboratorio_id} no encontrado.")
        if self.ws_repo.get_by_codigo_y_laboratorio(data.codigo, data.laboratorio_id):
            raise BadRequestException(
                f"Ya existe la workstation '{data.codigo}' en este laboratorio."
            )

        parametros = ParametrosPaginacion(pagina=1, tamano_pagina=1)
        cantidad_actual = self.ws_repo.listar(
            parametros, laboratorio_id=data.laboratorio_id
        ).total
        if cantidad_actual >= lab.capacidad_workstations:
            raise BadRequestException(
                f"El laboratorio '{lab.nombre}' alcanzó su capacidad máxima."
            )

        entidad = self.ws_repo.create(Workstation(**data.model_dump()))
        return WorkstationDTO.model_validate(entidad)

    def listar_por_laboratorio(
        self, paginacion: ParametrosPaginacion, lab_id: int
    ) -> Pagina[WorkstationDTO]:
        if not self.lab_repo.get_by_id(lab_id):
            raise NotFoundException(f"Laboratorio {lab_id} no encontrado.")
        pagina = self.ws_repo.listar(paginacion, laboratorio_id=lab_id)
        return mapear_pagina(pagina, WorkstationDTO.model_validate)

    def obtener_workstation(self, workstation_id: int) -> WorkstationDTO:
        return WorkstationDTO.model_validate(self._obtener_entidad(workstation_id))

    def actualizar_workstation(
        self, workstation_id: int, data: ActualizarWorkstationDTO
    ) -> WorkstationDTO:
        ws = self._obtener_entidad(workstation_id)
        datos = data.model_dump(exclude_unset=True)

        nuevo_lab_id = datos.get("laboratorio_id", ws.laboratorio_id)
        nuevo_codigo = datos.get("codigo", ws.codigo)

        if nuevo_lab_id != ws.laboratorio_id:
            nuevo_lab = self.lab_repo.get_by_id(nuevo_lab_id)
            if not nuevo_lab:
                raise NotFoundException(
                    f"Laboratorio destino {nuevo_lab_id} no encontrado."
                )
            parametros = ParametrosPaginacion(pagina=1, tamano_pagina=1)
            cantidad_destino = self.ws_repo.listar(
                parametros, laboratorio_id=nuevo_lab_id
            ).total
            if cantidad_destino >= nuevo_lab.capacidad_workstations:
                raise BadRequestException(
                    "El laboratorio destino no tiene capacidad disponible."
                )

        if nuevo_codigo != ws.codigo or nuevo_lab_id != ws.laboratorio_id:
            if self.ws_repo.get_by_codigo_y_laboratorio(nuevo_codigo, nuevo_lab_id):
                raise BadRequestException(
                    f"Ya existe el código '{nuevo_codigo}' en el laboratorio destino."
                )

        for campo, valor in datos.items():
            setattr(ws, campo, valor)
        return WorkstationDTO.model_validate(self.ws_repo.update(ws))

    def eliminar_workstation(self, workstation_id: int) -> None:
        self.ws_repo.delete(self._obtener_entidad(workstation_id))

    def _obtener_entidad(self, workstation_id: int) -> Workstation:
        ws = self.ws_repo.get_by_id(workstation_id)
        if not ws:
            raise NotFoundException(f"Workstation {workstation_id} no encontrada.")
        return ws
