"""Genera Documentacion_SDKSupaBase.docx con código embebido del proyecto Android."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = PROJECT_ROOT / "Documentacion_SDKSupaBase.docx"

SRC = PROJECT_ROOT / "app" / "src" / "main"
JAVA = SRC / "java" / "com" / "uteq" / "software" / "app"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_dependencies_block(build_gradle: str) -> str:
    start = build_gradle.find("dependencies {")
    if start == -1:
        return build_gradle
    depth = 0
    for i in range(start, len(build_gradle)):
        ch = build_gradle[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return build_gradle[start : i + 1]
    return build_gradle[start:]


def add_title_page(doc: Document) -> None:
    for _ in range(6):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("SDK Supabase - Contenedores UI - UTEQ")
    run.bold = True
    run.font.size = Pt(24)
    run.font.name = "Calibri"
    run.font.color.rgb = RGBColor(0x1A, 0x47, 0x7A)

    doc.add_paragraph()
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub.add_run("Aplicaciones Móviles — 6° Semestre")
    r.font.size = Pt(14)
    r.font.name = "Calibri"

    sub2 = doc.add_paragraph()
    sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = sub2.add_run(f"Documentación técnica — {date.today().strftime('%d/%m/%Y')}")
    r2.font.size = Pt(12)
    r2.font.name = "Calibri"
    r2.italic = True

    doc.add_page_break()


def add_heading(doc: Document, text: str, level: int = 1) -> None:
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = "Calibri"
        run.font.color.rgb = RGBColor(0x1A, 0x47, 0x7A)


def add_para(doc: Document, text: str, bold: bool = False) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.bold = bold


def add_code_block(doc: Document, code: str, filename: str | None = None) -> None:
    if filename:
        cap = doc.add_paragraph()
        cap.paragraph_format.space_before = Pt(6)
        cap.paragraph_format.space_after = Pt(4)
        r = cap.add_run(f"Archivo: {filename}")
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    for line in code.splitlines():
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.6)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(line if line else " ")
        run.font.name = "Consolas"
        run.font.size = Pt(9)

    doc.add_paragraph()


def add_tree_block(doc: Document, tree: str) -> None:
    add_code_block(doc, tree)


def add_screenshot_placeholder(doc: Document, title: str, description: str) -> None:
    add_heading(doc, title, level=3)
    add_para(doc, description)
    box = doc.add_paragraph()
    box.paragraph_format.left_indent = Cm(1)
    box.paragraph_format.space_before = Pt(12)
    box.paragraph_format.space_after = Pt(24)
    run = box.add_run("[ Insertar captura de pantalla aquí ]")
    run.italic = True
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)


def build_file_tree() -> str:
    return """SDKSupaBase/
├── app/
│   ├── build.gradle.kts
│   └── src/main/
│       ├── AndroidManifest.xml
│       ├── java/com/uteq/software/app/
│       │   ├── Adapters/
│       │   │   └── AlumnoAdapter.kt
│       │   ├── Models/
│       │   │   ├── Alumno.kt
│       │   │   └── Materia.kt
│       │   ├── Services/
│       │   │   ├── SupaBaseManager.kt
│       │   │   └── SupabaseErrorHnadler.kt
│       │   └── Utils/
│       │       ├── MainActivity.kt
│       │       └── MainActivity2.kt
│       └── res/
│           ├── layout/
│           │   ├── activity_main.xml
│           │   ├── activity_main2.xml
│           │   └── item_alumno.xml
│           └── values/
│               └── strings.xml"""


def build_document() -> Document:
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    add_title_page(doc)

    # 1. Descripción del proyecto
    add_heading(doc, "1. Descripción del proyecto")
    add_para(
        doc,
        "Esta aplicación Android demuestra la integración del SDK de Supabase (PostgREST) "
        "con contenedores de interfaz de usuario nativos. El proyecto consulta tablas remotas "
        "de alumnos y materias alojadas en Supabase, presentando los datos en dos pantallas: "
        "una vista simple con EditText (MainActivity) y una vista avanzada con AutoCompleteTextView "
        "para filtrar por semestre/materia y ListView personalizado con imágenes (MainActivity2).",
    )
    add_para(doc, "Tecnologías principales:", bold=True)
    bullets = [
        "Kotlin + Android SDK (minSdk 26, targetSdk 36)",
        "Supabase Kotlin SDK (BOM 3.6.0) — módulo PostgREST",
        "Kotlinx Serialization para modelos de datos",
        "Material Design 3 — TextInputLayout con ExposedDropdownMenu",
        "Glide para carga de imágenes de perfil desde servidor UTEQ",
        "Coroutines (lifecycleScope) para operaciones asíncronas",
    ]
    for item in bullets:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(item)
        run.font.name = "Calibri"
        run.font.size = Pt(11)

    # 2. Estructura de archivos
    add_heading(doc, "2. Estructura de archivos")
    add_para(doc, "Árbol de directorios relevantes del módulo app:")
    add_tree_block(doc, build_file_tree())

    # 3. Configuración Gradle
    add_heading(doc, "3. Configuración Gradle (dependencies)")
    add_para(doc, "Bloque dependencies de app/build.gradle.kts:")
    gradle = read_text(PROJECT_ROOT / "app" / "build.gradle.kts")
    add_code_block(doc, extract_dependencies_block(gradle), "app/build.gradle.kts")

    # 4. AndroidManifest
    add_heading(doc, "4. AndroidManifest")
    add_para(doc, "Manifest principal con permisos, actividades y configuración Supabase:")
    add_code_block(doc, read_text(SRC / "AndroidManifest.xml"), "app/src/main/AndroidManifest.xml")

    # 5. Recursos strings/arrays
    add_heading(doc, "5. Recursos strings/arrays (values)")
    add_para(
        doc,
        "Archivo strings.xml con nombre de la aplicación y arreglo de niveles/semestres. "
        "Nota: no existe arrays.xml separado; el string-array niveles está definido en strings.xml.",
    )
    add_code_block(doc, read_text(SRC / "res" / "values" / "strings.xml"), "res/values/strings.xml")

    # 6. Layouts XML
    add_heading(doc, "6. Layouts XML")

    layouts = [
        ("6.1 activity_main.xml", SRC / "res" / "layout" / "activity_main.xml"),
        ("6.2 activity_main2.xml", SRC / "res" / "layout" / "activity_main2.xml"),
        ("6.3 item_alumno.xml", SRC / "res" / "layout" / "item_alumno.xml"),
    ]
    for title, path in layouts:
        add_heading(doc, title, level=2)
        add_code_block(doc, read_text(path), str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"))

    # 7. Código Kotlin
    add_heading(doc, "7. Código Kotlin")

    kotlin_files = [
        ("7.1 Models/Alumno.kt", JAVA / "Models" / "Alumno.kt"),
        ("7.2 Models/Materia.kt", JAVA / "Models" / "Materia.kt"),
        ("7.3 Services/SupaBaseManager.kt", JAVA / "Services" / "SupaBaseManager.kt"),
        ("7.4 Services/SupabaseErrorHnadler.kt", JAVA / "Services" / "SupabaseErrorHnadler.kt"),
        ("7.5 Adapters/AlumnoAdapter.kt", JAVA / "Adapters" / "AlumnoAdapter.kt"),
        ("7.6 Utils/MainActivity.kt", JAVA / "Utils" / "MainActivity.kt"),
        ("7.7 Utils/MainActivity2.kt", JAVA / "Utils" / "MainActivity2.kt"),
    ]
    for title, path in kotlin_files:
        add_heading(doc, title, level=2)
        rel = str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        add_code_block(doc, read_text(path), rel)

    # 8. Capturas
    add_heading(doc, "8. Capturas de pantalla")
    add_para(
        doc,
        "Secciones reservadas para insertar capturas de pantalla de la aplicación en ejecución.",
    )
    add_screenshot_placeholder(
        doc,
        "8.1 Pantalla principal (MainActivity2)",
        "Captura de la pantalla de inicio con logo UTEQ, selectores de semestre y materia, "
        "y lista de alumnos con fotos.",
    )
    add_screenshot_placeholder(
        doc,
        "8.2 Lista de alumnos con datos",
        "Captura mostrando al menos un alumno con nombre, correo, teléfono e imagen de perfil.",
    )
    add_screenshot_placeholder(
        doc,
        "8.3 Filtro por semestre",
        "Captura del dropdown de semestres (AutoCompleteTextView) desplegado.",
    )
    add_screenshot_placeholder(
        doc,
        "8.4 Vista alternativa (MainActivity)",
        "Captura opcional de la pantalla MainActivity con la lista de alumnos en EditText.",
    )
    add_screenshot_placeholder(
        doc,
        "8.5 Diálogo de error Supabase",
        "Captura opcional del MaterialAlertDialogBuilder en caso de error de conexión.",
    )

    # 9. Conclusión
    add_heading(doc, "9. Conclusión")
    add_para(
        doc,
        "El proyecto SDKSupaBase integra exitosamente el SDK de Supabase en una aplicación Android "
        "nativa, demostrando consultas PostgREST a tablas alumnos y materias con filtrado dinámico "
        "por nivel/semestre. Se utilizan contenedores UI avanzados (AutoCompleteTextView, ListView "
        "con adapter personalizado, ConstraintLayout) y buenas prácticas como manejo de errores "
        "centralizado, coroutines para operaciones de red y serialización Kotlin para los modelos de datos.",
    )
    add_para(
        doc,
        "La arquitectura separa responsabilidades en capas: Models (datos), Services (cliente Supabase "
        "y manejo de errores), Adapters (presentación en ListView) y Utils (Activities). "
        "Glide complementa la experiencia visual cargando fotografías de perfil desde el servidor SGA de la UTEQ.",
    )

    return doc


def main() -> None:
    doc = build_document()
    doc.save(str(OUTPUT_PATH))
    print(f"Documento generado: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
