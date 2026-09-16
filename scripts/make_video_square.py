"""Square (1080x1080) version of the map timelapse, for Instagram.

Reuses the frames captured by scripts/make_video.py (outputs/video/raw) and
recomposes each one: the month in the page's own type at the top, the map in
the middle, the band counts below, and the logo at the foot.

Run:  .venv/bin/python scripts/make_video_square.py [--fps 6]
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

import imageio_ffmpeg
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

from lfd import ROOT

RAW = ROOT / "outputs" / "video" / "raw"
ASSETS = ROOT / "assets"
SIZE = 1080
PAPER = (0xF7, 0xF5, 0xEF)

# 2x-pixel boxes measured on a captured frame (1000x760 CSS layout)
MAP = (32, 243, 1348, 1122)          # the map canvas with the insets
BANDS = (1362, 755, 1972, 1122)      # the band counts card
INK = (0x1F, 0x2A, 0x27)
MUTED = (0x7E, 0x8A, 0x86)
FONT = "/System/Library/Fonts/Helvetica.ttc"
MONTH_FONT = ImageFont.truetype(FONT, 46, index=1)   # bold
CAP_FONT = ImageFont.truetype(FONT, 21)
CAPTION = "Twenty-year change in labor force by county"


def compose(src: Path, dst: Path, logo: Image.Image, month: str) -> None:
    """Caption and month on top, map in the middle, band counts below, logo at the foot.

    The month is drawn rather than cropped from the frame, so a long name like
    September never runs past a fixed box.
    """
    f = Image.open(src).convert("RGB")
    canvas = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(canvas)

    def fit(box, width):
        im = f.crop(box)
        return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)

    m, b = fit(MAP, 860), fit(BANDS, 470)
    cap_h, month_h, gap = 28, 62, 12
    total = cap_h + month_h + gap + m.height + gap + b.height + gap + logo.height
    y = max(20, (SIZE - total) // 2)

    d.text((SIZE / 2, y), CAPTION, font=CAP_FONT, fill=MUTED, anchor="ma")
    y += cap_h
    d.text((SIZE / 2, y), month, font=MONTH_FONT, fill=INK, anchor="ma")
    y += month_h + gap
    for part in (m, b, logo):
        canvas.paste(part, ((SIZE - part.width) // 2, y))
        y += part.height + gap
    canvas.save(dst)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fps", type=float, default=10.0, help="months per second")
    ap.add_argument("--hold-start", type=float, default=1.0)
    ap.add_argument("--hold-end", type=float, default=3.0)
    ap.add_argument("--out", type=Path,
                    default=ROOT / "posts" / "labor-force-history-viz" / "labor-force-history-viz-timelapse-square.mp4")
    a = ap.parse_args()

    shots = sorted(RAW.glob("*.png"))
    if not shots:
        raise SystemExit("no frames in outputs/video/raw; run scripts/make_video.py first")

    logo = Image.open(ASSETS / "d4tp-text-dark.png").convert("RGB")
    logo = logo.resize((240, round(logo.height * 240 / logo.width)), Image.LANCZOS)

    frames = ROOT / "outputs" / "video" / "square"
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir(parents=True)

    months = [f"{d:%B %Y}" for d in pd.date_range("2010-01-01", periods=len(shots), freq="MS")]
    pairs = ([(shots[0], months[0])] * round(a.hold_start * a.fps) + list(zip(shots, months))
             + [(shots[-1], months[-1])] * round(a.hold_end * a.fps))
    for n, (src, month) in enumerate(pairs):
        dst = frames / f"{n:04d}.png"
        if n and pairs[n - 1][0] == src:
            shutil.copyfile(frames / f"{n - 1:04d}.png", dst)
        else:
            compose(src, dst, logo, month)
    seq = pairs

    a.out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
                    "-framerate", str(a.fps), "-i", str(frames / "%04d.png"),
                    "-r", "30", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(a.out)], check=True)
    print(f"wrote {a.out}: {SIZE}x{SIZE}, {len(seq)/a.fps:.1f}s, {a.out.stat().st_size/1e6:.1f} MB")


if __name__ == "__main__":
    main()
