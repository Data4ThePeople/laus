---
title: "September 2026 update: 35% of counties in structural labor force loss"
subtitle: 1,132 U.S. counties were in structural loss in September, up 40 from a year earlier. Half the increase is in Michigan, and we are checking those numbers.
slug: labor-force-september-2026
date: 2026-11-03
section: Data 4 Thought
hero: images/labor-force-september-2026-hero-1680x1080.png
hero_alt:
meta_title:
description:
keywords:
schema_type: article
drop_cap: true
heading_spacer: 20px
caption_spacer: 20px
dividers: false
---

# September 2026 update: 35% of counties in structural labor force loss

<!-- Short national update (Eric, Nov 3, 2026). The Michigan spotlight is on hold until the CPS vs QCEW gap is vetted. -->

## The national picture

The Bureau of Labor Statistics (BLS) posted county labor force data through September 2026 on October 28, 2026. In September, 1,132 of 3,214 U.S. counties and Puerto Rico municipios were in structural labor force loss. That means their labor force was more than 10% below the same month 20 years earlier. It works out to 35.2% of all counties. The map below shows every county's 20-year change, month by month, through September 2026.

<iframe src="https://data4thepeople.github.io/laus/" width="100%" height="780" style="border:0" title="Twenty-year change in labor force by county"></iframe>
::: spacer 20px

Looking at the 3,207 counties with data in both years, the count rose by 40 from September 2025. 129 counties entered the structural loss group while 89 left it.

The chart below shows the share of counties in structural loss for every September since 2012. September 2026 is the third highest, behind two post-COVID years: 2022 (36.2%) and 2021 (35.5%).

![Bar chart of the share of U.S. counties and Puerto Rico municipios in structural labor force loss each September from 2012 to 2026. The share rises from 12.3% in 2012 to 26.6% in 2019, jumps to 33.8% in 2020, peaks at 36.2% in 2022, falls to 31.6% in 2024, then rises to 34.0% in 2025 and 35.2% in 2026, which is highlighted.](images/sep26-01-septembers.png)
*Structural labor force loss, every September since 2012. Source: U.S. Bureau of Labor Statistics (LAUS); Data 4 The People analysis.*

## The other five bands

Structural loss is one of six bands. Fast growth has become rarer. In September 2026, 374 counties (11.6%) had a labor force at least 20% larger than 20 years earlier, the Superstars and Hyper-Growth bands together. That is the lowest share of any September since 2012, when it was 983 counties (30.6%).

At the other end, 60.3% of counties had a smaller labor force than 20 years earlier, counting structural loss and at-risk contraction together. That is close to 2021 and 2022 (61.0% in both) and up from 30.4% in 2012.

The chart below shows the share of counties in each band for every September since 2012.

![Six small bar charts, one per band, showing the share of U.S. counties and Puerto Rico municipios in that band each September from 2012 to 2026. Structural Loss rises from 12.3% to 35.2%. At-risk Contraction rises from 18.0% to 25.0%. Below-trend Growth falls from 22.9% to 18.2%. Keeping Pace falls from 16.1% to 9.9%. Superstars falls from 18.2% to 7.4%. Hyper-Growth falls from 12.4% to 4.3%.](images/sep26-09-septembers-bands.png)
*Fewer fast-growing counties than in any September since 2012. Source: U.S. Bureau of Labor Statistics (LAUS); Data 4 The People analysis.*

## A note on the 2026 numbers

One state accounts for half of that net increase. In Michigan, 20 counties entered structural loss in the past year and none left. The next largest net gains were in Minnesota (10), Oklahoma (9) and Tennessee (9).

We are treating these numbers with caution. County labor force figures are built from state estimates that lean heavily on a household survey, and in 2026 that survey has drifted away from counts of jobs. In September, the count of employed residents trailed job counts by 2 points or more in 14 states, and Michigan's gap was the largest. Before 2020, that never happened in more than four states in a month. The chart below shows each month since 2015.

![Bar chart of the number of states, of 50 plus DC, where the one-year change in employed residents differs from the one-year change in jobs by 2 points or more, monthly from January 2015 to September 2026. Bars above the line count states where employed residents ran ahead; bars below count states where they trailed. Before 2020, counts stay under 5. In 2020 and early 2021, up to 28 states ran ahead. Trailing counts reach 18 in August 2021, are 0 to 3 through 2025, then rise to 18 in June 2026 and 14 in September 2026.](images/sep26-11-state-gaps.png)
*Employed residents trail jobs in as many states as in 2021. Source: U.S. Bureau of Labor Statistics (LAUS, QCEW, CES); Data 4 The People analysis.*

In 2020, COVID was a shock to the demographics of our labor force. Models that hadn't really been stressed in the past were stressed, and the BLS tried to make changes in real time. It reminds me of a shock to a refinery and the operator trying to monkey with the controllers to get the system back to homeostasis. But if you move the controllers too much, you can make the problem worse. This seems to be happening now, leading to two different measures for the workforce. One says Michigan is losing employed residents at an alarming clip. The other one says nothing is changing. Not knowing which one is correct may be even scarier than knowing.

Fewer households now answer the survey. Its response rate fell from 89.8% in September 2013 to 65.7% in September 2026. We do not yet know what is behind the gap, and we are looking into it for a future post. BLS is expected to revise the 2026 figures in early 2027.

::: divider

## What this does not tell you

- County labor force figures are model estimates, not direct counts. BLS controls them to a state or area total, so a small county's number is partly a share of a larger estimate.
- The 2026 figures are preliminary and are expected to change in the early-2027 revision.
- Employed residents and job counts measure different things: people where they live versus jobs where they are. They are not expected to match exactly. QCEW counts are about six months behind, so April to September 2026 uses the payroll survey, which is itself a sample survey and will be checked against QCEW when those counts come out.
- Seven New Orleans-area parishes have no data for September 2025 because of a gap in 2005 after Hurricane Katrina. That is why the year-over-year comparison uses 3,207 counties.
- This post does not say what caused the change.

## How we built this

Each county is compared with its own labor force in the same month 20 years earlier, using BLS Local Area Unemployment Statistics (not seasonally adjusted). A county is in structural loss when that change is below -10.0%. Comparisons over time always use the same month. For the survey check, we compare each state's one-year change in employed residents (Local Area Unemployment Statistics) with its one-year change in jobs, month by month, not seasonally adjusted: jobs from the BLS Quarterly Census of Employment and Wages through March 2026, and from the BLS Current Employment Statistics payroll survey after that. Response rates are BLS series LNU09300000. Code and method notes are in our [GitHub repository](https://github.com/Data4ThePeople/laus).
