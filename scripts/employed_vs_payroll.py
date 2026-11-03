"""Employed residents (LAUS) vs payroll jobs (CES), every state, 1990 to 2026.

For each state and month: one-year % change in LAUS employed residents (SA)
minus one-year % change in CES total nonfarm payroll jobs (SA). Shows how
unusual Michigan's 2026 gap is, against its own history and other states.
Cache: data/ces/state_emp_vs_payroll.csv.

Run:  .venv/bin/python scripts/employed_vs_payroll.py [--refresh]
"""
from __future__ import annotations

import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
from d4tp_env import load_env  # type: ignore  # noqa: E402
from tieout_september import bls  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "ces", "state_emp_vs_payroll.csv")
FIPS = [f"{i:02d}" for i in [1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                            28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50,
                            51, 53, 54, 55, 56]]


def fetch() -> pd.DataFrame:
    load_env()
    ids = [f"LASST{f}0000000000005" for f in FIPS] + [f"SMS{f}000000000000001" for f in FIPS]
    frames = [bls(ids, a, b) for a, b in [(1990, 2009), (2010, 2026)]]
    return pd.concat(frames, ignore_index=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    if a.refresh or not os.path.exists(CACHE):
        fetch().to_csv(CACHE, index=False)
    d = pd.read_csv(CACHE, dtype={"id": str}, parse_dates=["date"])
    d["fips"] = d.id.str.extract(r"^(?:LASST|SMS)(\d\d)")[0]
    d["kind"] = d.id.str[:3].map({"LAS": "emp", "SMS": "jobs"})
    w = d.pivot_table(index=["fips", "date"], columns="kind", values="v").sort_index()
    for k in ["emp", "jobs"]:
        w[f"{k}_yoy"] = w.groupby(level=0)[k].pct_change(12, fill_method=None) * 100
    w["gap"] = w.emp_yoy - w.jobs_yoy
    w = w.dropna(subset=["gap"])
    pd.set_option("display.width", 160)
    sep = w.xs(pd.Timestamp("2026-09-01"), level=1).sort_values("gap")
    print("== Sep 2026, employed residents yoy minus payroll jobs yoy (points), lowest 8 and highest 3")
    print(pd.concat([sep.head(8), sep.tail(3)])[["emp_yoy", "jobs_yoy", "gap"]].round(2))
    allg = w.gap
    print(f"== All state-months 1991-2026: n={len(allg)}, share with gap <= {sep.gap.min():.1f}: "
          f"{(allg <= sep.gap.min()).mean()*100:.2f}%")
    print("== The 15 lowest gaps in any state-month, excluding 2026")
    print(w[w.index.get_level_values(1).year < 2026].gap.nsmallest(15).round(2))
    mi = w.xs("26", level=0)
    print("== Michigan, lowest gaps 1991-2025, and 2026")
    print(mi[mi.index.year < 2026].gap.nsmallest(8).round(2))
    print(mi.loc["2025-09":, ["emp_yoy", "jobs_yoy", "gap"]].round(2))


if __name__ == "__main__":
    main()
