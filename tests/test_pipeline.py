import unittest
import pandas as pd
from src.pipeline import transform


class TestTransform(unittest.TestCase):
    def test_calculates_total_and_removes_invalid_rows(self):
        source = pd.DataFrame([
            {"id_venta": 1, "fecha": "2026-10-01", "cliente": " Ana ",
             "producto": " Teclado ", "cantidad": 2, "precio_unitario": 10.5},
            {"id_venta": 2, "fecha": "2026-10-02", "cliente": "",
             "producto": "Ratón", "cantidad": 1, "precio_unitario": 5},
            {"id_venta": 3, "fecha": "2026-10-02", "cliente": "Luis",
             "producto": "Cable", "cantidad": 0, "precio_unitario": 3},
        ])
        result = transform(source)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["cliente"], "Ana")
        self.assertEqual(result.iloc[0]["importe_total"], 21.0)

    def test_removes_exact_duplicates(self):
        row = {"id_venta": 1, "fecha": "2026-10-01", "cliente": "Ana",
               "producto": "Teclado", "cantidad": 1, "precio_unitario": 10}
        result = transform(pd.DataFrame([row, row]))
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
