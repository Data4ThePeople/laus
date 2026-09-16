"""Takeaway 3: the states where the most counties are sliding.

Writes two charts:
  03a  the five states with the largest share of counties on negative watch
  03b  a Michigan county map, negative watch against everything else

Both recompute from data/classified.parquet, data/watch.parquet and
data/geo.json at render time.

Run:  .venv/bin/python scripts/chart_negative_watch.py [--month 2026-07]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon

from lfd import CLASSIFIED_PATH, DATA, ROOT
from lfd.chartstyle import BG, CORAL, GRID, INK, MUTED, TEAL, figure, frame, word_legend
from lfd.watch import NEGATIVE, POSITIVE, WATCH_PATH

STATE_NAMES = {"VT": "Vermont", "MI": "Michigan", "WY": "Wyoming", "CO": "Colorado",
               "IL": "Illinois", "WV": "West Virginia", "ME": "Maine", "NC": "North Carolina"}
NEUTRAL = "#4A4F52"


def table(month: str) -> pd.DataFrame:
    cl = pd.read_parquet(CLASSIFIED_PATH)
    w = pd.read_parquet(WATCH_PATH)
    d = f"{month}-01"
    s = cl[cl.date == d].merge(w[w.date == d][["fips", "flag"]], on="fips")
    return s


def chart_states(s: pd.DataFrame, month: str, out: Path, top: int = 5) -> None:
    g = s.groupby("state").apply(lambda d: pd.Series({
        "counties": len(d), "neg": int((d.flag == NEGATIVE).sum()),
        "pos": int((d.flag == POSITIVE).sum()), "pct": 100 * (d.flag == NEGATIVE).mean()}),
        include_groups=False)
    g = g[g.counties >= 10].sort_values("pct", ascending=False).head(top).iloc[::-1]

    fig, ax = figure(8.4, 4.6)
    y = range(len(g))
    ax.barh(list(y), g.pct, color=[CORAL if i != "MI" else "#D98A62" for i in g.index], height=0.62)
    ax.set_yticks(list(y)); ax.set_yticklabels([STATE_NAMES.get(i, i) for i in g.index], color=INK, fontsize=11)
    ax.set_xlim(0, 108); ax.set_xticks([]); ax.grid(False)
    for i, (code, row) in enumerate(g.iterrows()):
        ax.annotate(f"{row.pct:.0f}%", xy=(row.pct, i), xytext=(8, 0), textcoords="offset points",
                    color=INK, fontsize=11, fontweight="bold", va="center")
        ax.annotate(f"{int(row.neg)} of {int(row.counties)} counties, "
                    f"{'none' if row.pos == 0 else int(row.pos)} recovering",
                    xy=(1.2, i), color=BG, fontsize=9.5, va="center", fontweight="bold")
    ax.tick_params(axis="y", pad=8)
    frame(fig, "Five states where the labor force is sliding almost everywhere",
          f"Counties on negative watch, {pd.Timestamp(f'{month}-01'):%B %Y}: labor force down from a year ago and from three years ago",
          top=0.83)
    fig.subplots_adjust(left=0.145, right=0.965)
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}")
    print(g.iloc[::-1].round(1).to_string())


def chart_michigan(s: pd.DataFrame, month: str, out: Path, state: str = "MI") -> None:
    geo = json.loads((DATA / "geo.json").read_text())
    units = geo["units"]
    flags = s.set_index("fips").flag
    names = s.set_index("fips").area
    lf = s.set_index("fips").labor_force

    fig, ax = figure(8.4, 5.6)
    patches, colours = [], []
    xs, ys = [], []
    for c in geo["counties"]:
        if c["state"] != state or c["fips"] not in flags.index:
            continue
        neg = flags[c["fips"]] == NEGATIVE
        for ring in c["rings"]:
            pts = [(ring[i] / units, ring[i + 1] / units) for i in range(0, len(ring), 2)]
            patches.append(Polygon(pts, closed=True))
            colours.append(CORAL if neg else NEUTRAL)
            xs += [p[0] for p in pts]; ys += [p[1] for p in pts]
    ax.add_collection(PatchCollection(patches, facecolor=colours, edgecolor=BG, linewidth=0.7))
    pad = 6
    ax.set_xlim(min(xs) - pad, max(xs) + pad * 6)
    ax.set_ylim(max(ys) + pad, min(ys) - pad)     # canvas y runs downward
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    ax.spines["bottom"].set_visible(False)

    # name the largest counties that are not sliding
    keep = [f for f in flags.index if f.startswith("26") and flags[f] != NEGATIVE]
    offsets = [(34, 36), (48, -4), (34, -40)]
    for (dx, dy), f in zip(offsets, sorted(keep, key=lambda f: -lf[f])[:3]):
        c = next(x for x in geo["counties"] if x["fips"] == f)
        cx = (c["bbox"][0] + c["bbox"][2]) / 2 / units
        cy = (c["bbox"][1] + c["bbox"][3]) / 2 / units
        ax.annotate(names[f].replace(" County, MI", ""), xy=(cx, cy), xytext=(dx, dy),
                    textcoords="offset points", color=INK, fontsize=9, fontweight="bold",
                    arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.9, shrinkA=0, shrinkB=2))

    n_neg = int((flags[[f for f in flags.index if f.startswith("26")]] == NEGATIVE).sum())
    n_all = len([f for f in flags.index if f.startswith("26")])
    n_pos = int((flags[[f for f in flags.index if f.startswith("26")]] == POSITIVE).sum())
    frame(fig, f"Michigan: {n_neg} of {n_all} counties are losing labor force",
          f"Counties on negative watch, {pd.Timestamp(f'{month}-01'):%B %Y}. "
          f"{'No Michigan county is' if n_pos == 0 else str(n_pos) + ' Michigan counties are'} recovering.", top=0.86)
    word_legend(fig, [("Negative watch", CORAL), ("Not on negative watch", MUTED)], y=0.80)
    fig.subplots_adjust(left=0.03, right=0.97, bottom=0.08)
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}: {n_neg} of {n_all} on negative watch, {n_pos} recovering")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--month", default="2026-07")
    ap.add_argument("--dir", type=Path, default=ROOT / "outputs" / "charts")
    a = ap.parse_args()
    s = table(a.month)
    a.dir.mkdir(parents=True, exist_ok=True)
    chart_states(s, a.month, a.dir / "03a-negative-watch-states.png")
    chart_michigan(s, a.month, a.dir / "03b-michigan-negative-watch.png")


if __name__ == "__main__":
    main()
