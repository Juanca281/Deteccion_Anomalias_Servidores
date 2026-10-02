from pathlib import Path
import argparse
import json

import numpy as np

from semana09_vision import (
    load_image,
    process_image,
    create_evidence as create_main_evidence,
)

from semana09_comparar_sigma import (
    analyze_sigma,
    create_comparison,
    SIGMAS,
)

from semana09_analizar_regiones import (
    analyze_regions,
    create_evidence as create_regions_evidence,
)


# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_IMAGE = (
    ROOT
    / "data"
    / "semana08"
    / "pruebas"
    / "prueba_latencia.png"
)

VISION_IMAGE = (
    ROOT
    / "artifacts"
    / "semana09_vision.png"
)

SIGMA_IMAGE = (
    ROOT
    / "artifacts"
    / "semana09_comparacion_sigma.png"
)

REGIONS_IMAGE = (
    ROOT
    / "artifacts"
    / "semana09_regiones.png"
)


# ============================================================
# ANALIZAR IMAGEN COMPLETA
# ============================================================

def analyze_image(
    image_path,
    sigma=2.0,
    min_area=50,
):

    image_path = Path(
        image_path
    )


    # ========================================================
    # 1. VALIDAR IMAGEN
    # ========================================================

    if not image_path.exists():

        raise FileNotFoundError(
            f"No existe la imagen: {image_path}"
        )


    # ========================================================
    # 2. CARGAR IMAGEN
    # ========================================================

    image = load_image(
        image_path
    )


    height = int(
        image.shape[0]
    )

    width = int(
        image.shape[1]
    )


    # ========================================================
    # 3. PROCESAMIENTO PRINCIPAL
    #
    # Canny + Otsu + regiones
    # ========================================================

    vision_result = process_image(
        image,
        sigma=sigma,
    )


    # ========================================================
    # 4. GENERAR EVIDENCIA PRINCIPAL
    # ========================================================

    create_main_evidence(
        image,
        vision_result[
            "edges"
        ],
        vision_result[
            "mask"
        ],
        sigma,
    )


    # ========================================================
    # 5. COMPARAR SIGMAS
    # ========================================================

    sigma_results = []


    for sigma_value in SIGMAS:

        result = analyze_sigma(
            image,
            sigma_value,
        )

        sigma_results.append(
            result
        )


    # ========================================================
    # 6. GENERAR COMPARACIÓN DE SIGMAS
    # ========================================================

    create_comparison(
        image,
        sigma_results,
    )


    # ========================================================
    # 7. ANALIZAR REGIONES
    # ========================================================

    regions_result = analyze_regions(
        image,
        min_area=min_area,
    )


    # ========================================================
    # 8. GENERAR EVIDENCIA DE REGIONES
    # ========================================================

    create_regions_evidence(
        image,
        regions_result,
        min_area,
    )


    # ========================================================
    # 9. REGIONES MÁS GRANDES
    # ========================================================

    regions_sorted = sorted(
        regions_result[
            "regions"
        ],
        key=lambda region: region.area,
        reverse=True,
    )


    largest_regions = []


    for region in regions_sorted[:10]:

        (
            min_row,
            min_col,
            max_row,
            max_col,
        ) = region.bbox


        region_height = int(
            max_row - min_row
        )

        region_width = int(
            max_col - min_col
        )


        largest_regions.append(
            {
                "label": int(
                    region.label
                ),

                "area": int(
                    region.area
                ),

                "height": (
                    region_height
                ),

                "width": (
                    region_width
                ),
            }
        )


    # ========================================================
    # 10. RESULTADOS DE SIGMA
    # ========================================================

    sigma_summary = []


    for result in sigma_results:

        sigma_summary.append(
            {
                "sigma": float(
                    result[
                        "sigma"
                    ]
                ),

                "edge_pixels": int(
                    result[
                        "edge_pixels"
                    ]
                ),

                "edge_percentage": round(
                    float(
                        result[
                            "edge_percentage"
                        ]
                    ),
                    2,
                ),
            }
        )


    # ========================================================
    # 11. UMBRAL
    # ========================================================

    threshold = float(
        vision_result[
            "threshold"
        ]
    )


    threshold_255 = (
        threshold
        * 255
    )


    # ========================================================
    # 12. RESULTADO FINAL
    # ========================================================

    result = {

        "success": True,

        "image": {

            "name": (
                image_path.name
            ),

            "path": str(
                image_path
            ),

            "width": width,

            "height": height,
        },


        "canny": {

            "selected_sigma": float(
                sigma
            ),

            "comparison": (
                sigma_summary
            ),
        },


        "otsu": {

            "threshold_01": round(
                threshold,
                4,
            ),

            "threshold_255": round(
                threshold_255,
                2,
            ),
        },


        "regions": {

            "total": int(
                regions_result[
                    "total_regions"
                ]
            ),

            "minimum_area": int(
                min_area
            ),

            "relevant": int(
                regions_result[
                    "relevant_count"
                ]
            ),

            "largest": (
                largest_regions
            ),
        },


        "artifacts": {

            "vision": (
                "artifacts/"
                "semana09_vision.png"
            ),

            "sigma_comparison": (
                "artifacts/"
                "semana09_comparacion_sigma.png"
            ),

            "regions": (
                "artifacts/"
                "semana09_regiones.png"
            ),
        },
    }


    return result


# ============================================================
# MOSTRAR RESULTADOS
# ============================================================

def show_result(
    result,
):

    print()

    print(
        "=" * 78
    )

    print(
        "SEMANA 9 - ANÁLISIS INTEGRADO DE VISIÓN"
    )

    print(
        "=" * 78
    )

    print()


    # ========================================================
    # IMAGEN
    # ========================================================

    print(
        "IMAGEN ANALIZADA"
    )

    print(
        "-" * 78
    )

    print(
        f"Nombre: "
        f"{result['image']['name']}"
    )

    print(
        f"Dimensiones: "
        f"{result['image']['width']} x "
        f"{result['image']['height']} px"
    )

    print()


    # ========================================================
    # CANNY
    # ========================================================

    print(
        "DETECCIÓN DE BORDES - CANNY"
    )

    print(
        "-" * 78
    )

    print(
        f"Sigma principal: "
        f"{result['canny']['selected_sigma']}"
    )

    print()


    print(
        f"{'SIGMA':<12}"
        f"{'PÍXELES BORDE':<20}"
        f"{'PORCENTAJE':<15}"
    )

    print(
        "-" * 50
    )


    for item in result[
        "canny"
    ][
        "comparison"
    ]:

        print(
            f"{item['sigma']:<12.1f}"
            f"{item['edge_pixels']:<20}"
            f"{item['edge_percentage']:.2f}%"
        )


    print()


    # ========================================================
    # OTSU
    # ========================================================

    print(
        "SEGMENTACIÓN - OTSU"
    )

    print(
        "-" * 78
    )

    print(
        f"Umbral 0-1: "
        f"{result['otsu']['threshold_01']:.4f}"
    )

    print(
        f"Umbral 0-255: "
        f"{result['otsu']['threshold_255']:.2f}"
    )

    print()


    # ========================================================
    # REGIONES
    # ========================================================

    print(
        "REGIONES CONECTADAS"
    )

    print(
        "-" * 78
    )

    print(
        f"Regiones totales: "
        f"{result['regions']['total']}"
    )

    print(
        f"Área mínima: "
        f"{result['regions']['minimum_area']} px"
    )

    print(
        f"Regiones relevantes: "
        f"{result['regions']['relevant']}"
    )

    print()


    print(
        "REGIONES MÁS GRANDES"
    )

    print(
        "-" * 78
    )

    print(
        f"{'REGIÓN':<12}"
        f"{'ÁREA':<15}"
        f"{'ALTO':<12}"
        f"{'ANCHO':<12}"
    )

    print(
        "-" * 55
    )


    for region in result[
        "regions"
    ][
        "largest"
    ]:

        print(
            f"{region['label']:<12}"
            f"{region['area']:<15}"
            f"{region['height']:<12}"
            f"{region['width']:<12}"
        )


    print()


    # ========================================================
    # EVIDENCIAS
    # ========================================================

    print(
        "EVIDENCIAS GENERADAS"
    )

    print(
        "-" * 78
    )


    print(
        result[
            "artifacts"
        ][
            "vision"
        ]
    )

    print(
        result[
            "artifacts"
        ][
            "sigma_comparison"
        ]
    )

    print(
        result[
            "artifacts"
        ][
            "regions"
        ]
    )


    print()

    print(
        "=" * 78
    )

    print(
        "ANÁLISIS COMPLETADO"
    )

    print(
        "=" * 78
    )

    print()


# ============================================================
# ARGUMENTOS
# ============================================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        description=(
            "Análisis integrado de visión "
            "por computador para Semana 9."
        )
    )


    parser.add_argument(
        "imagen",
        nargs="?",
        default=str(
            DEFAULT_IMAGE
        ),
        help=(
            "Imagen que se desea analizar."
        ),
    )


    parser.add_argument(
        "--sigma",
        type=float,
        default=2.0,
        help=(
            "Sigma principal utilizado "
            "por Canny."
        ),
    )


    parser.add_argument(
        "--min-area",
        type=int,
        default=50,
        help=(
            "Área mínima para considerar "
            "una región relevante."
        ),
    )


    parser.add_argument(
        "--json",
        action="store_true",
        help=(
            "Mostrar resultado "
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
            args.imagen,
            sigma=args.sigma,
            min_area=args.min_area,
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
                "=" * 78
            )

            print(
                "ERROR EN SEMANA 9"
            )

            print(
                "=" * 78
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