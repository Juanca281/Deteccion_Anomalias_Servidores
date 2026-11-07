"""Semana 13 - Motor de inferencia para detección de anomalías en servidores.

Implementa reglas lógicas positivas y encadenamiento hacia adelante.
No aprende reglas: aplica conocimiento explícito definido para el dominio.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Regla:
    """Regla lógica tipo Horn con premisas positivas y una conclusión."""

    nombre: str
    premisas: frozenset[str]
    conclusion: str
    descripcion: str = ""


def construir_reglas() -> list[Regla]:
    """Construye la base de conocimiento del proyecto ServidorIA."""

    return [
        Regla(
            "R1",
            frozenset({"cpu_alta", "ram_alta"}),
            "sobrecarga_recursos",
            "CPU y RAM elevadas indican sobrecarga de recursos.",
        ),
        Regla(
            "R2",
            frozenset({"latencia_alta", "errores_altos"}),
            "degradacion_servicio",
            "Latencia y errores elevados evidencian degradación del servicio.",
        ),
        Regla(
            "R3",
            frozenset({"disco_critico", "sobrecarga_recursos"}),
            "riesgo_critico",
            "Disco crítico junto con sobrecarga eleva el riesgo operacional.",
        ),
        Regla(
            "R4",
            frozenset({"sobrecarga_recursos", "degradacion_servicio"}),
            "incidente_prioridad_alta",
            "Sobrecarga y degradación justifican prioridad alta.",
        ),
        Regla(
            "R5",
            frozenset({"riesgo_critico", "incidente_prioridad_alta"}),
            "escalar_soporte",
            "Riesgo crítico e incidente de prioridad alta requieren escalamiento.",
        ),
        Regla(
            "R6",
            frozenset({"escalar_soporte"}),
            "mantenimiento_recomendado",
            "El escalamiento activa una recomendación de mantenimiento.",
        ),
    ]


def inferir(
    hechos_iniciales: set[str],
    reglas: list[Regla],
) -> tuple[set[str], list[dict[str, object]]]:
    """Aplica encadenamiento hacia adelante hasta alcanzar un punto fijo."""

    hechos = set(hechos_iniciales)
    trazas: list[dict[str, object]] = []
    cambios = True
    iteracion = 0

    while cambios:
        cambios = False
        iteracion += 1

        for regla in reglas:
            premisas_cumplidas = regla.premisas.issubset(hechos)
            conclusion_nueva = regla.conclusion not in hechos

            if premisas_cumplidas and conclusion_nueva:
                hechos.add(regla.conclusion)
                trazas.append(
                    {
                        "iteracion": iteracion,
                        "regla": regla.nombre,
                        "premisas": sorted(regla.premisas),
                        "conclusion": regla.conclusion,
                        "descripcion": regla.descripcion,
                    }
                )
                cambios = True

    return hechos, trazas


def analizar(hechos_iniciales: set[str]) -> dict[str, object]:
    """Ejecuta el motor y devuelve un resultado serializable."""

    reglas = construir_reglas()
    hechos_finales, trazas = inferir(hechos_iniciales, reglas)

    objetivo = "mantenimiento_recomendado"
    inferidos = sorted(hechos_finales - hechos_iniciales)

    return {
        "success": True,
        "hechos_iniciales": sorted(hechos_iniciales),
        "hechos_inferidos": inferidos,
        "hechos_finales": sorted(hechos_finales),
        "objetivo": objetivo,
        "demostrada": objetivo in hechos_finales,
        "estado": (
            "DEMOSTRADA"
            if objetivo in hechos_finales
            else "NO DEMOSTRADA con los hechos disponibles"
        ),
        "trazas": trazas,
        "reglas": [
            {
                "nombre": regla.nombre,
                "premisas": sorted(regla.premisas),
                "conclusion": regla.conclusion,
                "descripcion": regla.descripcion,
            }
            for regla in reglas
        ],
    }


def mostrar_resultado(nombre: str, hechos: set[str]) -> None:
    resultado = analizar(hechos)
    print(f"\n{nombre}")
    print("Hechos iniciales:", ", ".join(resultado["hechos_iniciales"]))
    for paso in resultado["trazas"]:
        premisas = " ∧ ".join(paso["premisas"])
        print(
            f"Inferencia {paso['regla']}: "
            f"{premisas} -> {paso['conclusion']}"
        )
    print("Conclusión mantenimiento_recomendado:", resultado["estado"])


def escenarios_demo() -> tuple[set[str], set[str]]:
    caso_a = {
        "cpu_alta",
        "ram_alta",
        "latencia_alta",
        "errores_altos",
        "disco_critico",
    }
    caso_b = caso_a - {"disco_critico"}
    return caso_a, caso_b


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hechos-json", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.hechos_json is not None:
        try:
            datos = json.loads(args.hechos_json)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"JSON de hechos inválido: {exc}") from exc

        if not isinstance(datos, list) or not all(
            isinstance(item, str) for item in datos
        ):
            raise SystemExit("--hechos-json debe contener una lista de textos.")

        resultado = analizar(set(datos))
        if args.json:
            print(json.dumps(resultado, ensure_ascii=False))
        else:
            mostrar_resultado("ESCENARIO PERSONALIZADO", set(datos))
        return

    caso_a, caso_b = escenarios_demo()

    if args.json:
        print(
            json.dumps(
                {
                    "success": True,
                    "caso_a": analizar(caso_a),
                    "caso_b": analizar(caso_b),
                },
                ensure_ascii=False,
            )
        )
        return

    print("=" * 68)
    print("SEMANA 13 - MOTOR DE INFERENCIA | SERVIDORIA")
    print("=" * 68)
    mostrar_resultado("CASO A: anomalía crítica completa", caso_a)
    mostrar_resultado("CASO B: sin evidencia de disco crítico", caso_b)
    print(
        "\nNota: una conclusión no demostrada no significa que sea falsa; "
        "solo indica que no existe evidencia suficiente en la base actual."
    )


if __name__ == "__main__":
    main()
