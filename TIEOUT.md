# Tie-out: September 2026 update

Claude's own tie-out, November 3, 2026. Numbers come from
`scripts/tieout_september.py`, which re-derives Structural Loss from the raw
county panel and cross-checks against series pulled fresh from the BLS and
Census APIs. Words were checked by hand against the source named in each row.
Verdicts: supported / partly / not / could not check.

The post draft does not exist yet, so this checks the six beats agreed on
November 2 and 3 and the four charts.

## Numbers

| Beat | Claim | Check | Result | Verdict |
|---|---|---|---|---|
| 1 | Sep 2026: 1,132 of 3,214 counties in SL (35.2%) | Re-derived from raw panel, strict < -10% | 1,132 of 3,214; classified file agrees | supported |
| 1 | Sep 2025: 1,091 of 3,207 (34.0%) | Same | 1,091 of 3,207 | supported |
| 1 | Up 40 on the same counties (129 entered, 89 left) | 3,207 common counties | 129, 89, net 40 (1,091 to 1,131) | supported |
| 1 | 7 counties in Sep 2026 only | Universe diff | 22051, 22071, 22075, 22087, 22089, 22095, 22103 (Katrina parishes); none in Sep 2025 only | supported |
| 1 | Third-highest September; 2022 36.2%, 2021 35.5% | All Septembers 2010 to 2026 | Rank 3 | supported |
| 1 | Chart bar values 2012 to 2026 | Recomputed | All 15 match the chart labels | supported |
| 2 | Michigan: 20 entered, 0 left | Common counties | 20, 0 | supported |
| 2 | 53 of 83 in SL, up from 33 | Same | 53, 33, 83 | supported |
| 2 | Next: MN +10, OK +9, TN +9 | Net by state | MI 20, MN 10, OK 9, TN 9, IA 7 | supported |
| 3 | MI labor force -4.7% (5,029,694 to 4,791,578) | Published `LAUST260000000000006`, fresh API | -4.734% | supported |
| 3 | Largest drop of any state | All 50 states + DC, fresh API | MI -4.7%, AZ -4.0%, VT -2.9% | supported |
| 3 | U.S. -0.5% | `LNU01000000` | -0.5% | supported |
| 3 | Neighbors fell 0.3% to 1.5%; WI rose | OH -1.2, IL -1.4, MN -1.5, IN -0.3, WI +2.6 | Within range | supported. Findings doc had AZ -4.1% and OH -1.3%; published series give -4.0% and -1.2%. Findings doc corrected. |
| 3 | 19 of 20 fell faster than the state | Entrant yoy vs state yoy | 19 of 20 | supported |
| 3 | None crossed on the 20-year base change alone | Sep 2025 level vs Sep 2006 base | 0 | supported |
| 3 | County sums match the state | 83 counties summed | 4,791,575 vs 4,791,578 (rounding) | supported |
| 3 | County values match BLS | Muskegon, Calhoun, Jackson, Berrien via API | Exact match, both months | supported |
| 4 | Six Detroit metro counties +0.6% | Panel | +0.6% | supported |
| 4 | Six counties are the Detroit-Warren-Dearborn MSA | Six-county sum vs published MSA series `LAUMT261982000000006` | 2,162,043 vs 2,162,044; 2,174,275 vs 2,174,276 | supported |
| 4 | Other 77 counties -8.7% (2,867,647 to 2,617,300) | Panel | Same | supported |
| 4 | Rest of state -3.6% Jan, -6.6% Apr, -8.7% Sep | Panel, same month yoy | Same | supported |
| 4 | Median county -8.6% | Panel | -8.6% | supported |
| 5 | Payroll jobs +0.04%, manufacturing -0.3% (Sep yoy, SA) | Cache vs fresh API | +0.04%, -0.27% both | supported |
| 5 | Chart: labor force -4.9%, jobs +0.2% since Jan 2025, SA | Cache vs fresh API | -4.89%, +0.22% | supported |
| 5 | Chart: no labor force estimate Oct 2025 | Cache | Missing in LAUS SA, present in CES | supported |
| 6 | Canada share Jan to Aug 2026: MI exports 38.8%, US 14.3%; MI imports 25.5%, US 11.2% | Cache, all 8 months present | Same | supported |
| 6 | Trade cache matches Census | Aug 2026 MI exports and imports to Canada, fresh API | Exact match | supported |

## Words

| Where | Text | Source | Verdict |
|---|---|---|---|
| Beat 4 | BLS estimates the Detroit metro and the rest of Michigan with separate models | LAUS technical note: Detroit-Warren-Dearborn "and their respective balances of state are produced using a similar model-based approach" | supported |
| Beat 5 | BLS re-estimates the 2026 state figures in early 2027 | Technical note: "In most years, historical data for the most recent five years are revised near the beginning of each calendar year" | supported with "usually" (fixed in findings Nov 3) |
| Chart 1 | "Structural labor force loss, every September since 2012"; "more than 10% below the same month 20 years earlier" | Method (strict < -10%) | supported |
| Chart 2 | "Michigan: 20 counties fell into structural loss in a year"; "53 of 83 are now in structural loss, up from 33" | Numbers above | supported |
| Chart 2 | Labels Muskegon, Berrien, Calhoun, Jackson | Four largest entrants by labor force | supported |
| Chart 3 | "Michigan's labor force is falling. Its job count is not." | -4.9% vs +0.2% since Jan 2025 | supported; 2026 values are preliminary |
| Chart 3 | "Labor force counts residents working or looking for work. Payroll jobs count positions at Michigan employers." | DATASETS.md, CES and LAUS sections | supported |
| Chart 4 | "Michigan trades with Canada far more than the nation does" | Shares are 38.8% vs 14.3%; in dollars the U.S. trades far more with Canada than Michigan does | fixed Nov 3: title now "Canada is a far bigger share of Michigan's trade than the nation's" | 

## Flags for Eric

1. **Two Michigan labor force drops.** Beat 3 uses the unadjusted series, Sep to Sep: -4.7%, matching the county data. Chart 3 uses the seasonally adjusted series from Jan 2025: -4.9%. On the seasonally adjusted series, Sep to Sep is -3.6%. BLS smooths the adjusted state series, and the two do not move in step. Each number is right for its series; the post should name which one it is using. Recorded in the findings doc Nov 3.
2. **Chart 4 title**: fixed Nov 3.
3. **Revision wording**: fixed Nov 3.
