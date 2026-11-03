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
and the annual revision at the start of each calendar year re-estimates up to
five prior years at once (published with the January data, usually in March). The
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

**Revisions.** BLS revises history. At the beginning of each calendar year
BLS revises up to five years of previous data ("in most years", per the LAUS
technical note), so the revision expected in early 2027 would re-estimate 2022
through 2026, including every 2025 and 2026 month used here. A county can
cross a band boundary in a revision without anything
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
Classification uses the unrounded percent change, so a county at -10.001%
is Structural Loss even though it prints as "-10.0%" at one decimal (Emmet
and Genesee, MI, in September 2025; Ross, OH, and Bee, TX, in September
2026). About 46 counties sat within a quarter point of the line in September
2026, so the national count is sensitive to revisions. The classified
universe includes Puerto Rico's 78 municipios; in September 2026, 38 of them
were in Structural Loss.

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

**Substate model areas.** In five states BLS models one large metro area and
the balance of the state separately, each controlled to the state total
(LAUS technical note, https://www.bls.gov/news.release/laus.tn.htm). The
five metros are Chicago, Cleveland, Detroit-Warren-Dearborn, Miami and
Seattle. In Michigan, counties outside the Detroit-Warren-Dearborn MSA
(Lapeer, Livingston, Macomb, Oakland, St. Clair, Wayne) are shares of the
balance-of-Michigan estimate, published as `LAUBS260000000000006`
(2,867,651 in September 2025, 2,617,302 in September 2026). The six-county
sum matches the published MSA series `LAUMT261982000000006` within one
person. For a Michigan county outside the Detroit metro, compare its change
with the balance-of-Michigan series, not the statewide one. Ohio works the
same way: the Cleveland MSA (Ashtabula, Cuyahoga, Geauga, Lake, Lorain,
Medina; CBSA 17410) and the other 82 Ohio counties, published as
`LAUBS390000000000006` (county sum 4,744,759 against 4,744,760 in September
2026).

**State employed residents.** For the survey check, `scripts/cps_quality.py`
pulls `LAUST<ff>0000000000005` (employed residents, not seasonally adjusted)
for the 50 states and DC, and `LNU02000000` (U.S. CPS employment, not
seasonally adjusted), 2012 to September 2026, into
`data/ces/laus_employed_nsa.csv`. Quarterly values are the average of the
quarter's three months; a quarter missing a month (Q4 2025, because of the
October 2025 gap) is dropped. LAUS state estimates are models that use the
CPS, payroll survey counts and unemployment insurance claims as inputs, so
they are not pure survey readings. The seasonally adjusted series moves
differently: Michigan employed residents fell 2.0% (not adjusted) and 1.3%
(adjusted) from January 2025 to January 2026. Compare like with like.

## Quarterly Census of Employment and Wages, state totals (U.S. Bureau of Labor Statistics)

**What it is.** Jobs at every employer covered by unemployment insurance, for
each month of each quarter. We use the state and U.S. totals: all ownerships
(`own_code` 0), all industries, `agglvl_code` 50 (state) and 10 (U.S.).

**Where it comes from.** QCEW open data CSV files, one per quarter,
`https://data.bls.gov/cew/data/api/<year>/<qtr>/industry/10.csv`. No key; the
same browser-like User-Agent as LAUS. `scripts/cps_quality.py` keeps only the
state and U.S. rows, in `data/qcew/state_total/qcew_states.csv`.

**Version and vintage.** Pulled November 3, 2026. 2014 Q1 to 2026 Q1; the
open data files start in 2014, and Q2 2026 was not yet posted. About five to
six months behind.

**Coverage.** Over 95% of U.S. jobs. It is a full count from tax filings, not
a sample. Excludes the self-employed, most farm workers, some religious
workers and military.

**Changes over time.** None that affect state totals.

**Suppressed, censored or masked values.** None at the state total level.

**Missing data.** None for the quarters used.

**Revisions.** Revised for up to four quarters, then final. 2025 and 2026
quarters can still change.

**Units and rounding.** Jobs, whole numbers, by place of work. Quarterly value
is the average of the three monthly counts.

**Known quirks.** Counts jobs where they are, not people where they live. A
person with two covered jobs counts twice; a self-employed person not at
all; cross-state commuters count in the state where they work. These
differences usually move slowly, so the one-year change in QCEW jobs and in
LAUS employed residents usually stays within about a point. The comparison
is one-year change against one-year change, same quarter, never levels.

**Uncertainty.** No sampling error (it is a census). Misreported location
codes for multi-site employers are the main error source.

**License and attribution.** Public domain. `U.S. Bureau of Labor Statistics
(QCEW)`.

## Current Employment Statistics, state payroll jobs (U.S. Bureau of Labor Statistics)

**What it is.** Monthly estimate of payroll jobs at employers in each state,
from a sample survey of employers. We use total nonfarm, not seasonally
adjusted, only for the months QCEW does not yet cover.

**Where it comes from.** BLS public API v2, key `BLS_API_KEY`. Series
`SMU<ff>000000000000001` for the 50 states and DC and `CEU0000000001` for the
U.S., 2014 to September 2026, cached in `data/ces/ces_states_nsa.csv` by
`scripts/cps_quality.py`.

**Version and vintage.** Pulled November 3, 2026. September 2026 is
preliminary. Data through September 2025 have been benchmarked to QCEW.

**Coverage.** Nonfarm payroll jobs by place of work. Excludes the
self-employed, farm workers and private household workers. Counts jobs, not
people.

**Changes over time.** Annual benchmark to QCEW each March, which replaces
earlier estimates for the prior year and more.

**Suppressed, censored or masked values.** None at the state total level.

**Missing data.** None for the months used; CES has an October 2025 value
where LAUS does not.

**Revisions.** Revised the next month, again at the annual benchmark.
April to September 2026 will be benchmarked to QCEW in early 2027.

**Units and rounding.** Thousands of jobs, one decimal. Only one-year percent
changes are used.

**Known quirks.** How we combine it with QCEW: for each state and month we
use the gap against QCEW where QCEW is published (through March 2026) and
the gap against CES after that (`data/ces/state_gaps_monthly.csv`, column
`source`). Across states, the CES one-year change has differed from QCEW's
by 0.07 to 0.21 points on average in each year 2015 to 2024, up to 0.46 in
late 2025 and 0.36 to 0.39 in January to March 2026. In Michigan, CES ran
below QCEW in early 2026 (January to March: CES -0.04% to -0.21%, QCEW
+0.29% to +0.92%), so using CES here, if anything, makes Michigan's gap
smaller, not larger.

**Uncertainty.** BLS publishes sampling error for state CES estimates; we do
not use it. Treat the April to September 2026 gaps as provisional until
QCEW is out.

**License and attribution.** Public domain. `U.S. Bureau of Labor Statistics
(CES)`.
