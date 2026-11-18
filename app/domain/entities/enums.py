import enum


class EstadoLaboratorio(str, enum.Enum):
    DISPONIBLE = "disponible"
    MANTENIMIENTO = "mantenimiento"
    CERRADO = "cerrado"


class EstadoWorkstation(str, enum.Enum):
    DISPONIBLE = "disponible"
    CON_FALLA = "con_falla"
    EN_MANTENIMIENTO = "en_mantenimiento"
    INHABILITADA = "inhabilitada"


class CategoriaTipoEquipo(str, enum.Enum):
    """Etiquetas generales: clasifican el catálogo, no enumeran equipos específicos."""

    HARDWARE = "hardware"
    SOFTWARE = "software"
    REDES = "redes"
    PERIFERICO = "periferico"
    ALMACENAMIENTO = "almacenamiento"
    SEGURIDAD = "seguridad"
    MOBILIARIO = "mobiliario"
    OTRO = "otro"


class EstadoEquipo(str, enum.Enum):
    OPERATIVO = "operativo"
    CON_FALLA = "con_falla"
    EN_MANTENIMIENTO = "en_mantenimiento"
    DE_BAJA = "de_baja"


class EstadoTipoEquipo(str, enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    DESCONTINUADO = "descontinuado"


class Moneda(str, enum.Enum):
    PEN = "pen"
    USD = "usd"
    EUR = "eur"


class TipoLicencia(str, enum.Enum):
    PERPETUA = "perpetua"
    SUSCRIPCION = "suscripcion"
    OEM = "oem"
    ACADEMICA = "academica"
    PRUEBA = "prueba"
    OTRO = "otro"


class EstadoLicencia(str, enum.Enum):
    ACTIVA = "activa"
    VENCIDA = "vencida"
    SUSPENDIDA = "suspendida"
    CANCELADA = "cancelada"


class TipoDocumento(str, enum.Enum):
    DNI = "dni"
    CARNET_EXTRANJERO = "carnet_extranjero"
    PASAPORTE = "pasaporte"
    CARNET_UNIVERSITARIO = "carnet_universitario"


class EstadoAlumno(str, enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"
    EGRESADO = "egresado"


class EstadoMatricula(str, enum.Enum):
    MATRICULADO = "matriculado"
    RETIRADO = "retirado"
    COMPLETADO = "completado"


class EstadoHorario(str, enum.Enum):
    PROGRAMADO = "programado"
    EN_CURSO = "en_curso"
    FINALIZADO = "finalizado"
    CANCELADO = "cancelado"


class PrioridadIncidente(str, enum.Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class EstadoIncidente(str, enum.Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    RESUELTO = "resuelto"
