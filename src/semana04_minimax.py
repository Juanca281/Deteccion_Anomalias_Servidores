from pathlib import Path


"""
Semana 04 - Minimax

Proyecto:
Detección de anomalías en servidores

Aplicación:
Minimax se utiliza para seleccionar una acción
ante una situación de riesgo operativo.
"""


# ============================================================
# CONFIGURACIÓN DEL PROYECTO
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"
REPORT_FILE = REPORTS_DIR / "semana04.md"


# ============================================================
# ACCIONES POSIBLES
# ============================================================

ACTIONS = [
    "Mantener servidor activo",
    "Redistribuir carga",
    "Activar servidor de respaldo",
]


# ============================================================
# EVALUACIÓN DE LAS ACCIONES
# ============================================================

def evaluate_action(action):
    """
    Asigna una utilidad a cada acción.

    Un valor mayor representa una decisión más favorable
    para mantener la disponibilidad del sistema.
    """

    utilities = {
        "Mantener servidor activo": 2,
        "Redistribuir carga": 6,
        "Activar servidor de respaldo": 8,
    }

    return utilities[action]


# ============================================================
# MINIMAX
# ============================================================

def minimax(actions, maximizing=True):
    """
    Implementación básica del algoritmo Minimax.

    MAX busca la acción con mayor utilidad.

    MIN representa un escenario donde se seleccionaría
    la alternativa con menor utilidad.
    """

    if not actions:
        return 0

    scores = []

    for action in actions:

        score = evaluate_action(action)

        scores.append(score)

    if maximizing:
        return max(scores)

    return min(scores)


# ============================================================
# MEJOR ACCIÓN
# ============================================================

def best_move(actions):
    """
    Devuelve la acción con mayor utilidad.
    """

    if not actions:
        return None

    best_action = actions[0]

    best_score = evaluate_action(
        best_action
    )

    for action in actions[1:]:

        score = evaluate_action(action)

        if score > best_score:

            best_score = score
            best_action = action

    return best_action


# ============================================================
# ESCENARIO
# ============================================================

print("=" * 70)
print("SEMANA 04 - MINIMAX")
print("PROYECTO: DETECCIÓN DE ANOMALÍAS EN SERVIDORES")
print("=" * 70)

print()

print("Situación:")

print(
    "Se detecta una anomalía en el servidor principal."
)

print()

print("Acciones disponibles:")

for number, action in enumerate(
    ACTIONS,
    start=1
):

    print(
        f"{number}. {action}"
    )


# ============================================================
# EVALUAR ACCIONES
# ============================================================

print()

print("Evaluación de acciones:")

print("-" * 70)

for action in ACTIONS:

    score = evaluate_action(action)

    print(
        f"{action}: utilidad = {score}"
    )


# ============================================================
# EJECUTAR MINIMAX
# ============================================================

max_value = minimax(
    ACTIONS,
    maximizing=True
)

selected_action = best_move(
    ACTIONS
)


# ============================================================
# MOSTRAR RESULTADO
# ============================================================

print()

print("=" * 70)
print("RESULTADO MINIMAX")
print("=" * 70)

print(
    f"Mejor acción: {selected_action}"
)

print(
    f"Utilidad: {max_value}"
)


# ============================================================
# GENERAR REPORTE MINIMAX
# ============================================================

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


minimax_report = []

minimax_report.append(
    "---"
)

minimax_report.append("")

minimax_report.append(
    "## 2. Minimax"
)

minimax_report.append("")

minimax_report.append(
    "Minimax se utiliza como mecanismo de toma de "
    "decisiones después de detectar una anomalía "
    "en un servidor."
)

minimax_report.append("")

minimax_report.append(
    "### Estado"
)

minimax_report.append("")

minimax_report.append(
    "El servidor principal presenta una anomalía "
    "operativa y el sistema debe seleccionar una acción."
)

minimax_report.append("")

minimax_report.append(
    "### Acciones disponibles"
)

minimax_report.append("")

for action in ACTIONS:

    minimax_report.append(
        f"- {action}"
    )

minimax_report.append("")

minimax_report.append(
    "### Función de utilidad"
)

minimax_report.append("")

for action in ACTIONS:

    score = evaluate_action(action)

    minimax_report.append(
        f"- **{action}:** utilidad {score}"
    )

minimax_report.append("")

minimax_report.append(
    "### Resultado"
)

minimax_report.append("")

minimax_report.append(
    f"**Mejor acción:** {selected_action}"
)

minimax_report.append("")

minimax_report.append(
    f"**Utilidad obtenida:** {max_value}"
)

minimax_report.append("")

minimax_report.append(
    "### Relación con el proyecto"
)

minimax_report.append("")

minimax_report.append(
    "Minimax puede utilizarse como componente de decisión "
    "después de detectar una anomalía. El sistema puede "
    "comparar diferentes acciones y seleccionar aquella "
    "que represente una mejor respuesta para mantener "
    "la disponibilidad de los servicios."
)

minimax_report.append("")

minimax_report.append(
    "## Conclusión de la Semana 04"
)

minimax_report.append("")

minimax_report.append(
    "A* y Minimax representan dos capacidades diferentes "
    "dentro de un sistema inteligente. A* permite buscar "
    "rutas considerando costos y una heurística, mientras "
    "que Minimax permite analizar alternativas de decisión "
    "mediante una función de utilidad."
)

minimax_report.append("")

minimax_report.append(
    "Dentro del proyecto, ambos algoritmos pueden "
    "complementar el proceso de detección de anomalías: "
    "A* como mecanismo de planificación y Minimax como "
    "mecanismo de selección de una respuesta."
)

minimax_report.append("")

minimax_report.append(
    "<!-- FIN_MINIMAX -->"
)


# ============================================================
# ACTUALIZAR SEMANA04.MD SIN BORRAR A*
# ============================================================

if REPORT_FILE.exists():

    existing_report = REPORT_FILE.read_text(
        encoding="utf-8"
    )

    if "<!-- FIN_MINIMAX -->" not in existing_report:

        with REPORT_FILE.open(
            "a",
            encoding="utf-8"
        ) as file:

            file.write("\n")

            file.write(
                "\n".join(minimax_report)
            )

    else:

        print()

        print(
            "La sección Minimax ya existe en semana04.md."
        )

else:

    REPORT_FILE.write_text(
        "\n".join(minimax_report),
        encoding="utf-8"
    )


print()

print(
    f"Reporte actualizado: {REPORT_FILE}"
)