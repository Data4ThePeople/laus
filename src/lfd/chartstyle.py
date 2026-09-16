"""House palette and helpers for the static chart PNGs.

Dark palette, as the Prismic and Mailchimp charts use: background #181A1B,
text #BBBDC0. Band colours come from the map and are lightened where a dark
background would swallow them.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG, INK, MUTED, GRID = "#181A1B", "#BBBDC0", "#8C9094", "#2A2E31"
CORAL = "#C4795A"      # loss, the Structural Loss band lightened for a dark background
TEAL = "#5FA78C"       # growth, the Superstars band lightened the same way
SOURCE = "U.S. Bureau of Labor Statistics (LAUS); Data 4 The People analysis."
CREDIT = "Built by Data 4 The People"


def figure(width: float = 8.4, height: float = 5.0):
    fig, ax = plt.subplots(figsize=(width, height), dpi=200)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)
    ax.set_axisbelow(True)
    return fig, ax


def frame(fig, title: str, subtitle: str, top: float = 0.80) -> None:
    """Title, subtitle, source line and credit, in the house positions."""
    fig.text(0.055, 0.955, title, color=INK, fontsize=15, fontweight="bold", va="top")
    fig.text(0.055, 0.893, subtitle, color=MUTED, fontsize=10, va="top")
    fig.text(0.055, 0.035, SOURCE, color=MUTED, fontsize=8.5)
    fig.text(0.945, 0.035, CREDIT, color=MUTED, fontsize=8.5, ha="right")
    fig.subplots_adjust(left=0.075, right=0.975, top=top, bottom=0.115)


def word_legend(fig, items: list[tuple[str, str]], y: float = 0.836, x: float = 0.055) -> None:
    """Legend as coloured words, house style, not dots."""
    for label, colour in items:
        t = fig.text(x, y, label, color=colour, fontsize=9.5, fontweight="bold", va="top")
        fig.canvas.draw()
        x += t.get_window_extent().width / fig.get_size_inches()[0] / fig.dpi + 0.022
