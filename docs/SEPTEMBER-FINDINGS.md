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
- Every month of 2026 so far is above the same month of 2025. The gap
  narrowed from 3.6 points in July (39.8% vs 36.2%) to 1.2 points in
  September (35.2% vs 34.0%).
- October 2025 shows 50% but covers only Puerto Rico's 78 municipios (the
  shutdown gap). Exclude it from any "record" statement.

## Michigan

- Michigan accounts for 20 of the 40 net new Structural Loss counties: 20
  entered, none left. 53 of 83 Michigan counties are now in Structural Loss,
  up from 33.
- Michigan's labor force fell 4.7% from September 2025 to September 2026
  (5,029,694 to 4,791,578 in the BLS statewide series), the largest drop of
  any state. Next: Arizona (-4.1%). Neighbors: Ohio -1.3%, Illinois -1.4%,
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
  beginning of each calendar year (same technical note). The 2026 Michigan
  figures will be re-estimated in early 2027.

### Trade with Canada (Census, dollars, not inflation-adjusted)

| January to August | 2024 | 2025 | 2026 |
|---|---|---|---|
| Michigan exports to Canada | $16.74B | $15.67B (-6.4%) | $16.49B (+5.2%) |
| Michigan imports from Canada | $30.17B | $28.65B (-5.0%) | $29.07B (+1.5%) |
| Michigan exports to Mexico | $11.43B | $11.01B (-3.7%) | $12.83B (+16.5%) |

- Trade with Canada fell in 2025 and partly recovered in 2026. The labor force
  decline is a 2026 event. The two do not line up in time.
- Tariff dates and rates: `docs/TARIFF-TIMELINE.md` (in progress).

## Open questions

- Whether the rest-of-Michigan decline survives the early-2027 revision.
- QCEW county manufacturing exposure vs labor force change (data cached,
  not yet run).
