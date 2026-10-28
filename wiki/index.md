# Wiki Index

Table of contents for this knowledge base. One line per page.

## Charts and visualisation

- [[sankey-income-statement]] — how to build an App-Economy-Insights-style Sankey income statement chart for a given stock symbol, end to end.

## Automation

- `.claude/skills/income-statement-chart/SKILL.md` — the skill that turns a bare ticker into a published income statement chart. Encodes the chartable gate, the mandatory segment breakdown, and the source traps.
- `bin/yoyfetch.py` — adds the year-ago figure for each income statement node, keeping only the lines whose basis matches what the chart draws.
- `bin/sadata.py` — reads a statement from stockanalysis.com's SvelteKit data endpoint and hydrates devalue's flattened payload. Shared by both fetchers.
- `bin/debtfetch.py` — builds a debt/coverage spec for every statement on the Financials page, pulling the balance sheet and cash flow column that matches the quarter the card already shows.
- `bin/debtbars.py` — the debt/coverage grouped bar chart that sits under the Sankey on the Financials card: debt, free cash flow and cash for the quarter the card covers. Same figure-JSON pipeline, same renderer.
- `bin/stamp.py` — versions the shared CSS and JS links in every page, so an edit under `assets/` cannot hide behind a browser's cached copy.

## Strategy

- [[options-wheel-strategy]] — the cash-secured put / covered call wheel on MU, SMH, MSFT, GOOG and TSLA: the rules, what the $3,000-a-week target actually requires, and the six-point entry checklist.

## Companies

- [[earnings-surprise-chart]] — the actual-vs-estimate EPS dots on each Financials card: where the figures come from, and why they are not the EPS the income statement beside them is built from.
- [[favorites-financials]] — index of the 67 income statement charts on the Financials tab, which of them carry a reported revenue segment split (53 do) and the data caveats that apply to them.
- [[coreweave-q2-fy26]] — CoreWeave Q2 2026: $2,575M revenue (+112% Y/Y), 66% gross margin, a $49M operating loss and a $626M net loss driven by financing cost.
- [[nebius-q2-fy26]] — Nebius Group Q2 2026: $582.3M revenue (+454% Y/Y) at a 77% gross margin, a $190.4M net loss that is almost all depreciation and interest, and capex running at eight times revenue.
- [[visa-q4-fy26]] — Visa fiscal Q4 2026: $12,139M of net revenue (+13% Y/Y) with no cost of revenue at all, a 60% operating margin, and $5,123M of client incentives netted out of revenue before the statement starts.
- [[micron-fq4-fy26]] — Micron's record fiscal Q4 2026: $54.2B revenue (+379% Y/Y), 87% gross margin, business-unit breakdown and the figures behind the Financials tab chart.

## Pages referenced but not yet written

These are linked from existing pages and still need to be created:

- `income-statement-basics` — the line items and identities a P&L has to satisfy.
- `watchlist-heatmap` — how `heatmap.html` is built, its data blocks, and the refresh jobs behind the Catalysts, Morning Brief and Events tabs.
- `data-sources` — which price, fundamentals and news sources this repo uses, and which ones block automated access.
