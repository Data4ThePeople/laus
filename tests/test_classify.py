import numpy as np
import pandas as pd
import pytest

from lfd.classify import (BINS, DISPLAY_ORDER, LABELS, STRUCTURAL_LOSS,
                          categorize, category_counts, classify, snapshot)


@pytest.mark.parametrize("pct,label", [
    (-0.50, "Structural Loss (<-10%)"),
    (-0.1000001, "Structural Loss (<-10%)"),
    (-0.10, "At-risk Contraction (-10-0%)"),     # Lincoln County, NE case: -10.0% is not SL
    (-0.05, "At-risk Contraction (-10-0%)"),
    (-0.0000001, "At-risk Contraction (-10-0%)"),
    (0.0, "Below-trend Growth (0-10%)"),
    (0.05, "Below-trend Growth (0-10%)"),
    (0.0999999, "Below-trend Growth (0-10%)"),
    (0.10, "Keeping Pace (10-20%)"),
    (0.1999999, "Keeping Pace (10-20%)"),
    (0.20, "Superstars (20-40%)"),
    (0.3999999, "Superstars (20-40%)"),
    (0.40, "Hyper-Growth (>40%)"),
    (3.0, "Hyper-Growth (>40%)"),
])
def test_band_boundaries(pct, label):
    assert categorize(pd.Series([pct]))[0] == label


def test_constants_are_consistent():
    assert len(BINS) == len(LABELS) + 1
    assert BINS == sorted(BINS)
    assert DISPLAY_ORDER[-1] == STRUCTURAL_LOSS
    assert set(DISPLAY_ORDER) == set(LABELS)


def _panel():
    """Two counties, Jan and Feb, 2000 and 2020, plus a 2020 month with no base."""
    rows = []
    for fips, area, lf2000, lf2020 in [
        ("01001", "Autauga County, AL", (1000, 1100), (1200, 1000)),
        ("72127", "San Juan Municipio, PR", (2000, 2000), (1700, 1800)),
    ]:
        for m, (a, b) in enumerate(zip(lf2000, lf2020), start=1):
            rows.append((fips, area, 2000, m, a))
            rows.append((fips, area, 2020, m, b))
        rows.append((fips, area, 2020, 3, 999))  # no March 2000 -> dropped
    p = pd.DataFrame(rows, columns=["fips", "area", "year", "month", "labor_force"])
    p["state"] = p.area.str[-2:]
    p["date"] = pd.to_datetime(dict(year=p.year, month=p.month, day=1))
    p["year"] = p.year.astype("int16")
    p["month"] = p.month.astype("int8")
    return p


def test_classify_same_month_lag():
    cl = classify(_panel())
    assert len(cl) == 4  # 2 counties x 2 months with a base
    jan = snapshot(cl, 2020, 1).set_index("fips")
    assert jan.loc["01001", "pct_change"] == pytest.approx(0.20)
    assert jan.loc["01001", "category"] == "Superstars (20-40%)"  # 20.0% exactly: left-closed
    assert jan.loc["72127", "pct_change"] == pytest.approx(-0.15)
    assert jan.loc["72127", "category"] == STRUCTURAL_LOSS
    feb = snapshot(cl, 2020, 2).set_index("fips")
    assert feb.loc["01001", "pct_change"] == pytest.approx(1000 / 1100 - 1)
    assert feb.loc["01001", "category"] == "At-risk Contraction (-10-0%)"


def test_missing_and_zero_base_dropped():
    p = _panel()
    p.loc[(p.fips == "01001") & (p.year == 2000) & (p.month == 1), "labor_force"] = np.nan
    p.loc[(p.fips == "72127") & (p.year == 2000) & (p.month == 2), "labor_force"] = 0
    cl = classify(p)
    assert len(cl) == 2


def test_category_counts_order_and_total():
    cl = classify(_panel())
    counts = category_counts(snapshot(cl, 2020, 1))
    assert list(counts.index) == DISPLAY_ORDER + ["Grand total"]
    assert counts["Grand total"] == 2
    assert counts[STRUCTURAL_LOSS] == 1
