# Labor force history by county

Every U.S. county and Puerto Rico municipio, classified by the change in its
civilian labor force against the same month 20 years earlier, month by month
since January 2010. Built by Data 4 The People.

- Live visualization: https://data4thepeople.github.io/laus/
- Methodology: https://www.data4thepeople.com/p/labor-force-history-viz

Source: U.S. Bureau of Labor Statistics, Local Area Unemployment Statistics
(LAUS), county civilian labor force, not seasonally adjusted. County shapes:
U.S. Census Bureau 2024 cartographic boundary files, 1:5,000,000.

## Rebuild it

Requires Python 3.12 and an internet connection.

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e ".[map,dev]"

.venv/bin/python -m lfd.ingest     # download BLS files (~340 MB), write the monthly panel
.venv/bin/python -m lfd.classify   # 20-year same-month change and the six bands
.venv/bin/python -m lfd.watch      # positive and negative watch flags
.venv/bin/python -m lfd.geo        # county shapes, projected with AK, HI and PR insets
.venv/bin/python -m lfd.viz        # write dist/index.html
```

Run the tests with `.venv/bin/python -m pytest`. Compare two months with
`.venv/bin/python -m lfd.compare 2025-07 2026-07`.

## Where things live

| What | Where |
|---|---|
| Band edges and labels | `src/lfd/classify.py` (`BINS`, `LABELS`) |
| Watch flag thresholds | `src/lfd/watch.py` |
| Band colors | `src/lfd/viz.py` (`COLORS`) |
| The page template | `src/lfd/templates/index.html` |

Downloaded and generated data files are not stored in the repository. The
commands above recreate them.

Questions or a different result: connect@data4thepeople.com
