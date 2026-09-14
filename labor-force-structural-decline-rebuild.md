# Structural Labor Force Decline — Rebuild Spec

**Project:** "Mapping the Viral Spread of Labor Force Decline" (Data 4 The People)
**Original build:** Tableau (classification + map) → Claude chat (Python comparison, tables, copy)
**Target rebuild:** Python project in PyCharm, driven by Claude Code
**Source of this spec:** Claude chats of June 10, 2026 (update piece) and May 9, 2026 (timelapse), plus the published March 2026 article. Sections marked *[reconstructed]* were not done in chat — they describe the Tableau work by what it fed into the chats, and propose a Python equivalent.

---

## 1. What the tool does

Classifies every U.S. county (plus Puerto Rico municipios) by the percentage change in its **civilian labor force over a 20-year window**, using BLS **LAUS** (Local Area Unemployment Statistics) county data, and tracks how many counties fall into each band over time. The headline metric is the count of counties in **Structural Loss** (20-yr change < −10%).

Published findings so far:
- March 2026: structural-loss counties grew from ~8% to ~32% of U.S. counties between 2010 and the latest data.
- June 2026 update: structural-loss counties went **1,028 (Apr 2025) → 1,160 (Apr 2026), +132 in twelve months**.

---

## 2. Data source

| Item | Detail |
|---|---|
| Program | BLS LAUS, county level, **not seasonally adjusted** (LAUS county data is only published NSA) |
| Measure | Civilian labor force (LAUS measure code `06`) |
| Series ID pattern | `LAU` + area code + measure. County labor force = `LAUCN` + 5-digit FIPS + `0000000006` (e.g. `LAUCN390570000000006` = Greene County, OH). *[reconstructed — verify against `la.series` before relying on it]* |
| Bulk flat files | `https://download.bls.gov/pub/time.series/la/` — `la.data.64.County` (all county observations), `la.area` (area codes → names), `la.series` (series metadata), `la.measure` |
| Frequency | Monthly; `period` column `M01`–`M13` (`M13` = annual average, drop it) |
| Gotcha | BLS blocks scripted downloads without a browser-like `User-Agent` header. Set one explicitly in `requests`. |
| Gotcha | County universe drifts. Apr 2025 had 3,214 areas, Apr 2026 had 3,207. The 7-county gap in June 2026 was traced to four New Orleans-area parishes missing from the newer file. Always reconcile universes before diffing. |
| Gotcha | Oct 2025 data gap from the appropriations lapse shows up as nulls in adjacent BLS series; check LAUS for the same. |

**Tableau export format that fed the chat work** (this is the contract the downstream code expects):

```
area, category, labor_force, pct_change
"Autauga County, AL", "Keeping Pace (10-20%)", "27,543", "12.4%"
```
- `labor_force` arrives with thousands separators and quotes → strip before casting to int.
- `pct_change` arrives as a percent string → strip `%`, divide by 100.
- Read with `encoding='utf-8-sig'` (BOM present in the Tableau CSV).

---

## 3. Classification logic

**Metric:** `pct_change = LF(t) / LF(t − 20 years, same month) − 1`

Same-month comparison is deliberate: because LAUS is NSA, comparing April to April (or December to December) removes seasonality *within* each 20-year measurement. Cross-month deltas (e.g. Dec 2025 vs Apr 2026 category counts) carry a mild seasonal-anchor ambiguity; **year-over-year same-month deltas are the clean basis** and are what the June 2026 piece switched to.

**Bands** (exact labels as used in the Tableau export and tables):

| Category label | Range | Band edges |
|---|---|---|
| `Hyper-Growth (>40%)` | > +40% | (0.40, ∞) |
| `Superstars (20-40%)` | +20% to +40% | (0.20, 0.40] |
| `Keeping Pace (10-20%)` | +10% to +20% | (0.10, 0.20] |
| `Below-trend Growth (0-10%)` | 0% to +10% | (0.00, 0.10] |
| `At-risk Contraction (-10-0%)` | −10% to 0% | (−0.10, 0.00] |
| `Structural Loss (<-10%)` | < −10% | (−∞, −0.10] |

Boundary handling: the Tableau build's exact inclusive/exclusive edges weren't recorded. Lincoln County, NE sat at exactly −10.0% and was treated as *outside* structural loss in Apr 2026, which implies **Structural Loss is strictly less than −10%** (i.e. −0.10 is At-risk). Use `pd.cut(..., right=True)` with the bins above and confirm the Lincoln County result matches on rebuild.

```python
BINS   = [-float("inf"), -0.10, 0.0, 0.10, 0.20, 0.40, float("inf")]
LABELS = ["Structural Loss (<-10%)", "At-risk Contraction (-10-0%)",
          "Below-trend Growth (0-10%)", "Keeping Pace (10-20%)",
          "Superstars (20-40%)", "Hyper-Growth (>40%)"]
df["category"] = pd.cut(df["pct_change"], bins=BINS, labels=LABELS, right=True)
```

Display order (top to bottom in tables): Hyper-Growth → Superstars → Keeping Pace → Below-trend → At-risk → Structural Loss (highlighted row) → Grand total.

---

## 4. Pipeline stages

### Stage A — Ingest *[reconstructed; was Tableau]*
1. Download `la.data.64.County`, `la.area`, `la.series` (with User-Agent header). Cache locally; the county file is several hundred MB.
2. Filter `la.data.64.County` to `series_id` ending in `06` (labor force), drop `M13`.
3. Join area names from `la.area` (`area_code` → `area_text`, e.g. "Greene County, OH").
4. Pivot to a tidy panel: `fips, area, year, month, labor_force`.
5. Persist as Parquet (`data/laus_county_lf.parquet`).

### Stage B — Classify *[reconstructed; was Tableau]*
For each `(fips, year, month)` with a valid observation 240 months earlier, compute `pct_change` and assign `category`. Output: `data/classified.parquet` with `fips, area, date, labor_force, pct_change, category`. This is the table the Tableau map was built on and is what every downstream step consumes.

### Stage C — Snapshot & compare (done in chat, June 2026)
Given two snapshot months `t0` and `t1` (same calendar month, one year apart is the standard):

1. **Category counts** for each snapshot + delta per category + grand total. Flag any universe mismatch (row counts differ).
2. **Set comparison on the structural-loss lists:**
   - `new_entrants = SL(t1) − SL(t0)` → sort by `labor_force` desc, top 10
   - `dropped = SL(t0) − SL(t1)` → sort by `labor_force` desc, top 10; **exclude** counties absent from the `t1` universe entirely (those are coverage gaps, not recoveries) and show each county's `t1` landing category
   - `worsened = SL(t0) ∩ SL(t1)` with `delta = pct(t1) − pct(t0)` → filter `labor_force > 20,000`, sort by `delta` asc, top 10
3. Note: category-count deltas and list-set deltas can differ slightly (Dec→Apr showed +107 vs +105) because of churn through the adjacent At-risk band and universe changes. Lead with the category-count number.
4. Decision from June 2026: **include Puerto Rico** in all tables (San Juan and Bayamón were among the sharpest deteriorations).

Reference implementation (verbatim from the chat, lightly tidied):

```python
import pandas as pd

def load(p):
    d = pd.read_csv(p, encoding="utf-8-sig")
    d.columns = ["area", "category", "lf", "pct"]
    d["lf"]  = d["lf"].astype(str).str.replace(",", "").str.replace('"', "").astype(int)
    d["pct"] = d["pct"].astype(str).str.replace("%", "").astype(float) / 100.0
    return d

ORDER = ["Hyper-Growth (>40%)", "Superstars (20-40%)", "Keeping Pace (10-20%)",
         "Below-trend Growth (0-10%)", "At-risk Contraction (-10-0%)", "Structural Loss (<-10%)"]
SL = "Structural Loss (<-10%)"

def compare(a0, a1):
    c0, c1 = a0.category.value_counts(), a1.category.value_counts()
    counts = pd.DataFrame({"t0": [c0.get(k, 0) for k in ORDER],
                           "t1": [c1.get(k, 0) for k in ORDER]}, index=ORDER)
    counts["delta"] = counts.t1 - counts.t0

    s0 = a0[a0.category == SL].set_index("area")
    s1 = a1[a1.category == SL].set_index("area")
    all1 = a1.set_index("area")

    new  = s1.loc[s1.index.difference(s0.index)].sort_values("lf", ascending=False)
    gone = s0.index.difference(s1.index)
    gone_present = gone.intersection(all1.index)          # still in the t1 universe
    gone_missing = gone.difference(all1.index)            # coverage gap — report separately
    dropped = s0.loc[gone_present].join(all1.loc[gone_present, ["category", "pct"]],
                                        rsuffix="_t1").sort_values("lf", ascending=False)
    both = s0.index.intersection(s1.index)
    wors = s1.loc[both, ["lf", "pct"]].join(s0.loc[both, ["pct"]], rsuffix="_t0")
    wors["delta"] = wors.pct - wors.pct_t0
    wors = wors[wors.lf > 20_000].sort_values("delta")

    return counts, new.head(10), dropped.head(10), wors.head(10), gone_missing
```

### Stage D — Render tables (done in chat, June 2026)
Four PNGs via matplotlib, **200 DPI**, D4TP palette:

| Role | Hex |
|---|---|
| Teal (headers, text) | `#085041` |
| Coral (structural-loss highlight, negatives) | `#712B13` |
| Paper (background) | `#F7F5EF` |

Each table carries: title, explanatory subtitle, and the source line
`U.S. Bureau of Labor Statistics (LAUS); Data 4 The People analysis.`
Structural-loss row in the category table is highlighted in coral with the delta bolded. Use a real minus sign (U+2212) for negatives in display text.

Tables:
1. Category comparison (6 bands + grand total, three columns: t0, t1, change)
2. Top-10 new entrants (county, labor force, 20-yr change)
3. Top-10 worsened (county, labor force, pct t0, pct t1, worsening in pts)
4. Top-10 dropped off (county, labor force, pct t0, pct t1, landing category)

### Stage E — Map *[was Tableau; optional to rebuild]*
County choropleth of `category`, filterable by `MY(Date)`. The published card image was a screenshot with slider/dropdown widgets removed and even white padding added. The May 2026 timelapse (2010→2025, one frame per month) was exported from Tableau as MOV and cleaned with ffmpeg (fade-through-white transitions replaced by hard cuts via frame-brightness detection; output 720p H.264 MP4, `-movflags +faststart`, ~5.6 MB).

For a Python rebuild: plotly `choropleth` with the Census county GeoJSON keyed on FIPS, one frame per month, export via `kaleido` and stitch with ffmpeg. Keeping Tableau for the interactive embed is also fine — Stage B's Parquet output is what Tableau would connect to.

### Stage F — Copy & CMS fields (done in chat)
Article voice: "geographic contagion" / "virus" framing, sober register, closes with **"The labor force data does not lie."** Methodology footer states the classification window, the source line, and any universe mismatch. Prismic fields produced: meta title (<60 chars), meta description (~155 chars), social context line, campaign name `labor-force-decline-update-YYYY-MM`, Article JSON-LD schema (see `/areas/d4tp-schema.md` conventions).

---

## 5. Proposed repo layout for Claude Code

```
labor-force-decline/
├── CLAUDE.md                 # paste sections 2–4 of this doc here
├── pyproject.toml            # pandas, pyarrow, requests, matplotlib, (plotly, kaleido)
├── data/
│   ├── raw/                  # la.data.64.County, la.area, la.series (gitignored)
│   ├── laus_county_lf.parquet
│   └── classified.parquet
├── src/lfd/
│   ├── ingest.py             # Stage A
│   ├── classify.py           # Stage B — BINS/LABELS live here, nowhere else
│   ├── compare.py            # Stage C
│   ├── tables.py             # Stage D
│   ├── map.py                # Stage E (optional)
│   └── cli.py                # `lfd snapshot 2025-04 2026-04 --out outputs/`
├── tests/
│   ├── test_classify.py      # boundary cases: -0.10, 0.0, 0.10, 0.20, 0.40
│   └── test_compare.py       # fixture reproducing Apr25→Apr26 = +132
└── outputs/
```

**Validation targets** (the rebuild should reproduce these exactly from raw LAUS before you trust anything new):
- Apr 2026 structural-loss count = **1,160**; Apr 2025 = **1,028**
- Apr 2026 category counts: Hyper-Growth 143, Superstars 256, Keeping Pace 312, Below-trend 561, At-risk 775, Structural Loss 1,160 (total 3,207)
- Dec 2025 category counts: 162 / 264 / 323 / 609 / 792 / 1,053 (total 3,203)
- Erie County, PA: SL in Dec 2025 (−10.4%), At-risk in Apr 2026 (−9.3%)
- Lucas County, OH tops Apr25→Apr26 new entrants by labor force
- Saginaw County, MI Apr 2026: LF 85,594, −12.6%

If raw-LAUS recomputation doesn't hit these, the likeliest causes are (a) boundary inclusivity, (b) BLS revisions since the Tableau extract (LAUS revises annually each spring), or (c) universe differences — check in that order.

---

## 6. Suggested first Claude Code prompt

> Read CLAUDE.md. Build `src/lfd/ingest.py` to download and cache the BLS LAUS county flat files (set a browser User-Agent), filter to labor-force series, join area names, and write `data/laus_county_lf.parquet`. Then build `classify.py` implementing the 20-year same-month percent change and the six-band classification exactly as specified. Add `tests/test_classify.py` covering the band boundaries. Stop before writing compare.py and show me the Apr 2026 category counts so I can check them against the validation targets.
