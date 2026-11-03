# Follow-up: household survey vs job counts (opened Nov 3, 2026)

Eric's call: very important, not covered elsewhere as far as he has seen,
too big for the September update. Its own study and post later.

## What we found so far

- States where the one-year change in LAUS employed residents trails jobs by
  2+ points (NSA; QCEW through Mar 2026, CES after): never more than 4 in a
  month before 2020; up to 28 states the other way (ahead) in 2020 to early
  2021; trailing peaks 18 in Aug 2021; 0 to 3 through 2025; 18 in Jun 2026,
  14 in Sep 2026. Chart: outputs/charts/sep26-11-state-gaps.png.
- Michigan Sep 2026: employed residents -5.0% (NSA), payroll jobs +0.0%.
  Largest gap of 51. Gap grew month by month through 2026, not as a January step.
- CES has tracked QCEW within about 0.1 to 0.2 points (state average) most
  years; 0.36 to 0.46 since late 2025.
- CPS household response rate (LNU09300000): 89.8% Sep 2013, 65.7% Sep 2026.
  Gaps did not grow steadily with it (calm 2024 to 2025).
- State CPS response rates can be computed from the basic monthly microdata:
  HRINTSTA 1 / (1 + 2), unique households. Reproduces the BLS national rate
  exactly (89.8% Sep 2013, 65.7% Sep 2026). Sep 2026 states: 48.4% to 81.0%,
  median 65.4%; Michigan 67.6%, Ohio 59.1%.

## Candidate explanations to test

1. January 2026 population controls: BLS says they cut the participation
   rate 0.4 and the employment-population ratio 0.5 points, mostly age mix
   (see Eric's "America is older than we thought"). Does the state-level age
   shift line up with the 2026 gaps? Puzzle: the gap grows through the year.
2. State response rates (from microdata) vs state gaps, several months pooled.
3. CES birth-death model change with January 2026 data (one secondary
   source; not yet verified against a BLS notice).
4. LAUS model specification (2021 redesign; inputs CPS, CES, UI claims).
5. 2021 to 2023 trailing episode: no documented cause found yet.

## Scripts and data

scripts/cps_quality.py, scripts/chart_state_gaps.py,
scripts/chart_cps_response.py, scripts/employed_vs_payroll.py,
data/ces/state_gaps_monthly.csv. Q2 2026 QCEW due about early December 2026.
