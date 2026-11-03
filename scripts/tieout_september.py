"""Tie-out for the September 2026 update: every number in the post beats and charts.

Two kinds of check:
  1. Recompute from the pipeline files, and re-derive Structural Loss straight
     from the raw county panel (not the classified file) as a check on classify.
  2. Cross-check against separately published series pulled fresh from the
     BLS and Census APIs: statewide LAUS for every state, the U.S. CPS labor
     force, the Detroit MSA LAUS series, a sample of Michigan county series,
     and one month of Census trade.

Results go to TIEOUT.md by hand, with the words checked alongside.

Run:  .venv/bin/python scripts/tieout_september.py
"""

from __future__ import annotations

import os
import sys

import pandas as pd
import requests

sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
from d4tp_env import get_key, load_env  # type: ignore  # noqa: E402

from lfd import CLASSIFIED_PATH, DATA  # noqa: E402
from lfd.classify import STRUCTURAL_LOSS  # noqa: E402

load_env()
SEP26, SEP25 = pd.Timestamp("2026-09-01"), pd.Timestamp("2025-09-01")
DETROIT = ["26087", "26093", "26099", "26125", "26147", "26163"]  # Lapeer, Livingston, Macomb, Oakland, St. Clair, Wayne
STATES = {"01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA", "08": "CO", "09": "CT", "10": "DE",
          "11": "DC", "12": "FL", "13": "GA", "15": "HI", "16": "ID", "17": "IL", "18": "IN", "19": "IA",
          "20": "KS", "21": "KY", "22": "LA", "23": "ME", "24": "MD", "25": "MA", "26": "MI", "27": "MN",
          "28": "MS", "29": "MO", "30": "MT", "31": "NE", "32": "NV", "33": "NH", "34": "NJ", "35": "NM",
          "36": "NY", "37": "NC", "38": "ND", "39": "OH", "40": "OK", "41": "OR", "42": "PA", "44": "RI",
          "45": "SC", "46": "SD", "47": "TN", "48": "TX", "49": "UT", "50": "VT", "51": "VA", "53": "WA",
          "54": "WV", "55": "WI", "56": "WY"}


def say(label, value):
    print(f"{label:<62} {value}")


def bls(series: list[str], start=2025, end=2026) -> pd.DataFrame:
    rows = []
    for i in range(0, len(series), 50):
        j = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/",
                          json={"seriesid": series[i:i + 50], "startyear": str(start), "endyear": str(end),
                                "registrationkey": get_key("BLS_API_KEY")}, timeout=120).json()
        assert j["status"] == "REQUEST_SUCCEEDED", j.get("message")
        for s in j["Results"]["series"]:
            for d in s["data"]:
                if d["period"].startswith("M") and d["period"] != "M13":
                    rows.append({"id": s["seriesID"], "date": pd.Timestamp(f'{d["year"]}-{d["period"][1:]}-01'),
                                 "v": pd.to_numeric(d["value"], errors="coerce")})
    return pd.DataFrame(rows)


def main() -> None:
    cl = pd.read_parquet(CLASSIFIED_PATH)
    cl["sl"] = cl.category.astype(str) == STRUCTURAL_LOSS
    panel = pd.read_parquet(DATA / "laus_county_lf.parquet")

    print("== 1. Structural Loss re-derived from the raw panel (not classified.parquet)")
    for d in [SEP25, SEP26]:
        now = panel[panel.date == d].set_index("fips").labor_force
        base = panel[panel.date == d - pd.DateOffset(years=20)].set_index("fips").labor_force
        both = pd.concat([now, base], axis=1, keys=["n", "b"]).dropna()
        pct = (both.n / both.b - 1) * 100
        raw_sl = int((pct < -10).sum())
        c = cl[cl.date == d]
        say(f"{d:%b %Y} SL raw / classified, universe raw / classified",
            f"{raw_sl} / {int(c.sl.sum())}, {len(both)} / {len(c)}")

    print("== 2. Beat 1: Septembers")
    s = cl[cl.date.dt.month == 9]
    g = s.groupby(s.date.dt.year).agg(n=("sl", "size"), sl=("sl", "sum"))
    g["pct"] = (g.sl / g.n * 100).round(1)
    print(g.loc[2012:].to_string())
    say("Rank of Sep 2026 among all Septembers", int(g.pct.rank(ascending=False)[2026]))
    a = cl[cl.date == SEP25].set_index("fips")
    b = cl[cl.date == SEP26].set_index("fips")
    common = a.index.intersection(b.index)
    ent = b.sl[common] & ~a.sl[common]
    left = a.sl[common] & ~b.sl[common]
    say("Common counties; entered; left; net", f"{len(common)}; {ent.sum()}; {left.sum()}; {ent.sum() - left.sum()}")
    say("SL Sep25 / Sep26 on common", f"{a.sl[common].sum()} / {b.sl[common].sum()}")
    say("In Sep26 only", sorted(b.index.difference(a.index)))
    say("In Sep25 only", sorted(a.index.difference(b.index)))

    print("== 3. Beat 2: Michigan and states")
    st = b.loc[common, "state"]
    net = (ent.astype(int) - left.astype(int)).groupby(st).sum().sort_values(ascending=False)
    say("Top 5 states by net", net.head(5).to_dict())
    mi = b.state == "MI"
    mi_c = common[st == "MI"]
    say("MI entered; left; SL now; SL then; counties",
        f"{ent[mi_c].sum()}; {left[mi_c].sum()}; {b.sl[mi].sum()}; {a.sl[a.state == 'MI'].sum()}; {mi.sum()}")

    print("== 4. Beat 3: statewide labor force, published series (BLS API, NSA)")
    ids = [f"LAUST{f}0000000000006" for f in STATES] + ["LNU01000000"]
    pub = bls(ids).pivot(index="id", columns="date", values="v")
    chg = (pub[SEP26] / pub[SEP25] * 100 - 100).round(1)
    names = {f"LAUST{f}0000000000006": ab for f, ab in STATES.items()} | {"LNU01000000": "US"}
    chg.index = chg.index.map(names)
    say("MI Sep25 -> Sep26", f"{pub.loc['LAUST260000000000006', SEP25]:,.0f} -> "
        f"{pub.loc['LAUST260000000000006', SEP26]:,.0f} ({chg['MI']:+.1f}%)")
    say("Five largest declines", chg.drop("US").sort_values().head(5).to_dict())
    say("US, OH, IL, MN, IN, WI", chg[["US", "OH", "IL", "MN", "IN", "WI"]].to_dict())
    mi_sum = panel[(panel.state == "MI") & (panel.date.isin([SEP25, SEP26]))].groupby("date").labor_force.sum()
    say("MI county sums Sep25 / Sep26", f"{mi_sum[SEP25]:,.0f} / {mi_sum[SEP26]:,.0f}")

    print("== 5. Beat 3: the 20 Michigan entrants")
    state_chg = pub.loc["LAUST260000000000006", SEP26] / pub.loc["LAUST260000000000006", SEP25] - 1
    e = b.loc[mi_c[ent[mi_c].values]]
    yoy = e.labor_force / a.loc[e.index, "labor_force"] - 1
    say("Entrants falling faster than the state", f"{int((yoy < state_chg).sum())} of {len(e)}")
    base_only = (a.loc[e.index, "labor_force"] / e.labor_force_base - 1) * 100
    say("Entrants that cross on base change alone", int((base_only < -10).sum()))
    say("Four largest entrants by LF", e.nlargest(4, "labor_force").area.tolist())

    print("== 6. Beat 4: Detroit metro vs rest of Michigan")
    for m in [1, 4, 9]:
        p = panel[(panel.state == "MI") & (panel.month == m) & (panel.year.isin([2025, 2026]))]
        grp = p.assign(det=p.fips.isin(DETROIT)).groupby(["det", "year"]).labor_force.sum().unstack()
        r = (grp[2026] / grp[2025] * 100 - 100).round(1)
        say(f"Month {m}: Detroit 6 / rest of MI change", f"{r[True]:+.1f}% / {r[False]:+.1f}%")
        if m == 9:
            say("Rest of MI Sep25 -> Sep26", f"{grp.loc[False, 2025]:,.0f} -> {grp.loc[False, 2026]:,.0f}")
            det_sum = grp.loc[True]
            msa = bls(["LAUMT261982000000006"]).pivot(index="id", columns="date", values="v").iloc[0]
            say("Detroit 6-county sum vs published MSA series, Sep25 / Sep26",
                f"{det_sum[2025]:,.0f} vs {msa[SEP25]:,.0f} / {det_sum[2026]:,.0f} vs {msa[SEP26]:,.0f}")
            say("Rest of MI counties, count", int(p[~p.fips.isin(DETROIT)].fips.nunique()))
    sp = panel[(panel.state == "MI") & (panel.date.isin([SEP25, SEP26]))].pivot(index="fips", columns="date", values="labor_force")
    say("Median MI county Sep change", f"{(sp[SEP26] / sp[SEP25] * 100 - 100).median():+.1f}%")
    sample = ["26121", "26025", "26075", "26021"]  # Muskegon, Calhoun, Jackson, Berrien
    cty = bls([f"LAUCN{f}0000000006" for f in sample]).pivot(index="id", columns="date", values="v")
    for f in sample:
        ours = sp.loc[f, [SEP25, SEP26]].tolist()
        theirs = cty.loc[f"LAUCN{f}0000000006", [SEP25, SEP26]].tolist()
        say(f"County {f} panel vs API, Sep25/Sep26", f"{ours} vs {theirs}")

    print("== 7. Beat 5: jobs vs labor force (cache vs fresh API)")
    c = pd.read_csv(DATA / "ces" / "mi_ces.csv", parse_dates=["date"]).pivot(index="date", columns="series_id", values="jobs_k")
    fresh = bls(["SMS26000000000000001", "SMS26000003000000001", "LASST260000000000006"]).pivot(
        index="date", columns="id", values="v")
    for sid in fresh.columns:
        f, k = fresh[sid], c[sid]
        scale = 1000 if sid.startswith("LA") else 1
        say(f"{sid} Sep yoy cache / fresh",
            f"{(k[SEP26] / k[SEP25] * 100 - 100):+.2f}% / {(f[SEP26] / f[SEP25] * 100 - 100):+.2f}%")
        say(f"{sid} Jan25 -> Sep26 cache / fresh",
            f"{(k[SEP26] / k['2025-01-01'] * 100 - 100):+.2f}% / {(f[SEP26] / f['2025-01-01'] * 100 - 100):+.2f}%")
        say(f"{sid} Sep26 level cache vs fresh", f"{k[SEP26] * scale:,.1f} vs {f[SEP26]:,.1f}")
        say(f"{sid} Oct 2025 present (cache)", pd.notna(k.get(pd.Timestamp('2025-10-01'))))

    print("== 8. Beat 6: Canada share (cache) and one month re-pulled")
    t = pd.read_csv(DATA / "trade" / "mi_trade.csv", parse_dates=["date"])
    y = t[(t.date >= "2026-01-01") & (t.date <= "2026-08-01")]
    sh = y.groupby(["geo", "flow", "partner"]).value_usd.sum().unstack("partner")
    say("Canada share Jan-Aug 2026", (sh.Canada / sh.World * 100).round(1).to_dict())
    say("Months in 2026", sorted(y.date.dt.month.unique().tolist()))
    key = get_key("CENSUS_API_KEY")
    for flow, field in [("exports", "ALL_VAL_MO"), ("imports", "GEN_VAL_MO")]:
        r = requests.get(f"https://api.census.gov/data/timeseries/intltrade/{flow}/statehs",
                         params={"get": field, "CTY_CODE": "1220", "STATE": "MI", "time": "2026-08", "key": key},
                         timeout=120).json()
        cached = t[(t.geo == "MI") & (t.flow == flow) & (t.partner == "Canada") & (t.date == "2026-08-01")].value_usd.iloc[0]
        say(f"MI {flow} Canada Aug 2026 cache vs API", f"{cached:,.0f} vs {float(r[1][0]):,.0f}")


if __name__ == "__main__":
    main()
