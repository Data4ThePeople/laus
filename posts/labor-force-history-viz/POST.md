---
title: Visualizing Labor Force Trends by County
subtitle: Where every U.S. county's labor force stands against 20 years ago, month by month since 2010, and exactly how we built it.
slug: labor-force-history-viz
prismic_label: "Visualization: Labor Force History"
prismic_id:
date: 2026-03-16
updated: 2026-09-15
section: Visualization
hero: images/labor-force-history-viz-hero-1680x1080.png
hero_alt: Screenshot of the Data 4 The People interactive map of 20-year change in labor force by county for July 2026. U.S. counties, with Alaska, Hawaii and Puerto Rico in insets, are shaded from dark teal for growth to dark coral for loss, and dark coral covers much of the Great Plains, the Midwest and Appalachia. A side panel shows Saginaw County, Michigan, down 18.2% over 20 years, and a count of 1,281 of 3,214 counties in Structural Loss.
meta_title: Labor Force by County: 20-Year Change Map, 2010 to Today
description: See how every U.S. county's labor force changed over 20 years, month by month since 2010. Free interactive map built on BLS county data.
keywords: labor force by county, county labor force data, labor force map by county, BLS LAUS county data, labor force decline by county, counties losing workers, county labor force trends, structural labor force decline
schema_type: dataset
license: https://www.data4thepeople.com/terms-of-use
temporal: 1990-01/2026-07
spatial: United States and Puerto Rico, all counties and county equivalents
measured: Civilian labor force|persons; 20-year change in civilian labor force, same month|percent
sources: https://www.bls.gov/lau/ | https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html
credit: U.S. Bureau of Labor Statistics (LAUS); Data 4 The People analysis.
app_url: https://data4thepeople.github.io/laus/
app_name: Twenty-year change in labor force by county
app_category: ReferenceApplication
drop_cap: false
heading_spacer: 20px
caption_spacer: 20px
dividers: false
---

# Visualizing Labor Force Trends by County

*This post includes an interactive data visualization, which is best viewed on a computer or tablet. However, if you must use your phone, at least turn it landscape.*

The map below shows every U.S. county's 20-year change in civilian labor force, month by month since January 2010, built from the Bureau of Labor Statistics' Local Area Unemployment Statistics.

<iframe src="https://data4thepeople.github.io/laus/" width="100%" height="780" style="border:0" title="Twenty-year change in labor force by county"></iframe>

::: spacer 40px

## Purpose

This visualization answers one question at a glance: is this county's labor force growing or shrinking over the long run, and is that changing now?

The labor force is the number of people in a county who are working or looking for work. Unlike the unemployment rate, it shrinks when people leave the workforce or move away. A county can post a low unemployment rate and still be losing the workers who pay for its schools, fire departments and roads. We made that case in [Mapping the Viral Spread of Labor Force Decline](https://www.data4thepeople.com/p/viral-labor-force-decline/), and this page is the tool behind it.

The challenge is that a labor force number means little on its own. A county of 20,000 workers may be thriving or collapsing. So this tool compares every county to itself, 20 years earlier in the same calendar month, and sorts the result into six bands. The band we care most about is Structural Loss, a labor force down more than 10% over two decades.

The tool provides four views of the same data:

1. **The map**, every county colored by its band in any month since January 2010
2. **The play animation**, the same map moving month by month, so the spread of structural loss is visible as it happens
3. **The hover chart**, one county's labor force over the exact 20-year window behind its color
4. **The watch flags and stats panels**, which show which counties are turning up or down right now, and how the counts have moved since a year earlier

The visualization is free, and we rebuild it after BLS publishes each new month of county data.

## How to use

**Observe.** The map is a heat map of every U.S. county and Puerto Rico municipio, colored by the change in its civilian labor force over the 20 years ending in the month shown. Six colors run from deepest teal for the fastest-growing counties to darkest coral for the counties in structural loss. The month is in large type above the map.

**Play.** Press Play to watch the map move one month at a time from January 2010 to the latest month. The 1x, 2x and 5x buttons set the speed. The slider and the arrow buttons step to any month by hand, and the left and right arrow keys do the same.

**Hover or tap.** Hover over any county, or tap it on a touch screen, to see its labor force, its 20-year change, its band, and a trend chart of the 20 years behind the color. Tap a county to pin it while the map plays. Hovering is essential. Some counties in structural loss have labor forces that have started to recover over the past three to five years. Others have continued to decline. You cannot see that difference on the map alone.

**Filter by state or territory.** The selector at the top zooms the map to one state or territory and fades the rest. Every count on the page then describes that state only.

**Watch flags.** Tick the box to add stripes to counties whose labor force is turning. Rising white stripes mark a positive watch. Falling dark stripes mark a negative watch. The definitions are in Part 4 below.

## What this page is

Every chart we publish should be verifiable, questionable and reproducible by anyone. This page documents the complete method: where the data comes from, every transformation, and every decision point. Nothing here is proprietary. The code and the data pipeline are public at [github.com/Data4ThePeople/laus](https://github.com/Data4ThePeople/laus), and a reader with a computer and an internet connection can rebuild the whole page from scratch.

## The data source

Every labor force figure comes from the U.S. Bureau of Labor Statistics program called Local Area Unemployment Statistics, or LAUS. LAUS publishes monthly estimates of the labor force, employment and unemployment for every county and county equivalent in the United States and Puerto Rico. The data is public and free.

We use one measure, the civilian labor force, at one geography, counties and equivalents. That is 3,225 series in all, including the 78 municipios of Puerto Rico, running monthly from January 1990 to the latest month. The county figures are not seasonally adjusted, because BLS does not publish seasonally adjusted county data. That fact shapes the whole method, as Part 1 explains.

**The files we read, from the BLS bulk download at download.bls.gov/pub/time.series/la/:**

::: embed 240px

The county shapes on the map come from the U.S. Census Bureau's 2024 cartographic boundary files at the 1:5,000,000 scale, which include Puerto Rico. Counties are joined to their data on the five-digit county FIPS code.

**Live retrieval.** Each build downloads the BLS files directly. There are no manual downloads and no hand-typed numbers. The map always reflects the most recent BLS release at the time it was built, and the footer of the map states the latest month it contains.

## Part 1, The map and the six bands

### Step 1: Compare each county to itself, 20 years earlier, in the same month

For every county and every month, we divide the labor force by the labor force in the same calendar month 20 years earlier, and subtract one. July 2026 is compared to July 2006. April 2026 is compared to April 2006.

The same-month rule matters because the county data is not seasonally adjusted. Farm counties swell in summer and fishing boroughs swell in season. Comparing a month to itself 20 years earlier cancels that pattern inside each comparison. It also means the map for one month should be compared to the same month in other years, never to the month before.

Because LAUS county data begins in January 1990, the first month with a 20-year comparison is January 2010. That is where the animation starts.

### Step 2: Sort the result into six bands

The six bands and their ranges are below.

::: embed 320px

Each edge belongs to the band above it. A county at exactly -10.0% is At-risk, not Structural Loss. A county at exactly +20.0% is a Superstar. The band edges live in one place in the code and every table, count and color on the page derives from them.

### Step 3: Color by band

The six bands use a diverging scale: teal for growth, coral for loss, with the two bands nearest zero in the lightest shades. The scale was checked for lightness order and text contrast so darker always means farther from zero on either side. Counties with no 20-year comparison in a month are drawn in a neutral gray.

### Step 4: Handle the months and counties with no comparison

A county gets no band in a month when either end of the 20-year comparison is missing. This happens more than you might expect, and the map shows it in gray rather than hiding it:

- **October 2025.** BLS published no county data for that month except for Puerto Rico, because of the federal appropriations lapse. The map shows October 2025 as gray with a note, and the same hole will appear in October 2045 when that month becomes the base.
- **Hurricane Katrina.** BLS published no data for seven New Orleans-area parishes from September 2005 through June 2006. Those parishes drop out of the map from September 2025 through June 2026 and return in July 2026.
- **Puerto Rico in March and April 2020.** BLS published no Puerto Rico data for those two months. Puerto Rico drops out of those two frames and will drop out again in 2040.
- **Alaska.** Seven census areas were created in 2010 or 2020 and do not yet have 20 years of history. They stay gray throughout.

### Step 5: Controls

- **Month.** A slider and step buttons choose any month from January 2010 to the latest month. The month is printed in large type.
- **State or territory.** A selector zooms the map to one state, fades every other county to about 20% so the neighbors stay visible, and filters every count on the page to that state. Alaska, Hawaii and Puerto Rico zoom into their own insets.
- **Insets.** Alaska, Hawaii and Puerto Rico sit in boxes below the lower 48. Puerto Rico is enlarged so its 78 municipios can be hovered.

## Part 2, The play animation (new)

Press Play and the map steps through every month from January 2010 to the latest month, 199 frames in all. At 1x the map advances three months a second, so the full run takes about 65 seconds. The 2x and 5x buttons run six and fifteen months a second. Frames cut hard from one month to the next with no fading, so what you see at any instant is one real month.

Playback stops on the latest month. Every panel on the page, including the hover chart for a pinned county, updates with each frame.

## Part 3, The hover trend chart

Hover or tap a county and the chart shows its monthly labor force over the exact 20 years behind its color: 240 months, ending in the month on the map. A dot marks each end of the window. The label above the chart reads the county's labor force, its 20-year change, its band and any watch flag.

### The scale is fixed, and it slides

Every series is indexed to 100 at the start of its window. The vertical scale is the same for every county: one index point is the same number of pixels whether you are looking at a county of 500 workers or five million. The chart window slides up or down to center on the county's line.

We did this because the two obvious choices both mislead. An axis that starts at zero flattens most counties into a nearly straight line and hides the change. An axis that stretches each county to fill the chart turns a 3% wiggle into a cliff. With a fixed scale, a 10% drop has the same slope in every county, and a flat county looks flat.

The default window spans 40 index points. When a county's line moves more than that, a hyper-growth county at +60% for example, the scale compresses to fit and the chart says "compressed scale" in the corner.

### About the labor force label

Labor force values in the label and in the lists are exact for counties whose labor force has never topped 65,000. For larger counties the value is within about 40 workers and shown as "about." This is a trade for a page that loads as one file with no server behind it. The BLS figure to the person is in the public BLS files.

## Part 4, Watch flags (new)

The color tells you where a county stands against 20 years ago. The stripes tell you which way it is heading right now.

The 20-year band moves slowly, and it moves for two reasons: what happened this month, and what dropped out of the window from 20 years back. A county can "improve" in 2026 because 2006 was a bad year there. So the watch flags ignore the 20-year window entirely and look at the last one to five years.

**Positive watch, all four must hold:**

1. The labor force, averaged over the last 12 months, is at least 2% above the lowest 12-month average of the past five years. It has climbed off a bottom.
2. That bottom is at least a year old. The climb has lasted; it is not last month's bounce.
3. The 12-month average is at least 1% higher than a year ago. It is still climbing now.
4. This month's labor force is higher than the same month three years ago. The gain is not a one-year blip.

**Negative watch, both must hold:**

1. The 12-month average is at least 1% lower than a year ago. It is shrinking now.
2. This month's labor force is at least 2% below the same month three years ago. The shrinking has gone on a while.

Everything else is unflagged: flat, drifting, or too mixed to call.

Why a 12-month average: the county data is not seasonally adjusted and small counties jump around month to month. Averaging a full year cancels the seasons and softens odd months. Why a three-year check as well: one year can be a bounce or a dip, so the flag needs two independent looks at the data to agree. Why the "bottom" test only on the positive side: recovering means recovering from something, so the rule needs a measurable low that has held for a year. "Still falling and smaller than three years ago" is already the whole negative story. The positive flag is stricter on purpose, because calling a recovery is the stronger claim.

A county can be in Structural Loss and on positive watch at the same time. That is the point. It is the county that has been hurt for 20 years but has turned.

## Part 5, The stats panels

**Counties by band.** The count in each band for the month on the map, with a bar for its share. When watch flags are on, the panel adds the count of positive and negative flags.

**Change from a year earlier.** Every count compares the month on the map to the same calendar month one year earlier, among counties with data in both months. The rows are: Structural Loss a year earlier and now; counties that entered and left Structural Loss; counties that moved down or up a band; counties whose 20-year change worsened or improved; Structural Loss counties on positive watch; and counties outside Structural Loss on negative watch.

**Top counties this month.** The largest counties, five on a full screen and three in the embedded view, by labor force, that entered Structural Loss since a year earlier; the largest in Structural Loss on positive watch; and the largest outside Structural Loss on negative watch.

All three panels follow the state selector.

## Updating

We rebuild the page after BLS publishes a new month of county data, which arrives roughly a month to six weeks after the month ends. The process is mechanical. A script downloads the BLS files, computes every 20-year change and band, computes the watch flags, and writes the page. The page is one file with no server behind it, published from the public repository. No number on it is typed by hand.

BLS revises county data each spring. When that happens the whole history is rebuilt, and counts for past months can shift by a few counties.

## Honest notes and limitations

- **Recent months are preliminary.** BLS county figures for the current year are estimates and are revised the following spring. A band or a flag on the latest month is softer than one from a year ago. Between the June 2026 article and this update, revisions moved the April 2026 Structural Loss count from 1,160 to 1,156.
- **Same-month only.** Because the data is not seasonally adjusted, the tool never compares one month to the month before it. Every comparison on the page is same-month: 20 years back for the bands, one year back for the change panel, three years back for the flags.
- **The band edges are sharp.** In April 2026, 47 counties sat within a quarter of a percentage point of the -10% line. Small revisions move counties across it. Lead with the trend, not with the exact count.
- **The county universe changes.** Seven Louisiana parishes drop out for ten months because of Katrina. Connecticut's data is on its nine planning regions, not its eight historical counties. Four Alaska areas were discontinued in 2009 or 2019 and seven were created. The page draws what BLS publishes and grays out the rest.
- **The flags describe movement, not cause.** A negative watch says the labor force is shrinking, not why. Small counties can flip a flag on modest changes; the lists sort by labor force so the large ones lead. The thresholds, 1% on the average and 2% over three years, are judgment calls, and they are the only tunable parts.
- **Labor force labels over 65,000 are rounded**, as Part 3 explains.
- **Color.** The band scale was checked in a perceptual color model for lightness order and contrast, and the watch flags use stripe direction rather than hue so they read without color. The gray used for counties with no data is close to the lightest teal band, so the hover label is the surest way to tell them apart.
- **We did not invent the data.** Every number on the page comes from BLS. Our contribution is the reorganization: the same-month 20-year comparison, the bands, the watch rules, and the interactivity.

## Reproduce it yourself

Everything needed is public. The repository at [github.com/Data4ThePeople/laus](https://github.com/Data4ThePeople/laus) holds the code, the tests, and this method. Run the five commands in its README in order: ingest, classify, watch, geo, viz. The first downloads about 340 megabytes from BLS; the last writes the page. The band edges, the watch thresholds and the color scale each live in one named place in the code.

If you rebuild it and get a different answer, we want to know. [Contact us](mailto:connect@data4thepeople.com).

## Common questions

### What is the civilian labor force?

It is the number of people age 16 and over who are either working or actively looking for work. It leaves out people who have retired, stopped looking, or moved away. That is why it can shrink while the unemployment rate looks fine: a person who leaves the workforce is not counted as unemployed.

### Why compare each county to 20 years ago instead of last year?

A one-year change is mostly noise in a small county, and it says nothing about whether a place is on a long slide or a long climb. Twenty years covers a full generation of workers entering and leaving, so the change shows the structure of a local economy rather than one good or bad year. The page also shows the one-year and three-year picture through the change panel and the watch flags.

### What does Structural Loss mean?

A county is in Structural Loss when its labor force is down more than 10% from the same month 20 years earlier. The name is ours, not the government's. We chose it because a decline of that size over that long a period is rarely a cycle. In our view, it often reflects an aging population that is not being replaced by younger workers.

### Why is the map gray for October 2025?

BLS did not publish county data for October 2025 because of the federal appropriations lapse. Only Puerto Rico has figures for that month. The map shows the gap as it is rather than filling it in. The same gap appears for seven New Orleans-area parishes from September 2025 through June 2026, because their data 20 years earlier is missing after Hurricane Katrina.

### What is a positive watch or a negative watch?

They are flags for counties whose labor force is turning right now, separate from the 20-year band. A positive watch means the labor force has climbed at least 2% off a low that is at least a year old, is still rising, and is above where it was three years ago. A negative watch means it is down at least 1% from a year ago and at least 2% from three years ago. Part 4 above has the full rules.

### Why does the hover chart not start at zero?

An axis that starts at zero shrinks a 15% decline to a small dip near the top of the chart, which makes the change hard to see. Instead the chart uses the same vertical scale for every county and slides its window to fit the data. A 10% drop looks the same in a county of 500 workers as in one of 500,000, and it is never stretched to look bigger than it is.

### How often is the page updated?

Each time BLS publishes a new month of county data, roughly a month to six weeks after the month ends. The rebuild is a script, not a manual edit, so every count and every flag updates at once. BLS also revises county data each spring, and the whole history is rebuilt when that happens.

### Why do the counts here differ from the June 2026 article?

BLS revised the county data after [that article](https://www.data4thepeople.com/p/geographic-virus-accelerating/) was written. The April 2026 Structural Loss count moved from 1,160 to 1,156, and the one-year change from 132 to 128. This page reflects the latest data.

### Is the visualization free to use?

Yes. The page is free to view, and the code is public to read. Use follows our terms of use.
