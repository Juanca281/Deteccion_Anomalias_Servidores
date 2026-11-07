"""Semana 14 - Red semántica aplicada a ServidorIA."""

from __future__ import annotations

import re
import unicodedata

RELACIONES_ADMITIDAS = {"es_un", "necesita", "monitorea"}
RELACIONES_HEREDABLES = {"necesita"}


def normalizar(texto: str) -> str:
    """Normaliza mayúsculas, tildes, guiones y espacios."""

    base = unicodedata.normalize("NFD", texto.casefold().strip())
    sin_tildes = "".join(
        c for c in base if unicodedata.category(c) != "Mn"
    )
    sin_tildes = sin_tildes.replace("-", "_")
    sin_tildes = re.sub(r"\s+", " ", sin_tildes)
    return sin_tildes


def normalizar_concepto(texto: str) -> str:
    """Convierte un concepto a una etiqueta canónica."""

    texto = normalizar(texto).strip(" .!?;:")
    texto = re.sub(r"\s+", "_", texto)
    return texto


def interpretar(oracion: str) -> tuple[str, str, str]:
    """Interpreta un conjunto restringido de oraciones del dominio."""

    texto = normalizar(oracion).strip(" .!?;:")

    patrones = [
        (
            r"(?:un|una|el|la) ([\w_]+) es (?:un|una|el|la) ([\w_]+)",
            "es_un",
        ),
        (
            r"(?:un|una|el|la) ([\w_]+) necesita ([\w_]+)",
            "necesita",
        ),
        (
            r"(?:un|una|el|la) ([\w_]+) monitorea ([\w_]+)",
            "monitorea",
        ),
    ]

    for patron, relacion in patrones:
        coincidencia = re.fullmatch(patron, texto)
        if coincidencia:
            sujeto, objeto = coincidencia.groups()
            return (
                normalizar_concepto(sujeto),
                relacion,
                normalizar_concepto(objeto),
            )

    raise ValueError(
        "Oración no admitida. Usa estructuras como: "
        "'El servidor_web es un servidor' o "
        "'El servidor necesita monitoreo'."
    )


class RedSemantica:
    """Grafo dirigido etiquetado con consultas e inferencia."""

    def __init__(self) -> None:
        self.aristas: dict[str, list[tuple[str, str]]] = {}
        self.triples: list[tuple[str, str, str]] = []

    def agregar(self, sujeto: str, relacion: str, objeto: str) -> None:
        sujeto = normalizar_concepto(sujeto)
        relacion = normalizar_concepto(relacion)
        objeto = normalizar_concepto(objeto)

        if relacion not in RELACIONES_ADMITIDAS:
            raise ValueError(f"Relación no admitida: {relacion}")

        triple = (sujeto, relacion, objeto)
        if triple in self.triples:
            return

        self.triples.append(triple)
        self.aristas.setdefault(sujeto, []).append((relacion, objeto))

    def agregar_oracion(self, oracion: str) -> tuple[str, str, str]:
        triple = interpretar(oracion)
        self.agregar(*triple)
        return triple

    def conceptos(self) -> list[str]:
        nodos: set[str] = set()
        for sujeto, _, objeto in self.triples:
            nodos.add(sujeto)
            nodos.add(objeto)
        return sorted(nodos)

    def relacionados(self, concepto: str) -> list[tuple[str, str]]:
        concepto = normalizar_concepto(concepto)
        return sorted(self.aristas.get(concepto, []))

    def ruta_es_un(self, origen: str, categoria: str) -> list[str] | None:
        """Devuelve una ruta jerárquica si existe, con control de ciclos."""

        origen = normalizar_concepto(origen)
        categoria = normalizar_concepto(categoria)
        pendientes: list[tuple[str, list[str]]] = [(origen, [origen])]
        visitados: set[str] = set()

        while pendientes:
            actual, ruta = pendientes.pop(0)

            if actual == categoria:
                return ruta

            if actual in visitados:
                continue

            visitados.add(actual)

            for relacion, destino in self.aristas.get(actual, []):
                if relacion == "es_un" and destino not in visitados:
                    pendientes.append((destino, ruta + [destino]))

        return None

    def es_un(self, origen: str, categoria: str) -> bool:
        return self.ruta_es_un(origen, categoria) is not None

    def propiedades_heredadas(
        self,
        concepto: str,
        relacion: str = "necesita",
    ) -> list[dict[str, str]]:
        """Hereda propiedades declaradas como propagables por jerarquía."""

        relacion = normalizar_concepto(relacion)
        if relacion not in RELACIONES_HEREDABLES:
            raise ValueError(
                f"La relación '{relacion}' no está definida como heredable."
            )

        concepto = normalizar_concepto(concepto)
        pendientes = [concepto]
        visitados: set[str] = set()
        resultados: dict[str, str] = {}

        while pendientes:
            actual = pendientes.pop()
            if actual in visitados:
                continue
            visitados.add(actual)

            for rel, destino in self.aristas.get(actual, []):
                if rel == "es_un":
                    pendientes.append(destino)
                elif rel == relacion and destino not in resultados:
                    resultados[destino] = actual

        return [
            {"propiedad": propiedad, "origen": origen}
            for propiedad, origen in sorted(resultados.items())
        ]
