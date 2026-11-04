"""Chart: number of states where employed residents and job counts differ by 2+ points, monthly, 2015 on.

For each state and month: one-year % change in LAUS employed residents minus
one-year % change in jobs, both not seasonally adjusted. Jobs are QCEW (tax
records) where published and CES payroll jobs after that. Above the line:
employed residents ran 2+ points ahead of jobs. Below: they trailed by 2+.
Reads data/ces/state_gaps_monthly.csv from scripts/cps_quality.py.

Run:  .venv/bin/python scripts/chart_state_gaps.py
"""
from __future__ import annotations

import pandas as pd
from matplotlib.ticker import FuncFormatter

from lfd import DATA, ROOT
from lfd.chartstyle import BG, CORAL, GRID, INK, MUTED, TEAL, figure, frame

OUT = ROOT / "outputs" / "charts" / "sep26-11-state-gaps.png"


def main() -> None:
    m = pd.read_csv(DATA / "ces" / "state_gaps_monthly.csv", parse_dates=["date"])
    m = m[(m.fips != "US") & (m.date >= "2015-01-01")]
    t = m.groupby("date").agg(src=("source", "first"), trail=("gap", lambda x: (x <= -2).sum()),
                              ahead=("gap", lambda x: (x >= 2).sum()), n=("gap", "count"))
    t = t.reindex(pd.date_range(t.index.min(), t.index.max(), freq="MS"))
    ok = t.n > 0
    ces = (t.src == "CES") & ok
    fig, ax = figure(8.4, 5.0)
    w = 24
    ax.bar(t.index[ok], t.ahead[ok], width=w, color=TEAL + "AA")
    ax.bar(t.index[ok & ~ces], -t.trail[ok & ~ces], width=w, color=CORAL)
    ax.bar(t.index[ces], -t.trail[ces], width=w, color=CORAL + "88", edgecolor=CORAL, linewidth=0.6)
    ax.axhline(0, color=MUTED, linewidth=0.8)
    covid = pd.Timestamp("2020-02-15")   # between the February and March 2020 bars
    ax.axvline(covid, color=INK, linewidth=0.9, linestyle=(0, (3, 3)))
    ax.text(covid - pd.Timedelta(days=40), 29.5, "COVID-19\nMarch 2020", ha="right", va="top", color=INK,
            fontsize=8.5, fontweight="bold", linespacing=1.3)
    ax.text(pd.Timestamp("2015-03-01"), 24, "Employed residents ran\n2+ points ahead of jobs", color=TEAL,
            fontsize=9, fontweight="bold", va="center")
    ax.text(pd.Timestamp("2015-03-01"), -16, "Employed residents trailed\njobs by 2+ points", color=CORAL,
            fontsize=9, fontweight="bold", va="center")
    for d, v, ha in [(pd.Timestamp("2021-08-01"), t.trail["2021-08-01"], "center"),
                     (pd.Timestamp("2026-06-01"), t.trail["2026-06-01"], "right")]:
        ax.annotate(f"{d:%b %Y}: {v}", xy=(d, -v), xytext=(0, -5), textcoords="offset points", ha=ha, va="top",
                    color=INK, fontsize=8.5, fontweight="bold")
    ax.plot([pd.Timestamp("2026-04-01"), pd.Timestamp("2026-09-01")], [6.5, 6.5], color=MUTED, linewidth=0.8)
    ax.text(pd.Timestamp("2026-09-15"), 7.3, "Payroll survey", ha="right", va="bottom", color=MUTED, fontsize=8)
    ax.set_ylim(-24, 30); ax.set_yticks(range(-20, 31, 10))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{abs(v):.0f}"))
    ax.set_xlim(pd.Timestamp("2014-11-01"), pd.Timestamp("2026-12-01"))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    last = t.index[ok][-1]
    frame(fig, "Employed residents trailed jobs in as many states in June 2026\nas at the 2021 high",
          "Number of states (of 50 plus DC) where the one-year change in employed residents differs from the\n"
          "one-year change in jobs by 2 points or more. Monthly, not seasonally adjusted. Jobs from tax records\n"
          f"(QCEW) through March 2026, payroll survey (CES) April to {last:%B %Y}. No estimate Oct 2025.", top=0.68, sub_y=0.845)
    fig.text(0.055, 0.035, "U.S. Bureau of Labor Statistics (LAUS, QCEW, CES); Data 4 The People analysis.",
             color=MUTED, fontsize=8.5, backgroundcolor=BG)
    fig.savefig(OUT, facecolor=BG)
    print(f"wrote {OUT}")
    print(t.loc["2026-01-01":, ["src", "trail", "ahead"]].to_string())


if __name__ == "__main__":
    main()
