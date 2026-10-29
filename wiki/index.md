# Wiki Index

Table of contents for this knowledge base. One line per page.

## Charts and visualisation

- [[sankey-income-statement]] — how to build an App-Economy-Insights-style Sankey income statement chart for a given stock symbol, end to end.

## Automation

- `.claude/skills/add-ticker/SKILL.md` — the skill that puts a new ticker everywhere it belongs: heatmap tile, IBKR watchlist, Financials card, events calendar, and the Catalysts and Morning Brief tabs when it is a favorite. Calls the income statement skill for the statement itself.
- `.claude/skills/income-statement-chart/SKILL.md` — the skill that turns a bare ticker into a published income statement chart. Encodes the chartable gate, the mandatory segment breakdown, and the source traps.
- `bin/yoyfetch.py` — adds the year-ago figure for each income statement node, keeping only the lines whose basis matches what the chart draws.
- `bin/sadata.py` — reads a statement from stockanalysis.com's SvelteKit data endpoint and hydrates devalue's flattened payload. Shared by both fetchers.
- `bin/debtfetch.py` — builds a debt/coverage spec for every statement on the Financials page, pulling the balance sheet and cash flow column that matches the quarter the card already shows.
- `bin/debtbars.py` — the debt/coverage grouped bar chart that sits under the Sankey on the Financials card: debt, free cash flow and cash for the quarter the card covers. Same figure-JSON pipeline, same renderer.
- `quotes.py --events` — refreshes `events.json`. Keeps a published date that has already passed for 10 days, because a past date is a fact (the day the company reported) while a future one may be a stale leftover; preserves the curated macro, Fed, corporate and market-holiday entries, which are never fetched.
- `bin/ownfetch.py` — builds the ownership spec for every Financials card: slice sizes from stockanalysis, the index/active split and the named holders from the SEC's own Form 13F data set. Checks each filing's implied price before trusting its share count.
- `bin/ownpie.py` — the share-ownership donut that sits beside the sankey, with the top five holders of each institutional slice on hover. Same figure-JSON pipeline, same renderer.
- `bin/passive-managers.json` — the managers counted as index and ETF rather than active. An editorial list, deliberately conservative, kept out of the code so it can be audited.
- `bin/stamp.py` — versions the shared CSS and JS links in every page, so an edit under `assets/` cannot hide behind a browser's cached copy.
- `prices.json` — the committed price snapshot the published site reads, because every quote feed refuses a cross-origin request from the Pages origin. Carries `generated`, `generatedLabel`, `source` and `quotes[{t, price, pct}]`; the writer is not built yet, so the file ships empty.

## Strategy

- [[options-wheel-strategy]] — the cash-secured put / covered call wheel on MU, SMH, MSFT, GOOG and TSLA: the rules, what the $3,000-a-week target actually requires, and the six-point entry checklist.

## Companies

- [[earnings-surprise-chart]] — the actual-vs-estimate EPS dots on each Financials card: where the figures come from, and why they are not the EPS the income statement beside them is built from.
- [[share-ownership-donut]] — the "Who owns the shares" chart on each Financials card: four slices of the whole share count, the five largest holders named on hover from their own 13F, and why the slice sizes and the holder names have to come from different sources.
- [[favorites-financials]] — index of the 70 income statement charts on the Financials tab, which of them carry a reported revenue segment split (56 do) and the data caveats that apply to them.
- [[coreweave-q2-fy26]] — CoreWeave Q2 2026: $2,575M revenue (+112% Y/Y), 66% gross margin, a $49M operating loss and a $626M net loss driven by financing cost.
- [[nebius-q2-fy26]] — Nebius Group Q2 2026: $582.3M revenue (+454% Y/Y) at a 77% gross margin, a $190.4M net loss that is almost all depreciation and interest, and capex running at eight times revenue.
- [[visa-q4-fy26]] — Visa fiscal Q4 2026: $12,139M of net revenue (+13% Y/Y) with no cost of revenue at all, a 60% operating margin, and $5,123M of client incentives netted out of revenue before the statement starts.
- [[vertiv-q2-fy26]] — Vertiv Holdings Q2 2026: $3,274.3M of net sales (+24% Y/Y) at a 38% gross margin, growth that is almost entirely the Americas, and the last quarter filed before the Oct 28, 2026 Q3 release.
- [[micron-fq4-fy26]] — Micron's record fiscal Q4 2026: $54.2B revenue (+379% Y/Y), 87% gross margin, business-unit breakdown and the figures behind the Financials tab chart.
- [[alphabet-q3-fy26]] — Alphabet Q3 2026: $127,577M revenue (+25% Y/Y) and operating income up 30%, but net income down 24% on a $20,980M swing in other income; Cloud more than doubled and free cash flow went negative.
- [[microsoft-fq1-fy27]] — Microsoft fiscal Q1 2027: $92,279M revenue (+19% Y/Y) at a 50% operating margin, Azure +48% and 36% of the company, Windows OEM and devices −22%, and the segments recast from three to two.
- [[servicenow-q3-fy26]] — ServiceNow Q3 2026: $4,106M revenue (+20.5% Y/Y) with operating income down 33%, cost of subscription revenue up 58%, and $7,524M of debt where there was $1,491M at the start of the year.
- [[vertiv-q3-fy26]] — Vertiv Q3 2026: $4,312.8M of net sales (+61% Y/Y), $463M above the top of its own guidance, organic orders up over 100%, and a balance sheet that flipped to net cash.
- [[ge-vernova-q3-fy26]] — GE Vernova Q3 2026: $12,642M revenue (+27% Y/Y) with operating income up 281%, $29.3B of orders (+96% organic) and a $197B backlog; the first card in the repo sourced from a 10-Q.
- [[iren-fq4-fy26]] — IREN fiscal Q4 2026: $137.2M revenue (−27% Y/Y) and a $684.0M net loss of which $450.4M is one impairment; the first quarter AI Cloud revenue passed Bitcoin Mining. Quarter derived from the 10-K minus the 10-Q.
- [[sandisk-fq1-fy27]] — Sandisk fiscal Q1 2027: $11,031M revenue (+378% Y/Y) at an 85% gross margin, Datacenter from $269M to $4,802M in a year, and an eight-for-one stock split announced alongside.
- [[amazon-q3-fy26]] — Amazon Q3 2026: $201.9B revenue (+12% Y/Y) with operating income up 61%, AWS +39% and accelerating for a fifth quarter, and net income down 2% on a $12B non-operating swing.
- [[intel-q3-fy26]] — Intel Q3 2026: $16,513M revenue (+21% Y/Y), operating income up 269%, Data Center & AI +78%, and a 17% larger share count after a $23B equity offering.
- [[coinbase-q3-fy26]] — Coinbase Q3 2026: $1,215.6M revenue (−35% Y/Y) at a 5% operating margin, and a 59% net margin that is almost entirely a $715M mark on its own crypto holdings.

## Pages referenced but not yet written

These are linked from existing pages and still need to be created:

- `income-statement-basics` — the line items and identities a P&L has to satisfy.
- `watchlist-heatmap` — how `heatmap.html` is built, its data blocks, and the refresh jobs behind the Catalysts, Morning Brief and Events tabs.
- `data-sources` — which price, fundamentals and news sources this repo uses, and which ones block automated access.
