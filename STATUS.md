# Status

Project: laus (structural labor force decline)
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: labor-force-history-viz (complete)
Step: complete
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
| 2f | Pushed to Prismic (draft) | 2026-09-15 | Update of live doc abfuCxQAACYAxMRO in the Migration Release; tables inline (Default variation); limitations blurb; divider before FAQ; embed margin reset |
| 2g | Mailchimp teaser | 2026-09-15 | Rebuild announcement only; Nebraska watch-flag image; feature lead-ins bolded |

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
- 2026-09-15 Embed fix: on wide screens the page ran past the 780px frame and scrolled inside it. The map now shrinks to fit when embedded at 680px or wider, and the footer method line is hidden when framed. Checked in a real 780px iframe at 820 to 1800 wide. Table embeds re-pushed in the Default (text-column) variation; the map iframe stays Full Width.
- 2026-09-15 Second scrollbar traced to the site: each embed renders inside its own iframe with an 8px default body margin, so a 780px map overflowed its 780px slice by 16px. The importer now adds a margin reset to every iframe embed. Draft re-pushed. (Eric's other double scrollbar was a cached copy of the old viz.)
- 2026-09-15 Step 2f done. Step 2g opened: announcement email for the rebuild and new functionality only.
- 2026-09-15 Step 2g: EMAIL.md drafted as a rebuild announcement (no findings in the text). Image: Nebraska map with watch flags, cropped so it carries no numbers. Email hero JPG 206KB. Waiting on approve or reject.
- 2026-09-15 Step 2g: Eric approved the email with the five feature lead-ins bolded.
- 2026-09-15 Step 2g done. labor-force-history-viz complete: every step 1 through 2g confirmed. Next: the Data 4 Thought main-takeaways post, with its own STATUS file.
- 2026-09-15 Social video: posts/labor-force-history-viz/labor-force-history-viz-timelapse-1080p.mp4, 1920x1080, 38.7s, 7.5 MB. Jan 2010 to Jul 2026 at 6 months a second (the page's 2x speed), Saginaw pinned. Rebuild with scripts/make_video.py after each data update.
- 2026-09-15 After completion: added a limitations note on the January 2026 population-control break and the within-year slowdown (checked against the national CPS series and the BLS control-adjustment table). POST.md edited and the Prismic draft re-pushed; formally this reopens 2b through 2f if Eric wants the gates re-run.
- 2026-09-15 Research for the takeaways post saved to docs/RECOVERY-RESEARCH.md: South Carolina (39 of 46 counties recovering) is migration plus rising participation, not projects; North Dakota (36 of 53) is mostly unexplained and already flattening. Includes the national migration test and the note that the watch rule lags.
- 2026-09-16 Second post opened with its own status file, STATUS-five-takeaways.md: five-takeaways-labor-force-decline, the Data 4 Thought takeaways piece.
