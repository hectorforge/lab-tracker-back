from typing import Any, Dict, List, Optional


class AppException(Exception):
    """Base de las excepciones de la aplicación.

    Los servicios lanzan estas excepciones en lugar de HTTPException para
    mantenerse desacoplados de FastAPI. Los handlers las traducen a ApiResponse.
    """

    status_code: int = 500
    code: str = "INTERNAL_ERROR"
    message: str = "Error interno del servidor."

    def __init__(
        self,
        message: Optional[str] = None,
        details: Any = None,
        errors: Optional[List[Dict[str, Any]]] = None,
    ):
        self.message = message or self.message
        self.details = details
        self.errors = errors or []
        super().__init__(self.message)


class BadRequestException(AppException):
    status_code = 400
    code = "BAD_REQUEST"
    message = "La solicitud contiene datos inválidos."


class ValidationException(AppException):
    status_code = 400
    code = "VALIDATION_ERROR"
    message = "No se cumplieron las validaciones de negocio."


class FileValidationException(AppException):
    status_code = 400
    code = "FILE_VALIDATION_ERROR"
    message = "El archivo proporcionado no cumple el formato requerido."


class UnauthorizedException(AppException):
    status_code = 401
    code = "UNAUTHORIZED"
    message = "Se requiere autenticación."


class ForbiddenException(AppException):
    status_code = 403
    code = "FORBIDDEN"
    message = "No tiene permisos para realizar esta acción."


class NotFoundException(AppException):
    status_code = 404
    code = "NOT_FOUND"
    message = "El recurso solicitado no existe."


class ConflictException(AppException):
    status_code = 409
    code = "CONFLICT"
    message = "El recurso entra en conflicto con el estado actual."


class BusinessRuleException(AppException):
    status_code = 422
    code = "BUSINESS_RULE_ERROR"
    message = "No se cumple una regla de negocio."


class DatabaseException(AppException):
    status_code = 500
    code = "DATABASE_ERROR"
    message = "Ocurrió un error al acceder a la base de datos."


class ExternalServiceException(AppException):
    status_code = 502
    code = "EXTERNAL_SERVICE_ERROR"
    message = "Un servicio externo no respondió correctamente."


class ServiceUnavailableException(AppException):
    status_code = 503
    code = "SERVICE_UNAVAILABLE"
    message = "El servicio no está disponible temporalmente."
