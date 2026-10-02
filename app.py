import json
import os
import subprocess
import sys
import uuid

from pathlib import Path

from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory,
)
from werkzeug.utils import secure_filename

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

ROOT = Path(__file__).resolve().parent

FRONTEND_DIR = ROOT / "frontend"


app = Flask(__name__)

# ============================================================
# SEMANA 8 - CONFIGURACIÓN
# ============================================================

SEMANA8_UPLOADS = (
    ROOT
    / "data"
    / "semana08"
    / "cargas"
)

SEMANA8_UPLOADS.mkdir(
    parents=True,
    exist_ok=True,
)

ALLOWED_IMAGE_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
}

# Máximo 10 MB por imagen
app.config[
    "MAX_CONTENT_LENGTH"
] = 10 * 1024 * 1024

app.json.ensure_ascii = False


@app.errorhandler(413)
def image_too_large(_error):
    return jsonify(
        {
            "success": False,
            "error": "La imagen supera el tamaño máximo permitido de 10 MB.",
        }
    ), 413


def allowed_image_file(
    filename,
):

    return (
        "."
        in filename

        and filename
        .rsplit(
            ".",
            1,
        )[1]
        .lower()

        in ALLOWED_IMAGE_EXTENSIONS
    )

# ============================================================
# SEMANA 9 - CONFIGURACIÓN
# ============================================================

SEMANA9_UPLOADS = (
    ROOT
    / "data"
    / "semana09"
    / "cargas"
)

SEMANA9_UPLOADS.mkdir(
    parents=True,
    exist_ok=True,
)

# ============================================================
# SCRIPTS AUTORIZADOS
# ============================================================

SCRIPTS = {

    "semana2":
        ROOT
        / "src"
        / "semana02_fundamentos.py",

    "semana3":
        ROOT
        / "src"
        / "semana03_taxonomia.py",

    "semana4_astar":
        ROOT
        / "src"
        / "semana04_astar.py",

    "semana4_minimax":
        ROOT
        / "src"
        / "semana04_minimax.py",

    "semana5":
        ROOT
        / "src"
        / "semana05_sistema_hibrido.py",

    "semana7":
        ROOT
        / "src"
        / "semana07_representaciones.py",
}


# ============================================================
# DIRECTORIOS AUTORIZADOS PARA VISUALIZAR ARCHIVOS
# ============================================================

ALLOWED_DIRECTORIES = [

    ROOT / "src",

    ROOT / "reports",

    ROOT / "data",
]


# ============================================================
# FRONTEND PRINCIPAL
# ============================================================

@app.route("/")
def index():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# ============================================================
# ARCHIVOS DEL FRONTEND
# ============================================================

@app.route(
    "/frontend/<path:filename>"
)
def frontend_files(filename):

    return send_from_directory(
        FRONTEND_DIR,
        filename
    )


# ============================================================
# VISUALIZAR ARCHIVOS DEL PROYECTO
# ============================================================

@app.route(
    "/project/<path:filename>"
)
def project_file(filename):

    requested_file = (
        ROOT / filename
    ).resolve()


    allowed = False


    for directory in ALLOWED_DIRECTORIES:

        directory = (
            directory.resolve()
        )

        try:

            requested_file.relative_to(
                directory
            )

            allowed = True

            break

        except ValueError:

            continue


    # ========================================================
    # VALIDAR DIRECTORIO
    # ========================================================

    if not allowed:

        return jsonify(
            {
                "error":
                    "Archivo no autorizado."
            }
        ), 403


    # ========================================================
    # VALIDAR EXISTENCIA
    # ========================================================

    if not requested_file.exists():

        return jsonify(
            {
                "error":
                    f"No existe el archivo: "
                    f"{filename}"
            }
        ), 404


    # ========================================================
    # VALIDAR QUE SEA ARCHIVO
    # ========================================================

    if not requested_file.is_file():

        return jsonify(
            {
                "error":
                    "La ruta no corresponde "
                    "a un archivo."
            }
        ), 400


    return send_from_directory(
        requested_file.parent,
        requested_file.name
    )


# ============================================================
# EJECUCIÓN GENERAL DE SCRIPTS
# ============================================================

@app.route(
    "/api/run/<script_name>",
    methods=["POST"]
)
def run_script(script_name):

    # ========================================================
    # VALIDAR SCRIPT
    # ========================================================

    if script_name not in SCRIPTS:

        return jsonify(
            {
                "success": False,
                "error":
                    "Script no autorizado."
            }
        ), 404


    script_path = SCRIPTS[
        script_name
    ]


    # ========================================================
    # VALIDAR EXISTENCIA
    # ========================================================

    if not script_path.exists():

        return jsonify(
            {
                "success": False,
                "error":
                    f"No existe el archivo "
                    f"{script_path.name}"
            }
        ), 404


    try:

        # ====================================================
        # UTF-8
        # ====================================================

        env = os.environ.copy()

        env["PYTHONUTF8"] = "1"

        env["PYTHONIOENCODING"] = (
            "utf-8"
        )


        # ====================================================
        # EJECUTAR
        # ====================================================

        process = subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                str(script_path)
            ],

            cwd=ROOT,

            capture_output=True,

            text=True,

            encoding="utf-8",

            errors="replace",

            timeout=60,

            env=env
        )


        stdout = (
            process.stdout.strip()
            if process.stdout
            else ""
        )


        stderr = (
            process.stderr.strip()
            if process.stderr
            else ""
        )


        success = (
            process.returncode == 0
        )


        return jsonify(
            {
                "success":
                    success,

                "script":
                    script_path.name,

                "returncode":
                    process.returncode,

                "stdout":
                    stdout,

                "stderr":
                    stderr
            }
        )


    except subprocess.TimeoutExpired:

        return jsonify(
            {
                "success": False,
                "error":
                    "La ejecución superó "
                    "el tiempo máximo permitido."
            }
        ), 408


    except Exception as error:

        return jsonify(
            {
                "success": False,
                "error":
                    str(error)
            }
        ), 500


# ============================================================
# SEMANA 7
# EJECUCIÓN CON DATOS INGRESADOS DESDE EL FRONTEND
# ============================================================

@app.route("/api/semana7", methods=["POST"])
def run_semana7():

    data = request.get_json(
        silent=True
    ) or {}


    # ========================================================
    # OBTENER OBSERVACIONES
    # ========================================================

    observations = data.get(
        "observaciones"
    )


    if not isinstance(
        observations,
        list
    ):

        return jsonify({
            "success": False,
            "error": (
                "Debe enviarse una lista "
                "de observaciones."
            )
        }), 400


    if len(observations) == 0:

        return jsonify({
            "success": False,
            "error": (
                "Debe existir al menos "
                "una observación."
            )
        }), 400


    # ========================================================
    # VALIDACIÓN BÁSICA
    # ========================================================

    required_fields = {
        "cpu",
        "ram",
        "disco",
        "latencia",
        "solicitudes",
        "errores",
        "estado",
    }


    for index, observation in enumerate(
        observations,
        start=1
    ):

        if not isinstance(
            observation,
            dict
        ):

            return jsonify({
                "success": False,
                "error": (
                    f"La lectura {index} "
                    "no tiene un formato válido."
                )
            }), 400


        missing_fields = (
            required_fields
            - observation.keys()
        )


        if missing_fields:

            return jsonify({
                "success": False,
                "error": (
                    f"La lectura {index} "
                    "tiene campos faltantes: "
                    + ", ".join(
                        sorted(
                            missing_fields
                        )
                    )
                )
            }), 400


    # ========================================================
    # SCRIPT SEMANA 7
    # ========================================================

    script_path = SCRIPTS[
        "semana7"
    ]


    if not script_path.exists():

        return jsonify({
            "success": False,
            "error": (
                "No existe el script "
                "de Semana 7."
            )
        }), 404


    # ========================================================
    # PREPARAR JSON PARA PYTHON
    # ========================================================

    observations_json = json.dumps(
        observations,
        ensure_ascii=False
    )


    env = os.environ.copy()

    env["PYTHONUTF8"] = "1"

    env["PYTHONIOENCODING"] = "utf-8"


    try:

        # ====================================================
        # EJECUTAR SEMANA 7
        # ====================================================

        process = subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                str(script_path),

                "--observaciones",
                observations_json,

                "--json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            env=env
        )


        stdout = (
            process.stdout.strip()
            if process.stdout
            else ""
        )


        stderr = (
            process.stderr.strip()
            if process.stderr
            else ""
        )


        # ====================================================
        # ERROR DE PYTHON
        # ====================================================

        if process.returncode != 0:

            error_message = stderr


            # Intentar leer el error JSON
            # generado por semana07_representaciones.py

            if stdout:

                try:

                    error_data = json.loads(
                        stdout
                    )


                    error_message = (
                        error_data.get(
                            "error"
                        )
                        or error_message
                    )

                except json.JSONDecodeError:
                    pass


            return jsonify({
                "success": False,
                "error": (
                    error_message
                    or "El análisis presentó un error."
                ),
                "stderr": stderr
            }), 500


        # ====================================================
        # CONVERTIR RESULTADO A JSON
        # ====================================================

        try:

            analysis = json.loads(
                stdout
            )


        except json.JSONDecodeError:

            return jsonify({
                "success": False,
                "error": (
                    "Semana 7 se ejecutó, "
                    "pero no devolvió un JSON válido."
                ),
                "stdout": stdout
            }), 500


        # ====================================================
        # RESPUESTA AL FRONTEND
        # ====================================================

        return jsonify({
            "success": True,
            "analysis": analysis
        })


    except subprocess.TimeoutExpired:

        return jsonify({
            "success": False,
            "error": (
                "La ejecución de Semana 7 "
                "superó el tiempo máximo permitido."
            )
        }), 408


    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500

# ============================================================
# API - SEMANA 8
# Reconocimiento de imágenes + SQLite + Ontología
# ============================================================

@app.route(
    "/api/semana8",
    methods=[
        "POST"
    ],
)
def api_semana8():

    try:

        # ====================================================
        # VALIDAR ARCHIVO
        # ====================================================

        if (
            "imagen"
            not in request.files
        ):

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "No se recibió "
                        "ninguna imagen."
                    ),
                }
            ), 400


        image = request.files[
            "imagen"
        ]


        if not image.filename:

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "La imagen no "
                        "tiene nombre."
                    ),
                }
            ), 400


        # ====================================================
        # VALIDAR EXTENSIÓN
        # ====================================================

        if not allowed_image_file(
            image.filename
        ):

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "Formato no permitido. "
                        "Utiliza PNG, JPG o JPEG."
                    ),
                }
            ), 400


        # ====================================================
        # CREAR NOMBRE SEGURO
        # ====================================================

        original_name = secure_filename(
            image.filename
        )


        unique_id = (
            uuid.uuid4()
            .hex[:12]
        )


        stored_name = (
            f"{unique_id}_"
            f"{original_name}"
        )


        image_path = (
            SEMANA8_UPLOADS
            / stored_name
        )


        # ====================================================
        # GUARDAR IMAGEN
        # ====================================================

        image.save(
            image_path
        )


        # ====================================================
        # EJECUTAR ANÁLISIS INTEGRADO
        # ====================================================

        script_path = (
            ROOT
            / "src"
            / "semana08_analisis.py"
        )


        process = subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                str(
                    script_path
                ),
                str(
                    image_path
                ),
                "--json",
            ],
            cwd=str(
                ROOT
            ),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )


        stdout = (
            process.stdout.strip()
        )


        stderr = (
            process.stderr.strip()
        )


        # ====================================================
        # VALIDAR EJECUCIÓN
        # ====================================================

        if not stdout:

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "El análisis no "
                        "devolvió información."
                    ),
                    "detail": stderr,
                }
            ), 500


        # ====================================================
        # CONVERTIR JSON
        # ====================================================

        try:

            analysis = json.loads(
                stdout
            )

        except json.JSONDecodeError:

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "El análisis devolvió "
                        "una respuesta inválida."
                    ),
                    "stdout": stdout,
                    "stderr": stderr,
                }
            ), 500


        # ====================================================
        # ERROR DEVUELTO POR EL SCRIPT
        # ====================================================

        if not analysis.get(
            "success",
            False,
        ):

            return jsonify(
                analysis
            ), 400


        # ====================================================
        # INFORMACIÓN ADICIONAL
        # ====================================================

        analysis[
            "upload"
        ] = {
            "original_name": (
                image.filename
            ),
            "stored_name": (
                stored_name
            ),
        }


        # ====================================================
        # RESPUESTA
        # ====================================================

        return jsonify(
            analysis
        )


    except subprocess.TimeoutExpired:

        return jsonify(
            {
                "success": False,
                "error": (
                    "El análisis superó "
                    "el tiempo máximo permitido."
                ),
            }
        ), 504


    except Exception as error:

        return jsonify(
            {
                "success": False,
                "error": str(
                    error
                ),
            }
        ), 500


# ============================================================
# API - SEMANA 9
# Canny + Otsu + Regiones conectadas
# ============================================================

@app.route(
    "/api/semana9",
    methods=["POST"],
)
def api_semana9():

    try:

        # ====================================================
        # VALIDAR IMAGEN
        # ====================================================

        if "imagen" not in request.files:

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "No se recibió ninguna imagen."
                    ),
                }
            ), 400


        image = request.files[
            "imagen"
        ]


        if not image.filename:

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "La imagen no tiene nombre."
                    ),
                }
            ), 400


        # ====================================================
        # VALIDAR EXTENSIÓN
        # ====================================================

        if not allowed_image_file(
            image.filename
        ):

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "Formato no permitido. "
                        "Utiliza PNG, JPG o JPEG."
                    ),
                }
            ), 400


        # ====================================================
        # PARÁMETROS
        # ====================================================

        try:

            sigma = float(
                request.form.get(
                    "sigma",
                    2.0,
                )
            )

        except ValueError:

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "El valor de sigma "
                        "no es válido."
                    ),
                }
            ), 400


        try:

            min_area = int(
                request.form.get(
                    "min_area",
                    50,
                )
            )

        except ValueError:

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "El área mínima "
                        "no es válida."
                    ),
                }
            ), 400


        # ====================================================
        # VALIDACIONES
        # ====================================================

        if sigma <= 0:

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "Sigma debe ser "
                        "mayor que 0."
                    ),
                }
            ), 400


        if min_area < 1:

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "El área mínima debe "
                        "ser mayor que 0."
                    ),
                }
            ), 400


        # ====================================================
        # NOMBRE SEGURO
        # ====================================================

        original_name = secure_filename(
            image.filename
        )


        unique_id = (
            uuid.uuid4()
            .hex[:12]
        )


        stored_name = (
            f"{unique_id}_"
            f"{original_name}"
        )


        image_path = (
            SEMANA9_UPLOADS
            / stored_name
        )


        # ====================================================
        # GUARDAR IMAGEN
        # ====================================================

        image.save(
            image_path
        )


        # ====================================================
        # SCRIPT SEMANA 9
        # ====================================================

        script_path = (
            ROOT
            / "src"
            / "semana09_analisis.py"
        )


        process = subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                str(script_path),
                str(image_path),

                "--sigma",
                str(sigma),

                "--min-area",
                str(min_area),

                "--json",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )


        stdout = (
            process.stdout.strip()
        )


        stderr = (
            process.stderr.strip()
        )


        # ====================================================
        # VALIDAR RESPUESTA
        # ====================================================

        if not stdout:

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "Semana 9 no devolvió "
                        "información."
                    ),
                    "detail": stderr,
                }
            ), 500


        # ====================================================
        # CONVERTIR JSON
        # ====================================================

        try:

            analysis = json.loads(
                stdout
            )

        except json.JSONDecodeError:

            return jsonify(
                {
                    "success": False,
                    "error": (
                        "Semana 9 devolvió una "
                        "respuesta inválida."
                    ),
                    "stdout": stdout,
                    "stderr": stderr,
                }
            ), 500


        # ====================================================
        # ERROR DEL SCRIPT
        # ====================================================

        if not analysis.get(
            "success",
            False,
        ):

            return jsonify(
                analysis
            ), 400


        # ====================================================
        # INFORMACIÓN DE CARGA
        # ====================================================

        analysis[
            "upload"
        ] = {

            "original_name": (
                image.filename
            ),

            "stored_name": (
                stored_name
            ),
        }


        return jsonify(
            analysis
        )


    except subprocess.TimeoutExpired:

        return jsonify(
            {
                "success": False,
                "error": (
                    "El procesamiento superó "
                    "el tiempo máximo permitido."
                ),
            }
        ), 504


    except Exception as error:

        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 500


    # ============================================================
    # ARCHIVOS GENERADOS
    # ============================================================

@app.route(
    "/artifacts/<path:filename>"
)
def serve_artifact(filename):

    return send_from_directory(
        ROOT / "artifacts",
        filename
    )

# ============================================================
# ESTADO DEL BACKEND
# ============================================================

@app.route(
    "/api/status"
)
def status():

    available_scripts = {
        name: path.exists()
        for name, path in SCRIPTS.items()
    }

    available_scripts.update(
        {
            "semana8": (ROOT / "src" / "semana08_analisis.py").exists(),
            "semana9": (ROOT / "src" / "semana09_analisis.py").exists(),
        }
    )

    return jsonify(
        {
            "status": "ok",
            "python": sys.version,
            "python_executable": sys.executable,
            "encoding": "utf-8",
            "current_week": 9,
            "scripts": available_scripts,
        }
    )

# ============================================================
# INICIAR SERVIDOR
# ============================================================

if __name__ == "__main__":

    print(
        "=" * 70
    )

    print(
        "PROYECTO IA - DETECCIÓN DE ANOMALÍAS EN SERVIDORES"
    )

    print(
        "=" * 70
    )


    print()

    print(
        "Frontend disponible en:"
    )

    print(
        "http://localhost:5000"
    )


    print()

    print(
        "Codificación de ejecución: UTF-8"
    )


    print()

    print(
        "Scripts disponibles:"
    )


    for name, path in SCRIPTS.items():

        status_text = (
            "OK"
            if path.exists()
            else "NO ENCONTRADO"
        )

        print(
            f"  {name}: {status_text}"
        )


    print()

    print(
        "=" * 70
    )


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
