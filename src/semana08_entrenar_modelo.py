from pathlib import Path
import json
import pickle

import numpy as np
from PIL import Image

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)


# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = (
    ROOT
    / "data"
    / "semana08"
)

ARTIFACTS_DIR = (
    ROOT
    / "artifacts"
)

ARTIFACTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

IMAGE_WIDTH = 64
IMAGE_HEIGHT = 64

TEST_SIZE = 0.25
RANDOM_STATE = 42


# ============================================================
# CATEGORÍAS
# ============================================================

CATEGORIES = {
    "normal": 0,
    "sobrecarga": 1,
    "latencia": 2,
    "disco": 3,
    "critico": 4,
}


CLASS_NAMES = {
    0: "Normal",
    1: "Sobrecarga CPU/RAM",
    2: "Latencia alta",
    3: "Saturación de disco",
    4: "Estado crítico",
}


# ============================================================
# PREPROCESAR IMAGEN
# ============================================================

def preprocess_image(
    image_path,
):

    image = Image.open(
        image_path
    )

    # Escala de grises
    image = image.convert(
        "L"
    )

    # Redimensionar
    image = image.resize(
        (
            IMAGE_WIDTH,
            IMAGE_HEIGHT,
        ),
        Image.Resampling.LANCZOS,
    )

    # Convertir a array
    image_array = np.array(
        image,
        dtype=np.float32,
    )

    # Normalizar entre 0 y 1
    image_array = (
        image_array
        / 255.0
    )

    # Convertir:
    #
    # 64 x 64
    # ↓
    # 4096 valores
    vector = image_array.flatten()

    return vector


# ============================================================
# CARGAR DATASET
# ============================================================

def load_dataset():

    features = []
    labels = []

    print()

    print(
        "=" * 65
    )

    print(
        "CARGANDO DATASET SEMANA 8"
    )

    print(
        "=" * 65
    )


    for (
        folder_name,
        label,
    ) in CATEGORIES.items():

        folder = (
            DATASET_DIR
            / folder_name
        )


        if not folder.exists():

            raise FileNotFoundError(
                f"No existe la carpeta: "
                f"{folder}"
            )


        images = sorted(
            folder.glob(
                "*.png"
            )
        )


        print(
            f"{folder_name:<15} "
            f"{len(images)} imágenes"
        )


        for image_path in images:

            vector = preprocess_image(
                image_path
            )

            features.append(
                vector
            )

            labels.append(
                label
            )


    X = np.array(
        features,
        dtype=np.float32,
    )

    y = np.array(
        labels,
        dtype=np.int64,
    )


    print()

    print(
        f"Total imágenes: "
        f"{len(X)}"
    )

    print(
        f"Características por imagen: "
        f"{X.shape[1]}"
    )


    return (
        X,
        y,
    )


# ============================================================
# ENTRENAR MODELO
# ============================================================

def train_model(
    X,
    y,
):

    # --------------------------------------------------------
    # División 75% entrenamiento / 25% prueba
    # --------------------------------------------------------

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


    print()

    print(
        "=" * 65
    )

    print(
        "DIVISIÓN DEL DATASET"
    )

    print(
        "=" * 65
    )

    print(
        f"Entrenamiento: "
        f"{len(X_train)} imágenes"
    )

    print(
        f"Prueba: "
        f"{len(X_test)} imágenes"
    )


    # --------------------------------------------------------
    # Red neuronal
    # --------------------------------------------------------

    model = MLPClassifier(

        # Dos capas ocultas
        hidden_layer_sizes=(
            128,
            64,
        ),

        # Función de activación
        activation="relu",

        # Optimizador
        solver="adam",

        # Regularización
        alpha=0.0005,

        # Máximo de iteraciones
        max_iter=500,

        # Detener entrenamiento cuando
        # deja de mejorar
        early_stopping=True,

        validation_fraction=0.15,

        n_iter_no_change=25,

        random_state=RANDOM_STATE,

        verbose=False,
    )


    print()

    print(
        "=" * 65
    )

    print(
        "ENTRENANDO RED NEURONAL"
    )

    print(
        "=" * 65
    )

    print(
        "MLPClassifier"
    )

    print(
        f"Entradas: "
        f"{IMAGE_WIDTH * IMAGE_HEIGHT} valores"
    )

    print(
        "Primera capa oculta: "
        "128 neuronas"
    )

    print(
        "Segunda capa oculta: "
        "64 neuronas"
    )

    print(
        "Clases de salida: 5"
    )

    print()


    model.fit(
        X_train,
        y_train,
    )


    # --------------------------------------------------------
    # Predicción
    # --------------------------------------------------------

    predictions = model.predict(
        X_test
    )


    accuracy = accuracy_score(
        y_test,
        predictions,
    )


    return (
        model,
        X_train,
        X_test,
        y_train,
        y_test,
        predictions,
        accuracy,
    )


# ============================================================
# MOSTRAR RESULTADOS
# ============================================================

def show_results(
    y_test,
    predictions,
    accuracy,
):

    print()

    print(
        "=" * 65
    )

    print(
        "RESULTADOS DEL MODELO"
    )

    print(
        "=" * 65
    )

    print()

    print(
        f"Accuracy: "
        f"{accuracy:.4f}"
    )

    print(
        f"Accuracy: "
        f"{accuracy * 100:.2f}%"
    )

    print()


    print(
        "REPORTE POR CLASE"
    )

    print(
        "-" * 65
    )


    target_names = [
        CLASS_NAMES[index]
        for index in sorted(
            CLASS_NAMES.keys()
        )
    ]


    print(
        classification_report(
            y_test,
            predictions,
            target_names=target_names,
            digits=2,
        )
    )


    print(
        "MATRIZ DE CONFUSIÓN"
    )

    print(
        "-" * 65
    )


    print(
        confusion_matrix(
            y_test,
            predictions,
        )
    )


# ============================================================
# GUARDAR MODELO
# ============================================================

def save_model(
    model,
    accuracy,
    train_size,
    test_size,
):

    model_path = (
        ARTIFACTS_DIR
        / "modelo_mlp.pkl"
    )


    config_path = (
        ARTIFACTS_DIR
        / "modelo_config.json"
    )


    # --------------------------------------------------------
    # Guardar modelo
    # --------------------------------------------------------

    with model_path.open(
        "wb"
    ) as file:

        pickle.dump(
            model,
            file,
        )


    # --------------------------------------------------------
    # Guardar configuración
    # --------------------------------------------------------

    config = {

        "image_width": (
            IMAGE_WIDTH
        ),

        "image_height": (
            IMAGE_HEIGHT
        ),

        "input_features": (
            IMAGE_WIDTH
            * IMAGE_HEIGHT
        ),

        "hidden_layers": [
            128,
            64,
        ],

        "classes": {
            str(key): value
            for (
                key,
                value,
            ) in CLASS_NAMES.items()
        },

        "accuracy": round(
            float(
                accuracy
            ),
            4,
        ),

        "training_images": int(
            train_size
        ),

        "test_images": int(
            test_size
        ),
    }


    config_path.write_text(
        json.dumps(
            config,
            ensure_ascii=False,
            indent=4,
        ),
        encoding="utf-8",
    )


    print()

    print(
        "Modelo guardado:"
    )

    print(
        model_path
    )

    print()

    print(
        "Configuración guardada:"
    )

    print(
        config_path
    )


# ============================================================
# MAIN
# ============================================================

def main():

    X, y = load_dataset()


    (
        model,
        X_train,
        X_test,
        y_train,
        y_test,
        predictions,
        accuracy,
    ) = train_model(
        X,
        y,
    )


    show_results(
        y_test,
        predictions,
        accuracy,
    )


    save_model(
        model,
        accuracy,
        len(X_train),
        len(X_test),
    )


    print()

    print(
        "=" * 65
    )

    print(
        "ENTRENAMIENTO COMPLETADO"
    )

    print(
        "=" * 65
    )


if __name__ == "__main__":

    main()