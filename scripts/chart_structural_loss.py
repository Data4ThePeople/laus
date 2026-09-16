"""Chart: share of U.S. counties in Structural Loss, every month on record.

The series starts January 2010, the first month with a 20-year comparison,
and every value is recomputed from data/classified.parquet at render time.
October 2025 is left as a gap because BLS published no county data that month.

Run:  .venv/bin/python scripts/chart_structural_loss.py [--out PATH]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

from lfd import CLASSIFIED_PATH, ROOT
from lfd.classify import STRUCTURAL_LOSS

BG, INK, MUTED, GRID = "#181A1B", "#BBBDC0", "#8C9094", "#2A2E31"
CORAL = "#C4795A"          # the Structural Loss band colour, lightened for a dark background
SOURCE = "U.S. Bureau of Labor Statistics (LAUS); Data 4 The People analysis."


def series() -> pd.DataFrame:
    cl = pd.read_parquet(CLASSIFIED_PATH)
    g = cl.groupby("date")["category"].agg(total="size",
                                           sl=lambda c: (c.astype(str) == STRUCTURAL_LOSS).sum())
    g = g[g.total > 1000]      # October 2025: Puerto Rico only, not a national reading
    g["share"] = g.sl / g.total * 100
    return g.reindex(pd.date_range(g.index.min(), g.index.max(), freq="MS"))   # gap stays a gap


def render(out: Path, minimal: bool = False) -> Path:
    g = series()
    first, last = g.dropna().iloc[0], g.dropna().iloc[-1]
    first_d, last_d = g.dropna().index[0], g.dropna().index[-1]
    covid = g.loc["2020-01":"2020-12"].share.idxmax()

    fig, ax = plt.subplots(figsize=(8.4, 5.0), dpi=200)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    # October 2025 has no county data. The fill bridges it so the shape reads
    # continuously, and the line is drawn dashed across the gap to mark it.
    bridged = g.share.interpolate()
    gap = g.share.isna()
    ax.fill_between(g.index, 0, bridged, color=CORAL, alpha=0.16, linewidth=0)
    span = g.index[gap.shift(1, fill_value=False) | gap | gap.shift(-1, fill_value=False)]
    ax.plot(span, bridged.loc[span], color=CORAL, linewidth=1.6, linestyle=(0, (2, 2)), zorder=3)
    ax.plot(g.index, g.share, color=CORAL, linewidth=2.0, solid_capstyle="round", zorder=4)

    ax.set_ylim(0, 48); ax.set_xlim(g.index.min(), last_d + pd.DateOffset(months=4))
    ax.set_yticks(range(0, 41, 10))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)

    fig.text(0.055, 0.955, "Counties in structural labor force loss, 2010 to 2026",
             color=INK, fontsize=15, fontweight="bold", va="top")
    fig.text(0.055, 0.893,
             "Share of U.S. counties whose labor force is more than 10% below the same month 20 years earlier",
             color=MUTED, fontsize=10, va="top")
    fig.text(0.055, 0.035, SOURCE, color=MUTED, fontsize=8.5)
    fig.text(0.945, 0.035, "Built by Data 4 The People", color=MUTED, fontsize=8.5, ha="right")
    fig.subplots_adjust(left=0.075, right=0.975, top=0.80, bottom=0.115)

    arrow = dict(arrowstyle="-", color=MUTED, linewidth=0.9, shrinkA=0, shrinkB=4)
    ax.scatter([last_d], [last.share], s=44, color=CORAL, zorder=5, edgecolor=BG, linewidth=1.5)
    ax.annotate(f"July 2026: {last.share:.0f}% of counties,\n{int(last.sl):,} of {int(last.total):,}",
                xy=(last_d, last.share), xytext=(-14, 34), textcoords="offset points",
                color=INK, fontsize=10, fontweight="bold", ha="right", va="bottom",
                linespacing=1.5, arrowprops=arrow)
    if minimal:                      # hero version: one call-out, nothing else
        fig.savefig(out, facecolor=BG)
        print(f"wrote {out} (minimal)")
        return out
    ax.annotate(f"COVID peak, {covid:%B %Y}: {g.loc[covid, 'share']:.1f}%",
                xy=(covid, g.loc[covid, "share"]), xytext=(10, 26), textcoords="offset points",
                color=MUTED, fontsize=9, ha="left", va="bottom", arrowprops=arrow)
    ax.annotate(f"{first_d:%B %Y}: {first.share:.0f}%, {int(first.sl):,} counties",
                xy=(first_d, first.share), xytext=(14, -26), textcoords="offset points",
                color=MUTED, fontsize=9, va="top", arrowprops=arrow)
    ax.annotate("No county data,\nOctober 2025",
                xy=(pd.Timestamp("2025-10-01"), float(bridged.loc["2025-10-01"])),
                xytext=(-18, -46), textcoords="offset points", color=MUTED, fontsize=8.5,
                ha="right", va="center", linespacing=1.4, arrowprops=arrow)

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out} ({out.stat().st_size/1e3:.0f} KB)")
    print(f"latest {last_d:%Y-%m}: {int(last.sl):,} of {int(last.total):,} counties, {last.share:.1f}%")
    print(f"previous record: {g.drop(last_d).share.idxmax():%Y-%m} at {g.drop(last_d).share.max():.1f}%")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=ROOT / "outputs" / "charts" / "01-structural-loss-over-time.png")
    ap.add_argument("--minimal", action="store_true", help="hero version: only the latest call-out")
    a = ap.parse_args()
    render(a.out, a.minimal)


if __name__ == "__main__":
    main()
