from pathlib import Path
from time import perf_counter
import argparse
import json
import unicodedata

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# ============================================================
# SEMANA 11
# BENCHMARK DE MODELOS
# PROYECTO: DETECCIÓN DE ANOMALÍAS EN SERVIDORES
# ============================================================


# ============================================================
# RUTAS DEL PROYECTO
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ARTIFACTS_DIR = ROOT / "artifacts"

ARTIFACTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

IMAGE_SIZE = (64, 64)
TEST_SIZE = 0.25
RANDOM_STATE = 42

EXTENSIONES_VALIDAS = {
    ".png",
    ".jpg",
    ".jpeg",
}

CLASES_ESPERADAS = (
    "normal",
    "sobrecarga",
    "latencia",
    "disco",
    "critico",
)

NOMBRES_MODELOS = {
    "logistic": "Logistic Regression",
    "forest": "Random Forest",
    "mlp": "MLPClassifier",
}


# ============================================================
# UTILIDADES DE TEXTO Y DATASET
# ============================================================

def normalizar_texto(texto):
    texto = str(texto).lower().strip()

    return "".join(
        caracter
        for caracter in unicodedata.normalize(
            "NFD",
            texto,
        )
        if unicodedata.category(
            caracter
        ) != "Mn"
    )


def identificar_clase(nombre_carpeta):
    nombre = normalizar_texto(
        nombre_carpeta
    )

    if "normal" in nombre:
        return "normal"

    if "sobrecarga" in nombre:
        return "sobrecarga"

    if "latencia" in nombre:
        return "latencia"

    if "disco" in nombre:
        return "disco"

    if "critico" in nombre:
        return "critico"

    return None


def detectar_clases(carpeta):
    clases = {}

    try:
        subcarpetas = [
            item
            for item in carpeta.iterdir()
            if item.is_dir()
        ]

    except (
        PermissionError,
        OSError,
    ):
        return clases

    for subcarpeta in subcarpetas:
        clase = identificar_clase(
            subcarpeta.name
        )

        if clase:
            clases[
                clase
            ] = subcarpeta

    return clases


def encontrar_dataset():
    dataset_semana08 = (
        DATA_DIR
        / "semana08"
    )

    if dataset_semana08.exists():
        clases = detectar_clases(
            dataset_semana08
        )

        if all(
            clase in clases
            for clase in CLASES_ESPERADAS
        ):
            return (
                dataset_semana08,
                clases,
            )

    candidatos = []

    if DATA_DIR.exists():
        for carpeta in DATA_DIR.rglob("*"):
            if not carpeta.is_dir():
                continue

            clases = detectar_clases(
                carpeta
            )

            if all(
                clase in clases
                for clase in CLASES_ESPERADAS
            ):
                candidatos.append(
                    (
                        carpeta,
                        clases,
                    )
                )

    if not candidatos:
        raise FileNotFoundError(
            "No se encontró un dataset válido dentro "
            "de data/. Se esperan las clases: normal, "
            "sobrecarga, latencia, disco y critico."
        )

    return candidatos[0]


# ============================================================
# PREPROCESAMIENTO
# ============================================================

def redimensionar_imagen(imagen):
    try:
        metodo = (
            Image.Resampling.LANCZOS
        )

    except AttributeError:
        metodo = (
            Image.LANCZOS
        )

    return imagen.resize(
        IMAGE_SIZE,
        metodo,
    )


def procesar_imagen(ruta_imagen):
    with Image.open(
        ruta_imagen
    ) as imagen:

        imagen = imagen.convert(
            "L"
        )

        imagen = redimensionar_imagen(
            imagen
        )

        datos = np.asarray(
            imagen,
            dtype=np.float32,
        )

        datos = (
            datos
            / 255.0
        )

        return datos.flatten()


def cargar_dataset(
    verbose=True,
):
    (
        dataset_dir,
        clases,
    ) = encontrar_dataset()

    X = []
    y = []
    distribucion = {}

    if verbose:
        print(
            "=" * 64
        )
        print(
            "SEMANA 11 - BENCHMARK DE MODELOS"
        )
        print(
            "PROYECTO: DETECCIÓN DE ANOMALÍAS EN SERVIDORES"
        )
        print(
            "=" * 64
        )
        print(
            "\nDataset encontrado:"
        )
        print(
            dataset_dir
        )
        print(
            "\nCargando imágenes...\n"
        )

    for clase in CLASES_ESPERADAS:
        carpeta = clases[
            clase
        ]

        imagenes = sorted(
            [
                archivo
                for archivo in carpeta.iterdir()
                if (
                    archivo.is_file()
                    and archivo.suffix.lower()
                    in EXTENSIONES_VALIDAS
                )
            ]
        )

        distribucion[
            clase
        ] = len(
            imagenes
        )

        if verbose:
            print(
                f"{clase}: "
                f"{len(imagenes)} imágenes"
            )

        for ruta_imagen in imagenes:
            try:
                X.append(
                    procesar_imagen(
                        ruta_imagen
                    )
                )
                y.append(
                    clase
                )

            except Exception as error:
                if verbose:
                    print(
                        "Advertencia: no se pudo cargar "
                        f"{ruta_imagen.name}: {error}"
                    )

    X = np.asarray(
        X,
        dtype=np.float32,
    )

    y = np.asarray(
        y,
    )

    if len(X) == 0:
        raise RuntimeError(
            "No se cargaron imágenes del dataset."
        )

    if len(
        np.unique(
            y
        )
    ) != len(
        CLASES_ESPERADAS
    ):
        raise RuntimeError(
            "El dataset no contiene las cinco clases "
            "esperadas."
        )

    return (
        X,
        y,
        dataset_dir,
        distribucion,
    )


# ============================================================
# MODELOS
# ============================================================

def crear_modelos():
    return {
        "logistic": make_pipeline(
            StandardScaler(),
            LogisticRegression(
                max_iter=1500,
                random_state=RANDOM_STATE,
            ),
        ),

        "forest": RandomForestClassifier(
            n_estimators=250,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),

        "mlp": make_pipeline(
            StandardScaler(),
            MLPClassifier(
                hidden_layer_sizes=(64,),
                max_iter=350,
                random_state=RANDOM_STATE,
            ),
        ),
    }


# ============================================================
# GRÁFICAS
# ============================================================

def generar_grafica_accuracy(
    resumen_df,
):
    nombres = [
        NOMBRES_MODELOS.get(
            modelo,
            modelo,
        )
        for modelo in resumen_df[
            "modelo"
        ]
    ]

    valores = (
        resumen_df[
            "accuracy"
        ].to_numpy()
        * 100
    )

    figura, eje = plt.subplots(
        figsize=(9, 5.5)
    )

    barras = eje.bar(
        nombres,
        valores,
        width=0.58,
    )

    eje.set_title(
        "Semana 11 - Accuracy promedio por modelo",
        fontsize=14,
        fontweight="bold",
    )
    eje.set_xlabel(
        "Modelo"
    )
    eje.set_ylabel(
        "Accuracy (%)"
    )

    minimo = max(
        0,
        float(
            valores.min()
        ) - 5,
    )

    eje.set_ylim(
        minimo,
        101.5,
    )

    eje.grid(
        axis="y",
        alpha=0.20,
    )
    eje.set_axisbelow(
        True
    )

    for barra, valor in zip(
        barras,
        valores,
    ):
        eje.text(
            barra.get_x()
            + barra.get_width() / 2,
            barra.get_height() + 0.15,
            f"{valor:.2f}%",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    figura.tight_layout()

    ruta = (
        ARTIFACTS_DIR
        / "semana11_accuracy.png"
    )

    figura.savefig(
        ruta,
        dpi=160,
        bbox_inches="tight",
    )

    plt.close(
        figura
    )

    return ruta


def generar_grafica_tiempos(
    repeticiones_df,
):
    orden_modelos = [
        "logistic",
        "forest",
        "mlp",
    ]

    figura, eje = plt.subplots(
        figsize=(10, 5.8)
    )

    x = np.arange(
        len(
            orden_modelos
        )
    )

    ejecuciones = sorted(
        repeticiones_df[
            "ejecucion"
        ].unique()
    )

    ancho = (
        0.72
        / max(
            len(
                ejecuciones
            ),
            1,
        )
    )

    desplazamiento_inicial = (
        -(
            len(
                ejecuciones
            ) - 1
        )
        * ancho
        / 2
    )

    for indice, ejecucion in enumerate(
        ejecuciones
    ):
        bloque = (
            repeticiones_df[
                repeticiones_df[
                    "ejecucion"
                ]
                == ejecucion
            ]
            .set_index(
                "modelo"
            )
            .reindex(
                orden_modelos
            )
        )

        valores = (
            bloque[
                "fit_seconds"
            ].to_numpy()
        )

        posiciones = (
            x
            + desplazamiento_inicial
            + indice
            * ancho
        )

        barras = eje.bar(
            posiciones,
            valores,
            width=ancho * 0.90,
            label=f"Ejecución {ejecucion}",
        )

        for barra, valor in zip(
            barras,
            valores,
        ):
            eje.text(
                barra.get_x()
                + barra.get_width() / 2,
                barra.get_height(),
                f"{valor:.3f}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

    eje.set_title(
        "Semana 11 - Tiempo de entrenamiento en 3 ejecuciones",
        fontsize=14,
        fontweight="bold",
    )

    eje.set_xlabel(
        "Modelo"
    )

    eje.set_ylabel(
        "Tiempo (segundos)"
    )

    eje.set_xticks(
        x,
        [
            NOMBRES_MODELOS[
                modelo
            ]
            for modelo in orden_modelos
        ],
    )

    eje.grid(
        axis="y",
        alpha=0.20,
    )

    eje.set_axisbelow(
        True
    )

    eje.legend(
        frameon=False
    )

    figura.tight_layout()

    ruta = (
        ARTIFACTS_DIR
        / "semana11_tiempos.png"
    )

    figura.savefig(
        ruta,
        dpi=160,
        bbox_inches="tight",
    )

    plt.close(
        figura
    )

    return ruta


def generar_graficas(
    resumen_df,
    repeticiones_df,
):
    return {
        "accuracy":
            generar_grafica_accuracy(
                resumen_df
            ),

        "tiempos":
            generar_grafica_tiempos(
                repeticiones_df
            ),
    }


# ============================================================
# BENCHMARK
# ============================================================

def ejecutar_benchmark(
    repeticiones=1,
    verbose=True,
):
    if repeticiones < 1:
        raise ValueError(
            "El número de repeticiones debe ser mayor que 0."
        )

    (
        X,
        y,
        dataset_dir,
        distribucion,
    ) = cargar_dataset(
        verbose=verbose
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    if verbose:
        print(
            "\nFORMA DEL DATASET"
        )
        print(
            f"Imágenes: {X.shape[0]}"
        )
        print(
            f"Características: {X.shape[1]}"
        )
        print(
            f"Clases: {len(np.unique(y))}"
        )

        print(
            "\nPARTICIÓN"
        )
        print(
            f"Entrenamiento: {len(X_train)}"
        )
        print(
            f"Prueba: {len(X_test)}"
        )
        print(
            f"Semilla: {RANDOM_STATE}"
        )
        print(
            f"Repeticiones: {repeticiones}"
        )

    filas = []
    ejecuciones_json = []

    for numero_ejecucion in range(
        1,
        repeticiones + 1,
    ):
        modelos = crear_modelos()
        resultados_ejecucion = []

        if verbose:
            print(
                "\n"
                + "=" * 64
            )
            print(
                f"EJECUCIÓN {numero_ejecucion}"
            )
            print(
                "=" * 64
            )

        for nombre, modelo in modelos.items():
            if verbose:
                print(
                    "\n"
                    + "-" * 64
                )
                print(
                    "Entrenando: "
                    f"{NOMBRES_MODELOS[nombre]}"
                )

            inicio = perf_counter()

            modelo.fit(
                X_train,
                y_train,
            )

            tiempo = (
                perf_counter()
                - inicio
            )

            predicciones = (
                modelo.predict(
                    X_test
                )
            )

            accuracy = (
                accuracy_score(
                    y_test,
                    predicciones,
                )
            )

            fila = {
                "ejecucion":
                    numero_ejecucion,

                "modelo":
                    nombre,

                "accuracy":
                    float(
                        accuracy
                    ),

                "fit_seconds":
                    float(
                        tiempo
                    ),
            }

            filas.append(
                fila
            )

            resultados_ejecucion.append(
                {
                    **fila,
                    "nombre":
                        NOMBRES_MODELOS[
                            nombre
                        ],
                }
            )

            if verbose:
                print(
                    f"Accuracy: {accuracy:.4f}"
                )
                print(
                    f"Tiempo: {tiempo:.4f} s"
                )

        ejecuciones_json.append(
            {
                "ejecucion":
                    numero_ejecucion,

                "resultados":
                    resultados_ejecucion,
            }
        )

    repeticiones_df = pd.DataFrame(
        filas
    )

    resumen_df = (
        repeticiones_df
        .groupby(
            "modelo",
            as_index=False,
        )
        .agg(
            accuracy=(
                "accuracy",
                "mean",
            ),
            accuracy_std=(
                "accuracy",
                "std",
            ),
            fit_seconds=(
                "fit_seconds",
                "mean",
            ),
            fit_seconds_std=(
                "fit_seconds",
                "std",
            ),
        )
    )

    resumen_df[
        "accuracy_std"
    ] = (
        resumen_df[
            "accuracy_std"
        ]
        .fillna(
            0.0
        )
    )

    resumen_df[
        "fit_seconds_std"
    ] = (
        resumen_df[
            "fit_seconds_std"
        ]
        .fillna(
            0.0
        )
    )

    resumen_df = (
        resumen_df
        .sort_values(
            by=[
                "accuracy",
                "fit_seconds",
            ],
            ascending=[
                False,
                True,
            ],
        )
        .reset_index(
            drop=True
        )
    )

    # benchmark.csv conserva la evidencia mínima solicitada:
    # una fila por modelo con accuracy y tiempo promedio.
    ruta_csv = (
        ARTIFACTS_DIR
        / "benchmark.csv"
    )

    resumen_df[
        [
            "modelo",
            "accuracy",
            "fit_seconds",
        ]
    ].to_csv(
        ruta_csv,
        index=False,
    )

    # Evidencia adicional con las 3 ejecuciones completas.
    ruta_repeticiones = (
        ARTIFACTS_DIR
        / "semana11_repeticiones.csv"
    )

    repeticiones_df.to_csv(
        ruta_repeticiones,
        index=False,
    )

    graficas = generar_graficas(
        resumen_df,
        repeticiones_df,
    )

    mejor_fila = resumen_df.iloc[
        0
    ]

    mejor_modelo = str(
        mejor_fila[
            "modelo"
        ]
    )

    resumen_json = []

    for _, fila in resumen_df.iterrows():
        modelo = str(
            fila[
                "modelo"
            ]
        )

        tiempos = (
            repeticiones_df[
                repeticiones_df[
                    "modelo"
                ]
                == modelo
            ][
                "fit_seconds"
            ]
            .astype(
                float
            )
            .tolist()
        )

        accuracies = (
            repeticiones_df[
                repeticiones_df[
                    "modelo"
                ]
                == modelo
            ][
                "accuracy"
            ]
            .astype(
                float
            )
            .tolist()
        )

        resumen_json.append(
            {
                "modelo":
                    modelo,

                "nombre":
                    NOMBRES_MODELOS[
                        modelo
                    ],

                "accuracy":
                    float(
                        fila[
                            "accuracy"
                        ]
                    ),

                "accuracy_std":
                    float(
                        fila[
                            "accuracy_std"
                        ]
                    ),

                "fit_seconds":
                    float(
                        fila[
                            "fit_seconds"
                        ]
                    ),

                "fit_seconds_std":
                    float(
                        fila[
                            "fit_seconds_std"
                        ]
                    ),

                "tiempos":
                    tiempos,

                "accuracies":
                    accuracies,
            }
        )

    resultado = {
        "success":
            True,

        "repeticiones":
            repeticiones,

        "dataset": {
            "ruta":
                str(
                    dataset_dir
                ),

            "imagenes":
                int(
                    X.shape[
                        0
                    ]
                ),

            "caracteristicas":
                int(
                    X.shape[
                        1
                    ]
                ),

            "clases":
                int(
                    len(
                        np.unique(
                            y
                        )
                    )
                ),

            "distribucion":
                distribucion,

            "entrenamiento":
                int(
                    len(
                        X_train
                    )
                ),

            "prueba":
                int(
                    len(
                        X_test
                    )
                ),

            "semilla":
                RANDOM_STATE,
        },

        "ejecuciones":
            ejecuciones_json,

        "resumen":
            resumen_json,

        "ganador": {
            "modelo":
                mejor_modelo,

            "nombre":
                NOMBRES_MODELOS[
                    mejor_modelo
                ],

            "accuracy":
                float(
                    mejor_fila[
                        "accuracy"
                    ]
                ),

            "fit_seconds":
                float(
                    mejor_fila[
                        "fit_seconds"
                    ]
                ),
        },

        "artifacts": {
            "benchmark_csv":
                "/artifacts/benchmark.csv",

            "repeticiones_csv":
                "/artifacts/semana11_repeticiones.csv",

            "accuracy":
                "/artifacts/semana11_accuracy.png",

            "tiempos":
                "/artifacts/semana11_tiempos.png",
        },
    }

    if verbose:
        print(
            "\n"
            + "=" * 64
        )
        print(
            "RESULTADOS PROMEDIO DEL BENCHMARK"
        )
        print(
            "=" * 64
        )

        print(
            resumen_df[
                [
                    "modelo",
                    "accuracy",
                    "fit_seconds",
                ]
            ].to_string(
                index=False
            )
        )

        print(
            "\nMODELO SELECCIONADO:"
        )
        print(
            resultado[
                "ganador"
            ][
                "nombre"
            ]
        )

        print(
            "Accuracy promedio: "
            f"{resultado['ganador']['accuracy'] * 100:.2f}%"
        )

        print(
            "Tiempo promedio: "
            f"{resultado['ganador']['fit_seconds']:.4f} s"
        )

        print(
            "\nArchivos generados:"
        )
        print(
            ruta_csv
        )
        print(
            ruta_repeticiones
        )
        print(
            graficas[
                "accuracy"
            ]
        )
        print(
            graficas[
                "tiempos"
            ]
        )

        print(
            "\nBenchmark completado correctamente."
        )

    return resultado


# ============================================================
# CLI
# ============================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Benchmark de modelos para el proyecto "
            "Detección de Anomalías en Servidores."
        )
    )

    parser.add_argument(
        "--repeticiones",
        type=int,
        default=1,
        help=(
            "Cantidad de veces que se ejecuta el benchmark. "
            "Para Semana 11 se recomiendan 3."
        ),
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help=(
            "Devuelve únicamente JSON por stdout. "
            "Se utiliza para la integración con Flask."
        ),
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        resultado = ejecutar_benchmark(
            repeticiones=args.repeticiones,
            verbose=not args.json,
        )

        if args.json:
            print(
                json.dumps(
                    resultado,
                    ensure_ascii=False,
                )
            )

    except KeyboardInterrupt:
        if args.json:
            print(
                json.dumps(
                    {
                        "success": False,
                        "error":
                            "Ejecución cancelada por el usuario.",
                    },
                    ensure_ascii=False,
                )
            )

        else:
            print(
                "\nEjecución cancelada por el usuario."
            )

    except Exception as error:
        if args.json:
            print(
                json.dumps(
                    {
                        "success": False,
                        "error": str(
                            error
                        ),
                    },
                    ensure_ascii=False,
                )
            )

        else:
            print(
                "\nERROR EN SEMANA 11:"
            )
            print(
                error
            )
            raise


if __name__ == "__main__":
    main()
