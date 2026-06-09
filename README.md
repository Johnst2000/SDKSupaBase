# SDK Supabase - Contenedores UI (UTEQ)

Aplicación móvil Android desarrollada como tarea académica de la asignatura **Aplicaciones Móviles**. El proyecto integra el SDK de **Supabase** (PostgREST) para consultar datos de alumnos y materias almacenados en la nube, presentándolos mediante contenedores de interfaz de usuario (spinners, listas personalizadas y vistas de texto).

La implementación sigue como referencia el diseño y la lógica del proyecto docente **ContenedoresUI_Supabase**, adaptado al paquete `com.uteq.software.app` con filtros por semestre y materias.

---

## Stack tecnológico

| Tecnología | Versión / Uso |
|---|---|
| **Kotlin** | Lenguaje principal |
| **Layouts XML** | `activity_main2.xml`, `activity_main.xml`, `item_alumno.xml` |
| **Supabase SDK** | BOM `3.6.0` — módulo `postgrest-kt` |
| **Ktor Client** | `3.5.0` — cliente HTTP para Android |
| **Kotlinx Serialization** | `1.8.1` — deserialización de modelos |
| **Glide** | `4.16.0` — carga de fotos de alumnos |
| **Material Design 3** | `1.14.0` — componentes UI (dropdowns, diálogos) |
| **Kotlin Coroutines** | `lifecycleScope` — operaciones asíncronas |
| **AndroidX** | AppCompat, Activity KTX, ConstraintLayout, Core KTX |

---

## Funcionalidades

- **MainActivity2 como launcher** — pantalla principal al iniciar la app (`AndroidManifest.xml`).
- **Filtro por Semestre y Materias** — `AutoCompleteTextView` con datos de `strings.xml` (niveles) y consulta dinámica a la tabla `materias` en Supabase.
- **Lista personalizada de alumnos** — `ListView` con `AlumnoAdapter` que muestra nombre, correo, teléfono y foto circular (Glide).
- **MainActivity (lista de alumnos en texto)** — actividad secundaria que consulta la tabla `alumnos` y muestra el resultado en un `EditText` de solo lectura.
- **Manejo de errores** — `SupabaseErrorHandler` muestra diálogos Material ante `RestException`; `MainActivity` captura errores y los muestra en pantalla.
- **Conexión PostgREST** — consultas `select` con filtros (`eq`) y ordenamiento (`order`) sobre tablas `alumnos` y `materias`.

---

## Estructura del proyecto

```
SDKSupaBase/
├── app/
│   ├── build.gradle.kts              # Configuración del módulo y dependencias
│   ├── proguard-rules.pro
│   └── src/main/
│       ├── AndroidManifest.xml       # Permisos, actividades y launcher
│       ├── java/com/uteq/software/app/
│       │   ├── Adapters/
│       │   │   └── AlumnoAdapter.kt          # Adapter ListView con Glide
│       │   ├── Models/
│       │   │   ├── Alumno.kt                 # Modelo serializable alumno
│       │   │   └── Materia.kt                # Modelo serializable materia
│       │   ├── Services/
│       │   │   ├── SupaBaseManager.kt        # Cliente Supabase (singleton)
│       │   │   └── SupabaseErrorHnadler.kt   # Diálogos de error
│       │   └── Utils/
│       │       ├── MainActivity2.kt          # Pantalla principal (launcher)
│       │       └── MainActivity.kt           # Lista de alumnos en texto
│       └── res/
│           ├── layout/
│           │   ├── activity_main2.xml        # UI principal con spinners y lista
│           │   ├── activity_main.xml         # UI lista de alumnos (texto)
│           │   └── item_alumno.xml           # Ítem de la lista con foto
│           ├── values/
│           │   ├── strings.xml               # Nombre app y array de semestres
│           │   ├── colors.xml
│           │   └── themes.xml
│           ├── drawable/                     # Iconos y recursos gráficos
│           └── xml/                          # Reglas de backup
├── gradle/
│   ├── libs.versions.toml            # Versiones centralizadas
│   └── wrapper/
├── build.gradle.kts                  # Build raíz
├── settings.gradle.kts
└── README.md
```

---

## Requisitos

| Requisito | Valor |
|---|---|
| **Android Studio** | Ladybug o superior (recomendado) |
| **JDK** | 11 |
| **Gradle** | 9.4.1 (wrapper incluido) |
| **AGP** | 9.2.1 |
| **minSdk** | 26 (Android 8.0) |
| **targetSdk** | 36 |
| **compileSdk** | 36 |
| **applicationId** | `com.uteq.software.app` |
| **Conexión a Internet** | Requerida (permiso `INTERNET` en el manifest) |
| **Cuenta Supabase** | Proyecto configurado con tablas `alumnos` y `materias` |

---

## Cómo ejecutar el proyecto

1. **Clonar o descargar** el repositorio en tu equipo.
2. **Abrir** la carpeta `SDKSupaBase` en Android Studio (*File → Open*).
3. Esperar a que **Gradle Sync** finalice correctamente.
4. Verificar que las credenciales de Supabase estén configuradas en `SupaBaseManager.kt` (ver sección siguiente).
5. Crear o seleccionar un **emulador** (API 26 o superior) o conectar un dispositivo físico con depuración USB habilitada.
6. Pulsar **Run ▶** (o `Shift + F10`) para compilar e instalar la app.
7. La app abrirá **MainActivity2** con los filtros de Semestre/Materias y la lista de alumnos.

---

## Archivos clave

| Archivo | Descripción |
|---|---|
| `AndroidManifest.xml` | Declara `MainActivity2` como LAUNCHER y `MainActivity` como secundaria |
| `MainActivity2.kt` | Lógica principal: carga alumnos/materias, spinners y ListView |
| `MainActivity.kt` | Consulta todos los alumnos y los muestra en formato texto |
| `SupaBaseManager.kt` | Singleton `SupabaseManager` — URL y API key del proyecto |
| `SupabaseErrorHnadler.kt` | Muestra `MaterialAlertDialogBuilder` ante errores REST |
| `AlumnoAdapter.kt` | Adapter personalizado con Glide para fotos circulares |
| `Alumno.kt` / `Materia.kt` | Modelos `@Serializable` para PostgREST |
| `activity_main2.xml` | Layout principal: logo, dropdowns Semestre/Materias, ListView |
| `activity_main.xml` | Layout secundario: EditText + indicador de progreso |
| `item_alumno.xml` | Layout de cada ítem: ImageView + TextViews de datos |
| `strings.xml` | Array `niveles` (Primero … Séptimo) para el spinner de semestre |
| `app/build.gradle.kts` | Dependencias Supabase, Glide, Material y configuración SDK |

---

## Configuración de Supabase

Las credenciales del proyecto se configuran en:

```
app/src/main/java/com/uteq/software/app/Services/SupaBaseManager.kt
```

Dentro del objeto `SupabaseManager`, asignar:

- `supabaseUrl` — URL del proyecto en el panel de Supabase.
- `supabaseKey` — clave pública (`anon` key) del proyecto.

> **Importante:** No incluir claves reales en repositorios públicos. Usar variables de entorno, `local.properties` o un archivo ignorado por `.gitignore` en entregas de producción. Para la tarea académica, solicitar las credenciales al docente o configurarlas localmente antes de ejecutar.

El cliente instala únicamente el módulo **Postgrest** (sin autenticación). Las tablas esperadas son:

| Tabla | Campos principales |
|---|---|
| `alumnos` | `id`, `nombres`, `correo`, `telefono`, `paralelo`, `foto` |
| `materias` | `id`, `nombre`, `nivel` |

Las fotos se cargan desde `https://sga.uteq.edu.ec` + ruta almacenada en el campo `foto`.

---

## Captura de pantalla en ejecución

<img width="873" height="1256" alt="image" src="https://github.com/user-attachments/assets/3ae4cec0-5fb3-4d96-9334-48e1bbf6d957" />

---

## Paquete de la aplicación

```
com.uteq.software.app
```

---

## Autor

| Campo | Dato |
|---|---|
| **Estudiante** | Silva Triviño John Jairo |
| **Carrera** | Ingeniería en Software |
| **Universidad** | Universidad Técnica Estatal de Quevedo (UTEQ) |
| **Asignatura** | Aplicaciones Móviles |
| **Semestre** | 6.º semestre — 2026 |

