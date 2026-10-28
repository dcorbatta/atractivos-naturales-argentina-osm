"""Validaciones de la consigna (AdD 5B2026 - Actividad Individual 1)."""
from pathlib import Path

import pandas as pd

PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "atractivos_naturales_argentina.csv"
# Caja envolvente aproximada de Argentina continental e insular (sin Antártida).
LAT_MIN, LAT_MAX = -55.2, -21.7
LON_MIN, LON_MAX = -73.7, -53.5

df = pd.read_csv(PATH)

assert 200 <= len(df) <= 2000, f"Filas fuera de rango: {len(df)}"
assert df.shape[1] >= 5, f"Columnas insuficientes: {df.shape[1]}"

# osm_id es un identificador, no una variable numérica analítica.
numeric_cols = [c for c in df.select_dtypes(include="number").columns if c != "osm_id"]
categorical_cols = df.select_dtypes(include=["object", "string", "category", "bool"]).columns.tolist()
# name es texto libre, no una categoría.
categorical_cols = [c for c in categorical_cols if c != "name"]

assert {"latitude", "longitude"}.issubset(numeric_cols)
assert len(numeric_cols) >= 2, f"Numéricas: {numeric_cols}"
assert len(categorical_cols) >= 2, f"Categóricas: {categorical_cols}"
assert df[["latitude", "longitude"]].notna().all().all(), "Hay coordenadas faltantes"
assert df["latitude"].between(-90, 90).all(), "Latitud inválida"
assert df["longitude"].between(-180, 180).all(), "Longitud inválida"
assert not df.duplicated(["osm_type", "osm_id"]).any(), "OSM IDs duplicados"
for col in ["attraction_type", "osm_type"]:
    assert df[col].nunique() >= 2, f"{col} tiene menos de 2 categorías observadas"

inside = df["latitude"].between(LAT_MIN, LAT_MAX) & df["longitude"].between(LON_MIN, LON_MAX)
outside = df[~inside]
assert outside.empty, f"{len(outside)} puntos fuera de la caja de Argentina:\n{outside}"

print(f"OK: {len(df)} filas, {df.shape[1]} columnas")
print("Numéricas:", numeric_cols)
print("Categóricas:", categorical_cols)
print("\nValores faltantes por columna:")
print(df.isna().sum().to_string())
print("\nCategorías de atractivos:")
print(df["attraction_type"].value_counts(dropna=False).to_string())
print("\nTipos de elemento OSM:")
print(df["osm_type"].value_counts(dropna=False).to_string())
print("\nCobertura de ele por tipo (% con elevación):")
print((df.groupby("attraction_type")["ele"].apply(lambda s: s.notna().mean()) * 100).round(1).to_string())
print("\nResumen numérico:")
print(df[numeric_cols].describe().round(2).to_string())
