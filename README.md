# Atractivos naturales de Argentina (OpenStreetMap)

Dataset de 1000 puntos de interés naturales de Argentina (cumbres, miradores, cascadas y cuevas), extraído de OpenStreetMap con la Overpass API. Se armó para la Actividad Individual 1 de Análisis de Datos (FIUBA-CEIA, 5B2026) y como base para explorar consultas de la app **Viaje**.

**Archivo principal:** [`data/processed/atractivos_naturales_argentina.csv`](data/processed/atractivos_naturales_argentina.csv) (CSV, UTF-8)

Descarga directa:
`https://raw.githubusercontent.com/dcorbatta/atractivos-naturales-argentina-osm/main/data/processed/atractivos_naturales_argentina.csv`

## Qué contiene

Datos reales; no se inventó ninguna fila. Una fila es un punto de interés natural individual. Extracción del 2026-10-23.

| Columna | Tipo | Descripción |
|---|---|---|
| `osm_type` | categórica | `node` o `way`: tipo de elemento en OSM |
| `osm_id` | identificador | ID original de OSM (no es una medición) |
| `name` | texto | Nombre, si está cargado (faltante en 44.8 %) |
| `attraction_type` | categórica | `peak`, `viewpoint`, `waterfall`, `cave_entrance` |
| `latitude`, `longitude` | numéricas | Coordenadas WGS84 |
| `ele` | numérica | Elevación en metros declarada en OSM (faltante en 78.9 %, casi toda existe solo para cumbres) |
| `has_name` | categórica | Si el punto tiene nombre |

## Cómo se armó la muestra

OSM tiene 12 852 elementos únicos de estos cuatro tipos en Argentina. Para quedar en 1000 filas se tomó una muestra determinística (`random_state=42`): todas las cuevas (104) y el resto repartido en partes iguales entre cumbres, miradores y cascadas.

**La muestra no refleja la proporción real por tipo** (en OSM las cumbres son el 75 %) ni es la totalidad de los puntos del país. Los detalles, los faltantes y las anomalías están en [`reports/validacion.md`](reports/validacion.md).

## Reproducir

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/fetch.py      # descarga de Overpass -> data/raw/
python scripts/prepare.py    # muestra de 1000 filas -> data/processed/
python scripts/validate.py   # chequea la consigna
```

La consulta original está en [`queries/argentina_naturaleza.overpassql`](queries/argentina_naturaleza.overpassql). Las cascadas se etiquetan `waterway=waterfall` (con `natural=waterfall` devuelve 0).

## Licencia y atribución

Datos © colaboradores de [OpenStreetMap](https://www.openstreetmap.org/copyright), disponibles bajo la [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/1-0/). Si usás o redistribuís estos datos, tenés que atribuir a OpenStreetMap y compartir las bases derivadas bajo la misma licencia.

Los datos de OSM pueden estar incompletos o desactualizados. No interpretes un punto como un lugar accesible, abierto o seguro sin verificarlo en otra fuente.
