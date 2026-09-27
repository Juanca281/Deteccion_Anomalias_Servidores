from pathlib import Path
import argparse
import json
import pickle

import numpy as np
from PIL import Image


# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

ARTIFACTS_DIR = ROOT / "artifacts"

MODEL_PATH = ARTIFACTS_DIR / "modelo_mlp.pkl"

CONFIG_PATH = ARTIFACTS_DIR / "modelo_config.json"


# ============================================================
# CLASES
# ============================================================

CLASS_NAMES = {
    0: "Normal",
    1: "Sobrecarga CPU/RAM",
    2: "Latencia alta",
    3: "Saturación de disco",
    4: "Estado crítico",
}


# ============================================================
# CARGAR CONFIGURACIÓN
# ============================================================

def load_config():

    if not CONFIG_PATH.exists():

        raise FileNotFoundError(
            "No existe modelo_config.json."
        )

    return json.loads(
        CONFIG_PATH.read_text(
            encoding="utf-8"
        )
    )


# ============================================================
# CARGAR MODELO
# ============================================================

def load_model():

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            "No existe modelo_mlp.pkl. "
            "Primero debes entrenar el modelo."
        )

    with MODEL_PATH.open(
        "rb"
    ) as file:

        model = pickle.load(
            file
        )

    return model


# ============================================================
# PREPROCESAR IMAGEN
# ============================================================

def preprocess_image(
    image_path,
    width,
    height,
):

    image_path = Path(
        image_path
    )

    if not image_path.exists():

        raise FileNotFoundError(
            f"No existe la imagen: "
            f"{image_path}"
        )

    image = Image.open(
        image_path
    )

    # Convertir a escala de grises

    image = image.convert(
        "L"
    )

    # Aplicar exactamente el mismo tamaño
    # utilizado durante el entrenamiento

    image = image.resize(
        (
            width,
            height,
        ),
        Image.Resampling.LANCZOS,
    )

    # Convertir a números

    image_array = np.array(
        image,
        dtype=np.float32,
    )

    # Normalizar entre 0 y 1

    image_array = (
        image_array
        / 255.0
    )

    # 32 x 32
    # ↓
    # 1024 valores

    vector = image_array.flatten()

    # El modelo espera una colección
    # de muestras

    return vector.reshape(
        1,
        -1,
    )


# ============================================================
# REALIZAR PREDICCIÓN
# ============================================================

def predict_image(
    image_path,
):

    config = load_config()

    model = load_model()

    width = config[
        "image_width"
    ]

    height = config[
        "image_height"
    ]

    vector = preprocess_image(
        image_path,
        width,
        height,
    )


    # ========================================================
    # CLASE PREDICHA
    # ========================================================

    prediction = int(
        model.predict(
            vector
        )[0]
    )


    # ========================================================
    # PROBABILIDADES
    # ========================================================

    probabilities = (
        model.predict_proba(
            vector
        )[0]
    )


    confidence = float(
        np.max(
            probabilities
        )
    )


    predicted_class = (
        CLASS_NAMES[
            prediction
        ]
    )


    # ========================================================
    # RESULTADOS POR CLASE
    # ========================================================

    class_probabilities = {}

    for (
        class_id,
        probability,
    ) in zip(
        model.classes_,
        probabilities,
    ):

        class_probabilities[
            CLASS_NAMES[
                int(class_id)
            ]
        ] = round(
            float(
                probability
            )
            * 100,
            2,
        )


    return {
        "image": str(
            image_path
        ),
        "class_id": prediction,
        "prediction": (
            predicted_class
        ),
        "confidence": round(
            confidence * 100,
            2,
        ),
        "probabilities": (
            class_probabilities
        ),
    }


# ============================================================
# MOSTRAR RESULTADO
# ============================================================

def show_result(
    result,
):

    print()

    print(
        "=" * 65
    )

    print(
        "SEMANA 8 - RECONOCIMIENTO DE IMAGEN"
    )

    print(
        "=" * 65
    )

    print()

    print(
        f"Imagen:"
    )

    print(
        result[
            "image"
        ]
    )

    print()

    print(
        f"Predicción: "
        f"{result['prediction']}"
    )

    print(
        f"Confianza: "
        f"{result['confidence']:.2f}%"
    )

    print()

    print(
        "PROBABILIDAD POR CLASE"
    )

    print(
        "-" * 65
    )


    ordered = sorted(
        result[
            "probabilities"
        ].items(),
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

    print(
        "=" * 65
    )


# ============================================================
# ARGUMENTOS
# ============================================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        description=(
            "Clasifica una gráfica "
            "de monitoreo de servidor."
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

        result = predict_image(
            args.imagen
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

        print(
            json.dumps(
                {
                    "success": False,
                    "error": str(
                        error
                    ),
                },
                ensure_ascii=False,
                indent=4,
            )
        )

        raise SystemExit(1)


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    main()