# Validación del dataset — AdD 5B2026, Actividad Individual 1

Todos los valores son observados al ejecutar `scripts/validate.py` sobre el CSV generado.

## Ficha de entrega

| Campo | Valor |
|---|---|
| Nombre del dataset | Atractivos naturales de Argentina (muestra derivada de OpenStreetMap) |
| Fuente | OpenStreetMap, vía Overpass API (`overpass-api.de`) |
| Enlace público | https://www.openstreetmap.org/ |
| Fecha de extracción | 2026-10-23 |
| Licencia | ODbL (https://www.openstreetmap.org/copyright) |
| Archivo | `data/processed/atractivos_naturales_argentina.csv` (CSV, UTF-8, un archivo) |
| Filas | 1000 |
| Columnas | 8: `osm_type`, `osm_id`, `name`, `attraction_type`, `latitude`, `longitude`, `ele`, `has_name` |
| Numéricas | `latitude`, `longitude`, `ele` (`osm_id` es identificador y no se cuenta) |
| Categóricas | `attraction_type` (4 categorías), `osm_type` (2), `has_name` (2) |
| Datos reales | Sí, ninguna fila fue inventada |

## Extracción

Total en OSM (Argentina, 2026-10-23): 12 859 elementos → 12 852 únicos tras quitar 7 objetos con más de una etiqueta de interés.

| Tipo | Etiqueta OSM | Únicos en OSM |
|---|---|---|
| peak | `natural=peak` | 9 641 |
| viewpoint | `tourism=viewpoint` | 2 092 |
| waterfall | `waterway=waterfall` | 1 015 |
| cave_entrance | `natural=cave_entrance` | 104 |

**Corrección respecto del README inicial:** las cascadas se etiquetan `waterway=waterfall`. Con `natural=waterfall` la consulta devuelve 0 elementos.

## Criterio de muestreo

La fuente excede las 2000 filas, así que se tomó una muestra determinística (`scripts/prepare.py`, `random_state=42`):
`cave_entrance` completo (104) y el resto repartido en partes iguales entre `peak`, `viewpoint` y `waterfall` hasta llegar a 1000.
Muestra final: peak 299, viewpoint 299, waterfall 298, cave_entrance 104.

**La muestra no es representativa de la proporción real por tipo** (en OSM, las cumbres son el 75 %). No es la totalidad de los puntos del país.

## Valores faltantes observados

| Columna | Faltantes |
|---|---|
| `name` | 448 (44.8 %) |
| `ele` | 789 (78.9 %) |
| resto | 0 |

Cobertura de `ele` por tipo: peak 67.2 %, viewpoint 2.7 %, cave_entrance 1.9 %, waterfall 0 %. Casi toda la elevación existe solo para cumbres, es decir, un faltante estructural, no aleatorio.

## Limitaciones y anomalías

- 2 registros con `ele = 0`: una cueva de Neuquén (osm_id 13283053198), en plena cordillera, probablemente un valor de relleno; y un mirador de Tierra del Fuego (osm_id 5067076021). Se dejaron sin modificar.
- Para elementos `way` (55 filas) la coordenada es el centro calculado por Overpass (`out center`), no la entrada física.
- No se incluyó `province`: requiere un cruce con límites provinciales que no se descargó.
- Se verificó que todos los puntos caen dentro de una caja envolvente aproximada de Argentina (lat −55.2 a −21.7, lon −73.7 a −53.5); no es una prueba de pertenencia exacta al territorio.
- Los datos de OSM pueden estar incompletos o desactualizados.
