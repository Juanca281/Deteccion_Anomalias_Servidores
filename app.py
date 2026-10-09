import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT / "frontend"
SRC_DIR = ROOT / "src"
ARTIFACTS_DIR = ROOT / "artifacts"

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.json.ensure_ascii = False

ALLOWED_IMAGE_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
}


# ============================================================
# CARPETAS DE CARGA
# ============================================================

SEMANA8_UPLOADS = ROOT / "data" / "semana08" / "cargas"
SEMANA9_UPLOADS = ROOT / "data" / "semana09" / "cargas"
SEMANA10_UPLOADS = ROOT / "data" / "semana10" / "cargas"

for upload_dir in (
    SEMANA8_UPLOADS,
    SEMANA9_UPLOADS,
    SEMANA10_UPLOADS,
):
    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


# ============================================================
# SCRIPTS DEL PROYECTO
# ============================================================

SCRIPTS = {
    "semana2": SRC_DIR / "semana02_fundamentos.py",
    "semana3": SRC_DIR / "semana03_taxonomia.py",
    "semana4_astar": SRC_DIR / "semana04_astar.py",
    "semana4_minimax": SRC_DIR / "semana04_minimax.py",
    "semana5": SRC_DIR / "semana05_sistema_hibrido.py",
    "semana7": SRC_DIR / "semana07_representaciones.py",
}

SEMANA8_SCRIPT = SRC_DIR / "semana08_analisis.py"
SEMANA9_SCRIPT = SRC_DIR / "semana09_analisis.py"
SEMANA10_SCRIPT = SRC_DIR / "semana10_texturas.py"


# ============================================================
# DIRECTORIOS VISIBLES DESDE /project
# ============================================================

ALLOWED_DIRECTORIES = [
    SRC_DIR,
    ROOT / "reports",
    ROOT / "data",
]


# ============================================================
# UTILIDADES
# ============================================================

def allowed_image_file(filename):
    """Valida imágenes PNG, JPG y JPEG."""

    return (
        bool(filename)
        and "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_IMAGE_EXTENSIONS
    )


def python_environment():
    """Fuerza UTF-8 en los scripts ejecutados por Flask."""

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    return env


def run_python_script(arguments, timeout=120):
    """Ejecuta un script Python del proyecto y captura su salida."""

    return subprocess.run(
        [
            sys.executable,
            "-X",
            "utf8",
            *[str(argument) for argument in arguments],
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        env=python_environment(),
    )


def save_uploaded_image(upload_dir):
    """
    Obtiene la imagen enviada como 'imagen', valida el formato
    y la guarda con un nombre único.
    """

    if "imagen" not in request.files:
        raise ValueError(
            "No se recibió ninguna imagen."
        )

    image = request.files["imagen"]

    if not image.filename:
        raise ValueError(
            "La imagen no tiene nombre."
        )

    if not allowed_image_file(
        image.filename
    ):
        raise ValueError(
            "Formato no permitido. "
            "Utiliza PNG, JPG o JPEG."
        )

    original_filename = image.filename
    safe_name = secure_filename(
        original_filename
    )

    if not safe_name:
        raise ValueError(
            "El nombre de la imagen no es válido."
        )

    stored_name = (
        f"{uuid.uuid4().hex[:12]}_"
        f"{safe_name}"
    )

    image_path = (
        upload_dir / stored_name
    )

    image.save(
        image_path
    )

    upload_info = {
        "original_name": original_filename,
        "stored_name": stored_name,
    }

    return image_path, upload_info


def parse_json_output(
    process,
    empty_message,
    invalid_message,
):
    """Convierte la salida estándar de un script en JSON."""

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

    if not stdout:
        return None, (
            jsonify(
                {
                    "success": False,
                    "error": empty_message,
                    "detail": stderr,
                }
            ),
            500,
        )

    try:
        return json.loads(stdout), None

    except json.JSONDecodeError:
        return None, (
            jsonify(
                {
                    "success": False,
                    "error": invalid_message,
                    "stdout": stdout,
                    "stderr": stderr,
                }
            ),
            500,
        )


# ============================================================
# ERRORES GENERALES
# ============================================================

@app.errorhandler(413)
def image_too_large(_error):
    return jsonify(
        {
            "success": False,
            "error": (
                "La imagen supera el tamaño "
                "máximo permitido de 10 MB."
            ),
        }
    ), 413


# ============================================================
# FRONTEND
# ============================================================

@app.route("/")
def index():
    return send_from_directory(
        FRONTEND_DIR,
        "index.html",
    )


@app.route(
    "/frontend/<path:filename>"
)
def frontend_files(filename):
    return send_from_directory(
        FRONTEND_DIR,
        filename,
    )


# ============================================================
# ARCHIVOS DEL PROYECTO
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

        try:
            requested_file.relative_to(
                directory.resolve()
            )

            allowed = True
            break

        except ValueError:
            continue

    if not allowed:
        return jsonify(
            {
                "error":
                    "Archivo no autorizado."
            }
        ), 403

    if not requested_file.exists():
        return jsonify(
            {
                "error":
                    f"No existe el archivo: "
                    f"{filename}"
            }
        ), 404

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
        requested_file.name,
    )


# ============================================================
# EJECUCIÓN GENERAL
# SEMANAS 2, 3, 4 Y 5
# ============================================================

@app.route(
    "/api/run/<script_name>",
    methods=["POST"],
)
def run_script(script_name):

    if script_name not in SCRIPTS:
        return jsonify(
            {
                "success": False,
                "error":
                    "Script no autorizado.",
            }
        ), 404

    script_path = SCRIPTS[
        script_name
    ]

    if not script_path.exists():
        return jsonify(
            {
                "success": False,
                "error":
                    f"No existe el archivo "
                    f"{script_path.name}",
            }
        ), 404

    try:

        process = run_python_script(
            [script_path],
            timeout=60,
        )

        return jsonify(
            {
                "success":
                    process.returncode == 0,
                "script":
                    script_path.name,
                "returncode":
                    process.returncode,
                "stdout":
                    process.stdout.strip(),
                "stderr":
                    process.stderr.strip(),
            }
        )

    except subprocess.TimeoutExpired:

        return jsonify(
            {
                "success": False,
                "error":
                    "La ejecución superó "
                    "el tiempo máximo permitido.",
            }
        ), 408

    except Exception as error:

        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 500


# ============================================================
# SEMANA 7
# TELEMETRÍA + REPRESENTACIONES + AUTÓMATA
# ============================================================

@app.route(
    "/api/semana7",
    methods=["POST"],
)
def run_semana7():

    data = request.get_json(
        silent=True
    ) or {}

    observations = data.get(
        "observaciones"
    )

    if not isinstance(
        observations,
        list,
    ):
        return jsonify(
            {
                "success": False,
                "error":
                    "Debe enviarse una lista "
                    "de observaciones.",
            }
        ), 400

    if not observations:
        return jsonify(
            {
                "success": False,
                "error":
                    "Debe existir al menos "
                    "una observación.",
            }
        ), 400

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
        start=1,
    ):

        if not isinstance(
            observation,
            dict,
        ):
            return jsonify(
                {
                    "success": False,
                    "error":
                        f"La lectura {index} "
                        "no tiene un formato válido.",
                }
            ), 400

        missing_fields = (
            required_fields
            - observation.keys()
        )

        if missing_fields:
            return jsonify(
                {
                    "success": False,
                    "error":
                        f"La lectura {index} "
                        "tiene campos faltantes: "
                        + ", ".join(
                            sorted(
                                missing_fields
                            )
                        ),
                }
            ), 400

    script_path = SCRIPTS[
        "semana7"
    ]

    if not script_path.exists():
        return jsonify(
            {
                "success": False,
                "error":
                    "No existe el script "
                    "de Semana 7.",
            }
        ), 404

    observations_json = json.dumps(
        observations,
        ensure_ascii=False,
    )

    try:

        process = run_python_script(
            [
                script_path,
                "--observaciones",
                observations_json,
                "--json",
            ],
            timeout=60,
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

        if process.returncode != 0:

            error_message = stderr

            if stdout:
                try:
                    error_data = json.loads(
                        stdout
                    )

                    error_message = (
                        error_data.get("error")
                        or error_message
                    )

                except json.JSONDecodeError:
                    pass

            return jsonify(
                {
                    "success": False,
                    "error":
                        error_message
                        or "El análisis presentó un error.",
                    "stderr": stderr,
                }
            ), 500

        try:
            analysis = json.loads(
                stdout
            )

        except json.JSONDecodeError:
            return jsonify(
                {
                    "success": False,
                    "error":
                        "Semana 7 se ejecutó, "
                        "pero no devolvió un JSON válido.",
                    "stdout": stdout,
                }
            ), 500

        return jsonify(
            {
                "success": True,
                "analysis": analysis,
            }
        )

    except subprocess.TimeoutExpired:

        return jsonify(
            {
                "success": False,
                "error":
                    "La ejecución de Semana 7 "
                    "superó el tiempo máximo permitido.",
            }
        ), 408

    except Exception as error:

        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 500


# ============================================================
# SEMANA 8
# RECONOCIMIENTO NEURONAL + SQLITE + ONTOLOGÍA
# ============================================================

@app.route(
    "/api/semana8",
    methods=["POST"],
)
def api_semana8():

    try:

        image_path, upload_info = (
            save_uploaded_image(
                SEMANA8_UPLOADS
            )
        )

        if not SEMANA8_SCRIPT.exists():
            return jsonify(
                {
                    "success": False,
                    "error":
                        "No existe el script "
                        "de Semana 8.",
                }
            ), 404

        process = run_python_script(
            [
                SEMANA8_SCRIPT,
                image_path,
                "--json",
            ],
            timeout=120,
        )

        analysis, error_response = (
            parse_json_output(
                process,
                (
                    "El análisis no "
                    "devolvió información."
                ),
                (
                    "El análisis devolvió "
                    "una respuesta inválida."
                ),
            )
        )

        if error_response:
            return error_response

        if not analysis.get(
            "success",
            False,
        ):
            return jsonify(
                analysis
            ), 400

        analysis["upload"] = (
            upload_info
        )

        return jsonify(
            analysis
        )

    except ValueError as error:

        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 400

    except subprocess.TimeoutExpired:

        return jsonify(
            {
                "success": False,
                "error":
                    "El análisis superó "
                    "el tiempo máximo permitido.",
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
# SEMANA 9
# CANNY + OTSU + REGIONES CONECTADAS
# ============================================================

@app.route(
    "/api/semana9",
    methods=["POST"],
)
def api_semana9():

    try:

        image_path, upload_info = (
            save_uploaded_image(
                SEMANA9_UPLOADS
            )
        )

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
                    "error":
                        "El valor de sigma "
                        "no es válido.",
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
                    "error":
                        "El área mínima "
                        "no es válida.",
                }
            ), 400

        if sigma <= 0:
            return jsonify(
                {
                    "success": False,
                    "error":
                        "Sigma debe ser "
                        "mayor que 0.",
                }
            ), 400

        if min_area < 1:
            return jsonify(
                {
                    "success": False,
                    "error":
                        "El área mínima debe "
                        "ser mayor que 0.",
                }
            ), 400

        if not SEMANA9_SCRIPT.exists():
            return jsonify(
                {
                    "success": False,
                    "error":
                        "No existe el script "
                        "de Semana 9.",
                }
            ), 404

        process = run_python_script(
            [
                SEMANA9_SCRIPT,
                image_path,
                "--sigma",
                sigma,
                "--min-area",
                min_area,
                "--json",
            ],
            timeout=120,
        )

        analysis, error_response = (
            parse_json_output(
                process,
                (
                    "Semana 9 no devolvió "
                    "información."
                ),
                (
                    "Semana 9 devolvió una "
                    "respuesta inválida."
                ),
            )
        )

        if error_response:
            return error_response

        if not analysis.get(
            "success",
            False,
        ):
            return jsonify(
                analysis
            ), 400

        analysis["upload"] = (
            upload_info
        )

        return jsonify(
            analysis
        )

    except ValueError as error:

        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 400

    except subprocess.TimeoutExpired:

        return jsonify(
            {
                "success": False,
                "error":
                    "El procesamiento superó "
                    "el tiempo máximo permitido.",
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
# SEMANA 10
# HISTOGRAMAS + OTSU + REGIONES + LBP
# ============================================================

@app.route(
    "/api/semana10",
    methods=["POST"],
)
def api_semana10():

    try:

        image_path, upload_info = (
            save_uploaded_image(
                SEMANA10_UPLOADS
            )
        )

        if not SEMANA10_SCRIPT.exists():
            return jsonify(
                {
                    "success": False,
                    "error":
                        "No existe el script "
                        "de Semana 10.",
                }
            ), 404

        process = run_python_script(
            [
                SEMANA10_SCRIPT,
                "--imagen",
                image_path,
                "--json",
            ],
            timeout=120,
        )

        if process.returncode != 0:

            stderr = (
                process.stderr.strip()
                if process.stderr
                else ""
            )

            stdout = (
                process.stdout.strip()
                if process.stdout
                else ""
            )

            error_message = stderr

            if stdout:
                try:
                    error_data = json.loads(
                        stdout
                    )

                    error_message = (
                        error_data.get("error")
                        or error_message
                    )

                except json.JSONDecodeError:
                    pass

            return jsonify(
                {
                    "success": False,
                    "error":
                        error_message
                        or "No se pudo analizar "
                           "la imagen.",
                }
            ), 500

        analysis, error_response = (
            parse_json_output(
                process,
                (
                    "El análisis no devolvió "
                    "información."
                ),
                (
                    "El análisis devolvió "
                    "una respuesta inválida."
                ),
            )
        )

        if error_response:
            return error_response

        analysis["success"] = True
        analysis["upload"] = upload_info

        return jsonify(
            analysis
        )

    except ValueError as error:

        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 400

    except subprocess.TimeoutExpired:

        return jsonify(
            {
                "success": False,
                "error":
                    "El análisis superó "
                    "el tiempo máximo permitido.",
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
# ARTIFACTOS GENERADOS
# ============================================================

@app.route(
    "/artifacts/<path:filename>"
)
def serve_artifact(filename):

    return send_from_directory(
        ARTIFACTS_DIR,
        filename,
    )


# ============================================================
# ESTADO DEL BACKEND
# ============================================================

@app.route("/api/status")
def status():

    available_scripts = {
        name: path.exists()
        for name, path
        in SCRIPTS.items()
    }

    available_scripts.update(
        {
            "semana8":
                SEMANA8_SCRIPT.exists(),
            "semana9":
                SEMANA9_SCRIPT.exists(),
            "semana10":
                SEMANA10_SCRIPT.exists(),
        }
    )

    return jsonify(
        {
            "status": "ok",
            "python": sys.version,
            "python_executable":
                sys.executable,
            "encoding": "utf-8",
            "current_week": 10,
            "scripts":
                available_scripts,
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
        "PROYECTO IA - "
        "DETECCIÓN DE ANOMALÍAS EN SERVIDORES"
    )

    print(
        "=" * 70
    )

    print(
        "\nFrontend disponible en:"
    )

    print(
        "http://localhost:5000"
    )

    print(
        "\nCodificación de ejecución: UTF-8"
    )

    print(
        "\nScripts disponibles:"
    )

    status_scripts = {
        **SCRIPTS,
        "semana8": SEMANA8_SCRIPT,
        "semana9": SEMANA9_SCRIPT,
        "semana10": SEMANA10_SCRIPT,
    }

    for name, path in status_scripts.items():

        status_text = (
            "OK"
            if path.exists()
            else "NO ENCONTRADO"
        )

        print(
            f"  {name}: {status_text}"
        )

    print(
        "\n" + "=" * 70
    )

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
