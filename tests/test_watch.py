import numpy as np
import pandas as pd

from lfd.watch import NEGATIVE, NONE, POSITIVE, compute


def _panel(fips, values, start="2000-01-01"):
    dates = pd.date_range(start, periods=len(values), freq="MS")
    return pd.DataFrame({"fips": fips, "area": fips, "date": dates, "labor_force": values})


def _last_flag(values):
    return int(compute(_panel("X", values)).flag.iloc[-1])


def test_flat_series_is_unflagged():
    assert _last_flag([10_000.0] * 120) == NONE


def test_v_shape_recovery_is_positive():
    # 5-year slide from 10,000 to 8,000, then 3 years climbing back to 9,000
    down = np.linspace(10_000, 8_000, 60)
    up = np.linspace(8_000, 9_000, 36)
    assert _last_flag(list(down) + list(up)) == POSITIVE


def test_fresh_bounce_is_not_yet_positive():
    # slide, then only 6 months of recovery: the low is too recent and the
    # 12-month average is still below where it was a year ago
    down = np.linspace(10_000, 8_000, 60)
    up = np.linspace(8_000, 8_400, 6)
    assert _last_flag(list(down) + list(up)) != POSITIVE


def test_coasting_above_an_old_low_is_unflagged():
    # fell, recovered two years ago, flat since: no momentum either way
    down = np.linspace(10_000, 8_000, 48)
    up = np.linspace(8_000, 9_000, 24)
    flat = [9_000.0] * 30
    assert _last_flag(list(down) + list(up) + flat) == NONE


def test_steady_slide_is_negative():
    assert _last_flag(list(np.linspace(10_000, 8_500, 96))) == NEGATIVE


def test_slow_drift_is_unflagged():
    # -1% over three years: within the noise band
    assert _last_flag(list(np.linspace(10_000, 9_900, 96))) == NONE


def test_gap_month_does_not_break_the_average():
    vals = list(np.linspace(10_000, 8_500, 96))
    vals[-3] = np.nan
    assert _last_flag(vals) == NEGATIVE
