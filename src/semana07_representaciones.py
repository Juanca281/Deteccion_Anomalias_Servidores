from pathlib import Path
import argparse
import json
import math
import re


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"
REPORT_PATH = REPORTS_DIR / "semana07.md"


# ============================================================
# UMBRALES ACADÉMICOS DEL PROYECTO
# ============================================================

LIMITS = {
    "cpu_alta": 80,
    "ram_alta": 85,
    "disco_alto": 90,
    "latencia_alta": 150,
    "solicitudes_altas": 1200,
    "errores_altos": 10,
}


# ============================================================
# VECTOR DE REFERENCIA
# ============================================================

REFERENCE = {
    "cpu": 50.0,
    "ram": 55.0,
    "disco": 60.0,
    "latencia": 50.0,
    "solicitudes": 500.0,
    "errores": 0.0,
}


# ============================================================
# ESCALA PARA NORMALIZACIÓN
# ============================================================

SCALE = {
    "cpu": 100.0,
    "ram": 100.0,
    "disco": 100.0,
    "latencia": 500.0,
    "solicitudes": 2000.0,
    "errores": 50.0,
}


# ============================================================
# ESTADOS DEL AUTÓMATA
# ============================================================

STATE_NAMES = {
    "q0": "NORMAL",
    "q1": "ADVERTENCIA",
    "q2": "ANOMALÍA",
    "q3": "CRÍTICO",
    "q4": "RECUPERACIÓN",
}


# ============================================================
# TABLA DE TRANSICIONES
# ============================================================

TRANSITIONS = {
    ("q0", "N"): "q0",
    ("q0", "A"): "q1",
    ("q0", "C"): "q3",
    ("q0", "R"): "q0",

    ("q1", "N"): "q0",
    ("q1", "A"): "q2",
    ("q1", "C"): "q3",
    ("q1", "R"): "q4",

    ("q2", "N"): "q4",
    ("q2", "A"): "q2",
    ("q2", "C"): "q3",
    ("q2", "R"): "q4",

    ("q3", "N"): "q4",
    ("q3", "A"): "q2",
    ("q3", "C"): "q3",
    ("q3", "R"): "q4",

    ("q4", "N"): "q0",
    ("q4", "A"): "q1",
    ("q4", "C"): "q3",
    ("q4", "R"): "q4",
}


# ============================================================
# UTILIDADES
# ============================================================

def clean_status(status):
    return str(status).strip().lower()


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


# ============================================================
# NORMALIZAR OBSERVACIÓN
# ============================================================

def normalize_observation(observation):
    return {
        "cpu": safe_float(
            observation.get("cpu", 0)
        ),
        "ram": safe_float(
            observation.get("ram", 0)
        ),
        "disco": safe_float(
            observation.get("disco", 0)
        ),
        "latencia": safe_float(
            observation.get("latencia", 0)
        ),
        "solicitudes": safe_float(
            observation.get("solicitudes", 0)
        ),
        "errores": safe_int(
            observation.get("errores", 0)
        ),
        "estado": str(
            observation.get(
                "estado",
                "Activo"
            )
        ).strip(),
    }


# ============================================================
# VALIDAR OBSERVACIÓN
# ============================================================

def validate_observation(observation):
    errors = []

    if not 0 <= observation["cpu"] <= 100:
        errors.append(
            "CPU debe estar entre 0 y 100."
        )

    if not 0 <= observation["ram"] <= 100:
        errors.append(
            "RAM debe estar entre 0 y 100."
        )

    if not 0 <= observation["disco"] <= 100:
        errors.append(
            "Disco debe estar entre 0 y 100."
        )

    if observation["latencia"] < 0:
        errors.append(
            "La latencia no puede ser negativa."
        )

    if observation["solicitudes"] < 0:
        errors.append(
            "Las solicitudes no pueden ser negativas."
        )

    if observation["errores"] < 0:
        errors.append(
            "Los errores no pueden ser negativos."
        )

    if clean_status(
        observation["estado"]
    ) not in {
        "activo",
        "inactivo",
        "mantenimiento",
    }:
        errors.append(
            "Estado del servidor no válido."
        )

    return errors


# ============================================================
# REPRESENTACIÓN NUMÉRICA
# ============================================================

def numeric_representation(observation):
    metrics = [
        "cpu",
        "ram",
        "disco",
        "latencia",
        "solicitudes",
        "errores",
    ]

    vector = [
        observation[metric]
        for metric in metrics
    ]

    reference_vector = [
        REFERENCE[metric]
        for metric in metrics
    ]

    normalized_current = []

    normalized_reference = []

    for metric in metrics:
        normalized_current.append(
            observation[metric]
            / SCALE[metric]
        )

        normalized_reference.append(
            REFERENCE[metric]
            / SCALE[metric]
        )

    squared_difference = 0

    for current, reference in zip(
        normalized_current,
        normalized_reference,
    ):
        squared_difference += (
            current - reference
        ) ** 2

    distance = math.sqrt(
        squared_difference
    )

    return {
        "vector": vector,
        "reference": reference_vector,
        "normalized_vector": normalized_current,
        "distance": round(
            distance,
            4
        ),
    }


# ============================================================
# REPRESENTACIÓN SIMBÓLICA
# ============================================================

def symbolic_representation(observation):
    facts = []

    if (
        observation["cpu"]
        >= LIMITS["cpu_alta"]
    ):
        facts.append(
            "cpu_alta"
        )

    if (
        observation["ram"]
        >= LIMITS["ram_alta"]
    ):
        facts.append(
            "memoria_alta"
        )

    if (
        observation["disco"]
        >= LIMITS["disco_alto"]
    ):
        facts.append(
            "disco_critico"
        )

    if (
        observation["latencia"]
        >= LIMITS["latencia_alta"]
    ):
        facts.append(
            "latencia_alta"
        )

    if (
        observation["solicitudes"]
        >= LIMITS["solicitudes_altas"]
    ):
        facts.append(
            "solicitudes_altas"
        )

    if (
        observation["errores"]
        >= LIMITS["errores_altos"]
    ):
        facts.append(
            "errores_altos"
        )

    if (
        clean_status(
            observation["estado"]
        )
        != "activo"
    ):
        facts.append(
            "servidor_no_disponible"
        )

    conclusions = []

    if (
        "cpu_alta" in facts
        and "memoria_alta" in facts
    ):
        conclusions.append(
            "sobrecarga_recursos"
        )

    if (
        "latencia_alta" in facts
        and "solicitudes_altas" in facts
    ):
        conclusions.append(
            "posible_congestion"
        )

    if (
        "errores_altos" in facts
        and "latencia_alta" in facts
    ):
        conclusions.append(
            "degradacion_servicio"
        )

    if (
        "disco_critico" in facts
    ):
        conclusions.append(
            "riesgo_almacenamiento"
        )

    if (
        "servidor_no_disponible"
        in facts
    ):
        conclusions.append(
            "indisponibilidad_servidor"
        )

    if len(facts) >= 3:
        conclusions.append(
            "anomalia_critica"
        )

    if not facts:
        facts.append(
            "telemetrias_normales"
        )

    if not conclusions:
        conclusions.append(
            "operacion_normal"
        )

    return {
        "facts": facts,
        "conclusions": conclusions,
    }


# ============================================================
# CLASIFICACIÓN AUTOMÁTICA DE UNA LECTURA
# ============================================================

def classify_observation(
    observation,
    previous_symbol=None,
):
    """
    Convierte las telemetrías reales del servidor
    en un símbolo para el autómata.

    N = Normal
    A = Advertencia
    C = Crítico
    R = Recuperación
    """

    conditions = {
        "cpu": (
            observation["cpu"]
            >= LIMITS["cpu_alta"]
        ),
        "ram": (
            observation["ram"]
            >= LIMITS["ram_alta"]
        ),
        "disco": (
            observation["disco"]
            >= LIMITS["disco_alto"]
        ),
        "latencia": (
            observation["latencia"]
            >= LIMITS["latencia_alta"]
        ),
        "solicitudes": (
            observation["solicitudes"]
            >= LIMITS[
                "solicitudes_altas"
            ]
        ),
        "errores": (
            observation["errores"]
            >= LIMITS["errores_altos"]
        ),
    }

    problems = [
        name
        for name, active
        in conditions.items()
        if active
    ]

    server_available = (
        clean_status(
            observation["estado"]
        )
        == "activo"
    )

    problem_count = len(
        problems
    )

    # --------------------------------------------------------
    # Clasificación básica
    # --------------------------------------------------------

    if (
        not server_available
        or problem_count >= 3
    ):
        base_symbol = "C"

    elif problem_count >= 1:
        base_symbol = "A"

    else:
        base_symbol = "N"

    # --------------------------------------------------------
    # Detección automática de recuperación
    # --------------------------------------------------------
    #
    # Si la lectura anterior se encontraba en
    # alerta o estado crítico y ahora las métricas
    # regresaron a valores normales, el símbolo
    # generado será R.
    # --------------------------------------------------------

    if (
        base_symbol == "N"
        and previous_symbol in {
            "A",
            "C",
        }
    ):
        symbol = "R"

    else:
        symbol = base_symbol

    return {
        "symbol": symbol,
        "base_symbol": base_symbol,
        "problem_count": problem_count,
        "problems": problems,
        "available": server_available,
    }


# ============================================================
# GENERAR SECUENCIA AUTOMÁTICA
# ============================================================

def generate_sequence(
    observations,
):
    sequence = []

    classifications = []

    previous_symbol = None

    for index, observation in enumerate(
        observations,
        start=1,
    ):
        classification = (
            classify_observation(
                observation,
                previous_symbol,
            )
        )

        symbol = classification[
            "symbol"
        ]

        sequence.append(
            symbol
        )

        classifications.append({
            "index": index,
            "symbol": symbol,
            "base_symbol": (
                classification[
                    "base_symbol"
                ]
            ),
            "problem_count": (
                classification[
                    "problem_count"
                ]
            ),
            "problems": (
                classification[
                    "problems"
                ]
            ),
            "available": (
                classification[
                    "available"
                ]
            ),
        })

        previous_symbol = symbol

    return {
        "sequence": "".join(
            sequence
        ),
        "classifications": (
            classifications
        ),
    }


# ============================================================
# EJECUTAR AUTÓMATA
# ============================================================

def run_automaton(
    sequence,
):
    current_state = "q0"

    trace = []

    for index, symbol in enumerate(
        sequence,
        start=1,
    ):
        previous_state = (
            current_state
        )

        transition = (
            previous_state,
            symbol,
        )

        if transition not in TRANSITIONS:
            raise ValueError(
                f"Transición no válida: "
                f"{previous_state} + {symbol}"
            )

        current_state = (
            TRANSITIONS[
                transition
            ]
        )

        trace.append({
            "step": index,
            "symbol": symbol,
            "from": previous_state,
            "from_name": (
                STATE_NAMES[
                    previous_state
                ]
            ),
            "to": current_state,
            "to_name": (
                STATE_NAMES[
                    current_state
                ]
            ),
        })

    return {
        "initial_state": "q0",
        "final_state": current_state,
        "final_name": (
            STATE_NAMES[
                current_state
            ]
        ),
        "trace": trace,
    }


# ============================================================
# RECONOCIMIENTO DE PATRONES
# ============================================================

def recognize_patterns(
    sequence,
):
    patterns = []

    # --------------------------------------------------------
    # Operación estable
    # --------------------------------------------------------

    if (
        sequence
        and set(sequence) == {"N"}
    ):
        patterns.append({
            "code": "operacion_estable",
            "name": (
                "Operación estable"
            ),
            "description": (
                "Todas las observaciones "
                "permanecieron en estado normal."
            ),
        })

    # --------------------------------------------------------
    # Degradación progresiva
    # N -> A -> C
    # --------------------------------------------------------

    if re.search(
        r"N+A+C",
        sequence,
    ):
        patterns.append({
            "code": (
                "degradacion_progresiva"
            ),
            "name": (
                "Degradación progresiva"
            ),
            "description": (
                "El servidor evolucionó "
                "desde operación normal "
                "hacia alerta y posteriormente "
                "a un estado crítico."
            ),
        })

    # --------------------------------------------------------
    # Alerta persistente
    # --------------------------------------------------------

    if "AAA" in sequence:
        patterns.append({
            "code": (
                "alerta_persistente"
            ),
            "name": (
                "Alerta persistente"
            ),
            "description": (
                "El servidor mantuvo varias "
                "observaciones consecutivas "
                "en condición de advertencia."
            ),
        })

    # --------------------------------------------------------
    # Falla crítica persistente
    # --------------------------------------------------------

    if "CCC" in sequence:
        patterns.append({
            "code": (
                "critico_persistente"
            ),
            "name": (
                "Falla crítica persistente"
            ),
            "description": (
                "Se detectaron múltiples "
                "lecturas críticas consecutivas."
            ),
        })

    # --------------------------------------------------------
    # Recuperación después de crítico
    # --------------------------------------------------------

    if (
        "CR" in sequence
        or "CCR" in sequence
        or "CCCR" in sequence
    ):
        patterns.append({
            "code": (
                "recuperacion_critica"
            ),
            "name": (
                "Recuperación después "
                "de estado crítico"
            ),
            "description": (
                "Después de una condición "
                "crítica, las métricas regresaron "
                "a valores normales."
            ),
        })

    # --------------------------------------------------------
    # Recuperación después de alerta
    # --------------------------------------------------------

    if (
        "AR" in sequence
        and not any(
            item["code"]
            == "recuperacion_critica"
            for item in patterns
        )
    ):
        patterns.append({
            "code": (
                "recuperacion_alerta"
            ),
            "name": (
                "Recuperación después "
                "de alerta"
            ),
            "description": (
                "El servidor presentó una "
                "advertencia y posteriormente "
                "regresó a condiciones normales."
            ),
        })

    # --------------------------------------------------------
    # Recuperación completada
    # --------------------------------------------------------

    if "RN" in sequence:
        patterns.append({
            "code": (
                "recuperacion_completada"
            ),
            "name": (
                "Recuperación completada"
            ),
            "description": (
                "Después del proceso de "
                "recuperación, el servidor "
                "regresó al estado normal."
            ),
        })

    # --------------------------------------------------------
    # Reincidencia
    # R -> A/C
    # --------------------------------------------------------

    if re.search(
        r"R[AC]",
        sequence,
    ):
        patterns.append({
            "code": (
                "reincidencia"
            ),
            "name": (
                "Reincidencia de anomalía"
            ),
            "description": (
                "Después de una recuperación "
                "se detectó nuevamente una "
                "condición anómala."
            ),
        })

    # --------------------------------------------------------
    # Sin patrón temporal específico
    # --------------------------------------------------------

    if not patterns:
        patterns.append({
            "code": (
                "sin_patron_especifico"
            ),
            "name": (
                "Sin patrón temporal específico"
            ),
            "description": (
                "Las observaciones fueron "
                "clasificadas correctamente, "
                "pero no forman uno de los "
                "patrones temporales definidos."
            ),
        })

    return patterns


# ============================================================
# DESCRIPCIÓN DEL ESTADO FINAL
# ============================================================

def final_state_description(
    state,
):
    descriptions = {
        "q0": (
            "El servidor finaliza "
            "en operación normal."
        ),
        "q1": (
            "El servidor presenta una "
            "advertencia inicial."
        ),
        "q2": (
            "El servidor presenta una "
            "anomalía persistente."
        ),
        "q3": (
            "El servidor finaliza "
            "en estado crítico."
        ),
        "q4": (
            "El servidor se encuentra "
            "en proceso de recuperación."
        ),
    }

    return descriptions.get(
        state,
        "Estado no identificado.",
    )


# ============================================================
# ANALIZAR OBSERVACIONES
# ============================================================

def analyze_observations(
    observations,
):
    normalized = []

    for index, raw in enumerate(
        observations,
        start=1,
    ):
        observation = (
            normalize_observation(
                raw
            )
        )

        validation_errors = (
            validate_observation(
                observation
            )
        )

        if validation_errors:
            raise ValueError(
                f"Lectura {index}: "
                + " ".join(
                    validation_errors
                )
            )

        normalized.append(
            observation
        )

    if not normalized:
        raise ValueError(
            "Debe existir al menos "
            "una observación."
        )

    # --------------------------------------------------------
    # Representaciones de cada lectura
    # --------------------------------------------------------

    readings = []

    for index, observation in enumerate(
        normalized,
        start=1,
    ):
        numeric = (
            numeric_representation(
                observation
            )
        )

        symbolic = (
            symbolic_representation(
                observation
            )
        )

        readings.append({
            "index": index,
            "data": observation,
            "numeric": numeric,
            "symbolic": symbolic,
        })

    # --------------------------------------------------------
    # Secuencia automática
    # --------------------------------------------------------

    generated = (
        generate_sequence(
            normalized
        )
    )

    sequence = (
        generated[
            "sequence"
        ]
    )

    # Añadir símbolo a cada lectura

    for (
        reading,
        classification,
    ) in zip(
        readings,
        generated[
            "classifications"
        ],
    ):
        reading[
            "classification"
        ] = classification

    # --------------------------------------------------------
    # Autómata
    # --------------------------------------------------------

    automaton = (
        run_automaton(
            sequence
        )
    )

    # --------------------------------------------------------
    # Patrones
    # --------------------------------------------------------

    patterns = (
        recognize_patterns(
            sequence
        )
    )

    # --------------------------------------------------------
    # Resultado
    # --------------------------------------------------------

    return {
        "observations": readings,
        "sequence": sequence,
        "automaton": automaton,
        "patterns": patterns,
        "final_description": (
            final_state_description(
                automaton[
                    "final_state"
                ]
            )
        ),
    }


# ============================================================
# AUTÓMATA VISUAL EN CONSOLA
# ============================================================

def visual_automaton(
    result,
):
    trace = (
        result[
            "automaton"
        ][
            "trace"
        ]
    )

    lines = []

    lines.append(
        "AUTÓMATA DE ESTADOS DEL SERVIDOR"
    )

    lines.append(
        "=" * 64
    )

    lines.append("")

    lines.append(
        "┌─────────────────┐"
    )

    lines.append(
        "│ q0              │"
    )

    lines.append(
        "│ NORMAL          │"
    )

    lines.append(
        "└────────┬────────┘"
    )

    for item in trace:
        lines.append(
            f"         │ {item['symbol']}"
        )

        lines.append(
            "         ▼"
        )

        state_label = (
            f"{item['to']} "
            f"{item['to_name']}"
        )

        lines.append(
            "┌─────────────────┐"
        )

        lines.append(
            f"│ {state_label:<15} │"
        )

        lines.append(
            "└─────────────────┘"
        )

    return "\n".join(
        lines
    )


# ============================================================
# GENERAR REPORTE
# ============================================================

def write_report(
    result,
):
    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = []

    lines.append(
        "# Semana 7 - Representaciones del reconocimiento"
    )

    lines.append("")

    lines.append(
        "## Descripción"
    )

    lines.append("")

    lines.append(
        "Se representó el comportamiento de un servidor "
        "mediante métodos numéricos, simbólicos y un "
        "autómata de estados. A diferencia de ingresar "
        "manualmente una secuencia, cada símbolo del "
        "autómata es generado automáticamente a partir "
        "de las telemetrías observadas."
    )

    lines.append("")

    # --------------------------------------------------------
    # DATOS
    # --------------------------------------------------------

    lines.append(
        "## Datos analizados"
    )

    lines.append("")

    lines.append(
        "| Lectura | CPU | RAM | Disco | Latencia | Solicitudes/min | Errores | Estado | Símbolo |"
    )

    lines.append(
        "|---:|---:|---:|---:|---:|---:|---:|---|:---:|"
    )

    for reading in result[
        "observations"
    ]:
        data = reading[
            "data"
        ]

        classification = reading[
            "classification"
        ]

        lines.append(
            f"| {reading['index']} "
            f"| {data['cpu']:.1f}% "
            f"| {data['ram']:.1f}% "
            f"| {data['disco']:.1f}% "
            f"| {data['latencia']:.1f} ms "
            f"| {data['solicitudes']:.0f} "
            f"| {data['errores']} "
            f"| {data['estado']} "
            f"| {classification['symbol']} |"
        )

    lines.append("")

    # --------------------------------------------------------
    # REPRESENTACIÓN NUMÉRICA
    # --------------------------------------------------------

    lines.append(
        "## Representación numérica"
    )

    lines.append("")

    lines.append(
        "| Lectura | Vector | Distancia al estado de referencia |"
    )

    lines.append(
        "|---:|---|---:|"
    )

    for reading in result[
        "observations"
    ]:
        numeric = reading[
            "numeric"
        ]

        lines.append(
            f"| {reading['index']} "
            f"| {numeric['vector']} "
            f"| {numeric['distance']:.4f} |"
        )

    lines.append("")

    # --------------------------------------------------------
    # REPRESENTACIÓN SIMBÓLICA
    # --------------------------------------------------------

    lines.append(
        "## Representación simbólica"
    )

    lines.append("")

    lines.append(
        "| Lectura | Hechos | Conclusiones |"
    )

    lines.append(
        "|---:|---|---|"
    )

    for reading in result[
        "observations"
    ]:
        symbolic = reading[
            "symbolic"
        ]

        facts = ", ".join(
            symbolic[
                "facts"
            ]
        )

        conclusions = ", ".join(
            symbolic[
                "conclusions"
            ]
        )

        lines.append(
            f"| {reading['index']} "
            f"| {facts} "
            f"| {conclusions} |"
        )

    lines.append("")

    # --------------------------------------------------------
    # AUTÓMATA
    # --------------------------------------------------------

    lines.append(
        "## Reconocimiento mediante autómata"
    )

    lines.append("")

    lines.append(
        f"Secuencia generada automáticamente: "
        f"`{result['sequence']}`"
    )

    lines.append("")

    lines.append(
        "| Paso | Entrada | Estado anterior | Estado resultante |"
    )

    lines.append(
        "|---:|:---:|---|---|"
    )

    for item in result[
        "automaton"
    ][
        "trace"
    ]:
        lines.append(
            f"| {item['step']} "
            f"| {item['symbol']} "
            f"| {item['from']} - {item['from_name']} "
            f"| {item['to']} - {item['to_name']} |"
        )

    lines.append("")

    lines.append(
        f"**Estado final:** "
        f"{result['automaton']['final_state']} "
        f"- {result['automaton']['final_name']}."
    )

    lines.append("")

    lines.append(
        result[
            "final_description"
        ]
    )

    lines.append("")

    # --------------------------------------------------------
    # PATRONES
    # --------------------------------------------------------

    lines.append(
        "## Patrones reconocidos"
    )

    lines.append("")

    for pattern in result[
        "patterns"
    ]:
        lines.append(
            f"- **{pattern['name']}**: "
            f"{pattern['description']}"
        )

    lines.append("")

    # --------------------------------------------------------
    # COMPARACIÓN REQUERIDA POR LA PRÁCTICA
    # --------------------------------------------------------

    lines.append(
        "## Comparación de representaciones"
    )

    lines.append("")

    lines.append(
        "| Representación | Ventaja | Limitación | Información que se pierde |"
    )

    lines.append(
        "|---|---|---|---|"
    )

    lines.append(
        "| Numérica "
        "| Permite comparar métricas y medir diferencias. "
        "| Requiere interpretar los valores. "
        "| Pierde parte del significado conceptual del problema. |"
    )

    lines.append(
        "| Simbólica "
        "| Facilita interpretar hechos y conclusiones. "
        "| Depende de reglas y umbrales definidos. "
        "| Reduce el detalle numérico original. |"
    )

    lines.append(
        "| Autómata "
        "| Permite representar la evolución temporal del servidor. "
        "| Resume varias métricas en pocos estados. "
        "| No conserva todos los valores exactos de cada lectura. |"
    )

    lines.append("")

    # --------------------------------------------------------
    # ANÁLISIS
    # --------------------------------------------------------

    lines.append(
        "## Análisis"
    )

    lines.append("")

    lines.append(
        "Las telemetrías se transformaron primero en "
        "representaciones numéricas y simbólicas. "
        "Posteriormente cada lectura fue clasificada "
        "automáticamente como normal, advertencia, crítica "
        "o recuperación. Estos símbolos fueron utilizados "
        "como entradas del autómata para identificar la "
        "evolución temporal del servidor y reconocer "
        "patrones de comportamiento."
    )

    REPORT_PATH.write_text(
        "\n".join(
            lines
        ),
        encoding="utf-8",
    )


# ============================================================
# MOSTRAR RESULTADO
# ============================================================

def print_result(
    result,
):
    print(
        "=" * 70
    )

    print(
        "SEMANA 7 - REPRESENTACIONES DEL RECONOCIMIENTO"
    )

    print(
        "=" * 70
    )

    print()

    print(
        "SECUENCIA GENERADA AUTOMÁTICAMENTE:"
    )

    print(
        result[
            "sequence"
        ]
    )

    print()

    print(
        visual_automaton(
            result
        )
    )

    print()

    print(
        "PATRONES RECONOCIDOS:"
    )

    for pattern in result[
        "patterns"
    ]:
        print(
            f"- {pattern['name']}"
        )

    print()

    print(
        "ESTADO FINAL:"
    )

    print(
        result[
            "automaton"
        ][
            "final_name"
        ]
    )

    print()

    print(
        result[
            "final_description"
        ]
    )

    print()

    print(
        f"Reporte generado: "
        f"{REPORT_PATH}"
    )


# ============================================================
# OBSERVACIONES DE DEMOSTRACIÓN
# ============================================================

def default_observations():
    return [
        {
            "cpu": 45,
            "ram": 52,
            "disco": 61,
            "latencia": 40,
            "solicitudes": 470,
            "errores": 0,
            "estado": "Activo",
        },
        {
            "cpu": 83,
            "ram": 74,
            "disco": 65,
            "latencia": 90,
            "solicitudes": 720,
            "errores": 2,
            "estado": "Activo",
        },
        {
            "cpu": 94,
            "ram": 91,
            "disco": 94,
            "latencia": 260,
            "solicitudes": 1600,
            "errores": 18,
            "estado": "Activo",
        },
        {
            "cpu": 96,
            "ram": 93,
            "disco": 95,
            "latencia": 290,
            "solicitudes": 1700,
            "errores": 24,
            "estado": "Activo",
        },
        {
            "cpu": 55,
            "ram": 61,
            "disco": 70,
            "latencia": 62,
            "solicitudes": 530,
            "errores": 1,
            "estado": "Activo",
        },
        {
            "cpu": 48,
            "ram": 57,
            "disco": 68,
            "latencia": 45,
            "solicitudes": 500,
            "errores": 0,
            "estado": "Activo",
        },
    ]


# ============================================================
# ARGUMENTOS
# ============================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Semana 7 - Representaciones "
            "del reconocimiento aplicadas "
            "a servidores."
        )
    )

    # --------------------------------------------------------
    # NUEVO MÉTODO:
    # lista completa de observaciones en JSON
    # --------------------------------------------------------

    parser.add_argument(
        "--observaciones",
        type=str,
        default=None,
        help=(
            "Lista JSON con varias "
            "observaciones del servidor."
        ),
    )

    # --------------------------------------------------------
    # COMPATIBILIDAD CON EL FRONTEND ANTERIOR
    # --------------------------------------------------------

    parser.add_argument(
        "--cpu",
        type=float,
        default=None,
    )

    parser.add_argument(
        "--ram",
        type=float,
        default=None,
    )

    parser.add_argument(
        "--disco",
        type=float,
        default=None,
    )

    parser.add_argument(
        "--latencia",
        type=float,
        default=None,
    )

    parser.add_argument(
        "--solicitudes",
        type=float,
        default=None,
    )

    parser.add_argument(
        "--errores",
        type=int,
        default=None,
    )

    parser.add_argument(
        "--estado",
        type=str,
        default=None,
    )

    # Este argumento se mantiene temporalmente
    # para no romper el app.py anterior.
    #
    # Ya NO se utiliza para controlar el autómata.
    # La secuencia se genera automáticamente.

    parser.add_argument(
        "--secuencia",
        type=str,
        default=None,
    )

    # Salida estructurada útil para Flask

    parser.add_argument(
        "--json",
        action="store_true",
        help=(
            "Devuelve el resultado completo "
            "en formato JSON."
        ),
    )

    return parser.parse_args()


# ============================================================
# CONSTRUIR OBSERVACIONES DESDE ARGUMENTOS
# ============================================================

def observations_from_arguments(
    args,
):
    # --------------------------------------------------------
    # Varias observaciones recibidas como JSON
    # --------------------------------------------------------

    if args.observaciones:
        try:
            observations = (
                json.loads(
                    args.observaciones
                )
            )
        except json.JSONDecodeError as error:
            raise ValueError(
                "El contenido de --observaciones "
                "no es un JSON válido."
            ) from error

        if not isinstance(
            observations,
            list,
        ):
            raise ValueError(
                "--observaciones debe contener "
                "una lista JSON."
            )

        return observations

    # --------------------------------------------------------
    # Compatibilidad con una única lectura
    # --------------------------------------------------------

    scalar_values = [
        args.cpu,
        args.ram,
        args.disco,
        args.latencia,
        args.solicitudes,
        args.errores,
        args.estado,
    ]

    if any(
        value is not None
        for value in scalar_values
    ):
        return [
            {
                "cpu": (
                    args.cpu
                    if args.cpu is not None
                    else 50
                ),
                "ram": (
                    args.ram
                    if args.ram is not None
                    else 55
                ),
                "disco": (
                    args.disco
                    if args.disco is not None
                    else 60
                ),
                "latencia": (
                    args.latencia
                    if args.latencia is not None
                    else 50
                ),
                "solicitudes": (
                    args.solicitudes
                    if args.solicitudes is not None
                    else 500
                ),
                "errores": (
                    args.errores
                    if args.errores is not None
                    else 0
                ),
                "estado": (
                    args.estado
                    if args.estado is not None
                    else "Activo"
                ),
            }
        ]

    # --------------------------------------------------------
    # Sin argumentos:
    # usar demostración completa
    # --------------------------------------------------------

    return default_observations()


# ============================================================
# MAIN
# ============================================================

def main():
    args = parse_arguments()

    try:
        observations = (
            observations_from_arguments(
                args
            )
        )

        result = (
            analyze_observations(
                observations
            )
        )

        write_report(
            result
        )

        if args.json:
            print(
                json.dumps(
                    result,
                    ensure_ascii=False,
                    indent=2,
                )
            )

        else:
            print_result(
                result
            )

    except Exception as error:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": str(error),
                },
                ensure_ascii=False,
                indent=2,
            )
        )

        raise SystemExit(1)


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()