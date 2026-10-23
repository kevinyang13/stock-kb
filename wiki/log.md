# Operations Log

Append-only record of wiki operations. Newest entries at the bottom.

---

## 2026-10-22 — Created the wiki, added the Sankey chart page

**Source**: Three reference infographics supplied in chat (SpaceX Q3 FY26, TSMC Q3 FY26, Alphabet Q1 FY26, all by App Economy Insights). These were pasted into the conversation and are not stored in `raw/`.

**What changed**:

- Created `wiki/index.md` and this log. The `wiki/` folder existed but was empty, so neither file was present before today.
- Added `wiki/sankey-income-statement.md` — a how-to for producing the chart for any ticker: sourcing the quarterly figures, the spec schema, rendering, and verification.
- Added `bin/sankey.py`, a tested generator that turns a JSON spec into HTML and PNG.
- Added `examples/tsm-q3-fy26.json`, the TSMC reference transcribed as a spec so the renderer could be checked against a known-good image.

**Verification**: Rendered the TSMC example and compared it to the reference infographic. Layout, column order and colour semantics match. The built-in validator flagged that net profit does not foot from the reference's own rounded figures ($23.6B computed vs $23.9B printed); this is noted on the page rather than silently corrected.

**Open items**: Three pages are linked but not yet written — `income-statement-basics`, `watchlist-heatmap`, `data-sources`. The generator does not yet handle negative lines (operating loss, tax benefit), which the SpaceX reference requires.

---

## 2026-10-22 — Micron FQ4 FY26 research, chart, and a Financials tab

**Source**: Micron Form 8-K Q4 FY26 press release exhibit (sec.gov), cross-checked against stockanalysis.com for revenue growth.

**What changed**:

- Added `wiki/micron-fq4-fy26.md` with the quarter's income statement, business-unit revenue including prior-year and prior-quarter columns, and full-year figures.
- Added `examples/mu-fq4-fy26.json` and rendered `assets/financials/MU-FQ4-FY26.png` with `bin/sankey.py`.
- Added a **Financials** tab to `heatmap.html`, driven by a new `financials.json` manifest so further tickers only need a spec, an image and a manifest entry.
- Tuned `bin/sankey.py`: the sankey domain now stops at 82% of the canvas and stage headers are bottom-anchored above it. Micron's 87% gross margin makes those nodes nearly full height, and the old label positions printed on top of the bars.

**Verification**: The validator reported no drift — Micron's figures foot exactly. Rendered output checked against the reference format, and the tab checked at desktop and 375px (no horizontal overflow; KPI tiles reflow two-up).

**Noted**: Micron's four business units sum to $54,223M against $54,229M consolidated. The filing does not explain the $6M gap; recorded on the page rather than silently reconciled.

---

## 2026-10-22 — CoreWeave Q2 FY26, and a loss layout for the generator

**Source**: CoreWeave Q2 2026 results release (investors.coreweave.com), cross-checked against stockanalysis.com.

**What changed**:

- Added `wiki/coreweave-q2-fy26.md`.
- Added `examples/crwv-q2-fy26.json` and `assets/financials/CRWV-Q2-FY26.png`; CRWV now leads the Financials tab.
- Extended `bin/sankey.py` with `build_loss()`. CoreWeave's $1,696M gross profit against $1,745M of operating expenses cannot be drawn with the profit layout — the flows do not conserve. The loss layout draws the net loss as a red source funding the expense pool, and checks that gross profit + net loss equals operating expenses + below-the-line charges.
- `money()` now takes a `decimals` argument and the spec takes `unit`/`decimals`, so a $49M operating loss is not rounded to $0.0B.
- Updated `wiki/sankey-income-statement.md`: documented the loss layout and removed the stale "negative lines are not handled" limitation. A tax benefit is still unhandled.

**Verification**: CoreWeave balances exactly ($1,696M + $626M = $2,322M), no validator warning. Re-rendered the MU and TSM examples afterwards with no regression. Financials tab checked with all three entries — images load, no horizontal overflow.

**Noted**: CoreWeave's "total operating expenses" subtotal of $2,624M includes cost of revenue, unlike Micron's presentation. Recorded on the page so the next spec is not built on the wrong subtotal.

---

## 2026-10-22 — Financials tab shows one statement at a time

**What changed**: The Financials tab previously stacked every statement down one long page. It now renders a single statement with a ticker selector above it, reusing the existing `.chip` styling from the heatmap filters. Clicking a ticker swaps the card in place; the first entry in `financials.json` is selected on load.

**Verification**: Checked at desktop and 375px. One article in the DOM at a time, chip state follows the selection, the correct image loads per ticker, chips wrap on mobile, no horizontal overflow.

---

## 2026-10-22 — Income statement charts for every favorite

**Source**: stockanalysis.com quarterly income statement pages (the `/financials/income-statement/` path, which carries the full line-by-line statement; the `/financials/` overview page only has headline rows). Micron and CoreWeave keep their filing-sourced entries.

**What changed**:

- Added ten specs and charts: NVDA, QCOM, GOOG, SNDK, TSM, TSLA, INTU, SMCI, IONQ, MSFT. With MU and CRWV the Financials tab now carries twelve statements.
- Replaced the TSM entry, which had been transcribed from the App Economy Insights reference image, with filed figures in New Taiwan dollars.
- Added `wiki/favorites-financials.md` recording what is covered and the caveats.

**Generator changes**:

- `build()` now handles a **negative** other-income figure, drawing net interest expense as a charge off operating profit. INTU (-$228M) and SMCI (-$20M) need it.
- Validator tolerance is now relative (0.5% of revenue, floor 0.15) instead of a fixed 0.15, which was meaningless for statements denominated in millions.
- `build()` gained the `decimals` support that `build_loss()` already had.
- The diagram domain dropped to 77% of the canvas and the "Operating expenses" label is pinned below its column; tall bars were printing over stage labels.
- In the loss layout the net loss gets its own column. IonQ's loss is 23 times its revenue, and in the shared column that bar buried the cost-of-revenue label.

**Verification**: All twelve render with no validator warnings — every statement foots. Clicked through all twelve chips in the browser: no broken images, no horizontal overflow.

**Noted**: SMH is an ETF and has no income statement, so eleven of the twelve favorites are covered, not twelve. Only Micron has a real segment split; the others show a single revenue bar rather than invented segments.

---

## 2026-10-22 — Split the tabs into separate pages

**What changed**: The site was one `heatmap.html` with five hidden panels. It is now five pages — `heatmap.html`, `catalysts.html`, `brief.html`, `events.html`, `financials.html` — plus an `index.html` that redirects to the heatmap. The nav is links instead of buttons, and `Site.nav()` highlights the current page.

Shared code moved out of the page: `assets/site.css` (all styling) and `assets/site.js` (escaping, number formatting, sector naming, and the paced stockanalysis quote fetcher). The watchlist moved from an inline JSON block to `watchlist.json` so the heatmap and catalysts pages read one copy.

`sectorLabel()` now takes the active category filter as an argument. It used to close over the heatmap's `picked` variable, which does not exist on the other pages.

**Verification**: Each page loaded and checked in the browser — heatmap 100 tiles / 96 priced / 34 chips, catalysts 12 cards with live day moves and sector labels, brief 8 sections, events 49 calendar cells, financials 12 chips with no broken images. Root redirect lands on the heatmap.

**Noted**: `quotes.py` serves only the page and `/api/quotes`, so it cannot serve the new CSS, JS and watchlist files. Use a static server (`python3 -m http.server`) for local viewing.
