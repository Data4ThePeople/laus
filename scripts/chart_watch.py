"""The states where counties are sliding, and the states where they are turning up.

  --flag negative  ->  03a five states by share on negative watch, 03b a state map
  --flag positive  ->  04a five states by share on positive watch, 04b a state map

Everything recomputes from data/classified.parquet, data/watch.parquet and
data/geo.json at render time.

Run:  .venv/bin/python scripts/chart_watch.py --flag negative --state MI
      .venv/bin/python scripts/chart_watch.py --flag positive --state SC
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon

from lfd import CLASSIFIED_PATH, DATA, ROOT
from lfd.chartstyle import BG, CORAL, GRID, INK, MUTED, TEAL, figure, frame, word_legend
from lfd.watch import NEGATIVE, POSITIVE, WATCH_PATH

STATE_NAMES = {"VT": "Vermont", "MI": "Michigan", "WY": "Wyoming", "CO": "Colorado",
               "IL": "Illinois", "WV": "West Virginia", "ME": "Maine", "NC": "North Carolina",
               "SC": "South Carolina", "ND": "North Dakota", "AR": "Arkansas", "AK": "Alaska",
               "NY": "New York", "TX": "Texas", "OH": "Ohio", "VA": "Virginia",
               "NV": "Nevada", "MD": "Maryland", "OK": "Oklahoma", "IA": "Iowa",
               "MO": "Missouri", "KS": "Kansas", "NE": "Nebraska", "PR": "Puerto Rico",
               "GA": "Georgia", "KY": "Kentucky", "LA": "Louisiana", "NM": "New Mexico",
               "MS": "Mississippi", "AL": "Alabama", "TN": "Tennessee", "IN": "Indiana",
               "MN": "Minnesota", "WI": "Wisconsin", "PA": "Pennsylvania", "MA": "Massachusetts"}
NEUTRAL = "#4A4F52"


def table(month: str) -> pd.DataFrame:
    cl = pd.read_parquet(CLASSIFIED_PATH)
    w = pd.read_parquet(WATCH_PATH)
    d = f"{month}-01"
    s = cl[cl.date == d].merge(w[w.date == d][["fips", "flag"]], on="fips")
    return s


def chart_states(s: pd.DataFrame, month: str, out: Path, flag: int, state: str, top: int = 5) -> None:
    """The five states with the largest share of counties carrying this flag."""
    rising = flag == POSITIVE
    colour, other = (TEAL, CORAL) if rising else (CORAL, TEAL)
    word = "on positive watch" if rising else "on negative watch"
    opposite = "on negative watch" if rising else "on positive watch"
    g = s.groupby("state").apply(lambda d: pd.Series({
        "counties": len(d), "neg": int((d.flag == flag).sum()),
        "pos": int((d.flag == (POSITIVE if not rising else NEGATIVE)).sum()),
        "pct": 100 * (d.flag == flag).mean()}),
        include_groups=False)
    g = g[g.counties >= 10].sort_values("pct", ascending=False).head(top).iloc[::-1]

    fig, ax = figure(8.4, 4.6)
    y = range(len(g))
    bright = "#D98A62" if not rising else "#7CC4A6"
    ax.barh(list(y), g.pct, color=[colour if i != state else bright for i in g.index], height=0.62)
    ax.set_yticks(list(y)); ax.set_yticklabels([STATE_NAMES.get(i, i) for i in g.index], color=INK, fontsize=11)
    ax.set_xlim(0, 108); ax.set_xticks([]); ax.grid(False)
    for i, (code, row) in enumerate(g.iterrows()):
        ax.annotate(f"{row.pct:.0f}%", xy=(row.pct, i), xytext=(8, 0), textcoords="offset points",
                    color=INK, fontsize=11, fontweight="bold", va="center")
        ax.annotate(f"{int(row.neg)} of {int(row.counties)} counties, "
                    f"{'none' if row.pos == 0 else int(row.pos)} {opposite}",
                    xy=(1.2, i), color=BG, fontsize=9.5, va="center", fontweight="bold")
    ax.tick_params(axis="y", pad=8)
    title = ("Five states where most counties are on positive watch" if rising
             else "Five states where most counties are on negative watch")
    sub = (f"Counties on positive watch, {pd.Timestamp(f'{month}-01'):%B %Y}: labor force climbing off a low and above where it was three years ago"
           if rising else
           f"Counties on negative watch, {pd.Timestamp(f'{month}-01'):%B %Y}: labor force down from a year ago and from three years ago")
    frame(fig, title, sub, top=0.83)
    fig.subplots_adjust(left=0.20, right=0.965)
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}")
    print(g.iloc[::-1].round(1).to_string())


def chart_state_map(s: pd.DataFrame, month: str, out: Path, flag: int, state: str) -> None:
    """One state's counties, the flagged ones against everything else."""
    rising = flag == POSITIVE
    colour = TEAL if rising else CORAL
    geo = json.loads((DATA / "geo.json").read_text())
    units = geo["units"]
    flags = s.set_index("fips").flag
    names = s.set_index("fips").area
    lf = s.set_index("fips").labor_force

    fig, ax = figure(8.4, 5.6)
    patches, colours = [], []
    xs, ys = [], []
    for c in geo["counties"]:
        if c["state"] != state or c["fips"] not in flags.index:
            continue
        neg = flags[c["fips"]] == flag
        for ring in c["rings"]:
            pts = [(ring[i] / units, ring[i + 1] / units) for i in range(0, len(ring), 2)]
            patches.append(Polygon(pts, closed=True))
            colours.append(colour if neg else NEUTRAL)
            xs += [p[0] for p in pts]; ys += [p[1] for p in pts]
    ax.add_collection(PatchCollection(patches, facecolor=colours, edgecolor=BG, linewidth=0.7))
    pad = 6
    ax.set_xlim(min(xs) - pad, max(xs) + pad * 6)
    ax.set_ylim(max(ys) + pad, min(ys) - pad)     # canvas y runs downward
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    ax.spines["bottom"].set_visible(False)

    # name the largest counties that are not sliding
    fips_state = {f for f in flags.index if names[f].endswith(f", {state}")}
    keep = [f for f in fips_state if flags[f] != flag]
    offsets = [(34, 36), (48, -4), (34, -40)]
    for (dx, dy), f in zip(offsets, sorted(keep, key=lambda f: -lf[f])[:3]):
        c = next(x for x in geo["counties"] if x["fips"] == f)
        cx = (c["bbox"][0] + c["bbox"][2]) / 2 / units
        cy = (c["bbox"][1] + c["bbox"][3]) / 2 / units
        ax.annotate(names[f].rsplit(" County", 1)[0].replace(f", {state}", ""), xy=(cx, cy), xytext=(dx, dy),
                    textcoords="offset points", color=INK, fontsize=9, fontweight="bold",
                    arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.9, shrinkA=0, shrinkB=2))

    fl = flags[list(fips_state)]
    n_flag, n_all = int((fl == flag).sum()), len(fl)
    n_other = int((fl == (NEGATIVE if rising else POSITIVE)).sum())
    name = STATE_NAMES.get(state, state)
    verb = "are turning back up" if rising else "are losing labor force"
    other_word = "on negative watch" if rising else "on positive watch"
    frame(fig, f"{name}: {n_flag} of {n_all} counties {verb}",
          f"Counties on {'positive' if rising else 'negative'} watch, {pd.Timestamp(f'{month}-01'):%B %Y}. "
          f"{'No ' + name + ' county is' if n_other == 0 else str(n_other) + ' are'} {other_word}.", top=0.86)
    word_legend(fig, [(("Positive watch" if rising else "Negative watch"), colour),
                      ("Not flagged", MUTED)], y=0.80)
    fig.subplots_adjust(left=0.03, right=0.97, bottom=0.08)
    fig.savefig(out, facecolor=BG)
    print(f"wrote {out}: {n_flag} of {n_all} on {'positive' if rising else 'negative'} watch, {n_other} {other_word}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--month", default="2026-07")
    ap.add_argument("--flag", choices=["negative", "positive"], default="negative")
    ap.add_argument("--state", default=None, help="the state to map; defaults to MI or SC")
    ap.add_argument("--dir", type=Path, default=ROOT / "outputs" / "charts")
    a = ap.parse_args()
    rising = a.flag == "positive"
    flag = POSITIVE if rising else NEGATIVE
    state = a.state or ("SC" if rising else "MI")
    prefix, kind = ("04", "positive") if rising else ("03", "negative")
    s = table(a.month)
    a.dir.mkdir(parents=True, exist_ok=True)
    chart_states(s, a.month, a.dir / f"{prefix}a-{kind}-watch-states.png", flag, state)
    chart_state_map(s, a.month, a.dir / f"{prefix}b-{state.lower()}-{kind}-watch.png", flag, state)


if __name__ == "__main__":
    main()
