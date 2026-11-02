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
month. Current pull: November 2, 2026 (files posted October 28, 2026), covering
January 1990 through September 2026. Each release can revise recent months,
and the annual spring processing revises several prior years at once. The
November pull revised July 2026 slightly (Structural Loss 1,281 to 1,279);
April 2025 and April 2026 did not move.

**Coverage.** 3,225 county series, January 1990 to September 2026. Every classified
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

**State totals.** County levels are shares of a model-based state estimate:
BLS controls every county in a state so they sum to the state figure. A large
move in the state estimate moves every county in that state in the same
direction. Before reading a cluster of counties in one state as local news,
compare each county's change with its state's. Michigan's 83 counties summed
to 4,791,575 in September 2026, against 4,791,578 in the published statewide
series `LAUST260000000000006` (rounding).

## Current Employment Statistics, state payroll jobs (U.S. Bureau of Labor Statistics)

**What it is.** Monthly count of payroll jobs at employers located in a state,
by industry. One cell is thousands of jobs in a state, industry and month.

**Where it comes from.** BLS public API v2 (`api.bls.gov`), key
`BLS_API_KEY`. Series used: `SMS26000000000000001` (Michigan total nonfarm,
seasonally adjusted), `SMS26000003000000001` (Michigan manufacturing,
seasonally adjusted), `SMU26000003133600001` (Michigan transportation
equipment manufacturing, NAICS 336, not seasonally adjusted), plus U.S.
totals `CES0000000001` and `CES3000000001`. The same cache holds two LAUS
statewide series for Michigan, seasonally adjusted, used only for the
labor force versus jobs chart: `LASST260000000000006` (labor force) and
`LASST260000000000005` (employed), stored in thousands. Cached in
`data/ces/mi_ces.csv`; the LAUS seasonally adjusted series has no October
2025 value.

**Version and vintage.** Pulled November 2, 2026, through September 2026. The
latest month is preliminary and is revised the next month. Every March, BLS
re-benchmarks state series to QCEW counts, which can move the prior two years.

**Coverage.** Nonfarm employers. Excludes the self-employed, farm workers and
household workers. A sample survey of employers, not a full count.

**Changes over time.** Industry codes follow NAICS; motor vehicle detail is
not published for every state or month. Use only the series listed above.

**Suppressed, censored or masked values.** Michigan detail below NAICS 336 is
not used because it is not published in every month.

**Missing data.** None in the five CES series: all run January 2015 to
September 2026 with every month present, including October 2025.

**Revisions.** Monthly and annual. We refresh the whole series each pull.

**Units and rounding.** Thousands of jobs, one decimal.

**Known quirks.** This counts jobs where they are, not people where they live.
A worker with two jobs counts twice; a Michigan resident working in Ohio is
not counted. It is not the same thing as the LAUS labor force, which counts
residents working or looking for work. Use it as a separate check, never as a
second measure of the same quantity.

**Uncertainty.** CES is a sample survey, and BLS publishes sampling error for
state estimates; small month-to-month moves in a state can sit within it.
Treat same-month year-over-year changes as the comparison.

**License and attribution.** Public domain. `U.S. Bureau of Labor Statistics
(CES)`.

## Quarterly Census of Employment and Wages, county by industry (U.S. Bureau of Labor Statistics)

**What it is.** Jobs and wages at every employer covered by unemployment
insurance, by county and industry, for each month of each quarter.

**Where it comes from.** QCEW open data CSV files,
`https://data.bls.gov/cew/data/api/<year>/<qtr>/area/<fips>.csv`. No key; the
same browser-like User-Agent as LAUS. Cached under `data/qcew/`.

**Version and vintage.** Latest available quarter is Q1 2026 (Q2 2026 not yet
posted on November 2, 2026). About five to six months behind.

**Coverage.** Over 95% of U.S. jobs: every employer that pays unemployment
insurance. It is a full count from tax filings, not a sample. Excludes the
self-employed and some farm and religious workers.

**Changes over time.** NAICS revisions in 2017 and 2022 do not touch
manufacturing at the levels we use (NAICS 31-33, 336, 3361 to 3363).

**Suppressed, censored or masked values.** Cells that would reveal one
employer are suppressed (`disclosure_code` "N", employment shown as zero). In
small Michigan counties, auto-industry cells are often suppressed. We report
suppressed cells as suppressed, never as zero, and use the next level up
(manufacturing total) where the detail is hidden. Michigan counties with a
suppressed transportation equipment (NAICS 336) cell: 34 of 66 in Q1 2026. For
manufacturing (NAICS 31-33), 4 of 83. County exposure therefore uses the
manufacturing share of all jobs.

**Missing data.** Suppression is the main gap; see above.

**Revisions.** Revised for up to four quarters, then final.

**Units and rounding.** Jobs, whole numbers; place of work.

**Known quirks.** Place of work, like CES. A county's auto employment share
says where the plants are, not where their workers live. Workers commute
across county lines, so exposure by county is approximate.

**Uncertainty.** No sampling error (it is a census). Misreported industry or
location codes for multi-site employers are the main error source.

**License and attribution.** Public domain. `U.S. Bureau of Labor Statistics
(QCEW)`.

## U.S. international trade by state (U.S. Census Bureau)

**What it is.** Monthly dollar value of goods exports from and imports to each
state, by trading partner country.

**Where it comes from.** Census International Trade API,
`https://api.census.gov/data/timeseries/intltrade/exports/statehs` (field
`ALL_VAL_MO`) and `.../imports/statehs` (field `GEN_VAL_MO`), key
`CENSUS_API_KEY`. Partner codes: Canada 1220, Mexico 2010, all countries
"-". U.S. totals for comparison come from `.../exports/hs` and
`.../imports/hs` with the same fields. Cached in `data/trade/mi_trade.csv`
(column `geo` is MI or US).

**Version and vintage.** Pulled November 2, 2026, through August 2026.
Monthly figures are revised with the annual revision each June.

**Coverage.** Goods only, not services. Nominal dollars, not adjusted for
prices or seasons. State export data based on ZIP codes begin January 2006.

**Changes over time.** None that affect 2023 to 2026.

**Suppressed, censored or masked values.** None at the state-by-country total.

**Missing data.** None: every month January 2022 to August 2026 is present for
Canada, Mexico and the world total, both flows.

**Revisions.** Annual. We refresh the whole series each pull.

**Units and rounding.** Dollars. Not inflation-adjusted, so compare the same
months a year apart and say "in dollars".

**Known quirks.** Exports are by "origin of movement", the state where goods
start their trip to the port, which can be a consolidation point rather than
where they were made. Imports are by "state of destination" as known when the
entry is filed, which may not be where goods are used. Census advises against
computing state trade balances from the two. Sources:
`https://www2.census.gov/programs-surveys/trade/aip/elom.html`,
`https://www2.census.gov/programs-surveys/trade/aip/state_import_FAQ.html`.
Auto parts can cross the Michigan-Ontario border several times before final
assembly, so trade values count some parts more than once.

**Uncertainty.** Census publishes no sampling error (administrative records);
the main error is misreported state of origin.

**License and attribution.** Public domain. `U.S. Census Bureau, International
Trade`.

## Tariff measures affecting U.S.-Canada trade (U.S. and Canadian government notices)

**What it is.** Dates, rates and covered goods for U.S. and Canadian tariff
measures since January 2025. Kept in `docs/TARIFF-TIMELINE.md`, every row
linked to a primary source (Federal Register, CBP, Supreme Court, Department
of Finance Canada, Canada Gazette).

**Known quirks.** Measures changed often, some were struck down or refunded,
and USMCA-qualifying goods were treated differently at each stage. Use
effective dates, not announcement dates. Rows without a primary source are
listed as unconfirmed and are not used in the post.

**License and attribution.** Government works; cite each notice.
