import pandas as pd
import pytest

from lfd.classify import STRUCTURAL_LOSS, categorize
from lfd.compare import compare, report


def _snap(rows):
    df = pd.DataFrame(rows, columns=["fips", "area", "labor_force", "pct_change"])
    df["category"] = categorize(df["pct_change"])
    return df


def test_compare_sets_and_counts():
    s0 = _snap([
        ("A", "Stays SL", 50_000, -0.15),
        ("B", "Leaves SL", 30_000, -0.11),
        ("C", "Enters SL", 40_000, -0.08),
        ("D", "Vanishes", 10_000, -0.20),   # SL at t0, absent at t1
        ("E", "Flat", 5_000, 0.05),
        ("F", "Small worsened", 8_000, -0.12),
    ])
    s1 = _snap([
        ("A", "Stays SL", 51_000, -0.18),
        ("B", "Leaves SL", 31_000, -0.09),
        ("C", "Enters SL", 39_000, -0.12),
        ("E", "Flat", 5_100, 0.06),
        ("F", "Small worsened", 7_900, -0.16),
        ("G", "New in universe", 9_000, -0.30),  # SL at t1, absent at t0
    ])
    c = compare(s0, s1, "t0", "t1", lf_floor=20_000)

    assert c.counts.loc[STRUCTURAL_LOSS].tolist() == [4, 4, 0]
    assert c.counts.loc["Grand total"].tolist() == [6, 6, 0]
    assert "universe mismatch" in c.universe_note

    assert list(c.new_entrants.index) == ["C"]
    assert c.new_entrants.loc["C", "category_t0"] == "At-risk Contraction (-10-0%)"
    assert list(c.dropped.index) == ["B"]
    assert c.dropped.loc["B", "landing_category"] == "At-risk Contraction (-10-0%)"
    assert list(c.missing_t1.index) == ["D"]
    assert list(c.missing_t0.index) == ["G"]
    # worsened: A and F both deepened; F is below the labor force floor
    assert list(c.worsened.index) == ["A"]
    assert c.worsened.loc["A", "delta"] == pytest.approx(-0.03)

    text = report(c)
    assert "−" in text and "Vanishes" in text and "New in universe" in text


def test_duplicate_fips_is_hard_failure():
    s = _snap([("A", "x", 1, -0.2), ("A", "y", 2, -0.2)])
    with pytest.raises(ValueError):
        compare(s, s, "t0", "t1")
