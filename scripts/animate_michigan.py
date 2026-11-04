"""Animated GIF of the Michigan two-measures chart (sep26-03) for social posts.

Both lines draw in from January 2024 to the latest month over about 8 seconds,
then the finished chart holds for about 5. Same data, colors, title and labels
as labor_force_vs_jobs() in chart_michigan.py. Labels only ever show a
published monthly value, never an in-between one. Modeled on
Sulfur/scripts/animate.py.

    .venv/bin/python scripts/animate_michigan.py [month] [seconds] [hold_seconds]
"""

from __future__ import annotations

import sys

import matplotlib.dates as mdates
import pandas as pd
from matplotlib.ticker import FuncFormatter
from PIL import Image

from lfd import DATA, ROOT
from lfd.chartstyle import BG, CORAL, GRID, INK, MUTED, figure, frame

sys.path.insert(0, str(ROOT / "scripts"))
from chart_michigan import LAUS_CES, SKY, _restamp_source  # noqa: E402

MONTH = sys.argv[1] if len(sys.argv) > 1 else "2026-09"
SECONDS = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
HOLD = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
FRAME_MS = 80
WIDTH_PX = 1200
OUT = ROOT / "posts" / "labor-force-september-2026" / "social"


def data():
    c = pd.read_csv(DATA / "ces" / "mi_ces.csv", parse_dates=["date"])
    w = c.pivot(index="date", columns="series", values="jobs_k").loc["2024-01-01":f"{MONTH}-01"]
    base = pd.Timestamp("2025-01-01")
    lf = w.mi_laus_employed_sa / w.mi_laus_employed_sa[base] * 100 - 100
    jobs = w.mi_total_nonfarm_sa / w.mi_total_nonfarm_sa[base] * 100 - 100
    return lf, jobs


def main() -> None:
    lf, jobs = data()
    last = lf.dropna().index[-1]
    fig, ax = figure(8.4, 5.0)
    fig.set_dpi(WIDTH_PX / fig.get_figwidth())
    ax.axhline(0, color=GRID, linewidth=1.0)

    # Fix the axes from the finished chart, exactly as the static PNG sets them.
    probe = [ax.plot(s.index, s, linewidth=2.2)[0] for s in (jobs, lf)]
    ylim = ax.get_ylim()
    for p in probe:
        p.remove()
    ax.set_ylim(ylim)
    ax.set_xlim(lf.index.min(), last + pd.DateOffset(months=6))
    yrs = [pd.Timestamp(f"{y}-01-01") for y in range(lf.index.min().year, last.year + 1)]
    ax.set_xticks(yrs); ax.set_xticklabels([f"Jan {t:%Y}" for t in yrs])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:+.0f}%" if v else "0%"))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    frame(fig, "Michigan's two measures of work split apart in 2026",
          f"Change since January 2025, seasonally adjusted, through {last:%B %Y}. Employed residents counts\n"
          "people living in Michigan who have a job. Payroll jobs count nonfarm jobs at Michigan employers.",
          top=0.79)
    _restamp_source(fig, LAUS_CES)
    fig.subplots_adjust(right=0.89)

    series = [(jobs, SKY, "Payroll jobs"), (lf, CORAL, "Employed residents")]
    lines = [ax.plot([], [], color=col, linewidth=2.2, solid_capstyle="round")[0] for _, col, _ in series]
    dots = [ax.scatter([], [], s=40, color=col, zorder=5, edgecolor=BG, linewidth=1.4) for _, col, _ in series]
    labels = [ax.annotate("", xy=(lf.index[0], 0), xytext=(10, 0), textcoords="offset points", color=col,
                          fontsize=9.5, fontweight="bold", va="center", linespacing=1.4, annotation_clip=False)
              for _, col, _ in series]
    gap = lf[lf.isna()].index
    gap_note = None
    if len(gap):
        g0 = gap[0]
        gap_note = ax.annotate(f"No estimate,\n{g0:%B %Y}", xy=(g0, lf.interpolate()[g0]), xytext=(0, -38),
                               textcoords="offset points", color=MUTED, fontsize=8.5, ha="center", va="top",
                               linespacing=1.4, arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.9))
        gap_note.set_visible(False)
    clock = ax.text(0.02, 0.08, "", transform=ax.transAxes, color=INK, fontsize=14, fontweight="bold")

    xnum = lambda t: t.value / 1e9  # noqa: E731  seconds, for interpolation only
    t0, t1 = lf.index[0], last

    def draw(cursor: pd.Timestamp, final: bool = False) -> Image.Image:
        for (s, _, name), ln, dot, lab in zip(series, lines, dots, labels):
            seen = s[s.index <= cursor]
            xs, ys = list(seen.index), list(seen.values)
            nxt = s[s.index > cursor]
            # Extend to the cursor only between two published months, so a gap stays a gap.
            if len(nxt) and len(seen) and pd.notna(seen.iloc[-1]) and pd.notna(nxt.iloc[0]):
                f = (xnum(cursor) - xnum(seen.index[-1])) / (xnum(nxt.index[0]) - xnum(seen.index[-1]))
                xs.append(cursor); ys.append(seen.iloc[-1] + f * (nxt.iloc[0] - seen.iloc[-1]))
            ln.set_data(xs, ys)
            pub = seen.dropna()
            if len(pub):
                tip_x, tip_y = (xs[-1], ys[-1]) if pd.notna(ys[-1]) else (pub.index[-1], pub.iloc[-1])
                dot.set_offsets([[mdates.date2num(pd.Timestamp(tip_x)), tip_y]])
                lab.xy = (tip_x, tip_y)
                lab.set_text(f"{name}\n{pub.iloc[-1]:+.1f}%")
        if gap_note is not None:
            gap_note.set_visible(cursor >= gap[0])
        shown = [m for m in lf.index if m <= cursor]
        clock.set_text("" if final else f"{shown[-1]:%B %Y}")
        fig.canvas.draw()
        return Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba()).convert("RGB").copy()

    n = int(round(SECONDS * 1000 / FRAME_MS))
    frames = [draw(t0 + (t1 - t0) * i / (n - 1)) for i in range(n)]
    end = draw(t1, final=True)

    OUT.mkdir(parents=True, exist_ok=True)
    pal = end.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames] + [pal]
    path = OUT / "sep26-03-mi-labor-force-jobs.gif"
    q[0].save(path, save_all=True, append_images=q[1:], duration=[FRAME_MS] * n + [int(HOLD * 1000)],
              loop=0, optimize=False, disposal=1)
    end.save(OUT / "sep26-03-mi-labor-force-jobs-final-frame.png")
    print(f"{path.name}: {len(q)} frames, {end.size[0]}x{end.size[1]}, {n * FRAME_MS / 1000:.1f}s + "
          f"{HOLD:.0f}s hold, {path.stat().st_size / 1e6:.2f} MB; last values jobs {jobs[last]:+.1f}%, "
          f"employed {lf[last]:+.1f}%")


if __name__ == "__main__":
    main()
