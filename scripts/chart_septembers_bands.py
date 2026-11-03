"""Chart: share of U.S. counties in each of the six bands, every September since 2012.

Small multiples, one panel per band, shared 0-40% scale so panels compare
directly. Same-month comparison only: every bar is a September. Values are
recomputed from data/classified.parquet at render time.

Run:  .venv/bin/python scripts/chart_septembers_bands.py [--month 2026-09] [--years 15]
"""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

from lfd import CLASSIFIED_PATH, ROOT
from lfd.chartstyle import BG, CREDIT, GRID, INK, MUTED, SOURCE
from lfd.classify import LABELS

OUT = ROOT / "outputs" / "charts" / "sep26-09-septembers-bands.png"
# Map band colours, lightened where the dark background would swallow them (worst to best).
COLOURS = ["#C4795A", "#D9A58C", "#B9D6C8", "#7FB5A3", "#5FA78C", "#4E9E84"]
SHORT = ["Structural Loss", "At-risk Contraction", "Below-trend Growth", "Keeping Pace", "Superstars", "Hyper-Growth"]
RANGE = ["below -10%", "-10% to 0%", "0% to 10%", "10% to 20%", "20% to 40%", "above 40%"]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--month", default="2026-09")
    ap.add_argument("--years", type=int, default=15)
    a = ap.parse_args()
    d = pd.Timestamp(f"{a.month}-01")
    cl = pd.read_parquet(CLASSIFIED_PATH)
    s = cl[(cl.date.dt.month == d.month) & (cl.date <= d)]
    t = pd.crosstab(s.date.dt.year, s.category.astype(str), normalize="index").reindex(columns=LABELS) * 100
    t = t.tail(a.years)

    fig, axes = plt.subplots(2, 3, figsize=(8.4, 5.6), dpi=200, sharey=True)
    fig.patch.set_facecolor(BG)
    for ax, lab, short, rng, col in zip(axes.flat, LABELS, SHORT, RANGE, COLOURS):
        ax.set_facecolor(BG)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(colors=MUTED, labelsize=7.5, length=0)
        ax.set_axisbelow(True)
        v = t[lab]
        ax.bar(v.index, v, color=[col if y == d.year else col + "66" for y in v.index], width=0.75)
        for y in (v.index[0], v.index[-1]):
            last = y == d.year
            ax.annotate(f"{v[y]:.1f}%", xy=(y, v[y]), xytext=(0, 3), textcoords="offset points", ha="center",
                        va="bottom", fontsize=7.5, color=INK if last else MUTED,
                        fontweight="bold" if last else "normal")
        ax.set_title(f"{short}\n", loc="left", color=col, fontsize=9.5, fontweight="bold", pad=2)
        ax.text(0, 1.02, rng, transform=ax.transAxes, color=MUTED, fontsize=7.5, va="bottom")
        ax.set_xticks([v.index[0], v.index[-1]]); ax.set_xticklabels([str(v.index[0]), str(v.index[-1])])
        ax.set_ylim(0, 42); ax.set_yticks(range(0, 41, 10))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
        ax.grid(axis="y", color=GRID, linewidth=0.8)
    fig.text(0.055, 0.955, f"Fewer fast-growing counties than in any {d:%B} since {t.index[0]}", color=INK, fontsize=15,
             fontweight="bold", va="top")
    fig.text(0.055, 0.898, "Share of U.S. counties and Puerto Rico municipios in each band, by change in labor force from\n"
             f"the same month 20 years earlier. {d:%B} of each year; {d.year} highlighted.", color=MUTED, fontsize=10, va="top")
    fig.text(0.055, 0.03, SOURCE, color=MUTED, fontsize=8.5)
    fig.text(0.945, 0.03, CREDIT, color=MUTED, fontsize=8.5, ha="right")
    fig.subplots_adjust(left=0.075, right=0.975, top=0.76, bottom=0.10, hspace=0.62, wspace=0.12)
    fig.savefig(OUT, facecolor=BG)
    print(f"wrote {OUT}"); print(t.round(1).to_string())


if __name__ == "__main__":
    main()
