from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from app.models.lab_models import (
    Laboratorio,
    Workstation,
    Equipo,
    TipoEquipo,
    Horario,
    AsignacionWorkstation,
    Incidente,
)
from app.schemas.lab_schemas import (
    LaboratorioCreate,
    LaboratorioUpdate,
    WorkstationCreate,
    WorkstationUpdate,
    EquipoCreate,
    EquipoUpdate,
    HorarioCreate,
    AsignacionCreate,
    IncidenteCreate,
    IncidenteUpdateEstado,
)


class AbstractLaboratorioService(ABC):
    @abstractmethod
    def crear_laboratorio(self, data: LaboratorioCreate) -> Laboratorio:
        """
        Registra un nuevo laboratorio validando que su código no esté duplicado.

        Args:
            data (LaboratorioCreate): Datos de creación del laboratorio.

        Returns:
            Laboratorio: Laboratorio recién creado.
        """
        pass

    @abstractmethod
    def listar_laboratorios(self, solo_disponibles: bool = False) -> List[Laboratorio]:
        """
        Obtiene la lista de laboratorios registrados.

        Args:
            solo_disponibles (bool): Si es True, filtra solo los laboratorios disponibles.

        Returns:
            List[Laboratorio]: Lista de laboratorios.
        """
        pass

    @abstractmethod
    def obtener_laboratorio(self, lab_id: int) -> Laboratorio:
        """
        Obtiene un laboratorio por su ID o lanza un error 404 si no existe.

        Args:
            lab_id (int): Identificador del laboratorio.

        Returns:
            Laboratorio: Laboratorio encontrado.
        """
        pass

    @abstractmethod
    def actualizar_laboratorio(
        self, lab_id: int, data: LaboratorioUpdate
    ) -> Laboratorio:
        """
        Actualiza los atributos de un laboratorio validando unicidad de código y capacidad.

        Args:
            lab_id (int): Identificador del laboratorio.
            data (LaboratorioUpdate): Campos a modificar.

        Returns:
            Laboratorio: Laboratorio actualizado.
        """
        pass

    @abstractmethod
    def eliminar_laboratorio(self, lab_id: int) -> None:
        """
        Elimina un laboratorio del sistema.

        Args:
            lab_id (int): Identificador del laboratorio a eliminar.

        Returns:
            None
        """
        pass


class AbstractWorkstationService(ABC):
    @abstractmethod
    def crear_workstation(self, data: WorkstationCreate) -> Workstation:
        """
        Registra una nueva workstation dentro de un laboratorio respetando su capacidad.

        Args:
            data (WorkstationCreate): Datos de la workstation.

        Returns:
            Workstation: Workstation creada.
        """
        pass

    @abstractmethod
    def listar_por_laboratorio(self, lab_id: int) -> List[Workstation]:
        """
        Lista todas las workstations pertenecientes a un laboratorio.

        Args:
            lab_id (int): Identificador del laboratorio.

        Returns:
            List[Workstation]: Lista de workstations del laboratorio.
        """
        pass

    @abstractmethod
    def obtener_workstation(self, workstation_id: int) -> Workstation:
        """
        Obtiene una workstation por su ID o lanza error 404 si no existe.

        Args:
            workstation_id (int): Identificador de la workstation.

        Returns:
            Workstation: Workstation encontrada.
        """
        pass

    @abstractmethod
    def actualizar_workstation(
        self, workstation_id: int, data: WorkstationUpdate
    ) -> Workstation:
        """
        Actualiza la información o estado de una workstation.

        Args:
            workstation_id (int): Identificador de la workstation.
            data (WorkstationUpdate): Datos a actualizar.

        Returns:
            Workstation: Workstation actualizada.
        """
        pass

    @abstractmethod
    def eliminar_workstation(self, workstation_id: int) -> None:
        """
        Elimina una workstation del laboratorio.

        Args:
            workstation_id (int): Identificador de la workstation.

        Returns:
            None
        """
        pass


class AbstractEquipoService(ABC):
    @abstractmethod
    def registrar_equipo(self, data: EquipoCreate) -> Equipo:
        """
        Registra un componente físico (CPU, monitor, estabilizador, teclado o mouse) en el inventario.

        Args:
            data (EquipoCreate): Datos patrimoniales y técnicos del equipo.

        Returns:
            Equipo: Equipo físico registrado.
        """
        pass

    @abstractmethod
    def listar_equipos(self) -> List[Equipo]:
        """
        Lista todo el equipamiento físico registrado en el sistema.

        Returns:
            List[Equipo]: Lista de equipos físicos.
        """
        pass

    @abstractmethod
    def listar_por_laboratorio(
        self, lab_id: int, tipo: Optional[TipoEquipo] = None
    ) -> List[Equipo]:
        """
        Lista el inventario físico de un laboratorio, con filtro opcional por tipo de equipo.

        Args:
            lab_id (int): Identificador del laboratorio.
            tipo (Optional[TipoEquipo]): Tipo de equipo a filtrar.

        Returns:
            List[Equipo]: Lista de equipos encontrados.
        """
        pass

    @abstractmethod
    def listar_por_workstation(self, workstation_id: int) -> List[Equipo]:
        """
        Lista todos los equipos físicos asignados a una workstation específica.

        Args:
            workstation_id (int): Identificador de la workstation.

        Returns:
            List[Equipo]: Equipos asignados a la workstation.
        """
        pass

    @abstractmethod
    def obtener_equipo(self, equipo_id: int) -> Equipo:
        """
        Obtiene un equipo físico por su ID.

        Args:
            equipo_id (int): Identificador del equipo.

        Returns:
            Equipo: Equipo encontrado.
        """
        pass

    @abstractmethod
    def actualizar_equipo(self, equipo_id: int, data: EquipoUpdate) -> Equipo:
        """
        Actualiza el estado, ubicación o características de un equipo físico.

        Args:
            equipo_id (int): Identificador del equipo.
            data (EquipoUpdate): Campos a modificar.

        Returns:
            Equipo: Equipo actualizado.
        """
        pass

    @abstractmethod
    def eliminar_equipo(self, equipo_id: int) -> None:
        """
        Elimina un equipo físico del inventario.

        Args:
            equipo_id (int): Identificador del equipo.

        Returns:
            None
        """
        pass


class AbstractHorarioService(ABC):
    @abstractmethod
    def crear_horario(self, data: HorarioCreate) -> Horario:
        """
        Crea un nuevo turno u horario en un laboratorio validando disponibilidad y ausencia de cruces.

        Args:
            data (HorarioCreate): Datos del turno a programar.

        Returns:
            Horario: Horario creado.
        """
        pass

    @abstractmethod
    def listar_horarios(
        self, laboratorio_id: Optional[int] = None, fecha: Optional[date] = None
    ) -> List[Horario]:
        """
        Lista los horarios registrados, con filtros opcionales por laboratorio y fecha.

        Args:
            laboratorio_id (Optional[int]): Identificador del laboratorio.
            fecha (Optional[date]): Fecha específica a consultar.

        Returns:
            List[Horario]: Lista de horarios encontrados.
        """
        pass

    @abstractmethod
    def obtener_horario(self, horario_id: int) -> Horario:
        """
        Obtiene un horario por su identificador único.

        Args:
            horario_id (int): Identificador del horario.

        Returns:
            Horario: Horario encontrado.
        """
        pass

    @abstractmethod
    def iniciar_turno(self, horario_id: int) -> Horario:
        """
        Cambia el estado de un horario programado a en_curso.

        Args:
            horario_id (int): Identificador del horario.

        Returns:
            Horario: Horario actualizado.
        """
        pass

    @abstractmethod
    def finalizar_turno(self, horario_id: int) -> Horario:
        """
        Cambia el estado de un horario activo a finalizado.

        Args:
            horario_id (int): Identificador del horario.

        Returns:
            Horario: Horario actualizado.
        """
        pass

    @abstractmethod
    def cancelar_turno(self, horario_id: int) -> Horario:
        """
        Cancela un horario que se encontraba programado.

        Args:
            horario_id (int): Identificador del horario.

        Returns:
            Horario: Horario cancelado.
        """
        pass

    @abstractmethod
    def asignar_workstation(
        self, horario_id: int, data: AsignacionCreate
    ) -> AsignacionWorkstation:
        """
        Asigna a un alumno como responsable de una workstation durante un turno específico.

        Args:
            horario_id (int): Identificador del horario/turno.
            data (AsignacionCreate): Datos con workstation_id, codigo_alumno y observaciones.

        Returns:
            AsignacionWorkstation: Registro de asignación creado.
        """
        pass

    @abstractmethod
    def listar_asignaciones_turno(
        self, horario_id: int
    ) -> List[AsignacionWorkstation]:
        """
        Lista todas las asignaciones de responsabilidad registradas en un turno.

        Args:
            horario_id (int): Identificador del horario.

        Returns:
            List[AsignacionWorkstation]: Lista de asignaciones del turno.
        """
        pass

    @abstractmethod
    def consultar_historial_alumno(
        self, codigo_alumno: str
    ) -> List[AsignacionWorkstation]:
        """
        Obtiene el historial de puestos asignados a un alumno mediante su código.

        Args:
            codigo_alumno (str): Código identificador del alumno.

        Returns:
            List[AsignacionWorkstation]: Historial de asignaciones del alumno.
        """
        pass


class AbstractIncidenteService(ABC):
    @abstractmethod
    def reportar_incidente(self, data: IncidenteCreate) -> Incidente:
        """
        Registra un incidente vinculado a una workstation o equipo, actualizando su estado a con_falla.

        Args:
            data (IncidenteCreate): Datos del reporte de falla.

        Returns:
            Incidente: Incidente registrado.
        """
        pass

    @abstractmethod
    def listar_incidentes(self, solo_pendientes: bool = False) -> List[Incidente]:
        """
        Lista los incidentes del sistema, con opción de filtrar solo los no resueltos.

        Args:
            solo_pendientes (bool): Si es True, retorna solo pendientes o en proceso.

        Returns:
            List[Incidente]: Lista de incidentes.
        """
        pass

    @abstractmethod
    def listar_por_equipo(self, equipo_id: int) -> List[Incidente]:
        """
        Lista los incidentes reportados sobre un equipo físico.

        Args:
            equipo_id (int): Identificador del equipo.

        Returns:
            List[Incidente]: Lista de incidentes del equipo.
        """
        pass

    @abstractmethod
    def listar_por_workstation(self, workstation_id: int) -> List[Incidente]:
        """
        Lista los incidentes reportados sobre una workstation.

        Args:
            workstation_id (int): Identificador de la workstation.

        Returns:
            List[Incidente]: Lista de incidentes de la workstation.
        """
        pass

    @abstractmethod
    def actualizar_estado(
        self, incidente_id: int, data: IncidenteUpdateEstado
    ) -> Incidente:
        """
        Actualiza el estado de un incidente y sincroniza el estado operativo del equipo/workstation.

        Args:
            incidente_id (int): Identificador del incidente.
            data (IncidenteUpdateEstado): Nuevo estado del incidente.

        Returns:
            Incidente: Incidente actualizado.
        """
        pass