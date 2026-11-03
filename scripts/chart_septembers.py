"""Chart: share of U.S. counties in Structural Loss, the last 15 Septembers.

Same-month comparison only: every bar is a September. Values are recomputed
from data/classified.parquet at render time.

Run:  .venv/bin/python scripts/chart_septembers.py [--month 2026-09] [--years 15]
"""

from __future__ import annotations

import argparse

import pandas as pd
from matplotlib.ticker import FuncFormatter

from lfd import CLASSIFIED_PATH, ROOT
from lfd.chartstyle import BG, CORAL, GRID, INK, MUTED, figure, frame
from lfd.classify import STRUCTURAL_LOSS

OUT = ROOT / "outputs" / "charts" / "sep26-01-septembers.png"
PAST = "#6E4A3C"   # earlier Septembers: the coral, darkened, so the latest stands out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--month", default="2026-09")
    ap.add_argument("--years", type=int, default=15)
    a = ap.parse_args()
    d = pd.Timestamp(f"{a.month}-01")

    cl = pd.read_parquet(CLASSIFIED_PATH)
    s = cl[(cl.date.dt.month == d.month) & (cl.date <= d)]
    g = s.groupby(s.date.dt.year).category.agg(
        total="size", sl=lambda c: (c.astype(str) == STRUCTURAL_LOSS).sum())
    g = g.tail(a.years)
    g["share"] = g.sl / g.total * 100

    fig, ax = figure(8.4, 5.0)
    cols = [CORAL if y == d.year else PAST for y in g.index]
    ax.bar(g.index, g.share, color=cols, width=0.72)
    for y, v in g.share.items():
        ax.annotate(f"{v:.1f}%", xy=(y, v), xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8,
                    color=INK if y == d.year else MUTED,
                    fontweight="bold" if y == d.year else "normal")
    ax.set_xticks(g.index)
    ax.set_xticklabels([str(y) for y in g.index], fontsize=8.5)
    ax.set_ylim(0, 44); ax.set_yticks(range(0, 41, 10))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    last = g.iloc[-1]
    frame(fig, f"Structural labor force loss, every {d:%B} since {g.index[0]}",
          f"Share of U.S. counties and Puerto Rico municipios whose labor force is more than 10% below\n"
          f"the same month 20 years earlier. "
          f"{d:%B %Y}: {int(last.sl):,} of {int(last.total):,}.", top=0.78)
    fig.savefig(OUT, facecolor=BG)
    print(f"wrote {OUT}"); print(g.round(1).to_string())


if __name__ == "__main__":
    main()
