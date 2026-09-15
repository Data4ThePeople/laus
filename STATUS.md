# Status

Project: laus (structural labor force decline)
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: labor-force-history-viz (update of the live Visualization methodology page; a second Data 4 Thought post follows)
Step: 2f
Since: 2026-09-15

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | 2026-09-14 | Pipeline, comparison, watch flags and interactive map built; live at https://data4thepeople.github.io/laus/. Tie-out in ~/.claude/plans/snazzy-sniffing-coral.md |
| 2a | Draft with brackets resolved | 2026-09-15 | Full rewrite of the Visualization methodology page modeled on the petroleum inventory page; tables in tables.html |
| 2b | Eric's edit, Claude's look-over | 2026-09-15 | No edits from Eric; 15 look-over items accepted |
| 2c | Slice markup | 2026-09-15 | 67 slices; no drop cap or dividers, matching the petroleum page; 2 empty table embeds |
| 2d | Hero 1680x1080 + alt text | 2026-09-15 | Padded snapshot of the viz, July 2026, Saginaw pinned; alt 438 chars |
| 2e | SEO | 2026-09-15 | Meta title 56 chars, description 136, 8 keywords; Dataset + WebApplication + FAQPage schema; 3 crawlable edits |
| 2f | Pushed to Prismic (draft) | | |
| 2g | Mailchimp teaser | | |

## Stale

None.

## Log

- 2026-09-14 Step 1 opened. Topic: update to "Mapping the Viral Spread of Labor Force Decline". Python rebuild of the Tableau tool from BLS LAUS county data, 20-year same-month bands, snapshot comparison, positive/negative watch flags, and a self-contained interactive map with a state selector. Data through July 2026.
- 2026-09-14 Step 1 done. Tie-out complete, every reported number recomputed from data/*.parquet. Waiting for the slug to open 2a.
- 2026-09-15 Step 2a opened for labor-force-history-viz: full update of the Visualization methodology page, modeled on the petroleum inventory seasonality methodology page. Second post (Data 4 Thought summary of changes, latest data, tool enhancements) to follow as its own slug.
- 2026-09-15 For 2f: Prismic document label is "Visualization: Labor Force History" (set as prismic_label in front matter). The importer needs the live page's document id in prismic_id to update it in place; the content API is private and no read token is in the env, so Eric supplies the id from the Prismic dashboard or a read token.
- 2026-09-15 Step 2a done for labor-force-history-viz. Step 2b opened: Eric edits POST.md directly, then asks for the look-over. A separate STATUS for the Data 4 Thought post is planned once the viz post is through the process.
- 2026-09-15 Step 2b look-over: 15 items, all accepted and applied. Map note no longer states a cause for the missing Puerto Rico months. README added. No LICENSE added; the free-to-use answer now defers to the site's terms of use.
- 2026-09-15 Step 2b done. Step 2c opened: slice markup.
- 2026-09-15 Step 2c done. Step 2d opened: hero.
- 2026-09-15 Step 2d done. Step 2e opened: SEO.
- 2026-09-15 Step 2e: Eric approved the assumed searches (labor force by county, county labor force data, labor force map by county, labor force decline by county) and accepted crawlable-text edits 1 to 3.
- 2026-09-15 Step 2e done. Step 2f opened: push to Prismic as a draft over the live page.
- 2026-09-15 Step 2f: pushed as an update to live document abfuCxQAACYAxMRO (id found in the site's public page payload). Draft lands in the Migration Release; tags and author empty. Label "Visualization: Labor Force History". Two empty table embeds await the code from tables.html.
- 2026-09-15 Plan split into two posts. (1) labor-force-history-viz: its 2g email is only an announcement of the rebuild and the new functionality (play, one map with AK/HI/PR, fair-scale hover chart, state selector, watch flags). No findings or takeaways in it. (2) The Data 4 Thought "main takeaways" post is a separate post worked the next day, with its own STATUS file.
- 2026-09-15 Step 2f re-push: both tables now go straight into their embeds through a new `::: html` fence in the importer (documented in SLICES.md), and a divider sits before Common questions. Same draft, abfuCxQAACYAxMRO.
- 2026-09-15 Step 2f re-push: Honest notes and limitations moved into a titled highlighted page blurb.
