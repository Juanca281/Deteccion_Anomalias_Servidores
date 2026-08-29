import heapq
from copy import deepcopy
from pathlib import Path


# ============================================================
# CONFIGURACIÓN DEL PROYECTO
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"
REPORT_FILE = REPORTS_DIR / "semana04.md"

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


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
    hasta el servidor de recuperación.
    """

    if node == goal:
        return 0

    return HEURISTIC.get(node, 0)


# ============================================================
# ALGORITMO A*
# ============================================================

def astar(network, start, goal):
    """
    Busca una ruta de menor costo utilizando:

        f(n) = g(n) + h(n)

    g(n): costo acumulado.
    h(n): estimación del costo restante.
    """

    frontier = [
        (h(start, goal), start)
    ]

    came_from = {
        start: None
    }

    cost = {
        start: 0
    }

    explored = []

    while frontier:

        _, current = heapq.heappop(frontier)

        if current in explored:
            continue

        explored.append(current)

        if current == goal:
            break

        for next_node, transition_cost in network.get(
            current,
            {}
        ).items():

            new_cost = (
                cost[current]
                + transition_cost
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
        return None, None, explored

    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = came_from[current]

    path.reverse()

    return (
        path,
        cost[goal],
        explored
    )


# ============================================================
# CASOS DE PRUEBA
# ============================================================

test_cases = []


# ------------------------------------------------------------
# CASO 1
# ------------------------------------------------------------

path_1, cost_1, explored_1 = astar(
    NETWORK,
    "Servidor-Web",
    "Servidor-Recuperacion"
)

test_cases.append(
    {
        "name": "Caso 1 - Ruta desde Servidor-Web",
        "start": "Servidor-Web",
        "goal": "Servidor-Recuperacion",
        "path": path_1,
        "cost": cost_1,
        "explored": explored_1,
        "expected": 9,
        "explanation": (
            "El algoritmo debe encontrar una ruta cuyo costo "
            "total sea 9. Aunque existe una conexión directa "
            "hacia el servidor de respaldo con costo 10, "
            "existen alternativas de menor costo pasando "
            "por otros servidores."
        ),
    }
)


# ------------------------------------------------------------
# CASO 2
# ------------------------------------------------------------

path_2, cost_2, explored_2 = astar(
    NETWORK,
    "Servidor-App",
    "Servidor-Recuperacion"
)

test_cases.append(
    {
        "name": "Caso 2 - Ruta desde Servidor-App",
        "start": "Servidor-App",
        "goal": "Servidor-Recuperacion",
        "path": path_2,
        "cost": cost_2,
        "explored": explored_2,
        "expected": 7,
        "explanation": (
            "Al iniciar desde Servidor-App se reduce el costo "
            "de recuperación. A* debe encontrar una alternativa "
            "con costo total 7."
        ),
    }
)


# ------------------------------------------------------------
# CASO 3
# ------------------------------------------------------------

modified_network = deepcopy(
    NETWORK
)

# Se simula una degradación del enlace entre
# monitoreo y recuperación.
modified_network[
    "Servidor-Monitoreo"
][
    "Servidor-Recuperacion"
] = 10


path_3, cost_3, explored_3 = astar(
    modified_network,
    "Servidor-Web",
    "Servidor-Recuperacion"
)

test_cases.append(
    {
        "name": "Caso 3 - Cambio de costo en la red",
        "start": "Servidor-Web",
        "goal": "Servidor-Recuperacion",
        "path": path_3,
        "cost": cost_3,
        "explored": explored_3,
        "expected": 9,
        "explanation": (
            "Se incrementa el costo entre Servidor-Monitoreo "
            "y Servidor-Recuperacion. El algoritmo debe adaptar "
            "la ruta y evitar esa conexión cuando exista una "
            "alternativa de menor costo."
        ),
    }
)


# ============================================================
# MOSTRAR RESULTADOS
# ============================================================

print("=" * 70)
print("SEMANA 04 - ALGORITMO A*")
print("PROYECTO: DETECCIÓN DE ANOMALÍAS EN SERVIDORES")
print("=" * 70)


for number, case in enumerate(
    test_cases,
    start=1
):

    print()
    print("-" * 70)

    print(
        f"CASO DE PRUEBA {number}"
    )

    print("-" * 70)

    print(
        f"Estado inicial: {case['start']}"
    )

    print(
        f"Meta: {case['goal']}"
    )

    print()

    if case["path"]:

        print(
            "Ruta encontrada:"
        )

        print(
            " -> ".join(case["path"])
        )

        print(
            f"Costo total: {case['cost']}"
        )

        print(
            "Estados explorados:"
        )

        print(
            " -> ".join(case["explored"])
        )

    else:

        print(
            "No se encontró una ruta."
        )

    print(
        f"Resultado esperado: costo {case['expected']}"
    )

    if case["cost"] == case["expected"]:

        print(
            "Validación: CORRECTA"
        )

    else:

        print(
            "Validación: REVISAR"
        )


# ============================================================
# GENERAR CONTENIDO DEL REPORTE
# ============================================================

astar_report = []

astar_report.append(
    "<!-- INICIO_ASTAR -->"
)

astar_report.append("")

astar_report.append(
    "## A. Descripción del problema"
)

astar_report.append("")

astar_report.append(
    "Dentro del proyecto de detección de anomalías en "
    "servidores se plantea un escenario en el que, después "
    "de identificar una falla o condición anómala, es "
    "necesario determinar una ruta de menor costo hacia "
    "un servidor o recurso de recuperación."
)

astar_report.append("")

astar_report.append(
    "Para representar este problema se utiliza una red "
    "de servidores conectados. Cada conexión tiene un costo "
    "que puede representar tiempo de respuesta, consumo de "
    "recursos, complejidad operativa o impacto de utilizar "
    "esa transición."
)

astar_report.append("")

astar_report.append(
    "A* es pertinente porque permite combinar el costo "
    "acumulado de una ruta con una estimación del costo "
    "restante hasta la meta."
)

astar_report.append("")

astar_report.append(
    "La función utilizada es:"
)

astar_report.append("")

astar_report.append(
    "**f(n) = g(n) + h(n)**"
)

astar_report.append("")

astar_report.append(
    "donde **g(n)** representa el costo acumulado y "
    "**h(n)** la estimación del costo restante."
)

astar_report.append("")

astar_report.append(
    "## B. Representación del problema"
)

astar_report.append("")

astar_report.append(
    "- **Estado inicial:** servidor desde el cual comienza "
    "el proceso de recuperación."
)

astar_report.append(
    "- **Estados posibles:** servidores que forman parte "
    "de la infraestructura modelada."
)

astar_report.append(
    "- **Acciones u operadores:** desplazarse desde un "
    "servidor hacia otro servidor conectado."
)

astar_report.append(
    "- **Transiciones:** conexiones disponibles entre "
    "los servidores."
)

astar_report.append(
    "- **Sucesores:** servidores directamente accesibles "
    "desde el estado actual."
)

astar_report.append(
    "- **Meta:** alcanzar el Servidor-Recuperacion."
)

astar_report.append(
    "- **Costo de camino:** suma de los costos asociados "
    "a todas las conexiones utilizadas."
)

astar_report.append(
    "- **Heurística:** estimación del costo restante desde "
    "cada servidor hasta el servidor de recuperación."
)

astar_report.append(
    "- **Criterio de selección:** escoger los estados "
    "utilizando el menor valor de f(n) = g(n) + h(n)."
)

astar_report.append("")

astar_report.append(
    "### Estados y sucesores"
)

astar_report.append("")

for server, successors in NETWORK.items():

    formatted_successors = ", ".join(
        f"{destination} (costo {cost})"
        for destination, cost in successors.items()
    )

    astar_report.append(
        f"- **{server}:** {formatted_successors}"
    )


astar_report.append("")

astar_report.append(
    "## C. Implementación"
)

astar_report.append("")

astar_report.append(
    "El algoritmo A* fue implementado en "
    "`src/semana04_astar.py`."
)

astar_report.append("")

astar_report.append(
    "Se utiliza una cola de prioridad para seleccionar "
    "el siguiente servidor a explorar. Para cada sucesor "
    "se calcula el nuevo costo acumulado g(n) y se suma "
    "la heurística h(n). El resultado determina la prioridad "
    "con la que el estado será explorado."
)

astar_report.append("")

astar_report.append(
    "## D. Resultados y pruebas"
)

astar_report.append("")


for number, case in enumerate(
    test_cases,
    start=1
):

    astar_report.append(
        f"### Caso de prueba {number}"
    )

    astar_report.append("")

    astar_report.append(
        f"**Configuración inicial:** {case['start']} → "
        f"{case['goal']}"
    )

    astar_report.append("")

    if number == 3:

        astar_report.append(
            "**Modificación:** el costo entre "
            "Servidor-Monitoreo y Servidor-Recuperacion "
            "se incrementó de 2 a 10."
        )

        astar_report.append("")

    if case["path"]:

        astar_report.append(
            "**Ruta obtenida:** "
            + " → ".join(case["path"])
        )

        astar_report.append("")

        astar_report.append(
            f"**Costo obtenido:** {case['cost']}"
        )

        astar_report.append("")

        astar_report.append(
            "**Estados explorados:** "
            + " → ".join(case["explored"])
        )

    else:

        astar_report.append(
            "No se encontró una ruta válida."
        )

    astar_report.append("")

    astar_report.append(
        f"**Resultado esperado:** costo {case['expected']}"
    )

    astar_report.append("")

    astar_report.append(
        "**Comparación:** "
        + (
            "el resultado obtenido coincide con el esperado."
            if case["cost"] == case["expected"]
            else "el resultado no coincide con el esperado."
        )
    )

    astar_report.append("")

    astar_report.append(
        f"**Explicación:** {case['explanation']}"
    )

    astar_report.append("")


astar_report.append(
    "## E. Análisis"
)

astar_report.append("")

astar_report.append(
    "### Ventajas"
)

astar_report.append("")

astar_report.append(
    "- A* permite considerar simultáneamente el costo "
    "recorrido y una estimación del costo pendiente."
)

astar_report.append(
    "- Puede adaptarse cuando cambian los costos de "
    "las conexiones entre servidores."
)

astar_report.append(
    "- Permite modelar decisiones de planificación "
    "posteriores a la detección de una anomalía."
)

astar_report.append("")

astar_report.append(
    "### Limitaciones"
)

astar_report.append("")

astar_report.append(
    "- Los costos utilizados son valores definidos para "
    "la práctica y no corresponden todavía a mediciones "
    "obtenidas directamente de servidores reales."
)

astar_report.append(
    "- La calidad de A* depende de la heurística utilizada."
)

astar_report.append(
    "- Una infraestructura con gran cantidad de servidores "
    "puede aumentar el número de estados y el uso de memoria."
)

astar_report.append("")

astar_report.append(
    "### Supuestos"
)

astar_report.append("")

astar_report.append(
    "- Se supone que las conexiones conocidas se encuentran "
    "disponibles durante cada ejecución."
)

astar_report.append(
    "- Los costos son valores positivos."
)

astar_report.append(
    "- La meta de los casos evaluados es alcanzar un "
    "servidor de recuperación."
)

astar_report.append("")

astar_report.append(
    "### Posibles mejoras"
)

astar_report.append("")

astar_report.append(
    "- Obtener costos automáticamente a partir de métricas "
    "reales como latencia, disponibilidad o carga."
)

astar_report.append(
    "- Modificar dinámicamente la red cuando un servidor "
    "sea identificado como no disponible."
)

astar_report.append(
    "- Integrar el resultado de A* con el módulo que detecte "
    "las anomalías en etapas posteriores del proyecto."
)

astar_report.append("")

astar_report.append(
    "<!-- FIN_ASTAR -->"
)


# ============================================================
# ACTUALIZAR REPORTE SIN BORRAR MINIMAX
# ============================================================

HEADER = """# Semana 04 - Marco tecnológico de la Inteligencia Artificial

## Proyecto: Detección de anomalías en servidores

La Semana 04 integra técnicas de búsqueda, heurísticas y
juegos dentro del repositorio acumulativo del proyecto.

"""


def update_section(
    file_path,
    start_marker,
    end_marker,
    new_content
):

    if file_path.exists():

        content = file_path.read_text(
            encoding="utf-8"
        )

    else:

        content = HEADER

    if (
        start_marker in content
        and end_marker in content
    ):

        before = content.split(
            start_marker
        )[0]

        after = content.split(
            end_marker,
            1
        )[1]

        content = (
            before
            + new_content
            + after
        )

    else:

        content = (
            content.rstrip()
            + "\n\n"
            + new_content
            + "\n"
        )

    file_path.write_text(
        content,
        encoding="utf-8"
    )


update_section(
    REPORT_FILE,
    "<!-- INICIO_ASTAR -->",
    "<!-- FIN_ASTAR -->",
    "\n".join(astar_report)
)


print()
print("=" * 70)
print(
    f"Reporte actualizado: {REPORT_FILE}"
)
print("=" * 70)