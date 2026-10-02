from pathlib import Path
import argparse

import matplotlib.pyplot as plt
import numpy as np
from skimage import io, filters, measure, color


# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

ARTIFACTS_DIR = ROOT / "artifacts"

DEFAULT_IMAGE = (
    ROOT
    / "data"
    / "semana08"
    / "pruebas"
    / "prueba_latencia.png"
)

OUTPUT_IMAGE = (
    ARTIFACTS_DIR
    / "semana09_regiones.png"
)


# ============================================================
# CARGAR IMAGEN
# ============================================================

def load_image(image_path):

    image_path = Path(image_path)

    if not image_path.exists():

        raise FileNotFoundError(
            f"No existe la imagen: {image_path}"
        )

    return io.imread(
        image_path,
        as_gray=True,
    )


# ============================================================
# ANALIZAR REGIONES
# ============================================================

def analyze_regions(
    image,
    min_area=50,
):

    # ========================================================
    # 1. UMBRAL OTSU
    # ========================================================

    threshold = filters.threshold_otsu(
        image
    )


    # ========================================================
    # 2. MÁSCARA
    #
    # Fondo blanco / contenido oscuro
    # ========================================================

    mask = image < threshold


    # ========================================================
    # 3. ETIQUETAR REGIONES
    # ========================================================

    labels = measure.label(
        mask,
        connectivity=2,
    )


    # ========================================================
    # 4. OBTENER PROPIEDADES
    # ========================================================

    regions = measure.regionprops(
        labels
    )


    total_regions = len(
        regions
    )


    # ========================================================
    # 5. FILTRAR POR ÁREA
    #
    # min_area es un criterio experimental
    # para descartar regiones muy pequeñas.
    # ========================================================

    relevant_regions = [
        region
        for region in regions
        if region.area >= min_area
    ]


    # ========================================================
    # 6. CREAR MÁSCARA FILTRADA
    # ========================================================

    filtered_mask = np.zeros_like(
        labels,
        dtype=bool,
    )


    for region in relevant_regions:

        filtered_mask[
            labels == region.label
        ] = True


    # ========================================================
    # 7. ETIQUETAR SOLO REGIONES RELEVANTES
    # ========================================================

    filtered_labels = measure.label(
        filtered_mask,
        connectivity=2,
    )


    return {
        "threshold": float(threshold),
        "mask": mask,
        "labels": labels,
        "regions": regions,
        "total_regions": total_regions,
        "relevant_regions": relevant_regions,
        "relevant_count": len(relevant_regions),
        "filtered_mask": filtered_mask,
        "filtered_labels": filtered_labels,
    }


# ============================================================
# CREAR EVIDENCIA
# ============================================================

def create_evidence(
    image,
    result,
    min_area,
):

    ARTIFACTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    colored_labels = color.label2rgb(
        result["filtered_labels"],
        image=image,
        bg_label=0,
        alpha=0.45,
    )


    fig, axes = plt.subplots(
        1,
        3,
        figsize=(15, 5),
    )


    # --------------------------------------------------------
    # ORIGINAL
    # --------------------------------------------------------

    axes[0].imshow(
        image,
        cmap="gray",
    )

    axes[0].set_title(
        "Imagen original"
    )


    # --------------------------------------------------------
    # TODAS LAS REGIONES
    # --------------------------------------------------------

    axes[1].imshow(
        result["mask"],
        cmap="gray",
    )

    axes[1].set_title(
        f"Otsu - {result['total_regions']} regiones"
    )


    # --------------------------------------------------------
    # REGIONES FILTRADAS
    # --------------------------------------------------------

    axes[2].imshow(
        colored_labels
    )

    axes[2].set_title(
        (
            f"Área ≥ {min_area} px\n"
            f"{result['relevant_count']} regiones"
        )
    )


    for axis in axes:

        axis.axis(
            "off"
        )


    fig.tight_layout()


    fig.savefig(
        OUTPUT_IMAGE,
        dpi=160,
    )


    plt.close(
        fig
    )


# ============================================================
# MOSTRAR RESULTADOS
# ============================================================

def show_results(
    result,
    min_area,
):

    regions_sorted = sorted(
        result["regions"],
        key=lambda region: region.area,
        reverse=True,
    )


    print()

    print(
        "=" * 75
    )

    print(
        "SEMANA 9 - ANÁLISIS DE REGIONES CONECTADAS"
    )

    print(
        "=" * 75
    )

    print()


    print(
        f"Umbral Otsu: "
        f"{result['threshold']:.4f}"
    )


    print(
        f"Regiones totales: "
        f"{result['total_regions']}"
    )


    print(
        f"Área mínima utilizada: "
        f"{min_area} píxeles"
    )


    print(
        f"Regiones con área >= {min_area}: "
        f"{result['relevant_count']}"
    )


    print()

    print(
        "10 REGIONES MÁS GRANDES"
    )

    print(
        "-" * 75
    )

    print(
        f"{'REGIÓN':<12}"
        f"{'ÁREA (px)':<15}"
        f"{'ALTO':<12}"
        f"{'ANCHO':<12}"
    )

    print(
        "-" * 55
    )


    for region in regions_sorted[:10]:

        min_row, min_col, max_row, max_col = (
            region.bbox
        )

        height = (
            max_row - min_row
        )

        width = (
            max_col - min_col
        )


        print(
            f"{region.label:<12}"
            f"{region.area:<15.0f}"
            f"{height:<12}"
            f"{width:<12}"
        )


    print()

    print(
        "Evidencia generada:"
    )

    print(
        OUTPUT_IMAGE
    )

    print()

    print(
        "=" * 75
    )


# ============================================================
# ARGUMENTOS
# ============================================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        description=(
            "Analiza el tamaño de las regiones "
            "conectadas detectadas con Otsu."
        )
    )


    parser.add_argument(
        "imagen",
        nargs="?",
        default=str(
            DEFAULT_IMAGE
        ),
        help="Imagen que se desea analizar.",
    )


    parser.add_argument(
        "--min-area",
        type=int,
        default=50,
        help=(
            "Área mínima en píxeles para considerar "
            "una región relevante."
        ),
    )


    return parser.parse_args()


# ============================================================
# MAIN
# ============================================================

def main():

    args = parse_arguments()


    try:

        image = load_image(
            args.imagen
        )


        result = analyze_regions(
            image,
            min_area=args.min_area,
        )


        create_evidence(
            image,
            result,
            args.min_area,
        )


        show_results(
            result,
            args.min_area,
        )


    except Exception as error:

        print()

        print(
            "ERROR:"
        )

        print(
            error
        )

        raise SystemExit(1)


if __name__ == "__main__":

    main()