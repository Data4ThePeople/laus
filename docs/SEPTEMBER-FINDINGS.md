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
| sep26-01-septembers.png | chart_septembers.py | U.S. share in Structural Loss, every September 2012 to 2026 (beat 1, per Eric) |
| sep26-01-structural-loss-over-time.png | chart_structural_loss.py --out | Monthly series, 2010 to Sep 2026; not used in beat 1 |
| sep26-02-mi-county-map.png | chart_michigan.py | 20 entered, 33 already, 30 not |
| sep26-03-mi-labor-force-jobs.png | chart_michigan.py | MI labor force -4.9% vs payroll jobs +0.2% since Jan 2025, SA |
| sep26-04-mi-canada-share.png | chart_michigan.py | Canada's share of MI vs U.S. trade |

Beat 1 shows only the last 15 Septembers (Eric, Nov 2, 2026). Tariff piece shelved for now (Eric, Nov 2, 2026).

Framing (Eric, Nov 2, 2026): the gap between the labor force and job counts
is called out as something to keep an eye on, not explained.

## Open questions

- Whether the rest-of-Michigan decline survives the early-2027 revision.
- QCEW county manufacturing exposure vs labor force change (data cached,
  not yet run).
