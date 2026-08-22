from dataclasses import dataclass
from pathlib import Path
import csv
import re
import unicodedata


# ============================================================
# RUTAS DEL PROYECTO
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

CSV_FILE = ROOT / "data" / "casos_ia.csv"
REPORTS_DIR = ROOT / "reports"
REPORT_FILE = REPORTS_DIR / "semana03.md"


# ============================================================
# ESTRUCTURA DE CATEGORÍAS
# ============================================================

@dataclass(frozen=True)
class Category:
    name: str
    keywords: tuple[str, ...]


CATEGORIES = [
    Category(
        "Aprendizaje automatico predictivo",
        (
            "predecir",
            "prediccion",
            "historicos",
            "historico",
            "falla",
            "demanda",
            "patrones",
            "clasificar",
            "clasificacion",
            "anormal",
            "anomalia",
            "anormalidad",
            "inusual",
            "inusuales",
            "desviacion",
            "desviaciones",
        ),
    ),

    Category(
        "Sistemas expertos",
        (
            "reglas",
            "alerta",
            "alerta critica",
            "situacion de riesgo",
            "determinar mediante reglas",
        ),
    ),

    Category(
        "Busqueda y optimizacion",
        (
            "optimizar",
            "optimizacion",
            "distribucion",
            "recursos",
            "sobrecarga",
            "capacidad",
            "primero",
        ),
    ),

    Category(
        "Sistemas de recomendacion",
        (
            "recomendar",
            "recomendacion",
            "recomendar acciones",
            "que servidor debe",
        ),
    ),
]


# ============================================================
# REGLAS PERSONALIZADAS
# ============================================================

CUSTOM_RULES = {
    "Aprendizaje automatico predictivo": (
        "comportamiento anormal",
        "patrones anormales",
        "patrones anomalos",
        "comportamientos inusuales",
        "incrementos inusuales",
        "desviaciones",
        "registros historicos",
        "predecir",
        "prediccion",
        "clasificar",
    ),

    "Sistemas expertos": (
        "aplicar reglas",
        "mediante reglas",
        "generar una alerta",
        "alerta critica",
        "situacion de riesgo",
    ),

    "Busqueda y optimizacion": (
        "optimizar la distribucion",
        "optimizar",
        "distribucion de recursos",
        "recursos adicionales",
        "capacidad disponible",
    ),

    "Sistemas de recomendacion": (
        "recomendar acciones",
        "recomendar que servidor",
    ),
}


# ============================================================
# TÉCNICAS RECOMENDADAS
# ============================================================

TECHNIQUES = {
    "Aprendizaje automatico predictivo":
        "Isolation Forest, Random Forest, regresion o arbol de decision.",

    "Sistemas expertos":
        "Motor de reglas basado en condiciones y umbrales.",

    "Busqueda y optimizacion":
        "Algoritmos de optimizacion para asignacion de recursos.",

    "Sistemas de recomendacion":
        "Sistema de recomendacion basado en reglas o puntuaciones.",
}


# ============================================================
# NORMALIZACIÓN DE TEXTO
# ============================================================

def normalize(text):
    """
    Normaliza un texto:
    - Convierte a minusculas.
    - Elimina tildes.
    - Reemplaza caracteres especiales.
    - Elimina espacios adicionales.
    """

    text = unicodedata.normalize(
        "NFD",
        text.strip().lower()
    )

    text = "".join(
        character
        for character in text
        if unicodedata.category(character) != "Mn"
    )

    text = re.sub(r"[^a-z0-9]+", " ", text)

    return re.sub(r"\s+", " ", text).strip()


def normalize_header(text):
    """Normaliza los encabezados del archivo CSV."""
    return normalize(text).replace(" ", "")


# ============================================================
# CONSTRUCCIÓN DE CATEGORÍAS
# ============================================================

def build_categories():
    """
    Combina las palabras clave generales con las reglas
    personalizadas de cada categoría.
    """

    return [
        Category(
            category.name,
            category.keywords + CUSTOM_RULES.get(
                category.name,
                ()
            ),
        )
        for category in CATEGORIES
    ]


# ============================================================
# CLASIFICACIÓN
# ============================================================

def classify_problem(description):
    """
    Clasifica una descripción según las palabras clave
    encontradas en cada categoría.

    Retorna:
        primary: categoría principal.
        detected: categorías detectadas.
        scores: puntuación de cada categoría.
    """

    text = normalize(description)

    scores = {
        category.name: sum(
            normalize(keyword) in text
            for keyword in category.keywords
        )
        for category in build_categories()
    }

    detected = [
        name
        for name, score in scores.items()
        if score > 0
    ]

    if detected:
        primary = max(
            detected,
            key=scores.get
        )
    else:
        primary = "Sin clasificar"

    return primary, detected, scores


# ============================================================
# LECTURA DEL CSV
# ============================================================

def read_cases():
    """
    Lee los casos desde data/casos_ia.csv.

    El CSV contiene una única columna:
        descripcion
    """

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {CSV_FILE}"
        )

    with CSV_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError(
                "El archivo CSV no tiene encabezados."
            )

        reader.fieldnames = [
            normalize_header(header)
            for header in reader.fieldnames
        ]

        if "descripcion" not in reader.fieldnames:
            raise ValueError(
                "El archivo CSV debe contener una columna "
                "llamada 'descripcion'."
            )

        cases = []

        for number, row in enumerate(reader, start=1):

            description = row["descripcion"].strip()

            if not description:
                continue

            cases.append(
                {
                    "id": number,
                    "descripcion": description,
                }
            )

    if len(cases) < 20:
        raise ValueError(
            f"Se requieren minimo 20 casos. "
            f"Se encontraron {len(cases)}."
        )

    return cases


# ============================================================
# GENERACIÓN DEL REPORTE MARKDOWN
# ============================================================

def generate_report(
    cases,
    results,
    category_count
):
    """
    Genera automáticamente:

        reports/semana03.md
    """

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    report = []

    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    report.append("# Semana 03 - Taxonomía y clasificación")
    report.append("")

    report.append(
        "## Proyecto: Detección de anomalías en servidores"
    )
    report.append("")

    report.append(
        "Este informe presenta la aplicación de una "
        "taxonomía de inteligencia artificial al problema "
        "de detección de anomalías operativas en servidores."
    )

    report.append("")

    # --------------------------------------------------------
    # OBJETIVO
    # --------------------------------------------------------

    report.append("## Objetivo")
    report.append("")

    report.append(
        "Identificar qué técnicas y categorías de "
        "inteligencia artificial pueden aplicarse a "
        "diferentes situaciones relacionadas con el "
        "monitoreo y operación de servidores."
    )

    report.append("")

    # --------------------------------------------------------
    # CASOS ANALIZADOS
    # --------------------------------------------------------

    report.append("## Casos analizados")
    report.append("")

    report.append(
        f"Se procesaron **{len(cases)} casos**."
    )

    report.append("")

    # --------------------------------------------------------
    # CLASIFICACIÓN
    # --------------------------------------------------------

    report.append("## Clasificación")
    report.append("")

    report.append(
        "| ID | Descripción | Categoría principal | "
        "Categorías detectadas | Técnica recomendada |"
    )

    report.append(
        "|---:|---|---|---|---|"
    )

    for result in results:

        description = (
            result["descripcion"]
            .replace("|", "\\|")
        )

        detected = (
            ", ".join(result["detected"])
            if result["detected"]
            else "Ninguna"
        )

        report.append(
            f"| {result['id']} | "
            f"{description} | "
            f"{result['automatic']} | "
            f"{detected} | "
            f"{result['technique']} |"
        )

    report.append("")

    # --------------------------------------------------------
    # DISTRIBUCIÓN POR CATEGORÍA
    # --------------------------------------------------------

    report.append("## Distribución por categoría")
    report.append("")

    for category, quantity in category_count.items():

        report.append(
            f"- **{category}:** {quantity} casos"
        )

    report.append("")

    # --------------------------------------------------------
    # TÉCNICAS RECOMENDADAS
    # --------------------------------------------------------

    report.append("## Técnicas recomendadas")
    report.append("")

    for category, technique in TECHNIQUES.items():

        report.append(
            f"### {category}"
        )

        report.append("")

        report.append(technique)

        report.append("")

    # --------------------------------------------------------
    # CONCLUSIÓN
    # --------------------------------------------------------

    report.append("## Conclusión")
    report.append("")

    report.append(
        "La taxonomía permite identificar diferentes "
        "enfoques de inteligencia artificial aplicables "
        "al monitoreo de servidores. Los casos analizados "
        "muestran que la detección de anomalías puede "
        "combinar aprendizaje automático, sistemas "
        "expertos, optimización y sistemas de recomendación."
    )

    report.append("")

    report.append(
        "Esta clasificación constituye la base para "
        "las siguientes etapas del proyecto, donde se "
        "implementará un sistema específico para detectar "
        "anomalías en métricas de rendimiento de servidores."
    )

    report.append("")

    # --------------------------------------------------------
    # GUARDAR ARCHIVO
    # --------------------------------------------------------

    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    return REPORT_FILE


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():

    cases = read_cases()

    results = []

    print("=" * 80)
    print("SEMANA 03 - TAXONOMÍA Y CLASIFICACIÓN")
    print("PROYECTO: DETECCIÓN DE ANOMALÍAS EN SERVIDORES")
    print("=" * 80)

    # --------------------------------------------------------
    # CLASIFICAR CASOS
    # --------------------------------------------------------

    for case in cases:

        automatic, detected, scores = classify_problem(
            case["descripcion"]
        )

        result = {
            "id": case["id"],
            "descripcion": case["descripcion"],
            "automatic": automatic,
            "detected": detected,
            "scores": scores,
            "technique": TECHNIQUES.get(
                automatic,
                "Análisis adicional"
            ),
        }

        results.append(result)

        print()
        print(f"Caso {case['id']}:")
        print(
            f"Descripción: {case['descripcion']}"
        )

        print(
            f"Categoría principal: {automatic}"
        )

        print(
            "Categorías detectadas: "
            + (
                ", ".join(detected)
                if detected
                else "Ninguna"
            )
        )

        print(
            f"Técnica recomendada: "
            f"{result['technique']}"
        )

    # --------------------------------------------------------
    # RESUMEN
    # --------------------------------------------------------

    category_count = {}

    for result in results:

        category = result["automatic"]

        category_count[category] = (
            category_count.get(category, 0) + 1
        )

    print()
    print("=" * 80)
    print("RESUMEN")
    print("=" * 80)

    print(
        f"Casos procesados: {len(cases)}"
    )

    print()
    print("Distribución por categoría:")

    for category, quantity in category_count.items():

        print(
            f"- {category}: {quantity}"
        )

    # --------------------------------------------------------
    # CREAR REPORTE
    # --------------------------------------------------------

    report_path = generate_report(
        cases,
        results,
        category_count
    )

    print()
    print("=" * 80)
    print("REPORTE GENERADO")
    print("=" * 80)

    print(
        f"Archivo: {report_path}"
    )


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()