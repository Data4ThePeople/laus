"""Stage E, part 1: county shapes, projected in Python into a fixed reference
canvas so the page needs no projection code.

Source: Census cartographic boundary counties, 2024 vintage, 1:5m
(cb_2024_us_county_5m), cached under data/raw/geo/. Includes Puerto Rico.

Composite projection in the Albers USA style, extended with Puerto Rico:
the lower 48 on Albers (29.5/45.5, center -96); Alaska on its own Albers,
scaled down and placed lower left; Hawaii lower middle; Puerto Rico lower
right, scaled up so its 78 municipios can be hovered.

Output: data/geo.json with, for every county, its FIPS, name, state and rings
in tenths of a reference pixel on a REF_W x REF_H canvas, plus the inset
boxes. Simplified after projection so eastern counties still read at embed
size.

Run:  python -m lfd.geo
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pandas as pd
import requests
import shapefile  # pyshp
from pyproj import Transformer
from shapely.geometry import MultiPolygon, Polygon, shape
from shapely.ops import transform as shp_transform

from lfd import DATA, PANEL_PATH, RAW

GEO_RAW = RAW / "geo"
GEO_OUT = DATA / "geo.json"
SHP_NAME = "cb_2024_us_county_5m"
SHP_URL = f"https://www2.census.gov/geo/tiger/GENZ2024/shp/{SHP_NAME}.zip"

REF_W, REF_H = 1000, 660     # reference canvas in CSS pixels
UNITS = 10                   # stored coordinates are tenths of a pixel
SIMPLIFY_PX = 0.35           # Douglas-Peucker tolerance after projection
MARGIN = 12

# Territories without LAUS county series: American Samoa, Guam, N. Marianas, USVI.
DROP_STATEFP = {"60", "66", "69", "78"}

ALBERS = {
    "conus": "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96 +datum=WGS84 +units=m",
    "ak": "+proj=aea +lat_1=55 +lat_2=65 +lat_0=50 +lon_0=-154 +datum=WGS84 +units=m",
    "hi": "+proj=aea +lat_1=8 +lat_2=18 +lat_0=13 +lon_0=-157 +datum=WGS84 +units=m",
    "pr": "+proj=aea +lat_1=17 +lat_2=19 +lat_0=18 +lon_0=-66.5 +datum=WGS84 +units=m",
}
# Relative scale and anchor (as a fraction of the CONUS frame) for each inset.
# Anchor = where the inset's bbox center lands, in reference pixels.
INSETS = {
    "ak": {"scale": 0.36, "cx": 0.135 * REF_W, "cy": 0.86 * REF_H},
    "hi": {"scale": 1.0,  "cx": 0.345 * REF_W, "cy": 0.90 * REF_H},
    "pr": {"scale": 3.2,  "cx": 0.90 * REF_W,  "cy": 0.905 * REF_H},
}


def region(statefp: str) -> str:
    return {"02": "ak", "15": "hi", "72": "pr"}.get(statefp, "conus")


def fetch(refresh: bool = False) -> Path:
    GEO_RAW.mkdir(parents=True, exist_ok=True)
    shp = GEO_RAW / f"{SHP_NAME}.shp"
    if shp.exists() and not refresh:
        return shp
    z = GEO_RAW / f"{SHP_NAME}.zip"
    r = requests.get(SHP_URL, headers={"User-Agent": "Mozilla/5.0 Data4ThePeople/lfd (https://www.data4thepeople.com)"},
                     timeout=120)
    r.raise_for_status()
    z.write_bytes(r.content)
    with zipfile.ZipFile(z) as zf:
        zf.extractall(GEO_RAW)
    return shp


def read_counties(shp: Path) -> list[dict]:
    rd = shapefile.Reader(str(shp))
    fields = [f[0] for f in rd.fields[1:]]
    out = []
    for sr in rd.iterShapeRecords():
        rec = dict(zip(fields, sr.record))
        if rec["STATEFP"] in DROP_STATEFP:
            continue
        out.append({"fips": rec["GEOID"], "name": rec["NAME"], "state": rec["STUSPS"],
                    "statefp": rec["STATEFP"], "geom": shape(sr.shape.__geo_interface__)})
    return out


def _polys(g) -> list[Polygon]:
    if isinstance(g, Polygon):
        return [g]
    if isinstance(g, MultiPolygon):
        return list(g.geoms)
    return []


def project_all(counties: list[dict]) -> tuple[list[dict], dict]:
    """Project each region, then place regions on the reference canvas."""
    tf = {k: Transformer.from_crs("EPSG:4326", v, always_xy=True) for k, v in ALBERS.items()}
    for c in counties:
        c["region"] = region(c["statefp"])
        t = tf[c["region"]]
        c["proj"] = shp_transform(lambda x, y, t=t: t.transform(x, y), c["geom"])

    # CONUS frame: fit its bbox into the canvas with a margin.
    def bbox(reg):
        xs, ys = [], []
        for c in counties:
            if c["region"] == reg:
                b = c["proj"].bounds
                xs += [b[0], b[2]]; ys += [b[1], b[3]]
        return min(xs), min(ys), max(xs), max(ys)

    cb = bbox("conus")
    cw, ch = cb[2] - cb[0], cb[3] - cb[1]
    s = min((REF_W - 2 * MARGIN) / cw, (REF_H - 2 * MARGIN - 0.14 * REF_H) / ch)  # leave a strip below
    ox = MARGIN + ((REF_W - 2 * MARGIN) - cw * s) / 2
    oy = MARGIN

    def place_conus(x, y):
        return ox + (x - cb[0]) * s, oy + (cb[3] - y) * s

    placers = {"conus": place_conus}
    boxes = {}
    for reg, spec in INSETS.items():
        b = bbox(reg)
        rs = s * spec["scale"]
        bw, bh = (b[2] - b[0]) * rs, (b[3] - b[1]) * rs
        x0, y0 = spec["cx"] - bw / 2, spec["cy"] - bh / 2

        def place(x, y, b=b, rs=rs, x0=x0, y0=y0):
            return x0 + (x - b[0]) * rs, y0 + (b[3] - y) * rs

        placers[reg] = place
        pad = 4
        boxes[reg] = [round(x0 - pad, 1), round(y0 - pad, 1), round(bw + 2 * pad, 1), round(bh + 2 * pad, 1)]

    out = []
    for c in counties:
        pl = placers[c["region"]]
        g = shp_transform(lambda x, y, pl=pl: pl(x, y), c["proj"])
        g = g.simplify(SIMPLIFY_PX, preserve_topology=True)
        rings = []
        for poly in _polys(g):
            if poly.area < 0.15:      # sub-pixel islands
                continue
            for ring in [poly.exterior, *poly.interiors]:
                pts = [(round(x * UNITS), round(y * UNITS)) for x, y in ring.coords[:-1]]
                # drop consecutive duplicates after rounding
                dedup = [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]
                if len(dedup) >= 3:
                    rings.append([v for p in dedup for v in p])
        if not rings:  # keep at least the largest polygon even if tiny
            poly = max(_polys(g), key=lambda p: p.area)
            pts = [(round(x * UNITS), round(y * UNITS)) for x, y in poly.exterior.coords[:-1]]
            rings.append([v for p in pts for v in p])
        b = g.bounds
        out.append({"fips": c["fips"], "name": c["name"], "state": c["state"], "region": c["region"],
                    "rings": rings, "bbox": [round(b[0] * UNITS), round(b[1] * UNITS),
                                             round(b[2] * UNITS), round(b[3] * UNITS)]})
    out.sort(key=lambda c: c["fips"])
    return out, boxes


def reconcile(counties: list[dict]) -> None:
    """Print LAUS counties without a shape and shapes without a LAUS series."""
    panel = pd.read_parquet(PANEL_PATH, columns=["fips", "area", "date", "labor_force"])
    latest = panel[panel.date == panel.date.max()]
    laus = panel.drop_duplicates("fips").set_index("fips").area
    shapes = {c["fips"]: f'{c["name"]}, {c["state"]}' for c in counties}
    no_shape = sorted(set(laus.index) - set(shapes))
    no_laus = sorted(set(shapes) - set(laus.index))
    print(f"shapes: {len(shapes):,}  LAUS counties: {len(laus):,}  "
          f"with a value in latest month: {latest.labor_force.notna().sum():,}")
    print(f"LAUS without a shape ({len(no_shape)}): {[laus[f] for f in no_shape]}")
    print(f"shape without LAUS ({len(no_laus)}): {[shapes[f] for f in no_laus]}")
    dup = pd.Series([c["fips"] for c in counties]).duplicated()
    if dup.any():
        raise ValueError("duplicate FIPS in shapes")


def main() -> None:
    shp = fetch()
    counties = read_counties(shp)
    placed, boxes = project_all(counties)
    n_pts = sum(len(r) // 2 for c in placed for r in c["rings"])
    GEO_OUT.parent.mkdir(parents=True, exist_ok=True)
    GEO_OUT.write_text(json.dumps({"ref": [REF_W, REF_H], "units": UNITS, "insets": boxes,
                                   "counties": placed}, separators=(",", ":")))
    print(f"wrote {GEO_OUT}: {len(placed):,} counties, {n_pts:,} points, "
          f"{GEO_OUT.stat().st_size / 1e6:.2f} MB json; insets {boxes}")
    reconcile(placed)


if __name__ == "__main__":
    main()
