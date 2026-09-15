"""Stage E, part 2: build the self-contained interactive map, dist/index.html.

Everything the page draws is emitted here from the pipeline outputs. The
template (templates/index.html) carries no numbers of its own: band edges
come from classify.BINS, labels from classify.LABELS, colors from COLORS
below, and every value from the Parquet files.

Blocks are typed arrays, gzip-compressed and base64-encoded; the page
decodes them with the browser's built-in DecompressionStream.

Block layout (nC counties in META.counties order, nF frames, nM months):
  geo    Int16   per county: nRings; per ring: nPts, x0, y0, dx, dy, ...
                 in tenths of a reference pixel; nRings = 0 when no shape
  cat    Uint8   nF x nC, band code 0..5 in LABELS order, 255 = no data
  pct    Uint8   two planes of nF x nC bytes: low then high bytes of the
                 frame-to-frame delta (mod 65536) of the 20-year change in
                 tenths of a percent, stored as int16 with -32768 = none;
                 v[f] = (v[f-1] + delta) mod 65536, v[-1] = 0
  lf     Uint16  two planes of nC x nM bytes: low bytes then high bytes of
                 the month-to-month delta of the quantized labor force;
                 q[t] = (q[t-1] + delta) mod 65536, q[-1] = 0, 65535 = missing,
                 value = q * META.lfScale[county]
  watch  Uint8   nF x nC, 0 none, 1 positive watch, 2 negative watch

Run:  python -m lfd.viz
"""

from __future__ import annotations

import base64
import gzip
import json
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from lfd import CLASSIFIED_PATH, DIST, PANEL_PATH
from lfd.classify import BINS, LABELS
from lfd.geo import GEO_OUT
from lfd.watch import WATCH_PATH

TEMPLATE = Path(__file__).parent / "templates" / "index.html"
ASSETS = Path(__file__).resolve().parents[2] / "assets"
LOGO_ON_LIGHT = ASSETS / "d4tp-text-dark.svg"     # dark plate, white type
LOGO_ON_DARK = ASSETS / "d4tp-text-light_3.svg"   # white plate, dark type
OUT = DIST / "index.html"
FIRST_FRAME = "2010-01"

# Six bands, worst to best (LABELS order). Diverging coral -> teal; checked
# in OKLab for lightness order within each arm and text contrast on paper.
COLORS = ["#712B13", "#C4795A", "#B9D6C8", "#7FB5A3", "#3E8C74", "#085041"]
NODATA = "#E6E3DD"
PALETTE = {"teal": "#085041", "coral": "#712B13", "paper": "#F7F5EF", "ink": "#1F2A27"}

# Known causes for months with missing data; the affected counts come from the data.
GAP_CAUSES = {
    "2025-10": "the federal appropriations lapse",
}


def _b64gz(arr: np.ndarray) -> str:
    return base64.b64encode(gzip.compress(arr.tobytes(), 9)).decode("ascii")


def build_geo_block(geo: dict, index: dict[str, int], n: int) -> np.ndarray:
    per = {c["fips"]: c for c in geo["counties"]}
    out: list[int] = []
    for fips, _ in sorted(index.items(), key=lambda kv: kv[1]):
        c = per.get(fips)
        rings = c["rings"] if c else []
        out.append(len(rings))
        for r in rings:
            out.append(len(r) // 2)
            px, py = 0, 0
            for i in range(0, len(r), 2):
                x, y = r[i], r[i + 1]
                out += [x - px, y - py]
                px, py = x, y
    a = np.array(out, dtype=np.int64)
    if a.max() > 32767 or a.min() < -32768:
        raise ValueError("geometry delta exceeds int16")
    return a.astype(np.int16)


def build_lf_block(panel: pd.DataFrame, fips_order: list[str], months: pd.DatetimeIndex):
    wide = (panel.pivot(index="fips", columns="date", values="labor_force")
                 .reindex(index=fips_order, columns=months))
    a = wide.to_numpy()
    mx = np.nanmax(np.where(np.isnan(a), 0, a), axis=1)
    scale = np.maximum(mx / 65000.0, 1.0)
    q = np.rint(a / scale[:, None])
    q = np.where(np.isnan(q), 65535, q).astype(np.int32)
    d = np.diff(q, axis=1, prepend=0) & 0xFFFF
    lo = (d & 0xFF).astype(np.uint8)
    hi = (d >> 8).astype(np.uint8)
    return np.concatenate([lo.ravel(), hi.ravel()]), scale


def build() -> dict:
    geo = json.loads(GEO_OUT.read_text())
    panel = pd.read_parquet(PANEL_PATH)
    cl = pd.read_parquet(CLASSIFIED_PATH)
    watch = pd.read_parquet(WATCH_PATH)

    first = panel.drop_duplicates("fips").set_index("fips")
    laus_names, laus_state = first["area"], first["state"]
    geo_names = {c["fips"]: f'{c["name"]}, {c["state"]}' for c in geo["counties"]}
    geo_state = {c["fips"]: c["state"] for c in geo["counties"]}
    fips_order = sorted(set(laus_names.index) | set(geo_names))
    index = {f: i for i, f in enumerate(fips_order)}
    n = len(fips_order)
    counties = [{"f": f, "n": laus_names.get(f, geo_names.get(f)), "s": laus_state.get(f, geo_state.get(f))}
                for f in fips_order]

    months = pd.period_range(panel.date.min(), panel.date.max(), freq="M").to_timestamp()
    frames = pd.period_range(FIRST_FRAME, panel.date.max(), freq="M").to_timestamp()
    nM, nF = len(months), len(frames)
    m0 = list(months).index(frames[0])
    assert m0 == 240, f"first frame must be 240 months after the panel start, got {m0}"

    code = {lab: i for i, lab in enumerate(LABELS)}
    cat = np.full((nF, n), 255, dtype=np.uint8)
    pct = np.full((nF, n), -32768, dtype=np.int16)
    fidx = {d: i for i, d in enumerate(frames)}
    sub = cl[cl.date.isin(frames)]
    r = sub.date.map(fidx).to_numpy()
    c = sub.fips.map(index).to_numpy()
    cat[r, c] = sub.category.astype(str).map(code).to_numpy().astype(np.uint8)
    pct[r, c] = np.clip(np.rint(sub["pct_change"].to_numpy() * 1000), -32767, 32767).astype(np.int16)

    wf = np.zeros((nF, n), dtype=np.uint8)
    ws = watch[watch.date.isin(frames)]
    wf[ws.date.map(fidx).to_numpy(), ws.fips.map(index).to_numpy()] = ws.flag.to_numpy().astype(np.uint8)

    lf_block, scale = build_lf_block(panel, fips_order, months)
    geo_block = build_geo_block(geo, index, n)

    # Gap notes: counties missing in a frame but present in both neighbors.
    notes = {}
    has = cat != 255
    for f in range(1, nF - 1):
        back = has[max(0, f - 3):f].any(axis=0)
        ahead = has[f + 1:f + 4].any(axis=0)
        gap = back & ahead & ~has[f]
        if gap.sum() >= 20:
            states = pd.Series([counties[i]["n"].rsplit(", ", 1)[-1] for i in np.where(gap)[0]]).value_counts()
            where = f"in {states.index[0]}" if len(states) == 1 else "nationwide"
            key = f"{frames[f]:%Y-%m}"
            cause = GAP_CAUSES.get(key)
            notes[f] = (f"BLS published no data for {int(gap.sum()):,} counties {where} this month"
                        + (f" ({cause})." if cause else "."))

    # Consistency check: the counts the page will derive must match Python.
    for f, d in [(fidx[pd.Timestamp("2026-04-01")], "2026-04")] if pd.Timestamp("2026-04-01") in fidx else []:
        from lfd.classify import category_counts, snapshot
        py = category_counts(snapshot(cl, 2026, 4))
        js = {LABELS[k]: int((cat[f] == k).sum()) for k in range(6)}
        for lab in LABELS:
            assert py[lab] == js[lab], f"{d} {lab}: python {py[lab]} vs block {js[lab]}"

    meta = {
        "ref": geo["ref"], "units": geo["units"], "insets": geo["insets"],
        "counties": counties, "nC": n,
        "frameStart": FIRST_FRAME, "nF": nF, "lfStart": f"{months[0]:%Y-%m}", "nM": nM, "m0": m0,
        "bins": [None if b in (float("inf"), -float("inf")) else b for b in BINS],
        "labels": LABELS, "colors": COLORS, "nodata": NODATA, "palette": PALETTE,
        "lfScale": [round(float(s), 4) for s in scale],
        "notes": notes,
        "latest": f"{months[-1]:%Y-%m}", "built": date.today().isoformat(),
        "source": "U.S. Bureau of Labor Statistics, Local Area Unemployment Statistics (LAUS), county civilian labor force, not seasonally adjusted.",
    }
    pd16 = np.diff(pct.astype(np.int32) & 0xFFFF, axis=0, prepend=0) & 0xFFFF
    pct_block = np.concatenate([(pd16 & 0xFF).astype(np.uint8).ravel(), (pd16 >> 8).astype(np.uint8).ravel()])
    blocks = {"geo": _b64gz(geo_block), "cat": _b64gz(cat), "pct": _b64gz(pct_block),
              "lf": _b64gz(lf_block), "watch": _b64gz(wf)}
    return {"meta": meta, "blocks": blocks}


def render(out: Path = OUT) -> Path:
    built = build()
    html = TEMPLATE.read_text()
    inject = ("const META = " + json.dumps(built["meta"], separators=(",", ":")) + ";\n"
              + "const BLOCKS = " + json.dumps(built["blocks"], separators=(",", ":")) + ";")
    assert "/*__DATA__*/" in html
    html = html.replace("/*__DATA__*/", inject)
    for marker, path, cls in (("<!--__LOGO_ON_LIGHT__-->", LOGO_ON_LIGHT, "logo logo-light"),
                              ("<!--__LOGO_ON_DARK__-->", LOGO_ON_DARK, "logo logo-dark")):
        svg = path.read_text()
        svg = svg[svg.index("<svg"):]
        svg = svg.replace("<svg ", f'<svg class="{cls}" role="img" aria-label="Data 4 The People" ', 1)
        # scope the SVG's own style rule so two inline copies do not collide
        svg = svg.replace('<style>.cls-1{fill:#fff;}</style>', "")
        svg = svg.replace('class="cls-1"', 'fill="#fff"')
        assert marker in html
        html = html.replace(marker, svg)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    sizes = {k: len(v) / 1e6 for k, v in built["blocks"].items()}
    print(f"wrote {out}: {out.stat().st_size / 1e6:.2f} MB total; blocks (MB base64): "
          + ", ".join(f"{k} {v:.2f}" for k, v in sizes.items()))
    print(f"counties {built['meta']['nC']}, frames {built['meta']['nF']}, months {built['meta']['nM']}, "
          f"gap notes at frames {list(built['meta']['notes'])}")
    return out


def main(argv: list[str] | None = None) -> None:
    render()


if __name__ == "__main__":
    main()
