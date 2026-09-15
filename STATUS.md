# Status

Project: laus (structural labor force decline)
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: labor-force-history-viz (update of the live Visualization methodology page; a second Data 4 Thought post follows)
Step: 2b
Since: 2026-09-15

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | 2026-09-14 | Pipeline, comparison, watch flags and interactive map built; live at https://data4thepeople.github.io/laus/. Tie-out in ~/.claude/plans/snazzy-sniffing-coral.md |
| 2a | Draft with brackets resolved | 2026-09-15 | Full rewrite of the Visualization methodology page modeled on the petroleum inventory page; tables in tables.html |
| 2b | Eric's edit, Claude's look-over | | |
| 2c | Slice markup | | |
| 2d | Hero 1680x1080 + alt text | | |
| 2e | SEO | | |
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
