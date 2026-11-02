"""Charts for the Michigan spotlight in the September 2026 update.

    sep26-02-mi-county-map.png      counties that entered Structural Loss in the past year
    sep26-03-mi-labor-force-jobs.png  Michigan labor force vs payroll jobs, indexed
    sep26-04-mi-canada-share.png    Canada's share of Michigan trade vs the U.S.

Every value is recomputed at render time from data/classified.parquet,
data/ces/mi_ces.csv and data/trade/mi_trade.csv. Sources and limits: DATASETS.md.

Run:  .venv/bin/python scripts/chart_michigan.py [--month 2026-09]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from matplotlib.ticker import FuncFormatter

from lfd import CLASSIFIED_PATH, DATA, ROOT
from lfd.chartstyle import BG, CORAL, CREDIT, GRID, INK, MUTED, TEAL, figure, frame, word_legend
from lfd.classify import STRUCTURAL_LOSS

OUT = ROOT / "outputs" / "charts"
NEUTRAL = "#4A4F52"
BRIGHT = "#E39A72"          # entered in the past year: the coral, lightened
DEEP = "#7E4A36"            # already in Structural Loss: the coral, darkened
DEEP_TEXT = "#A86F59"       # legend word for DEEP, readable on the dark background
SKY = "#7FA7C9"             # payroll jobs line, distinct from coral and teal
LAUS_CES = "U.S. Bureau of Labor Statistics (LAUS, CES); Data 4 The People analysis."
TRADE = "U.S. Census Bureau, International Trade; Data 4 The People analysis."


def _restamp_source(fig, text: str) -> None:
    """frame() writes the LAUS-only source line; swap it for this chart's sources."""
    for t in fig.texts:
        if t.get_text().startswith("U.S. Bureau of Labor Statistics (LAUS);"):
            t.set_text(text)


def county_map(month: str) -> Path:
    d = pd.Timestamp(f"{month}-01")
    prev = d - pd.DateOffset(years=1)
    cl = pd.read_parquet(CLASSIFIED_PATH)
    mi = cl[cl.state == "MI"]
    now = mi[mi.date == d].set_index("fips")
    then = mi[mi.date == prev].set_index("fips")
    sl_now = now.category.astype(str) == STRUCTURAL_LOSS
    sl_then = (then.category.astype(str) == STRUCTURAL_LOSS).reindex(now.index)
    status = pd.Series("not", index=now.index)
    status[sl_now & (sl_then == True)] = "already"   # noqa: E712  (NaN-safe)
    status[sl_now & (sl_then != True)] = "entered"   # noqa: E712
    n_entered = int((status == "entered").sum())
    n_left = int((~sl_now & (sl_then == True)).sum())  # noqa: E712
    n_sl, n_all = int(sl_now.sum()), len(now)

    geo = json.loads((DATA / "geo.json").read_text())
    units = geo["units"]
    colour = {"entered": BRIGHT, "already": DEEP, "not": NEUTRAL}
    fig, ax = figure(8.4, 6.4)
    patches, colours, xs, ys = [], [], [], []
    for c in geo["counties"]:
        if c["fips"] not in status.index:
            continue
        for ring in c["rings"]:
            pts = [(ring[i] / units, ring[i + 1] / units) for i in range(0, len(ring), 2)]
            patches.append(Polygon(pts, closed=True))
            colours.append(colour[status[c["fips"]]])
            xs += [p[0] for p in pts]; ys += [p[1] for p in pts]
    ax.add_collection(PatchCollection(patches, facecolor=colours, edgecolor=BG, linewidth=0.7))
    pad = 6
    ax.set_xlim(min(xs) - pad * 8, max(xs) + pad * 8)
    ax.set_ylim(max(ys) + pad * 3, min(ys) - pad)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    ax.spines["bottom"].set_visible(False)

    # label the largest counties that entered, leader lines out to open space
    names = now.area.str.replace(" County, MI", "", regex=False)
    offsets = {"Muskegon": (-90, 10), "Berrien": (-80, -10), "Calhoun": (-40, -48), "Jackson": (50, -50)}
    for f in now[status == "entered"].nlargest(4, "labor_force").index:
        c = next(x for x in geo["counties"] if x["fips"] == f)
        ring = max(c["rings"], key=len)
        cx = sum(ring[0::2]) / (len(ring) / 2) / units
        cy = sum(ring[1::2]) / (len(ring) / 2) / units
        ax.annotate(names[f], xy=(cx, cy), xytext=offsets.get(names[f], (60, 0)),
                    textcoords="offset points", color=INK, fontsize=9, fontweight="bold",
                    ha="center", va="center",
                    arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.9, shrinkA=4, shrinkB=0))

    frame(fig, f"Michigan: {n_entered} counties fell into structural loss in a year",
          f"Michigan counties by labor force status, {d:%B %Y}. {n_sl} of {n_all} are now in "
          f"structural loss, up from {n_sl - n_entered + n_left}.", top=0.86)
    word_legend(fig, [(f"Entered since {prev:%B %Y} ({n_entered})", BRIGHT),
                      (f"Already in structural loss ({n_sl - n_entered})", DEEP_TEXT),
                      (f"Not in structural loss ({n_all - n_sl})", MUTED)], y=0.80)
    fig.subplots_adjust(left=0.03, right=0.97, top=0.78, bottom=0.07)
    out = OUT / "sep26-02-mi-county-map.png"
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}: entered {n_entered}, left {n_left}, SL {n_sl} of {n_all}")
    return out


def labor_force_vs_jobs(month: str) -> Path:
    c = pd.read_csv(DATA / "ces" / "mi_ces.csv", parse_dates=["date"])
    w = c.pivot(index="date", columns="series", values="jobs_k").loc["2024-01-01":f"{month}-01"]
    base = pd.Timestamp("2025-01-01")
    lf = w.mi_laus_labor_force_sa / w.mi_laus_labor_force_sa[base] * 100 - 100
    jobs = w.mi_total_nonfarm_sa / w.mi_total_nonfarm_sa[base] * 100 - 100
    fig, ax = figure(8.4, 5.0)
    ax.axhline(0, color=GRID, linewidth=1.0)
    ax.plot(jobs.index, jobs, color=SKY, linewidth=2.2, solid_capstyle="round")
    ax.plot(lf.index, lf, color=CORAL, linewidth=2.2, solid_capstyle="round")
    last = lf.dropna().index[-1]
    for s, col, label in [(jobs, SKY, "Payroll jobs"), (lf, CORAL, "Labor force")]:
        v = s[last]
        ax.scatter([last], [v], s=40, color=col, zorder=5, edgecolor=BG, linewidth=1.4)
        ax.annotate(f"{label}\n{v:+.1f}%", xy=(last, v), xytext=(10, 0), textcoords="offset points",
                    color=col, fontsize=9.5, fontweight="bold", va="center", linespacing=1.4)
    ax.set_xlim(lf.index.min(), last + pd.DateOffset(months=6))
    yrs = [pd.Timestamp(f"{y}-01-01") for y in range(lf.index.min().year, last.year + 1)]
    ax.set_xticks(yrs); ax.set_xticklabels([f"Jan {t:%Y}" for t in yrs])
    gap = lf[lf.isna()].index
    if len(gap):
        g0 = gap[0]
        ax.annotate(f"No estimate,\n{g0:%B %Y}", xy=(g0, lf.interpolate()[g0]), xytext=(0, -38),
                    textcoords="offset points", color=MUTED, fontsize=8.5, ha="center", va="top",
                    linespacing=1.4, arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.9))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:+.0f}%" if v else "0%"))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    frame(fig, "Michigan's labor force is falling. Its job count is not.",
          f"Change since January 2025, seasonally adjusted, through {last:%B %Y}.\nLabor force counts "
          "residents working or looking for work. Payroll jobs count positions at Michigan employers.",
          top=0.79)
    _restamp_source(fig, LAUS_CES)
    fig.subplots_adjust(right=0.93)
    out = OUT / "sep26-03-mi-labor-force-jobs.png"
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}: through {last:%Y-%m}, labor force {lf[last]:+.2f}%, jobs {jobs[last]:+.2f}%")
    return out


def canada_share() -> Path:
    t = pd.read_csv(DATA / "trade" / "mi_trade.csv", parse_dates=["date"])
    last = t.date.max()
    yr = t[t.date.dt.year == last.year]
    s = yr.groupby(["geo", "flow", "partner"]).value_usd.sum().unstack("partner")
    share = (s.Canada / s.World * 100).unstack("geo")   # rows: flow, cols: MI, US
    fig, ax = figure(8.4, 4.6)
    rows = [("exports", "Exports to Canada"), ("imports", "Imports from Canada")]
    y = 0
    ticks, labels = [], []
    for flow, label in rows:
        for geo, col, name in [("MI", CORAL, "Michigan"), ("US", NEUTRAL, "United States")]:
            v = share.loc[flow, geo]
            ax.barh(y, v, color=col, height=0.62)
            ax.annotate(f"{v:.0f}%", xy=(v, y), xytext=(8, 0), textcoords="offset points",
                        color=INK, fontsize=10.5, fontweight="bold", va="center")
            ticks.append(y); labels.append(name)
            y += 1
        ax.annotate(label, xy=(0, y - 2.6), color=INK, fontsize=10.5, fontweight="bold",
                    annotation_clip=False, xytext=(0, 0), textcoords="offset points")
        y += 1.0
    ax.set_yticks(ticks); ax.set_yticklabels(labels, color=MUTED, fontsize=10)
    ax.invert_yaxis(); ax.set_xticks([]); ax.grid(False)
    ax.set_xlim(0, share.values.max() * 1.25)
    frame(fig, "Michigan trades with Canada far more than the nation does",
          f"Canada's share of all goods exports and imports, January to {last:%B %Y}, in dollars", top=0.80)
    _restamp_source(fig, TRADE)
    fig.subplots_adjust(left=0.2)
    out = OUT / "sep26-04-mi-canada-share.png"
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}: Jan-{last:%b %Y}"); print(share.round(1).to_string())
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--month", default="2026-09")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    county_map(a.month)
    labor_force_vs_jobs(a.month)
    canada_share()


if __name__ == "__main__":
    main()
