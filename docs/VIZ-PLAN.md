# Interactive map: enhancement plan

Status: draft for Eric's review. Nothing here has been run or built.

Covers Stage E (the map), which replaces the Tableau embed and the ffmpeg
timelapse, plus a new Stage C2 (watch flags) that feeds both the map and the
tables. Four enhancements were asked for: a play button with speeds, one map
with Alaska, Hawaii and Puerto Rico, a hover trend chart with fair scaling,
and monthly stats on counties getting better or worse inside their band.

---

## 0. Delivery shape

- One self-contained `dist/index.html`. Vanilla JS, no CDN, no library.
  Map on a `<canvas>` (3,200 polygons redrawn every frame; canvas is fast
  enough at 15 frames a second, SVG is not). Hover chart on a small second
  canvas. Sized for the Prismic 780px frame, light theme pinned when framed,
  "Built by Data 4 The People" in the footer.
- Built by a new `src/lfd/viz.py` (`lfd viz`) from `data/classified.parquet`,
  the raw panel, and cached Census geometry. The HTML template lives in
  `src/lfd/templates/index.html`; the build injects the data blocks, the band
  edges from `classify.BINS`, the labels, and the colors. Nothing in the JS
  is hand-typed from the data.
- Data is embedded as base64 typed arrays, decoded once on load.
- Payload budget: about 3 MB total. Breakdown in section 5.

## 1. Play button with 1x, 2x, 5x

- Controls in one bar above the map: play/pause, a speed toggle (1x, 2x,
  5x), a month slider, step-back and step-forward buttons, the current month
  in large type ("April 2026").
- Cadence: 1x is 3 months a second. Jan 2010 to Apr 2026 is 196 frames, so
  1x plays in about 65 seconds, 2x in 33 and 5x in 13. Driven by
  `requestAnimationFrame` with a time accumulator, so a slow machine drops
  frames instead of slowing down.
- Hard cuts between months, matching the cleaned timelapse. No fades.
- Play stops on the latest month rather than looping, and the button turns
  into "replay". The stats panel and the hover chart update with every frame.
  If the mouse is over a county when play starts, that county stays pinned
  in the hover chart until the mouse moves.
- Keyboard: space toggles play, left and right arrows step one month.
- Frame range: Jan 2010 through the latest month, since LAUS county data
  starts Jan 1990 and the 20-year window needs it.

## 2. One map with Alaska, Hawaii and Puerto Rico

- Geometry: Census cartographic boundary counties, 2024 vintage, 1:5m scale
  (`cb_2024_us_county_5m`). It includes Puerto Rico's 78 municipios.
  Downloaded once and cached under `data/raw/geo/`. Simplified with shapely
  to keep the file small; the tolerance is tuned so small eastern counties
  still read at embed size.
- Projection: done in Python, not in the browser. A composite Albers in the
  style of the usual "Albers USA" layout, extended with Puerto Rico:
  the lower 48 on Albers (standard parallels 29.5 and 45.5, center -96),
  Alaska scaled to about 35% and placed lower left, Hawaii lower middle,
  Puerto Rico lower right below Florida. Each inset gets a thin box.
- Coordinates are emitted pre-projected in integer pixel units on a
  1000 by 640 reference canvas, delta-encoded, and the browser scales them
  to the container. That is why the JS needs no projection code.
- Join key: Census GEOID is the 5-digit FIPS, which is LAUS `area_code[2:7]`.
  The build prints a reconciliation: LAUS counties with no shape, shapes
  with no LAUS series. Duplicates are a hard failure. Known cases to check
  on the first run: Connecticut, which switched from 8 counties to 9
  planning regions (Census 2022 onward; LAUS switched too, the year needs
  confirming), and the 2019 split of Valdez-Cordova, AK into two census
  areas. Counties with a shape but no value in a given month are drawn in a
  neutral gray labeled "no data" and are not counted in the stats.
- Colors: the six bands on a diverging scale from teal (Hyper-Growth) to
  coral (Structural Loss), with the near-zero bands lighter. Final hexes
  come from the `dataviz` skill palette check so the ramp is readable in
  light and dark themes. Legend as colored words, not dots.

## 3. Hover trend chart with fair scaling

**What it shows.** The county's monthly labor force over the 20-year window
that produced its current band: 240 points ending at the frame month. The
two same-month anchors (window start and frame month) are marked, and the
label reads "Saginaw County, MI: 85,594, -12.6% over 20 years". Showing the
exact window the band was computed on is the point; the reader sees the
same comparison the color came from.

**The scaling rule: fixed scale, sliding window.**

- Each series is indexed to its window-start value equals 100.
- The vertical scale is fixed for every county: 1 index point is the same
  number of pixels everywhere. The default chart height shows a 40-point
  span, so a 10% drop is always the same visual slope, in Saginaw or in
  San Juan.
- The window slides to center on the series: the y-range is the midpoint of
  the series' min and max, plus and minus 20 points. Gridlines every 10
  index points, labeled, with the 100 line labeled "start of window".
- Only when a series spans more than 40 index points (a hyper-growth county
  at +60%, or a collapse past -40%) does the scale compress to fit, and the
  chart says "compressed scale" in small type.
- The scale never expands. A county with a 3% wiggle shows a nearly flat
  line inside a 40-point window, which is the honest picture. Tableau's
  zero-based axis hid every change; a min-to-max autoscale would turn every
  wiggle into a cliff. The fixed scale is the middle that treats every
  county the same way.

Right-hand labels show the actual labor force at the start and end anchors
so the index does not hide the size of the county.

**Data needed.** Monthly labor force for every county from Jan 1990. That is
about 3,220 counties by 440 months by 4 bytes, 5.7 MB raw, which is too
much to embed as is. Plan: store each county's series as month-to-month
deltas in a compact variable-length encoding, gzip the block in Python, and
decode in the browser with the built-in `DecompressionStream`. Estimated
1.2 to 1.8 MB. `DecompressionStream` is a browser built-in, not a library,
supported in Chrome, Firefox and Safari since 2023. If it is missing the
page still draws the map and the stats and shows a one-line note in the
chart area.

## 4. Movers stats and watch flags

Two different things are being asked for, and they need two different
measures.

### 4a. Monthly movers panel (band changes)

A small panel beside the map, recomputed for each frame from the embedded
20-year metric, showing the count of counties versus the same month a year
earlier:

- entered Structural Loss, left Structural Loss
- moved down a band, moved up a band (any band)
- 20-year metric improved, worsened (any size)
- the six band counts for the frame month as a horizontal stacked bar

The comparison is same-month, one year back, to match the June 2026 piece.
Caveat to print under the panel: the 20-year metric moves for two reasons,
this month's labor force and the month that dropped out of the window 20
years ago. A county's metric can "improve" because 2006 was bad, not
because 2026 is good. This is why the watch flags below are built on recent
labor force, not on the metric.

### 4b. Watch flags (trajectory inside a band)

Goal: flag a county that is still in Structural Loss but has bottomed out and
is climbing (positive watch), or a county in any band whose labor force is
sliding even though the 20-year number has not moved it yet (negative
watch). Candidates, all using same-month comparisons so seasonality drops
out:

1. **Year-over-year streak.** LF this month versus the same month a year ago,
   positive for 12 straight months means positive watch, negative for 12
   straight means negative watch. Simple to explain. Weak point: one odd
   month breaks a streak, and a county can be "up year over year" while
   still below its 2019 level.
2. **Distance from the 5-year trough or peak.** Take the 12-month average of
   LF. Positive watch if it is at least 2% above its lowest 12-month average
   of the last five years and that low was at least 12 months ago. Negative
   watch if it is at a new 5-year low, or within 1% of one set in the last
   12 months. This is the most direct reading of "bottomed out".
3. **Three-year change.** LF versus the same month three years ago, above
   +2% or below -2%. Smooth and easy to say in a sentence. Weak point: it
   lags a turn by a year or more.
4. **Slope of a 36-month fit.** Statistically cleaner, hard to explain to a
   reader, and it does not know where the trough is.
5. **Boundary proximity plus direction.** Metric within 2 points of a band
   edge and the year-over-year direction points across it. Useful as a
   separate "about to move" tag, but it is about the metric, not the
   trajectory, so it inherits the base-effect problem.
6. **Position against its own 20-year trough.** The window's low point was
   at least 24 months ago and the county is now 3% or more above it.
   Similar to 2 but tied to the same window the band uses.

**Recommendation: candidate 2 with candidate 3 as a confirmation.**
Positive watch = 12-month average LF at least 2% above its 5-year low, the
low at least 12 months old, and the 3-year change positive. Negative watch =
12-month average within 1% of a 5-year low set in the last 12 months, and the
3-year change at or below -2%. Reason: the trough rule is exactly the
"bottomed out and recovering" idea in plain words, the 12-month average
keeps a single odd month from tripping it, and the 3-year check stops a
one-year bounce from counting as a recovery. Both are same-month safe and
both can be said in one sentence under a chart. The thresholds (2%, 1%, 12
months, 5 years) are tunables; the first run prints Erie PA, Saginaw MI, San
Juan PR, Lucas OH and Lincoln NE under each candidate so we can see which
rule matches what the eye sees in their hover charts.

**Where it shows up.**

- A "watch flags" toggle on the map draws a stripe pattern over flagged
  counties (teal stripes for positive, dark stripes for negative) on top of
  the band color, so the band is still readable. Off by default.
- The stats panel adds two lines: "Structural Loss, recovering: N" and
  "Negative watch outside Structural Loss: N", plus the top 10 of each by
  labor force for the frame month.
- The hover chart marks the 5-year trough or peak with a small dot and
  labels the flag ("positive watch since March 2025").
- Python side: `src/lfd/watch.py` computes flags for every county-month and
  writes `data/watch.parquet`; `tables.py` gets two more tables (top 10
  recovering, top 10 negative watch) for the post.

## 5. Payload budget

| Block | Encoding | Estimate |
|---|---|---|
| County shapes, projected | int16 deltas, base64 | 700 to 900 KB |
| 20-year metric, 196 frames by 3,220 counties | int16 tenths of a percent | 1.3 MB raw, about 500 KB after gzip |
| Monthly LF from 1990 for hover chart | varint deltas, gzip | 1.2 to 1.8 MB |
| Watch flags, 196 frames | 2 bits per county-month | under 50 KB |
| Names, FIPS, band edges, labels, colors | JSON | under 100 KB |

Total about 3 MB. Bands and movers are derived in the browser from the
metric block using the edges emitted from `classify.BINS`, so the JS never
carries its own copy of the rule. If 3 MB is too heavy for the embed, the
first thing to cut is hover-chart history before 2005 (the earliest frame
needs 1990, but a shorter chart window could start at 2005 for a 40% saving).

## 6. Build order

1. `geo.py`: fetch, simplify, project, reconcile against the LAUS universe.
2. `watch.py` plus tests on synthetic series (a V-shape, a slide, a flat line).
3. `viz.py`: encode the blocks, render the template, print the payload sizes.
4. Template JS: map draw, play loop, hover chart, movers panel, flag layer.
5. Check in the Prismic frame size and at phone width.

## 7. Open questions for Eric

- Frames run Jan 2010 to the latest month. 2010 is the floor because the
  20-year window needs data from 1990. Confirm that range, or pick a
  shorter one (2015 onward, say) for a quicker loop.
- Oct 2025: if LAUS carries nulls for that month, show the frame as
  "no data" gray, or skip the frame.
- Puerto Rico in the map inset, yes or no. The June 2026 decision was to
  include it in tables.
- Thresholds for the watch flags, once the five spot-check counties are
  printed under each candidate.
