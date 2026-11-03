"""Chart: CPS household response rate, monthly, January 2013 to the latest month.

BLS series LNU09300000 (cached by scripts/cps_quality.py in data/ces/cps_response_rate.csv).
Response rate = housing units that completed interviews / eligible housing units.

Run:  .venv/bin/python scripts/chart_cps_response.py
"""
from __future__ import annotations

import pandas as pd
from matplotlib.ticker import FuncFormatter

from lfd import DATA, ROOT
from lfd.chartstyle import BG, CORAL, GRID, INK, MUTED, figure, frame

OUT = ROOT / "outputs" / "charts" / "sep26-10-cps-response.png"


def main() -> None:
    r = pd.read_csv(DATA / "ces" / "cps_response_rate.csv", parse_dates=["date"]).sort_values("date").set_index("date").v
    r = r.reindex(pd.date_range(r.index.min(), r.index.max(), freq="MS"))
    fig, ax = figure(8.4, 5.0)
    ax.plot(r.index, r, color=CORAL, linewidth=2.0)
    first, last = r.dropna().index[0], r.dropna().index[-1]
    sep0 = pd.Timestamp(f"{first.year}-09-01")
    for d, ha, off in [(sep0, "left", (4, 8)), (last, "right", (-4, -16))]:
        ax.plot([d], [r[d]], "o", color=CORAL, markersize=5)
        ax.annotate(f"{d:%B %Y}: {r[d]:.1f}%", xy=(d, r[d]), xytext=off, textcoords="offset points", ha=ha,
                    color=INK, fontsize=9.5, fontweight="bold")
    ax.annotate("No estimate,\nOct 2025", xy=(pd.Timestamp("2025-10-01"), r["2025-09-01"]), xytext=(0, 22),
                textcoords="offset points", color=MUTED, fontsize=8, ha="center", va="bottom")
    ax.set_ylim(50, 100); ax.set_yticks(range(50, 101, 10))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    frame(fig, "Fewer households are answering the jobs survey",
          "Household response rate in the Current Population Survey, a main input to state and county\n"
          f"labor force estimates. Monthly, {first:%B %Y} to {last:%B %Y}.", top=0.78)
    fig.text(0.055, 0.035, "U.S. Bureau of Labor Statistics (CPS, series LNU09300000); Data 4 The People analysis.",
             color=MUTED, fontsize=8.5, backgroundcolor=BG)
    fig.savefig(OUT, facecolor=BG)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
