from pathlib import Path
import os
import subprocess
import sys
import json

from flask import (
    Flask,
    jsonify,
    request,
    send_from_directory,
)


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

ROOT = Path(__file__).resolve().parent

FRONTEND_DIR = ROOT / "frontend"


app = Flask(__name__)

app.json.ensure_ascii = False


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

    # ========================================================
    # RECIBIR JSON
    # ========================================================

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )


    # ========================================================
    # CONVERTIR DATOS
    # ========================================================

    try:

        cpu = float(
            data.get(
                "cpu",
                50
            )
        )


        ram = float(
            data.get(
                "ram",
                55
            )
        )


        disk = float(
            data.get(
                "disco",
                60
            )
        )


        latency = float(
            data.get(
                "latencia",
                50
            )
        )


        requests_per_minute = float(
            data.get(
                "solicitudes",
                500
            )
        )


        errors = int(
            data.get(
                "errores",
                0
            )
        )


        status = str(
            data.get(
                "estado",
                "Activo"
            )
        ).strip()


        sequence = str(
            data.get(
                "secuencia",
                "N"
            )
        ).upper().replace(
            " ",
            ""
        ).strip()


    except (
        TypeError,
        ValueError
    ):

        return jsonify(
            {
                "success": False,

                "error":
                    "Los datos ingresados "
                    "no son válidos."
            }
        ), 400


    # ========================================================
    # VALIDAR CPU
    # ========================================================

    if not 0 <= cpu <= 100:

        return jsonify(
            {
                "success": False,

                "error":
                    "CPU debe estar entre "
                    "0 y 100."
            }
        ), 400


    # ========================================================
    # VALIDAR RAM
    # ========================================================

    if not 0 <= ram <= 100:

        return jsonify(
            {
                "success": False,

                "error":
                    "RAM debe estar entre "
                    "0 y 100."
            }
        ), 400


    # ========================================================
    # VALIDAR DISCO
    # ========================================================

    if not 0 <= disk <= 100:

        return jsonify(
            {
                "success": False,

                "error":
                    "El uso de disco debe "
                    "estar entre 0 y 100."
            }
        ), 400


    # ========================================================
    # VALIDAR LATENCIA
    # ========================================================

    if latency < 0:

        return jsonify(
            {
                "success": False,

                "error":
                    "La latencia no puede "
                    "ser negativa."
            }
        ), 400


    # ========================================================
    # VALIDAR SOLICITUDES
    # ========================================================

    if requests_per_minute < 0:

        return jsonify(
            {
                "success": False,

                "error":
                    "Las solicitudes por minuto "
                    "no pueden ser negativas."
            }
        ), 400


    # ========================================================
    # VALIDAR ERRORES
    # ========================================================

    if errors < 0:

        return jsonify(
            {
                "success": False,

                "error":
                    "La cantidad de errores "
                    "no puede ser negativa."
            }
        ), 400


    # ========================================================
    # VALIDAR ESTADO
    # ========================================================

    valid_statuses = {
        "activo",
        "inactivo",
        "mantenimiento"
    }


    if status.lower() not in valid_statuses:

        return jsonify(
            {
                "success": False,

                "error":
                    "El estado del servidor "
                    "no es válido."
            }
        ), 400


    # ========================================================
    # VALIDAR SECUENCIA
    # ========================================================

    valid_symbols = {
        "N",
        "A",
        "C",
        "R"
    }


    if not sequence:

        return jsonify(
            {
                "success": False,

                "error":
                    "La secuencia no puede "
                    "estar vacía."
            }
        ), 400


    for symbol in sequence:

        if symbol not in valid_symbols:

            return jsonify(
                {
                    "success": False,

                    "error":
                        "La secuencia solo puede "
                        "contener N, A, C y R."
                }
            ), 400


    # ========================================================
    # SCRIPT SEMANA 7
    # ========================================================

    script_path = SCRIPTS[
        "semana7"
    ]


    if not script_path.exists():

        return jsonify(
            {
                "success": False,

                "error":
                    "No existe el script "
                    "de Semana 7."
            }
        ), 404


    # ========================================================
    # CONFIGURACIÓN UTF-8
    # ========================================================

    env = os.environ.copy()

    env["PYTHONUTF8"] = "1"

    env["PYTHONIOENCODING"] = (
        "utf-8"
    )


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

                "--cpu",
                str(cpu),

                "--ram",
                str(ram),

                "--disco",
                str(disk),

                "--latencia",
                str(latency),

                "--solicitudes",
                str(
                    requests_per_minute
                ),

                "--errores",
                str(errors),

                "--estado",
                status,

                "--secuencia",
                sequence
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
                    stderr,

                "input": {

                    "cpu":
                        cpu,

                    "ram":
                        ram,

                    "disco":
                        disk,

                    "latencia":
                        latency,

                    "solicitudes":
                        requests_per_minute,

                    "errores":
                        errors,

                    "estado":
                        status,

                    "secuencia":
                        sequence
                }
            }
        )


    except subprocess.TimeoutExpired:

        return jsonify(
            {
                "success": False,

                "error":
                    "La ejecución de Semana 7 "
                    "superó el tiempo máximo "
                    "permitido."
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
# ESTADO DEL BACKEND
# ============================================================

@app.route(
    "/api/status"
)
def status():

    available_scripts = {

        name:
            path.exists()

        for name, path
        in SCRIPTS.items()
    }


    return jsonify(
        {
            "status":
                "ok",

            "python":
                sys.version,

            "python_executable":
                sys.executable,

            "encoding":
                "utf-8",

            "scripts":
                available_scripts
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