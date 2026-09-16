"""Chart: the share of counties that lost labor force from January to July,
every year since 1990.

Both ends of the window sit inside the same year, so this comparison never
crosses the January population-control change. Every value is recomputed from
data/laus_county_lf.parquet at render time.

Run:  .venv/bin/python scripts/chart_jan_july.py [--out PATH]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from matplotlib.ticker import FuncFormatter

from lfd import PANEL_PATH, ROOT
from lfd.chartstyle import BG, CORAL, GRID, INK, MUTED, TEAL, figure, frame, word_legend

FIRST, COVID = 1990, 2020


def series() -> pd.DataFrame:
    lf = pd.read_parquet(PANEL_PATH).pivot(index="date", columns="fips", values="labor_force")
    rows = []
    for y in range(FIRST, lf.index.max().year + 1):
        jan, jul = pd.Timestamp(f"{y}-01-01"), pd.Timestamp(f"{y}-07-01")
        if jan not in lf.index or jul not in lf.index:
            continue
        r = (lf.loc[jul] / lf.loc[jan] - 1).dropna()
        rows.append((y, len(r), (r < 0).mean() * 100))
    t = pd.DataFrame(rows, columns=["year", "counties", "down"]).set_index("year")
    t["up"] = 100 - t.down          # counties that gained or held
    return t


def render(out: Path) -> Path:
    t = series()
    latest, prior = t.index.max(), t.loc[FIRST:2019, "down"].median()

    fig, ax = figure()
    ax.bar(t.index, t.down, color=CORAL, width=0.78)
    ax.bar(t.index, t.up, bottom=t.down, color=TEAL, width=0.78, alpha=0.40)
    ax.axhline(prior, color=INK, linewidth=1.0, linestyle=(0, (4, 3)))
    ax.annotate(f"{FIRST} to 2019 median: {prior:.0f}%", xy=(FIRST - 0.4, prior), xytext=(0, 7),
                textcoords="offset points", color=INK, fontsize=9, va="bottom")

    ax.set_ylim(0, 100); ax.set_xlim(FIRST - 1, latest + 1)
    ax.set_yticks(range(0, 101, 25))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_xticks([y for y in t.index if y % 5 == 0 and y < latest - 1] + [latest])

    for y in (COVID, latest - 1, latest):
        ax.annotate(f"{t.loc[y, 'down']:.0f}%", xy=(y, t.loc[y, "down"]), xytext=(0, 6),
                    textcoords="offset points", color=INK, fontsize=9.5, fontweight="bold", ha="center")
    frame(fig, "The weakest first seven months on record, outside the pandemic",
          "Share of U.S. counties whose labor force fell from January to July, months that normally add workers")
    word_legend(fig, [("Lost labor force", CORAL), ("Gained or held", TEAL)])

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out} ({out.stat().st_size/1e3:.0f} KB)")
    print(t.tail(4).round(1).to_string())
    print(f"{FIRST}-2019 median {prior:.1f}% | {latest} rank {(t.down > t.loc[latest,'down']).sum() + 1} of {len(t)}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=ROOT / "outputs" / "charts" / "02-january-to-july.png")
    render(ap.parse_args().out)


if __name__ == "__main__":
    main()
