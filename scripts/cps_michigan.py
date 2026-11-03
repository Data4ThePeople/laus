"""Michigan labor force participation from CPS microdata, January to September.

Pulls the Census CPS basic monthly files for Michigan (2024 to 2026), caches
them in data/cps/mi_cps.csv, and prints participation by year, by age group,
and for prime age (25-54) in the four Detroit metro counties the CPS identifies
(Wayne, Oakland, Macomb, Livingston) and everywhere else. St. Clair and Lapeer
are not identified in the CPS files, so they fall in the second group.
Small sample: about 1,570 Michigan adults a month in 2026. Method and limits:
DATASETS.md, "Current Population Survey microdata".

Run:  .venv/bin/python scripts/cps_michigan.py [--refresh]
"""

from __future__ import annotations

import argparse
import os
import sys

import pandas as pd
import requests

sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
from d4tp_env import get_key, load_env  # type: ignore  # noqa: E402

from lfd import DATA  # noqa: E402

CACHE = DATA / "cps" / "mi_cps.csv"
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep"]
DETROIT = [163, 125, 99, 93]   # Wayne, Oakland, Macomb, Livingston; St. Clair, Lapeer not identified in CPS
W = "PWCMPWGT"                         # composite weight, used for official labor force figures


def fetch() -> pd.DataFrame:
    load_env()
    key = get_key("CENSUS_API_KEY")
    frames = []
    for y in [2024, 2025, 2026]:
        for i, m in enumerate(MONTHS, 1):
            r = requests.get(f"https://api.census.gov/data/{y}/cps/basic/{m}",
                             params={"get": f"PRTAGE,PEMLR,{W}", "for": "county:*", "in": "state:26",
                                     "key": key}, timeout=180)
            r.raise_for_status()
            j = r.json()
            frames.append(pd.DataFrame(j[1:], columns=j[0]).assign(year=y, month=i))
    d = pd.concat(frames, ignore_index=True)
    for c in ["PRTAGE", "PEMLR", W, "county"]:
        d[c] = pd.to_numeric(d[c])
    return d.drop(columns="state")


def summary(g: pd.DataFrame) -> pd.Series:
    w = g[W]
    return pd.Series({"pop_k": w.sum() / 9 / 1000, "lfpr": (w * g.lf).sum() / w.sum() * 100,
                      "people_per_month": len(g) / 9})


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    if a.refresh or not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        fetch().to_csv(CACHE, index=False)
    d = pd.read_csv(CACHE)
    d = d[(d.PRTAGE >= 16) & (d.PEMLR > 0)].copy()      # civilian 16+; PEMLR -1 = not in universe
    d["lf"] = d.PEMLR.isin([1, 2, 3, 4])                # employed or unemployed
    d["age"] = pd.cut(d.PRTAGE, [15, 24, 54, 64, 200], labels=["16-24", "25-54", "55-64", "65+"])
    d["area"] = d.county.isin(DETROIT).map({True: "Detroit 4", False: "Rest incl. St. Clair, Lapeer"})
    pd.set_option("display.width", 120)

    print("== Michigan, Jan-Sep average"); print(d.groupby("year").apply(summary).round(1))
    by_age = d.groupby(["year", "age"], observed=True).apply(summary)
    by_age["share"] = by_age.pop_k / by_age.groupby(level=0).pop_k.transform("sum") * 100
    print("== By age"); print(by_age.round(1))
    p0, p1 = by_age.loc[2025], by_age.loc[2026]
    mix = ((p1.share - p0.share) * p0.lfpr).sum() / 100
    within = (p0.share * (p1.lfpr - p0.lfpr)).sum() / 100
    print(f"== 2025 to 2026: age-mix effect {mix:+.1f} points, within-age effect {within:+.1f} points")
    print("== Prime age (25-54) by area")
    print(d[d.age == "25-54"].groupby(["area", "year"]).apply(summary).round(1))


if __name__ == "__main__":
    main()
