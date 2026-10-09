"""Pipeline ETL de ventas: CSV -> limpieza/transformación -> CSV y SQLite."""
from pathlib import Path
import logging
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "ventas.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_FILE = PROCESSED_DIR / "ventas_limpias.csv"
DB_DIR = ROOT / "data" / "warehouse"
DB_FILE = DB_DIR / "ventas.db"
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"

REQUIRED_COLUMNS = [
    "id_venta", "fecha", "cliente", "producto", "cantidad", "precio_unitario"
]


def configure_logging():
    """Configura logs en consola y en un fichero."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )


def extract(path=RAW_FILE):
    """E: extrae los datos desde el CSV de origen."""
    if not path.exists():
        raise FileNotFoundError(f"No existe el fichero de entrada: {path}")
    df = pd.read_csv(path)
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas obligatorias: {sorted(missing)}")
    logging.info("Extracción completada: %s filas", len(df))
    return df


def transform(df):
    """T: normaliza, valida y calcula el importe de cada venta."""
    result = df.copy()
    result = result.drop_duplicates()

    result["fecha"] = pd.to_datetime(result["fecha"], errors="coerce")
    result["cantidad"] = pd.to_numeric(result["cantidad"], errors="coerce")
    result["precio_unitario"] = pd.to_numeric(
        result["precio_unitario"], errors="coerce"
    )
    result["cliente"] = result["cliente"].astype("string").str.strip()
    result["producto"] = result["producto"].astype("string").str.strip()

    before = len(result)
    valid = (
        result["id_venta"].notna()
        & result["fecha"].notna()
        & result["cliente"].notna()
        & result["cliente"].ne("")
        & result["producto"].notna()
        & result["producto"].ne("")
        & result["cantidad"].notna()
        & result["cantidad"].gt(0)
        & result["precio_unitario"].notna()
        & result["precio_unitario"].ge(0)
    )
    result = result.loc[valid].copy()
    result["cantidad"] = result["cantidad"].astype(int)
    result["importe_total"] = (
        result["cantidad"] * result["precio_unitario"]
    ).round(2)
    result["fecha"] = result["fecha"].dt.strftime("%Y-%m-%d")
    logging.info("Transformación completada: %s filas válidas; %s descartadas",
                 len(result), before - len(result))
    return result


def load(df):
    """L: guarda un CSV curado y carga una tabla SQLite."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    DB_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(PROCESSED_FILE, index=False, encoding="utf-8")
    with sqlite3.connect(DB_FILE) as connection:
        df.to_sql("ventas", connection, if_exists="replace", index=False)
    logging.info("Carga completada: CSV=%s; SQLite=%s", PROCESSED_FILE, DB_FILE)


def run_pipeline():
    configure_logging()
    logging.info("Inicio del pipeline ETL")
    raw = extract()
    clean = transform(raw)
    load(clean)
    logging.info("Pipeline finalizado correctamente: %s registros cargados", len(clean))


if __name__ == "__main__":
    run_pipeline()
