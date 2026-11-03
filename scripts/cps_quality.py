"""Household survey quality check: CPS response rates, and employed residents (LAUS) vs QCEW jobs by state.

1. CPS household response rate, BLS series LNU09300000 (monthly, 2013 on).
2. For each state and quarter, one-year % change in LAUS employed residents
   (not seasonally adjusted, average of the quarter's three months) minus the
   one-year % change in QCEW employment (all ownerships, all industries,
   average of the quarter's three months). QCEW is a count from unemployment
   insurance tax records, not a survey.
3. The same comparison by month, against QCEW where it exists and against
   CES payroll jobs (not seasonally adjusted) for the months QCEW does not yet
   cover; plus how closely CES has tracked QCEW. Writes
   data/ces/state_gaps_monthly.csv for scripts/chart_state_gaps.py.
Caches: data/qcew/state_total/qcew_states.csv, data/ces/laus_employed_nsa.csv,
data/ces/ces_states_nsa.csv, data/ces/cps_response_rate.csv.

Run:  .venv/bin/python scripts/cps_quality.py [--refresh]
"""
from __future__ import annotations

import argparse
import io
import os
import sys

import pandas as pd
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
from d4tp_env import load_env  # type: ignore  # noqa: E402
from employed_vs_payroll import FIPS  # noqa: E402
from tieout_september import bls  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QCEW = os.path.join(ROOT, "data", "qcew", "state_total", "qcew_states.csv")
LAUS = os.path.join(ROOT, "data", "ces", "laus_employed_nsa.csv")
RESP = os.path.join(ROOT, "data", "ces", "cps_response_rate.csv")
CES = os.path.join(ROOT, "data", "ces", "ces_states_nsa.csv")
MONTHLY = os.path.join(ROOT, "data", "ces", "state_gaps_monthly.csv")
UA = {"User-Agent": f"Data 4 The People research ({os.environ.get('D4TP_CONTACT', 'https://www.data4thepeople.org')})"}


def fetch_qcew(last=(2026, 1)) -> pd.DataFrame:
    rows = []
    for y in range(2014, last[0] + 1):
        for q in range(1, 5):
            if (y, q) > last:
                break
            r = requests.get(f"https://data.bls.gov/cew/data/api/{y}/{q}/industry/10.csv", headers=UA, timeout=180)
            r.raise_for_status()
            d = pd.read_csv(io.StringIO(r.text), dtype={"area_fips": str}, low_memory=False)
            d = d[(d.own_code == 0) & d.agglvl_code.isin([10, 50])]
            rows.append(d[["area_fips", "year", "qtr", "month1_emplvl", "month2_emplvl", "month3_emplvl"]])
            print(y, q, len(d))
    return pd.concat(rows, ignore_index=True)


def yoy(x: pd.DataFrame) -> pd.DataFrame:
    """One-year % change by calendar month; a missing month stays missing (no row shifting)."""
    x = x.reindex(pd.date_range(x.index.min(), x.index.max(), freq="MS"))
    return (x / x.shift(12) - 1) * 100


def monthly() -> pd.DataFrame:
    """Per state and month: one-year change in LAUS employed, QCEW jobs and CES jobs, all NSA."""
    la = pd.read_csv(LAUS, dtype={"id": str}, parse_dates=["date"])
    la["fips"] = la.id.str[5:7].where(la.id != "LNU02000000", "US")
    ce = pd.read_csv(CES, dtype={"id": str}, parse_dates=["date"])
    ce["fips"] = ce.id.str[3:5].where(ce.id != "CEU0000000001", "US")
    qc = pd.read_csv(QCEW, dtype={"area_fips": str})
    qc["fips"] = qc.area_fips.str[:2].where(qc.area_fips != "US000", "US")
    q = pd.concat([pd.DataFrame({"fips": qc.fips, "v": qc[f"month{m}_emplvl"],
                                 "date": pd.to_datetime(dict(year=qc.year, month=(qc.qtr - 1) * 3 + m, day=1))})
                   for m in (1, 2, 3)])
    out = []
    for name, x in [("emp", la), ("qcew", q), ("ces", ce)]:
        y = yoy(x.pivot_table(index="date", columns="fips", values="v")).stack().rename(name)
        out.append(y)
    return pd.concat(out, axis=1).rename_axis(["date", "fips"]).reset_index()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    load_env()
    if a.refresh or not os.path.exists(QCEW):
        os.makedirs(os.path.dirname(QCEW), exist_ok=True)
        fetch_qcew().to_csv(QCEW, index=False)
    if a.refresh or not os.path.exists(LAUS):
        ids = [f"LAUST{f}0000000000005" for f in FIPS] + ["LNU02000000"]
        pd.concat([bls(ids, 2012, 2026)], ignore_index=True).to_csv(LAUS, index=False)
    if a.refresh or not os.path.exists(CES):
        bls([f"SMU{f}000000000000001" for f in FIPS] + ["CEU0000000001"], 2014, 2026).to_csv(CES, index=False)
    if a.refresh or not os.path.exists(RESP):
        bls(["LNU09300000"], 2013, 2026).to_csv(RESP, index=False)

    r = pd.read_csv(RESP, parse_dates=["date"]).set_index("date").v
    print("== CPS household response rate, %: annual average and latest")
    print(r.groupby(r.index.year).mean().round(1).to_string()); print("latest", r.index[-1].date(), r.iloc[-1])

    qc = pd.read_csv(QCEW, dtype={"area_fips": str})
    qc["fips"] = qc.area_fips.str[:2].where(qc.area_fips != "US000", "US")
    qc["jobs"] = qc[["month1_emplvl", "month2_emplvl", "month3_emplvl"]].mean(axis=1)
    qc = qc.set_index(["fips", "year", "qtr"]).jobs
    la = pd.read_csv(LAUS, dtype={"id": str}, parse_dates=["date"])
    la["fips"] = la.id.str[5:7].where(la.id != "LNU02000000", "US")
    la["year"], la["qtr"] = la.date.dt.year, (la.date.dt.month - 1) // 3 + 1
    g = la.groupby(["fips", "year", "qtr"]).agg(v=("v", "mean"), n=("v", "count"))
    emp = g.v[g.n == 3]
    w = pd.DataFrame({"emp": emp, "jobs": qc}).dropna().sort_index()
    prev = w.copy()
    prev.index = prev.index.set_levels(prev.index.levels[1] + 1, level=1)   # same quarter, one year later
    for k in ["emp", "jobs"]:
        w[k + "_yoy"] = (w[k] / prev[k].reindex(w.index) - 1) * 100
    w["gap"] = w.emp_yoy - w.jobs_yoy
    w = w.dropna(subset=["gap"])
    st = w.drop("US", level=0)
    s = st.groupby(level=[1, 2]).gap.agg(median="median", n_le_2=lambda x: (x <= -2).sum(),
                                          n_abs_2=lambda x: (x.abs() >= 2).sum(), mad=lambda x: x.abs().mean())
    s["us_gap"] = w.xs("US", level=0).gap
    pd.set_option("display.width", 160); pd.set_option("display.multi_sparse", False)
    print("== By quarter: median state gap, states with gap <= -2, states with |gap| >= 2, mean |gap|, U.S. gap (points)")
    print(s.round(2).to_string())
    last = st.xs((2026, 1), level=[1, 2]).sort_values("gap")
    print("== 2026 Q1, lowest 10 states"); print(last.head(10)[["emp_yoy", "jobs_yoy", "gap"]].round(2))


    m = monthly()
    m["gap_qcew"], m["gap_ces"] = m.emp - m.qcew, m.emp - m.ces
    m["gap"] = m.gap_qcew.fillna(m.gap_ces)            # QCEW where it exists, CES after
    m["source"] = m.gap_qcew.notna().map({True: "QCEW", False: "CES"}).where(m.gap.notna())
    m.to_csv(MONTHLY, index=False)
    sm = m[m.fips != "US"]
    print("== CES minus QCEW one-year change, mean absolute difference across states (points)")
    d = (sm.ces - sm.qcew).abs().groupby(sm.date).mean().dropna()
    print(d.groupby(d.index.year).agg(["min", "max"]).round(2).to_string())
    t = sm[sm.date >= "2025-01-01"].groupby("date").agg(
        source=("source", "first"), n_le_2=("gap", lambda x: (x <= -2).sum()), mean_abs=("gap", lambda x: x.abs().mean()),
        n_le_2_ces=("gap_ces", lambda x: (x <= -2).sum()))
    print("== Monthly, states with employed residents trailing jobs by 2+ points (QCEW where available, CES after)")
    print(t.round(2).to_string())
    print("== September mean absolute gap vs CES, 2015 on")
    sep = sm[sm.date.dt.month == 9].groupby("date").gap_ces.apply(lambda x: x.abs().mean())
    print(sep.loc["2015":].round(2).to_string())
    print("== Michigan"); print(m[(m.fips == "26") & (m.date >= "2025-09-01")][["date", "emp", "qcew", "ces"]].round(2).to_string(index=False))
    print("== Sep 2026 lowest 8 (CES)")
    print(sm[sm.date == "2026-09-01"].nsmallest(8, "gap_ces")[["fips", "emp", "ces", "gap_ces"]].round(2).to_string(index=False))


if __name__ == "__main__":
    main()

