from pathlib import Path
import argparse
import json

from semana08_predecir_imagen import predict_image

from semana08_evidencia import (
    save_evidence,
)

from semana08_ontologia import (
    create_ontology,
    interpret_prediction,
)


# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# ANALIZAR IMAGEN
# ============================================================

def analyze_image(
    image_path,
):

    image_path = Path(
        image_path
    )


    # ========================================================
    # 1. VALIDAR IMAGEN
    # ========================================================

    if not image_path.exists():

        raise FileNotFoundError(
            f"No existe la imagen: "
            f"{image_path}"
        )


    # ========================================================
    # 2. RED NEURONAL
    # ========================================================

    prediction = predict_image(
        image_path
    )


    # ========================================================
    # 3. REGISTRAR EVIDENCIA
    # ========================================================

    evidence = save_evidence(
        prediction
    )


    # ========================================================
    # 4. CREAR / ACTUALIZAR ONTOLOGÍA
    # ========================================================

    create_ontology()


    # ========================================================
    # 5. INTERPRETACIÓN ONTOLÓGICA
    # ========================================================

    ontology = interpret_prediction(
        prediction[
            "prediction"
        ],
        prediction[
            "confidence"
        ],
    )


    # ========================================================
    # 6. RESULTADO FINAL
    # ========================================================

    result = {

        "success": True,

        "image": {
            "name": image_path.name,
            "path": str(
                image_path
            ),
        },

        "prediction": {
            "class_id": prediction[
                "class_id"
            ],

            "class": prediction[
                "prediction"
            ],

            "confidence": prediction[
                "confidence"
            ],

            "confidence_level": evidence[
                "confidence_level"
            ],

            "probabilities": prediction[
                "probabilities"
            ],
        },

        "evidence": {
            "id": evidence[
                "id"
            ],

            "date": evidence[
                "date"
            ],

            "database": (
                "artifacts/imagenes.db"
            ),
        },

        "ontology": {
            "concept": ontology[
                "concept"
            ],

            "type": ontology[
                "type"
            ],

            "affected_metrics": ontology[
                "affected_metrics"
            ],

            "interpretation": ontology[
                "interpretation"
            ],

            "graph": (
                "artifacts/ontologia.graphml"
            ),
        },
    }


    return result


# ============================================================
# MOSTRAR RESULTADO
# ============================================================

def show_result(
    result,
):

    print()

    print(
        "=" * 70
    )

    print(
        "SEMANA 8 - ANÁLISIS INTEGRADO"
    )

    print(
        "=" * 70
    )

    print()


    # ========================================================
    # IMAGEN
    # ========================================================

    print(
        "IMAGEN ANALIZADA"
    )

    print(
        "-" * 70
    )

    print(
        f"Nombre: "
        f"{result['image']['name']}"
    )

    print(
        f"Ruta: "
        f"{result['image']['path']}"
    )

    print()


    # ========================================================
    # RED NEURONAL
    # ========================================================

    print(
        "RED NEURONAL"
    )

    print(
        "-" * 70
    )

    print(
        f"Predicción: "
        f"{result['prediction']['class']}"
    )

    print(
        f"Confianza: "
        f"{result['prediction']['confidence']:.2f}%"
    )

    print(
        f"Nivel: "
        f"{result['prediction']['confidence_level']}"
    )

    print()


    # ========================================================
    # PROBABILIDADES
    # ========================================================

    print(
        "PROBABILIDAD POR CLASE"
    )

    print(
        "-" * 70
    )


    probabilities = (
        result[
            "prediction"
        ][
            "probabilities"
        ]
    )


    ordered = sorted(
        probabilities.items(),
        key=lambda item: item[1],
        reverse=True,
    )


    for (
        class_name,
        probability,
    ) in ordered:

        print(
            f"{class_name:<25} "
            f"{probability:>6.2f}%"
        )


    print()


    # ========================================================
    # SQLITE
    # ========================================================

    print(
        "EVIDENCIA SQLITE"
    )

    print(
        "-" * 70
    )

    print(
        f"ID evidencia: "
        f"{result['evidence']['id']}"
    )

    print(
        f"Fecha: "
        f"{result['evidence']['date']}"
    )

    print(
        f"Base de datos: "
        f"{result['evidence']['database']}"
    )

    print()


    # ========================================================
    # ONTOLOGÍA
    # ========================================================

    print(
        "INTERPRETACIÓN ONTOLÓGICA"
    )

    print(
        "-" * 70
    )

    print(
        f"Concepto: "
        f"{result['ontology']['concept']}"
    )

    print(
        f"Tipo: "
        f"{result['ontology']['type']}"
    )


    metrics = (
        result[
            "ontology"
        ][
            "affected_metrics"
        ]
    )


    if metrics:

        print(
            "Métricas afectadas: "
            + ", ".join(
                metrics
            )
        )

    else:

        print(
            "Métricas afectadas: "
            "Ninguna"
        )


    print()

    print(
        "Interpretación:"
    )

    print(
        result[
            "ontology"
        ][
            "interpretation"
        ]
    )

    print()


    print(
        f"Ontología: "
        f"{result['ontology']['graph']}"
    )


    print()

    print(
        "=" * 70
    )

    print(
        "ANÁLISIS COMPLETADO"
    )

    print(
        "=" * 70
    )

    print()


# ============================================================
# ARGUMENTOS
# ============================================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        description=(
            "Análisis integrado de imágenes "
            "de monitoreo de servidores."
        )
    )


    parser.add_argument(
        "imagen",
        type=str,
        help=(
            "Ruta de la imagen "
            "que se desea analizar."
        ),
    )


    parser.add_argument(
        "--json",
        action="store_true",
        help=(
            "Mostrar la respuesta "
            "en formato JSON."
        ),
    )


    return parser.parse_args()


# ============================================================
# MAIN
# ============================================================

def main():

    args = parse_arguments()


    try:

        result = analyze_image(
            args.imagen
        )


        # ====================================================
        # JSON
        # ====================================================

        if args.json:

            print(
                json.dumps(
                    result,
                    ensure_ascii=False,
                    indent=4,
                )
            )


        # ====================================================
        # TERMINAL
        # ====================================================

        else:

            show_result(
                result
            )


    except Exception as error:

        error_result = {
            "success": False,
            "error": str(
                error
            ),
        }


        if args.json:

            print(
                json.dumps(
                    error_result,
                    ensure_ascii=False,
                    indent=4,
                )
            )

        else:

            print()

            print(
                "=" * 70
            )

            print(
                "ERROR EN EL ANÁLISIS"
            )

            print(
                "=" * 70
            )

            print()

            print(
                str(
                    error
                )
            )

            print()


        raise SystemExit(1)


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    main()