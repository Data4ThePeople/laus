"""Stage C2: watch flags, the trajectory inside a band.

Positive watch: the 12-month average labor force is at least 2% above its
5-year low, that low is at least 12 months old, and the same-month 3-year
change is positive. Reads as "bottomed out and climbing".

Negative watch: the 12-month average is down at least 1% from a year
earlier, and the same-month 3-year change is -2% or worse. Reads as
"sliding, and not done". (A "near its 5-year low" test was tried first and
missed counties like Saginaw, MI in 2026, down 5% in three years but still
above the 2021 trough that sat inside the window.)

Positive watch also requires the 12-month average to be up at least 1% from
a year earlier, so a county coasting flat above an old low is not flagged.

Everything is same-month or a 12-month average, so seasonality drops out.
Flags are computed for every county-month and written to data/watch.parquet
(fips, date, flag) with flag 0 none, 1 positive, 2 negative.

Run:  python -m lfd.watch  (also prints the spot-check counties)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from lfd import DATA, PANEL_PATH

WATCH_PATH = DATA / "watch.parquet"

AVG_MONTHS = 12          # smoothing window
LOW_MONTHS = 60          # look-back for the low (5 years)
RECENT_MONTHS = 12       # "recent" for where the low sits
CHANGE_MONTHS = 36       # same-month change horizon
POS_ABOVE_LOW = 0.02     # positive: avg at least this far above the low
AVG_RISE = 0.01          # positive: avg12 up at least this vs a year ago
AVG_FALL = -0.01         # negative: avg12 down at least this vs a year ago
POS_CHANGE = 0.0         # positive: 3-year change above this
NEG_CHANGE = -0.02       # negative: 3-year change at or below this

NONE, POSITIVE, NEGATIVE = 0, 1, 2
FLAG_LABEL = {NONE: "", POSITIVE: "positive watch", NEGATIVE: "negative watch"}


def components(panel: pd.DataFrame) -> pd.DataFrame:
    """Per county-month: avg12, low60, low12, chg36. Panel must be sorted by
    fips, date and be one row per month (gaps as NaN rows, as ingest writes)."""
    p = panel.sort_values(["fips", "date"]).copy()
    g = p.groupby("fips", sort=False)["labor_force"]
    p["avg12"] = g.transform(lambda s: s.rolling(AVG_MONTHS, min_periods=AVG_MONTHS - 2).mean())
    ga = p.groupby("fips", sort=False)["avg12"]
    p["low60"] = ga.transform(lambda s: s.rolling(LOW_MONTHS, min_periods=LOW_MONTHS - 12).min())
    p["low12"] = ga.transform(lambda s: s.rolling(RECENT_MONTHS, min_periods=RECENT_MONTHS - 2).min())
    p["chg36"] = g.transform(lambda s: s / s.shift(CHANGE_MONTHS) - 1.0)
    p["avg_yoy"] = ga.transform(lambda s: s / s.shift(12) - 1.0)
    return p


def flag(p: pd.DataFrame) -> pd.Series:
    ok = p.avg12.notna() & p.chg36.notna() & p.avg_yoy.notna()
    ok_low = ok & p.low60.notna() & p.low12.notna()
    low_is_old = p.low12 > p.low60 * (1 + 1e-9)          # 5-year low set before the last 12 months
    pos = (ok_low & (p.avg12 >= p.low60 * (1 + POS_ABOVE_LOW)) & low_is_old
           & (p.avg_yoy >= AVG_RISE) & (p.chg36 > POS_CHANGE))
    neg = ok & (p.avg_yoy <= AVG_FALL) & (p.chg36 <= NEG_CHANGE)
    f = pd.Series(NONE, index=p.index, dtype="int8")
    f[pos] = POSITIVE
    f[neg] = NEGATIVE
    return f


def compute(panel: pd.DataFrame) -> pd.DataFrame:
    p = components(panel)
    p["flag"] = flag(p)
    return p[["fips", "area", "date", "labor_force", "avg12", "low60", "low12", "avg_yoy", "chg36", "flag"]]


SPOT = ["Erie County, PA", "Saginaw County, MI", "San Juan Municipio, PR",
        "Lucas County, OH", "Lincoln County, NE", "Genesee County, MI", "Orleans Parish, LA"]


def spot_check(w: pd.DataFrame, dates: list[str]) -> str:
    rows = w[w.area.isin(SPOT) & w.date.isin(pd.to_datetime(dates))].copy()
    rows["above_low"] = (rows.avg12 / rows.low60 - 1) * 100
    rows["chg36"] = rows.chg36 * 100
    rows["avg_yoy"] = rows.avg_yoy * 100
    rows["flag"] = rows.flag.map(FLAG_LABEL)
    rows["date"] = rows.date.dt.strftime("%Y-%m")
    cols = ["area", "date", "labor_force", "avg12", "above_low", "avg_yoy", "chg36", "flag"]
    return rows[cols].sort_values(["area", "date"]).to_string(index=False, float_format=lambda v: f"{v:,.1f}")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--panel", type=Path, default=PANEL_PATH)
    ap.add_argument("--out", type=Path, default=WATCH_PATH)
    args = ap.parse_args(argv)
    panel = pd.read_parquet(args.panel)
    w = compute(panel)
    w[["fips", "date", "flag"]].to_parquet(args.out, index=False)
    latest = w.date.max()
    print(f"wrote {args.out}: {len(w):,} rows")
    print(f"\nflags at {latest:%Y-%m}: positive {int((w[w.date == latest].flag == POSITIVE).sum())}, "
          f"negative {int((w[w.date == latest].flag == NEGATIVE).sum())}")
    print("\nspot checks:")
    print(spot_check(w, ["2025-04-01", "2026-04-01", f"{latest:%Y-%m-01}"]))


if __name__ == "__main__":
    main()
