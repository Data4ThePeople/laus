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
| 5 | Chart: employed residents -4.5%, jobs +0.2% since Jan 2025, SA (chart switched from labor force Nov 3) | Cache `LASST260000000000005` and CES | -4.55%, +0.22% | supported; fresh API Nov 3: 4,803,978 to 4,585,469 (-4.55%), Oct 2025 missing, matches cache |
| 5 | Chart: no labor force estimate Oct 2025 | Cache | Missing in LAUS SA, present in CES | supported |
| 5 | MI participation 60.8% to 58.5% (Sep yoy, SA) | Fresh API `LASST260000000000008` | 60.8, 58.5 | supported |
| 5 | CPS Jan-Sep avg: 16+ population 8.23M to 8.24M; participation 61.4% to 58.2% | `scripts/cps_michigan.py`, Census CPS API | Same | supported (own computation; small sample) |
| 5 | CPS age mix -1.3 points, within age -1.9 points | Same | Same | supported as computed; rough given sample |
| 5 | CPS prime age outside Wayne, Oakland, Macomb, Livingston: 85.8% to 83.3% | Same; St. Clair and Lapeer have 0 identified records | Same | supported as computed; lower confidence |
| 5 | CPS sample about 1,570 people a month in 2026 (1,670 in 2025, 1,800 in 2024) | Same | 1,568.6; 1,667.4; 1,804.9 | supported |
| 6 | Canada share Jan to Aug 2026: MI exports 38.8%, US 14.3%; MI imports 25.5%, US 11.2% | Cache, all 8 months present | Same | supported |
| 6 | Trade cache matches Census | Aug 2026 MI exports and imports to Canada, fresh API | Exact match | supported |

## Words

| Where | Text | Source | Verdict |
|---|---|---|---|
| Beat 4 | BLS estimates the Detroit metro and the rest of Michigan with separate models | LAUS technical note: Detroit-Warren-Dearborn "and their respective balances of state are produced using a similar model-based approach" | supported |
| Beat 5 | BLS re-estimates the 2026 state figures in early 2027 | Technical note: "In most years, historical data for the most recent five years are revised near the beginning of each calendar year" | supported with "usually" (fixed in findings Nov 3) |
| Chart 1 | "Structural labor force loss, every September since 2012"; "Share of U.S. counties and Puerto Rico municipios ... more than 10% below the same month 20 years earlier" (relabeled Nov 3) | Method (strict < -10%); universe includes 78 PR municipios | supported |
| Chart 2 | "Michigan: 20 counties fell into structural loss in a year"; "53 of 83 are now in structural loss, up from 33" | Numbers above | supported |
| Chart 2 | Labels Muskegon, Berrien, Calhoun, Jackson | Four largest entrants by labor force | supported |
| Chart 3 | "Fewer Michiganders are working, but payroll jobs are not falling" (retitled Nov 3) | Employed residents -4.5%, payroll +0.2% since Jan 2025 | supported; 2026 values are model estimates, usually revised early 2027 |
| Chart 3 | "Employed residents counts people living in Michigan who have a job. Payroll jobs count positions at Michigan employers." | DATASETS.md, CES and LAUS sections | supported |
| Chart 4 | "Michigan trades with Canada far more than the nation does" | Shares are 38.8% vs 14.3%; in dollars the U.S. trades far more with Canada than Michigan does | fixed Nov 3: title now "Canada is a far bigger share of Michigan's trade than the nation's" | 

## Flags for Eric

1. **Two Michigan labor force drops.** Beat 3 uses the unadjusted series, Sep to Sep: -4.7%, matching the county data. Chart 3 uses the seasonally adjusted series from Jan 2025: -4.9%. On the seasonally adjusted series, Sep to Sep is -3.6%. BLS smooths the adjusted state series, and the two do not move in step. Each number is right for its series; the post should name which one it is using. Recorded in the findings doc Nov 3.
2. **Chart 4 title**: fixed Nov 3.
3. **Revision wording**: fixed Nov 3.

## Independent tie-out (fresh agent, November 3, 2026)

Given the sources, DATASETS.md and the four chart PNGs only. Pulled LAUS flat
files, the BLS API and the Census API again and recomputed with its own code.

- Numbers: no differences. Every number on the four charts matches, as do
  the beat figures it recomputed (national counts, Michigan counts, state
  ranks, Detroit and rest-of-state changes, CES, Canada shares).
- It confirmed the Detroit MSA county list (six-county sum matches the BLS
  MSA series), the separate-model wording, and the five-year revision.
- Could not check: map colors by geometry (checked by eye only); OMB
  delineation files not downloaded.
- Wording flags: Chart 4 title (already fixed); Chart 1 says "U.S. counties"
  but includes 78 Puerto Rico municipios (38 in SL; without PR, Sep 2026 is
  34.9%); Chart 3 states a model estimate as fact; Chart 2 "fell" may read as
  20 separate local events.
- Method flags, fixed in DATASETS.md Nov 3: balance-of-Michigan series and
  substate model areas added; classification on unrounded values stated;
  revision timing and five-year window stated; Puerto Rico in the universe
  stated.
- Other: Sep 2025 vs Sep 2026 raw difference is +41; +40 on the common
  universe (St. John the Baptist, a returning Katrina parish, is in SL).
  Only 7 of the 20 Michigan entrants fell more than the balance of Michigan
  (-8.7%); 13 fell less.

## Second independent tie-out (fresh agent, November 3, 2026): jobs chart and CPS

- Jobs chart: every value, the line shapes and the October 2025 gap match a
  fresh pull. Wording flags: subtitle omits "nonfarm"; no preliminary note;
  "not falling" is right at the endpoint ("holding steady" is a little more
  exact). No implied cause.
- Fair comparison: a fair side-by-side (the two employment measures BLS
  publishes for states), not like-for-like (residence vs place of work,
  people vs jobs). CES is an input to the LAUS model.
- CPS: statewide and age-group values match `scripts/cps_michigan.py`
  (participation 61.37 to 58.16; shift-share -1.31 / -1.92; prime age
  85.8 to 83.3 outside the Detroit group, 83.0 to 81.5 inside).
- Not supported: the prime-age drop outside Detroit is inside the 95% margin
  of error (SE about 1.3 to 1.9 points); Detroit vs rest cannot be told
  apart; the age-mix split is likely sample noise. DATASETS.md CPS section
  updated to say so.
- Its claim that DATASETS mislabels LAUS units: not a difference. The API
  returns persons; `scripts/fetch_sources.py` divides by 1,000, so the cache
  is in thousands as DATASETS says.
- Its leading-zero bug check: `scripts/cps_michigan.py` converts county codes
  to numbers before matching, so Macomb and Livingston are included (its
  corrected values equal ours).
