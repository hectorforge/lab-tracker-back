# Comandos paso a paso para ejecutar
cp .env.example .env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

## Base de datos PostgreSQL y Docker

La API usa **PostgreSQL** por defecto con el driver `psycopg` 3:

```
DATABASE_URL=postgresql+psycopg://labtracker:labtracker@localhost:5432/labtracker
```

Levantar PostgreSQL y la API juntos:

```bash
cp .env.example .env      # ajusta credenciales si lo deseas
docker compose up --build
```

- `db`: `postgres:16-alpine`, con volumen persistente `pgdata` y healthcheck
  `pg_isready`. Expone el puerto `${POSTGRES_PORT:-5432}`.
- `api`: construida con el `Dockerfile` (multi-stage, usuario no root),
  espera a que `db` esté sano y se conecta usando el hostname `db`.
  Expone `http://localhost:8000` (`/docs`, `/openapi.json`).

Al iniciar, `create_all()` crea el esquema en PostgreSQL. Los cambios de
estructura posteriores se gestionan con Alembic; la migración ligera de
columnas solo se aplica cuando se usa SQLite para desarrollo.

Para ejecutar solo la base de datos y correr la API localmente:

```bash
docker compose up -d db
uvicorn main:app --reload
```

## Módulo de alumnos, tipos de equipo, matrículas y licencias

### Arquitectura

```
app/
├── domain/
│   ├── entities/       # alumno.py, equipo.py, laboratorio.py, licencia.py, ... + enums.py, comun.py
│   ├── repositories/   # alumno_repository.py, equipo_repository.py, ... (contratos)
│   └── exceptions/     # exceptions.py (NotFoundException, ConflictException, ...)
├── application/
│   ├── dtos/           # alumno_dto.py, equipo_dto.py, laboratorio_dto.py, licencia_dto.py, ...
│   ├── services/       # alumno_service_impl.py, ... y cargar_matriculas_use_case.py
│   └── interfaces/     # alumno_service.py, equipo_service.py, ... (contratos)
├── infrastructure/
│   ├── database/       # config.py, database.py (engine, sesión, create_all + migración)
│   └── repositories/   # alumno_repository_impl.py, equipo_repository_impl.py, ...
├── api/
│   ├── endpoints/      # alumno_endpoints.py, equipo_endpoints.py, ... (routers)
│   ├── http/           # alumno.http, equipo.http, ... (peticiones listas para probar)
│   ├── api_response.py
│   ├── exception_handlers.py
│   └── pagination.py
└── main.py
```

Solo cuatro carpetas de alto nivel: `domain`, `application`, `infrastructure` y `api`.

- **No existe `app/schemas` ni `app/models` ni `app/dtos` sueltos**: los DTOs viven en `application/dtos` y son el contrato HTTP y de servicio, con validación Pydantic (`field_validator` en modo `before` para normalizar códigos y `model_validator` para reglas compuestas).
- `domain/entities` agrupa **todas las tablas SQLModel**, los enums y las utilidades; cada entidad expone `validar()`, ejecutada por el repositorio antes de insertar/actualizar.
- Los contratos de repositorio y servicio usan sufijo simple (`alumno_repository`, `alumno_service`); sus implementaciones usan `_impl` (`alumno_repository_impl`, `alumno_service_impl`).
- `api/pagination.py`: `ParametrosPaginacion`, `Pagina[T]` y `get_paginacion`. El repositorio aplica `offset/limit` y calcula totales.
- `api/api_response.py`: `ApiResponse[T]` con `isSuccess`, `status`, `message`, `details`, `errors`, `timestamp`, `traceId` y `path`.
- `api/exception_handlers.py`: traduce cualquier excepción (de negocio, validación, HTTP o no controlada) a `ApiResponse`. Los servicios lanzan excepciones de `domain/exceptions`, nunca `HTTPException`.

La lógica de negocio vive en el servicio; los endpoints solo traducen HTTP ↔ DTO y devuelven `ApiResponse`.

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
| POST | `/auth/login` | Login con `username` + `password`; devuelve JWT. |
| GET | `/auth/me` | Datos del usuario autenticado. |
| POST / PUT / GET / DELETE | `/roles` | CRUD de roles (solo administrador). |
| POST / PUT / GET / DELETE | `/usuarios` | CRUD de usuarios internos con foto (solo administrador). |
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

### Seguridad, roles y permisos

El acceso es **solo interno** y se realiza exclusivamente con `username` + `password` mediante `POST /auth/login`. La respuesta trae el JWT en `details.access_token`; envíalo en el header `Authorization: Bearer <token>` en las demás peticiones. `GET /auth/me` devuelve el usuario autenticado.

Roles sembrados automáticamente al arrancar:

| Rol | Permisos |
| --- | --- |
| `administrador` | Acceso total: CRUD de laboratorios, workstations, equipos, tipos de equipo, licencias, alumnos, horarios, asignaciones, matrículas (incluida la carga Excel), incidencias, usuarios y roles. |
| `gestion_laboratorios` | **Solo consulta** de laboratorios, workstations, equipos, tipos de equipo, licencias, alumnos, horarios, asignaciones, matrículas e incidencias. Puede ver los alumnos asignados a cada laboratorio/equipo, pero no modificar nada. |
| `docente` | **Solo consulta** de horarios, matriculas, asignaciones, alumnos y equipos. Además puede **reportar incidentes** (`POST /incidentes/`). No puede gestionar usuarios, roles ni catálogos. |

Todos los endpoints van protegidos con una dependencia de rol (`requiere_admin`, `requiere_lectura`, `requiere_admin_o_docente`). Un rol no autorizado recibe `403` con `codigo: FORBIDDEN`; sin token o con token inválido/expirado, `401` con `codigo: UNAUTHORIZED`.

Variables de entorno de seguridad (ver `.env.example`):

```
JWT_SECRET_KEY=cambiar-este-secreto-en-produccion
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
RATE_LIMIT_PER_MINUTE=100
LOGIN_RATE_LIMIT_PER_MINUTE=5
```

**Rate limiting**: middleware en memoria con ventana deslizante de 60 s por IP. General: 100 req/min; `/auth/login`: 5 req/min para mitigar fuerza bruta. Al excederse responde `429` con `codigo: RATE_LIMIT_EXCEEDED`, header `Retry-After` y cabeceras `X-RateLimit-Limit`/`X-RateLimit-Remaining`. En despliegues multi-instancia se debe usar un backend compartido (Redis). También se añaden cabeceras de seguridad (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`).

Las contraseñas se almacenan con hash **bcrypt**; nunca se exponen en los DTOs.

### Imágenes y adjuntos

- `laboratorios.url_imagen` y `equipos.url_imagen`: enlace HTTP/HTTPS a la foto del laboratorio o equipo (máx. 500 caracteres). Se valida en el DTO y se devuelve en las respuestas.
- `incidentes.url_imagenes`: arreglo de enlaces a fotos del fallo y de la reparación. Se acepta al reportar el incidente y al actualizar su estado (se acumulan sin repetir).

### Pruebas con archivos `.http`

En `app/api/http/` hay un archivo por controlador (`alumno.http`, `equipo.http`, `laboratorio.http`, `licencia.http`, `matricula.http`, `tipo_equipo.http`, `horario.http`, `incidente.http`, `workstation.http`). Ábrelos con la extensión REST Client de VS Code o JetBrains; cada uno define `@baseUrl`, IDs de ejemplo y una petición por endpoint con datos válidos. El de matrículas incluye el multipart para subir `matriculados.xlsx` y el comando para generarlo.

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