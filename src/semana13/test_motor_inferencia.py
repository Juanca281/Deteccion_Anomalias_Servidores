"""Pruebas funcionales de Semana 13."""

import unittest

from motor_inferencia import Regla, construir_reglas, inferir


class MotorInferenciaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.base = {
            "cpu_alta",
            "ram_alta",
            "latencia_alta",
            "errores_altos",
            "disco_critico",
        }

    def test_caso_a_demuestra_mantenimiento(self) -> None:
        hechos, trazas = inferir(self.base, construir_reglas())
        self.assertIn("mantenimiento_recomendado", hechos)
        self.assertTrue(any(p["regla"] == "R6" for p in trazas))

    def test_caso_b_no_demuestra_mantenimiento(self) -> None:
        hechos, _ = inferir(
            self.base - {"disco_critico"},
            construir_reglas(),
        )
        self.assertNotIn("mantenimiento_recomendado", hechos)

    def test_hechos_iniciales_se_conservan(self) -> None:
        original = set(self.base)
        inferir(self.base, construir_reglas())
        self.assertEqual(self.base, original)

    def test_no_hay_conclusiones_duplicadas(self) -> None:
        hechos, trazas = inferir(self.base, construir_reglas())
        conclusiones = [paso["conclusion"] for paso in trazas]
        self.assertEqual(len(conclusiones), len(set(conclusiones)))
        self.assertEqual(len(hechos), len(set(hechos)))

    def test_ciclo_termina(self) -> None:
        reglas = [
            Regla("C1", frozenset({"a"}), "b"),
            Regla("C2", frozenset({"b"}), "a"),
        ]
        hechos, trazas = inferir({"a"}, reglas)
        self.assertEqual(hechos, {"a", "b"})
        self.assertEqual(len(trazas), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
