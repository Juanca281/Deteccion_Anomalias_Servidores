from pathlib import Path
from datetime import datetime
import argparse
import json
import sqlite3

from semana08_predecir_imagen import predict_image


# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

ARTIFACTS_DIR = ROOT / "artifacts"

DATABASE_PATH = (
    ARTIFACTS_DIR
    / "imagenes.db"
)


# ============================================================
# CREAR BASE DE DATOS
# ============================================================

def initialize_database():

    ARTIFACTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS evidencias (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre_imagen TEXT NOT NULL,

            ruta_imagen TEXT NOT NULL,

            clase_id INTEGER NOT NULL,

            prediccion TEXT NOT NULL,

            confianza REAL NOT NULL,

            nivel_confianza TEXT NOT NULL,

            probabilidades TEXT NOT NULL,

            fecha_analisis TEXT NOT NULL

        )
        """
    )


    connection.commit()

    connection.close()


# ============================================================
# DETERMINAR NIVEL DE CONFIANZA
# ============================================================

def get_confidence_level(
    confidence,
):

    if confidence >= 55:

        return "Confiable"


    if confidence >= 40:

        return "Moderada"


    return "No concluyente"


# ============================================================
# GUARDAR EVIDENCIA
# ============================================================

def save_evidence(
    result,
):

    initialize_database()


    image_path = Path(
        result["image"]
    )


    confidence = float(
        result["confidence"]
    )


    confidence_level = (
        get_confidence_level(
            confidence
        )
    )


    probabilities_json = json.dumps(
        result["probabilities"],
        ensure_ascii=False,
    )


    analysis_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO evidencias (

            nombre_imagen,
            ruta_imagen,
            clase_id,
            prediccion,
            confianza,
            nivel_confianza,
            probabilidades,
            fecha_analisis

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            image_path.name,

            str(
                image_path
            ),

            result[
                "class_id"
            ],

            result[
                "prediction"
            ],

            confidence,

            confidence_level,

            probabilities_json,

            analysis_date,
        ),
    )


    evidence_id = (
        cursor.lastrowid
    )


    connection.commit()

    connection.close()


    return {
        "id": evidence_id,
        "image": image_path.name,
        "prediction": result[
            "prediction"
        ],
        "confidence": confidence,
        "confidence_level": (
            confidence_level
        ),
        "probabilities": result[
            "probabilities"
        ],
        "date": analysis_date,
    }


# ============================================================
# ANALIZAR Y REGISTRAR IMAGEN
# ============================================================

def analyze_and_save(
    image_path,
):

    # --------------------------------------------------------
    # 1. Red neuronal
    # --------------------------------------------------------

    prediction = predict_image(
        image_path
    )


    # --------------------------------------------------------
    # 2. Guardar evidencia
    # --------------------------------------------------------

    evidence = save_evidence(
        prediction
    )


    return evidence


# ============================================================
# OBTENER EVIDENCIAS
# ============================================================

def get_evidences():

    initialize_database()


    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = (
        sqlite3.Row
    )


    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT

            id,
            nombre_imagen,
            prediccion,
            confianza,
            nivel_confianza,
            fecha_analisis

        FROM evidencias

        ORDER BY id DESC
        """
    )


    rows = cursor.fetchall()

    connection.close()


    return [
        dict(row)
        for row in rows
    ]


# ============================================================
# MOSTRAR EVIDENCIA
# ============================================================

def show_evidence(
    evidence,
):

    print()

    print(
        "=" * 65
    )

    print(
        "SEMANA 8 - REGISTRO DE EVIDENCIA"
    )

    print(
        "=" * 65
    )

    print()

    print(
        f"ID evidencia: "
        f"{evidence['id']}"
    )

    print(
        f"Imagen: "
        f"{evidence['image']}"
    )

    print(
        f"Predicción: "
        f"{evidence['prediction']}"
    )

    print(
        f"Confianza: "
        f"{evidence['confidence']:.2f}%"
    )

    print(
        f"Nivel: "
        f"{evidence['confidence_level']}"
    )

    print(
        f"Fecha: "
        f"{evidence['date']}"
    )


    print()

    print(
        "PROBABILIDADES"
    )

    print(
        "-" * 65
    )


    ordered = sorted(
        evidence[
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
        "Evidencia almacenada en:"
    )

    print(
        DATABASE_PATH
    )

    print()

    print(
        "=" * 65
    )


# ============================================================
# MOSTRAR HISTORIAL
# ============================================================

def show_history():

    evidences = get_evidences()


    print()

    print(
        "=" * 80
    )

    print(
        "HISTORIAL DE EVIDENCIAS - SEMANA 8"
    )

    print(
        "=" * 80
    )


    if not evidences:

        print()

        print(
            "No existen evidencias registradas."
        )

        return


    print()

    print(
        f"{'ID':<5}"
        f"{'IMAGEN':<30}"
        f"{'PREDICCIÓN':<25}"
        f"{'CONFIANZA':<12}"
        f"{'NIVEL'}"
    )

    print(
        "-" * 100
    )


    for evidence in evidences:

        print(
            f"{evidence['id']:<5}"
            f"{evidence['nombre_imagen']:<30}"
            f"{evidence['prediccion']:<25}"
            f"{evidence['confianza']:<12.2f}"
            f"{evidence['nivel_confianza']}"
        )


    print()


# ============================================================
# ARGUMENTOS
# ============================================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        description=(
            "Analiza imágenes y registra "
            "evidencias en SQLite."
        )
    )


    parser.add_argument(
        "imagen",
        nargs="?",
        help=(
            "Ruta de la imagen "
            "que se desea analizar."
        ),
    )


    parser.add_argument(
        "--listar",
        action="store_true",
        help=(
            "Mostrar evidencias "
            "almacenadas."
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

        # ----------------------------------------------------
        # LISTAR EVIDENCIAS
        # ----------------------------------------------------

        if args.listar:

            show_history()

            return


        # ----------------------------------------------------
        # VALIDAR IMAGEN
        # ----------------------------------------------------

        if not args.imagen:

            print(
                "Debes indicar una imagen "
                "o utilizar --listar."
            )

            return


        # ----------------------------------------------------
        # ANALIZAR Y REGISTRAR
        # ----------------------------------------------------

        evidence = analyze_and_save(
            args.imagen
        )


        # ----------------------------------------------------
        # SALIDA JSON
        # ----------------------------------------------------

        if args.json:

            print(
                json.dumps(
                    evidence,
                    ensure_ascii=False,
                    indent=4,
                )
            )

        else:

            show_evidence(
                evidence
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