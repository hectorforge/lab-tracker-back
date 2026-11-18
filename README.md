# Comandos paso a paso para ejecutar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

## Módulo de alumnos, tipos de equipo, matrículas y licencias

### Arquitectura

- `app/models`: **un archivo por modelo** (`alumno.py`, `equipo.py`, `licencia.py`, …). Los enums están agrupados en `app/models/enums.py` y las utilidades compartidas en `app/models/comun.py`. `app/models/__init__.py` reexporta todo. Cada entidad relevante expone `validar()`, ejecutada por el repositorio antes de insertar/actualizar.
- `app/core/pagination.py`: `ParametrosPaginacion`, `Pagina[T]` y la dependencia `get_paginacion`. El **repositorio** aplica `offset/limit` y calcula `total` y `total_paginas`.
- `app/core/api_response.py`: `ApiResponse[T]` con `isSuccess`, `status`, `message`, `details`, `errors`, `timestamp`, `traceId` y `path`. Cualquier tipo (DTO, página o lista) puede ir en `details`.
- `app/core/exceptions.py`: excepciones propias (`NotFoundException`, `ConflictException`, `FileValidationException`, `DatabaseException`, …). Los servicios lanzan estas, nunca `HTTPException`.
- `app/core/exception_handlers.py`: traduce cualquier excepción (de negocio, de validación, HTTP o no controlada) a `ApiResponse`.
- `app/dtos`: DTOs de Pydantic usados **exclusivamente por los servicios** (entrada y salida). Validan forma, rangos y formatos con `field_validator` / `model_validator`.
- `app/schemas`: contratos HTTP de la API. Los routers convierten el schema al DTO correspondiente (`CrearAlumnoDTO.model_validate(data)`, etc.).
- `app/repositories/interfaces` y `app/repositories/implementaciones`: un archivo por contrato y por implementación, respectivamente.
- `app/services/interfaces` y `app/services/implementaciones`: idem para la capa de servicio.

La lógica de negocio vive en el servicio; ni los routers ni los DTOs consultan la BD.

### Formato de respuesta y paginación

Todas las respuestas (éxito o error) usan el mismo sobre:

```json
{
  "isSuccess": true,
  "status": 200,
  "message": "Lista de alumnos obtenida correctamente.",
  "details": {
    "items": [],
    "total": 25,
    "pagina": 1,
    "tamano_pagina": 10,
    "total_paginas": 3
  },
  "errors": [],
  "timestamp": "2026-11-17T...Z",
  "traceId": "uuid",
  "path": "/alumnos/"
}
```

Los listados aceptan `?pagina=1&tamano_pagina=10` (máx. 100). En caso de error, `isSuccess=false`, `details` puede traer información adicional y `errors` incluye `codigo`, `mensaje` y `campo`. Por ejemplo, un horario inexistente devuelve 404 con `codigo: NOT_FOUND`; un archivo inválido, 400 con `codigo: FILE_VALIDATION_ERROR`; un dato inválido del body, 422 con el `campo` correspondiente.

### Endpoints nuevos

| Método | Ruta | Descripción |
| --- | --- | --- |
| POST / PUT / GET / DELETE | `/tipos-equipo` | CRUD del catálogo (categoría genérica, vida útil, costo referencial, licencia requerida, estado). |
| POST / PUT / GET / DELETE | `/licencias` | CRUD de licencias por equipo o por tipo de equipo. Filtros: `equipo_id`, `estado`. |
| POST / PUT / GET / DELETE | `/alumnos` | CRUD de alumnos. Filtros: `carrera`, `estado`, `busqueda`, `skip`, `limit`. |
| POST | `/matriculas/carga-excel` | Carga masiva de matriculados desde un `.xlsx` a un `horario_id`. |
| GET | `/matriculas/plantilla` | Devuelve las columnas requeridas y opcionales del Excel. |
| GET | `/matriculas/horario/{horario_id}` | Lista los alumnos matriculados en un turno. |
| DELETE | `/matriculas/{matricula_id}` | Da de baja una matrícula. |

El campo `tipo_equipo_id` de `/equipos` vincula el equipo físico con el catálogo; el servicio valida que esté activo y que su categoría coincida con la `categoria` del equipo.

### Categorías, costos y licencias

- La antigua enumeración de equipos specific (`cpu`, `monitor`, …) se reemplazó por `CategoriaTipoEquipo`, una lista **genérica de etiquetas**: `hardware`, `software`, `redes`, `periferico`, `almacenamiento`, `seguridad`, `mobiliario`, `otro`. El tipo concreto (CPU Docente, Monitor 24", etc.) se describe en `tipos_equipo.nombre`.
- `Equipo` registra `costo_estimado`, `costo_adquisicion`, `moneda`, `fecha_adquisicion`, `proveedor` y `garantia_hasta`. `TipoEquipo` registra `costo_referencial`, `moneda` y `requiere_licencia`.
- `Licencia` permite `tipo` (perpetua, suscripción, OEM, académica, prueba), `clave_producto`, `fabricante`, `cantidad_usuarios`, `fecha_vencimiento`, `costo`, `moneda`, `estado` y su vínculo con `equipo_id` y/o `tipo_equipo_id`. El servicio valida que el equipo y el tipo existan, que la categoría sea coherente y que una licencia vencida no quede activa.

### Carga masiva

`POST /matriculas/carga-excel` usa `multipart/form-data` con:

- `horario_id` (form): ID del turno destino. Debe existir y estar `programado` o `en_curso`.
- `archivo` (file): archivo `.xlsx`.
- `permitir_parciales` (form, opcional, por defecto `false`):
  - `false`: modo atómico; si cualquier fila tiene error, no se guarda nada y se devuelve el reporte de errores.
  - `true`: se insertan solo las filas válidas y se reportan las inválidas.

Columnas requeridas (la primera fila debe ser el encabezado): `codigo`, `nombres`, `apellidos`, `correo_institucional`, `carrera`.

Columnas opcionales: `tipo_documento`, `numero_documento`, `correo_personal`, `telefono`, `fecha_nacimiento`, `semestre`, `grupo`, `estado`, `observaciones`. Se aceptan alias frecuentes (`codigo_alumno`, `correo`, `email`, `programa`, etc.).

Ejemplo con curl:

```bash
curl -X POST "http://127.0.0.1:8000/matriculas/carga-excel" \
  -F "horario_id=1" \
  -F "permitir_parciales=false" \
  -F "archivo=@matriculados.xlsx"
```

La respuesta incluye `total_filas_leidas`, `registros_insertados`, `alumnos_creados`, `alumnos_reutilizados`, `filas_con_error` y un detalle de `errores` con `fila`, `campo` y `mensaje`.

Notas de negocio aplicadas en el servicio:

- Los alumnos existentes se reutilizan por `codigo`; se completan solo los datos que tenían vacíos.
- Se rechazan códigos o correos duplicados dentro del Excel y alumnos ya matriculados en el mismo horario.
- Los errores críticos (archivo inválido, columnas faltantes, horario no activo) devuelven 400/404 y no escriben en la BD; los errores de persistencia hacen rollback completo.

### Base de datos

Al iniciar la app se crean las tablas nuevas y, en SQLite, se agregan a una base ya existente las columnas `equipos.tipo_equipo_id`, `equipos.categoria` (y las de costo/licenciamiento) y `asignaciones_workstation.alumno_id` (no se requiere Alembic para este proyecto).