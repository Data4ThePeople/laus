"""Stage B: 20-year same-month percent change in labor force and the six bands.

BINS and LABELS live here and nowhere else. Every table, map and viz derives
its bands from these constants.

pct_change = LF(t) / LF(t - 20 years, same month) - 1

Structural Loss is strictly below -10%: exactly -10.0% lands in At-risk.
Bins are left-closed, [lo, hi), so every boundary value belongs to the band
above it (-10.0% At-risk, 0.0% Below-trend, 10.0% Keeping Pace, and so on).
The spec's prose says this; its code sample (right=True) says the opposite.
The Lincoln County, NE check on real data is what settles it.

Run:  python -m lfd.classify [--snapshot YYYY-MM]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from lfd import CLASSIFIED_PATH, PANEL_PATH

WINDOW_YEARS = 20

BINS = [-float("inf"), -0.10, 0.0, 0.10, 0.20, 0.40, float("inf")]
LABELS = [
    "Structural Loss (<-10%)",
    "At-risk Contraction (-10-0%)",
    "Below-trend Growth (0-10%)",
    "Keeping Pace (10-20%)",
    "Superstars (20-40%)",
    "Hyper-Growth (>40%)",
]
STRUCTURAL_LOSS = LABELS[0]

# Top-to-bottom order for tables: best band first, Structural Loss last.
DISPLAY_ORDER = list(reversed(LABELS))


def categorize(pct_change: pd.Series) -> pd.Series:
    """Assign the band. Returns an ordered Categorical (worst to best)."""
    return pd.cut(pct_change, bins=BINS, labels=LABELS, right=False, ordered=True)


def classify(panel: pd.DataFrame, window_years: int = WINDOW_YEARS) -> pd.DataFrame:
    """Compute pct_change and category for every county-month that has a valid
    observation `window_years` earlier in the same calendar month.

    Rows where either observation is missing, or the base is not positive, are
    dropped: they have no defined 20-year change.
    """
    cur = panel[["fips", "area", "state", "year", "month", "date", "labor_force"]]
    base = (panel[["fips", "year", "month", "labor_force"]]
            .rename(columns={"labor_force": "labor_force_base"}))
    base = base.assign(year=(base.year + window_years).astype("int16"))
    out = cur.merge(base, on=["fips", "year", "month"], how="inner")
    ok = out.labor_force.notna() & out.labor_force_base.notna() & (out.labor_force_base > 0)
    out = out[ok].copy()
    # Round away float noise so a county sitting exactly on a band edge
    # (e.g. 1200/1000 - 1 = 0.19999999999999996) lands on the edge itself.
    out["pct_change"] = (out.labor_force / out.labor_force_base - 1.0).round(12)
    out["category"] = categorize(out["pct_change"])
    out = out.sort_values(["date", "fips"]).reset_index(drop=True)
    return out[["fips", "area", "state", "year", "month", "date",
                "labor_force", "labor_force_base", "pct_change", "category"]]


def snapshot(classified: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    s = classified[(classified.year == year) & (classified.month == month)]
    if s.empty:
        raise ValueError(f"no classified rows for {year}-{month:02d}")
    return s.reset_index(drop=True)


def category_counts(snap: pd.DataFrame) -> pd.Series:
    """Counts per band in display order, plus a Grand total row."""
    counts = snap.category.value_counts().reindex(DISPLAY_ORDER, fill_value=0)
    counts.loc["Grand total"] = counts.sum()
    counts.name = "counties"
    return counts


def _parse_ym(s: str) -> tuple[int, int]:
    y, m = s.split("-")
    return int(y), int(m)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--panel", type=Path, default=PANEL_PATH)
    ap.add_argument("--out", type=Path, default=CLASSIFIED_PATH)
    ap.add_argument("--snapshot", help="YYYY-MM to print category counts for (default: latest)")
    args = ap.parse_args(argv)

    panel = pd.read_parquet(args.panel)
    cl = classify(panel)
    cl.to_parquet(args.out, index=False)
    print(f"wrote {args.out}: {len(cl):,} rows, {cl.date.min():%Y-%m} to {cl.date.max():%Y-%m}")

    if args.snapshot:
        y, m = _parse_ym(args.snapshot)
    else:
        y, m = int(cl.year.max()), int(cl[cl.year == cl.year.max()].month.max())
    snap = snapshot(cl, y, m)
    print(f"\ncategory counts, {y}-{m:02d} ({len(snap):,} counties):")
    print(category_counts(snap).to_string())


if __name__ == "__main__":
    main()
