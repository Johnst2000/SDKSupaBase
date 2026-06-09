# SDK Supabase — Contenedores UI (UTEQ)

Aplicación Android desarrollada como tarea académica de **Aplicaciones Móviles** (6.º semestre). Consulta la tabla `alumnos` en **Supabase** mediante el SDK oficial (`postgrest-kt`), muestra los registros en un `ListView` personalizado con fotos circulares (Glide) y permite filtrar materias por semestre con `Spinner`.

**Paquete:** `com.uteq.software.app`  
**Actividad launcher:** `MainActivity2`

---

## Tabla de cumplimiento de la rúbrica

| Requisito | Implementación | Archivo(s) |
|---|---|---|
| Logo institucional (`ImageView`) | `@drawable/logo` en pantalla principal | `activity_main2.xml` |
| Dropdown semestre (`Spinner`) | `spinnerSemestre` + array `niveles` | `activity_main2.xml`, `strings.xml`, `MainActivity2.kt` |
| Dropdown materia (`Spinner`) | `spinnerMaterias` con datos de Supabase | `activity_main2.xml`, `MainActivity2.kt` |
| Lista alumnos (`ListView`) | `lvAlumnos` | `activity_main2.xml` |
| Ítem personalizado (foto, nombre, correo, teléfono, iconos) | `item_alumno.xml` + `AlumnoAdapter` | `item_alumno.xml`, `AlumnoAdapter.kt` |
| SDK Supabase oficial, consulta async | `SupabaseManager.client.from("alumnos").select { … }` en `lifecycleScope` | `SupaBaseManager.kt`, `MainActivity2.kt` |
| Orden alfabético por `nombres` | `order("nombres", Order.ASCENDING)` | `MainActivity2.kt`, `MainActivity.kt` |
| Modelo `Alumno` exacto | `id:Int`, `nombres`, `correo`, `telefono`, `foto` (String) | `Alumno.kt` |
| `AlumnoAdapter extends ArrayAdapter<Alumno>` | Sí, layout `item_alumno` | `AlumnoAdapter.kt` |
| Glide + `circleCrop()` | URL base SGA + ruta `foto` | `AlumnoAdapter.kt` |
| Credenciales fuera del código | `local.properties` → `BuildConfig` | `local.properties`, `app/build.gradle.kts`, `SupaBaseManager.kt` |
| Sin RecyclerView / Compose / Retrofit / Volley / Firebase | No presentes en dependencias ni código | `libs.versions.toml`, proyecto completo |
| Contenedores UI permitidos | `ConstraintLayout`, `LinearLayout`, `ImageView`, `TextView`, `Spinner`, `ListView` | layouts XML |

---

## Stack tecnológico

| Tecnología | Versión / Uso |
|---|---|
| **Kotlin** | Lenguaje principal |
| **Layouts XML** | Sin Jetpack Compose |
| **Supabase SDK** | BOM `3.6.0` — módulo `postgrest-kt` |
| **Ktor Client** | `3.5.0` — transporte HTTP (requerido por Supabase SDK) |
| **Kotlinx Serialization** | `1.8.1` — deserialización de modelos |
| **Glide** | `4.16.0` — imágenes con `circleCrop()` |
| **AndroidX** | AppCompat, Activity KTX, ConstraintLayout, Core KTX |
| **Coroutines** | `lifecycleScope.launch` — consultas asíncronas |

> **Nota:** La dependencia `material` se usa solo para diálogos de error (`MaterialAlertDialogBuilder`). La UI principal de la rúbrica usa únicamente contenedores permitidos.

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                      MainActivity2 (LAUNCHER)               │
│  Spinner Semestre → Spinner Materias → ListView Alumnos     │
└──────────────────────────┬──────────────────────────────────┘
                           │ lifecycleScope.launch
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              SupabaseManager (SupaBaseManager.kt)         │
│  BuildConfig.SUPABASE_URL / BuildConfig.SUPABASE_KEY        │
│  createSupabaseClient → Postgrest                           │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST (PostgREST)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Supabase Cloud                           │
│  Tabla `alumnos`  (id, nombres, correo, telefono, foto)     │
│  Tabla `materias` (id, nombre, nivel)                       │
└─────────────────────────────────────────────────────────────┘

ListView ← AlumnoAdapter ← ArrayList<Alumno>
              └── Glide → https://sga.uteq.edu.ec + foto
```

### Flujo de datos

1. Al abrir la app, `MainActivity2` consulta `alumnos` ordenados por `nombres ASC`.
2. El `Spinner` de semestre carga opciones desde `strings.xml` (`Primero` … `Séptimo`).
3. Al elegir semestre, se consulta `materias` filtradas por `nivel`.
4. El `Spinner` de materias se llena con los nombres devueltos.
5. El `ListView` muestra todos los alumnos mediante `AlumnoAdapter` (foto circular, nombre en mayúsculas, correo y teléfono con iconos).

---

## Estructura del proyecto

```
SDKSupaBase/
├── app/
│   ├── build.gradle.kts              # buildConfigField desde local.properties
│   └── src/main/
│       ├── AndroidManifest.xml       # MainActivity2 = LAUNCHER
│       ├── java/com/uteq/software/app/
│       │   ├── Adapters/AlumnoAdapter.kt
│       │   ├── Models/Alumno.kt, Materia.kt
│       │   ├── Services/
│       │   │   ├── SupaBaseManager.kt    # SupabaseManager singleton
│       │   │   └── SupabaseErrorHnadler.kt
│       │   └── Utils/MainActivity2.kt, MainActivity.kt
│       └── res/layout/
│           ├── activity_main2.xml    # UI principal (rúbrica)
│           ├── activity_main.xml     # Actividad secundaria (texto plano)
│           └── item_alumno.xml       # Ítem ListView
├── gradle/libs.versions.toml
├── local.properties.example          # Plantilla de credenciales (sin claves reales)
├── local.properties                  # NO subir a Git — sdk.dir + Supabase
├── generate_documentacion.py         # Genera Documentacion_SDKSupaBase.docx
└── README.md
```

---

## Requisitos previos

| Requisito | Valor |
|---|---|
| Android Studio | Ladybug o superior |
| JDK | 11 |
| Gradle (wrapper) | 9.4.1 |
| AGP | 9.2.1 |
| minSdk | 26 |
| targetSdk / compileSdk | 36 |
| Internet | Obligatorio (`INTERNET` en manifest) |
| Proyecto Supabase | Tablas `alumnos` y `materias` configuradas |

---

## Instalación paso a paso

### 1. Clonar o descargar

```bash
git clone <URL_DE_TU_REPOSITORIO>
cd SDKSupaBase
```

O descargar el ZIP desde GitHub y extraerlo.

### 2. Configurar `local.properties` (obligatorio)

Android Studio crea `local.properties` automáticamente con `sdk.dir`. Debes **añadir** las credenciales de Supabase:

```properties
sdk.dir=C\:\\Users\\TU_USUARIO\\AppData\\Local\\Android\\Sdk

SUPABASE_URL=https://TU_PROYECTO.supabase.co
SUPABASE_KEY=TU_CLAVE_SUPABASE
```

**Opción rápida:** copiar la plantilla:

```bash
copy local.properties.example local.properties
```

Luego editar `local.properties` con tus valores reales.

> **Seguridad:** `local.properties` está en `.gitignore`. **Nunca** subas claves al repositorio. Las credenciales se inyectan en compilación como `BuildConfig.SUPABASE_URL` y `BuildConfig.SUPABASE_KEY`.

### 3. Abrir en Android Studio

1. *File → Open* → seleccionar carpeta `SDKSupaBase`.
2. Esperar **Gradle Sync** (descarga dependencias Supabase, Glide, etc.).
3. Si sync falla por credenciales vacías, verificar que `SUPABASE_URL` y `SUPABASE_KEY` existen en `local.properties`.

### 4. Ejecutar

1. Crear emulador API 26+ o conectar dispositivo con depuración USB.
2. Run ▶ (o `Shift+F10`).
3. La app abre **MainActivity2** con logo, spinners y lista de alumnos.

### 5. Compilar APK debug (entrega)

```bash
.\gradlew assembleDebug
```

APK generado en: `app/build/outputs/apk/debug/app-debug.apk`

---

## Configuración Supabase

### Tablas esperadas

**`alumnos`**

| Columna | Tipo | Uso |
|---|---|---|
| `id` | int | Identificador |
| `nombres` | text | Nombre completo (orden alfabético) |
| `correo` | text | Correo electrónico |
| `telefono` | text | Teléfono |
| `foto` | text | Ruta relativa en SGA (ej. `/fotos/alumno.jpg`) |

**`materias`**

| Columna | Tipo | Uso |
|---|---|---|
| `id` | int | Identificador |
| `nombre` | text | Nombre de la materia |
| `nivel` | int | Semestre (1=Primero … 7=Séptimo) |

### Modelo Kotlin (rúbrica)

```kotlin
data class Alumno(
    val id: Int,
    val nombres: String,
    val correo: String,
    val telefono: String,
    val foto: String
)
```

### Cadena BuildConfig → SupabaseManager

En `app/build.gradle.kts`:

```kotlin
buildFeatures { buildConfig = true }

buildConfigField("String", "SUPABASE_URL", "\"${localProperties.getProperty("SUPABASE_URL", "")}\"")
buildConfigField("String", "SUPABASE_KEY", "\"${localProperties.getProperty("SUPABASE_KEY", "")}\"")
```

En `SupaBaseManager.kt`:

```kotlin
createSupabaseClient(
    supabaseUrl = BuildConfig.SUPABASE_URL,
    supabaseKey = BuildConfig.SUPABASE_KEY
) { install(Postgrest) }
```

---

## Publicar en GitHub

1. Crear repositorio vacío en GitHub.
2. Verificar que **no** se incluye `local.properties` (`git status` no debe listarlo).
3. Sí incluir `local.properties.example` para que el docente sepa qué variables configurar.
4. Subir el proyecto:

```bash
git add .
git commit -m "Entrega SDK Supabase - Contenedores UI"
git push -u origin master
```

5. En el README del repo (este archivo), el evaluador encontrará instalación, rúbrica y arquitectura.

---

## Capturas de pantalla (para PDF / informe)

Colocar imágenes en `docs/capturas/` con estos nombres:

| Archivo | Contenido sugerido |
|---|---|
| `captura_01_mainactivity2.png` | Pantalla principal: logo, spinners, ListView |
| `captura_02_lista_fotos.png` | Detalle de ítems con foto circular Glide |
| `captura_03_filtros.png` | Spinner semestre/materia desplegado |
| `captura_04_mainactivity.png` | MainActivity secundaria (lista texto) |
| `captura_05_documentacion.png` | Android Studio / Supabase dashboard |

Referencia en markdown (insertar tras tomar capturas):

```markdown
![MainActivity2](docs/capturas/captura_01_mainactivity2.png)
```

> El **PDF de entrega** lo genera el estudiante; el código y este README están listos para copiar al informe.

---

## Archivos clave

| Archivo | Rol |
|---|---|
| `MainActivity2.kt` | Launcher: spinners, consulta async, ListView |
| `AlumnoAdapter.kt` | `ArrayAdapter<Alumno>` + Glide `circleCrop()` |
| `Alumno.kt` | Data class según rúbrica |
| `SupaBaseManager.kt` | Cliente Supabase con `BuildConfig` |
| `activity_main2.xml` | Layout principal rúbrica |
| `item_alumno.xml` | Layout ítem: foto, nombre, correo, teléfono, iconos |
| `app/build.gradle.kts` | `buildConfigField` + dependencias |
| `local.properties.example` | Plantilla sin secretos |

---

## Documentación Word (opcional)

Informe técnico para entrega:

```bash
pip install python-docx
python generate_documentacion.py
```

Genera `Documentacion_SDKSupaBase.docx`. **Regenerar** tras cambios importantes (Spinner, BuildConfig) para que el Word refleje el código actual.

---

## Solución de problemas

| Problema | Solución |
|---|---|
| Lista vacía / error REST | Verificar `SUPABASE_URL` y `SUPABASE_KEY` en `local.properties`; re-sync Gradle |
| Fotos no cargan | Comprobar campo `foto` y conectividad a `https://sga.uteq.edu.ec` |
| Gradle sync falla | JDK 11, Android SDK 36 instalado |
| Emulador ADB | Ver `EMULATOR_ADB_FIX.md` |

---

## Autor

| Campo | Dato |
|---|---|
| **Estudiante** | [Nombre completo] |
| **Carrera** | Ingeniería en Software |
| **Universidad** | UTEQ |
| **Asignatura** | Aplicaciones Móviles |
| **Semestre** | 6.º — 2026 |

---

## Referencia docente

Basado en **ContenedoresUI_Supabase** — proyecto de referencia del docente para contenedores UI con Supabase en Android.

---

*Proyecto académico — UTEQ · Aplicaciones Móviles · 2026*
