# laus: structural labor force decline

Python rebuild of the "Mapping the Viral Spread of Labor Force Decline" tool.
The full spec is `labor-force-structural-decline-rebuild.md` at the repo root;
read it before touching the pipeline. The viz enhancement plan is
`docs/VIZ-PLAN.md`.

## What it does

Classifies every U.S. county and Puerto Rico municipio by the 20-year
same-month percent change in civilian labor force (BLS LAUS, county level,
not seasonally adjusted) into six bands. Headline metric: the count of
counties in Structural Loss (strictly below -10%).

## Layout

```
src/lfd/ingest.py     Stage A: download + cache BLS flat files -> data/laus_county_lf.parquet
src/lfd/classify.py   Stage B: 20-year pct_change + bands -> data/classified.parquet
                      BINS and LABELS live here and nowhere else.
src/lfd/compare.py    Stage C: two-snapshot comparison (to build)
src/lfd/tables.py     Stage D: matplotlib tables, 200 DPI (to build)
src/lfd/viz.py        Stage E: self-contained interactive map -> dist/index.html (to build)
src/lfd/cli.py        `lfd ingest`, `lfd classify`, later `lfd snapshot`, `lfd viz`
tests/                pytest; boundary cases and small synthetic panels
data/raw/             BLS flat files, gitignored, several hundred MB
outputs/              rendered tables
dist/                 built viz
```

Run with the project venv: `.venv/bin/python -m lfd.ingest`, then
`.venv/bin/python -m lfd.classify --snapshot 2026-04`. Tests: `.venv/bin/python -m pytest`.

## Rules

- Bands are left-closed: -10.0% exactly is At-risk, not Structural Loss.
  The spec's prose says this and its code sample says the opposite; the
  prose wins until the Lincoln County, NE check on real data says otherwise.
- Same-month comparisons only. Year-over-year same-month deltas are the clean
  basis for any "change over time" statement.
- Reconcile the county universe before diffing two snapshots. Report
  counties missing from one file separately; they are coverage gaps, not
  recoveries.
- BLS downloads need a browser-like User-Agent with a contact address. It is
  read from `D4TP_CONTACT` in the central `.env`; default is the D4TP site URL.
- Nothing hardcoded in the viz; bands, colors and counts are emitted from the
  Python side at build time. Duplicate keys are a hard failure.
- Interactive viz: vanilla JS, no CDN, no charting library, one
  self-contained HTML, sized for the Prismic 780px frame, light theme when
  framed, "Built by Data 4 The People" on it.
- Palette for tables: teal `#085041`, coral `#712B13`, paper `#F7F5EF`.
  Source line: `U.S. Bureau of Labor Statistics (LAUS); Data 4 The People analysis.`

## Validation targets (must reproduce from raw LAUS before trusting anything new)

| Snapshot | Hyper | Superstars | Keeping | Below | At-risk | SL | Total |
|---|---|---|---|---|---|---|---|
| Apr 2025 | | | | | | 1,028 | 3,214 |
| Dec 2025 | 162 | 264 | 323 | 609 | 792 | 1,053 | 3,203 |
| Apr 2026 | 143 | 256 | 312 | 561 | 775 | 1,160 | 3,207 |

Spot checks: Erie County, PA is SL in Dec 2025 (-10.4%) and At-risk in Apr
2026 (-9.3%). Lucas County, OH tops the Apr 2025 to Apr 2026 new entrants by
labor force. Saginaw County, MI in Apr 2026: LF 85,594, -12.6%. Lincoln
County, NE at -10.0% in Apr 2026 is At-risk.

If the numbers miss, check in order: boundary inclusivity, BLS annual spring
revisions since the Tableau extract, universe differences.
