"""Charts for the Michigan spotlight in the September 2026 update.

    sep26-02-mi-county-map.png      counties that entered Structural Loss in the past year
    sep26-03-mi-labor-force-jobs.png  Michigan employed residents vs payroll jobs, indexed
    sep26-04-mi-canada-share.png    Canada's share of Michigan trade vs the U.S.
    sep26-05-mi-vs-neighbors.png    one-year labor force change, Michigan, neighbors, U.S.
    sep26-06-mi-detroit-vs-rest.png Detroit metro vs rest of Michigan, monthly, same month a year earlier
    sep26-07-mi-participation.png   labor force participation rate, Michigan, Ohio, U.S.
    sep26-08-mi-oh-outside-metros.png  Michigan vs Ohio outside metros of 500,000+, monthly, same month a year earlier

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
LAUS_CPS = "U.S. Bureau of Labor Statistics (LAUS, CPS); Data 4 The People analysis."


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
    lf = w.mi_laus_employed_sa / w.mi_laus_employed_sa[base] * 100 - 100   # residents with a job
    jobs = w.mi_total_nonfarm_sa / w.mi_total_nonfarm_sa[base] * 100 - 100
    fig, ax = figure(8.4, 5.0)
    ax.axhline(0, color=GRID, linewidth=1.0)
    ax.plot(jobs.index, jobs, color=SKY, linewidth=2.2, solid_capstyle="round")
    ax.plot(lf.index, lf, color=CORAL, linewidth=2.2, solid_capstyle="round")
    last = lf.dropna().index[-1]
    for s, col, label in [(jobs, SKY, "Payroll jobs"), (lf, CORAL, "Employed residents")]:
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
    frame(fig, "Michigan's two measures of work split apart in 2026",
          f"Change since January 2025, seasonally adjusted, through {last:%B %Y}. Employed residents counts\n"
          "people living in Michigan who have a job. Payroll jobs count nonfarm jobs at Michigan employers.",
          top=0.79)
    _restamp_source(fig, LAUS_CES)
    fig.subplots_adjust(right=0.89)
    out = OUT / "sep26-03-mi-labor-force-jobs.png"
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}: through {last:%Y-%m}, employed residents {lf[last]:+.2f}%, jobs {jobs[last]:+.2f}%")
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
    frame(fig, "Canada is a far bigger share of Michigan's trade than the nation's",
          f"Canada's share of all goods exports and imports, January to {last:%B %Y}, in dollars", top=0.80)
    _restamp_source(fig, TRADE)
    fig.subplots_adjust(left=0.2)
    out = OUT / "sep26-04-mi-canada-share.png"
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}: Jan-{last:%b %Y}"); print(share.round(1).to_string())
    return out


def _ces() -> pd.DataFrame:
    c = pd.read_csv(DATA / "ces" / "mi_ces.csv", parse_dates=["date"])
    return c.pivot(index="date", columns="series", values="jobs_k")


def neighbors(month: str) -> Path:
    d = pd.Timestamp(f"{month}-01")
    prev = d - pd.DateOffset(years=1)
    w = _ces()
    rows = [("Michigan", "mi_laus_labor_force_nsa"), ("Ohio", "oh_laus_labor_force_nsa"),
            ("Illinois", "il_laus_labor_force_nsa"), ("Minnesota", "mn_laus_labor_force_nsa"),
            ("Indiana", "in_laus_labor_force_nsa"), ("Wisconsin", "wi_laus_labor_force_nsa"),
            ("United States", "us_cps_labor_force_nsa")]
    chg = pd.Series({name: (w.loc[d, col] / w.loc[prev, col] - 1) * 100 for name, col in rows})
    order = ["Michigan", "United States"] + chg.drop(["Michigan", "United States"]).sort_values().index.tolist()
    chg = chg[order]
    fig, ax = figure(8.4, 5.0)
    ys = range(len(chg))
    cols = [CORAL if n == "Michigan" else (MUTED if n == "United States" else NEUTRAL) for n in chg.index]
    ax.barh(list(ys), chg.values, color=cols, height=0.62)
    ax.axvline(0, color=MUTED, linewidth=1.0)
    for y, (n, v) in zip(ys, chg.items()):
        ax.annotate(f"{v:+.1f}%", xy=(v, y), xytext=(-8 if v < 0 else 8, 0), textcoords="offset points",
                    ha="right" if v < 0 else "left", va="center", fontsize=10,
                    color=INK, fontweight="bold" if n == "Michigan" else "normal")
    ax.set_yticks(list(ys)); ax.set_yticklabels(chg.index, color=MUTED, fontsize=10)
    ax.invert_yaxis(); ax.set_xticks([]); ax.grid(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(chg.min() * 1.35, max(chg.max(), 0) * 1.6 + 0.5)
    frame(fig, "Michigan's labor force fell more than any other state's",
          f"Change in civilian labor force, {prev:%B %Y} to {d:%B %Y}, not seasonally adjusted.\n"
          "Michigan and its neighbors, with the U.S. total.", top=0.79)
    _restamp_source(fig, LAUS_CPS)
    fig.subplots_adjust(left=0.2)
    out = OUT / "sep26-05-mi-vs-neighbors.png"
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}"); print(chg.round(2).to_string())
    return out


DETROIT = ["26087", "26093", "26099", "26125", "26147", "26163"]


def detroit_vs_rest(month: str) -> Path:
    d = pd.Timestamp(f"{month}-01")
    p = pd.read_parquet(DATA / "laus_county_lf.parquet")
    p = p[p.state == "MI"].assign(area=lambda x: x.fips.isin(DETROIT).map({True: "det", False: "rest"}))
    g = p.groupby(["area", "date"]).labor_force.sum().unstack("area")
    g = g.reindex(pd.date_range(g.index.min(), g.index.max(), freq="MS"))  # full months, so shift(12) is a year
    yoy = (g / g.shift(12) - 1) * 100       # same month a year earlier
    yoy = yoy.loc[f"{d.year}-01-01":d]
    fig, ax = figure(8.4, 5.0)
    ax.axhline(0, color=GRID, linewidth=1.0)
    for col, colour, label in [("det", SKY, "Detroit metro (6 counties)"), ("rest", CORAL, "Rest of Michigan (77 counties)")]:
        s = yoy[col]
        ax.plot(s.index, s, color=colour, linewidth=2.2, marker="o", markersize=4)
        v = s.iloc[-1]
        ax.annotate(f"{label}\n{v:+.1f}%", xy=(s.index[-1], v), xytext=(10, 0), textcoords="offset points",
                    color=colour, fontsize=9.5, fontweight="bold", va="center", linespacing=1.4)
    ax.set_xlim(yoy.index.min() - pd.DateOffset(days=12), d + pd.DateOffset(months=4))
    ax.set_xticks(yoy.index); ax.set_xticklabels([f"{t:%b}" for t in yoy.index])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:+.0f}%" if v else "0%"))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    frame(fig, "Michigan's labor force drop is outside the Detroit metro",
          f"Change in civilian labor force from the same month a year earlier, {d.year}, not seasonally adjusted.\n"
          "BLS estimates the Detroit metro and the rest of Michigan as separate areas.", top=0.79)
    fig.subplots_adjust(right=0.78)
    out = OUT / "sep26-06-mi-detroit-vs-rest.png"
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}"); print(yoy.round(2).to_string())
    return out


def participation(month: str) -> Path:
    d = pd.Timestamp(f"{month}-01")
    w = _ces().loc["2024-01-01":d]
    fig, ax = figure(8.4, 5.0)
    lines = [("us_cps_lfpr_sa", MUTED, "United States"), ("oh_laus_lfpr_sa", SKY, "Ohio"),
             ("mi_laus_lfpr_sa", CORAL, "Michigan")]
    for col, colour, label in lines:
        s = w[col]
        ax.plot(s.index, s, color=colour, linewidth=2.2, solid_capstyle="round")
        last = s.dropna().index[-1]
        ax.scatter([last], [s[last]], s=36, color=colour, zorder=5, edgecolor=BG, linewidth=1.3)
        ax.annotate(f"{label} {s[last]:.1f}%", xy=(last, s[last]), xytext=(10, 0), textcoords="offset points",
                    color=colour, fontsize=9.5, fontweight="bold", va="center")
    gap = w.mi_laus_lfpr_sa[w.mi_laus_lfpr_sa.isna()].index
    if len(gap):
        g0 = gap[0]
        ax.annotate(f"No estimate,\n{g0:%B %Y}", xy=(g0, w.mi_laus_lfpr_sa.interpolate()[g0]),
                    xytext=(0, -40), textcoords="offset points", color=MUTED, fontsize=8.5, ha="center",
                    va="top", linespacing=1.4, arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.9))
    ax.set_xlim(w.index.min(), d + pd.DateOffset(months=6))
    yrs = [pd.Timestamp(f"{y}-01-01") for y in range(2024, d.year + 1)]
    ax.set_xticks(yrs); ax.set_xticklabels([f"Jan {t:%Y}" for t in yrs])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    frame(fig, "Participation fell faster in Michigan than in Ohio or the U.S.",
          f"Share of adults working or looking for work, seasonally adjusted, January 2024 to {d:%B %Y}.",
          top=0.81)
    _restamp_source(fig, LAUS_CPS)
    fig.subplots_adjust(right=0.84)
    out = OUT / "sep26-07-mi-participation.png"
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}"); print(w[[c for c, _, _ in lines]].loc[pd.to_datetime(["2024-01-01", "2025-09-01", d])].to_string())
    return out


MODEL_METROS = {"MI": ("19820", "Detroit"), "OH": ("17410", "Cleveland")}   # BLS substate model areas


def balance_of_state(month: str) -> Path:
    """Michigan outside the Detroit metro vs Ohio outside the Cleveland metro: the BLS balance-of-state areas."""
    d = pd.Timestamp(f"{month}-01")
    omb = pd.read_csv(DATA / "geo_ref" / "omb_cbsa_2023.csv", dtype=str)
    omb["fips"] = omb["FIPS State Code"] + omb["FIPS County Code"]
    p = pd.read_parquet(DATA / "laus_county_lf.parquet")
    fig, ax = figure(8.4, 5.0)
    ax.axhline(0, color=GRID, linewidth=1.0)
    res = {}
    for st, colour, name in [("OH", SKY, "Ohio"), ("MI", CORAL, "Michigan")]:
        code, metro = MODEL_METROS[st]
        q = p[(p.state == st) & ~p.fips.isin(set(omb[omb["CBSA Code"] == code].fips))]
        g = q.groupby("date").labor_force.sum()
        g = g.reindex(pd.date_range(g.index.min(), g.index.max(), freq="MS"))
        yoy = ((g / g.shift(12) - 1) * 100).loc[f"{d.year}-01-01":d]
        res[name] = yoy
        ax.plot(yoy.index, yoy, color=colour, linewidth=2.2, marker="o", markersize=4)
        ax.annotate(f"{name} outside\n{metro}, {q.fips.nunique()} counties\n{yoy.iloc[-1]:+.1f}%",
                    xy=(yoy.index[-1], yoy.iloc[-1]), xytext=(10, 0), textcoords="offset points", color=colour,
                    fontsize=9.5, fontweight="bold", va="center", linespacing=1.4)
    idx = res["Michigan"].index
    ax.set_xlim(idx.min() - pd.DateOffset(days=12), d + pd.DateOffset(months=4))
    ax.set_xticks(idx); ax.set_xticklabels([f"{t:%b}" for t in idx])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:+.0f}%" if v else "0%"))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_ylim(-10, 0.6)
    frame(fig, "The rest of Michigan fell far more than the rest of Ohio",
          f"Change in civilian labor force from the same month a year earlier, {d.year}, not seasonally adjusted.\n"
          "Counties outside the Detroit and Cleveland metro areas, which BLS estimates separately.", top=0.77)
    _restamp_source(fig, "U.S. Bureau of Labor Statistics (LAUS); OMB 2023 metro areas; Data 4 The People analysis.")
    fig.subplots_adjust(right=0.8)
    out = OUT / "sep26-08-mi-oh-balance-of-state.png"
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}"); print(pd.DataFrame(res).round(2).to_string())
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--month", default="2026-09")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    county_map(a.month)
    labor_force_vs_jobs(a.month)
    canada_share()
    neighbors(a.month)
    detroit_vs_rest(a.month)
    participation(a.month)
    balance_of_state(a.month)


if __name__ == "__main__":
    main()
