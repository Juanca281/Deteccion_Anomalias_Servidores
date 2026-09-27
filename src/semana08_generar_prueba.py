from pathlib import Path
import random

import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = ROOT / "data" / "semana08" / "pruebas"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

POINTS = 40
RANDOM_SEED = 1234

np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


# ============================================================
# UTILIDADES
# ============================================================

def create_series(
    mean,
    deviation,
    minimum,
    maximum,
    trend=0,
):

    values = np.random.normal(
        mean,
        deviation,
        POINTS,
    )

    trend_values = np.linspace(
        0,
        random.uniform(-trend, trend),
        POINTS,
    )

    values = values + trend_values

    return np.clip(
        values,
        minimum,
        maximum,
    )


def add_spikes(
    values,
    probability,
    strength,
    maximum,
):

    values = values.copy()

    for index in range(len(values)):

        if random.random() < probability:

            values[index] += random.uniform(
                strength * 0.5,
                strength,
            )

    return np.clip(
        values,
        0,
        maximum,
    )


# ============================================================
# GENERADORES POR CLASE
# ============================================================

def generate_normal():

    cpu = create_series(
        mean=48,
        deviation=4,
        minimum=30,
        maximum=65,
        trend=4,
    )

    ram = create_series(
        mean=58,
        deviation=3,
        minimum=42,
        maximum=72,
        trend=3,
    )

    disk = create_series(
        mean=63,
        deviation=2,
        minimum=52,
        maximum=75,
        trend=2,
    )

    latency = create_series(
        mean=50,
        deviation=7,
        minimum=20,
        maximum=90,
        trend=8,
    )

    return cpu, ram, disk, latency


def generate_overload():

    cpu = create_series(
        mean=90,
        deviation=3,
        minimum=80,
        maximum=100,
        trend=3,
    )

    ram = create_series(
        mean=88,
        deviation=3,
        minimum=78,
        maximum=100,
        trend=3,
    )

    disk = create_series(
        mean=64,
        deviation=2,
        minimum=52,
        maximum=76,
        trend=2,
    )

    latency = create_series(
        mean=85,
        deviation=10,
        minimum=45,
        maximum=130,
        trend=10,
    )

    cpu = add_spikes(
        cpu,
        probability=0.08,
        strength=6,
        maximum=100,
    )

    return cpu, ram, disk, latency


def generate_latency():

    cpu = create_series(
        mean=50,
        deviation=4,
        minimum=33,
        maximum=66,
        trend=4,
    )

    ram = create_series(
        mean=59,
        deviation=3,
        minimum=44,
        maximum=73,
        trend=3,
    )

    disk = create_series(
        mean=64,
        deviation=2,
        minimum=52,
        maximum=76,
        trend=2,
    )

    latency = create_series(
        mean=230,
        deviation=18,
        minimum=180,
        maximum=300,
        trend=20,
    )

    latency = add_spikes(
        latency,
        probability=0.12,
        strength=25,
        maximum=300,
    )

    return cpu, ram, disk, latency


def generate_disk():

    cpu = create_series(
        mean=49,
        deviation=4,
        minimum=32,
        maximum=65,
        trend=4,
    )

    ram = create_series(
        mean=58,
        deviation=3,
        minimum=43,
        maximum=72,
        trend=3,
    )

    disk = create_series(
        mean=95,
        deviation=1.2,
        minimum=90,
        maximum=100,
        trend=1,
    )

    latency = create_series(
        mean=60,
        deviation=8,
        minimum=25,
        maximum=95,
        trend=8,
    )

    return cpu, ram, disk, latency


def generate_critical():

    cpu = create_series(
        mean=94,
        deviation=2,
        minimum=87,
        maximum=100,
        trend=2,
    )

    ram = create_series(
        mean=92,
        deviation=2,
        minimum=86,
        maximum=100,
        trend=2,
    )

    disk = create_series(
        mean=95,
        deviation=1.2,
        minimum=90,
        maximum=100,
        trend=1,
    )

    latency = create_series(
        mean=245,
        deviation=18,
        minimum=190,
        maximum=300,
        trend=18,
    )

    latency = add_spikes(
        latency,
        probability=0.10,
        strength=20,
        maximum=300,
    )

    return cpu, ram, disk, latency


# ============================================================
# MAPA DE ESCENARIOS
# ============================================================

SCENARIOS = {
    "prueba_normal.png": generate_normal,
    "prueba_sobrecarga.png": generate_overload,
    "prueba_latencia.png": generate_latency,
    "prueba_disco.png": generate_disk,
    "prueba_critico.png": generate_critical,
}


# ============================================================
# CREAR GRÁFICA
# ============================================================

def create_chart(
    filename,
    generator,
):

    cpu, ram, disk, latency = generator()

    time = np.arange(POINTS)

    plt.figure(figsize=(8, 5))

    plt.plot(
        time,
        cpu,
        label="CPU (%)",
        linewidth=2,
    )

    plt.plot(
        time,
        ram,
        label="RAM (%)",
        linewidth=2,
    )

    plt.plot(
        time,
        disk,
        label="Disco (%)",
        linewidth=2,
    )

    plt.plot(
        time,
        latency / 3,
        label="Latencia (escala)",
        linewidth=2,
    )

    plt.ylim(0, 105)
    plt.xlim(0, POINTS - 1)

    plt.xlabel("Tiempo")
    plt.ylabel("Uso / Nivel")
    plt.title("Monitoreo del servidor")
    plt.grid(alpha=0.25)
    plt.legend(loc="upper left", fontsize=8, frameon=True)
    plt.tight_layout()

    output_path = OUTPUT_DIR / filename

    plt.savefig(
        output_path,
        dpi=100,
    )

    plt.close()

    return output_path


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("GENERANDO IMÁGENES DE PRUEBA - SEMANA 8")
    print("=" * 60)
    print()

    generated = []

    for filename, generator in SCENARIOS.items():

        path = create_chart(
            filename,
            generator,
        )

        generated.append(path)

        print(f"Generada: {path.name}")

    print()
    print("=" * 60)
    print("TOTAL DE IMÁGENES DE PRUEBA:", len(generated))
    print("RUTA:", OUTPUT_DIR)
    print("=" * 60)


if __name__ == "__main__":
    main()