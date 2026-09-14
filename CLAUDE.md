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

## Repo and hosting

GitHub: https://github.com/Data4ThePeople/laus (public, in the Data4ThePeople
org, never under esp-D4TP). GitHub Pages serves `dist/` at
https://data4thepeople.github.io/laus/ via `.github/workflows/pages.yml` on
every push to main that touches `dist/`. That URL is the Prismic embed.

## Layout

```
src/lfd/ingest.py     Stage A: download + cache BLS flat files -> data/laus_county_lf.parquet
src/lfd/classify.py   Stage B: 20-year pct_change + bands -> data/classified.parquet
                      BINS and LABELS live here and nowhere else.
src/lfd/compare.py    Stage C: two-snapshot comparison, `python -m lfd.compare 2025-04 2026-04`
src/lfd/watch.py      Stage C2: positive / negative watch flags -> data/watch.parquet
src/lfd/tables.py     Stage D: matplotlib tables, 200 DPI (to build)
src/lfd/geo.py        Stage E1: Census county shapes, composite Albers with AK/HI/PR insets -> data/geo.json
src/lfd/viz.py        Stage E2: encodes blocks + templates/index.html -> dist/index.html
src/lfd/templates/    the page: vanilla JS, no library; carries no data of its own
src/lfd/cli.py        `lfd ingest | classify | snapshot | viz`
tests/                pytest; boundary cases and small synthetic panels
data/raw/             BLS flat files, gitignored, several hundred MB
outputs/              rendered tables
dist/                 built viz
```

Run with the project venv, in order: `python -m lfd.ingest`, `lfd.classify`,
`lfd.watch`, `lfd.geo`, `lfd.viz`. Tests: `.venv/bin/python -m pytest`.
Deep links into the viz: `dist/index.html#fips=26145&month=2026-04&watch=1&state=MI`.
The state selector zooms the map, fades other states, and filters every
stat card. Logos live in `assets/` and are inlined at build time; the logo
sits in the header standalone and moves to the footer inside the Prismic frame.
Preview at sizes with headless Chrome; note it enforces a minimum window
width of about 500px, so test phone width through a 390px iframe wrapper.

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

## Data facts learned from the first real run (Sep 14, 2026)

- Panel: 3,225 county series, Jan 1990 to Jul 2026. 2026 months are
  preliminary until the spring revision.
- Oct 2025 (appropriations lapse): null for every county except Puerto
  Rico's 78 municipios. Every classified frame for Oct 2025 and Oct 2045 is
  therefore almost empty.
- Hurricane Katrina: seven New Orleans-area parishes are null Sep 2005 to
  Jun 2006, so they drop out of the classified universe Sep 2025 to Jun 2026
  and return Jul 2026. Four of them were in Structural Loss at Apr 2025; that
  is the "four parishes" in the June 2026 piece. Coverage gap, not recovery.
- Puerto Rico: null Mar and Apr 2020 (survey suspended), so PR is absent
  from the Mar and Apr 2040 frames too.
- Alaska: four areas end in Dec 2009 or Dec 2019 and seven begin Jan 2010 or
  Jan 2020 (plus Yakutat from 1994). The new ones cannot be classified until
  they have 20 years of history. Draw them as "no data".
- Connecticut is on the nine planning regions (FIPS 09110 to 09190) for the
  whole history, which matches the Census 2022+ shapes.
- Extreme 20-year changes (Loving TX, Douglas CO, McMullen TX) are real, not
  errors. Small resort and fishing counties swing 15%+ month to month, which
  is why every comparison is same-month.
- Validation on this run: Apr 2025 SL 1,028 exact; Apr 2026 SL 1,156 vs the
  published 1,160 (BLS revisions since the Tableau extract; 47 counties sit
  within a quarter point of the line). Apr25 to Apr26 = +128 vs published +132.
- The spec's Saginaw figure (85,594) is its Apr 2025 labor force, not Apr 2026.

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
