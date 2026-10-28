"""Convierte el JSON crudo de Overpass en data/processed/atractivos_naturales_argentina.csv.

Muestreo (determinístico, ver reports/validacion.md):
  - cave_entrance se toma completo (105 puntos, la categoría menos frecuente).
  - Las otras tres categorías aportan la misma cantidad hasta llegar a N_TOTAL,
    con pandas.sample(random_state=42).
La muestra NO representa la proporción real de cada tipo en Argentina.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "osm_atractivos_argentina.json"
OUT = ROOT / "data" / "processed" / "atractivos_naturales_argentina.csv"
N_TOTAL = 1000
SEED = 42


def parse_ele(value):
    """'1234', '1234.5' o '1234 m' -> float; cualquier otra cosa -> NaN."""
    if value is None:
        return float("nan")
    try:
        return float(str(value).lower().replace("m", "").replace(",", ".").strip())
    except ValueError:
        return float("nan")


def load_rows() -> pd.DataFrame:
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    rows = []
    for category, resp in raw["categories"].items():
        for el in resp["elements"]:
            tags = el.get("tags", {})
            lat = el.get("lat", el.get("center", {}).get("lat"))
            lon = el.get("lon", el.get("center", {}).get("lon"))
            rows.append(
                {
                    "osm_type": el["type"],
                    "osm_id": el["id"],
                    "name": tags.get("name"),
                    "attraction_type": category,
                    "latitude": lat,
                    "longitude": lon,
                    "ele": parse_ele(tags.get("ele")),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    df = load_rows()
    print(f"Elementos crudos: {len(df)}")

    df = df.dropna(subset=["latitude", "longitude"])
    df = df.drop_duplicates(subset=["osm_type", "osm_id", "attraction_type"])
    # Un mismo objeto OSM con dos etiquetas de interés cuenta una sola vez.
    df = df.drop_duplicates(subset=["osm_type", "osm_id"])
    print(f"Tras limpieza (coordenadas, duplicados): {len(df)}")
    print(df["attraction_type"].value_counts().to_string())

    caves = df[df["attraction_type"] == "cave_entrance"]
    others = df[df["attraction_type"] != "cave_entrance"]
    kinds = sorted(others["attraction_type"].unique())
    remaining = N_TOTAL - len(caves)
    base, extra = divmod(remaining, len(kinds))
    parts = [caves]
    for i, kind in enumerate(kinds):
        n = base + (1 if i < extra else 0)
        pool = others[others["attraction_type"] == kind]
        parts.append(pool.sample(n=min(n, len(pool)), random_state=SEED))
    sample = pd.concat(parts).sort_values(["attraction_type", "osm_type", "osm_id"])

    sample["has_name"] = sample["name"].notna()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sample.to_csv(OUT, index=False, encoding="utf-8")
    print(f"Muestra exportada: {len(sample)} filas -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
