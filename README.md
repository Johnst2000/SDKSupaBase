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
├── generate_documentacion.py         # Script para generar Documentacion_SDKSupaBase.docx
├── EMULATOR_ADB_FIX.md               # Notas de solución de problemas con emulador
└── README.md
```


## Capturas de pantalla en ejecución



