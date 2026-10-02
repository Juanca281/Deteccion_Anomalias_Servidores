from pathlib import Path
import argparse

import matplotlib.pyplot as plt
from skimage import feature, filters, io, measure


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
    / "semana09_vision.png"
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

    # Cargar directamente en escala de grises.
    # El resultado queda aproximadamente entre 0 y 1.

    image = io.imread(
        image_path,
        as_gray=True,
    )

    return image


# ============================================================
# PROCESAR IMAGEN
# ============================================================

def process_image(
    image,
    sigma=2.0,
):

    # ========================================================
    # 1. DETECCIÓN DE CONTORNOS - CANNY
    # ========================================================

    edges = feature.canny(
        image,
        sigma=sigma,
    )


    # ========================================================
    # 2. UMBRAL AUTOMÁTICO - OTSU
    # ========================================================

    threshold = filters.threshold_otsu(
        image
    )


    # ========================================================
    # 3. MÁSCARA BINARIA
    #
    # En la práctica original se utiliza:
    #
    #     image > threshold
    #
    # porque se buscan objetos claros.
    #
    # Nuestras gráficas tienen fondo blanco y contenido
    # principalmente más oscuro, por lo que utilizamos:
    #
    #     image < threshold
    #
    # Esto permite conservar las líneas, textos y elementos
    # oscuros de la gráfica como regiones de interés.
    # ========================================================

    mask = image < threshold


    # ========================================================
    # 4. REGIONES CONECTADAS
    # ========================================================

    labels = measure.label(
        mask,
        connectivity=2,
    )


    regions = int(
        labels.max()
    )


    return {
        "edges": edges,
        "threshold": float(threshold),
        "mask": mask,
        "labels": labels,
        "regions": regions,
    }


# ============================================================
# GENERAR EVIDENCIA VISUAL
# ============================================================

def create_evidence(
    image,
    edges,
    mask,
    sigma,
):

    ARTIFACTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    fig, axes = plt.subplots(
        1,
        3,
        figsize=(12, 4),
    )


    # --------------------------------------------------------
    # Imagen original
    # --------------------------------------------------------

    axes[0].imshow(
        image,
        cmap="gray",
    )

    axes[0].set_title(
        "Original"
    )


    # --------------------------------------------------------
    # Canny
    # --------------------------------------------------------

    axes[1].imshow(
        edges,
        cmap="gray",
    )

    axes[1].set_title(
        f"Canny - sigma={sigma}"
    )


    # --------------------------------------------------------
    # Otsu
    # --------------------------------------------------------

    axes[2].imshow(
        mask,
        cmap="gray",
    )

    axes[2].set_title(
        "Segmentación Otsu"
    )


    # --------------------------------------------------------
    # Ocultar ejes
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
    image_path,
    image,
    result,
    sigma,
):

    threshold = result[
        "threshold"
    ]

    threshold_255 = (
        threshold * 255
    )


    print()

    print(
        "=" * 70
    )

    print(
        "SEMANA 9 - RECONOCIMIENTO DE IMÁGENES"
    )

    print(
        "=" * 70
    )

    print()

    print(
        "IMAGEN UTILIZADA"
    )

    print(
        "-" * 70
    )

    print(
        image_path
    )

    print()

    print(
        f"Dimensiones: "
        f"{image.shape[1]} x "
        f"{image.shape[0]} píxeles"
    )

    print()


    print(
        "DETECCIÓN DE CONTORNOS"
    )

    print(
        "-" * 70
    )

    print(
        f"Algoritmo: Canny"
    )

    print(
        f"Sigma: {sigma}"
    )

    print()


    print(
        "SEGMENTACIÓN"
    )

    print(
        "-" * 70
    )

    print(
        f"Umbral Otsu (0-1): "
        f"{threshold:.4f}"
    )

    print(
        f"Umbral equivalente (0-255): "
        f"{threshold_255:.2f}"
    )

    print()


    print(
        "REGIONES"
    )

    print(
        "-" * 70
    )

    print(
        f"Regiones conectadas: "
        f"{result['regions']}"
    )

    print()


    print(
        "EVIDENCIA GENERADA"
    )

    print(
        "-" * 70
    )

    print(
        OUTPUT_IMAGE
    )

    print()

    print(
        "=" * 70
    )

    print(
        "PROCESAMIENTO COMPLETADO"
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
            "Procesamiento de imágenes de "
            "monitoreo de servidores."
        )
    )


    parser.add_argument(
        "imagen",
        nargs="?",
        default=str(
            DEFAULT_IMAGE
        ),
        help=(
            "Ruta de la imagen que "
            "se desea procesar."
        ),
    )


    parser.add_argument(
        "--sigma",
        type=float,
        default=2.0,
        help=(
            "Valor sigma utilizado "
            "por Canny."
        ),
    )


    return parser.parse_args()


# ============================================================
# MAIN
# ============================================================

def main():

    args = parse_arguments()

    image_path = Path(
        args.imagen
    )


    try:

        # ====================================================
        # 1. CARGAR IMAGEN
        # ====================================================

        image = load_image(
            image_path
        )


        # ====================================================
        # 2. PROCESAR
        # ====================================================

        result = process_image(
            image,
            sigma=args.sigma,
        )


        # ====================================================
        # 3. GENERAR EVIDENCIA
        # ====================================================

        create_evidence(
            image,
            result["edges"],
            result["mask"],
            args.sigma,
        )


        # ====================================================
        # 4. MOSTRAR RESULTADOS
        # ====================================================

        show_results(
            image_path,
            image,
            result,
            args.sigma,
        )


    except Exception as error:

        print()

        print(
            "=" * 70
        )

        print(
            "ERROR"
        )

        print(
            "=" * 70
        )

        print(
            str(error)
        )

        print()

        raise SystemExit(1)


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    main()