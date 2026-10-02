from pathlib import Path
import argparse

import matplotlib.pyplot as plt
import numpy as np
from skimage import feature, io


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
    / "semana09_comparacion_sigma.png"
)


# ============================================================
# VALORES A COMPARAR
# ============================================================

SIGMAS = [
    1.0,
    2.0,
    4.0,
]


# ============================================================
# CARGAR IMAGEN
# ============================================================

def load_image(image_path):

    image_path = Path(
        image_path
    )

    if not image_path.exists():

        raise FileNotFoundError(
            f"No existe la imagen: {image_path}"
        )

    return io.imread(
        image_path,
        as_gray=True,
    )


# ============================================================
# ANALIZAR SIGMA
# ============================================================

def analyze_sigma(
    image,
    sigma,
):

    edges = feature.canny(
        image,
        sigma=sigma,
    )


    edge_pixels = int(
        np.count_nonzero(
            edges
        )
    )


    total_pixels = (
        image.shape[0]
        * image.shape[1]
    )


    edge_percentage = (
        edge_pixels
        / total_pixels
        * 100
    )


    return {
        "sigma": sigma,
        "edges": edges,
        "edge_pixels": edge_pixels,
        "edge_percentage": edge_percentage,
    }


# ============================================================
# GENERAR COMPARACIÓN
# ============================================================

def create_comparison(
    image,
    results,
):

    ARTIFACTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    fig, axes = plt.subplots(
        1,
        4,
        figsize=(16, 4),
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
    # RESULTADOS CANNY
    # --------------------------------------------------------

    for index, result in enumerate(
        results,
        start=1,
    ):

        axes[index].imshow(
            result["edges"],
            cmap="gray",
        )

        axes[index].set_title(
            (
                f"Sigma {result['sigma']}\n"
                f"{result['edge_pixels']} píxeles de borde"
            )
        )


    # --------------------------------------------------------
    # OCULTAR EJES
    # --------------------------------------------------------

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
    results,
):

    print()

    print(
        "=" * 75
    )

    print(
        "SEMANA 9 - COMPARACIÓN DE SIGMA EN CANNY"
    )

    print(
        "=" * 75
    )

    print()


    print(
        f"{'SIGMA':<12}"
        f"{'PÍXELES DE BORDE':<22}"
        f"{'PORCENTAJE':<15}"
    )

    print(
        "-" * 55
    )


    for result in results:

        print(
            f"{result['sigma']:<12.1f}"
            f"{result['edge_pixels']:<22}"
            f"{result['edge_percentage']:.2f}%"
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
            "Comparación de valores sigma "
            "en detección de bordes Canny."
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


    return parser.parse_args()


# ============================================================
# MAIN
# ============================================================

def main():

    args = parse_arguments()

    image = load_image(
        args.imagen
    )


    results = []


    for sigma in SIGMAS:

        result = analyze_sigma(
            image,
            sigma,
        )

        results.append(
            result
        )


    create_comparison(
        image,
        results,
    )


    show_results(
        results
    )


if __name__ == "__main__":

    main()