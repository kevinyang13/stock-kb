# Wiki Index

Table of contents for this knowledge base. One line per page.

## Charts and visualisation

- [[sankey-income-statement]] — how to build an App-Economy-Insights-style Sankey income statement chart for a given stock symbol, end to end.

## Automation

- `.claude/skills/income-statement-chart/SKILL.md` — the skill that turns a bare ticker into a published income statement chart. Encodes the chartable gate, the mandatory segment breakdown, and the source traps.
- `bin/debtbars.py` — the debt/coverage grouped bar chart that sits under the Sankey on the Financials card: debt, free cash flow and cash for the quarter the card covers. Same figure-JSON pipeline, same renderer.
- `bin/stamp.py` — versions the shared CSS and JS links in every page, so an edit under `assets/` cannot hide behind a browser's cached copy.

## Strategy

- [[options-wheel-strategy]] — the cash-secured put / covered call wheel on MU, SMH, MSFT, GOOG and TSLA: the rules, what the $3,000-a-week target actually requires, and the six-point entry checklist.

## Companies

- [[favorites-financials]] — index of the 66 income statement charts on the Financials tab, with the data caveats that apply to them.
- [[coreweave-q2-fy26]] — CoreWeave Q2 2026: $2,575M revenue (+112% Y/Y), 66% gross margin, a $49M operating loss and a $626M net loss driven by financing cost.
- [[nebius-q2-fy26]] — Nebius Group Q2 2026: $582.3M revenue (+454% Y/Y) at a 77% gross margin, a $190.4M net loss that is almost all depreciation and interest, and capex running at eight times revenue.
- [[micron-fq4-fy26]] — Micron's record fiscal Q4 2026: $54.2B revenue (+379% Y/Y), 87% gross margin, business-unit breakdown and the figures behind the Financials tab chart.

## Pages referenced but not yet written

These are linked from existing pages and still need to be created:

- `income-statement-basics` — the line items and identities a P&L has to satisfy.
- `watchlist-heatmap` — how `heatmap.html` is built, its data blocks, and the refresh jobs behind the Catalysts, Morning Brief and Events tabs.
- `data-sources` — which price, fundamentals and news sources this repo uses, and which ones block automated access.
