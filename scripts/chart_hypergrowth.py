"""Takeaway 5: the hyper-growth counties that have stopped growing.

  05a   share of hyper-growth counties whose labor force is below a year earlier
  05-1..n  one labor force trend per county, for the Prismic carousel

Run:  .venv/bin/python scripts/chart_hypergrowth.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from matplotlib.ticker import FuncFormatter
from PIL import Image

from lfd import CLASSIFIED_PATH, PANEL_PATH, ROOT
from lfd.chartstyle import BG, CORAL, GRID, INK, MUTED, TEAL, figure, frame

HG = "Hyper-Growth (>40%)"
# Prismic's carousel lays its caption over the bottom of the image, so each
# county chart carries a band of empty background for that text to sit in.
CAPTION_BAND = 100
STALLING = ["37183", "37119", "08031", "51107", "04021"]      # Wake, Mecklenburg, Denver, Loudoun, Pinal
STRONG = ["05007", "45019", "48329"]                           # Benton AR, Charleston SC, Midland TX
TREND_FROM = "2016-01-01"


def load():
    cl = pd.read_parquet(CLASSIFIED_PATH)
    lf = pd.read_parquet(PANEL_PATH).pivot(index="date", columns="fips", values="labor_force")
    return cl, lf


def chart_share(cl: pd.DataFrame, lf: pd.DataFrame, out: Path) -> None:
    yoy = (lf / lf.shift(12) - 1) * 100
    cl = cl.assign(cat=cl["category"].astype(str))
    rows = []
    for d, g in cl.groupby("date"):
        hg = [f for f in g.loc[g.cat == HG, "fips"] if d in yoy.index]
        v = yoy.loc[d, hg].dropna() if hg else pd.Series(dtype=float)
        if len(v) >= 20:
            rows.append((d, float((v < 0).mean() * 100)))
    t = pd.Series(dict(rows)).sort_index()
    t = t.reindex(pd.date_range(t.index.min(), t.index.max(), freq="MS"))

    fig, ax = figure()
    ax.fill_between(t.index, 0, t.interpolate(), color=CORAL, alpha=0.16, linewidth=0)
    ax.plot(t.index, t, color=CORAL, linewidth=2.0)
    ax.set_ylim(0, 92); ax.set_yticks(range(0, 81, 20))
    ax.set_xlim(t.index.min(), t.index.max() + pd.DateOffset(months=4))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.grid(axis="y", color=GRID, linewidth=0.8)

    last_d, last_v = t.dropna().index[-1], t.dropna().iloc[-1]
    arrow = dict(arrowstyle="-", color=MUTED, linewidth=0.9, shrinkA=0, shrinkB=4)
    ax.scatter([last_d], [last_v], s=44, color=CORAL, zorder=5, edgecolor=BG, linewidth=1.5)
    ax.annotate(f"July 2026: {last_v:.0f}%", xy=(last_d, last_v), xytext=(-12, 30),
                textcoords="offset points", color=INK, fontsize=10, fontweight="bold",
                ha="right", va="bottom", arrowprops=arrow)
    for when, label in (("2020-04-01", "Pandemic: {v:.0f}%"), ("2023-07-01", "Three years ago: {v:.0f}%")):
        d = pd.Timestamp(when)
        ax.annotate(label.format(v=t[d]), xy=(d, t[d]), xytext=(10, 22), textcoords="offset points",
                    color=MUTED, fontsize=9, va="bottom", arrowprops=arrow)
    frame(fig, "Even the fastest-growing counties have stopped growing",
          "Share of hyper-growth counties whose labor force is below the same month a year earlier")
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}: July 2026 {last_v:.1f}%")


def chart_county(cl: pd.DataFrame, lf: pd.DataFrame, fips: str, out: Path) -> None:
    row = cl[(cl.date == "2026-07-01") & (cl.fips == fips)].iloc[0]
    s = lf[fips].loc[TREND_FROM:]
    now, year_ago = s.iloc[-1], s.loc["2025-07-01"]
    yoy = (now / year_ago - 1) * 100
    peak_d = s.idxmax()
    rising = yoy > 0
    colour = TEAL if rising else CORAL

    fig, ax = figure(8.0, 4.5)
    ax.plot(s.index, s, color=colour, linewidth=2.2)
    ax.axvspan(pd.Timestamp("2025-07-01"), s.index[-1], color=INK, alpha=0.07, linewidth=0)
    ax.scatter([s.index[-1]], [now], s=46, color=colour, zorder=5, edgecolor=BG, linewidth=1.5)
    if not rising:
        ax.scatter([peak_d], [s.max()], s=36, color=MUTED, zorder=4, edgecolor=BG, linewidth=1.2)
        ax.annotate(f"peak {peak_d:%b %Y}", xy=(peak_d, s.max()), xytext=(0, 12),
                    textcoords="offset points", color=MUTED, fontsize=9, ha="center")
    lo, hi = s.min(), s.max()
    span = hi - lo
    ax.set_ylim(lo - span * 0.12, hi + span * 0.24)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v/1000:,.0f}K"))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.annotate("past 12 months", xy=(pd.Timestamp("2025-12-01"), ax.get_ylim()[0]),
                xytext=(0, 8), textcoords="offset points", color=MUTED, fontsize=8.5, ha="center")

    name = row.area
    change = f"{'up' if rising else 'down'} {abs(yoy):.1f}% in the past year"
    frame(fig, name, f"Labor force, monthly. Up {row['pct_change']*100:.0f}% over 20 years, and {change}.",
          top=0.82)
    fig.savefig(out, facecolor=BG)
    im = Image.open(out).convert("RGB")
    canvas = Image.new("RGB", (im.width, im.height + CAPTION_BAND), BG)
    canvas.paste(im, (0, 0))
    canvas.save(out)
    print(f"  {name}: {yoy:+.1f}% year over year, peak {peak_d:%Y-%m}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", type=Path, default=ROOT / "outputs" / "charts")
    a = ap.parse_args()
    a.dir.mkdir(parents=True, exist_ok=True)
    cl, lf = load()
    chart_share(cl, lf, a.dir / "05a-hypergrowth-falling.png")
    names = cl.drop_duplicates("fips").set_index("fips").area
    for n, fips in enumerate(STALLING + STRONG, start=1):
        slug = names[fips].lower().replace(" county", "").replace(" parish", "").replace("/city", "")
        slug = slug.replace(", ", "-").replace(" ", "-")
        chart_county(cl, lf, fips, a.dir / f"05-{n}-{slug}.png")


if __name__ == "__main__":
    main()
