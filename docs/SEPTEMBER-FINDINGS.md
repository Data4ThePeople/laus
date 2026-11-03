# September 2026 update: findings so far

Working notes for Step 1 of the september-update post. Every figure is
recomputed from `data/*.parquet` and the caches in `data/ces`, `data/qcew` and
`data/trade` (pulled November 2, 2026). Not yet tied out.

## National

- September 2026: 1,132 of 3,214 counties in Structural Loss (35.2%).
- September 2025: 1,091 of 3,207 (34.0%). On the 3,207 counties with data in
  both months, the count rose by 40 (129 entered, 89 left). The seven
  New Orleans-area parishes are in the 2026 universe but not 2025 (Katrina
  coverage gap).
- Not a September record: 2022 (36.2%) and 2021 (35.5%) were higher.
  September 2026 is the third-highest September since the series starts in
  2010.
- Not in the post (Eric, Nov 3, 2026): the July 2026 all-time monthly
  record (39.8%) and the month-by-month 2026 vs 2025 gap. Beat 1 compares
  Septembers only.
- October 2025 shows 50% but covers only Puerto Rico's 78 municipios (the
  shutdown gap). Exclude it from any "record" statement.

## Michigan

- Michigan accounts for 20 of the 40 net new Structural Loss counties: 20
  entered, none left. 53 of 83 Michigan counties are now in Structural Loss,
  up from 33.
- Michigan's labor force fell 4.7% from September 2025 to September 2026
  (5,029,694 to 4,791,578 in the BLS statewide series), the largest drop of
  any state. Next: Arizona (-4.0%). Neighbors: Ohio -1.2%, Illinois -1.4%,
  Minnesota -1.5%, Indiana -0.3%, Wisconsin +2.6%. U.S.: -0.5%.
- The flips are not a 20-year-base effect: none of the 20 would have crossed
  -10% on the change in the 2006 base month alone. 19 of 20 fell faster
  than the state.

### The drop is split in two, along the line of BLS's estimation models

- BLS estimates the Detroit-Warren-Dearborn metro area and the "balance of
  Michigan" with separate models, both controlled to the state total
  (LAUS technical note, https://www.bls.gov/news.release/laus.tn.htm).
- The six Detroit metro counties (Wayne, Oakland, Macomb, Livingston, Lapeer,
  St. Clair) each rose 0.4% to 0.6%; together +0.6%.
- The other 77 counties together fell 8.7% (2,867,647 to 2,617,300). The
  median Michigan county fell 8.6%. 76 of 83 counties fell more than 3%.
  Manufacturing counties and northern tourism counties fell by about the
  same amount.
- The rest-of-state decline widened through the year: -3.6% in January,
  -6.6% in April, -8.7% in September (each versus the same month of 2025).

### Other data does not show a drop of that size

- Payroll jobs located in Michigan (CES, seasonally adjusted), September
  2025 to September 2026: total +0.04%, manufacturing -0.3%. Transportation
  equipment manufacturing (not seasonally adjusted) +0.4%.
- QCEW, a full count of jobs from unemployment insurance tax records, runs
  only through March 2026. March 2025 to March 2026: Michigan +0.1%
  (4,166,401 to 4,170,449); Detroit metro -0.2%; rest of Michigan +0.4%.
  Over the same months, LAUS labor force: Detroit metro +0.2%, rest of
  Michigan -4.9%; LAUS employed residents statewide -2.4% (4,779,337 to
  4,666,224). CES total nonfarm, March: -0.2%.
- Household survey side of LAUS: employed Michigan residents fell from
  4,797,679 to 4,559,610 (-5.0%); unemployed were flat (232,015 to 231,968);
  unemployment rate 4.6% to 4.8%.
- LAUS state data for the most recent five years are revised near the
  beginning of each calendar year "in most years" (same technical note). Post
  wording: BLS usually revises the 2026 figures in early 2027.
- Which series each number uses (say so in the post): the -4.7% one-year drop
  is the unadjusted statewide series, September to September, matching the
  county data. The jobs chart uses the seasonally adjusted series from January
  2025 (-4.9%). On the adjusted series, September to September is -3.6%; BLS
  smooths the adjusted state series, so the two do not move in step.

### Trade with Canada (Census, dollars, not inflation-adjusted)

| January to August | 2024 | 2025 | 2026 |
|---|---|---|---|
| Michigan exports to Canada | $16.74B | $15.67B (-6.4%) | $16.49B (+5.2%) |
| Michigan imports from Canada | $30.17B | $28.65B (-5.0%) | $29.07B (+1.5%) |
| Michigan exports to Mexico | $11.43B | $11.01B (-3.7%) | $12.83B (+16.5%) |

- Trade with Canada fell in 2025 and partly recovered in 2026. The labor force
  decline is a 2026 event. The two do not line up in time.
- Tariff dates and rates: `docs/TARIFF-TIMELINE.md` (32 rows, each linked
  to a primary source; uncertain items listed separately).
- The newest measures sit at or past the edge of the trade data, which ends
  in August 2026: U.S. Section 338 duties of 50% on listed Canadian goods
  from August 22, 2026 (applying regardless of USMCA origin, per the White
  House), the motor vehicle list stacking on Section 232 from September 15,
  an import ban from September 29, a new product list from October 30, and
  Canada's new tariffs and 50% steel and aluminum surtaxes from September 8,
  2026. Their effect on Michigan trade is not yet in any published data.
- Wording: the Section 338 proclamation titles characterize Canada's
  conduct. Cite them by number, not title.

### How much Michigan relies on Canada (January to August 2026, dollars)

- Canada took 38.8% of Michigan's goods exports, against 14.3% for the U.S.
  as a whole.
- Canada supplied 25.5% of Michigan's goods imports, against 11.2% for the U.S.

## Charts (outputs/charts/, rebuilt by scripts)

| File | Script | What it shows |
|---|---|---|
| sep26-01-septembers.png | chart_septembers.py | Share of U.S. counties and Puerto Rico municipios in Structural Loss, every September 2012 to 2026 (beat 1, per Eric) |
| sep26-01-structural-loss-over-time.png | chart_structural_loss.py --out | Monthly series, 2010 to Sep 2026; not used in beat 1 |
| sep26-02-mi-county-map.png | chart_michigan.py | 20 entered, 33 already, 30 not |
| sep26-03-mi-labor-force-jobs.png | chart_michigan.py | MI employed residents -4.5% vs payroll jobs +0.2% since Jan 2025, SA (switched from labor force Nov 3, per Eric) |
| sep26-04-mi-canada-share.png | chart_michigan.py | Canada's share of MI vs U.S. trade; not in the post (Eric, Nov 3: the last section becomes his close) |
| sep26-05-mi-vs-neighbors.png | chart_michigan.py | One-year labor force change, MI, neighbors, U.S. (added Nov 3, per Eric) |
| sep26-06-mi-detroit-vs-rest.png | chart_michigan.py | Detroit metro vs rest of MI, monthly yoy, 2026 (rest eased to about -7% in Jul and Aug) |
| sep26-07-mi-participation.png | chart_michigan.py | Participation rate, MI, OH, U.S., SA, Jan 2024 to Sep 2026 |
| sep26-08-mi-oh-balance-of-state.png | chart_michigan.py | Rest of MI (outside Detroit, 77 counties) vs rest of OH (outside Cleveland, 82 counties), monthly yoy, 2026. Replaced the outside-500k+-metros chart Nov 3, per Eric, because Michigan's other metros fell as much as its rural counties |
| sep26-09-septembers-bands.png | chart_septembers_bands.py | All six bands, share of counties, every September 2012 to 2026 (added Nov 3, per Eric) |

Beat 1 shows only the last 15 Septembers (Eric, Nov 2, 2026). Tariff piece shelved for now (Eric, Nov 2, 2026).

Framing (Eric, Nov 2, 2026): the gap between the labor force and job counts
is called out as something to keep an eye on, not explained.

## Open questions

- Whether the rest-of-Michigan decline survives the early-2027 revision.
- QCEW county manufacturing exposure vs labor force change (data cached,
  not yet run).

## Participation and age (Nov 3, 2026)

Decision (Eric, Nov 3, 2026, after the second independent tie-out), beat 5:
- Lead with the published LAUS participation rate: 60.8% to 58.5%.
- CPS statewide direction: adult population held steady, participation fell
  (61.4% to 58.2%, January to September averages). Say confidence is lower
  because the Michigan sample is small.
- Census population estimates: aging lowers the labor force roughly 0.5% to
  1% a year, too slow to explain the drop.
- Left out: prime-age participation outside Detroit (inside the margin of
  error), Detroit vs rest in the CPS (cannot be told apart), and the CPS
  age-mix split (likely sample noise).
Script: `scripts/cps_michigan.py`. The CPS "Detroit" group is Wayne, Oakland,
Macomb and Livingston only (St. Clair and Lapeer are not identified in CPS).

Eric's question: is the drop fewer prime-age workers?

- **LAUS statewide participation** (seasonally adjusted, `LASST260000000000008`):
  Michigan 60.8% in Sep 2025 to 58.5% in Sep 2026 (-2.3 points). Ohio 62.3%
  to 61.2%; U.S. 62.5% to 61.8%. The labor force divided by the participation
  rate gives a 16+ population that rose slightly, so the drop is in
  participation, not in the number of adults.
- **CPS microdata for Michigan** (Census API `cps/basic`, composite weight
  `PWCMPWGT`, January to September averages): participation 61.4% (2025) to
  58.2% (2026). Weighted 16+ population 8.23 million to 8.24 million.
  - The CPS weights control Michigan's total adult population, not its age
    mix, so the age mix within the state comes from the sample and swings
    month to month (prime-age weighted count ranges 3.50 to 3.96 million).
  - Shift-share on those averages: the older age mix accounts for -1.3
    points, lower participation within age groups for -1.9 points. Given
    the sample, treat the split as rough.
  - Prime age (25-54), outside Wayne, Oakland, Macomb and Livingston:
    participation 85.8% to 83.3%. In those four counties: 83.0% to 81.5%.
  - Sample size: about 1,570 Michigan people age 16+ per month in 2026,
    down from about 1,670 in 2025 and 1,800 in 2024.
- **Census population estimates** (Vintage 2025, `cc-est2025-alldata-26.csv`,
  July 1 each year, through 2025):
  - Prime-age population in Michigan rose 0.6% in each of 2024 and 2025.
  - In the 20 counties that entered Structural Loss: prime age 477,800
    (2024) to 479,300 (2025); 65+ share of adults rose 29.3% to 29.9%.
    The 65+ share has risen about 0.6 points a year since 2020 in each group
    of counties (20 entrants, Detroit 6, rest).
  - Aging at that pace lowers the labor force by roughly 0.5% to 1% a year (0.6 points moving from groups with about 60% to 85% participation to one with about 15%). It
    does not produce an 8.7% one-year drop. No 2026 estimate exists yet.
- LAUS publishes no county population or participation rate. County
  participation for 2026 cannot be computed.

### Statewide prime-age participation (Nov 3, 2026)

- CPS, January to September averages, Michigan, ages 25 to 54: 84.6% (2025)
  to 82.5% (2026), -2.1 points. About 713 and 625 people a month.
- Household-cluster bootstrap SE 1.0 (z 2.15). With an assumed design
  effect of 1.5 to 2.0 for geographic clustering, SE 1.2 to 1.4 (z 1.75 to
  1.5). Script: `scripts/cps_prime_age_error.py`.
- Reading: close to the margin of error. It can be stated as "the survey
  suggests", not as a measured decline.

### Michigan vs Ohio outside the big metros (Nov 3, 2026)

Script: `scripts/cps_mi_oh.py`. County lists from the OMB 2023 delineation
(`data/geo_ref/omb_cbsa_2023.csv`). "Outside 500k+ metros": Michigan drops
Detroit and Grand Rapids; Ohio drops Cleveland, Columbus, Cincinnati, Dayton,
Akron and Toledo (Akron is in the same CPS size class as Dayton and Toledo
and cannot be separated). CPS uses its own metro-size and metro-status codes.

LAUS labor force, change from the same month of 2025:

| Area | Counties | Jan | Apr | Sep |
|---|---|---|---|---|
| Michigan outside 500k+ metros | 72 | -3.5% | -6.6% | -8.7% |
| Ohio outside 500k+ metros | 59 | -1.5% | -1.5% | -1.2% |
| Michigan nonmetro | 53 | -3.6% | -6.1% | -8.3% |
| Ohio nonmetro | 47 | -1.7% | -1.2% | -0.9% |

CPS participation, January to September averages (change in points; z =
change / household-bootstrap SE; second z assumes a design effect of 2.0):

| Area | Ages | 2025 | 2026 | Change | z |
|---|---|---|---|---|---|
| Michigan outside 500k+ metros | 16+ | 59.2% | 54.6% | -4.6 | 3.0 / 2.1 |
| Ohio outside 500k+ metros | 16+ | 61.3% | 60.0% | -1.4 | 1.0 / 0.7 |
| Michigan outside 500k+ metros | 25-54 | 84.6% | 82.4% | -2.2 | 1.3 / 0.9 |
| Ohio outside 500k+ metros | 25-54 | 82.1% | 82.4% | +0.3 | 0.2 / 0.1 |

- The LAUS gap between the two states outside the big metros is large
  (Michigan -8.7%, Ohio -1.2% in September).
- In the CPS, Michigan's all-adult drop outside the big metros clears the
  error on its own; Ohio's does not. The difference between the two states
  (-3.2 points) is about 1.6 times its error, so not clearly beyond it.
  Part of any all-adult change can come from the sample's age mix.
- Prime age: neither state's change is distinguishable from zero outside
  the big metros. Nonmetro CPS samples are too small to use (about 110
  prime-age Michiganders a month).

### Chart 8 reframed: balance of state (Nov 3, 2026)

The third independent tie-out found that Michigan's other metro areas fell
about as much as its rural counties (Sep yoy: Grand Rapids -8.8%, Lansing
-10.2%, Kalamazoo -9.2%, Flint -8.7%, Ann Arbor -8.4%), while Ohio's six
500k+ metros fell 0.5% to 2.3%. The "outside the big metros" chart implied a
small-place story the data does not support. Eric chose to replace it with
the two BLS balance-of-state areas (MI outside Detroit -8.7%, OH outside
Cleveland -1.4% in September) and to add the metro sentence. The 500k+
grouping table above is kept as exploration only.

### Employed residents vs payroll jobs: how unusual is the gap? (Nov 3, 2026)

Eric's question: how can employed residents fall while payroll jobs do not?
Script: `scripts/employed_vs_payroll.py`. One-year change, SA, September 2026:

| State | Employed residents (LAUS) | Payroll jobs (CES) | Gap, points |
|---|---|---|---|
| Connecticut | -3.6% | +0.9% | -4.5 |
| Arizona | -3.7% | +0.6% | -4.2 |
| Michigan | -3.6% | +0.0% | -3.7 |
| New Mexico | -2.2% | +1.3% | -3.5 |
| Minnesota | -2.2% | +1.2% | -3.4 |

- 17 states have a gap of 2 points or more in Sep 2026; 12 in Sep 2022; 0 to 2
  in every other September 2015 to 2025 (2020 skipped). Median state gap -1.2.
- Michigan's gap widened every month of 2026, from -1.3 in January to -3.7
  in September. Its only larger gap since 1991 was May 2021 (-4.4).
- Of 21,828 state-months since 1991, 0.26% have a gap at or below -4.5.
- U.S.: CPS employment -0.3%, CES payroll +0.3% (Sep 2026).
- QCEW (tax-record count), Michigan, all jobs: Jan 2026 +0.9%, Feb +0.5%,
  Mar +0.3% from a year earlier (Q2 2026 not posted). LAUS employed residents
  in the same months: -1.3%, -1.4%, -1.6%.
- Reading: the concept differences (residence vs workplace, people vs jobs,
  self-employed, multiple jobs, commuters) usually keep the two within about
  a point a year. They do not plausibly cover about 175,000 people. The
  household side (LAUS, which leans on the CPS) is weak in many states in
  2026; the employer side and the tax records are not. Which is closer to
  right will not be known until revisions; 2022's gaps did not all close.

