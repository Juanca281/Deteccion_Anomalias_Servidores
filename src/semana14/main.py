"""Demostración ejecutable de la red semántica de ServidorIA."""

from __future__ import annotations

import argparse
import json

from red_semantica import RedSemantica


ORACIONES_PREDETERMINADAS = [
    "El servidor_web es un servidor.",
    "El servidor_bd es un servidor.",
    "El servidor es un activo_ti.",
    "El activo_ti es una infraestructura.",
    "El servidor necesita monitoreo.",
    "El servidor_bd necesita respaldo.",
    "El monitor monitorea servidor_web.",
]


def construir_red(oraciones: list[str]) -> tuple[RedSemantica, list[tuple[str, str, str]]]:
    red = RedSemantica()
    triples = []

    for oracion in oraciones:
        triple = red.agregar_oracion(oracion)
        triples.append(triple)

    return red, triples


def analizar(
    oraciones: list[str],
    origen: str = "servidor_web",
    categoria: str = "infraestructura",
    concepto_propiedades: str = "servidor_web",
) -> dict[str, object]:
    red, triples = construir_red(oraciones)
    ruta = red.ruta_es_un(origen, categoria)
    propiedades = red.propiedades_heredadas(concepto_propiedades, "necesita")

    triple_consulta = (origen, "es_un", categoria)
    es_explicita = triple_consulta in red.triples
    demostrada = ruta is not None

    if demostrada and es_explicita:
        tipo_consulta = "explicita"
        explicacion = (
            f"La relación {origen} es_un {categoria} está almacenada directamente "
            "como un triple de la red."
        )
    elif demostrada:
        tipo_consulta = "inferida"
        explicacion = (
            f"La relación {origen} es_un {categoria} no está almacenada directamente. "
            "Se demuestra recorriendo la jerarquía es_un."
        )
    else:
        tipo_consulta = "sin_evidencia"
        explicacion = (
            f"No existe una ruta es_un desde {origen} hasta {categoria} con los hechos "
            "actualmente almacenados. Esto significa que la conclusión no está demostrada, "
            "no que sea universalmente falsa."
        )

    inferencias = []

    if demostrada and not es_explicita:
        inferencias.append({
            "tipo": "jerarquia",
            "triple": [origen, "es_un", categoria],
            "ruta": ruta or [],
            "explicacion": explicacion,
        })

    for item in propiedades:
        triple_propiedad = (
            concepto_propiedades,
            "necesita",
            item["propiedad"],
        )
        if triple_propiedad not in red.triples:
            inferencias.append({
                "tipo": "herencia",
                "triple": list(triple_propiedad),
                "origen_propiedad": item["origen"],
                "explicacion": (
                    f"{concepto_propiedades} hereda la propiedad necesita "
                    f"{item['propiedad']} desde la categoría {item['origen']}."
                ),
            })

    consulta_negativa_origen = "servidor_web"
    consulta_negativa_categoria = "servidor_bd"
    ruta_negativa = red.ruta_es_un(
        consulta_negativa_origen,
        consulta_negativa_categoria,
    )

    return {
        "success": True,
        "oraciones": oraciones,
        "triples": [list(t) for t in triples],
        "conceptos": red.conceptos(),
        "cantidad_conceptos": len(red.conceptos()),
        "cantidad_triples": len(red.triples),
        "consulta_jerarquia": {
            "origen": origen,
            "categoria": categoria,
            "demostrada": demostrada,
            "es_explicita": es_explicita,
            "tipo": tipo_consulta,
            "ruta": ruta or [],
            "explicacion": explicacion,
        },
        "propiedades": {
            "concepto": concepto_propiedades,
            "relacion": "necesita",
            "resultados": propiedades,
        },
        "inferencias": inferencias,
        "consulta_sin_evidencia": {
            "origen": consulta_negativa_origen,
            "categoria": consulta_negativa_categoria,
            "demostrada": ruta_negativa is not None,
            "ruta": ruta_negativa or [],
            "interpretacion": (
                "No demostrada con la evidencia disponible."
                if ruta_negativa is None
                else "Demostrada por la red actual."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--oraciones-json", default=None)
    parser.add_argument("--origen", default="servidor_web")
    parser.add_argument("--categoria", default="infraestructura")
    parser.add_argument("--propiedades", default="servidor_web")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.oraciones_json:
        try:
            oraciones = json.loads(args.oraciones_json)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"JSON de oraciones inválido: {exc}") from exc

        if not isinstance(oraciones, list) or not all(
            isinstance(item, str) for item in oraciones
        ):
            raise SystemExit("Las oraciones deben enviarse como lista de textos.")
    else:
        oraciones = ORACIONES_PREDETERMINADAS

    try:
        resultado = analizar(
            oraciones,
            args.origen,
            args.categoria,
            args.propiedades,
        )
    except ValueError as exc:
        if args.json:
            print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False))
            raise SystemExit(2) from exc
        raise

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False))
        return

    print("=" * 68)
    print("SEMANA 14 - RED SEMÁNTICA | SERVIDORIA")
    print("=" * 68)

    print("\nTRIPLES EXPLÍCITOS")
    for sujeto, relacion, objeto in resultado["triples"]:
        print(f"  ({sujeto}, {relacion}, {objeto})")

    consulta = resultado["consulta_jerarquia"]
    print(
        f"\n¿{consulta['origen']} es_un {consulta['categoria']}?:",
        consulta["demostrada"],
    )
    print("Tipo de resultado:", consulta["tipo"])
    print("Explicación:", consulta["explicacion"])

    if consulta["ruta"]:
        print("Ruta:", " -> ".join(consulta["ruta"]))

    print(f"\nPropiedades heredadas de {args.propiedades}:")
    propiedades = resultado["propiedades"]["resultados"]
    if propiedades:
        for item in propiedades:
            print(
                f"  necesita {item['propiedad']} "
                f"(heredado desde {item['origen']})"
            )
    else:
        print("  No se encontraron propiedades heredables.")

    print("\nINFERENCIAS GENERADAS")
    if resultado["inferencias"]:
        for item in resultado["inferencias"]:
            triple = item["triple"]
            print(f"  ({triple[0]}, {triple[1]}, {triple[2]})")
            print(f"    {item['explicacion']}")
    else:
        print("  No se generaron inferencias nuevas para estas consultas.")

    negativa = resultado["consulta_sin_evidencia"]
    print(
        f"\nConsulta sin evidencia: {negativa['origen']} es_un "
        f"{negativa['categoria']}? -> {negativa['demostrada']}"
    )
    print("Interpretación:", negativa["interpretacion"])


if __name__ == "__main__":
    main()
