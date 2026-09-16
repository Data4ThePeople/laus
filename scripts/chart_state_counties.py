"""Year-over-year labor force change for a state's largest counties.

Built for the Colorado section: the big metro counties are all falling, but
most of them do not yet carry the map's negative-watch flag, because that flag
also asks for a three-year decline.

Run:  .venv/bin/python scripts/chart_state_counties.py --state CO --top 10
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from matplotlib.ticker import FuncFormatter

from lfd import CLASSIFIED_PATH, PANEL_PATH, ROOT
from lfd.chartstyle import BG, CORAL, GRID, INK, MUTED, TEAL, figure, frame
from lfd.watch import NEGATIVE, WATCH_PATH

NAMES = {"CO": "Colorado", "MI": "Michigan", "SC": "South Carolina"}


def render(state: str, month: str, top: int, out: Path) -> None:
    cl = pd.read_parquet(CLASSIFIED_PATH)
    lf = pd.read_parquet(PANEL_PATH).pivot(index="date", columns="fips", values="labor_force")
    w = pd.read_parquet(WATCH_PATH)
    d = f"{month}-01"
    s = cl[(cl.date == d) & (cl.state == state)].copy()
    s["flag"] = s.fips.map(w[w.date == d].set_index("fips").flag)
    year_ago = (pd.Timestamp(d) - pd.DateOffset(years=1)).strftime("%Y-%m-%d")
    s["yoy"] = [(lf.loc[d][f] / lf.loc[year_ago][f] - 1) * 100 for f in s.fips]
    s["name"] = s.area.str.replace(f", {state}", "", regex=False).str.replace(" County/city", "").str.replace(" County", "")
    g = s.nlargest(top, "labor_force").sort_values("labor_force")

    fig, ax = figure(8.4, 5.0)
    colours = [CORAL if v < 0 else TEAL for v in g.yoy]
    ax.barh(range(len(g)), g.yoy, color=colours, height=0.62)
    ax.set_yticks(range(len(g))); ax.set_yticklabels(g.name, color=INK, fontsize=10.5)
    ax.axvline(0, color=GRID, linewidth=1.0)
    lo = min(g.yoy.min() * 1.55, -1)
    ax.set_xlim(lo, abs(lo) * 0.35); ax.set_xticks([]); ax.grid(False)
    for i, row in enumerate(g.itertuples()):
        ax.annotate(f"{row.yoy:+.1f}%", xy=(row.yoy, i), xytext=(-8 if row.yoy < 0 else 8, 0),
                    textcoords="offset points", color=INK, fontsize=10.5, fontweight="bold",
                    va="center", ha="right" if row.yoy < 0 else "left")
        ax.annotate(f"{row.labor_force/1000:,.0f}K workers", xy=(abs(lo) * 0.03, i),
                    color=MUTED, fontsize=9, va="center")
    flagged = g[g.flag == NEGATIVE].name.tolist()
    note = ("None is on negative watch yet" if not flagged
            else f"Only {' and '.join(flagged)} is on negative watch so far")
    frame(fig, f"{NAMES.get(state, state)}'s largest counties are all shrinking",
          f"Change in labor force, {pd.Timestamp(year_ago):%B %Y} to {pd.Timestamp(d):%B %Y}. {note}.",
          top=0.82)
    fig.subplots_adjust(left=0.155, right=0.965)
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}")
    print(g[["name", "labor_force", "yoy", "flag"]].round(1).to_string(index=False))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--state", default="CO")
    ap.add_argument("--month", default="2026-07")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()
    out = a.out or ROOT / "outputs" / "charts" / f"03c-{a.state.lower()}-largest-counties.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    render(a.state, a.month, a.top, out)


if __name__ == "__main__":
    main()
