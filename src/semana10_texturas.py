from pathlib import Path
import argparse
import json

import matplotlib.pyplot as plt
import numpy as np

from skimage import (
    io,
    color,
    filters,
    measure,
    util,
)

from skimage.feature import local_binary_pattern


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data" / "semana10"

ARTIFACTS = ROOT / "artifacts"

ARTIFACTS.mkdir(
    parents=True,
    exist_ok=True,
)


IMAGEN_SUCIA = (
    DATA_DIR / "ventilador_sucio.jpeg"
)

IMAGEN_LIMPIA = (
    DATA_DIR / "ventilador_limpio.jpeg"
)


MIN_AREA = 50

RADIO_LBP = 2

PUNTOS_LBP = 8 * RADIO_LBP


# ============================================================
# ANALIZAR UNA IMAGEN
# ============================================================

def analizar_imagen(ruta):
    ruta = Path(ruta)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No existe la imagen: {ruta}"
        )


    # --------------------------------------------------------
    # Cargar imagen
    # --------------------------------------------------------

    imagen = io.imread(ruta)


    # --------------------------------------------------------
    # Convertir a escala de grises
    # --------------------------------------------------------

    if imagen.ndim == 3:
        gris = color.rgb2gray(
            imagen
        )

    else:
        gris = util.img_as_float(
            imagen
        )


    # --------------------------------------------------------
    # Histograma de intensidad
    # --------------------------------------------------------

    histograma, bins = np.histogram(
        gris.ravel(),
        bins=32,
        range=(0, 1),
        density=True,
    )


    # --------------------------------------------------------
    # Otsu
    # --------------------------------------------------------

    umbral = filters.threshold_otsu(
        gris
    )


    mascara = (
        gris > umbral
    )


    # --------------------------------------------------------
    # Regiones conectadas
    # --------------------------------------------------------

    etiquetas = measure.label(
        mascara,
        connectivity=2,
    )


    regiones = [
        region
        for region in measure.regionprops(
            etiquetas
        )
        if region.area > MIN_AREA
    ]


    areas = np.array(
        [
            region.area
            for region in regiones
        ],
        dtype=float,
    )


    area_promedio = (
        float(areas.mean())
        if len(areas)
        else 0.0
    )


    desviacion_area = (
        float(areas.std())
        if len(areas)
        else 0.0
    )


    # --------------------------------------------------------
    # LBP
    # --------------------------------------------------------

    gris_uint8 = util.img_as_ubyte(
        gris
    )


    lbp = local_binary_pattern(
        gris_uint8,
        PUNTOS_LBP,
        RADIO_LBP,
        method="uniform",
    )


    bins_lbp = np.arange(
        0,
        PUNTOS_LBP + 3,
    )


    histograma_lbp, _ = np.histogram(
        lbp.ravel(),
        bins=bins_lbp,
        density=True,
    )


    # --------------------------------------------------------
    # Vector de características
    # --------------------------------------------------------

    features = np.concatenate([
        [
            len(regiones),
            area_promedio,
            desviacion_area,
        ],
        histograma,
        histograma_lbp,
    ])


    return {
        "ruta": str(ruta),

        "imagen": imagen,

        "gris": gris,

        "mascara": mascara,

        "lbp": lbp,

        "histograma": histograma,

        "bins": bins,

        "histograma_lbp": histograma_lbp,

        "umbral": float(umbral),

        "regiones": len(regiones),

        "area_promedio": area_promedio,

        "desviacion_area": desviacion_area,

        "pixeles_mascara": int(
            mascara.sum()
        ),

        "features": features,
    }


# ============================================================
# DISTANCIA ENTRE DOS VECTORES
# ============================================================

def distancia_l1(a, b):
    return float(
        np.sum(
            np.abs(a - b)
        )
    )


# ============================================================
# COMPARAR FOTO DEL USUARIO
# ============================================================

def comparar_con_referencias(
    usuario,
    limpio,
    sucio,
):

    # --------------------------------------------------------
    # Intensidad
    # --------------------------------------------------------

    diferencia_base_intensidad = (
        distancia_l1(
            limpio["histograma"],
            sucio["histograma"],
        )
    )

    diferencia_base_intensidad = max(
        diferencia_base_intensidad,
        0.000001,
    )


    distancia_intensidad_limpio = (
        distancia_l1(
            usuario["histograma"],
            limpio["histograma"],
        )
        / diferencia_base_intensidad
    )


    distancia_intensidad_sucio = (
        distancia_l1(
            usuario["histograma"],
            sucio["histograma"],
        )
        / diferencia_base_intensidad
    )


    # --------------------------------------------------------
    # Textura LBP
    # --------------------------------------------------------

    diferencia_base_lbp = (
        distancia_l1(
            limpio["histograma_lbp"],
            sucio["histograma_lbp"],
        )
    )


    diferencia_base_lbp = max(
        diferencia_base_lbp,
        0.000001,
    )


    distancia_lbp_limpio = (
        distancia_l1(
            usuario["histograma_lbp"],
            limpio["histograma_lbp"],
        )
        / diferencia_base_lbp
    )


    distancia_lbp_sucio = (
        distancia_l1(
            usuario["histograma_lbp"],
            sucio["histograma_lbp"],
        )
        / diferencia_base_lbp
    )


    # --------------------------------------------------------
    # Características de regiones
    # --------------------------------------------------------

    claves_regiones = [
        "area_promedio",
        "desviacion_area",
    ]


    distancias_region_limpio = []

    distancias_region_sucio = []


    for clave in claves_regiones:

        diferencia_referencia = abs(
            limpio[clave]
            - sucio[clave]
        )


        if diferencia_referencia > 0:

            distancias_region_limpio.append(
                abs(
                    usuario[clave]
                    - limpio[clave]
                )
                / diferencia_referencia
            )


            distancias_region_sucio.append(
                abs(
                    usuario[clave]
                    - sucio[clave]
                )
                / diferencia_referencia
            )


    distancia_region_limpio = (
        float(
            np.mean(
                distancias_region_limpio
            )
        )
        if distancias_region_limpio
        else 0.0
    )


    distancia_region_sucio = (
        float(
            np.mean(
                distancias_region_sucio
            )
        )
        if distancias_region_sucio
        else 0.0
    )


    # --------------------------------------------------------
    # Distancia general
    # --------------------------------------------------------

    distancia_limpio = float(
        np.mean([
            distancia_intensidad_limpio,
            distancia_lbp_limpio,
            distancia_region_limpio,
        ])
    )


    distancia_sucio = float(
        np.mean([
            distancia_intensidad_sucio,
            distancia_lbp_sucio,
            distancia_region_sucio,
        ])
    )


    # --------------------------------------------------------
    # Interpretación
    # --------------------------------------------------------

    if distancia_sucio < distancia_limpio:

        estado = (
            "SIMILAR_A_REFERENCIA_SUCIA"
        )

        recomendacion = (
            "La imagen presenta características "
            "visuales más cercanas a la referencia "
            "con acumulación de suciedad. "
            "Se recomienda revisar físicamente el "
            "sistema de ventilación y realizar "
            "mantenimiento preventivo si corresponde."
        )

    else:

        estado = (
            "SIMILAR_A_REFERENCIA_LIMPIA"
        )

        recomendacion = (
            "La imagen presenta características "
            "visuales más cercanas a la referencia "
            "limpia. Se recomienda mantener el "
            "esquema habitual de mantenimiento "
            "preventivo."
        )


    return {
        "estado": estado,

        "distancia_limpio": round(
            distancia_limpio,
            4,
        ),

        "distancia_sucio": round(
            distancia_sucio,
            4,
        ),

        "recomendacion": recomendacion,
    }


# ============================================================
# COMPARACIÓN ACADÉMICA
# ============================================================

def ejecutar_comparacion():

    sucio = analizar_imagen(
        IMAGEN_SUCIA
    )

    limpio = analizar_imagen(
        IMAGEN_LIMPIA
    )


    # --------------------------------------------------------
    # Guardar vectores
    # --------------------------------------------------------

    features = np.vstack([
        sucio["features"],
        limpio["features"],
    ])


    np.save(
        ARTIFACTS
        / "semana10_features.npy",
        features,
    )


    # --------------------------------------------------------
    # Histograma comparativo
    # --------------------------------------------------------

    centros_sucio = (
        sucio["bins"][:-1]
        + sucio["bins"][1:]
    ) / 2


    centros_limpio = (
        limpio["bins"][:-1]
        + limpio["bins"][1:]
    ) / 2


    fig, ax = plt.subplots(
        figsize=(10, 5)
    )


    ax.plot(
        centros_sucio,
        sucio["histograma"],
        label="Ventilador sucio",
    )


    ax.plot(
        centros_limpio,
        limpio["histograma"],
        label="Ventilador limpio",
    )


    ax.axvline(
        sucio["umbral"],
        linestyle="--",
        label=(
            f"Otsu sucio: "
            f"{sucio['umbral']:.4f}"
        ),
    )


    ax.axvline(
        limpio["umbral"],
        linestyle="--",
        label=(
            f"Otsu limpio: "
            f"{limpio['umbral']:.4f}"
        ),
    )


    ax.set_title(
        "Comparación de histogramas "
        "de intensidad - Semana 10"
    )

    ax.set_xlabel(
        "Intensidad"
    )

    ax.set_ylabel(
        "Densidad"
    )

    ax.legend()

    fig.tight_layout()


    fig.savefig(
        ARTIFACTS
        / "semana10_histograma.png",
        dpi=160,
    )


    plt.close(fig)


    # --------------------------------------------------------
    # Evidencia visual
    # --------------------------------------------------------

    fig, axes = plt.subplots(
        2,
        4,
        figsize=(16, 8),
    )


    datos = [
        (
            sucio,
            "Ventilador sucio",
        ),
        (
            limpio,
            "Ventilador limpio",
        ),
    ]


    for fila, (
        resultado,
        titulo,
    ) in enumerate(datos):

        axes[fila, 0].imshow(
            resultado["imagen"]
        )

        axes[fila, 0].set_title(
            titulo
        )


        axes[fila, 1].imshow(
            resultado["gris"],
            cmap="gray",
        )

        axes[fila, 1].set_title(
            "Escala de grises"
        )


        axes[fila, 2].imshow(
            resultado["mascara"],
            cmap="gray",
        )

        axes[fila, 2].set_title(
            "Máscara Otsu"
        )


        axes[fila, 3].imshow(
            resultado["lbp"],
            cmap="gray",
        )

        axes[fila, 3].set_title(
            "Textura LBP"
        )


        for columna in range(4):

            axes[
                fila,
                columna
            ].axis("off")


    fig.suptitle(
        "Semana 10 - Comparación visual "
        "del estado físico del equipo"
    )

    fig.tight_layout()


    fig.savefig(
        ARTIFACTS
        / "semana10_analisis_visual.png",
        dpi=160,
    )


    plt.close(fig)


    # --------------------------------------------------------
    # Consola
    # --------------------------------------------------------

    print("=" * 60)

    print(
        "SEMANA 10 - COMPARACIÓN ACADÉMICA"
    )

    print("=" * 60)


    print("\nIMAGEN SUCIA")

    print(
        "Otsu:",
        round(
            sucio["umbral"],
            4,
        ),
    )

    print(
        "Regiones:",
        sucio["regiones"],
    )

    print(
        "Área promedio:",
        round(
            sucio["area_promedio"],
            2,
        ),
    )

    print(
        "Desviación:",
        round(
            sucio["desviacion_area"],
            2,
        ),
    )


    print("\nIMAGEN LIMPIA")

    print(
        "Otsu:",
        round(
            limpio["umbral"],
            4,
        ),
    )

    print(
        "Regiones:",
        limpio["regiones"],
    )

    print(
        "Área promedio:",
        round(
            limpio["area_promedio"],
            2,
        ),
    )

    print(
        "Desviación:",
        round(
            limpio["desviacion_area"],
            2,
        ),
    )


    diferencia_lbp = distancia_l1(
        sucio["histograma_lbp"],
        limpio["histograma_lbp"],
    )


    print(
        "\nDiferencia LBP:",
        round(
            diferencia_lbp,
            4,
        ),
    )


    print(
        "\nCaracterísticas por imagen:",
        len(
            sucio["features"]
        ),
    )


    print(
        "Forma del archivo:",
        features.shape,
    )


# ============================================================
# ANALIZAR FOTO DEL USUARIO
# ============================================================

def ejecutar_usuario(
    ruta_imagen,
    salida_json=False,
):

    usuario = analizar_imagen(
        ruta_imagen
    )

    limpio = analizar_imagen(
        IMAGEN_LIMPIA
    )

    sucio = analizar_imagen(
        IMAGEN_SUCIA
    )


    comparacion = (
        comparar_con_referencias(
            usuario,
            limpio,
            sucio,
        )
    )


    resultado = {
        "imagen": str(
            ruta_imagen
        ),

        "umbral_otsu": round(
            usuario["umbral"],
            4,
        ),

        "regiones": (
            usuario["regiones"]
        ),

        "area_promedio": round(
            usuario["area_promedio"],
            2,
        ),

        "desviacion_area": round(
            usuario["desviacion_area"],
            2,
        ),

        "estado": (
            comparacion["estado"]
        ),

        "distancia_limpio": (
            comparacion[
                "distancia_limpio"
            ]
        ),

        "distancia_sucio": (
            comparacion[
                "distancia_sucio"
            ]
        ),

        "recomendacion": (
            comparacion[
                "recomendacion"
            ]
        ),
    }


    if salida_json:

        print(
            json.dumps(
                resultado,
                ensure_ascii=False,
                indent=2,
            )
        )

    else:

        print("=" * 60)

        print(
            "SEMANA 10 - ANÁLISIS "
            "DE IMAGEN DEL USUARIO"
        )

        print("=" * 60)


        print(
            "\nOtsu:",
            resultado[
                "umbral_otsu"
            ],
        )

        print(
            "Regiones:",
            resultado[
                "regiones"
            ],
        )

        print(
            "Área promedio:",
            resultado[
                "area_promedio"
            ],
        )

        print(
            "Desviación:",
            resultado[
                "desviacion_area"
            ],
        )


        print(
            "\nEstado:",
            resultado[
                "estado"
            ],
        )


        print(
            "Distancia referencia limpia:",
            resultado[
                "distancia_limpio"
            ],
        )


        print(
            "Distancia referencia sucia:",
            resultado[
                "distancia_sucio"
            ],
        )


        print(
            "\nRECOMENDACIÓN:"
        )

        print(
            resultado[
                "recomendacion"
            ]
        )


# ============================================================
# ARGUMENTOS
# ============================================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        description=(
            "Semana 10 - análisis físico "
            "de equipos mediante visión artificial."
        )
    )


    parser.add_argument(
        "--imagen",
        type=str,
        default=None,
        help=(
            "Fotografía del equipo "
            "que se desea analizar."
        ),
    )


    parser.add_argument(
        "--json",
        action="store_true",
        help=(
            "Devuelve el análisis "
            "en formato JSON."
        ),
    )


    return parser.parse_args()


# ============================================================
# MAIN
# ============================================================

def main():

    args = parse_arguments()


    if args.imagen:

        ejecutar_usuario(
            args.imagen,
            args.json,
        )

    else:

        ejecutar_comparacion()


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()