from pathlib import Path
import argparse
import json

import networkx as nx


# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

ARTIFACTS_DIR = ROOT / "artifacts"

ONTOLOGY_PATH = (
    ARTIFACTS_DIR
    / "ontologia.graphml"
)


# ============================================================
# INTERPRETACIONES DEL PROYECTO
# ============================================================

INTERPRETATIONS = {

    "Normal": {
        "concept": "EstadoNormal",
        "type": "Estado",
        "affected_metrics": [],
        "interpretation": (
            "El servidor presenta un comportamiento "
            "estable y no se identifican anomalías "
            "relevantes en las métricas analizadas."
        ),
    },

    "Sobrecarga CPU/RAM": {
        "concept": "SobrecargaCPURAM",
        "type": "Anomalia",
        "affected_metrics": [
            "CPU",
            "RAM",
        ],
        "interpretation": (
            "Se identifica un consumo elevado de CPU "
            "y memoria RAM, asociado a una posible "
            "sobrecarga de recursos del servidor."
        ),
    },

    "Latencia alta": {
        "concept": "LatenciaAlta",
        "type": "Anomalia",
        "affected_metrics": [
            "Latencia",
        ],
        "interpretation": (
            "Se identifica un incremento anormal en "
            "la latencia del servidor, lo cual puede "
            "afectar los tiempos de respuesta."
        ),
    },

    "Saturación de disco": {
        "concept": "SaturacionDisco",
        "type": "Anomalia",
        "affected_metrics": [
            "Disco",
        ],
        "interpretation": (
            "El almacenamiento presenta niveles "
            "elevados de utilización y puede estar "
            "cerca de su capacidad máxima."
        ),
    },

    "Estado crítico": {
        "concept": "EstadoCritico",
        "type": "AnomaliaCritica",
        "affected_metrics": [
            "CPU",
            "RAM",
            "Disco",
            "Latencia",
        ],
        "interpretation": (
            "Se observa una combinación de métricas "
            "en niveles críticos que representa un "
            "estado general de riesgo para el servidor."
        ),
    },
}


# ============================================================
# CREAR ONTOLOGÍA
# ============================================================

def create_ontology():

    ARTIFACTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    graph = nx.DiGraph()


    # ========================================================
    # CONCEPTOS PRINCIPALES
    # ========================================================

    graph.add_node(
        "Servidor",
        tipo="Infraestructura",
        descripcion=(
            "Equipo o sistema que presta "
            "servicios tecnológicos."
        ),
    )


    graph.add_node(
        "GraficaMonitoreo",
        tipo="EvidenciaVisual",
        descripcion=(
            "Representación gráfica de las "
            "métricas del servidor."
        ),
    )


    graph.add_node(
        "Metrica",
        tipo="Concepto",
        descripcion=(
            "Variable utilizada para medir "
            "el comportamiento del servidor."
        ),
    )


    graph.add_node(
        "Anomalia",
        tipo="Concepto",
        descripcion=(
            "Comportamiento fuera de los "
            "rangos esperados."
        ),
    )


    graph.add_node(
        "Estado",
        tipo="Concepto",
        descripcion=(
            "Condición general identificada "
            "en el servidor."
        ),
    )


    graph.add_node(
        "Prediccion",
        tipo="ResultadoIA",
        descripcion=(
            "Resultado obtenido mediante "
            "la red neuronal."
        ),
    )


    graph.add_node(
        "Evidencia",
        tipo="Registro",
        descripcion=(
            "Registro almacenado en SQLite "
            "como soporte de una predicción."
        ),
    )


    # ========================================================
    # MÉTRICAS
    # ========================================================

    metrics = {
        "CPU": (
            "Uso del procesador."
        ),
        "RAM": (
            "Uso de memoria RAM."
        ),
        "Disco": (
            "Uso del almacenamiento."
        ),
        "Latencia": (
            "Tiempo de respuesta del sistema."
        ),
    }


    for (
        metric,
        description,
    ) in metrics.items():

        graph.add_node(
            metric,
            tipo="Metrica",
            descripcion=description,
        )


        graph.add_edge(
            metric,
            "Metrica",
            relacion="es_tipo_de",
        )


    # ========================================================
    # ESTADOS Y ANOMALÍAS
    # ========================================================

    graph.add_node(
        "EstadoNormal",
        tipo="Estado",
        descripcion=(
            "Funcionamiento estable "
            "del servidor."
        ),
    )


    graph.add_edge(
        "EstadoNormal",
        "Estado",
        relacion="es_tipo_de",
    )


    graph.add_node(
        "SobrecargaCPURAM",
        tipo="Anomalia",
        descripcion=(
            "Consumo elevado de CPU y RAM."
        ),
    )


    graph.add_node(
        "LatenciaAlta",
        tipo="Anomalia",
        descripcion=(
            "Tiempo de respuesta superior "
            "a los valores esperados."
        ),
    )


    graph.add_node(
        "SaturacionDisco",
        tipo="Anomalia",
        descripcion=(
            "Utilización elevada del "
            "almacenamiento."
        ),
    )


    graph.add_node(
        "EstadoCritico",
        tipo="AnomaliaCritica",
        descripcion=(
            "Combinación de múltiples "
            "métricas en estado crítico."
        ),
    )


    anomalies = [
        "SobrecargaCPURAM",
        "LatenciaAlta",
        "SaturacionDisco",
        "EstadoCritico",
    ]


    for anomaly in anomalies:

        graph.add_edge(
            anomaly,
            "Anomalia",
            relacion="es_tipo_de",
        )


    # ========================================================
    # RELACIONES DEL DOMINIO
    # ========================================================

    graph.add_edge(
        "Servidor",
        "GraficaMonitoreo",
        relacion="genera",
    )


    graph.add_edge(
        "GraficaMonitoreo",
        "Metrica",
        relacion="representa",
    )


    graph.add_edge(
        "GraficaMonitoreo",
        "Prediccion",
        relacion="es_analizada_para_generar",
    )


    graph.add_edge(
        "Prediccion",
        "Evidencia",
        relacion="se_registra_como",
    )


    graph.add_edge(
        "Evidencia",
        "GraficaMonitoreo",
        relacion="proviene_de",
    )


    # ========================================================
    # RELACIONES DE ANOMALÍAS
    # ========================================================

    graph.add_edge(
        "SobrecargaCPURAM",
        "CPU",
        relacion="afecta",
    )


    graph.add_edge(
        "SobrecargaCPURAM",
        "RAM",
        relacion="afecta",
    )


    graph.add_edge(
        "LatenciaAlta",
        "Latencia",
        relacion="afecta",
    )


    graph.add_edge(
        "SaturacionDisco",
        "Disco",
        relacion="afecta",
    )


    graph.add_edge(
        "EstadoCritico",
        "CPU",
        relacion="puede_afectar",
    )


    graph.add_edge(
        "EstadoCritico",
        "RAM",
        relacion="puede_afectar",
    )


    graph.add_edge(
        "EstadoCritico",
        "Disco",
        relacion="puede_afectar",
    )


    graph.add_edge(
        "EstadoCritico",
        "Latencia",
        relacion="puede_afectar",
    )


    # ========================================================
    # GUARDAR GRAPHML
    # ========================================================

    nx.write_graphml(
        graph,
        ONTOLOGY_PATH,
    )


    return graph


# ============================================================
# INTERPRETAR PREDICCIÓN
# ============================================================

def interpret_prediction(
    prediction,
    confidence=None,
):

    if prediction not in INTERPRETATIONS:

        raise ValueError(
            f"No existe interpretación "
            f"para: {prediction}"
        )


    base = INTERPRETATIONS[
        prediction
    ]


    result = {
        "prediction": prediction,
        "concept": base[
            "concept"
        ],
        "type": base[
            "type"
        ],
        "affected_metrics": base[
            "affected_metrics"
        ],
        "interpretation": base[
            "interpretation"
        ],
    }


    # ========================================================
    # CONFIANZA
    # ========================================================

    if confidence is not None:

        confidence = float(
            confidence
        )


        if confidence >= 55:

            confidence_level = (
                "Confiable"
            )

        elif confidence >= 40:

            confidence_level = (
                "Moderada"
            )

        else:

            confidence_level = (
                "No concluyente"
            )


        result[
            "confidence"
        ] = confidence

        result[
            "confidence_level"
        ] = confidence_level


    return result


# ============================================================
# MOSTRAR ONTOLOGÍA
# ============================================================

def show_ontology(
    graph,
):

    print()

    print(
        "=" * 65
    )

    print(
        "ONTOLOGÍA - SEMANA 8"
    )

    print(
        "=" * 65
    )

    print()

    print(
        f"Conceptos: "
        f"{graph.number_of_nodes()}"
    )

    print(
        f"Relaciones: "
        f"{graph.number_of_edges()}"
    )

    print()


    print(
        "CONCEPTOS"
    )

    print(
        "-" * 65
    )


    for (
        node,
        data,
    ) in graph.nodes(
        data=True
    ):

        print(
            f"{node:<25} "
            f"{data.get('tipo', '')}"
        )


    print()

    print(
        "RELACIONES"
    )

    print(
        "-" * 65
    )


    for (
        source,
        target,
        data,
    ) in graph.edges(
        data=True
    ):

        print(
            f"{source:<22} "
            f"--{data['relacion']}--> "
            f"{target}"
        )


    print()

    print(
        "Archivo generado:"
    )

    print(
        ONTOLOGY_PATH
    )

    print()


# ============================================================
# ARGUMENTOS
# ============================================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        description=(
            "Ontología para reconocimiento "
            "de anomalías de servidores."
        )
    )


    parser.add_argument(
        "--prediccion",
        type=str,
        help=(
            "Predicción que se desea "
            "interpretar."
        ),
    )


    parser.add_argument(
        "--confianza",
        type=float,
        help=(
            "Nivel de confianza "
            "de la predicción."
        ),
    )


    parser.add_argument(
        "--json",
        action="store_true",
        help=(
            "Mostrar interpretación "
            "en formato JSON."
        ),
    )


    return parser.parse_args()


    # ========================================================
    # MAIN
    # ========================================================

def main():

    args = parse_arguments()

    graph = create_ontology()


    # ========================================================
    # INTERPRETAR UNA PREDICCIÓN
    # ========================================================

    if args.prediccion:

        try:

            result = interpret_prediction(
                args.prediccion,
                args.confianza,
            )


            if args.json:

                print(
                    json.dumps(
                        result,
                        ensure_ascii=False,
                        indent=4,
                    )
                )


            else:

                print()

                print(
                    "=" * 65
                )

                print(
                    "INTERPRETACIÓN ONTOLÓGICA"
                )

                print(
                    "=" * 65
                )

                print()

                print(
                    f"Predicción: "
                    f"{result['prediction']}"
                )

                print(
                    f"Concepto: "
                    f"{result['concept']}"
                )

                print(
                    f"Tipo: "
                    f"{result['type']}"
                )


                if result[
                    "affected_metrics"
                ]:

                    print(
                        "Métricas afectadas: "
                        + ", ".join(
                            result[
                                "affected_metrics"
                            ]
                        )
                    )

                else:

                    print(
                        "Métricas afectadas: "
                        "Ninguna"
                    )


                if (
                    "confidence"
                    in result
                ):

                    print(
                        f"Confianza: "
                        f"{result['confidence']:.2f}%"
                    )

                    print(
                        f"Nivel: "
                        f"{result['confidence_level']}"
                    )


                print()

                print(
                    "Interpretación:"
                )

                print(
                    result[
                        "interpretation"
                    ]
                )

                print()


        except ValueError as error:

            print(
                f"Error: {error}"
            )


        return


    # ========================================================
    # MOSTRAR ONTOLOGÍA COMPLETA
    # ========================================================

    show_ontology(
        graph
    )


if __name__ == "__main__":

    main()