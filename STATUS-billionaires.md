# Status: Betting the house on billionaires

Project: laus (structural labor force decline)
Process: ~/.claude/d4tp-process/PROCESS.md
Siblings: STATUS.md (Visualization methodology page, complete),
STATUS-five-takeaways.md (Data 4 Thought takeaways, complete)

## Current

Post: betting-the-house-on-billionaires
Step: 2a
Since: 2026-09-20

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | 2026-09-20 | Nebraska and Arkansas cut of the existing classified panel; DATASETS.md written; tie-out below |
| 2a | Draft with brackets resolved | | POST.md written, six brackets resolved, 12 edits proposed and all 12 accepted and applied |
| 2b | Eric's edit, Claude's look-over | | |
| 2c | Slice markup | | |
| 2d | Hero 1680x1080 + alt text | | |
| 2e | SEO | | |
| 2f | Pushed to Prismic (draft) | | |
| 2g | Mailchimp teaser | | |

## Stale

None.

## Open items

- The Prismic importer hardcodes `image/png` on upload (`to_prismic.py:561`).
  Both maps in this post are GIFs. Fix the content type before step 2f or the
  animation will not survive the push.
- Hero is not chosen. The post has no static chart, so 2d is either an AI image
  or a padded still frame from one of the two maps.
- Political content addressed in 2a: the fifth billionaire paragraph is now
  about the decisions rather than the officeholder, and the Middle East
  paragraph points at the documented conflict of interest rather than motive.
  Worth a second read at 2b with the fiscal sponsor in mind.

## Tie-out, step 1

Recomputed from `data/classified.parquet` (pull of September 14, 2026) on
2026-09-20. Every number that appears in the post:

| Claim in the post | Value | Source |
|---|---|---|
| Nebraska counties in structural loss, January 2010 | 4 of 93 | classified.parquet |
| Nebraska counties in structural loss, July 2026 | 59 of 93 (63%) | classified.parquet |
| Arkansas counties in structural loss, January 2010 | 12 of 75 | classified.parquet |
| Arkansas counties in structural loss, July 2026 | 45 of 75 (60%) | classified.parquet |
| Sarpy County, NE, July 2026 | +51.8%, Hyper-Growth, LF 114,462 | classified.parquet |
| Douglas County, NE (Omaha), July 2026 | +23.5%, Superstars, LF 333,788 | classified.parquet |
| Benton County, AR (Bentonville), July 2026 | +70.9%, Hyper-Growth, LF 176,988 | classified.parquet |
| Washington County, AR, July 2026 | +40.6%, Hyper-Growth, LF 145,184 | classified.parquet |
| Saline County, AR, July 2026 | +43.6%, Hyper-Growth, LF 70,420 | classified.parquet |
| U.S. counties in structural loss, July 2026 | 1,281 of 3,214 (40%) | classified.parquet |
| U.S. billionaires, 2026 | 989 | Forbes 2026 World's Billionaires List |

Nebraska hyper-growth counties, July 2026: Sarpy only.
Arkansas hyper-growth counties, July 2026: Benton, Saline, Washington.

## Log

- 2026-09-20 Post opened as a spin-off from five-takeaways-labor-force-decline.
  Eric brought the full draft and two animated maps (Nebraska and Arkansas,
  January 2010 to July 2026). Folder renamed from `posts/billionaires` to
  `posts/betting-the-house-on-billionaires`; the GIFs moved to `images/` as
  `01-labor-force-nebraska.gif` and `02-labor-force-arkansas.gif`.
- 2026-09-20 Step 1 closed. No new pipeline work: the post uses the existing
  classified panel filtered to NE and AR. DATASETS.md written at the project
  root, which had been missing since the first post.
- 2026-09-20 Step 1 finding that changes the text: Omaha is in Douglas County,
  which is Superstars (+23.5%), not Hyper-Growth. The only Nebraska
  hyper-growth county is Sarpy, the suburb next door. In Arkansas, Benton is
  hyper-growth as the draft says, but so are Washington and Saline, and Saline
  is a Little Rock suburb with no Walton connection. The draft's sentence about
  the darkest green counties is proposed for revision in step 2a.
- 2026-09-20 Step 2a: POST.md written with Eric's prose verbatim, six brackets
  resolved (the two GIF embeds, the Bentonville simile, and the sourcing pass),
  11 source links added inline, and a "How we measured
  this" note added after a divider. 12 edits proposed in chat as a numbered
  list, waiting on accept/reject.
- 2026-09-20 Step 2a: Eric accepted all 12 edits. Applied. The biggest one
  replaces the darkest-green sentence with the real counties: Benton at 71% in
  Arkansas, Sarpy at 52% in Nebraska with Douglas at 24%.
- 2026-09-20 House rule for this post, set by Eric: the billionaires in the
  opening section are described, never named. The link on the description is
  how a reader who does not recognize them finds out who they are. The two
  naming sentences added at 2a were removed and their links moved onto Eric's
  own descriptive phrases. Buffett and the Waltons stay named in the second
  section, where naming them is the point.
- 2026-09-20 Standing-constraint flag raised with Eric: the fiscal sponsor does
  not permit political commentary, and the draft's fifth billionaire paragraph
  attributed trade policy, immigration policy and a war to a sitting
  officeholder.
- 2026-09-20 Eric agreed. The Middle East paragraph now points at the sovereign
  wealth in the envoy's own fund instead of insinuating a motive, and was later
  broken into a question plus two one-fact sentences. The DOGE sentence was left
  alone: it names a program and a documented staffing outcome, not a party.
- 2026-09-20 The fifth billionaire paragraph was cut entirely, after two
  rewrites. The deciding reason was not risk. The other four examples are
  private people doing what government used to do, which is the thesis; a
  sitting president making trade, immigration and war decisions is the office
  doing its own job, so the paragraph argued against the section it sat in.
  The immigration point it carried moved to the maps section as one short
  paragraph on the four ways a county's labor force can change, which also sets
  up the limits note. Source swapped to the BLS foreign-born release itself:
  19.1% of the labor force in 2025.
