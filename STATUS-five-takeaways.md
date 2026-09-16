# Status: Data 4 Thought takeaways post

Project: laus (structural labor force decline)
Process: ~/.claude/d4tp-process/PROCESS.md
Sibling: STATUS.md, which covers the Visualization methodology page (complete)

## Current

Post: five-takeaways-labor-force-decline
Step: 2f
Since: 2026-09-16

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | 2026-09-14 | Shared with the viz page; research in docs/RECOVERY-RESEARCH.md |
| 2a | Draft with brackets resolved | 2026-09-16 | Spare draft, charts carry the story |
| 2b | Eric's edit, Claude's look-over | 2026-09-16 | Eric edited; 10 items proposed and all accepted |
| 2c | Slice markup | 2026-09-16 | 44 slices; one divider above the notes; carousel full width |
| 2d | Hero 1680x1080 + alt text | 2026-09-16 | Takeaway 1 chart, minimal variant, one call-out |
| 2e | SEO | 2026-09-16 | Meta title 51 chars, description 152, 8 keywords, Article + FAQ schema |
| 2f | Pushed to Prismic (draft) | | |
| 2g | Mailchimp teaser | | |

## Stale

None.

## Log

- 2026-09-16 Post opened. Five takeaways from the rebuilt visualization.
  Takeaway 1: counties in structural loss over the full series, 40% in July 2026, an all-time high.
  Takeaway 2: January to July change by year since 1990, 2026 the weakest outside 2020.
  Takeaway 3: states with the most counties on negative watch, with the Michigan map.
  Takeaway 4: states with the most counties on positive watch, with the South Carolina map.
  Takeaway 5: hyper-growth counties stalling, 48% now below a year earlier, with an eight-slide carousel.
- 2026-09-16 Charts copied into posts/five-takeaways-labor-force-decline/images. POST.md holds the
  charts, captions, alt text and the carousel fence. Title, prose, hero and SEO are still open.
  Every chart regenerates from scripts/chart_*.py.
- 2026-09-16 Draft written at Eric's request, deliberately spare: 472 words of prose across the five takeaways, with the charts carrying the story. Every number tied out against the data. Title, hero and SEO still open.
- 2026-09-16 Step 2b done. Eric's edits reviewed; both brackets resolved. The Colorado claim was corrected:
  the Denver metro counties are NOT on negative watch (the flag also needs a three-year decline), though all
  ten of Colorado's largest counties are down year over year. New chart 03c-co-largest-counties.png.
  The December 2025 structural loss share was 33%. Step 2c opened.
- 2026-09-16 Step 2c: dividers turned on between top-level sections, carousel set to the full-width variation. 44 slices, 8 carousel slides, 3 FAQ entries in the schema, 16 images all with alt text.
- 2026-09-16 Step 2c corrected: dividers off. Section headings get the 20px spacer and a single divider sits above the methodology blurb, per PROCESS.md step 2c. Carousel stays full width.
- 2026-09-16 Step 2c done. Step 2d opened: hero.
- 2026-09-16 Step 2d done. Step 2e opened: SEO.
- 2026-09-16 Step 2e: meta title 51 chars, description 152, 8 keywords, Article plus FAQ schema with three questions. Four crawlable-text edits accepted, including internal links to the March and June pieces. The shared schema builder now sets the house terms-of-use license on Article as well as Dataset pages, replacing a hard-coded Creative Commons default.
- 2026-09-16 Step 2e done. Step 2f opened: push to Prismic as a draft.
- 2026-09-16 Step 2f: pushed to Prismic. New draft aqrqxxEAACsAk4Np in the Migration Release, uid five-takeaways-labor-force-decline, label "Data 4 Thought: Five Takeaways, Labor Force". 17 images uploaded including the hero. Tags and author empty. Re-running updates this same draft.
- 2026-09-16 Publication set to September 16, 2026 at 4:30pm Eastern (date plus a time line in front matter). Draft re-pushed.
- 2026-09-16 Carousel images now carry a 150px band of background at the bottom, because Prismic lays the slide caption over the image and it was landing on the source line. Captions also keep their italics now (importer fix).
- 2026-09-16 Importer fix: a re-rendered image used to keep its old asset in Prismic, because uploads were cached by path alone. The cache now records size and modified time and re-uploads a changed file.
