import heapq
from pathlib import Path


# ============================================================
# CONFIGURACIÓN DEL PROYECTO
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"
REPORT_FILE = REPORTS_DIR / "semana04.md"


# ============================================================
# RED DE SERVIDORES
# ============================================================

NETWORK = {
    "Servidor-Web": {
        "Servidor-App": 2,
        "Servidor-Backup": 10,
    },
    "Servidor-App": {
        "Servidor-Web": 2,
        "Servidor-BD": 2,
        "Servidor-Monitoreo": 5,
    },
    "Servidor-BD": {
        "Servidor-App": 2,
        "Servidor-Backup": 3,
    },
    "Servidor-Backup": {
        "Servidor-Web": 4,
        "Servidor-BD": 3,
        "Servidor-Recuperacion": 2,
    },
    "Servidor-Monitoreo": {
        "Servidor-App": 5,
        "Servidor-Recuperacion": 2,
    },
    "Servidor-Recuperacion": {
        "Servidor-Backup": 2,
        "Servidor-Monitoreo": 2,
    },
}


# ============================================================
# HEURÍSTICA
# ============================================================

HEURISTIC = {
    "Servidor-Web": 4,
    "Servidor-App": 3,
    "Servidor-BD": 2,
    "Servidor-Backup": 2,
    "Servidor-Monitoreo": 1,
    "Servidor-Recuperacion": 0,
}


def h(node, goal):
    """
    Estima el costo restante desde un servidor
    hasta el servidor objetivo.
    """
    return HEURISTIC.get(node, 0)


# ============================================================
# ALGORITMO A*
# ============================================================

def astar(start, goal):

    frontier = [(0, start)]

    came_from = {
        start: None
    }

    cost = {
        start: 0
    }

    while frontier:

        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for next_node, transition_cost in NETWORK.get(
            current, {}
        ).items():

            new_cost = (
                cost[current] + transition_cost
            )

            if (
                next_node not in cost
                or new_cost < cost[next_node]
            ):

                cost[next_node] = new_cost

                priority = (
                    new_cost
                    + h(next_node, goal)
                )

                heapq.heappush(
                    frontier,
                    (priority, next_node)
                )

                came_from[next_node] = current

    if goal not in came_from:
        return None, None

    # Reconstrucción de la ruta encontrada
    path = []

    current = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()

    return path, cost[goal]


# ============================================================
# ESCENARIO DE PRUEBA
# ============================================================

START = "Servidor-Web"
GOAL = "Servidor-Recuperacion"

path, total_cost = astar(
    START,
    GOAL
)


# ============================================================
# MOSTRAR RESULTADOS
# ============================================================

print("=" * 70)
print("SEMANA 04 - BÚSQUEDA A*")
print("PROYECTO: DETECCIÓN DE ANOMALÍAS EN SERVIDORES")
print("=" * 70)

print()

print(f"Estado inicial: {START}")
print(f"Meta: {GOAL}")

print()

if path:

    print("Ruta encontrada:")

    for position, server in enumerate(
        path,
        start=1
    ):
        print(
            f"{position}. {server}"
        )

    print()

    print(
        f"Costo total: {total_cost}"
    )

else:

    print(
        "No existe una ruta válida."
    )


# ============================================================
# GENERAR REPORTE SEMANA 04
# ============================================================

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


report = []

report.append(
    "# Semana 04 - Búsqueda y toma de decisiones"
)

report.append("")

report.append(
    "## Proyecto: Detección de anomalías en servidores"
)

report.append("")

report.append(
    "Durante la Semana 04 se aplican algoritmos clásicos "
    "de inteligencia artificial relacionados con búsqueda, "
    "heurísticas y toma de decisiones."
)

report.append("")

report.append(
    "Los ejercicios se adaptan al proyecto de detección "
    "de anomalías en servidores con el propósito de integrar "
    "los conceptos vistos en clase con un escenario de "
    "infraestructura tecnológica."
)

report.append("")

report.append("---")

report.append("")

report.append(
    "## 1. Búsqueda A*"
)

report.append("")

report.append(
    "El algoritmo A* se utiliza para encontrar una ruta "
    "de menor costo entre servidores dentro de una red."
)

report.append("")

report.append(
    "### Componentes del problema"
)

report.append("")

report.append(
    f"- **Estado inicial:** {START}"
)

report.append(
    f"- **Meta:** {GOAL}"
)

report.append(
    "- **Acción:** desplazarse desde un servidor hacia "
    "otro servidor conectado."
)

report.append(
    "- **Costo:** valor asociado a cada transición "
    "entre servidores."
)

report.append(
    "- **Heurística:** estimación del costo restante "
    "hasta alcanzar el servidor objetivo."
)

report.append("")

report.append(
    "### Resultado"
)

report.append("")

if path:

    report.append(
        "**Ruta encontrada:** "
        + " → ".join(path)
    )

    report.append("")

    report.append(
        f"**Costo total:** {total_cost}"
    )

else:

    report.append(
        "No se encontró una ruta válida."
    )

report.append("")

report.append(
    "### Relación con el proyecto"
)

report.append("")

report.append(
    "Dentro del sistema de detección de anomalías, A* "
    "puede representar un mecanismo de planificación para "
    "buscar una ruta alternativa de atención o recuperación "
    "cuando uno de los servidores presenta una falla."
)

report.append("")

report.append(
    "<!-- FIN_ASTAR -->"
)

report.append("")


REPORT_FILE.write_text(
    "\n".join(report),
    encoding="utf-8"
)


print()

print(
    f"Reporte A* generado: {REPORT_FILE}"
)