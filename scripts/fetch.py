"""Descarga los atractivos naturales de Argentina desde Overpass API.

Una consulta por categoría (la consulta combinada puede agotar el timeout).
Guarda la respuesta cruda sin modificar en data/raw/.
"""
import json
import time
from datetime import date
from pathlib import Path

import requests

ENDPOINT = "https://overpass-api.de/api/interpreter"
HEADERS = {"User-Agent": "fiuba-add-actividad1/1.0 (trabajo practico, uso academico)"}
RAW = Path(__file__).resolve().parent.parent / "data" / "raw"

CATEGORIES = {
    "waterfall": ("waterway", "waterfall"),
    "viewpoint": ("tourism", "viewpoint"),
    "peak": ("natural", "peak"),
    "cave_entrance": ("natural", "cave_entrance"),
}


def query(key: str, value: str) -> str:
    return (
        "[out:json][timeout:180];\n"
        'area["ISO3166-1"="AR"][admin_level=2]->.ar;\n'
        f'nwr["{key}"="{value}"](area.ar);\n'
        "out center tags;"
    )


def fetch(name: str, key: str, value: str, retries: int = 3) -> dict:
    for attempt in range(1, retries + 1):
        resp = requests.post(
            ENDPOINT, data={"data": query(key, value)}, headers=HEADERS, timeout=240
        )
        if resp.status_code == 200:
            return resp.json()
        print(f"  {name}: HTTP {resp.status_code} (intento {attempt}/{retries})")
        time.sleep(30 * attempt)
    resp.raise_for_status()


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    combined = {"extraction_date": date.today().isoformat(), "source": ENDPOINT, "categories": {}}
    for name, (key, value) in CATEGORIES.items():
        data = fetch(name, key, value)
        n = len(data.get("elements", []))
        print(f"{name}: {n} elementos (osm3s: {data.get('osm3s', {}).get('timestamp_osm_base')})")
        (RAW / f"osm_{name}.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        combined["categories"][name] = data
        time.sleep(10)
    (RAW / "osm_atractivos_argentina.json").write_text(
        json.dumps(combined, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
