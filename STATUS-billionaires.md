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
| 2b | Eric's edit, Claude's look-over | 2026-09-20 | Eric cut the immigration paragraph and rewrote the closer; 9 look-over items proposed and all accepted |
| 2c | Slice markup | 2026-09-20 | 17 slices; one dropcap fence, one divider, two captioned GIFs, 14 links |
| 2d | Hero 1680x1080 + alt text | | Prompt 13 render in place, alt 426 chars, shipped as JPG |
| 2e | SEO | | |
| 2f | Pushed to Prismic (draft) | | |
| 2g | Mailchimp teaser | | |

## Stale

None.

## Open items

- The hero's green ring is a clean circle. The post says the maps do not prove
  causality; a perfect halo around the gold tree implies they do. Raised with
  Eric at 2d; his call.
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

- 2026-09-20 Step 2d: hero settled on the seventh prompt. A drone view of a
  dead orchard running to the horizon with one enormous tree cast in solid gold
  at the center and a tight ring of living green at its base. Seven rounds: the
  farmhouse on coin columns, the green island and the tilted scale were
  rejected; the bridge, lit grid and one-tree set followed; Eric took the one
  tree and added the gradient; then bigger and living; then dead trees to the
  horizon; then literal metal rather than autumn leaves. Scrooge McDuck and
  Mr. Burns were asked about and declined as owned characters; the vault and
  diving board was offered as the archetype instead and not used.
- 2026-09-20 Hero shipped as JPG, not the PNG the process names. The same frame
  is 3.8 MB as PNG and 1.06 MB as JPG at quality 92, because PNG is the wrong
  container for a photograph. The importer reads the hero path from front
  matter and does not care about the extension. Worth folding back into
  PROCESS.md as "PNG for chart heroes, JPG for photographic ones".

- 2026-09-20 Prompt 1 rejected. Hero concept back open; Eric is working on
  other directions before any new prompts are written.

- 2026-09-20 Step 2c confirmed. Step 2d opened on the AI image path. Eric ruled
  out a still frame of either state map as the hero. Three prompts written;
  Eric chose prompt 1, the clapboard farmhouse with no foundation resting on
  five widely spaced columns of stacked coins, one patch of green grass at the
  base of one column.

- 2026-09-20 Step 2b confirmed. Step 2c opened.
- 2026-09-20 Step 2c: one fence added, `::: dropcap` above "Lately, it feels
  like America is only as strong as its billionaires", because the post opens
  with the disclaimer blurb and the automatic first-paragraph drop cap would
  have landed on the disclaimer. Everything else came from the defaults.
  Convert-only run gives 17 slices. Captions and the source line keep their
  italics, all 14 links carry target=_blank, both alt texts are under 500
  characters (364 and 377).
- 2026-09-20 Importer fixed and pushed (commit 6094214 in ~/.claude/tools/prismic):
  asset uploads hardcoded `image/png`, which would have stripped the animation
  from both GIFs at 2f. It now reads the type from the file suffix and falls
  back to PNG for anything unrecognized.

- 2026-09-20 Step 2b: Eric edited POST.md directly. He cut the immigration
  paragraph, split the Benton/Sarpy/Douglas numbers into their own sentences,
  quantified the concentration-risk opener, and replaced the closing line with
  "we have no say. Money talks." Look-over found 9 items, all accepted: the
  $8.4 trillion figure and its link, two county capitalizations, a missing
  percent sign, Sarpy described as a suburb rather than a county, "in such few
  people", a missing denominator, a trailing space, "median" to "typical", and
  the original "America is only as strong as its billionaires" restored as the
  last line so the closing echoes the opening.
- 2026-09-20 Closing trimmed: "We are only as strong as those who hold the
  money" cut, because it restated the line right after it. Ending is now
  "we have no say. Money talks. America is only as strong as its billionaires."

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
