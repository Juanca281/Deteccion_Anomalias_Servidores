"""Pruebas unitarias de Semana 14."""

import unittest

from red_semantica import RedSemantica, interpretar, normalizar


class RedSemanticaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.red = RedSemantica()
        self.red.agregar("servidor_web", "es_un", "servidor")
        self.red.agregar("servidor", "es_un", "activo_ti")
        self.red.agregar("activo_ti", "es_un", "infraestructura")
        self.red.agregar("servidor", "necesita", "monitoreo")

    def test_relacion_explicita(self) -> None:
        self.assertTrue(self.red.es_un("servidor_web", "servidor"))

    def test_transitividad(self) -> None:
        self.assertTrue(self.red.es_un("servidor_web", "infraestructura"))
        self.assertEqual(
            self.red.ruta_es_un("servidor_web", "infraestructura"),
            ["servidor_web", "servidor", "activo_ti", "infraestructura"],
        )

    def test_herencia_propiedad(self) -> None:
        propiedades = self.red.propiedades_heredadas("servidor_web")
        self.assertEqual(
            propiedades,
            [{"propiedad": "monitoreo", "origen": "servidor"}],
        )

    def test_sin_evidencia_suficiente(self) -> None:
        self.assertFalse(self.red.es_un("servidor_web", "servidor_bd"))

    def test_interpretar_oracion(self) -> None:
        self.assertEqual(
            interpretar("El servidor_web es un servidor."),
            ("servidor_web", "es_un", "servidor"),
        )

    def test_normalizacion(self) -> None:
        self.assertEqual(normalizar("  LATÉNCIA  "), "latencia")

    def test_oracion_invalida(self) -> None:
        with self.assertRaises(ValueError):
            interpretar("El servidor está funcionando muy rápido.")

    def test_ciclo_no_bloquea(self) -> None:
        self.red.agregar("infraestructura", "es_un", "servidor_web")
        self.assertFalse(self.red.es_un("servidor_web", "base_datos"))
        self.assertEqual(
            self.red.propiedades_heredadas("servidor_web"),
            [{"propiedad": "monitoreo", "origen": "servidor"}],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
