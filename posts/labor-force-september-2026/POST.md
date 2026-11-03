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

<!-- Short national update (Eric, Nov 3, 2026). The Michigan spotlight is on hold until the CPS vs CES gap is vetted. -->

## The national picture

The Bureau of Labor Statistics (BLS) posted county labor force data through September 2026 on October 28, 2026. In September, 1,132 of 3,214 U.S. counties and Puerto Rico municipios were in structural labor force loss. That means their labor force was more than 10% below the same month 20 years earlier. It works out to 35.2% of all counties. The map below shows every county's 20-year change, month by month, through September 2026.

<iframe src="https://data4thepeople.github.io/laus/" width="100%" height="780" style="border:0" title="Twenty-year change in labor force by county"></iframe>
::: spacer 20px

Looking at the 3,207 counties with data in both years, the count rose by 40 from September 2025. 129 counties entered the structural loss group while 89 left it.

The chart below shows the share of counties in structural loss for every September since 2012. September 2026 is the third highest, behind two post-COVID years: 2022 (36.2%) and 2021 (35.5%).

![Bar chart of the share of U.S. counties and Puerto Rico municipios in structural labor force loss each September from 2012 to 2026. The share rises from 12.3% in 2012 to 26.6% in 2019, jumps to 33.8% in 2020, peaks at 36.2% in 2022, falls to 31.6% in 2024, then rises to 34.0% in 2025 and 35.2% in 2026, which is highlighted.](images/sep26-01-septembers.png)
*Structural labor force loss, every September since 2012. Source: U.S. Bureau of Labor Statistics (LAUS); Data 4 The People analysis.*

## A note on the 2026 numbers

One state accounts for half of that net increase. In Michigan, 20 counties entered structural loss in the past year and none left. The next largest net gains were in Minnesota (10), Oklahoma (9) and Tennessee (9).

We are treating the Michigan figures with caution. BLS builds county labor force numbers from state estimates that lean heavily on a household survey. In 2026, that survey-based count of employed residents has fallen well below the count of payroll jobs in several states, including Michigan, Connecticut, Arizona and Minnesota. In Michigan, employed residents fell 3.6% from September 2025 to September 2026 while payroll jobs were flat. Gaps that large are rare, and we are looking into them before drawing conclusions. BLS is expected to revise the 2026 figures in early 2027.

::: divider

## What this does not tell you

- County labor force figures are model estimates, not direct counts. BLS controls them to a state or area total, so a small county's number is partly a share of a larger estimate.
- The 2026 figures are preliminary and are expected to change in the early-2027 revision.
- Employed residents and payroll jobs count different things: people where they live versus jobs where they are. They are not expected to match exactly, but they usually stay within about a point of each other over a year.
- Seven New Orleans-area parishes have no data for September 2025 because of a gap in 2005 after Hurricane Katrina. That is why the year-over-year comparison uses 3,207 counties.
- This post does not say what caused the change.

## How we built this

Each county is compared with its own labor force in the same month 20 years earlier, using BLS Local Area Unemployment Statistics (not seasonally adjusted). A county is in structural loss when that change is below -10.0%. Comparisons over time always use the same month. Employed residents (seasonally adjusted) also come from Local Area Unemployment Statistics, and payroll jobs from the BLS Current Employment Statistics survey. Code and method notes are in our [GitHub repository](https://github.com/Data4ThePeople/laus).
