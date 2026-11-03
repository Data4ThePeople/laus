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
with the balance-of-Michigan series, not the statewide one.

## Current Employment Statistics, state payroll jobs (U.S. Bureau of Labor Statistics)

**What it is.** Monthly count of payroll jobs at employers located in a state,
by industry. One cell is thousands of jobs in a state, industry and month.

**Where it comes from.** BLS public API v2 (`api.bls.gov`), key
`BLS_API_KEY`. Series used: `SMS26000000000000001` (Michigan total nonfarm,
seasonally adjusted), `SMS26000003000000001` (Michigan manufacturing,
seasonally adjusted), `SMU26000003133600001` (Michigan transportation
equipment manufacturing, NAICS 336, not seasonally adjusted), plus U.S.
totals `CES0000000001` and `CES3000000001`. The same cache holds two LAUS
statewide series for Michigan, seasonally adjusted, stored in thousands:
`LASST260000000000005` (employed residents), which the jobs chart compares
with CES total nonfarm, and `LASST260000000000006` (labor force). The chart
uses employed residents rather than the labor force because payroll jobs
cannot include unemployed people; employed residents and payroll jobs are
the two employment measures BLS publishes side by side for states. The cache
also holds statewide labor force, not seasonally adjusted, for Michigan,
Ohio, Illinois, Minnesota, Indiana and Wisconsin (`LAUST<fips>0000000000006`,
thousands) and the U.S. CPS labor force `LNU01000000` (already in
thousands), for the state comparison chart; and participation rates,
seasonally adjusted, in percent: `LASST260000000000008` (Michigan),
`LASST390000000000008` (Ohio) and `LNS11300000` (U.S.). The rates have no
October 2025 value. Cached in
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

## Current Population Survey microdata, Michigan (U.S. Census Bureau for BLS)

**What it is.** The monthly household survey behind the national unemployment
rate and the main input to the LAUS state model. One row per person
interviewed: age (`PRTAGE`), labor force status (`PEMLR`: 1-2 employed, 3-4
unemployed, 5-7 not in the labor force) and the composite weight
(`PWCMPWGT`) that BLS uses for official labor force figures.

**Where it comes from.** Census API, `https://api.census.gov/data/<year>/cps/basic/<mon>`,
key `CENSUS_API_KEY`, Michigan only, pulled by `scripts/cps_michigan.py`
into `data/cps/mi_cps.csv`. January to September of 2024, 2025 and 2026.

**Version and vintage.** Pulled November 3, 2026. Microdata are not revised;
the weights reflect the population controls in force each January.

**Coverage.** Civilian, noninstitutional, age 16 and over. About 1,570
Michigan adults a month in 2026, down from about 1,670 in 2025 and 1,800
in 2024. People stay in the sample for several months in a row, so pooling
nine months does not give nine times as many separate people.

**Changes over time.** New population controls each January change the
weights. The weights hold Michigan's total adult population to the control,
not its age mix, so the age mix within Michigan comes from the sample and
moves month to month.

**Suppressed, censored or masked values.** Counties are identified only where
the population is large enough, and identification changes over the period:
in Michigan, Monroe and Calhoun have far fewer identified people in 2026 than
in early 2025, Cass appears only from August 2025, and Livingston's
identified sample falls from about 30 to 45 people a month to about 15 to
27. Among the Detroit metro counties, Wayne, Oakland, Macomb and Livingston
are identified in every month; St. Clair and Lapeer are not, so a CPS
"Detroit" group is those four counties and the rest-of-state group includes
St. Clair and Lapeer. The API returns county codes without leading zeros
("93", "99"); match them as numbers or zero-pad them, or Macomb and
Livingston drop out silently. Armed forces members (`PRPERTYP` 3) have
`PEMLR` -1 and fall out of the civilian universe.

**Missing data.** None for January to September in these years.

**Revisions.** None to microdata.

**Units and rounding.** Weighted people; rates computed from weighted sums.

**Known quirks.** This is the survey LAUS is built on, not an independent
check of it. Results tell us where in the survey a LAUS change shows up
(participation, age groups), not whether it is right.

**Uncertainty.** A state sample this size has wide error bars. The
independent tie-out (November 3, 2026) estimated the standard error of the
2025 to 2026 change in prime-age participation outside the Detroit group
(-2.5 points) at about 1.3 to 1.9 points, using a household-cluster bootstrap
plus an assumed design effect of 1.5 to 2.0 (an assumption, not a published
figure). The change is inside the 95% margin of error under every
assumption tried, and the difference between the Detroit group (-1.5) and
the rest (-2.5) is well inside it. The age-mix split is also unreliable:
the prime-age share fell almost 2 points in one year in the sample, faster
than Michigan's population ages, so most of that "age-mix effect" is likely
sample noise. Use the CPS only for the statewide direction (lower
participation, not fewer adults), at lower confidence than the published
LAUS figures. Use Census population estimates, not the CPS, for any
statement about aging.

**License and attribution.** Public domain. `U.S. Census Bureau, Current
Population Survey`.

## Population estimates by county and age (U.S. Census Bureau)

**What it is.** Estimated resident population on July 1 of each year, by
county, age group, sex, race and Hispanic origin. We use the total by
five-year age group.

**Where it comes from.** `https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/counties/asrh/cc-est2025-alldata-26.csv`
(Michigan), cached in `data/popest/`. No key.

**Version and vintage.** Vintage 2025, covering April 1, 2020 through July 1,
2025. Each new vintage revises every earlier year back to 2020. No 2026
estimate exists yet.

**Coverage.** Every Michigan county. Estimates, not counts: built from the
2020 Census base plus births, deaths and migration.

**Changes over time.** `YEAR` codes: 1 is the April 1, 2020 base, 2 to 7 are
July 1, 2020 to 2025. `AGEGRP` 0 is the total; 1 to 18 are five-year groups
(6 to 11 are ages 25 to 54; 14 to 18 are 65 and over).

**Suppressed, censored or masked values.** None.

**Missing data.** None.

**Revisions.** Every vintage. We use Vintage 2025 only.

**Units and rounding.** People.

**Known quirks.** Age groups are five-year bands, so "16 and over" cannot be
matched exactly; we use adults 20 and over as the base for shares.

**Uncertainty.** Census publishes no error bars for these estimates.
Migration is the least certain part, especially for recent years.

**License and attribution.** Public domain. `U.S. Census Bureau, Population
Estimates Program`.
