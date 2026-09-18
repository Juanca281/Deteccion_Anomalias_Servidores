from pathlib import Path
import argparse

import numpy as np


# ============================================================
# CONFIGURACIÓN DEL PROYECTO
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

REPORTS_DIR = ROOT / "reports"
REPORT_PATH = REPORTS_DIR / "semana07.md"

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# VALORES DE REFERENCIA
# ============================================================

# Vector:
# [temperatura, carga, errores]

REFERENCE = np.array(
    [
        70.0,
        0.80,
        2.0,
    ]
)


# ============================================================
# ESCALAS PARA NORMALIZACIÓN
# ============================================================

# Se normalizan los valores para evitar que una
# característica domine completamente la distancia.

SCALE = np.array(
    [
        100.0,  # temperatura
        1.0,    # carga
        10.0,   # errores
    ]
)


# ============================================================
# 1. REPRESENTACIÓN NUMÉRICA
# ============================================================

def numeric_representation(
    temperature,
    load,
    errors
):
    """
    Representa el estado del servidor mediante
    un vector numérico y calcula su distancia
    respecto a un estado de referencia.
    """

    sample = np.array(
        [
            float(temperature),
            float(load),
            float(errors),
        ]
    )

    normalized_sample = (
        sample / SCALE
    )

    normalized_reference = (
        REFERENCE / SCALE
    )

    difference = (
        normalized_sample
        - normalized_reference
    )

    distance = np.linalg.norm(
        difference
    )

    return {
        "sample": sample,
        "reference": REFERENCE,
        "normalized_sample": normalized_sample,
        "normalized_reference": normalized_reference,
        "distance": float(distance),
    }


# ============================================================
# 2. REPRESENTACIÓN SIMBÓLICA
# ============================================================

def symbolic_representation(
    temperature,
    load,
    errors
):
    """
    Convierte datos numéricos en hechos simbólicos
    y posteriormente aplica reglas simples.
    """

    facts = set()

    conclusions = []


    # ========================================================
    # GENERACIÓN DE HECHOS
    # ========================================================

    if temperature >= 70:

        facts.add(
            "temperatura_alta"
        )


    if load >= 0.80:

        facts.add(
            "carga_alta"
        )


    if errors >= 3:

        facts.add(
            "errores_presentes"
        )


    # ========================================================
    # REGLA 1
    # ========================================================

    if {
        "temperatura_alta",
        "carga_alta",
    }.issubset(facts):

        conclusions.append(
            "riesgo_termico"
        )


    # ========================================================
    # REGLA 2
    # ========================================================

    if {
        "carga_alta",
        "errores_presentes",
    }.issubset(facts):

        conclusions.append(
            "degradacion_servicio"
        )


    # ========================================================
    # REGLA 3
    # ========================================================

    if {
        "temperatura_alta",
        "carga_alta",
        "errores_presentes",
    }.issubset(facts):

        conclusions.append(
            "anomalia_critica"
        )


    # ========================================================
    # ESTADO NORMAL
    # ========================================================

    if not conclusions:

        conclusions.append(
            "operacion_sin_riesgo_critico"
        )


    return {
        "facts": sorted(facts),
        "conclusions": conclusions,
    }


# ============================================================
# 3. RECONOCIMIENTO MEDIANTE AUTÓMATA
# ============================================================

def automaton_representation(
    sequence
):
    """
    Reconoce una anomalía persistente.

    Alfabeto:
        N = comportamiento normal
        A = comportamiento anómalo

    q0:
        estado normal

    q1:
        se detectó una anomalía

    q2:
        se detectaron dos o más anomalías consecutivas

    q2 es el estado de aceptación.
    """

    sequence = (
        sequence
        .upper()
        .strip()
    )


    if not sequence:

        raise ValueError(
            "La secuencia no puede estar vacía."
        )


    valid_symbols = {
        "N",
        "A",
    }


    for symbol in sequence:

        if symbol not in valid_symbols:

            raise ValueError(
                "La secuencia solo puede contener "
                "N (normal) y A (anomalía)."
            )


    # ========================================================
    # ESTADO INICIAL
    # ========================================================

    state = "q0"


    # ========================================================
    # TABLA DE TRANSICIONES
    # ========================================================

    transitions = {

        ("q0", "N"): "q0",
        ("q0", "A"): "q1",

        ("q1", "N"): "q0",
        ("q1", "A"): "q2",

        ("q2", "N"): "q0",
        ("q2", "A"): "q2",
    }


    trace = []


    # ========================================================
    # PROCESAR SECUENCIA
    # ========================================================

    for symbol in sequence:

        previous_state = state

        state = transitions[
            (
                state,
                symbol
            )
        ]

        trace.append(
            f"{previous_state} --{symbol}--> {state}"
        )


    # ========================================================
    # ESTADO DE ACEPTACIÓN
    # ========================================================

    accepted = (
        state == "q2"
    )


    return {
        "sequence": sequence,
        "final_state": state,
        "accepted": accepted,
        "trace": trace,
    }


# ============================================================
# ANALIZAR SERVIDOR
# ============================================================

def analyze_server(
    temperature,
    load,
    errors,
    sequence
):
    """
    Ejecuta las tres representaciones sobre
    un mismo fenómeno del proyecto.
    """

    numeric = numeric_representation(
        temperature,
        load,
        errors
    )


    symbolic = symbolic_representation(
        temperature,
        load,
        errors
    )


    automaton = automaton_representation(
        sequence
    )


    return {
        "temperature": temperature,
        "load": load,
        "errors": errors,
        "sequence": sequence,
        "numeric": numeric,
        "symbolic": symbolic,
        "automaton": automaton,
    }


# ============================================================
# GENERAR REPORTE
# ============================================================

def write_report(
    result
):
    """
    Genera automáticamente reports/semana07.md.
    """

    numeric = result[
        "numeric"
    ]

    symbolic = result[
        "symbolic"
    ]

    automaton = result[
        "automaton"
    ]


    # ========================================================
    # FORMATEAR HECHOS
    # ========================================================

    facts_text = (
        ", ".join(
            symbolic["facts"]
        )
        if symbolic["facts"]
        else "ninguno"
    )


    conclusions_text = (
        ", ".join(
            symbolic["conclusions"]
        )
    )


    # ========================================================
    # FORMATEAR RECORRIDO DEL AUTÓMATA
    # ========================================================

    trace_text = "\n".join(
        f"- {step}"
        for step in automaton[
            "trace"
        ]
    )


    accepted_text = (
        "Sí"
        if automaton["accepted"]
        else "No"
    )


    lines = [

        "# Semana 07 - Representaciones del reconocimiento",

        "",

        "## Proyecto: Detección de anomalías en servidores",

        "",

        (
            "La Semana 07 representa un mismo evento de "
            "monitoreo mediante tres enfoques diferentes: "
            "representación numérica, representación "
            "simbólica y reconocimiento mediante autómatas."
        ),

        "",

        "## Datos analizados",

        "",

        f"- **Temperatura:** {result['temperature']} °C",

        f"- **Carga:** {result['load']}",

        f"- **Errores:** {result['errors']}",

        (
            f"- **Secuencia temporal:** "
            f"{result['sequence']}"
        ),

        "",

        "---",

        "",

        "## 1. Representación numérica",

        "",

        (
            "El servidor se representa mediante un vector "
            "formado por temperatura, carga y cantidad "
            "de errores."
        ),

        "",

        (
            "**Vector actual:** "
            f"{numeric['sample'].tolist()}"
        ),

        "",

        (
            "**Vector de referencia:** "
            f"{numeric['reference'].tolist()}"
        ),

        "",

        (
            "**Vector normalizado actual:** "
            f"{numeric['normalized_sample'].round(3).tolist()}"
        ),

        "",

        (
            "**Distancia numérica:** "
            f"{numeric['distance']:.3f}"
        ),

        "",

        (
            "Una distancia pequeña indica que el estado "
            "actual es parecido al estado de referencia. "
            "Una distancia mayor indica una diferencia "
            "más significativa."
        ),

        "",

        "---",

        "",

        "## 2. Representación simbólica",

        "",

        (
            "Los valores numéricos se convierten en "
            "conceptos que pueden ser utilizados por "
            "reglas explícitas."
        ),

        "",

        f"**Hechos detectados:** {facts_text}",

        "",

        (
            "**Conclusiones simbólicas:** "
            f"{conclusions_text}"
        ),

        "",

        (
            "Por ejemplo, cuando temperatura_alta y "
            "carga_alta están presentes, el sistema "
            "puede concluir riesgo_termico."
        ),

        "",

        "---",

        "",

        "## 3. Reconocimiento mediante autómata",

        "",

        (
            "El autómata analiza una secuencia temporal "
            "de estados del servidor."
        ),

        "",

        "- **N:** comportamiento normal.",

        "- **A:** comportamiento anómalo.",

        "",

        (
            "El estado q2 representa la detección de "
            "dos o más anomalías consecutivas al final "
            "de la secuencia."
        ),

        "",

        f"**Secuencia:** {automaton['sequence']}",

        "",

        f"**Estado final:** {automaton['final_state']}",

        "",

        (
            "**¿Se reconoce una anomalía persistente?:** "
            f"{accepted_text}"
        ),

        "",

        "### Recorrido",

        "",

        trace_text,

        "",

        "---",

        "",

        "## Comparación de representaciones",

        "",

        (
            "| Representación | Ventaja | Limitación | "
            "Pérdida de información |"
        ),

        (
            "|---|---|---|---|"
        ),

        (
            "| Numérica | Permite medir diferencias y "
            "comparar estados mediante distancias. | "
            "Requiere definir escalas y valores de "
            "referencia. | No explica por sí sola el "
            "significado operativo del resultado. |"
        ),

        (
            "| Simbólica | Produce hechos y conclusiones "
            "fáciles de explicar. | Depende de umbrales "
            "y reglas definidas previamente. | Al convertir "
            "72 °C en temperatura_alta se pierde el valor "
            "exacto. |"
        ),

        (
            "| Autómata | Permite reconocer patrones "
            "secuenciales y persistencia de anomalías. | "
            "Solo reconoce patrones definidos mediante sus "
            "estados y transiciones. | La secuencia N/A no "
            "conserva los valores exactos de las métricas. |"
        ),

        "",

        "## Conversión entre representaciones",

        "",

        (
            "Los valores numéricos del monitoreo pueden "
            "convertirse en hechos simbólicos utilizando "
            "umbrales. Por ejemplo, una temperatura igual "
            "o superior a 70 °C se transforma en el hecho "
            "`temperatura_alta`."
        ),

        "",

        (
            "De forma similar, varias observaciones del "
            "servidor pueden convertirse en una secuencia "
            "de estados N y A. El autómata utiliza dicha "
            "secuencia para identificar persistencia en "
            "el comportamiento anómalo."
        ),

        "",

        "## Limitaciones",

        "",

        (
            "- Los valores de referencia y los umbrales "
            "son definidos para la práctica y deberían "
            "ajustarse con datos reales."
        ),

        (
            "- Una representación simbólica simplifica "
            "los valores originales."
        ),

        (
            "- El autómata solamente considera estados "
            "N y A, por lo que no diferencia tipos de "
            "anomalías."
        ),

        (
            "- La distancia numérica indica diferencia, "
            "pero por sí sola no determina la causa de "
            "la anomalía."
        ),

        "",

        "## Conclusión",

        "",

        (
            "La misma situación de un servidor puede "
            "representarse de diferentes maneras. La "
            "representación numérica permite realizar "
            "comparaciones matemáticas; la simbólica "
            "facilita la explicación mediante hechos y "
            "reglas; y el autómata permite reconocer "
            "patrones temporales."
        ),

        "",

        (
            "La combinación de estas representaciones "
            "complementa el sistema de detección de "
            "anomalías desarrollado durante el semestre."
        ),

        "",
    ]


    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )


# ============================================================
# MOSTRAR RESULTADOS
# ============================================================

def print_results(
    result
):
    """
    Muestra los resultados en consola.
    """

    numeric = result[
        "numeric"
    ]

    symbolic = result[
        "symbolic"
    ]

    automaton = result[
        "automaton"
    ]


    print(
        "=" * 70
    )

    print(
        "SEMANA 07 - REPRESENTACIONES DEL RECONOCIMIENTO"
    )

    print(
        "PROYECTO: DETECCIÓN DE ANOMALÍAS EN SERVIDORES"
    )

    print(
        "=" * 70
    )


    print()

    print(
        "DATOS DE ENTRADA"
    )

    print(
        "-" * 70
    )

    print(
        f"Temperatura: {result['temperature']} °C"
    )

    print(
        f"Carga: {result['load']}"
    )

    print(
        f"Errores: {result['errors']}"
    )

    print(
        f"Secuencia: {result['sequence']}"
    )


    # ========================================================
    # NUMÉRICO
    # ========================================================

    print()

    print(
        "1. REPRESENTACIÓN NUMÉRICA"
    )

    print(
        "-" * 70
    )

    print(
        "Vector actual:",
        numeric["sample"].tolist()
    )

    print(
        "Vector referencia:",
        numeric["reference"].tolist()
    )

    print(
        "Distancia:",
        round(
            numeric["distance"],
            3
        )
    )


    # ========================================================
    # SIMBÓLICO
    # ========================================================

    print()

    print(
        "2. REPRESENTACIÓN SIMBÓLICA"
    )

    print(
        "-" * 70
    )

    print(
        "Hechos:",
        ", ".join(
            symbolic["facts"]
        ) or "ninguno"
    )

    print(
        "Conclusiones:",
        ", ".join(
            symbolic["conclusions"]
        )
    )


    # ========================================================
    # AUTÓMATA
    # ========================================================

    print()

    print(
        "3. AUTÓMATA"
    )

    print(
        "-" * 70
    )

    for step in automaton[
        "trace"
    ]:

        print(
            step
        )


    print()

    print(
        "Estado final:",
        automaton["final_state"]
    )

    print(
        "Anomalía persistente:",
        automaton["accepted"]
    )


    print()

    print(
        "=" * 70
    )

    print(
        f"Reporte generado: {REPORT_PATH}"
    )

    print(
        "=" * 70
    )


# ============================================================
# ARGUMENTOS
# ============================================================

def get_arguments():

    parser = argparse.ArgumentParser(
        description=(
            "Semana 07 - Representaciones "
            "del reconocimiento"
        )
    )


    parser.add_argument(
        "--temperatura",
        type=float,
        default=72.0,
        help="Temperatura del servidor"
    )


    parser.add_argument(
        "--carga",
        type=float,
        default=0.85,
        help="Carga del servidor entre 0 y 1"
    )


    parser.add_argument(
        "--errores",
        type=int,
        default=3,
        help="Cantidad de errores"
    )


    parser.add_argument(
        "--secuencia",
        type=str,
        default="NAA",
        help=(
            "Secuencia temporal usando "
            "N=normal y A=anomalía"
        )
    )


    return parser.parse_args()


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================

if __name__ == "__main__":

    args = get_arguments()


    result = analyze_server(
        temperature=args.temperatura,
        load=args.carga,
        errors=args.errores,
        sequence=args.secuencia
    )


    print_results(
        result
    )


    write_report(
        result
    )