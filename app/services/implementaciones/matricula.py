import re
from datetime import date, datetime, timezone
from typing import Any, BinaryIO, Dict, List, Optional, Set, Tuple

from openpyxl import load_workbook
from pydantic import ValidationError
from sqlmodel import Session

from app.core.exceptions import (
    BusinessRuleException,
    DatabaseException,
    FileValidationException,
    NotFoundException,
)
from app.core.pagination import mapear_pagina, Pagina, ParametrosPaginacion
from app.dtos import (
    AlumnoDTO,
    ColumnaPlantillaDTO,
    ErrorFilaExcelDTO,
    FilaMatriculaDTO,
    MatriculaDTO,
    ResultadoCargaMatriculaDTO,
)
from app.models import (
    Alumno,
    EstadoAlumno,
    EstadoHorario,
    EstadoMatricula,
    Horario,
    Matricula,
    TipoDocumento,
)
from app.repositories.interfaces import (
    AbstractAlumnoRepository,
    AbstractHorarioRepository,
    AbstractMatriculaRepository,
)
from app.services.interfaces import AbstractMatriculaService

COLUMNAS_REQUERIDAS: Dict[str, str] = {
    "codigo": "Código institucional del alumno (ej. 2023123456).",
    "nombres": "Nombres del alumno.",
    "apellidos": "Apellidos del alumno.",
    "correo_institucional": "Correo institucional (ej. alumno@universidad.edu.pe).",
    "carrera": "Programa académico (ej. Ingeniería de Sistemas).",
}

COLUMNAS_OPCIONALES: Dict[str, str] = {
    "tipo_documento": "dni, carnet_extranjero, pasaporte o carnet_universitario.",
    "numero_documento": "Número de documento de identidad.",
    "correo_personal": "Correo personal de contacto.",
    "telefono": "Teléfono de contacto.",
    "fecha_nacimiento": "Fecha en formato AAAA-MM-DD o DD/MM/AAAA.",
    "semestre": "Semestre actual (número entero).",
    "grupo": "Grupo o sección (ej. A, B, T1).",
    "estado": "Estado del alumno; por defecto activo.",
    "observaciones": "Notas adicionales sobre el alumno o la matrícula.",
}

ALIASES_ENCABEZADOS: Dict[str, str] = {
    "codigo_alumno": "codigo",
    "codigo_estudiante": "codigo",
    "cod_matricula": "codigo",
    "nombre": "nombres",
    "nombres_alumno": "nombres",
    "apellido": "apellidos",
    "apellidos_alumno": "apellidos",
    "correo": "correo_institucional",
    "email": "correo_institucional",
    "correo_electronico": "correo_institucional",
    "email_institucional": "correo_institucional",
    "programa": "carrera",
    "carrera_profesional": "carrera",
    "tipo_doc": "tipo_documento",
    "documento": "numero_documento",
    "dni": "numero_documento",
    "celular": "telefono",
    "fecha_nac": "fecha_nacimiento",
    "f_nacimiento": "fecha_nacimiento",
    "obs": "observaciones",
}

TIPOS_DOCUMENTO: Dict[str, TipoDocumento] = {
    "dni": TipoDocumento.DNI,
    "ce": TipoDocumento.CARNET_EXTRANJERO,
    "ci": TipoDocumento.CARNET_EXTRANJERO,
    "carnet_extranjero": TipoDocumento.CARNET_EXTRANJERO,
    "pasaporte": TipoDocumento.PASAPORTE,
    "carnet_universitario": TipoDocumento.CARNET_UNIVERSITARIO,
    "ciu": TipoDocumento.CARNET_UNIVERSITARIO,
}

ESTADOS_ALUMNO: Dict[str, EstadoAlumno] = {e.value: e for e in EstadoAlumno}
PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PATRON_CODIGO = re.compile(r"^[A-Z0-9\-_]+$")
FORMATOS_FECHA = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y")


class MatriculaService(AbstractMatriculaService):
    """Servicio de matrícula masiva. Toda la validación de negocio reside aquí."""

    def __init__(
        self,
        session: Session,
        horario_repo: AbstractHorarioRepository,
        alumno_repo: AbstractAlumnoRepository,
        matricula_repo: AbstractMatriculaRepository,
    ):
        self.session = session
        self.horario_repo = horario_repo
        self.alumno_repo = alumno_repo
        self.matricula_repo = matricula_repo

    # ------------------------------------------------------------------
    # API pública (siempre DTOs de entrada y salida)
    # ------------------------------------------------------------------

    def cargar_matriculas_desde_excel(
        self,
        horario_id: int,
        archivo: BinaryIO,
        nombre_archivo: str,
        permitir_parciales: bool = False,
    ) -> ResultadoCargaMatriculaDTO:
        horario = self._validar_horario(horario_id)
        filas = self._leer_excel(archivo, nombre_archivo)
        if not filas:
            raise FileValidationException("El archivo Excel no contiene filas de alumnos para matricular.")

        registros, errores = self._validar_filas(filas)
        total_filas = len(filas)
        filas_con_errores = {error.fila for error in errores}
        candidatos = [r for r in registros if r.fila not in filas_con_errores]

        alumnos_existentes = self.alumno_repo.get_by_codigos(
            {r.codigo for r in candidatos}
        )
        ya_matriculados = self.matricula_repo.get_codigos_matriculados(
            horario_id, {r.codigo for r in candidatos}
        )
        correos_en_bd = self.alumno_repo.get_by_correos(
            {r.correo_institucional for r in candidatos}
        )

        for registro in candidatos:
            alumno_existente = alumnos_existentes.get(registro.codigo)
            if registro.codigo in ya_matriculados:
                errores.append(
                    ErrorFilaExcelDTO(
                        fila=registro.fila,
                        codigo=registro.codigo,
                        campo="codigo",
                        mensaje=(
                            f"El alumno '{registro.codigo}' ya está matriculado "
                            "en este horario."
                        ),
                    )
                )
            if registro.correo_institucional in correos_en_bd and (
                alumno_existente is None
                or alumno_existente.correo_institucional
                != registro.correo_institucional
            ):
                errores.append(
                    ErrorFilaExcelDTO(
                        fila=registro.fila,
                        codigo=registro.codigo,
                        campo="correo_institucional",
                        mensaje=(
                            f"El correo '{registro.correo_institucional}' ya pertenece "
                            "a otro alumno registrado."
                        ),
                    )
                )

        filas_con_errores = {error.fila for error in errores}
        filas_con_error = len(filas_con_errores)
        validos = [r for r in candidatos if r.fila not in filas_con_errores]
        modo = "parcial" if permitir_parciales else "atomico"

        if errores and not permitir_parciales:
            self.session.rollback()
            return ResultadoCargaMatriculaDTO(
                horario_id=horario_id,
                total_filas_leidas=total_filas,
                filas_validas=len(validos),
                alumnos_creados=0,
                alumnos_reutilizados=0,
                registros_insertados=0,
                filas_con_error=filas_con_error,
                errores=errores,
                modo=modo,
                mensaje=(
                    "Carga cancelada: se detectaron errores en "
                    f"{filas_con_error} fila(s). No se guardó ningún registro; "
                    "corrija el archivo y vuelva a intentarlo."
                ),
            )

        return self._persistir(
            horario=horario,
            registros=validos,
            alumnos_existentes=alumnos_existentes,
            total_filas=total_filas,
            errores=errores,
            filas_con_error=filas_con_error,
            modo=modo,
        )

    def listar_matriculas_por_horario(
        self, paginacion: ParametrosPaginacion, horario_id: int
    ) -> Pagina[MatriculaDTO]:
        self._validar_horario(horario_id, exigir_activo=False)
        pagina = self.matricula_repo.listar(paginacion, horario_id=horario_id)
        return mapear_pagina(pagina, self._a_dto)

    def eliminar_matricula(self, matricula_id: int) -> None:
        entidad = self.matricula_repo.get_by_id(matricula_id)
        if not entidad:
            raise NotFoundException(f"Matrícula {matricula_id} no encontrada.")
        self.matricula_repo.delete(entidad)

    def columnas_plantilla(self) -> List[ColumnaPlantillaDTO]:
        columnas = [
            ColumnaPlantillaDTO(nombre=n, requerida=True, descripcion=d)
            for n, d in COLUMNAS_REQUERIDAS.items()
        ]
        columnas += [
            ColumnaPlantillaDTO(nombre=n, requerida=False, descripcion=d)
            for n, d in COLUMNAS_OPCIONALES.items()
        ]
        return columnas

    # ------------------------------------------------------------------
    # Validaciones y lectura del Excel
    # ------------------------------------------------------------------

    def _validar_horario(
        self, horario_id: int, exigir_activo: bool = True
    ) -> Horario:
        horario = self.horario_repo.get_by_id(horario_id)
        if not horario:
            raise NotFoundException(f"Horario {horario_id} no encontrado.")
        if exigir_activo and horario.estado not in (
            EstadoHorario.PROGRAMADO,
            EstadoHorario.EN_CURSO,
        ):
            raise BusinessRuleException("El horario no está activo "
                    f"(estado: {horario.estado.value}). Solo se pueden matricular "
                    "alumnos en turnos programados o en curso.")
        return horario

    def _leer_excel(
        self, archivo: BinaryIO, nombre_archivo: str
    ) -> List[Tuple[int, Dict[str, Any]]]:
        if not nombre_archivo or not nombre_archivo.lower().endswith(".xlsx"):
            raise FileValidationException("El archivo debe tener extensión .xlsx.")
        try:
            libro = load_workbook(archivo, read_only=True, data_only=True)
        except Exception:
            raise FileValidationException("No se pudo abrir el archivo. Verifique que sea un .xlsx válido.")

        try:
            if not libro.sheetnames:
                raise FileValidationException("El archivo Excel no contiene hojas.")
            hoja = libro[libro.sheetnames[0]]
            filas_iter = hoja.iter_rows(values_only=True)
            try:
                cabeceras = next(filas_iter)
            except StopIteration:
                raise FileValidationException("El archivo Excel está vacío.")

            indice_columnas: Dict[str, int] = {}
            for indice, valor in enumerate(cabeceras):
                nombre = self._normalizar_encabezado(valor)
                if not nombre:
                    continue
                if nombre in indice_columnas:
                    raise FileValidationException(f"La columna '{nombre}' aparece más de una vez.")
                indice_columnas[nombre] = indice

            faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in indice_columnas]
            if faltantes:
                raise FileValidationException("Faltan columnas requeridas: "
                        f"{', '.join(faltantes)}. "
                        "Consulte la plantilla con GET /matriculas/plantilla.")

            filas: List[Tuple[int, Dict[str, Any]]] = []
            for numero, valores in enumerate(filas_iter, start=2):
                if all(v is None or str(v).strip() == "" for v in valores):
                    continue
                filas.append(
                    (
                        numero,
                        {
                            columna: valores[indice] if indice < len(valores) else None
                            for columna, indice in indice_columnas.items()
                        },
                    )
                )
            return filas
        finally:
            libro.close()

    def _validar_filas(
        self, filas: List[Tuple[int, Dict[str, Any]]]
    ) -> Tuple[List[FilaMatriculaDTO], List[ErrorFilaExcelDTO]]:
        registros: List[FilaMatriculaDTO] = []
        errores: List[ErrorFilaExcelDTO] = []
        codigos_vistos: Dict[str, int] = {}
        correos_vistos: Dict[str, int] = {}

        for numero, crudo in filas:
            registro, errores_fila = self._validar_celdas(numero, crudo)
            errores.extend(errores_fila)

            codigo = registro.codigo if registro else self._texto(crudo.get("codigo"))
            correo = (
                registro.correo_institucional
                if registro
                else self._texto(crudo.get("correo_institucional"))
            )
            if codigo:
                codigo = codigo.upper()
                if codigo in codigos_vistos:
                    errores.append(
                        ErrorFilaExcelDTO(
                            fila=numero,
                            codigo=codigo,
                            campo="codigo",
                            mensaje=(
                                "Código duplicado dentro del archivo "
                                f"(primera aparición en la fila {codigos_vistos[codigo]})."
                            ),
                        )
                    )
                else:
                    codigos_vistos[codigo] = numero

            if correo:
                correo = correo.lower()
                if correo in correos_vistos:
                    errores.append(
                        ErrorFilaExcelDTO(
                            fila=numero,
                            codigo=codigo,
                            campo="correo_institucional",
                            mensaje=(
                                "Correo duplicado dentro del archivo "
                                f"(primera aparición en la fila {correos_vistos[correo]})."
                            ),
                        )
                    )
                else:
                    correos_vistos[correo] = numero

            if registro:
                registros.append(registro)

        return registros, errores

    def _validar_celdas(
        self, numero: int, crudo: Dict[str, Any]
    ) -> Tuple[Optional[FilaMatriculaDTO], List[ErrorFilaExcelDTO]]:
        errores: List[ErrorFilaExcelDTO] = []

        def agregar(campo: str, mensaje: str, codigo: Optional[str] = None) -> None:
            errores.append(
                ErrorFilaExcelDTO(
                    fila=numero, codigo=codigo, campo=campo, mensaje=mensaje
                )
            )

        codigo = self._texto(crudo.get("codigo"))
        if codigo:
            codigo = codigo.upper()
            if len(codigo) > 30 or not PATRON_CODIGO.match(codigo):
                agregar(
                    "codigo",
                    "El código solo admite letras, números, guiones y guiones bajos (máx. 30).",
                    codigo,
                )
        else:
            agregar("codigo", "El código es obligatorio.")

        nombres = self._texto(crudo.get("nombres"))
        if not nombres:
            agregar("nombres", "Los nombres son obligatorios.", codigo)

        apellidos = self._texto(crudo.get("apellidos"))
        if not apellidos:
            agregar("apellidos", "Los apellidos son obligatorios.", codigo)

        correo = self._texto(crudo.get("correo_institucional"))
        if correo:
            correo = correo.lower()
            if not PATRON_CORREO.match(correo):
                agregar(
                    "correo_institucional", "El correo institucional no es válido.", codigo
                )
        else:
            agregar(
                "correo_institucional", "El correo institucional es obligatorio.", codigo
            )

        carrera = self._texto(crudo.get("carrera"))
        if not carrera:
            agregar("carrera", "La carrera o programa académico es obligatorio.", codigo)

        tipo_documento = TipoDocumento.DNI
        texto_tipo_documento = self._texto(crudo.get("tipo_documento"))
        if texto_tipo_documento:
            clave = self._normalizar_encabezado(texto_tipo_documento)
            tipo_documento = TIPOS_DOCUMENTO.get(clave)
            if tipo_documento is None:
                agregar("tipo_documento", "Tipo de documento no reconocido.", codigo)
                tipo_documento = TipoDocumento.DNI

        fecha_nacimiento = self._parsear_fecha(
            crudo.get("fecha_nacimiento"), numero, "fecha_nacimiento", codigo, errores
        )

        semestre: Optional[int] = None
        texto_semestre = self._texto(crudo.get("semestre"))
        if texto_semestre:
            try:
                semestre = int(float(texto_semestre))
                if not 1 <= semestre <= 20:
                    raise ValueError
            except (TypeError, ValueError):
                agregar("semestre", "El semestre debe ser un número entre 1 y 20.", codigo)
                semestre = None

        estado = EstadoAlumno.ACTIVO
        texto_estado = self._texto(crudo.get("estado"))
        if texto_estado:
            estado = ESTADOS_ALUMNO.get(texto_estado.strip().lower())
            if estado is None:
                agregar("estado", "Estado de alumno no reconocido.", codigo)
                estado = EstadoAlumno.ACTIVO

        observaciones = self._texto(crudo.get("observaciones"))
        if observaciones and len(observaciones) > 250:
            observaciones = observaciones[:250]

        if not codigo or errores:
            return None, errores

        datos = {
            "fila": numero,
            "codigo": codigo,
            "nombres": nombres,
            "apellidos": apellidos,
            "tipo_documento": tipo_documento,
            "numero_documento": self._texto(crudo.get("numero_documento")),
            "correo_institucional": correo,
            "correo_personal": self._texto(crudo.get("correo_personal")),
            "telefono": self._texto(crudo.get("telefono")),
            "fecha_nacimiento": fecha_nacimiento,
            "carrera": carrera,
            "semestre": semestre,
            "grupo": self._texto(crudo.get("grupo")),
            "estado": estado,
            "observaciones": observaciones,
        }

        # Validación estructural de la fila mediante su DTO.
        try:
            return FilaMatriculaDTO(**datos), errores
        except ValidationError as exc:
            for detalle in exc.errors():
                agregar(
                    str(detalle["loc"][0]) if detalle["loc"] else "fila",
                    detalle["msg"],
                    codigo,
                )
            return None, errores

    # ------------------------------------------------------------------
    # Persistencia transaccional
    # ------------------------------------------------------------------

    def _persistir(
        self,
        horario: Horario,
        registros: List[FilaMatriculaDTO],
        alumnos_existentes: Dict[str, Alumno],
        total_filas: int,
        errores: List[ErrorFilaExcelDTO],
        filas_con_error: int,
        modo: str,
    ) -> ResultadoCargaMatriculaDTO:
        alumnos_por_codigo: Dict[str, Alumno] = {}
        alumnos_nuevos: List[Alumno] = []
        alumnos_reutilizados = 0

        try:
            for registro in registros:
                alumno = alumnos_existentes.get(registro.codigo)
                if alumno is not None:
                    alumnos_reutilizados += 1
                    self._completar_alumno(alumno, registro)
                else:
                    datos_alumno = registro.model_dump(
                        exclude={"fila", "observaciones"}
                    )
                    alumno = Alumno(**datos_alumno)
                    alumnos_existentes[registro.codigo] = alumno
                    alumnos_nuevos.append(alumno)
                alumnos_por_codigo[registro.codigo] = alumno

            if alumnos_nuevos:
                self.session.add_all(alumnos_nuevos)
                self.session.flush()

            for registro in registros:
                self.session.add(
                    Matricula(
                        alumno_id=alumnos_por_codigo[registro.codigo].id,
                        horario_id=horario.id,
                        estado=EstadoMatricula.MATRICULADO,
                        observaciones=registro.observaciones,
                    )
                )

            self.session.commit()
        except Exception as exc:
            self.session.rollback()
            raise DatabaseException("Error crítico durante la carga masiva. Se deshicieron todos "
                    f"los cambios. Detalle: {exc}")

        cantidad = len(registros)
        mensaje = (
            f"Carga parcial completada: {cantidad} alumno(s) matriculado(s) en el "
            f"horario {horario.id} y {filas_con_error} fila(s) con error omitidas."
            if errores
            else f"Carga completada: {cantidad} alumno(s) matriculado(s) "
            f"en el horario {horario.id}."
        )

        return ResultadoCargaMatriculaDTO(
            horario_id=horario.id,
            total_filas_leidas=total_filas,
            filas_validas=cantidad,
            alumnos_creados=len(alumnos_nuevos),
            alumnos_reutilizados=alumnos_reutilizados,
            registros_insertados=cantidad,
            filas_con_error=filas_con_error,
            errores=errores,
            modo=modo,
            mensaje=mensaje,
        )

    def _completar_alumno(self, alumno: Alumno, registro: FilaMatriculaDTO) -> None:
        campos_a_completar = (
            "numero_documento",
            "correo_personal",
            "telefono",
            "fecha_nacimiento",
            "semestre",
            "grupo",
        )
        for campo in campos_a_completar:
            valor = getattr(registro, campo)
            if valor is not None and getattr(alumno, campo, None) is None:
                setattr(alumno, campo, valor)
        alumno.actualizado_en = datetime.now(timezone.utc)

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------

    @staticmethod
    def _a_dto(matricula: Matricula) -> MatriculaDTO:
        datos = MatriculaDTO.model_validate(matricula).model_dump()
        datos["alumno"] = (
            AlumnoDTO.model_validate(matricula.alumno) if matricula.alumno else None
        )
        return MatriculaDTO(**datos)

    @staticmethod
    def _normalizar_encabezado(valor: Any) -> str:
        texto = "" if valor is None else str(valor).strip().lower()
        normalizado = re.sub(r"[^a-z0-9]+", "_", texto).strip("_")
        return ALIASES_ENCABEZADOS.get(normalizado, normalizado)

    @staticmethod
    def _texto(valor: Any) -> Optional[str]:
        if valor is None:
            return None
        texto = str(valor).strip()
        return texto or None

    @staticmethod
    def _parsear_fecha(
        valor: Any,
        numero: int,
        campo: str,
        codigo: Optional[str],
        errores: List[ErrorFilaExcelDTO],
    ) -> Optional[date]:
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            return None
        if isinstance(valor, datetime):
            return valor.date()
        if isinstance(valor, date):
            return valor
        texto = str(valor).strip()
        for formato in FORMATOS_FECHA:
            try:
                return datetime.strptime(texto, formato).date()
            except ValueError:
                continue
        errores.append(
            ErrorFilaExcelDTO(
                fila=numero,
                codigo=codigo,
                campo=campo,
                mensaje="La fecha debe tener formato AAAA-MM-DD o DD/MM/AAAA.",
            )
        )
        return None
