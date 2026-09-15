"""Render the interactive map playing from January 2010 to the latest month as
a 1920x1080 MP4 for social media.

Each month is captured from the built page (dist/index.html) in headless
Chrome through its deep link, cropped to the header, controls, map, trend
chart and band counts, padded onto the page's paper color, and encoded with
the ffmpeg binary bundled by imageio-ffmpeg.

Run:  .venv/bin/python scripts/make_video.py [--fps 6] [--county 26145]
Needs Google Chrome and `pip install -e ".[video]"`.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import imageio_ffmpeg
import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dist" / "index.html"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PAPER = (0xF7, 0xF5, 0xEF)
W, H, PAD = 1920, 1080, 60
CROP = (16, 16, 1984, 1122)   # 2x pixels: header through the band counts card (bottom edge 1113, next card 1131)


def months() -> list[str]:
    from lfd import CLASSIFIED_PATH
    dates = pd.read_parquet(CLASSIFIED_PATH, columns=["date"])["date"]
    return [f"{d:%Y-%m}" for d in pd.date_range("2010-01-01", dates.max(), freq="MS")]


def capture(args) -> Path:
    i, month, county, raw_dir = args
    out = raw_dir / f"{i:03d}.png"
    if out.exists():
        return out
    url = f"file://{PAGE}#month={month}" + (f"&fips={county}" if county else "")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--virtual-time-budget=5000",
                    "--window-size=1000,760", f"--screenshot={out}", url],
                   check=True, capture_output=True, timeout=120)
    return out


def compose(src: Path, dst: Path) -> None:
    im = Image.open(src).convert("RGB").crop(CROP)
    s = min((W - 2 * PAD) / im.width, (H - 2 * PAD) / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), PAPER)
    canvas.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    canvas.save(dst)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fps", type=float, default=6.0, help="months per second (6 = the page's 2x speed)")
    ap.add_argument("--county", default="26145", help="FIPS to pin in the trend chart; empty for none")
    ap.add_argument("--hold-start", type=float, default=1.5)
    ap.add_argument("--hold-end", type=float, default=4.0)
    ap.add_argument("--work", type=Path, default=ROOT / "outputs" / "video")
    ap.add_argument("--out", type=Path,
                    default=ROOT / "posts" / "labor-force-history-viz" / "labor-force-history-viz-timelapse-1080p.mp4")
    args = ap.parse_args()

    ms = months()
    raw, frames = args.work / "raw", args.work / "frames"
    raw.mkdir(parents=True, exist_ok=True)
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir(parents=True)

    with ThreadPoolExecutor(max_workers=6) as pool:
        shots = list(pool.map(capture, [(i, m, args.county, raw) for i, m in enumerate(ms)]))
    print(f"captured {len(shots)} months, {ms[0]} to {ms[-1]}")

    seq = [shots[0]] * round(args.hold_start * args.fps) + shots + [shots[-1]] * round(args.hold_end * args.fps)
    for n, src in enumerate(seq):
        dst = frames / f"{n:04d}.png"
        if n and seq[n - 1] == src:
            shutil.copyfile(frames / f"{n - 1:04d}.png", dst)
        else:
            compose(src, dst)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
                    "-framerate", str(args.fps), "-i", str(frames / "%04d.png"),
                    "-r", "30", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(args.out)], check=True)
    secs = len(seq) / args.fps
    print(f"wrote {args.out}: {W}x{H}, {secs:.1f}s, {args.out.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
