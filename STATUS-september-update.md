# Status: September 2026 update

Project: laus (structural labor force decline)
Process: ~/.claude/d4tp-process/PROCESS.md
Siblings: STATUS.md (Visualization methodology page, complete),
STATUS-five-takeaways.md (Data 4 Thought takeaways, complete),
STATUS-billionaires.md (Betting the house on billionaires, complete)

## Current

Post: labor-force-september-2026
Step: 2f
Since: 2026-11-03

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | 2026-11-03 | Six beats; findings in docs/SEPTEMBER-FINDINGS.md; tie-outs in TIEOUT.md |
| 2a | Draft with brackets resolved | 2026-11-03 | Reconfirmed after the pivot to a short national update; three charts plus live map; four independent tie-outs |
| 2b | Eric's edit, Claude's look-over | 2026-11-04 | Reopened Nov 4 for Eric's Prismic edits; Michigan chart (sep26-03) back in, retitled |
| 2c | Slice markup | 2026-11-04 | Re-run after 2b: 35 blocks, 22 slices, 4 charts |
| 2d | Hero 1680x1080 + alt text | 2026-11-04 | Reconfirmed; September chart, padded; alt 393 chars |
| 2e | SEO | 2026-11-04 | Reconfirmed; description updated to match the rewrite |
| 2f | Pushed to Prismic (draft) | | |
| 2g | Mailchimp teaser | | |

## Stale

- 2f (2026-11-04): back to 2b; Eric made many changes to the text. 2f draft in Prismic (auqkIhIAACwAbEjm) is out of date; re-run 2c to 2f, and the importer will update the same draft.


## Log

- 2026-11-02 Step 1 opened. Topic: September 2026 update. BLS posted new LAUS county files on Oct 28; the panel now runs through Sep 2026 and the live viz is already rebuilt (commit f77c3d9). Starting figures: Sep 2026, 1,132 of 3,214 counties in Structural Loss (35.2%); Sep 2025 to Sep 2026, +40 on the 3,207 counties in both months.
- 2026-11-02 Hero idea from Eric for 2d: an AI image of the Michigan state flag at half staff. Use it as the starting prompt in hero-prompt.md.
- 2026-11-02 Michigan check: the 20 flips sit in the "balance of Michigan" LAUS model area (77 counties, -8.7% yoy); the six Detroit metro counties rose 0.6%. CES payroll jobs in Michigan are flat. Findings in docs/SEPTEMBER-FINDINGS.md. Waiting on Eric for the spotlight framing.
- 2026-11-02 Eric chose the framing: Michigan spotlight as "the map turned in 2026, here is what is behind it" (Detroit vs rest-of-state model split, flat payroll and QCEW jobs, trade with Canada and tariff dates as context with the timing caveat).
- 2026-11-02 Tariff timeline done (docs/TARIFF-TIMELINE.md, primary sources; Section 338 proclamations 11048 and 11076 spot-checked in the Federal Register API).
- 2026-11-03 Tariff piece shelved. Beat 1 shows the last 15 Septembers; July record dropped. Own and independent tie-outs done (TIEOUT.md): no number differences; fixes made to the Canada chart title, revision wording, Puerto Rico label and DATASETS.md. Jobs chart now compares employed residents with payroll jobs. Eric chose to explain the Michigan drop with the CPS participation finding, stated as lower confidence and directional because the sample is small.
- 2026-11-03 Second independent tie-out (jobs chart, CPS): values match; prime-age outside-Detroit change and CPS age split not supported. Eric chose beat 5: published LAUS participation rate first, CPS statewide direction at lower confidence, Census estimates for aging; prime-age and age-split numbers left out. "Nonfarm" added to the jobs chart subtitle.
- 2026-11-03 Step 1 confirmed by Eric. Next: 2a, needs a slug.
- 2026-11-03 Step 2a opened. Slug: michigan-map-turned. posts/michigan-map-turned/ created; four charts copied to images/. Waiting for Eric's draft.
- 2026-11-03 Title changed to "Where did Michigan's workers go?" with a new subtitle; slug changed from michigan-map-turned to where-did-michigans-workers-go (folder renamed). Canada chart dropped; the last section becomes Eric's close.
- 2026-11-03 Third independent tie-out: numbers match; chart 8's "outside the big metros" framing flagged because Michigan's other metros fell 8% to 10%. Eric chose to swap chart 8 for rest of Michigan vs rest of Ohio (BLS balance-of-state areas) and add a sentence with the metro numbers.
- 2026-11-03 Revision caveat added to the "largest drop of any state" sentence, per Eric.
- 2026-11-03 Step 2a confirmed by Eric. Next: 2b, Eric's edit and Claude's look-over.
- 2026-11-03 Step 2b opened. Waiting for Eric's edit of POST.md.
- 2026-11-03 Employed residents vs payroll jobs check: Michigan's gap (-3.7 points, Sep 2026) is rare but shared by 17 states with gaps of 2+ points; QCEW sides with payroll. Eric: the CPS vs CES gap needs its own study; the post pivots to a short national update until he vets the CPS data. Slug changed to labor-force-september-2026; Michigan sections and six Michigan charts dropped from the post (kept in outputs/ and git history); trade and tariff sources removed from DATASETS.md. Back to 2a.
- 2026-11-03 Added chart and section on all six bands, every September since 2012. Eric: CES is not trusted either; the note section now uses CPS response rates (LNU09300000) and LAUS employed residents vs QCEW by state. DATASETS.md trimmed to LAUS, QCEW state totals and the CPS response rate; CES, CPS microdata, population estimates and OMB sections removed.
- 2026-11-03 Eric: use CES for the months QCEW does not cover, and chart the number of states with a 2+ point gap over time. Added sep26-11-state-gaps.png and rewrote the check paragraphs; CES section back in DATASETS.md. Also found that state CPS response rates can be computed from the microdata (HRINTSTA; matches BLS national 89.8% and 65.7% exactly); not in the post, for Eric's study.
- 2026-11-03 Note section cut to one chart (state gaps) and three short paragraphs, per Eric; response-rate chart removed from the post (kept in outputs/). Eric's paragraph on 2020 and the refinery analogy added after the chart (typo fixes only). Follow-up study notes in docs/FOLLOWUP-CPS-QCEW-GAP.md.
- 2026-11-03 Eric removed the response-rate paragraph; response rates are no longer in the post (DATASETS.md section removed; notes stay in docs/FOLLOWUP-CPS-QCEW-GAP.md).
- 2026-11-03 Eric's closing paragraph added; "worsening response rates" links to the BLS response-rate page; response-rate source restored in DATASETS.md.

- 2026-11-03: Eric accepted edits 1-4 and 6-10 (rejected 5, title unchanged): subtitle and body wording, Katrina bullet corrected, cause bullet rewritten, state-gap chart retitled for June 2026 (two-line title).

- 2026-11-03: Eric edited the caution paragraph; accepted wording fix and a reading guide for the state-gap chart (Michigan example: -5.0% vs +0.03%, from data/ces/state_gaps_monthly.csv).

- 2026-11-03: Eric edited the chart walk-through and refinery paragraph; accepted paragraph split, source wording, and "roughly agree" fix.
- 2026-11-03 Step 2a done (reconfirmed after the pivot).
- 2026-11-03 Step 2b opened.
- 2026-11-03 2b look-over: accepted items 1-4 (numeral start, QCEW defined, "measures" not "surveys", unused image removed).
- 2026-11-03 Step 2b done.
- 2026-11-03 Step 2c opened. HTML note removed from POST.md (it had become the drop cap). Embed still fits 780px at desktop widths (checked at 600, 780, 1000, 1280).
- 2026-11-03 Step 2c done.
- 2026-11-03 Step 2d opened.
- 2026-11-03 Hero: September structural-loss chart padded to 1680x1080 (hero pad); hero_alt set.
- 2026-11-03 Step 2d done.
- 2026-11-03 Step 2e: meta title, description, keywords written; links to labor-force-history-viz and five-takeaways added.
- 2026-11-03 Step 2e done.
- 2026-11-03 Step 2f: date set to 2026-11-04, time 06:30 Eastern (EST, -05:00; DST ended Nov 1). Pushed to Prismic as draft auqkIhIAACwAbEjm in the Migration Release; 4 images uploaded. Tags and author empty.
- 2026-11-04 Back to 2b (Eric: "i ended up making a lot of changes"). First section in: "But can we trust the latest data?", with the Michigan employed vs payroll chart (sep26-03) back in per his bracket.
- 2026-11-04 2b: accepted 1, 2, 3, 5, 6 on the data-trust section; Michigan chart retitled; DATASETS.md covers the SA Michigan series.
- 2026-11-04 Step 2b done (second time). 2c, 2d, 2e and 2f to re-run.
- 2026-11-04 Step 2c re-run: 35 blocks, 22 slices, 4 chart images (Michigan chart sep26-03 new).
- 2026-11-04 Step 2c done (re-run).
- 2026-11-04 Step 2d re-check: hero unchanged, hero check ok, source matches the September chart.
- 2026-11-04 Step 2d done (reconfirmed).
- 2026-11-04 Step 2e re-check: meta description updated to match the rewrite.
- 2026-11-04 Step 2e done (reconfirmed).
- 2026-11-04 Step 2f re-run: draft auqkIhIAACwAbEjm updated in the Migration Release (22 slices; Michigan chart uploaded). Date 2026-11-04, 06:30 Eastern.
