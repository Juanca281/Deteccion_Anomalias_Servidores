from pathlib import Path
import random

import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = (
    ROOT
    / "data"
    / "semana08"
)


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

CATEGORIES = [
    "normal",
    "sobrecarga",
    "latencia",
    "disco",
    "critico",
]

IMAGES_PER_CATEGORY = 200

POINTS = 40

RANDOM_SEED = 42


np.random.seed(
    RANDOM_SEED
)

random.seed(
    RANDOM_SEED
)


# ============================================================
# CREAR CARPETAS
# ============================================================

def create_directories():

    for category in CATEGORIES:

        folder = (
            DATASET_DIR
            / category
        )

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )


# ============================================================
# ELIMINAR DATASET ANTERIOR
# ============================================================

def clear_previous_dataset():

    print(
        "Eliminando dataset anterior..."
    )

    for category in CATEGORIES:

        folder = (
            DATASET_DIR
            / category
        )

        if not folder.exists():
            continue

        for image in folder.glob(
            "*.png"
        ):

            image.unlink()


# ============================================================
# CREAR SERIE BASE
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


    # --------------------------------------------------------
    # Pequeña tendencia positiva o negativa
    # --------------------------------------------------------

    trend_values = np.linspace(
        0,
        random.uniform(
            -trend,
            trend,
        ),
        POINTS,
    )


    values = (
        values
        + trend_values
    )


    return np.clip(
        values,
        minimum,
        maximum,
    )


# ============================================================
# AGREGAR PICOS
# ============================================================

def add_spikes(
    values,
    probability,
    strength,
    maximum,
):

    values = values.copy()


    for index in range(
        len(values)
    ):

        if (
            random.random()
            < probability
        ):

            values[index] += (
                random.uniform(
                    strength * 0.5,
                    strength,
                )
            )


    return np.clip(
        values,
        0,
        maximum,
    )


# ============================================================
# CLASE NORMAL
# ============================================================

def generate_normal():

    cpu = create_series(
        mean=random.uniform(
            40,
            55,
        ),
        deviation=random.uniform(
            3,
            6,
        ),
        minimum=25,
        maximum=70,
        trend=5,
    )


    ram = create_series(
        mean=random.uniform(
            50,
            62,
        ),
        deviation=random.uniform(
            2,
            5,
        ),
        minimum=35,
        maximum=75,
        trend=4,
    )


    disk = create_series(
        mean=random.uniform(
            55,
            68,
        ),
        deviation=random.uniform(
            1,
            3,
        ),
        minimum=45,
        maximum=78,
        trend=2,
    )


    latency = create_series(
        mean=random.uniform(
            35,
            65,
        ),
        deviation=random.uniform(
            5,
            10,
        ),
        minimum=15,
        maximum=100,
        trend=10,
    )


    return (
        cpu,
        ram,
        disk,
        latency,
    )


# ============================================================
# SOBRECARGA CPU / RAM
# ============================================================

def generate_overload():

    cpu = create_series(
        mean=random.uniform(
            84,
            94,
        ),
        deviation=random.uniform(
            2,
            5,
        ),
        minimum=75,
        maximum=100,
        trend=4,
    )


    ram = create_series(
        mean=random.uniform(
            82,
            92,
        ),
        deviation=random.uniform(
            2,
            5,
        ),
        minimum=74,
        maximum=100,
        trend=4,
    )


    disk = create_series(
        mean=random.uniform(
            55,
            70,
        ),
        deviation=random.uniform(
            2,
            4,
        ),
        minimum=45,
        maximum=80,
        trend=3,
    )


    latency = create_series(
        mean=random.uniform(
            60,
            105,
        ),
        deviation=random.uniform(
            7,
            15,
        ),
        minimum=30,
        maximum=145,
        trend=15,
    )


    cpu = add_spikes(
        cpu,
        probability=0.08,
        strength=7,
        maximum=100,
    )


    return (
        cpu,
        ram,
        disk,
        latency,
    )


# ============================================================
# LATENCIA ALTA
# ============================================================

def generate_high_latency():

    cpu = create_series(
        mean=random.uniform(
            42,
            58,
        ),
        deviation=random.uniform(
            3,
            6,
        ),
        minimum=28,
        maximum=72,
        trend=5,
    )


    ram = create_series(
        mean=random.uniform(
            50,
            65,
        ),
        deviation=random.uniform(
            2,
            5,
        ),
        minimum=38,
        maximum=76,
        trend=4,
    )


    disk = create_series(
        mean=random.uniform(
            55,
            70,
        ),
        deviation=random.uniform(
            1,
            3,
        ),
        minimum=45,
        maximum=80,
        trend=2,
    )


    latency = create_series(
        mean=random.uniform(
            190,
            245,
        ),
        deviation=random.uniform(
            12,
            25,
        ),
        minimum=150,
        maximum=300,
        trend=25,
    )


    latency = add_spikes(
        latency,
        probability=0.15,
        strength=30,
        maximum=300,
    )


    return (
        cpu,
        ram,
        disk,
        latency,
    )


# ============================================================
# SATURACIÓN DE DISCO
# ============================================================

def generate_disk_saturation():

    cpu = create_series(
        mean=random.uniform(
            42,
            58,
        ),
        deviation=random.uniform(
            3,
            6,
        ),
        minimum=28,
        maximum=72,
        trend=5,
    )


    ram = create_series(
        mean=random.uniform(
            50,
            65,
        ),
        deviation=random.uniform(
            2,
            5,
        ),
        minimum=38,
        maximum=76,
        trend=4,
    )


    # --------------------------------------------------------
    # Disco claramente elevado
    # --------------------------------------------------------

    disk = create_series(
        mean=random.uniform(
            92,
            97,
        ),
        deviation=random.uniform(
            0.8,
            2,
        ),
        minimum=88,
        maximum=100,
        trend=1,
    )


    latency = create_series(
        mean=random.uniform(
            45,
            80,
        ),
        deviation=random.uniform(
            5,
            10,
        ),
        minimum=20,
        maximum=120,
        trend=10,
    )


    return (
        cpu,
        ram,
        disk,
        latency,
    )


# ============================================================
# ESTADO CRÍTICO
# ============================================================

def generate_critical():

    cpu = create_series(
        mean=random.uniform(
            90,
            96,
        ),
        deviation=random.uniform(
            1.5,
            4,
        ),
        minimum=82,
        maximum=100,
        trend=3,
    )


    ram = create_series(
        mean=random.uniform(
            88,
            95,
        ),
        deviation=random.uniform(
            1.5,
            4,
        ),
        minimum=82,
        maximum=100,
        trend=3,
    )


    disk = create_series(
        mean=random.uniform(
            92,
            97,
        ),
        deviation=random.uniform(
            0.8,
            2,
        ),
        minimum=88,
        maximum=100,
        trend=1,
    )


    latency = create_series(
        mean=random.uniform(
            215,
            270,
        ),
        deviation=random.uniform(
            12,
            25,
        ),
        minimum=175,
        maximum=300,
        trend=20,
    )


    latency = add_spikes(
        latency,
        probability=0.12,
        strength=25,
        maximum=300,
    )


    return (
        cpu,
        ram,
        disk,
        latency,
    )


# ============================================================
# OBTENER DATOS SEGÚN CATEGORÍA
# ============================================================

def generate_data(
    category,
):

    if category == "normal":
        return generate_normal()

    if category == "sobrecarga":
        return generate_overload()

    if category == "latencia":
        return generate_high_latency()

    if category == "disco":
        return generate_disk_saturation()

    if category == "critico":
        return generate_critical()


    raise ValueError(
        f"Categoría no reconocida: "
        f"{category}"
    )


# ============================================================
# CREAR GRÁFICA
# ============================================================

def create_chart(
    category,
    index,
):

    (
        cpu,
        ram,
        disk,
        latency,
    ) = generate_data(
        category
    )


    time = np.arange(
        POINTS
    )


    # ========================================================
    # IMPORTANTE
    #
    # La estructura visual permanece FIJA.
    #
    # Solo cambian los valores de las métricas.
    # ========================================================

    fig = plt.figure(
        figsize=(
            8,
            5,
        )
    )


    # CPU

    plt.plot(
        time,
        cpu,
        label="CPU (%)",
        linewidth=2,
    )


    # RAM

    plt.plot(
        time,
        ram,
        label="RAM (%)",
        linewidth=2,
    )


    # DISCO

    plt.plot(
        time,
        disk,
        label="Disco (%)",
        linewidth=2,
    )


    # LATENCIA
    #
    # Se divide entre 3 para representar
    # la latencia dentro de la misma escala.

    plt.plot(
        time,
        latency / 3,
        label="Latencia (escala)",
        linewidth=2,
    )


    # ========================================================
    # CONFIGURACIÓN FIJA
    # ========================================================

    plt.ylim(
        0,
        105,
    )


    plt.xlim(
        0,
        POINTS - 1,
    )


    plt.xlabel(
        "Tiempo"
    )


    plt.ylabel(
        "Uso / Nivel"
    )


    plt.title(
        "Monitoreo del servidor"
    )


    plt.grid(
        alpha=0.25
    )


    plt.legend(
        loc="upper left",
        fontsize=8,
        frameon=True,
    )


    plt.tight_layout()


    # ========================================================
    # GUARDAR
    # ========================================================

    filename = (
        f"{category}_"
        f"{index:04d}.png"
    )


    output_path = (
        DATASET_DIR
        / category
        / filename
    )


    plt.savefig(
        output_path,
        dpi=100,
    )


    plt.close(
        fig
    )


# ============================================================
# GENERAR DATASET COMPLETO
# ============================================================

def generate_dataset():

    create_directories()

    clear_previous_dataset()


    print()

    print(
        "=" * 65
    )

    print(
        "GENERANDO DATASET SEMANA 8"
    )

    print(
        "=" * 65
    )

    print()


    total = 0


    for category in CATEGORIES:

        print(
            f"Generando categoría: "
            f"{category}"
        )


        for index in range(
            1,
            IMAGES_PER_CATEGORY + 1,
        ):

            create_chart(
                category,
                index,
            )

            total += 1


        print(
            f"  ✓ "
            f"{IMAGES_PER_CATEGORY} "
            f"imágenes"
        )


    print()

    print(
        "=" * 65
    )

    print(
        "DATASET GENERADO CORRECTAMENTE"
    )

    print(
        "=" * 65
    )

    print()

    print(
        f"Normal: "
        f"{IMAGES_PER_CATEGORY}"
    )

    print(
        f"Sobrecarga: "
        f"{IMAGES_PER_CATEGORY}"
    )

    print(
        f"Latencia: "
        f"{IMAGES_PER_CATEGORY}"
    )

    print(
        f"Disco: "
        f"{IMAGES_PER_CATEGORY}"
    )

    print(
        f"Crítico: "
        f"{IMAGES_PER_CATEGORY}"
    )

    print()

    print(
        f"TOTAL: "
        f"{total} imágenes"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    generate_dataset()