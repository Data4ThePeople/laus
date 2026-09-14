"""Stage C: compare two classified snapshots.

Given t0 and t1 (same calendar month, one year apart is the standard):

1. Category counts for each snapshot, delta per band, grand total.
   Universe mismatch (different row counts) is flagged, never hidden.
2. Set comparison on the Structural Loss lists, keyed on FIPS:
   - new_entrants: in SL at t1, not at t0 (sorted by labor force, desc)
   - dropped: in SL at t0, still in the t1 universe, not in SL at t1, with
     the t1 landing category
   - missing: in SL at t0 and absent from the t1 universe entirely. These
     are coverage gaps (a null base month, a null current month), reported
     separately and never counted as recoveries.
   - worsened: in SL at both, delta = pct(t1) - pct(t0), labor force above a
     floor, sorted by delta ascending

Category-count deltas and list-set deltas differ slightly because of churn
through the adjacent band and universe changes. Lead with the category count.

Run:  python -m lfd.compare 2025-04 2026-04 [--top 10] [--lf-floor 20000]
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from lfd import CLASSIFIED_PATH
from lfd.classify import DISPLAY_ORDER, STRUCTURAL_LOSS, category_counts, snapshot

KEEP = ["fips", "area", "labor_force", "pct_change", "category"]


@dataclass
class Comparison:
    t0: str
    t1: str
    counts: pd.DataFrame
    new_entrants: pd.DataFrame
    dropped: pd.DataFrame
    worsened: pd.DataFrame
    missing_t1: pd.DataFrame          # SL at t0, absent from t1 universe
    missing_t0: pd.DataFrame          # SL at t1, absent from t0 universe
    universe_note: str = ""
    lf_floor: int = 20_000
    notes: list[str] = field(default_factory=list)


def _sl(snap: pd.DataFrame) -> pd.DataFrame:
    return snap.loc[snap.category == STRUCTURAL_LOSS, KEEP].set_index("fips")


def compare(s0: pd.DataFrame, s1: pd.DataFrame, t0: str, t1: str,
            lf_floor: int = 20_000) -> Comparison:
    """s0, s1 are snapshot frames from classify.snapshot()."""
    for s, name in ((s0, t0), (s1, t1)):
        if s.fips.duplicated().any():
            raise ValueError(f"duplicate FIPS in snapshot {name}")

    counts = pd.DataFrame({t0: category_counts(s0), t1: category_counts(s1)})
    counts["change"] = counts[t1] - counts[t0]

    u0, u1 = set(s0.fips), set(s1.fips)
    note = ""
    if u0 != u1:
        only0, only1 = sorted(u0 - u1), sorted(u1 - u0)
        note = (f"universe mismatch: {len(u0):,} counties at {t0}, {len(u1):,} at {t1}; "
                f"{len(only0)} only at {t0}, {len(only1)} only at {t1}")

    sl0, sl1 = _sl(s0), _sl(s1)
    all0 = s0.set_index("fips")
    all1 = s1.set_index("fips")

    new_idx = sl1.index.difference(sl0.index)
    new = sl1.loc[new_idx].copy()
    # where the county came from at t0 (band), if it was in the t0 universe
    new["category_t0"] = all0.reindex(new.index)["category"].astype(object)
    new["pct_change_t0"] = all0.reindex(new.index)["pct_change"]
    missing_t0 = new[new.category_t0.isna()]
    new = new[new.category_t0.notna()].sort_values("labor_force", ascending=False)

    gone_idx = sl0.index.difference(sl1.index)
    present = gone_idx.intersection(all1.index)
    absent = gone_idx.difference(all1.index)
    dropped = sl0.loc[present].join(all1.loc[present, ["category", "pct_change", "labor_force"]],
                                    rsuffix="_t1")
    dropped = dropped.rename(columns={"category": "category_t0", "pct_change": "pct_change_t0",
                                      "labor_force": "labor_force_t0",
                                      "category_t1": "landing_category"})
    dropped = dropped.sort_values("labor_force_t1", ascending=False)
    missing_t1 = sl0.loc[absent].sort_values("labor_force", ascending=False)

    both = sl0.index.intersection(sl1.index)
    wors = sl1.loc[both, ["area", "labor_force", "pct_change"]].join(
        sl0.loc[both, ["pct_change"]], rsuffix="_t0")
    wors = wors.rename(columns={"pct_change": "pct_change_t1"})
    wors["delta"] = (wors.pct_change_t1 - wors.pct_change_t0).round(12)
    wors = wors[wors.labor_force > lf_floor].sort_values("delta")

    c = Comparison(t0, t1, counts, new, dropped, wors, missing_t1, missing_t0, note, lf_floor)
    c.notes.append(f"SL count change (category table): {counts.loc[STRUCTURAL_LOSS, 'change']:+d}")
    c.notes.append(f"SL set change: +{len(new)} entered, -{len(dropped)} left, "
                   f"{len(missing_t1)} SL-at-{t0} absent at {t1}, "
                   f"{len(missing_t0)} SL-at-{t1} absent at {t0}")
    return c


def _pct(x: float) -> str:
    s = f"{x * 100:.1f}%"
    return s.replace("-", "−")


def _fmt_table(df: pd.DataFrame, cols: dict[str, str], top: int) -> str:
    out = df.head(top).reset_index(drop=True).copy()
    for c in out.columns:
        if c.startswith("pct_change") or c == "delta":
            out[c] = out[c].map(_pct)
        elif c.startswith("labor_force"):
            out[c] = out[c].map(lambda v: f"{v:,.0f}")
    out = out[list(cols)].rename(columns=cols)
    out.index = out.index + 1
    return out.to_string()


def report(c: Comparison, top: int = 10) -> str:
    lines = [f"Snapshot comparison: {c.t0} -> {c.t1}", ""]
    if c.universe_note:
        lines += ["!! " + c.universe_note, ""]
    lines += ["Category counts", c.counts.to_string(), ""]
    lines += ["\n".join(c.notes), ""]
    lines += [f"Top {top} new entrants to Structural Loss (by labor force)",
              _fmt_table(c.new_entrants, {"area": "county", "labor_force": "labor force",
                                          "pct_change_t0": f"{c.t0}", "pct_change": f"{c.t1}",
                                          "category_t0": f"band at {c.t0}"}, top), ""]
    lines += [f"Top {top} worsened inside Structural Loss (labor force > {c.lf_floor:,})",
              _fmt_table(c.worsened, {"area": "county", "labor_force": "labor force",
                                      "pct_change_t0": f"{c.t0}", "pct_change_t1": f"{c.t1}",
                                      "delta": "change (pts)"}, top), ""]
    lines += [f"Top {top} dropped out of Structural Loss (by labor force)",
              _fmt_table(c.dropped, {"area": "county", "labor_force_t1": "labor force",
                                     "pct_change_t0": f"{c.t0}", "pct_change_t1": f"{c.t1}",
                                     "landing_category": "landing band"}, top), ""]
    if len(c.missing_t1):
        lines += [f"Structural Loss at {c.t0}, absent from the {c.t1} universe (coverage gap, not recovery)",
                  _fmt_table(c.missing_t1, {"area": "county", "labor_force": f"labor force {c.t0}",
                                            "pct_change": f"{c.t0}"}, 50), ""]
    if len(c.missing_t0):
        lines += [f"Structural Loss at {c.t1}, absent from the {c.t0} universe",
                  _fmt_table(c.missing_t0, {"area": "county", "labor_force": f"labor force {c.t1}",
                                            "pct_change": f"{c.t1}"}, 50), ""]
    return "\n".join(lines)


def _ym(s: str) -> tuple[int, int]:
    y, m = s.split("-")
    return int(y), int(m)


def run(t0: str, t1: str, path: Path = CLASSIFIED_PATH, lf_floor: int = 20_000) -> Comparison:
    cl = pd.read_parquet(path)
    s0 = snapshot(cl, *_ym(t0))
    s1 = snapshot(cl, *_ym(t1))
    return compare(s0, s1, t0, t1, lf_floor)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("t0", help="YYYY-MM")
    ap.add_argument("t1", help="YYYY-MM")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--lf-floor", type=int, default=20_000)
    ap.add_argument("--classified", type=Path, default=CLASSIFIED_PATH)
    args = ap.parse_args(argv)
    if _ym(args.t0)[1] != _ym(args.t1)[1]:
        print(f"note: {args.t0} and {args.t1} are different calendar months; "
              "the comparison carries a seasonal-anchor ambiguity")
    print(report(run(args.t0, args.t1, args.classified, args.lf_floor), args.top))


if __name__ == "__main__":
    main()
