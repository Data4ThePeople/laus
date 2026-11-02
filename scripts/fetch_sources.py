"""Fetch the non-LAUS sources for the September 2026 Michigan spotlight.

Writes small CSV caches (committed, so the post rebuilds without the APIs):
    data/ces/mi_ces.csv          CES Michigan payroll jobs, monthly
    data/qcew/mi_qcew.csv        QCEW Michigan counties, selected industries
    data/trade/mi_trade.csv      Census Michigan exports and imports by partner

Method and limits for each source are in DATASETS.md.

Run:  .venv/bin/python scripts/fetch_sources.py
"""

from __future__ import annotations

import io
import os
import sys

import pandas as pd
import requests

sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
from d4tp_env import get_key, load_env  # type: ignore  # noqa: E402

from lfd import ROOT  # noqa: E402
from lfd.ingest import user_agent  # noqa: E402

load_env()

CES_SERIES = {
    "SMS26000000000000001": "mi_total_nonfarm_sa",
    "SMS26000003000000001": "mi_manufacturing_sa",
    "SMU26000003133600001": "mi_transport_equip_mfg_nsa",
    "CES0000000001": "us_total_nonfarm_sa",
    "CES3000000001": "us_manufacturing_sa",
}
# QCEW industry codes: 10 = all industries (own_code 0), the rest private (own_code 5)
QCEW_INDUSTRIES = {"10": 0, "31-33": 5, "336": 5, "3361": 5, "3362": 5, "3363": 5}
QCEW_PERIODS = [(2024, "a"), (2025, 1), (2026, 1)]
PARTNERS = {"1220": "Canada", "2010": "Mexico", "-": "World"}


def fetch_ces() -> pd.DataFrame:
    key = get_key("BLS_API_KEY")
    rows = []
    for start, end in [(2015, 2024), (2025, 2026)]:  # API caps a request at 20 years
        r = requests.post(
            "https://api.bls.gov/publicAPI/v2/timeseries/data/",
            json={"seriesid": list(CES_SERIES), "startyear": str(start),
                  "endyear": str(end), "registrationkey": key},
            timeout=120,
        )
        j = r.json()
        if j["status"] != "REQUEST_SUCCEEDED":
            raise RuntimeError(j.get("message"))
        for s in j["Results"]["series"]:
            for d in s["data"]:
                if not d["period"].startswith("M") or d["period"] == "M13":
                    continue
                val = pd.to_numeric(d["value"], errors="coerce")  # "-" = not collected
                rows.append({"series": CES_SERIES[s["seriesID"]], "series_id": s["seriesID"],
                             "date": f'{d["year"]}-{d["period"][1:]}-01', "jobs_k": val})
    df = pd.DataFrame(rows).drop_duplicates(["series_id", "date"])
    return df.sort_values(["series", "date"])


def fetch_qcew() -> pd.DataFrame:
    frames = []
    for year, qtr in QCEW_PERIODS:
        for ind, own in QCEW_INDUSTRIES.items():
            url = f"https://data.bls.gov/cew/data/api/{year}/{qtr}/industry/{ind.replace('-', '_')}.csv"
            r = requests.get(url, headers={"User-Agent": user_agent()}, timeout=120)
            r.raise_for_status()
            d = pd.read_csv(io.StringIO(r.text), dtype={"area_fips": str, "industry_code": str,
                                                          "disclosure_code": str})
            d = d[d.area_fips.str.startswith("26") & (d.own_code == own)
                  & ~d.area_fips.str.endswith("000") & ~d.area_fips.str.endswith("999")]
            emp = "annual_avg_emplvl" if qtr == "a" else "month3_emplvl"
            d = d.assign(period=f"{year}{'A' if qtr == 'a' else 'Q' + str(qtr)}",
                         employment=d[emp])
            frames.append(d[["area_fips", "period", "industry_code", "own_code",
                             "disclosure_code", "employment"]])
    out = pd.concat(frames, ignore_index=True)
    out["suppressed"] = out.disclosure_code.fillna("").str.strip().eq("N")
    out.loc[out.suppressed, "employment"] = pd.NA
    return out.drop(columns="disclosure_code")


def fetch_trade() -> pd.DataFrame:
    key = get_key("CENSUS_API_KEY")
    base = "https://api.census.gov/data/timeseries/intltrade"
    rows = []
    for flow, path, field in [("exports", "exports/statehs", "ALL_VAL_MO"),
                              ("imports", "imports/statehs", "GEN_VAL_MO")]:
        for code, name in PARTNERS.items():
            params = {"get": f"STATE,{field}", "STATE": "MI", "time": "from 2022-01", "key": key}
            if code != "-":
                params["CTY_CODE"] = code
            else:
                params["CTY_CODE"] = "-"  # all countries total
            r = requests.get(f"{base}/{path}", params=params, timeout=120)
            r.raise_for_status()
            j = r.json()
            hdr = j[0]
            for rec in j[1:]:
                d = dict(zip(hdr, rec))
                rows.append({"flow": flow, "partner": name, "date": d["time"] + "-01",
                             "value_usd": float(d[field])})
    return pd.DataFrame(rows).sort_values(["flow", "partner", "date"])


def main() -> None:
    for sub, fn, name in [("ces", fetch_ces, "mi_ces.csv"),
                          ("qcew", fetch_qcew, "mi_qcew.csv"),
                          ("trade", fetch_trade, "mi_trade.csv")]:
        out = ROOT / "data" / sub
        out.mkdir(parents=True, exist_ok=True)
        df = fn()
        df.to_csv(out / name, index=False)
        print(f"wrote data/{sub}/{name}: {len(df):,} rows")


if __name__ == "__main__":
    main()
