from pathlib import Path
import os
import subprocess
import sys

from flask import Flask, jsonify, send_from_directory


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT / "frontend"

app = Flask(__name__)

# Evita convertir caracteres Unicode en secuencias ASCII
app.json.ensure_ascii = False


# ============================================================
# SCRIPTS AUTORIZADOS
# ============================================================

SCRIPTS = {
    "semana2": ROOT / "src" / "semana02_fundamentos.py",

    "semana3": ROOT / "src" / "semana03_taxonomia.py",

    "semana4_astar": ROOT / "src" / "semana04_astar.py",

    "semana4_minimax": ROOT / "src" / "semana04_minimax.py",

    "semana5": ROOT / "src" / "semana05_sistema_hibrido.py",
}


# ============================================================
# DIRECTORIOS PERMITIDOS PARA VISUALIZAR
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
    """
    Carga la página principal del proyecto.
    """

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# ============================================================
# ARCHIVOS DEL FRONTEND
# ============================================================

@app.route("/frontend/<path:filename>")
def frontend_files(filename):
    """
    Permite cargar CSS, JavaScript y otros archivos
    pertenecientes al frontend.
    """

    return send_from_directory(
        FRONTEND_DIR,
        filename
    )


# ============================================================
# VISUALIZAR ARCHIVOS DEL PROYECTO
# ============================================================

@app.route("/project/<path:filename>")
def project_file(filename):
    """
    Permite visualizar archivos ubicados únicamente
    dentro de:

    - src/
    - reports/
    - data/
    """

    requested_file = (
        ROOT / filename
    ).resolve()

    allowed = False


    # ========================================================
    # VALIDAR DIRECTORIO
    # ========================================================

    for directory in ALLOWED_DIRECTORIES:

        directory = directory.resolve()

        try:

            requested_file.relative_to(
                directory
            )

            allowed = True

            break

        except ValueError:

            continue


    # ========================================================
    # ARCHIVO NO AUTORIZADO
    # ========================================================

    if not allowed:

        return jsonify(
            {
                "error": "Archivo no autorizado."
            }
        ), 403


    # ========================================================
    # ARCHIVO NO EXISTE
    # ========================================================

    if not requested_file.exists():

        return jsonify(
            {
                "error": (
                    f"No existe el archivo: "
                    f"{filename}"
                )
            }
        ), 404


    # ========================================================
    # VALIDAR QUE SEA ARCHIVO
    # ========================================================

    if not requested_file.is_file():

        return jsonify(
            {
                "error": (
                    "La ruta no corresponde "
                    "a un archivo."
                )
            }
        ), 400


    return send_from_directory(
        requested_file.parent,
        requested_file.name
    )


# ============================================================
# EJECUTAR SCRIPT
# ============================================================

@app.route(
    "/api/run/<script_name>",
    methods=["POST"]
)
def run_script(script_name):
    """
    Ejecuta únicamente los scripts definidos
    previamente en SCRIPTS.

    La ejecución fuerza UTF-8 para evitar problemas
    con tildes, ñ, símbolos y emojis en Windows.
    """


    # ========================================================
    # VALIDAR SCRIPT
    # ========================================================

    if script_name not in SCRIPTS:

        return jsonify(
            {
                "success": False,
                "error": "Script no autorizado."
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
                "error": (
                    f"No existe el archivo "
                    f"{script_path.name}"
                )
            }
        ), 404


    try:

        # ====================================================
        # VARIABLES DE ENTORNO UTF-8
        # ====================================================

        env = os.environ.copy()

        env["PYTHONUTF8"] = "1"

        env["PYTHONIOENCODING"] = "utf-8"


        # ====================================================
        # EJECUTAR PYTHON EN MODO UTF-8
        # ====================================================

        process = subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                str(script_path),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            env=env,
        )


        # ====================================================
        # CAPTURAR SALIDA NORMAL
        # ====================================================

        stdout = (
            process.stdout.strip()
            if process.stdout
            else ""
        )


        # ====================================================
        # CAPTURAR ERRORES
        # ====================================================

        stderr = (
            process.stderr.strip()
            if process.stderr
            else ""
        )


        # ====================================================
        # VALIDAR RESULTADO
        # ====================================================

        success = (
            process.returncode == 0
        )


        # ====================================================
        # RESPUESTA AL FRONTEND
        # ====================================================

        return jsonify(
            {
                "success": success,

                "script": script_path.name,

                "returncode": process.returncode,

                "stdout": stdout,

                "stderr": stderr,
            }
        )


    # ========================================================
    # TIEMPO MÁXIMO SUPERADO
    # ========================================================

    except subprocess.TimeoutExpired:

        return jsonify(
            {
                "success": False,

                "error": (
                    "La ejecución superó "
                    "el tiempo máximo permitido."
                )
            }
        ), 408


    # ========================================================
    # ERROR GENERAL
    # ========================================================

    except Exception as error:

        return jsonify(
            {
                "success": False,

                "error": str(error)
            }
        ), 500


# ============================================================
# ESTADO DEL SISTEMA
# ============================================================

@app.route("/api/status")
def status():
    """
    Comprueba el estado del backend Flask
    y verifica cuáles scripts existen.
    """

    available_scripts = {}


    for name, path in SCRIPTS.items():

        available_scripts[
            name
        ] = path.exists()


    return jsonify(
        {
            "status": "ok",

            "python": sys.version,

            "encoding": "utf-8",

            "scripts": available_scripts,
        }
    )


# ============================================================
# EJECUCIÓN PRINCIPAL
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


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )