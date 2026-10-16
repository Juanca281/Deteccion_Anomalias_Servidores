from pathlib import Path
from time import perf_counter
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

IMAGE_SIZE = (
    64,
    64,
)

TEST_SIZE = 0.25

RANDOM_STATE = 42

EXTENSIONES_VALIDAS = {
    ".png",
    ".jpg",
    ".jpeg",
}


# ============================================================
# CLASES DEL PROYECTO
# ============================================================

CLASES_ESPERADAS = (
    "normal",
    "sobrecarga",
    "latencia",
    "disco",
    "critico",
)


# ============================================================
# NOMBRES PARA MOSTRAR
# ============================================================

NOMBRES_MODELOS = {
    "logistic": "Logistic Regression",
    "forest": "Random Forest",
    "mlp": "MLP",
}


# ============================================================
# NORMALIZAR TEXTO
# ============================================================

def normalizar_texto(texto):

    texto = str(
        texto
    ).lower().strip()

    texto = "".join(
        caracter
        for caracter in unicodedata.normalize(
            "NFD",
            texto,
        )
        if unicodedata.category(
            caracter
        ) != "Mn"
    )

    return texto


# ============================================================
# IDENTIFICAR CLASE
# ============================================================

def identificar_clase(
    nombre_carpeta,
):

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


# ============================================================
# BUSCAR DATASET
# ============================================================

def encontrar_dataset():

    # --------------------------------------------------------
    # Primero intenta usar directamente data/semana08
    # --------------------------------------------------------

    dataset_semana08 = (
        DATA_DIR
        / "semana08"
    )

    if dataset_semana08.exists():

        clases = {}

        for carpeta in (
            dataset_semana08.iterdir()
        ):

            if not carpeta.is_dir():
                continue

            clase = identificar_clase(
                carpeta.name
            )

            if clase:

                clases[
                    clase
                ] = carpeta

        if all(
            clase in clases
            for clase in CLASES_ESPERADAS
        ):

            return (
                dataset_semana08,
                clases,
            )

    # --------------------------------------------------------
    # Si cambia la ruta, busca automáticamente dentro de data
    # --------------------------------------------------------

    candidatos = []

    for carpeta in DATA_DIR.rglob("*"):

        if not carpeta.is_dir():
            continue

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

            continue

        for subcarpeta in subcarpetas:

            clase = identificar_clase(
                subcarpeta.name
            )

            if clase:

                clases[
                    clase
                ] = subcarpeta

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
            "de la carpeta data/. Se esperan las clases: "
            "normal, sobrecarga, latencia, disco y critico."
        )

    return candidatos[0]


# ============================================================
# REDIMENSIONAR IMAGEN
# ============================================================

def redimensionar_imagen(
    imagen,
):

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


# ============================================================
# CARGAR UNA IMAGEN
# ============================================================

def procesar_imagen(
    ruta_imagen,
):

    with Image.open(
        ruta_imagen
    ) as imagen:

        # ----------------------------------------------------
        # Escala de grises
        # ----------------------------------------------------

        imagen = imagen.convert(
            "L"
        )

        # ----------------------------------------------------
        # Redimensionar a 64 x 64
        # ----------------------------------------------------

        imagen = redimensionar_imagen(
            imagen
        )

        # ----------------------------------------------------
        # Convertir a matriz NumPy
        # ----------------------------------------------------

        datos = np.asarray(
            imagen,
            dtype=np.float32,
        )

        # ----------------------------------------------------
        # Normalizar entre 0 y 1
        # ----------------------------------------------------

        datos = (
            datos
            / 255.0
        )

        # ----------------------------------------------------
        # 64 x 64 = 4096 características
        # ----------------------------------------------------

        vector = (
            datos.flatten()
        )

        return vector


# ============================================================
# CARGAR DATASET COMPLETO
# ============================================================

def cargar_dataset():

    (
        dataset_dir,
        clases,
    ) = encontrar_dataset()

    X = []

    y = []

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

        print(
            f"{clase}: "
            f"{len(imagenes)} imágenes"
        )

        for ruta_imagen in imagenes:

            try:

                vector = procesar_imagen(
                    ruta_imagen
                )

                X.append(
                    vector
                )

                y.append(
                    clase
                )

            except Exception as error:

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
    )


# ============================================================
# CREAR MODELOS
# ============================================================

def crear_modelos():

    modelos = {

        # ----------------------------------------------------
        # MODELO 1
        # Línea base
        # ----------------------------------------------------

        "logistic": make_pipeline(

            StandardScaler(),

            LogisticRegression(
                max_iter=1500,
                random_state=RANDOM_STATE,
            ),

        ),

        # ----------------------------------------------------
        # MODELO 2
        # Random Forest
        # ----------------------------------------------------

        "forest":

            RandomForestClassifier(
                n_estimators=250,
                random_state=RANDOM_STATE,
                n_jobs=-1,
            ),

        # ----------------------------------------------------
        # MODELO 3
        # Red neuronal MLP
        # ----------------------------------------------------

        "mlp": make_pipeline(

            StandardScaler(),

            MLPClassifier(
                hidden_layer_sizes=(
                    64,
                ),
                max_iter=350,
                random_state=RANDOM_STATE,
            ),

        ),

    }

    return modelos


# ============================================================
# GENERAR GRÁFICA DE ACCURACY
# ============================================================

def generar_grafica_accuracy(
    df,
):

    nombres = [
        NOMBRES_MODELOS.get(
            modelo,
            modelo,
        )
        for modelo in df[
            "modelo"
        ]
    ]

    valores = (
        df[
            "accuracy"
        ].to_numpy()
        * 100
    )

    figura, eje = plt.subplots(
        figsize=(
            9,
            5.5,
        )
    )

    barras = eje.bar(
        nombres,
        valores,
        width=0.58,
    )

    eje.set_title(
        "Semana 11 - Accuracy por modelo",
        fontsize=14,
        fontweight="bold",
    )

    eje.set_xlabel(
        "Modelo"
    )

    eje.set_ylabel(
        "Accuracy (%)"
    )

    eje.set_ylim(
        0,
        105,
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
            + barra.get_width()
            / 2,

            barra.get_height()
            + 0.8,

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


# ============================================================
# GENERAR GRÁFICA DE TIEMPOS
# ============================================================

def generar_grafica_tiempos(
    df,
):

    nombres = [
        NOMBRES_MODELOS.get(
            modelo,
            modelo,
        )
        for modelo in df[
            "modelo"
        ]
    ]

    tiempos = (
        df[
            "fit_seconds"
        ].to_numpy()
    )

    figura, eje = plt.subplots(
        figsize=(
            9,
            5.5,
        )
    )

    barras = eje.bar(
        nombres,
        tiempos,
        width=0.58,
    )

    eje.set_title(
        "Semana 11 - Tiempo de entrenamiento",
        fontsize=14,
        fontweight="bold",
    )

    eje.set_xlabel(
        "Modelo"
    )

    eje.set_ylabel(
        "Tiempo (segundos)"
    )

    eje.grid(
        axis="y",
        alpha=0.20,
    )

    eje.set_axisbelow(
        True
    )

    maximo = float(
        max(
            tiempos
        )
    )

    if maximo <= 0:

        maximo = 1.0

    eje.set_ylim(
        0,
        maximo * 1.20,
    )

    for barra, valor in zip(
        barras,
        tiempos,
    ):

        eje.text(
            barra.get_x()
            + barra.get_width()
            / 2,

            barra.get_height()
            + (
                maximo * 0.025
            ),

            f"{valor:.4f} s",

            ha="center",
            va="bottom",

            fontsize=10,
            fontweight="bold",
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


# ============================================================
# GENERAR TODAS LAS GRÁFICAS
# ============================================================

def generar_graficas(
    df,
):

    ruta_accuracy = (
        generar_grafica_accuracy(
            df
        )
    )

    ruta_tiempos = (
        generar_grafica_tiempos(
            df
        )
    )

    return {
        "accuracy":
            ruta_accuracy,

        "tiempos":
            ruta_tiempos,
    }


# ============================================================
# MOSTRAR DISTRIBUCIÓN
# ============================================================

def mostrar_distribucion(
    y,
):

    print(
        "\nDISTRIBUCIÓN DE CLASES"
    )

    for clase in CLASES_ESPERADAS:

        cantidad = int(
            np.sum(
                y == clase
            )
        )

        print(
            f"{clase}: "
            f"{cantidad}"
        )


# ============================================================
# EJECUTAR BENCHMARK
# ============================================================

def ejecutar_benchmark():

    # ========================================================
    # CARGAR DATOS
    # ========================================================

    (
        X,
        y,
        dataset_dir,
    ) = cargar_dataset()

    mostrar_distribucion(
        y
    )

    print(
        "\nFORMA DEL DATASET"
    )

    print(
        f"Imágenes: "
        f"{X.shape[0]}"
    )

    print(
        f"Características: "
        f"{X.shape[1]}"
    )

    print(
        f"Clases: "
        f"{len(np.unique(y))}"
    )

    # ========================================================
    # MISMO SPLIT PARA TODOS LOS MODELOS
    # ========================================================

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_test_split(

        X,
        y,

        test_size=
            TEST_SIZE,

        random_state=
            RANDOM_STATE,

        stratify=
            y,

    )

    print(
        "\nPARTICIÓN"
    )

    print(
        f"Entrenamiento: "
        f"{len(X_train)}"
    )

    print(
        f"Prueba: "
        f"{len(X_test)}"
    )

    print(
        f"Semilla: "
        f"{RANDOM_STATE}"
    )

    # ========================================================
    # CREAR MODELOS
    # ========================================================

    modelos = (
        crear_modelos()
    )

    resultados = []

    # ========================================================
    # ENTRENAR Y EVALUAR
    # ========================================================

    for (
        nombre,
        modelo,
    ) in modelos.items():

        print(
            "\n"
            + "-" * 64
        )

        print(
            "Entrenando: "
            f"{NOMBRES_MODELOS[nombre]}"
        )

        inicio = (
            perf_counter()
        )

        # ----------------------------------------------------
        # Entrenamiento
        # ----------------------------------------------------

        modelo.fit(
            X_train,
            y_train,
        )

        tiempo = (
            perf_counter()
            - inicio
        )

        # ----------------------------------------------------
        # Predicción
        # ----------------------------------------------------

        predicciones = (
            modelo.predict(
                X_test
            )
        )

        # ----------------------------------------------------
        # Accuracy
        # ----------------------------------------------------

        accuracy = (
            accuracy_score(
                y_test,
                predicciones,
            )
        )

        resultados.append(
            {
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
        )

        print(
            "Accuracy: "
            f"{accuracy:.4f}"
        )

        print(
            "Tiempo: "
            f"{tiempo:.4f} s"
        )

    # ========================================================
    # CREAR DATAFRAME
    # ========================================================

    df = pd.DataFrame(
        resultados
    )

    # ========================================================
    # ORDENAR POR ACCURACY
    # ========================================================

    df = df.sort_values(
        by=[
            "accuracy",
            "fit_seconds",
        ],
        ascending=[
            False,
            True,
        ],
    )

    df = df.reset_index(
        drop=True
    )

    # ========================================================
    # GUARDAR CSV
    # ========================================================

    ruta_csv = (
        ARTIFACTS_DIR
        / "benchmark.csv"
    )

    df.to_csv(
        ruta_csv,
        index=False,
    )

    # ========================================================
    # GENERAR GRÁFICAS
    # ========================================================

    graficas = (
        generar_graficas(
            df
        )
    )

    # ========================================================
    # MOSTRAR RESULTADOS
    # ========================================================

    print(
        "\n"
        + "=" * 64
    )

    print(
        "RESULTADOS DEL BENCHMARK"
    )

    print(
        "=" * 64
    )

    print(
        df.to_string(
            index=False
        )
    )

    # ========================================================
    # MODELO GANADOR
    # ========================================================

    mejor_fila = (
        df.iloc[0]
    )

    mejor_modelo = (
        str(
            mejor_fila[
                "modelo"
            ]
        )
    )

    mejor_accuracy = float(
        mejor_fila[
            "accuracy"
        ]
    )

    mejor_tiempo = float(
        mejor_fila[
            "fit_seconds"
        ]
    )

    print(
        "\n"
        + "=" * 64
    )

    print(
        "DECISIÓN DEL BENCHMARK"
    )

    print(
        "=" * 64
    )

    print(
        "Modelo con mayor accuracy:"
    )

    print(
        NOMBRES_MODELOS.get(
            mejor_modelo,
            mejor_modelo,
        )
    )

    print(
        f"Accuracy: "
        f"{mejor_accuracy * 100:.2f}%"
    )

    print(
        f"Tiempo de entrenamiento: "
        f"{mejor_tiempo:.4f} s"
    )

    # ========================================================
    # ARCHIVOS GENERADOS
    # ========================================================

    print(
        "\n"
        + "=" * 64
    )

    print(
        "ARCHIVOS GENERADOS"
    )

    print(
        "=" * 64
    )

    print(
        "\nCSV:"
    )

    print(
        ruta_csv
    )

    print(
        "\nGráfica de accuracy:"
    )

    print(
        graficas[
            "accuracy"
        ]
    )

    print(
        "\nGráfica de tiempos:"
    )

    print(
        graficas[
            "tiempos"
        ]
    )

    print(
        "\nDataset utilizado:"
    )

    print(
        dataset_dir
    )

    print(
        "\nBenchmark completado correctamente."
    )


# ============================================================
# MAIN
# ============================================================

def main():

    try:

        ejecutar_benchmark()

    except KeyboardInterrupt:

        print(
            "\nEjecución cancelada "
            "por el usuario."
        )

    except Exception as error:

        print(
            "\nERROR EN SEMANA 11:"
        )

        print(
            error
        )

        raise


if __name__ == "__main__":

    main()