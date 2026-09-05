from pathlib import Path
import unicodedata

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import make_pipeline


# ============================================================
# CONFIGURACIÓN DEL PROYECTO
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"

KB_PATH = DATA_DIR / "base_conocimiento.txt"
REPORT_PATH = REPORTS_DIR / "semana05.md"


# ============================================================
# PROCESAMIENTO BÁSICO DE LENGUAJE NATURAL
# ============================================================

def normalize_text(text: str) -> str:
    """
    Convierte el texto a minúsculas y elimina tildes.

    Esto permite comparar palabras de una manera
    más uniforme.
    """

    text = text.lower().strip()

    text = unicodedata.normalize(
        "NFD",
        text
    )

    return "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )


# ============================================================
# SISTEMA EXPERTO
# 5 REGLAS PROPIAS
# ============================================================

RULES = [

    # --------------------------------------------------------
    # REGLA 1
    # --------------------------------------------------------

    {
        "id": "R1",
        "name": "revisar_rendimiento",

        "keywords": [
            "cpu",
            "memoria",
            "lento",
            "lentitud",
            "recursos",
        ],

        "action": (
            "Revisar consumo de CPU, memoria "
            "y procesos activos."
        ),
    },

    # --------------------------------------------------------
    # REGLA 2
    # --------------------------------------------------------

    {
        "id": "R2",
        "name": "revisar_conectividad",

        "keywords": [
            "dns",
            "red",
            "conectividad",
            "latencia",
            "paquetes",
        ],

        "action": (
            "Validar DNS, enlace de red, puerta de enlace "
            "y comunicación entre servidores."
        ),
    },

    # --------------------------------------------------------
    # REGLA 3
    # --------------------------------------------------------

    {
        "id": "R3",
        "name": "revisar_almacenamiento",

        "keywords": [
            "disco",
            "espacio",
            "almacenamiento",
            "logs",
            "registros",
        ],

        "action": (
            "Revisar uso de disco, crecimiento de logs "
            "y espacio disponible."
        ),
    },

    # --------------------------------------------------------
    # REGLA 4
    # --------------------------------------------------------

    {
        "id": "R4",
        "name": "revisar_seguridad",

        "keywords": [
            "bloqueado",
            "credenciales",
            "acceso",
            "sesion",
            "denegado",
        ],

        "action": (
            "Revisar credenciales, bloqueos "
            "e intentos fallidos de acceso."
        ),
    },

    # --------------------------------------------------------
    # REGLA 5
    # --------------------------------------------------------

    {
        "id": "R5",
        "name": "revisar_disponibilidad",

        "keywords": [
            "caido",
            "no responde",
            "indisponible",
            "reinicia",
            "detenido",
        ],

        "action": (
            "Validar servicios, puertos, dependencias "
            "y eventos recientes del servidor."
        ),
    },
]


# ============================================================
# EJEMPLOS DE ENTRENAMIENTO
# 15 EJEMPLOS ETIQUETADOS
# ============================================================

TRAIN_X = [

    # --------------------------------------------------------
    # RENDIMIENTO
    # --------------------------------------------------------

    "servidor lento con cpu alta",

    "uso de memoria elevado y respuesta lenta",

    "procesos consumen demasiados recursos del servidor",


    # --------------------------------------------------------
    # RED
    # --------------------------------------------------------

    "servidor no resuelve dns",

    "hay perdida de conectividad entre servidores",

    "latencia alta en la red del servidor",


    # --------------------------------------------------------
    # ALMACENAMIENTO
    # --------------------------------------------------------

    "disco del servidor casi lleno",

    "no hay espacio para guardar registros",

    "almacenamiento supera el noventa por ciento",


    # --------------------------------------------------------
    # SEGURIDAD
    # --------------------------------------------------------

    "usuario bloqueado al ingresar al servidor",

    "intentos fallidos de inicio de sesion",

    "credenciales rechazadas y acceso denegado",


    # --------------------------------------------------------
    # DISPONIBILIDAD
    # --------------------------------------------------------

    "servidor no responde a las solicitudes",

    "servicio principal esta caido",

    "servidor se reinicia y queda indisponible",
]


# ============================================================
# CATEGORÍAS
# ============================================================

TRAIN_Y = [

    "rendimiento",
    "rendimiento",
    "rendimiento",

    "red",
    "red",
    "red",

    "almacenamiento",
    "almacenamiento",
    "almacenamiento",

    "seguridad",
    "seguridad",
    "seguridad",

    "disponibilidad",
    "disponibilidad",
    "disponibilidad",
]


# ============================================================
# 3 CONSULTAS DE PRUEBA
# ============================================================

TEST_QUERIES = [

    (
        "El servidor de aplicaciones está muy lento "
        "y presenta consumo alto de CPU y memoria."
    ),

    (
        "El servidor web no resuelve nombres DNS "
        "y presenta pérdida de conectividad."
    ),

    (
        "El servidor de base de datos tiene el disco "
        "casi lleno y no puede guardar registros."
    ),
]


# ============================================================
# CARGAR BASE DE CONOCIMIENTO
# ============================================================

def load_documents() -> list[str]:
    """
    Lee data/base_conocimiento.txt.

    También verifica que existan como mínimo
    8 entradas.
    """

    if not KB_PATH.exists():

        raise FileNotFoundError(
            "No existe data/base_conocimiento.txt. "
            "Créalo antes de ejecutar Semana 5."
        )

    docs = [

        line.strip()

        for line in KB_PATH.read_text(
            encoding="utf-8"
        ).splitlines()

        if line.strip()
    ]

    if len(docs) < 8:

        raise ValueError(
            "data/base_conocimiento.txt debe contener "
            "al menos 8 entradas."
        )

    return docs


# ============================================================
# APLICAR REGLAS DEL SISTEMA EXPERTO
# ============================================================

def apply_rules(query: str) -> list[dict]:
    """
    Revisa qué reglas coinciden con las palabras
    presentes en la consulta.
    """

    q = normalize_text(query)

    fired = []

    for rule in RULES:

        matches = [

            keyword

            for keyword in rule["keywords"]

            if keyword in q
        ]

        if matches:

            fired.append(
                {
                    "id": rule["id"],
                    "name": rule["name"],
                    "action": rule["action"],
                    "matches": matches,
                }
            )

    return fired


# ============================================================
# RECUPERACIÓN DE INFORMACIÓN
# TF-IDF
# ============================================================

def build_retriever(documents: list[str]):
    """
    Convierte la base de conocimiento
    en vectores TF-IDF.
    """

    vectorizer = TfidfVectorizer(
        strip_accents="unicode",
        lowercase=True,
    )

    matrix = vectorizer.fit_transform(
        documents
    )

    return vectorizer, matrix


# ============================================================
# CLASIFICADOR
# ============================================================

def build_classifier():
    """
    Construye un clasificador de texto utilizando
    TF-IDF y Regresión Logística.
    """

    classifier = make_pipeline(

        TfidfVectorizer(
            strip_accents="unicode",
            lowercase=True,
            ngram_range=(1, 2),
        ),

        LogisticRegression(
            max_iter=1000,
            random_state=42,
        ),
    )

    classifier.fit(
        TRAIN_X,
        TRAIN_Y
    )

    return classifier


# ============================================================
# SISTEMA HÍBRIDO
# ============================================================

def answer(
    query: str,
    documents: list[str],
    vectorizer,
    doc_matrix,
    classifier,
) -> dict:

    # --------------------------------------------------------
    # 1. SISTEMA EXPERTO
    # --------------------------------------------------------

    fired_rules = apply_rules(
        query
    )


    # --------------------------------------------------------
    # 2. RECUPERACIÓN DE INFORMACIÓN
    # --------------------------------------------------------

    similarities = cosine_similarity(

        vectorizer.transform(
            [query]
        ),

        doc_matrix,

    )[0]


    best_index = int(
        similarities.argmax()
    )


    # --------------------------------------------------------
    # 3. CLASIFICACIÓN
    # --------------------------------------------------------

    predicted_class = str(

        classifier.predict(
            [query]
        )[0]

    )


    # --------------------------------------------------------
    # 4. RESULTADO TRAZABLE
    # --------------------------------------------------------

    return {

        "reglas": fired_rules,

        "evidencia": documents[
            best_index
        ],

        "similitud": float(
            similarities[best_index]
        ),

        "clase": predicted_class,
    }


# ============================================================
# GENERAR REPORTS/SEMANA05.MD
# ============================================================

def write_report(
    rows: list[tuple[str, dict]]
) -> None:

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    lines = [

        "# Semana 05 - Sistema híbrido",

        "",

        "## Proyecto: Detección de anomalías en servidores",

        "",

        (
            "El sistema combina reglas expertas, "
            "recuperación de información con TF-IDF "
            "y similitud coseno, clasificación de texto "
            "y procesamiento básico de lenguaje natural."
        ),

        "",

        "## Configuración",

        "",

        (
            f"- Entradas en la base de conocimiento: "
            f"{len(DOCUMENTS)}"
        ),

        (
            f"- Reglas expertas: "
            f"{len(RULES)}"
        ),

        (
            f"- Ejemplos etiquetados: "
            f"{len(TRAIN_X)}"
        ),

        (
            "- Categorías: "
            + ", ".join(
                sorted(
                    set(TRAIN_Y)
                )
            )
        ),

        "",

        "## Pruebas",

        "",

        (
            "| # | Consulta | Regla activada | "
            "Evidencia recuperada | Similitud | "
            "Clasificación |"
        ),

        (
            "|---|---|---|---|---:|---|"
        ),
    ]


    # ========================================================
    # TABLA DE RESULTADOS
    # ========================================================

    for index, (
        query,
        result
    ) in enumerate(
        rows,
        start=1
    ):

        rule_names = ", ".join(

            (
                f"{rule['id']} - "
                f"{rule['name']}"
            )

            for rule in result["reglas"]

        ) or "ninguna"


        lines.append(

            f"| {index} "
            f"| {query} "
            f"| {rule_names} "
            f"| {result['evidencia']} "
            f"| {result['similitud']:.3f} "
            f"| {result['clase']} |"

        )


    # ========================================================
    # EXPLICACIÓN DE LAS PRUEBAS
    # ========================================================

    lines += [

        "",

        "## Explicación de resultados",

        "",
    ]


    for index, (
        query,
        result
    ) in enumerate(
        rows,
        start=1
    ):

        lines.append(
            f"### Consulta {index}"
        )

        lines.append("")

        lines.append(
            f"**Entrada:** {query}"
        )

        lines.append("")


        # ----------------------------------------------------
        # REGLAS
        # ----------------------------------------------------

        if result["reglas"]:

            for rule in result["reglas"]:

                lines.append(

                    f"- **{rule['id']} - "
                    f"{rule['name']}:** "

                    f"se activó por las palabras "

                    f"`{', '.join(rule['matches'])}`. "

                    f"Acción: {rule['action']}"

                )

        else:

            lines.append(
                "- **Regla:** no se activó ninguna regla."
            )


        lines.append("")


        # ----------------------------------------------------
        # EVIDENCIA
        # ----------------------------------------------------

        lines.append(

            f"- **Evidencia recuperada:** "
            f"{result['evidencia']}"

        )


        # ----------------------------------------------------
        # SIMILITUD
        # ----------------------------------------------------

        lines.append(

            f"- **Similitud:** "
            f"{result['similitud']:.3f}"

        )


        # ----------------------------------------------------
        # CLASIFICACIÓN
        # ----------------------------------------------------

        lines.append(

            f"- **Clasificación:** "
            f"{result['clase']}"

        )

        lines.append("")


    # ========================================================
    # RELACIÓN CON LOS TEMAS DE LA SEMANA
    # ========================================================

    lines += [

        "## Relación con los temas de la Semana 5",

        "",

        (
            "- **Sistema experto:** las reglas representan "
            "decisiones explicables del dominio."
        ),

        (
            "- **Ingeniería del conocimiento:** la experiencia "
            "del dominio se organiza en la base de conocimiento, "
            "reglas y ejemplos etiquetados."
        ),

        (
            "- **Recuperación de información:** TF-IDF y "
            "similitud coseno buscan la evidencia textual "
            "más relacionada con la consulta."
        ),

        (
            "- **Reconocimiento de patrones:** el clasificador "
            "identifica patrones de palabras y asigna "
            "una categoría."
        ),

        (
            "- **PLN:** las consultas en lenguaje natural "
            "se normalizan y se transforman en señales "
            "que pueden procesar las reglas y los modelos."
        ),

        "",

        "## Limitaciones",

        "",

        (
            "- La base de conocimiento es pequeña "
            "y debe crecer con casos reales."
        ),

        (
            "- Las reglas dependen de palabras clave "
            "y pueden no cubrir todas las formas de "
            "expresar un incidente."
        ),

        (
            "- El clasificador utiliza pocos ejemplos "
            "de entrenamiento, por lo que puede equivocarse "
            "con consultas muy diferentes."
        ),

        (
            "- La similitud textual no reemplaza "
            "la validación técnica de un administrador "
            "de servidores."
        ),

        "",

        "## Conclusión",

        "",

        (
            "La Semana 5 agrega al proyecto un sistema "
            "híbrido sencillo y trazable. Cada consulta "
            "deja evidencia de la regla aplicada, el "
            "documento recuperado, la similitud obtenida "
            "y la categoría predicha."
        ),

        "",
    ]


    REPORT_PATH.write_text(

        "\n".join(
            lines
        ),

        encoding="utf-8",
    )


# ============================================================
# PREPARAR SISTEMA
# ============================================================

DOCUMENTS = load_documents()


RETRIEVER, DOC_MATRIX = build_retriever(
    DOCUMENTS
)


CLASSIFIER = build_classifier()


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================

if __name__ == "__main__":

    results = []

    print(
        "=" * 72
    )

    print(
        "SEMANA 05 - SISTEMA HÍBRIDO"
    )

    print(
        "PROYECTO: DETECCIÓN DE ANOMALÍAS EN SERVIDORES"
    )

    print(
        "=" * 72
    )


    # ========================================================
    # PROCESAR LAS 3 CONSULTAS
    # ========================================================

    for number, query in enumerate(
        TEST_QUERIES,
        start=1
    ):

        result = answer(

            query,

            DOCUMENTS,

            RETRIEVER,

            DOC_MATRIX,

            CLASSIFIER,
        )


        results.append(
            (
                query,
                result
            )
        )


        print()

        print(
            f"CONSULTA {number}"
        )

        print(
            "-" * 72
        )

        print(
            f"Entrada: {query}"
        )


        # ----------------------------------------------------
        # MOSTRAR REGLAS
        # ----------------------------------------------------

        if result["reglas"]:

            for rule in result["reglas"]:

                print(

                    f"Regla: "
                    f"{rule['id']} - "
                    f"{rule['name']} "

                    f"(palabras: "
                    f"{', '.join(rule['matches'])})"

                )

                print(
                    f"Acción: {rule['action']}"
                )

        else:

            print(
                "Regla: ninguna"
            )


        # ----------------------------------------------------
        # MOSTRAR RECUPERACIÓN
        # ----------------------------------------------------

        print(
            f"Evidencia: {result['evidencia']}"
        )

        print(
            f"Similitud: "
            f"{result['similitud']:.3f}"
        )


        # ----------------------------------------------------
        # MOSTRAR CLASIFICACIÓN
        # ----------------------------------------------------

        print(
            f"Clasificación: {result['clase']}"
        )


    # ========================================================
    # CREAR REPORTE
    # ========================================================

    write_report(
        results
    )


    print()

    print(
        "=" * 72
    )

    print(
        f"Reporte generado: {REPORT_PATH}"
    )

    print(
        "=" * 72
    )