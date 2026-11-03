"""Michigan vs Ohio, outside the big metros: labor force (LAUS) and participation (CPS).

Two area definitions, applied the same way in both states:
  outside 500k+ metros  MI drops Detroit and Grand Rapids; OH drops Cleveland,
                        Columbus, Cincinnati, Dayton, Akron and Toledo
  nonmetro              counties outside every Metropolitan Statistical Area
LAUS uses county lists from the OMB 2023 delineation (data/geo_ref/omb_cbsa_2023.csv);
the CPS uses its own metro-size (GTCBSASZ) and metro-status (GTMETSTA) codes,
because it hides the county for much of the big metros. CPS: January to
September 2025 vs 2026, household-cluster bootstrap for the sampling error.

Run:  .venv/bin/python scripts/cps_mi_oh.py [--refresh]
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
from d4tp_env import get_key, load_env  # type: ignore  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "cps", "mi_oh_cps.csv")
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep"]
STATES = {"26": "Michigan", "39": "Ohio"}
BIG = {"26": ["19820", "24340"],                                       # Detroit, Grand Rapids
       "39": ["17410", "18140", "17140", "19430", "10420", "45780"]}   # Cleveland, Columbus, Cincinnati, Dayton, Akron, Toledo
W = "PWCMPWGT"


def fetch() -> pd.DataFrame:
    load_env()
    key = get_key("CENSUS_API_KEY")
    frames = []
    for st in STATES:
        for y in [2025, 2026]:
            for i, m in enumerate(MONTHS, 1):
                r = requests.get(f"https://api.census.gov/data/{y}/cps/basic/{m}",
                                 params={"get": f"HRHHID,HRHHID2,PRTAGE,PEMLR,GTCBSASZ,GTMETSTA,{W}", "for": "county:*",
                                         "in": f"state:{st}", "key": key}, timeout=180)
                r.raise_for_status()
                j = r.json()
                frames.append(pd.DataFrame(j[1:], columns=j[0]).assign(year=y, month=i))
    return pd.concat(frames, ignore_index=True)


def change(d: pd.DataFrame, reps: int = 2000) -> dict:
    """Weighted participation 2025 and 2026, and bootstrap SE of the change (households resampled)."""
    d = d.assign(wl=d[W] * d.lf)
    g = d.groupby(["hh", "year"])[[W, "wl"]].sum().unstack(fill_value=0)
    wt, lf = g[W].reindex(columns=[2025, 2026], fill_value=0).values, g["wl"].reindex(columns=[2025, 2026], fill_value=0).values

    def rate(i):
        return lf[i].sum(0) / wt[i].sum(0) * 100
    r = rate(np.arange(len(g)))
    rng = np.random.default_rng(1)
    se = np.std([np.diff(rate(rng.integers(0, len(g), len(g))))[0] for _ in range(reps)])
    c = r[1] - r[0]
    return {"2025": round(r[0], 1), "2026": round(r[1], 1), "change": round(c, 2), "se": round(se, 2),
            "z": round(c / se, 2), "z_de2": round(c / (se * np.sqrt(2)), 2),
            "people_per_month": int(round(len(d) / 18))}


def laus_side() -> pd.DataFrame:
    omb = pd.read_csv(os.path.join(ROOT, "data", "geo_ref", "omb_cbsa_2023.csv"), dtype=str)
    omb["fips"] = omb["FIPS State Code"] + omb["FIPS County Code"]
    metro = omb[omb["Metropolitan/Micropolitan Statistical Area"] == "Metropolitan Statistical Area"]
    p = pd.read_parquet(os.path.join(ROOT, "data", "laus_county_lf.parquet"))
    rows = []
    for st, name in STATES.items():
        q = p[p.state == {"26": "MI", "39": "OH"}[st]]
        big = set(metro[metro["CBSA Code"].isin(BIG[st])].fips)
        allm = set(metro.fips)
        for area, x in [("statewide", q), ("outside 500k+ metros", q[~q.fips.isin(big)]),
                        ("nonmetro", q[~q.fips.isin(allm)])]:
            g = x.groupby("date").labor_force.sum()
            row = {"state": name, "area": area, "counties": x.fips.nunique()}
            for m in [1, 4, 9]:
                row[f"{m:02d}"] = round((g[f"2026-{m:02d}-01"] / g[f"2025-{m:02d}-01"] - 1) * 100, 1)
            rows.append(row)
    return pd.DataFrame(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    pd.set_option("display.width", 160)
    print("== LAUS labor force, change from the same month of 2025 (Jan, Apr, Sep 2026), %")
    print(laus_side().to_string(index=False))
    if a.refresh or not os.path.exists(CACHE):
        fetch().to_csv(CACHE, index=False)
    d = pd.read_csv(CACHE, dtype={"HRHHID": str, "HRHHID2": str, "state": str})
    d["state"] = d.state.str.zfill(2)
    d = d[(d.PRTAGE >= 16) & (d.PEMLR > 0)].copy()
    d["lf"] = d.PEMLR.isin([1, 2, 3, 4]).astype(float)
    d["hh"] = d.state + "-" + d.HRHHID + "-" + d.HRHHID2
    rows = []
    for st, name in STATES.items():
        s = d[d.state == st]
        for area, x in [("statewide", s), ("outside 500k+ metros", s[s.GTCBSASZ.isin([0, 2, 3])]),
                        ("nonmetro", s[s.GTMETSTA == 2])]:
            for ages, y in [("16+", x), ("25-54", x[(x.PRTAGE >= 25) & (x.PRTAGE <= 54)])]:
                rows.append({"state": name, "area": area, "ages": ages, **change(y)})
    print("== CPS participation, January to September averages")
    print(pd.DataFrame(rows).to_string(index=False))
    print("z: change / household-bootstrap SE. z_de2: with an assumed design effect of 2.0.")


if __name__ == "__main__":
    main()
