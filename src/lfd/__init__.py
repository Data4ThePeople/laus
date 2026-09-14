"""lfd: structural labor force decline, county classification from BLS LAUS."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
RAW = DATA / "raw"
OUTPUTS = ROOT / "outputs"
DIST = ROOT / "dist"

PANEL_PATH = DATA / "laus_county_lf.parquet"
CLASSIFIED_PATH = DATA / "classified.parquet"
