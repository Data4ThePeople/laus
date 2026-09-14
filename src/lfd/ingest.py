"""Stage A: download and cache the BLS LAUS county flat files, filter to the
civilian labor force series, join area names, and write a tidy monthly panel.

Output: data/laus_county_lf.parquet with columns
    fips (str, 5), area (str), state (str, 2), year (int16), month (int8),
    date (datetime64, first of month), labor_force (float64, NaN when BLS
    reports no value)

Run:  python -m lfd.ingest [--refresh]
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests

from lfd import PANEL_PATH, RAW

BASE_URL = "https://download.bls.gov/pub/time.series/la/"
FILES = {
    "data": "la.data.64.County",
    "area": "la.area",
    "series": "la.series",
    "measure": "la.measure",
}
LABOR_FORCE_MEASURE = "06"
COUNTY_AREA_TYPE = "F"  # la.area_type: F = "Counties and equivalents"


def _load_env() -> None:
    """Load the central D4TP .env so D4TP_CONTACT can be set there."""
    try:
        sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
        from d4tp_env import load_env  # type: ignore

        load_env()
    except Exception:
        pass


def user_agent() -> str:
    """Browser-like UA with a contact address; BLS blocks bare scripted requests."""
    _load_env()
    contact = os.environ.get("D4TP_CONTACT", "https://www.data4thepeople.com")
    return (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        f"(KHTML, like Gecko) Chrome/124.0 Safari/537.36 Data4ThePeople/lfd ({contact})"
    )


def download(name: str, refresh: bool = False, raw_dir: Path = RAW) -> Path:
    """Fetch one flat file into raw_dir. Reuses the cached copy unless refresh."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    dest = raw_dir / name
    if dest.exists() and not refresh:
        return dest
    url = BASE_URL + name
    tmp = dest.with_suffix(dest.suffix + ".part")
    headers = {"User-Agent": user_agent(), "Accept": "*/*"}
    t0 = time.time()
    with requests.get(url, headers=headers, stream=True, timeout=120) as r:
        if r.status_code == 403:
            raise RuntimeError(
                f"BLS returned 403 for {url}. The User-Agent was rejected; "
                "set D4TP_CONTACT in the central .env and retry."
            )
        r.raise_for_status()
        size = 0
        with open(tmp, "wb") as fh:
            for chunk in r.iter_content(chunk_size=1 << 20):
                fh.write(chunk)
                size += len(chunk)
    tmp.replace(dest)
    print(f"downloaded {name}: {size / 1e6:.1f} MB in {time.time() - t0:.0f}s")
    return dest


def _read_flat(path: Path, **kw) -> pd.DataFrame:
    """BLS flat files are tab separated with padded cells; strip everything."""
    df = pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False, **kw)
    df.columns = [c.strip() for c in df.columns]
    for c in df.columns:
        df[c] = df[c].str.strip()
    return df


def load_series(raw_dir: Path = RAW) -> pd.DataFrame:
    """Labor force series for counties: series_id, area_code, fips."""
    s = _read_flat(raw_dir / FILES["series"],
                   usecols=["series_id", "area_type_code", "area_code", "measure_code"])
    s = s[(s.measure_code == LABOR_FORCE_MEASURE) & (s.area_type_code == COUNTY_AREA_TYPE)]
    # County area codes look like CN0100100000000; positions 2:7 are the FIPS.
    s = s.assign(fips=s.area_code.str[2:7])
    dup = s.fips.duplicated(keep=False)
    if dup.any():
        raise ValueError(f"duplicate FIPS in la.series labor force rows:\n{s[dup]}")
    return s[["series_id", "area_code", "fips"]].reset_index(drop=True)


def load_areas(raw_dir: Path = RAW) -> pd.DataFrame:
    a = _read_flat(raw_dir / FILES["area"], usecols=["area_type_code", "area_code", "area_text"])
    a = a[a.area_type_code == COUNTY_AREA_TYPE]
    return a[["area_code", "area_text"]].rename(columns={"area_text": "area"})


def load_observations(series: pd.DataFrame, raw_dir: Path = RAW) -> pd.DataFrame:
    """All monthly labor force observations for the county series."""
    path = raw_dir / FILES["data"]
    keep = set(series.series_id)
    parts = []
    for chunk in pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False,
                             usecols=["series_id", "year", "period", "value"],
                             chunksize=2_000_000):
        chunk.columns = [c.strip() for c in chunk.columns]
        chunk["series_id"] = chunk["series_id"].str.strip()
        chunk = chunk[chunk.series_id.isin(keep)]
        parts.append(chunk)
    obs = pd.concat(parts, ignore_index=True)
    obs["period"] = obs["period"].str.strip()
    obs = obs[obs.period != "M13"]  # annual averages
    obs["month"] = obs["period"].str[1:].astype("int8")
    obs["year"] = obs["year"].str.strip().astype("int16")
    val = obs["value"].str.strip().replace({"-": None, "": None})
    obs["labor_force"] = pd.to_numeric(val, errors="coerce")
    return obs[["series_id", "year", "month", "labor_force"]]


def build_panel(raw_dir: Path = RAW) -> pd.DataFrame:
    series = load_series(raw_dir)
    areas = load_areas(raw_dir)
    obs = load_observations(series, raw_dir)
    panel = (obs.merge(series, on="series_id", how="left")
                .merge(areas, on="area_code", how="left"))
    missing = panel.area.isna()
    if missing.any():
        raise ValueError(f"{missing.sum()} observations have no area name; "
                         f"codes: {panel.loc[missing, 'area_code'].unique()[:10]}")
    panel["state"] = panel["area"].str.rsplit(", ", n=1).str[-1]
    panel["date"] = pd.to_datetime(dict(year=panel.year, month=panel.month, day=1))
    panel = panel[["fips", "area", "state", "year", "month", "date", "labor_force"]]
    panel = panel.sort_values(["fips", "date"]).reset_index(drop=True)
    dup = panel.duplicated(["fips", "date"], keep=False)
    if dup.any():
        raise ValueError(f"duplicate (fips, date) rows:\n{panel[dup].head()}")
    return panel


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", action="store_true", help="re-download even if cached")
    ap.add_argument("--out", type=Path, default=PANEL_PATH)
    args = ap.parse_args(argv)

    for name in FILES.values():
        download(name, refresh=args.refresh)
    panel = build_panel()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(args.out, index=False)
    n_fips = panel.fips.nunique()
    span = f"{panel.date.min():%Y-%m} to {panel.date.max():%Y-%m}"
    print(f"wrote {args.out}: {len(panel):,} rows, {n_fips:,} counties, {span}")
    last = panel[panel.date == panel.date.max()]
    print(f"latest month {panel.date.max():%Y-%m}: {last.labor_force.notna().sum():,} counties with a value")


if __name__ == "__main__":
    main()
