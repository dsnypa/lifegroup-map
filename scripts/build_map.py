#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import folium
import pandas as pd


DEFAULT_CENTER = (29.4243, -98.4911)
DEFAULT_ZOOM = 10
DEFAULT_RADIUS_MILES = 1.5
DEFAULT_COLOR = "#cc0000"


def short_label(name: str) -> str:
    n = str(name).strip()
    low = n.lower()
    if low == "harvest city ya":
        return "Harvest City YA"
    if low == "seniors life group":
        return "Seniors"
    if low == "women's life group":
        return "Women's"
    return n.replace(" Life Group", "").split()[0]


def deterministic_offset(lat: float, lon: float, key: str, max_deg: float = 0.0032) -> tuple[float, float]:
    h = int(hashlib.md5(key.encode("utf-8")).hexdigest()[:8], 16)
    lat_off = (((h % 1000) / 1000) - 0.5) * (2 * max_deg)
    lon_off = ((((h // 1000) % 1000) / 1000) - 0.5) * (2 * max_deg)
    return lat + lat_off, lon + lon_off


def load_rows(csv_path: Path) -> list[dict]:
    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]

    required = {"Name", "Latitude", "Longitude"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    df = df.dropna(subset=["Latitude", "Longitude"]).copy()

    rows: list[dict] = []
    for _, r in df.iterrows():
        name = str(r["Name"]).strip()
        label = str(r["Label"]).strip() if "Label" in df.columns and pd.notna(r.get("Label")) else short_label(name)
        note = str(r["Note"]).strip() if "Note" in df.columns and pd.notna(r.get("Note")) else ""
        radius_miles = float(r["RadiusMiles"]) if "RadiusMiles" in df.columns and pd.notna(r.get("RadiusMiles")) else DEFAULT_RADIUS_MILES
        color = str(r["Color"]).strip() if "Color" in df.columns and pd.notna(r.get("Color")) else DEFAULT_COLOR

        rows.append(
            {
                "name": name,
                "label": label,
                "note": note,
                "lat": float(r["Latitude"]),
                "lon": float(r["Longitude"]),
                "radius_meters": int(radius_miles * 1609.34),
                "color": color,
            }
        )
    return rows


def build_map(rows: list[dict], output_path: Path) -> None:
    m = folium.Map(location=list(DEFAULT_CENTER), zoom_start=DEFAULT_ZOOM, control_scale=True)

    for idx, row in enumerate(rows):
        olat, olon = deterministic_offset(row["lat"], row["lon"], row["name"] + "|" + row["note"], max_deg=0.0032)

        spread = [(0, 0), (0.008, -0.008), (-0.008, 0.008)][idx % 3]
        label_lat = olat + spread[0]
        label_lon = olon + spread[1]

        tooltip = row["name"] + (f" - {row['note']}" if row["note"] else "")

        folium.Circle(
            location=(olat, olon),
            radius=row["radius_meters"],
            color=row["color"],
            weight=2,
            fill=True,
            fill_color=row["color"],
            fill_opacity=0.22,
            tooltip=tooltip,
        ).add_to(m)

        html = f"""
        <div style="
            font-size:10px;
            color:#111;
            background: rgba(255,255,255,0.72);
            padding:2px 4px;
            border-radius:3px;
            border:1px solid rgba(0,0,0,0.18);
            white-space: nowrap;
            font-family: Arial, sans-serif;
            box-shadow: 0 0 2px rgba(0,0,0,0.12);">
            {row["label"]}
        </div>
        """
        folium.Marker(
            location=(label_lat, label_lon),
            icon=folium.DivIcon(html=html),
        ).add_to(m)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(output_path))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a LifeGroup location map from CSV coordinates.")
    parser.add_argument("--input", default="input/lifegroups.csv", help="Input CSV path")
    parser.add_argument("--output", default="output/lifegroups_map.html", help="Output HTML path")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    rows = load_rows(input_path)
    build_map(rows, output_path)

    print(f"Loaded {len(rows)} plotted locations from {input_path}")
    print(f"Wrote map to {output_path}")


if __name__ == "__main__":
    main()
