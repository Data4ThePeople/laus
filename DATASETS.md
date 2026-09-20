# Datasets

One section per dataset, written before any analysis, updated whenever we learn
something new. The point is to know the traps before they show up in a chart.

## Local Area Unemployment Statistics, county civilian labor force (U.S. Bureau of Labor Statistics)

**What it is.** One row per county (and Puerto Rico municipio) per month. The
cell we use is the civilian labor force: everyone 16 and over who lives in that
county and is either working or actively looking for work. It counts people
where they live, not where they work.

**Where it comes from.** The LAUS flat files at
`https://download.bls.gov/pub/time.series/la/`, pulled by `src/lfd/ingest.py`
into `data/raw/` (several hundred MB, gitignored) and cached as
`data/laus_county_lf.parquet`. No login. The download needs a browser-like
User-Agent with a contact address, read from `D4TP_CONTACT` in the central
`.env`.

**Version and vintage.** Monthly release, about three weeks after the reference
month. Current pull: September 14, 2026, covering January 1990 through July
2026. Each release can revise recent months, and the annual spring processing
revises several prior years at once.

**Coverage.** 3,225 county series, January 1990 to July 2026. Every classified
county-month needs a valid observation in the same calendar month 20 years
earlier, so the classified panel is smaller than the raw panel and its size
moves month to month. Typical classified universe is about 3,210 counties.
LAUS values are not all direct measurements: sub-state estimates come from a
model built on the Current Population Survey, state unemployment insurance
claims and the Current Employment Statistics payroll survey, then controlled to
the state total. Counties below the model's size threshold are disaggregated
from their labor market area, so a small county's month is an allocation of a
larger area's estimate rather than an independent reading. BLS documents this
in the LAUS estimation methodology.

**Changes over time.** Connecticut switched from eight counties to nine
planning regions (FIPS 09110 to 09190); our file carries the planning regions
for the whole history, which matches the Census 2022 and later shapes. Alaska
redraws areas: four end in December 2009 or December 2019, seven begin in
January 2010 or January 2020, and Yakutat begins in 1994. A new Alaska area
cannot be classified until it has 20 years of history, so we draw it as "no
data". Every January the series is re-benchmarked to new population controls,
which puts a small step in the level that is not a change in the labor market.
January 2026 carries one of these breaks.

**Suppressed, censored or masked values.** None for the labor force level at
county detail. Values are published rounded, which matters only for the
smallest counties.

**Missing data.** Missing is a genuine gap, never zero. The known gaps:
October 2025 is null for every county except Puerto Rico's 78 municipios, from
the appropriations lapse. Puerto Rico is null for March and April 2020, when
the survey was suspended. Seven New Orleans-area parishes are null from
September 2005 to June 2006 after Hurricane Katrina. Because we compare to the
same month 20 years back, each of these gaps knocks a set of counties out of
the classified universe twice: once in the gap year and once 20 years later.
Counties missing from one snapshot and present in another are coverage gaps,
not recoveries, and we report them separately.

**Revisions.** BLS revises history. The annual spring processing re-estimates
several prior years, so a county can cross a band boundary without anything
changing on the ground. Months from the current year are preliminary. We do not
pin a vintage; we refresh the whole series on each pull and re-run the
validation table in `CLAUDE.md`.

**Units and rounding.** People, published as whole numbers. Percent change is
computed from the two published levels and shown to one decimal place. For
small counties the published precision is finer than the real accuracy.

**Known quirks.** Extreme 20-year changes in tiny counties (Loving TX, Douglas
CO, McMullen TX) are real, not errors; small resort, energy and fishing
counties can swing more than 15% month to month. That is why every comparison
in this project is same-month. Band edges are left-closed: exactly -10.0% is
At-risk, not Structural Loss (checked against Lincoln County, NE).

**Uncertainty.** BLS publishes no confidence interval for county labor force
levels. It states that sub-state estimates are model-based and less reliable
the smaller the area, and that the model is controlled to the state total, so
county errors offset within a state rather than accumulating. Treat any single
small county's month as indicative and any month-to-month move in one small
county as noise until a same-month comparison confirms it.

**License and attribution.** Public domain, a U.S. government work. Credit line:
`U.S. Bureau of Labor Statistics (LAUS); Data 4 The People analysis.`
