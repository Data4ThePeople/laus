"""Build the LinkedIn document carousel for the takeaways post.

Nine 1200x1500 pages: a cover, the five takeaways, two extra charts and a
closing page. Each page places an existing chart on the house dark background
with a short line of copy above it, so the file is rebuilt whenever the charts
are.

Run:  .venv/bin/python scripts/make_linkedin_pdf.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from lfd import ROOT
from lfd.chartstyle import BG, CORAL, INK, MUTED, TEAL

CHARTS = ROOT / "posts" / "five-takeaways-labor-force-decline" / "images"
W, H, MARGIN = 1200, 1200, 64
FONT = "/System/Library/Fonts/Helvetica.ttc"
TITLE = ImageFont.truetype(FONT, 58, index=1)
KICKER = ImageFont.truetype(FONT, 27, index=1)
BODY = ImageFont.truetype(FONT, 30)
FOOT = ImageFont.truetype(FONT, 22)

PAGES = [
    ("Five takeaways", "40% of U.S. counties now have a labor force\nmore than 10% smaller than 20 years ago.\n\n1,281 of 3,214 counties, the highest on record.", None),
    ("1. Two in five counties are shrinking", "7% of counties in 2010. 40% today.", "01-structural-loss-over-time.png"),
    ("2. The weakest year outside 2020", "Counties normally add workers from January to July.\nThis year 38% lost them, against a long-run 21%.", "02-january-to-july.png"),
    ("3. Whole states are sliding", "In Michigan, 72 of 83 counties are on negative watch,\nand not one is recovering.", "03b-mi-negative-watch.png"),
    ("3b. Colorado starts at the top", "All ten of its largest counties are shrinking,\nDenver included.", "03c-co-largest-counties.png"),
    ("4. A few are going the other way", "In South Carolina, 39 of 46 counties are turning up,\nholding 95% of the state's workers.", "04b-sc-positive-watch.png"),
    ("5. Even the boom counties stalled", "Two years ago, 3% of hyper-growth counties were\nshrinking. Today 48% are.", "05a-hypergrowth-falling.png"),
    ("The places you would not expect", "Wake County, North Carolina peaked in July 2025.", "05-1-wake-nc.png"),
    ("Look up your own county", "The map is free. Press play to watch 16 years,\npick your state, hover any county.\n\ndata4thepeople.com", None),
]


def page(title: str, body: str, chart: str | None) -> Image.Image:
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((MARGIN, MARGIN), "DATA 4 THE PEOPLE", font=KICKER, fill=CORAL)
    y = MARGIN + 60
    for line in title.split("\n"):
        d.text((MARGIN, y), line, font=TITLE, fill=INK); y += 70
    y += 18
    for line in body.split("\n"):
        d.text((MARGIN, y), line, font=BODY, fill=MUTED); y += 44
    if chart:
        c = Image.open(CHARTS / chart).convert("RGB")
        width = W - 2 * MARGIN
        c = c.resize((width, round(c.height * width / c.width)), Image.LANCZOS)
        im.paste(c, (MARGIN, y + 46))
    d.text((MARGIN, H - MARGIN - 10), "U.S. Bureau of Labor Statistics (LAUS)", font=FOOT, fill=MUTED)
    if chart or title.startswith("Five"):
        d.text((W - MARGIN, H - MARGIN - 10), "swipe", font=FOOT, fill=TEAL, anchor="ra")
    return im


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=ROOT / "outputs" / "linkedin-carousel.pdf")
    a = ap.parse_args()
    pages = [page(*p) for p in PAGES]
    a.out.parent.mkdir(parents=True, exist_ok=True)
    pages[0].save(a.out, save_all=True, append_images=pages[1:], resolution=150.0)
    print(f"wrote {a.out}: {len(pages)} pages, {W}x{H}, {a.out.stat().st_size/1e6:.1f} MB")
    pages[1].save(a.out.with_suffix(".preview.png"))


if __name__ == "__main__":
    main()
