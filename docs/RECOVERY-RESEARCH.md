# Which states are recovering, and why: research notes

Prepared Sep 15, 2026 for the Data 4 Thought takeaways post. Data as of the
July 2026 LAUS county release. Nothing here is a causal claim.

## The question

Of the counties whose labor force is turning up (positive watch), which states
have the most, and is there anything behind it?

## The two candidates

| | South Carolina | North Dakota |
|---|---|---|
| Counties recovering | 39 of 46 (84.8%) | 36 of 53 (67.9%) |
| Counties on negative watch | 0 | 1 |
| State labor force, Jul 2025 to Jul 2026 | +2.6% | -0.7% |
| Median county, last 3 months vs year earlier | +2.4% | +0.6% |
| Recovering counties still rising on that test | 37 of 39 | 26 of 36 |
| 12-month average above its 5-year low, median | +10.9% | +5.8% |

National context: 577 counties on positive watch and 574 on negative in July
2026, out of 3,214 with data. The national labor force is down 0.8%.

## When each state's counties turned

South Carolina turned in waves, earliest in the metros: 2 counties in 2014, 9
in 2021 (Charleston, Greenville, Berkeley, Horry, Dorchester, Lexington,
Anderson, Pickens, Kershaw), 5 in 2022, 8 in 2023 to 2024, 15 in 2025 to 2026
(the smallest rural counties last).

North Dakota turned late and shallow: 16 of its 36 turned during 2026, and 10
of the 36 are down year over year in the latest month. Bowman is down 11.3%
while its 12-month average is up 6.1%, which is the rule's lag showing.

## What the research found

### South Carolina: migration and participation, not projects

- 41 of 46 counties had positive net domestic migration in 2025 (Census
  Vintage 2025). That is close to the 39 recovering.
- All state population growth since 2020 is in-migration. Deaths exceeded
  births in four of five years. Residents 65+ were 52% of 2024-25 growth, so a
  large share of arrivals are retirees who do not enter the labor force.
- Participation rate rose from 57.7% (Jan 2022) to 58.8% (Jul 2026) while the
  national rate fell from 62.2% to 61.4%. Prime-age participation went from
  78.6% (2023) to 82.7% (Apr 2026).
- Proposed explanation from the Richmond Fed's work: foreign-born workers are
  about 8% of South Carolina's labor force, among the lowest in its district,
  and the national decline is concentrated in that population.
- The project story does not hold. Several headline projects never produced
  jobs (Albemarle lithium in Chester paused before construction; the Hampton
  County ag-tech campus stalled; MycoWorks in Union opened 2023 and the company
  was liquidated in 2025; AESC in Florence paused expansions Jun 2025). Most
  real projects open after the county turned: Eaton in Union 2027, Homanit in
  Clarendon 2028, Hampton Lumber in Allendale 2027, Cyclic Materials in
  Chesterfield 2028.
- The few close matches: Sumter (e-VAC magnets opened fall 2025, turn Nov
  2025, but two closures cost 249 jobs in the same window), Greenwood (E.A.
  Sween opened Feb 2024 and ES Foundry hired 400+, turn Aug 2024, but Teijin
  suspended Dec 2025), Barnwell (tissue mill restarted Aug 2025, turn Jul 2026).
- State programs predate the turns: SC WINS free technical college tuition from
  2019, readySC since 1961, the rural closing fund funded once in 2019.

### North Dakota: mostly unexplained

- One county has a driver of matching size and timing: Dickey, where Applied
  Digital's roughly $1.3B data center campus at Ellendale (town of about 1,100)
  had about 450 construction workers on site by Nov 2025 and more than 1,000
  lodged in Aberdeen, South Dakota by Jan 2026. Dickey's labor force is up
  14.3% in a year and 56% in three.
- Two have the right activity and the wrong timing: Oliver (data center
  rezoning May 2026, after its turn) and Ward (Minot Air Force Base program and
  a pig iron plant, both starting construction 2027).
- Eleven recovering counties have no identifiable driver: Rolette, Sioux,
  Benson, Traill, Pembina, Pierce, Bottineau, Adams, Hettinger, Billings, Bowman.
- Oil does not explain it. The five counties that are 96.7% of state production
  are all absent from the recovering list. Drilling fell through 2025 and did
  not return in 2026 despite the price spike; operators added workover rigs,
  not crews.

## Data checks we ran ourselves

1. **"The 2026 cluster is an annual-revision artifact."** Not supported. North
   Dakota's January 2026 came in 1.0 point *weaker* than its own 2015-2019
   January norm, with only 25% of counties above their norm. An upward revision
   would look like the opposite. South Carolina was +0.11, near normal.
2. **Does migration explain labor force change nationally?** Joined the Census
   county file to our data for 1,826 counties above 20,000 people. Correlation
   with net domestic migration is +0.12; international migration +0.01; natural
   change +0.07. By quintile of net domestic migration, the median labor force
   change runs -1.10%, -0.89%, -0.79%, -0.46%, -0.40%. Even the highest-inflow
   counties are losing labor force at the median. Migration softens the decline
   rather than reversing it.
3. **South Carolina beats its own migration.** Median county migration rate
   +0.59% but median labor force change +1.49%. Michigan is the mirror image:
   75% of counties gained migrants, median labor force change -7.4%. The gap is
   participation, not headcount.
4. **The flags lag.** A positive watch fires on a 12-month average, so a county
   can qualify while its recent months fall. Adding a test that the last three
   months exceed the same three a year earlier would cut North Dakota from 36
   to 26 counties and South Carolina only from 39 to 37. Not applied; it would
   change the published rule.

## Still to verify before print

- ES Foundry in Greenwood: announcement date, investment, first production
  month. The researcher called it the most under-covered real hiring event.
- Whether Dickey County's construction workers were counted as North Dakota
  residents. County labor force is assigned by residence using commuting
  patterns from an older survey, so a new worksite can inflate a small county.
- BLS revised substate and county estimates on May 19, 2026 with inputs back to
  2016, so counties that turned in 2026 sit on a recently rebuilt series.

## How to use this

Lead with South Carolina as a participation and migration story, with the
national quintile table as the spine. Use North Dakota as the caution: a
recovery flag is a signal to investigate, not a finding. See
[docs/VIZ-PLAN.md](VIZ-PLAN.md) section 4b for how the flags are defined.
