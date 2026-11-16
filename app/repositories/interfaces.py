from abc import ABC, abstractmethod
from datetime import date, time
from typing import Optional, List
from app.models.lab_models import (
    Laboratorio,
    Workstation,
    Equipo,
    TipoEquipo,
    Horario,
    AsignacionWorkstation,
    Incidente,
)


class AbstractLaboratorioRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Laboratorio]:
        """
        Obtiene un laboratorio por su identificador único.

        Args:
            id (int): Identificador del laboratorio.

        Returns:
            Optional[Laboratorio]: Instancia del laboratorio si existe, o None en caso contrario.
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Laboratorio]:
        """
        Lista todos los laboratorios registrados con paginación.

        Args:
            skip (int): Cantidad de registros a omitir.
            limit (int): Cantidad máxima de registros a retornar.

        Returns:
            List[Laboratorio]: Lista de laboratorios encontrados.
        """
        pass

    @abstractmethod
    def create(self, obj: Laboratorio) -> Laboratorio:
        """
        Persiste un nuevo laboratorio en la base de datos.

        Args:
            obj (Laboratorio): Entidad laboratorio a registrar.

        Returns:
            Laboratorio: Laboratorio persistido con su ID generado.
        """
        pass

    @abstractmethod
    def update(self, obj: Laboratorio) -> Laboratorio:
        """
        Guarda los cambios realizados sobre un laboratorio existente.

        Args:
            obj (Laboratorio): Instancia modificada del laboratorio.

        Returns:
            Laboratorio: Laboratorio actualizado.
        """
        pass

    @abstractmethod
    def delete(self, obj: Laboratorio) -> None:
        """
        Elimina un laboratorio de la base de datos.

        Args:
            obj (Laboratorio): Instancia del laboratorio a eliminar.

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_by_codigo(self, codigo: str) -> Optional[Laboratorio]:
        """
        Busca un laboratorio por su código único institucional.

        Args:
            codigo (str): Código del laboratorio.

        Returns:
            Optional[Laboratorio]: Laboratorio encontrado o None.
        """
        pass

    @abstractmethod
    def get_disponibles(self) -> List[Laboratorio]:
        """
        Obtiene únicamente los laboratorios cuyo estado es disponible.

        Returns:
            List[Laboratorio]: Lista de laboratorios disponibles.
        """
        pass


class AbstractWorkstationRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Workstation]:
        """
        Obtiene una workstation por su identificador único.

        Args:
            id (int): Identificador de la workstation.

        Returns:
            Optional[Workstation]: Instancia encontrada o None.
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Workstation]:
        """
        Lista todas las workstations registradas con paginación.

        Args:
            skip (int): Registros a omitir.
            limit (int): Máximo de registros a retornar.

        Returns:
            List[Workstation]: Lista de workstations.
        """
        pass

    @abstractmethod
    def create(self, obj: Workstation) -> Workstation:
        """
        Registra una nueva workstation en la base de datos.

        Args:
            obj (Workstation): Entidad workstation a crear.

        Returns:
            Workstation: Workstation creada con ID asignado.
        """
        pass

    @abstractmethod
    def update(self, obj: Workstation) -> Workstation:
        """
        Actualiza una workstation existente en la base de datos.

        Args:
            obj (Workstation): Instancia modificada.

        Returns:
            Workstation: Workstation actualizada.
        """
        pass

    @abstractmethod
    def delete(self, obj: Workstation) -> None:
        """
        Elimina una workstation de la base de datos.

        Args:
            obj (Workstation): Instancia a eliminar.

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_by_laboratorio(self, laboratorio_id: int) -> List[Workstation]:
        """
        Lista todas las workstations pertenecientes a un laboratorio específico.

        Args:
            laboratorio_id (int): Identificador del laboratorio.

        Returns:
            List[Workstation]: Workstations del laboratorio.
        """
        pass

    @abstractmethod
    def get_by_codigo_y_laboratorio(
        self, codigo: str, laboratorio_id: int
    ) -> Optional[Workstation]:
        """
        Busca una workstation por su código dentro de un laboratorio específico.

        Args:
            codigo (str): Código interno de la workstation (ej. WS-01).
            laboratorio_id (int): Identificador del laboratorio.

        Returns:
            Optional[Workstation]: Workstation encontrada o None.
        """
        pass


class AbstractEquipoRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Equipo]:
        """
        Obtiene un equipo físico por su identificador único.

        Args:
            id (int): Identificador del equipo.

        Returns:
            Optional[Equipo]: Equipo encontrado o None.
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Equipo]:
        """
        Lista todo el inventario de equipos físicos con paginación.

        Args:
            skip (int): Registros a omitir.
            limit (int): Máximo de registros a retornar.

        Returns:
            List[Equipo]: Lista de equipos registrados.
        """
        pass

    @abstractmethod
    def create(self, obj: Equipo) -> Equipo:
        """
        Registra un nuevo equipo físico en el inventario.

        Args:
            obj (Equipo): Entidad equipo a persistir.

        Returns:
            Equipo: Equipo creado con su ID generado.
        """
        pass

    @abstractmethod
    def update(self, obj: Equipo) -> Equipo:
        """
        Actualiza los datos de un equipo físico existente.

        Args:
            obj (Equipo): Instancia modificada del equipo.

        Returns:
            Equipo: Equipo actualizado.
        """
        pass

    @abstractmethod
    def delete(self, obj: Equipo) -> None:
        """
        Elimina un equipo físico del inventario.

        Args:
            obj (Equipo): Instancia del equipo a eliminar.

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_by_codigo_patrimonial(self, codigo_patrimonial: str) -> Optional[Equipo]:
        """
        Busca un equipo por su código patrimonial único.

        Args:
            codigo_patrimonial (str): Código patrimonial o de inventario.

        Returns:
            Optional[Equipo]: Equipo encontrado o None.
        """
        pass

    @abstractmethod
    def get_by_laboratorio(
        self, laboratorio_id: int, tipo: Optional[TipoEquipo] = None
    ) -> List[Equipo]:
        """
        Lista los equipos inventariados en un laboratorio, opcionalmente filtrados por tipo.

        Args:
            laboratorio_id (int): Identificador del laboratorio.
            tipo (Optional[TipoEquipo]): Tipo de componente (CPU, monitor, etc.).

        Returns:
            List[Equipo]: Equipos del laboratorio que cumplen el filtro.
        """
        pass

    @abstractmethod
    def get_by_workstation(self, workstation_id: int) -> List[Equipo]:
        """
        Lista todos los equipos físicos asignados a una workstation específica.

        Args:
            workstation_id (int): Identificador de la workstation.

        Returns:
            List[Equipo]: Equipos instalados en dicha workstation.
        """
        pass


class AbstractHorarioRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Horario]:
        """
        Obtiene un horario/turno por su identificador único.

        Args:
            id (int): Identificador del horario.

        Returns:
            Optional[Horario]: Horario encontrado o None.
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Horario]:
        """
        Lista todos los horarios registrados con paginación.

        Args:
            skip (int): Registros a omitir.
            limit (int): Máximo de registros a retornar.

        Returns:
            List[Horario]: Lista de horarios.
        """
        pass

    @abstractmethod
    def create(self, obj: Horario) -> Horario:
        """
        Crea un nuevo horario o turno en un laboratorio.

        Args:
            obj (Horario): Entidad horario a registrar.

        Returns:
            Horario: Horario persistido.
        """
        pass

    @abstractmethod
    def update(self, obj: Horario) -> Horario:
        """
        Actualiza un horario existente en la base de datos.

        Args:
            obj (Horario): Instancia modificada del horario.

        Returns:
            Horario: Horario actualizado.
        """
        pass

    @abstractmethod
    def get_conflictos(
        self, laboratorio_id: int, fecha: date, hora_inicio: time, hora_fin: time
    ) -> List[Horario]:
        """
        Detecta horarios activos que se solapan con un rango horario en un laboratorio.

        Args:
            laboratorio_id (int): Identificador del laboratorio.
            fecha (date): Fecha del turno.
            hora_inicio (time): Hora de inicio del turno.
            hora_fin (time): Hora de finalización del turno.

        Returns:
            List[Horario]: Lista de horarios en conflicto.
        """
        pass

    @abstractmethod
    def get_by_laboratorio_y_fecha(
        self, laboratorio_id: int, fecha: Optional[date] = None
    ) -> List[Horario]:
        """
        Lista los horarios de un laboratorio, con filtro opcional por fecha.

        Args:
            laboratorio_id (int): Identificador del laboratorio.
            fecha (Optional[date]): Fecha específica a consultar.

        Returns:
            List[Horario]: Horarios ordenados cronológicamente.
        """
        pass

    @abstractmethod
    def create_asignacion(
        self, asignacion: AsignacionWorkstation
    ) -> AsignacionWorkstation:
        """
        Registra la asignación de responsabilidad de un alumno a una workstation en un turno.

        Args:
            asignacion (AsignacionWorkstation): Entidad de asignación a persistir.

        Returns:
            AsignacionWorkstation: Asignación creada.
        """
        pass

    @abstractmethod
    def get_asignacion_por_horario_y_workstation(
        self, horario_id: int, workstation_id: int
    ) -> Optional[AsignacionWorkstation]:
        """
        Verifica si una workstation ya tiene un alumno responsable en un horario dado.

        Args:
            horario_id (int): Identificador del horario.
            workstation_id (int): Identificador de la workstation.

        Returns:
            Optional[AsignacionWorkstation]: Asignación existente o None.
        """
        pass

    @abstractmethod
    def get_asignacion_por_horario_y_alumno(
        self, horario_id: int, codigo_alumno: str
    ) -> Optional[AsignacionWorkstation]:
        """
        Verifica si un alumno ya tiene asignada una workstation en el mismo horario.

        Args:
            horario_id (int): Identificador del horario.
            codigo_alumno (str): Código identificador del alumno.

        Returns:
            Optional[AsignacionWorkstation]: Asignación existente o None.
        """
        pass

    @abstractmethod
    def get_asignaciones_por_horario(
        self, horario_id: int
    ) -> List[AsignacionWorkstation]:
        """
        Obtiene todas las asignaciones de workstations registradas en un turno específico.

        Args:
            horario_id (int): Identificador del horario.

        Returns:
            List[AsignacionWorkstation]: Lista de asignaciones del turno.
        """
        pass

    @abstractmethod
    def get_historial_alumno(self, codigo_alumno: str) -> List[AsignacionWorkstation]:
        """
        Consulta el historial de asignaciones de workstations de un alumno por su código.

        Args:
            codigo_alumno (str): Código identificador del alumno.

        Returns:
            List[AsignacionWorkstation]: Lista de asignaciones ordenadas por fecha reciente.
        """
        pass


class AbstractIncidenteRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Incidente]:
        """
        Obtiene un incidente por su identificador único.

        Args:
            id (int): Identificador del incidente.

        Returns:
            Optional[Incidente]: Incidente encontrado o None.
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Incidente]:
        """
        Lista todos los incidentes registrados con paginación.

        Args:
            skip (int): Registros a omitir.
            limit (int): Máximo de registros a retornar.

        Returns:
            List[Incidente]: Lista de incidentes.
        """
        pass

    @abstractmethod
    def create(self, obj: Incidente) -> Incidente:
        """
        Registra un nuevo incidente de mantenimiento.

        Args:
            obj (Incidente): Entidad incidente a persistir.

        Returns:
            Incidente: Incidente creado.
        """
        pass

    @abstractmethod
    def update(self, obj: Incidente) -> Incidente:
        """
        Actualiza el estado o información de un incidente.

        Args:
            obj (Incidente): Instancia modificada del incidente.

        Returns:
            Incidente: Incidente actualizado.
        """
        pass

    @abstractmethod
    def get_pendientes(self) -> List[Incidente]:
        """
        Obtiene todos los incidentes que aún no han sido resueltos.

        Returns:
            List[Incidente]: Incidentes en estado pendiente o en proceso.
        """
        pass

    @abstractmethod
    def get_by_equipo(self, equipo_id: int) -> List[Incidente]:
        """
        Lista los incidentes asociados a un equipo físico específico.

        Args:
            equipo_id (int): Identificador del equipo.

        Returns:
            List[Incidente]: Historial de incidentes del equipo.
        """
        pass

    @abstractmethod
    def get_by_workstation(self, workstation_id: int) -> List[Incidente]:
        """
        Lista los incidentes asociados a una workstation específica.

        Args:
            workstation_id (int): Identificador de la workstation.

        Returns:
            List[Incidente]: Historial de incidentes de la workstation.
        """
        pass

    @abstractmethod
    def count_abiertos_por_equipo(self, equipo_id: int) -> int:
        """
        Cuenta cuántos incidentes sin resolver tiene actualmente un equipo físico.

        Args:
            equipo_id (int): Identificador del equipo.

        Returns:
            int: Cantidad de incidentes abiertos.
        """
        pass

    @abstractmethod
    def count_abiertos_por_workstation(self, workstation_id: int) -> int:
        """
        Cuenta cuántos incidentes sin resolver tiene actualmente una workstation.

        Args:
            workstation_id (int): Identificador de la workstation.

        Returns:
            int: Cantidad de incidentes abiertos.
        """
        pass