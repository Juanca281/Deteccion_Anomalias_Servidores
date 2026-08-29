from pathlib import Path


# ============================================================
# CONFIGURACIÓN
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"
REPORT_FILE = REPORTS_DIR / "semana04.md"

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# CONFIGURACIÓN DEL JUEGO
# ============================================================

WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


# ============================================================
# GANADOR
# ============================================================

def winner(board):

    for a, b, c in WIN_LINES:

        if (
            board[a] == board[b]
            and board[b] == board[c]
            and board[a] != " "
        ):
            return board[a]

    return None


# ============================================================
# ESTADO TERMINAL
# ============================================================

def terminal(board):

    return (
        winner(board) is not None
        or " " not in board
    )


# ============================================================
# FUNCIÓN DE UTILIDAD
# ============================================================

def utility(board):

    result = winner(board)

    if result == "X":
        return 1

    if result == "O":
        return -1

    return 0


# ============================================================
# MINIMAX
# ============================================================

def minimax(board, maximizing, counter):

    counter["nodes"] += 1

    if terminal(board):
        return utility(board)

    scores = []

    if maximizing:
        mark = "X"
    else:
        mark = "O"

    for index, cell in enumerate(board):

        if cell == " ":

            next_board = board.copy()

            next_board[index] = mark

            score = minimax(
                next_board,
                not maximizing,
                counter
            )

            scores.append(score)

    if maximizing:
        return max(scores)

    return min(scores)


# ============================================================
# MEJOR JUGADA
# ============================================================

def best_move(board):

    choices = []

    counter = {
        "nodes": 0
    }

    for index, cell in enumerate(board):

        if cell == " ":

            next_board = board.copy()

            next_board[index] = "X"

            score = minimax(
                next_board,
                False,
                counter
            )

            choices.append(
                (score, index)
            )

    if not choices:
        return None, None, counter["nodes"]

    best_score = max(
        score
        for score, index in choices
    )

    for score, index in choices:

        if score == best_score:

            return (
                index,
                score,
                counter["nodes"]
            )


# ============================================================
# MINIMAX CON PODA ALFA-BETA
# ============================================================

def minimax_alpha_beta(
    board,
    maximizing,
    alpha,
    beta,
    counter
):

    counter["nodes"] += 1

    if terminal(board):
        return utility(board)

    if maximizing:

        value = float("-inf")

        for index, cell in enumerate(board):

            if cell == " ":

                next_board = board.copy()

                next_board[index] = "X"

                value = max(
                    value,
                    minimax_alpha_beta(
                        next_board,
                        False,
                        alpha,
                        beta,
                        counter
                    )
                )

                alpha = max(
                    alpha,
                    value
                )

                if alpha >= beta:
                    break

        return value

    else:

        value = float("inf")

        for index, cell in enumerate(board):

            if cell == " ":

                next_board = board.copy()

                next_board[index] = "O"

                value = min(
                    value,
                    minimax_alpha_beta(
                        next_board,
                        True,
                        alpha,
                        beta,
                        counter
                    )
                )

                beta = min(
                    beta,
                    value
                )

                if alpha >= beta:
                    break

        return value


# ============================================================
# MEJOR JUGADA CON ALFA-BETA
# ============================================================

def best_move_alpha_beta(board):

    choices = []

    counter = {
        "nodes": 0
    }

    alpha = float("-inf")
    beta = float("inf")

    for index, cell in enumerate(board):

        if cell == " ":

            next_board = board.copy()

            next_board[index] = "X"

            score = minimax_alpha_beta(
                next_board,
                False,
                alpha,
                beta,
                counter
            )

            choices.append(
                (score, index)
            )

            alpha = max(
                alpha,
                score
            )

    if not choices:
        return None, None, counter["nodes"]

    best_score = max(
        score
        for score, index in choices
    )

    for score, index in choices:

        if score == best_score:

            return (
                index,
                score,
                counter["nodes"]
            )


# ============================================================
# MOSTRAR TABLERO
# ============================================================

def board_text(board):

    values = []

    for index, cell in enumerate(board):

        if cell == " ":
            values.append(
                str(index + 1)
            )

        else:
            values.append(cell)

    return (
        f"{values[0]} | {values[1]} | {values[2]}\n"
        f"--+---+--\n"
        f"{values[3]} | {values[4]} | {values[5]}\n"
        f"--+---+--\n"
        f"{values[6]} | {values[7]} | {values[8]}"
    )


# ============================================================
# CASOS DE PRUEBA
# ============================================================

TEST_CASES = [

    {
        "name": "Caso 1 - Jugada ganadora",
        "board": [
            "X", "O", "X",
            "O", "X", " ",
            " ", " ", "O",
        ],
        "explanation": (
            "MAX puede ganar colocando X en la posición 7, "
            "completando la diagonal."
        ),
    },

    {
        "name": "Caso 2 - Análisis de respuesta de MIN",
        "board": [
            "X", "O", " ",
            " ", "O", " ",
            "X", " ", " ",
        ],
        "explanation": (
            "MAX debe considerar las respuestas futuras de MIN "
            "y seleccionar la jugada que produzca la mejor "
            "utilidad posible frente a un adversario racional."
        ),
    },

    {
        "name": "Caso 3 - Estado avanzado",
        "board": [
            "X", "O", "X",
            "X", "O", " ",
            "O", "X", " ",
        ],
        "explanation": (
            "El tablero tiene pocas posiciones disponibles, "
            "por lo que Minimax puede evaluar todas las "
            "alternativas restantes."
        ),
    },
]


# ============================================================
# EJECUCIÓN DE PRUEBAS
# ============================================================

results = []

print("=" * 70)
print("SEMANA 04 - MINIMAX")
print("PRÁCTICA DE JUEGOS ADVERSARIALES")
print("=" * 70)


for number, case in enumerate(
    TEST_CASES,
    start=1
):

    board = case["board"]

    move, score, nodes = best_move(
        board
    )

    (
        move_ab,
        score_ab,
        nodes_ab
    ) = best_move_alpha_beta(
        board
    )

    results.append(
        {
            "name": case["name"],
            "board": board,
            "explanation": case["explanation"],
            "move": move,
            "score": score,
            "nodes": nodes,
            "move_ab": move_ab,
            "score_ab": score_ab,
            "nodes_ab": nodes_ab,
        }
    )

    print()

    print(
        f"CASO {number}"
    )

    print(
        "-" * 70
    )

    print(
        board_text(board)
    )

    print()

    print(
        f"Mejor jugada Minimax: posición {move + 1}"
    )

    print(
        f"Utilidad: {score}"
    )

    print(
        f"Nodos evaluados Minimax: {nodes}"
    )

    print(
        f"Nodos evaluados Alfa-Beta: {nodes_ab}"
    )

    print(
        f"Jugada Alfa-Beta: posición {move_ab + 1}"
    )


# ============================================================
# CREAR TEXTO DEL REPORTE
# ============================================================

report = []

report.append(
    "<!-- INICIO_MINIMAX -->"
)

report.append("")

report.append(
    "## F. Minimax y juegos adversariales"
)

report.append("")

report.append(
    "### Aplicabilidad al proyecto"
)

report.append("")

report.append(
    "El proyecto de detección de anomalías en servidores "
    "no constituye directamente un problema adversarial."
)

report.append("")

report.append(
    "Una anomalía, una sobrecarga o una falla de hardware "
    "no representan un agente racional que tome decisiones "
    "con el propósito de perjudicar al sistema."
)

report.append("")

report.append(
    "Por esta razón, Minimax no se aplica directamente "
    "como algoritmo principal del proyecto. Para cumplir "
    "con la práctica de la Semana 04 se implementa el "
    "ejemplo de referencia mediante el juego de tres en línea."
)

report.append("")

report.append(
    "### Diferencia entre A* y Minimax"
)

report.append("")

report.append(
    "A* corresponde a un problema de búsqueda. Explora "
    "estados utilizando costos y una heurística hasta "
    "alcanzar una meta."
)

report.append("")

report.append(
    "Minimax corresponde a un problema adversarial. "
    "MAX intenta maximizar el resultado mientras que "
    "MIN intenta minimizarlo."
)

report.append("")

report.append(
    "## G. Representación del problema Minimax"
)

report.append("")

report.append(
    "- **Estado:** configuración actual del tablero."
)

report.append(
    "- **Acciones:** posiciones vacías disponibles."
)

report.append(
    "- **Jugador MAX:** X."
)

report.append(
    "- **Jugador MIN:** O."
)

report.append(
    "- **Estado terminal:** victoria de X, victoria de O o empate."
)

report.append(
    "- **Utilidad si gana X:** +1."
)

report.append(
    "- **Utilidad si gana O:** -1."
)

report.append(
    "- **Utilidad en empate:** 0."
)

report.append("")

report.append(
    "## H. Implementación"
)

report.append("")

report.append(
    "El algoritmo se encuentra implementado en "
    "`src/semana04_minimax.py`."
)

report.append("")

report.append(
    "Minimax genera los posibles estados sucesores del "
    "tablero de forma recursiva. Cuando juega MAX selecciona "
    "la mayor utilidad disponible y cuando juega MIN "
    "selecciona la menor."
)

report.append("")

report.append(
    "De esta manera se supone que ambos jugadores actúan "
    "racionalmente."
)

report.append("")

report.append(
    "## I. Resultados y casos de prueba"
)

report.append("")


for number, result in enumerate(
    results,
    start=1
):

    report.append(
        f"### Caso Minimax {number}"
    )

    report.append("")

    report.append(
        f"**Escenario:** {result['name']}"
    )

    report.append("")

    report.append(
        "```text"
    )

    report.append(
        board_text(
            result["board"]
        )
    )

    report.append(
        "```"
    )

    report.append("")

    report.append(
        f"**Mejor jugada:** posición "
        f"{result['move'] + 1}"
    )

    report.append("")

    report.append(
        f"**Utilidad:** {result['score']}"
    )

    report.append("")

    report.append(
        f"**Nodos evaluados por Minimax:** "
        f"{result['nodes']}"
    )

    report.append("")

    report.append(
        f"**Nodos evaluados con poda alfa-beta:** "
        f"{result['nodes_ab']}"
    )

    report.append("")

    report.append(
        f"**Resultado alfa-beta:** posición "
        f"{result['move_ab'] + 1}"
    )

    report.append("")

    report.append(
        f"**Explicación:** "
        f"{result['explanation']}"
    )

    report.append("")

    if (
        result["move"] == result["move_ab"]
        and result["score"] == result["score_ab"]
    ):

        report.append(
            "**Comparación:** Minimax y alfa-beta "
            "obtuvieron la misma decisión."
        )

    else:

        report.append(
            "**Comparación:** los resultados deben revisarse."
        )

    report.append("")


# ============================================================
# PODA ALFA-BETA
# ============================================================

report.append(
    "## J. Poda alfa-beta"
)

report.append("")

report.append(
    "La poda alfa-beta optimiza Minimax evitando explorar "
    "ramas que ya no pueden modificar la decisión final."
)

report.append("")

report.append(
    "Alfa representa el mejor resultado conocido para MAX "
    "y beta representa el mejor resultado conocido para MIN."
)

report.append("")

report.append(
    "Cuando alfa es mayor o igual que beta, una rama puede "
    "descartarse porque continuar evaluándola no cambiará "
    "la decisión final."
)

report.append("")

report.append(
    "Esto permite reducir el número de estados evaluados "
    "manteniendo la misma decisión que Minimax."
)

report.append("")

report.append(
    "## K. Análisis"
)

report.append("")

report.append(
    "### Ventajas"
)

report.append("")

report.append(
    "- Permite analizar decisiones frente a un adversario racional."
)

report.append(
    "- Considera posibles respuestas futuras antes de decidir."
)

report.append(
    "- La poda alfa-beta reduce estados innecesarios."
)

report.append("")

report.append(
    "### Limitaciones"
)

report.append("")

report.append(
    "- El número de estados puede crecer rápidamente."
)

report.append(
    "- Requiere un escenario con objetivos opuestos."
)

report.append(
    "- No representa naturalmente una anomalía de servidor."
)

report.append("")

report.append(
    "### Supuestos"
)

report.append("")

report.append(
    "- MAX y MIN actúan racionalmente."
)

report.append(
    "- Ambos jugadores conocen las reglas."
)

report.append(
    "- Cada jugador selecciona la decisión que más favorece su objetivo."
)

report.append("")

report.append(
    "### Posibles mejoras"
)

report.append("")

report.append(
    "- Utilizar funciones de evaluación para árboles más grandes."
)

report.append(
    "- Aplicar límites de profundidad."
)

report.append(
    "- Utilizar poda alfa-beta en problemas con mayor cantidad de estados."
)

report.append("")

report.append(
    "## Conclusión de Minimax"
)

report.append("")

report.append(
    "Minimax permitió comprender la diferencia entre un "
    "problema de búsqueda y un problema adversarial."
)

report.append("")

report.append(
    "En el proyecto, A* se utiliza directamente para la "
    "planificación de rutas de recuperación, mientras que "
    "Minimax se desarrolla como práctica de referencia "
    "porque las anomalías de servidores no constituyen "
    "adversarios racionales."
)

report.append("")

report.append(
    "<!-- FIN_MINIMAX -->"
)


# ============================================================
# ESCRIBIR EL REPORTE
# ============================================================

minimax_content = "\n".join(
    report
)

START_MARKER = "<!-- INICIO_MINIMAX -->"
END_MARKER = "<!-- FIN_MINIMAX -->"


if REPORT_FILE.exists():

    current_content = REPORT_FILE.read_text(
        encoding="utf-8"
    )

else:

    current_content = (
        "# Semana 04 - Marco tecnológico "
        "de la Inteligencia Artificial\n\n"
        "## Proyecto: Detección de anomalías en servidores\n"
    )


if (
    START_MARKER in current_content
    and END_MARKER in current_content
):

    before = current_content.split(
        START_MARKER,
        1
    )[0]

    after = current_content.split(
        END_MARKER,
        1
    )[1]

    final_content = (
        before.rstrip()
        + "\n\n"
        + minimax_content
        + after
    )

else:

    final_content = (
        current_content.rstrip()
        + "\n\n"
        + minimax_content
        + "\n"
    )


REPORT_FILE.write_text(
    final_content,
    encoding="utf-8"
)


# ============================================================
# VERIFICACIÓN FINAL
# ============================================================

print()
print("=" * 70)
print("REPORTE GENERADO")
print("=" * 70)

print(
    f"Ruta exacta: {REPORT_FILE.resolve()}"
)

print(
    f"¿El archivo existe?: {REPORT_FILE.exists()}"
)

print(
    f"Tamaño del archivo: "
    f"{REPORT_FILE.stat().st_size} bytes"
)

print()
print(
    "Minimax fue agregado a semana04.md sin borrar A*."
)