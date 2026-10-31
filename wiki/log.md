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

---

## 2026-10-23 — Revenue broken out by segment

**Source**: each company's own quarterly release. stockanalysis.com's `revenue-by-segment` page was tried first and rejected: its figures are annual even with `?p=quarterly`, and NVDA's two segments there sum to $303B against $96.2B of quarterly revenue.

**What changed**: Nine of the twelve statements now show revenue split by reported segment instead of a single bar — NVDA, MSFT, GOOG, MU, SNDK, TSM, TSLA, QCOM, INTU. SMCI, IONQ and CRWV keep one bar, because no split is published (Supermicro) or only one revenue line exists (the other two).

**Verification**: every split was checked against the revenue total before being used. MSFT, GOOG, QCOM and SNDK foot exactly. TSLA is out by $44M on $28.0B and TSM by NT$0.1B, both rounding and both inside the validator's relative tolerance. All twelve re-rendered with no validator warnings, and all twelve chips were clicked in the browser with no broken images.

**Noted**: two segment sets are derived rather than reported. TSMC publishes platform mix only as rounded percentages, applied here to revenue. Intuit's Global Business Solutions is shown as the remainder so its two segments foot, since the release rounds it to $3.4B. NVIDIA reorganised its segments this quarter — Gaming, Professional Visualization and Automotive are gone, replaced by an Edge Computing line.

---

## 2026-10-23 — Added Meta, and a source conflict worth recording

**Source**: Meta Form 8-K, Q3 2026 results exhibit (quarter ended Sep 30, 2026), with the cost lines from stockanalysis.com.

**What changed**: Added `examples/meta-q3-fy26.json` and `assets/financials/META-Q3-FY26.png`; the Financials tab now carries thirteen statements. Segments are Advertising $63,061M, other Family of Apps $1,097M and Reality Labs $443M, which foot to revenue exactly.

**Conflict found**: stockanalysis.com reports Meta's Q3 operating income as **$22,878M**; the 8-K reports **$12,988M**. The difference is a $9,890M operating charge that the aggregator places below the operating line. The chart follows the filing: revenue less cost of revenue, R&D, marketing/G&A and that charge gives $12,988M, and pretax of $13,001M then follows from $13M of interest and other. This is the first disagreement between the two sources on a headline line rather than on rounding, and it is now noted on `wiki/favorites-financials.md`.

**Also noted**: Reality Labs earned $443M and lost $4,129M at the operating line, against Family of Apps operating income of $17,117M.

**Verification**: the statement foots with no validator warning. Thirteen chips render on the Financials tab with the Meta chart loading correctly.

---

## 2026-10-23 — META marked as a favorite

**What changed**: `watchlist.json` now carries `"fav": true` on META, taking the favorites from twelve to thirteen: MU, SNDK, SMH, NVDA, TSM, TSLA, SMCI, QCOM, GOOG, META, MSFT, INTU, IONQ.

**Verification**: the heatmap renders thirteen starred tiles and META is one of them.

**Follow-on**: the favorites list is read at generation time by the Morning Brief and the Events calendar, so META will not appear in the brief's favorites section or carry the `fav` flag on its earnings until those files are next refreshed.

---

## 2026-10-23 — SPCX added as a favorite, and tax benefits now draw

**What changed**: SPCX marked `"fav": true` in `watchlist.json`, taking favorites to fourteen. Added `examples/spcx-q3-fy26.json` and `assets/financials/SPCX-Q3-FY26.png`; the Financials tab now carries fourteen statements.

**Generator**: `build()` handles a **negative** tax line. A tax benefit adds to profit, so it is drawn as a green Tax benefit node flowing into net profit rather than a charge out of operating profit. This was the last limitation listed on `wiki/sankey-income-statement.md`, and it was the SpaceX reference image that originally exposed it.

**Figures**: revenue $14,575M (+161% Y/Y), gross $9,103M, operating $4,019M, net $4,404M — net exceeds pretax ($4,014M) because of the $390M tax benefit. Segments are Super Intelligence $7,600M, Connectivity/Starlink $5,250M (+69%), Space $1,770M.

**Source conflict noted**: the App Economy Insights reference chart for this same quarter shows operating profit of $2.8B and R&D of $4.6B against the filed $4,019M and $3,574M used here. The segment split agrees between the two. Recorded on the card.

**Verification**: SPCX foots with no validator warning. Re-rendered NVDA, INTU, META, MU and GOOG afterwards with no regression — the tax-benefit branch does not touch the positive-tax path. Fourteen chips render on the tab.

---

## 2026-10-23 — Nintendo added

**Source**: stockanalysis.com quarterly income statement for Tokyo 7974; segment split from Nintendo's own Q1 FY27 results release (nintendo.co.jp, Aug 6 2026).

**What changed**: Added `examples/ntdoy-q1-fy27.json` and `assets/financials/7974-Q1-FY27.png`. Fifteen statements on the Financials tab. Nintendo is the first entry that is not in the watchlist — the tab is manifest-driven, so that works without any page change.

**Figures**: revenue ¥517.8B (-10% Y/Y), gross ¥281.4B (54%), operating ¥142.6B (28%), net ¥147.4B. Segments are Dedicated video game platform ¥483.0B (-13%) and IP related income ¥34.8B (+107%), which foot to revenue exactly.

**Noted**: revenue fell 10% while operating profit rose roughly 150% — the prior-year quarter was the Switch 2 launch. Net profit exceeds operating profit because ¥63.5B of non-operating income (mostly FX and interest on cash) sits below the line. Cost of sales also absorbed about $300M of IEEPA tariff refunds. Nintendo does not split R&D out of SG&A, so operating expenses are one line.

**Verification**: foots with no validator warning; fifteen chips render and the yen figures display correctly.

---

## 2026-10-23 — Nintendo converted to USD

**What changed**: The Nintendo chart and card now show US dollars instead of yen, so it is directly comparable with the other fourteen statements. The filed yen figures are kept in the card's notes.

**Rate**: USD/JPY **156.87**, as of Oct 23 2026, confirmed against two independent sources — CNBC quoted 156.86 and IBKR IDEALPRO quoted 156.8675 (bid 156.79 / ask 156.945).

**Converted**: revenue ¥517.8B → $3,301M, gross ¥281.4B → $1,794M, operating ¥142.6B → $909M, net ¥147.4B → $940M. Segments: platform $3,079M, IP related income $222M.

**Noted**: every dollar figure on this card is derived, not filed, and moves with the exchange rate. The rate, its date and both sources are recorded on the card so the conversion can be audited or redone. Margins are unaffected by the conversion.

**Verification**: all identities still foot after conversion (gross $1,794M, operating $909M, net $940M) with no validator warning.

---

## 2026-10-23 — Site named Stock Signal Desk

**What changed**: The site had no name of its own — `HEATMAP` was the masthead on every page, so each page branded itself as the heatmap, and `index.html` separately called it "Stock KB". The masthead is now **STOCK SIGNAL DESK** across all pages, with the page's own name in the strapline (`Heatmap — colored by the day's move`, `Financials — where the money goes`, and so on). Titles follow the same pattern: `Stock Signal Desk · Heatmap`.

**Call Sheet wired in**: `tracker.html` was orphaned — reachable only by typing the URL, linked from nothing. It now carries the same masthead and nav as the other pages and appears as the sixth nav item. It keeps its own stylesheet, so the nav styles were copied across and its oversized hero masthead was reduced to match the compact bar the other pages use.

**Verification**: all six pages load with the new masthead, the nav highlights the current page (`Site.nav()` on the five shared-CSS pages, hardcoded on the Call Sheet since it does not load `site.js`), and the heatmap still renders 100 tiles.

---

## 2026-10-23 — Income statements for the whole watchlist

**What changed**: The Financials tab went from 15 statements to **65**. Added 50 charts covering every remaining watchlist name that files an income statement.

**Classification first**: of the 100 watchlist symbols, 25 are ETFs or funds and have no income statement, 6 are shells with no usable filing (CLBR, CCXI, BITF, BCII, MFH, XNET), and 4 more were excluded after fetching — SPCE, QUBT and CAN report **negative gross profit** (cost of revenue exceeds revenue, so there is no flow to draw) and HQ reports no revenue line at all.

**New tool**: `bin/mkspec.py` turns a row of income statement figures into a spec, picking the profit or loss layout automatically. It derives two bridging lines so every statement foots: cost of revenue as revenue minus reported gross profit, and the non-operating line as net plus tax minus operating profit. This was necessary because sources routinely report a cost of revenue that does not reconcile with their own gross profit — GE was out by $1,020M and IBM by $114M, both caught by the validator.

**Generator**: `build_loss()` gained a non-operating income source. MSTR's charges exceed gross profit plus its net loss, because non-operating income covered part of the burn; without a second source the loss layout could not balance.

**Verification**: every one of the 65 renders with no validator warning. All 65 chips clicked in the browser — no broken images, no horizontal overflow.

**Noted**: all 50 new charts show a single revenue bar. Segment splits were pulled only for the names done earlier by hand. Several statements are in non-USD currencies as filed — SKHY in Korean won, ASML in euro, MDA in Canadian dollars, TSM in New Taiwan dollars — and their cards say so.

---

## 2026-10-23 — Segment breakdown made mandatory, and a skill to enforce it

**Why**: the bulk watchlist pass produced 50 charts with a single "Total revenue" bar. That was a
shortcut, and left unwritten it would quietly become the default for every future ticker.

**Wiki**: `wiki/sankey-income-statement.md` gains a new **Step 2 — break revenue out by segment —
required**, ahead of writing the spec. It states the validation rule (segments must sum to revenue
within ~0.5%), what to do when a company genuinely publishes no split (say so on the card, never let
a missing fetch look like a missing disclosure), and repeats the warning about
`metrics/revenue-by-segment/` being annual data. Later steps renumbered.

**Skill**: added `.claude/skills/income-statement-chart/SKILL.md`, project-scoped so it travels with
the repo. It covers the whole procedure — the chartable/not-chartable gate including private
companies, core P&L sourcing, the mandatory segment step, rendering, validation, publishing — plus
the traps found the hard way: sources that disagree with themselves, aggregators that disagree with
filings, tax benefits, negative other income, loss makers with non-operating income, and non-USD
filings.

**Code**: `bin/mkspec.py` now **warns when segments are missing** and requires an explicit
`no_segment_split=True` to pass silently. When segments are supplied it checks they sum to revenue
and warns on drift. Enforcement lives in the tool, not only in prose.

**Noted**: the 50 single-bar charts are recorded on `wiki/favorites-financials.md` as a backlog to
fill in, explicitly not a standard to copy.

---

## 2026-10-24 — Segment audit, and the first 13 gaps closed

**Audit**: of the 65 statements, 12 had a real segment split, 3 were hand-verified as companies that publish none (CRWV, IONQ, SMCI), and **50 had an unverified single revenue bar** — the residue of the bulk watchlist pass.

A first pass at the audit reported the opposite and had to be corrected. It matched the string "no segment split" in the card notes, but those notes read *"no segment split **was pulled** for this name"* — a statement about what had been fetched, not about what the company discloses. The corrected audit keys off the spec's actual segment count and an explicit allow-list of verified-none tickers.

**Closed this pass (13)**: AAPL, AMZN, AVGO, INTC, IBM, ORCL, DELL, CSCO, ADBE, CRM, VZ, NFLX, AMD. Every split was validated against the revenue total before use.

**Judgement calls recorded on the cards**:

- **INTC** segments cannot be summed to revenue — $5.5B of intersegment eliminations, and Intel Foundry's revenue is mostly internal. The chart shows DCAI, CCPG and an external residual.
- **VZ** Business revenue is derived as the residual; only Consumer ($26.2B) was confirmed from the 10-Q.
- **NFLX** UCAN came from the 8-K; EMEA, LATAM and APAC from secondary coverage. They sum to within $1M of revenue.
- **ADBE** does not report Digital Media / Digital Experience in its release — it splits by revenue type, so the chart uses Subscription / Services / Product.
- **T** segment table for Q3 FY26 was not published in any source reachable this pass. Left pending rather than guessed.

**Tooling**: added `bin/addsegs.py`, which attaches a verified split to an existing spec, re-renders, and warns if the segments do not sum to revenue. It caught two unit mistakes of mine where I passed billions into a spec denominated in millions.

**Remaining**: 37 still on a single bar — ARQQ ASML ASTS BA BKSY CLSK COHR COIN DDOG FLY GE HD HIVE HUT INFQ LUNR MARA MDA MRVL MSTR NET NOW NU OUST PHM PL PLTR QBTS RDW RGTI RIOT RKLB SKHY SNOW T VOYG XNDU. Many of the micro-caps genuinely report one revenue line; each still needs checking before it can be marked verified-none.

---

## 2026-10-24 — Fixed overlapping flows in the loss layout

**Reported**: the Infleqtion chart showed the green non-operating income band crossing the red
flows, with labels sitting on top of bars.

**Two causes, both fixed in `bin/sankey.py`**:

1. **Declaration order.** Plotly stacks the links entering a node in the order they are declared,
   not by the vertical position of their sources. The pool's three sources were declared gross →
   loss → income while their nodes sat at gross → income → loss, so the bands crossed. They are now
   declared in the same top-to-bottom order as their positions.
2. **A node parked in a corridor.** The net-loss and non-operating income nodes were at `x=0.37`,
   directly in the path of the revenue → cost-of-revenue link, so that band ran straight through
   them. Both moved into the gross column, and cost of revenue was given a column of its own at
   `x=0.40` — it is a pure sink off revenue, so nothing crosses it, and the space beneath it holds
   its label.

**Also fixed**: precision. `bin/mkspec.py` chose 0 decimals for anything under $20bn, so a $13.5M
company rendered as `$14M` and its gross margin read 14% instead of 16%. Sub-$1bn statements now use
one decimal. 22 small-cap specs were regenerated.

**Documented**: `wiki/sankey-income-statement.md` gains an "Avoiding overlap" section covering all
three failure modes (crossing bands, nodes in corridors, labels on bars) and a precision table. The
skill gains the same four-point visual check, since the validator proves the numbers conserve but
says nothing about whether the chart can be read.

**Verification**: all 66 specs re-rendered; the only validator warning is the known TSM
reference-image discrepancy, which is the transcribed example rather than the filed statement. All
65 published images refreshed.

## 2026-10-23 — money figures enlarged and colour-coded

**Source**: user request — "i want the $ amount to be bigger fonts and color green/red".

**Changed**: `bin/sankey.py`. Both `label()` helpers — the one in `build()` and the one in
`build_loss()` — now render the first sub-line, which is always the money figure, at 19px bold in
the node's own colour. Remaining sub-lines stay 12px grey. Profit nodes therefore show green
amounts, cost nodes red, revenue and segment nodes black, so the cost structure reads before any
number does.

**Side effect fixed**: the taller label block pushed the loss layout's net-loss label into the
cost-of-revenue bar. The third sub-line ("funds the gap") was dropped — the money figure plus one
ratio is the most a label can carry without colliding. Verified on INFQ Q2 FY26, which was the
original overlap report.

**Documented**: `wiki/sankey-income-statement.md` design conventions now carry a label typography
table and the two-sub-line limit. `.claude/skills/income-statement-chart/SKILL.md` gains both as a
fifth visual check.

**Verification**: all 66 specs re-rendered; the only validator warning is the known TSM
reference-image discrepancy. All 65 published images refreshed and `financials.json` timestamp
bumped for cache busting.

## 2026-10-23 — Financials charts render live in the browser

**Source**: user request — "instead of images.. can the same diagram be done via web
html/javascript/etc?", then "lets change all and update financials.html".

**Why it was cheap**: the charts were already Plotly figures. kaleido flattened them to PNG at the
very last step. Dropping that step needed no rewrite of the layout.

**Changed**:

- `bin/sankey.py` gains `--json`, writing the figure to `charts/{TICKER}-{PERIOD}.json` with the
  design width and height split into a `design` block for the browser to rescale against.
- Nodes and links carry `hovertemplate`s, so a hover reads `Data Center → Revenue / $89.0B` in the
  statement's own currency and precision. Names ride in `customdata` rather than `node.label`: a
  populated label makes plotly draw node text, and even a transparent `textfont` leaves a glyph
  beside every bar. That artifact was caught on the first render and fixed.
- `assets/sankey.js` rescales the figure to its container, caches fetched figures, and replaces a
  previous mount rather than stacking ResizeObservers on the same element.
- `financials.html` renders the live chart and keeps the PNG as a fallback plus an "open as an
  image" link.
- `chart-live.html` is the prototype harness with width switchers, kept for testing narrow layouts.

**Numbers**: 12KB of JSON against a 395KB PNG per chart; 888KB against 22MB across all 65. All 65
render in under 400ms. PNG output is unchanged and still generated.

**Bug found while testing**: the pages' no-cache meta tags cover only the HTML, so a stale
`assets/site.css` hid the new rules completely — the same class of failure as the PNG caching bug
earlier today. `bin/stamp.py` now rewrites every page's asset links to `?v=<newest asset mtime>`.
Run it after any edit under `assets/`.

**Known limit, not solved**: below a 0.42 scale the chart stops shrinking and pans horizontally.
A five-column Sankey at 390px has roughly 7px text. The PNGs never fitted a phone either, so this
is not a regression, but a real phone layout needs a stacked variant.

**Verification**: all 65 chart JSONs fetched and drawn in the browser with no failures; profit
layout (NVDA) and loss layout (CRWV) both checked by eye; no console errors; ticker switching
confirmed to tear down the previous chart.

## 2026-10-23 — zoom and pan on the Financials charts

**Source**: user request — "allow to zoom".

**How it works**: a plotly sankey is not a cartesian plot, so it has no native zoom — `scrollZoom`
and `dragmode` do nothing. Zoom is a re-render at a larger scale instead: `draw(div, fig, zoom)`
feeds `container width x zoom` into the same scaling path already used to fit the chart, and
whatever no longer fits is panned. A CSS transform would have been less code and would have blurred
the type; re-laying out keeps the text sharp and the hover hit-boxes true.

**Controls**: a `− / Fit / +` pill stepping 0.5, 0.75, 1, 1.5, 2, 2.5, 3; ⌘/ctrl + scroll, which is
also what a trackpad pinch sends; drag to pan; double-click to refit. The zoom holds whatever is at
the anchor point under the same point afterwards. A press that never travels 4px stays a click, so
hover still works with drag-to-pan armed.

**Four bugs found and fixed while building it**, all recorded in
`wiki/sankey-income-statement.md`:

1. `Plotly.react` moves a sankey's node rectangles but leaves the link paths on their old geometry,
   so every band vanished at 200%. Switched to `Plotly.newPlot`.
2. `.fin-chart` was a shrinking flex child, so the zoomed chart was squeezed back to the container
   width — the chart measured 1382px at every zoom level. Needs `flex: 0 0 auto`.
3. `align-items` defaults to `stretch`, so once the box had a capped height the chart was squashed
   vertically to match. `.fin-fig` needs `align-items: flex-start`.
4. Without a height cap a 3x chart made the page three times taller and scrolled the controls away
   from the chart. The box takes `max-height: 78vh` while panning.

**Verification**: measured the geometry at each step — 1382x764 at fit, 2764x1528 at 200%,
4146x2292 at 300%, box held at 1382x739 with both axes panning, and an exact return to 1382x764 on
Fit. Re-drew all 65 charts and checked each one renders its full link count, none slower than
500ms. Hover confirmed working at 150%.

## 2026-10-24 — options wheel strategy page

**Source**: user described their options strategy and asked for a wiki page capturing it, plus help
judging good and bad sell-put entries from technicals, catalysts and fundamentals.

**Created**: `wiki/options-wheel-strategy.md`. Records the four stated rules, the arithmetic behind
the $3,000-a-week target, a six-point entry checklist derived from those rules, and dated readings
for all five names.

**Data**: daily history for MU, SMH, MSFT, GOOG and TSLA from stockanalysis.com (Yahoo and stooq
both refused — 429 and a challenge page). MU's close cross-checked against the IBKR connector and
matched to the cent, $877.55. Live MU Nov-20 put quotes pulled from IBKR for the 800, 760 and 720
strikes. Earnings dates and P/E from stockanalysis.com. SMH holdings from its ETF page.

**The finding worth keeping**: the income target is not reachable at current volatility under the
stated rules. $3,000/week on $300,000 is 1.00% of capital per week, or 52% a year. The best-paying
line available — a MU 800 put, 8.8% out, on the highest-volatility name of the five — pays 0.69% a
week. Whole account in that one trade gives $1,649/week, 55% of target. "Avoid assignment" and
"$3,000 a week" pull the same lever in opposite directions, and the page says so rather than
presenting a strike that appears to square them.

**Correction caught before publishing**: the first pass computed RSI as a plain mean of the last 14
changes (Cutler's) rather than Wilder's smoothing. It read MU 29, SMH 15, GOOG 24 — against the
correct 38, 33 and 31. SMH would have been published as "extremely oversold" on a number that was
five points off the standard. The calculator now uses Wilder's for both RSI and ATR.

**Flagged as needing verification**: GOOG's forward P/E (23.39) sits above its trailing P/E (15.92),
which implies falling earnings and more likely reflects a one-off gain in the trailing twelve
months. Not resolved against the filing.

**Not done**: no recommendation of any specific trade, and no order placed or staged. The page
states plainly that it records the user's rules and factual readings, not advice.

---

## 2026-10-26 — Added NBIS (Nebius Group) to the watchlist and every page

**Source**: Nebius Group 6-K exhibit 99.1, filed 2026-08-12
(`sec.gov/Archives/edgar/data/1513845/000110465926094844/nbis-20260812xex99d1.htm`). Prices,
52-week range and quotes from stockanalysis.com and the IBKR connector, both 2026-10-26. Headlines
from stockanalysis.com's NBIS page. Earnings-date estimates from ChartRow and Earnings Whisper.

**What changed**:

- `watchlist.json` — NBIS added after CRWV, `"fav": true`, sector `AI Infra`, tags
  `AI Infra / AI / Cloud / Data Center`. 100 symbols to 101, favorites 14 to 15. No `pe`: Nebius
  publishes no forward P/E (trailing is 933 on a near-zero EPS, which says nothing useful).
- `ibkr-conids.json` — NBIS conid 88819736, NASDAQ, resolved through IBKR `search_contracts`.
- The IBKR watchlist "Stock KB Heatmap" (id 100) — NBIS inserted after CRWV. That API is
  full-replace, so all 98 existing instruments were resubmitted with it and the result read back and
  checked: 99 instruments, every original intact.
- `financials.json` — NBIS Q2 FY26 entry, 65 statements to 66.
- `charts/NBIS-Q2-FY26.json` and `assets/financials/NBIS-Q2-FY26.png` — the live figure and raster.
- `examples/nbis-q2-fy26.json` — the spec.
- `events.json` — NBIS earnings at 2026-11-10, titled `(est.)`.
- `news.json` — an NBIS catalyst entry.
- `brief.json` — NBIS added to watchlist favorites.
- `wiki/nebius-q2-fy26.md` — new page: the statement, the segment table, where the loss comes from,
  the source disagreement, what is moving the stock, and the technical reading.
- `wiki/favorites-financials.md` — counts updated, plus a section on the Nebius source
  disagreement and its segment split.
- `wiki/index.md` — the new page listed; the Financials count corrected from twelve to 66.

**The finding worth keeping**: Nebius is a one-segment company wearing three names. AI cloud is
$574.9M of $585.9M in segment revenue; TripleTen ($10.0M, shrinking 19%) and Avride ($1.0M) are
rounding. Gross margin is 77%, so nothing is being sold at a loss — the $190.4M net loss is
depreciation ($259.7M, 45% of revenue, larger than the loss itself) plus $95.0M of net interest.
Adjusted EBITDA was +$236.2M. The number behind the debt headlines is capex: **$8,130.3M in the
first half against $981.3M of first-half revenue**, about eight times revenue.

**Second source disagreement on operating income.** stockanalysis.com reports −$1.3M, the filing
−$175.9M. The aggregator moves roughly $174.6M out of product development and SG&A, almost
certainly share-based compensation booked as an unusual item. The filing is used. This is the
second such case after Meta's Q3 FY26, and the same rule applied: when operating income looks too
clean, read the filing.

**Chart problem found and fixed in the render loop**: the first pass set the AI cloud segment note
to "$574.9M less $3.6M eliminations". That label block grew wider than the 300px left margin and
plotly dropped the whole annotation — the largest segment in the chart rendered with **no label at
all**, and the validator said nothing, because it only checks that the figures conserve. Shortened
to "net of eliminations" and re-rendered. Worth remembering: a long segment note does not wrap or
clip, it disappears.

**Eliminations**: $3.6M of intersegment eliminations is netted against the AI cloud bar so the three
segments foot to $582.3M. The reported figure is $574.9M, and both the card note and the wiki page
say so.

**Earnings date is not confirmed.** Nebius has not published one; ChartRow says Nov 10 and Earnings
Whisper says Nov 11. `events.json` carries Nov 10 with `(est.)` in the title and a note on the
disagreement.

**Verification**: all six pages checked in a local browser at 1280px. Heatmap shows the NBIS tile
with its favorite star, "AI INFRA" and a live $153.27 / −3.45%. Catalysts renders the card with its
three headlines. Morning Brief lists it under favorites. Financials shows the chip, the four KPIs,
the live chart; hover values were read back from the trace and foot in both directions
(571.3 + 10 + 1 = 582.3; 448.7 + 190.4 = 639.1 = 191 + 173.9 + 259.7 + 14.5), and one zoom step
redraws all 11 link bands. Events carries the row but does not display it: the month view renders a
fixed 42-day grid that ends 2026-11-07, so every Nov 10 event is out of view until November. That
is pre-existing behaviour, not caused by this change.

**Not done**: no entry on the Call Sheet. That page stores predictions, and there is no call on
NBIS to record — inventing one would corrupt the hit-rate table. `news.json` and `brief.json` are
otherwise from the Oct 19 run; both now carry a note saying the NBIS entry was added by hand on
Oct 26 so the stale dates are not read as covering it. NBIS was deliberately **not** added to the
five-name table in [[options-wheel-strategy]]: rule 4 of that strategy is "only names I am familiar
with", and adding a sixth would misstate the rules the page records.

---

## 2026-10-26 — Debt level and coverage chart for NBIS and CRWV

**Source**: Reference panel supplied in chat (an App-Economy-Insights style "Debt level and
coverage" grouped bar chart). Figures from stockanalysis.com quarterly balance sheet and cash flow
statements, both read 2026-10-26. Nebius's Q2 capex cross-checked against the 6-K.

**What changed**:

- `bin/debtbars.py` — new generator. Three bars for one quarter: debt, free cash flow, cash and
  equivalents. Emits the same figure JSON as `bin/sankey.py` (`--json`, with a `design` block) plus
  a PNG.
- `examples/nbis-debt.json`, `examples/crwv-debt.json` — the specs.
- `charts/NBIS-debt.json`, `charts/CRWV-debt.json` — the live figures.
- `assets/sankey.js` — `scaled()` now also scales axis tick fonts, the legend font and trace
  `textfont`, all guarded so a sankey is unaffected. Header comment updated: it is no longer a
  sankey-only renderer.
- `financials.html` — renders a second figure under the sankey when the item carries a `"debt"`
  key, and unmounts it on ticker change alongside the first.
- `assets/site.css` — `.fin-fig-debt{margin-top:14px}`. `bin/stamp.py` run.
- `financials.json` — `"debt"` keys and a coverage note on the NBIS and CRWV items.
- `wiki/nebius-q2-fy26.md`, `wiki/coreweave-q2-fy26.md` — a debt and coverage section each.
- `wiki/sankey-income-statement.md`, `wiki/index.md` — the second chart type documented.

**Scope changed mid-build**: the first pass drew three to four annual periods per ticker, like the
reference. The multi-year version was discarded on request for the single target quarter — the one
the Financials card is already about. The annual figures that pass gathered are in this entry
below, since they were verified and are the reason the window question came up at all.

**The finding worth keeping**: free cash flow is **negative for both**, so unlike the reference
panel these charts need a zero line and bars below it. For the quarter ended Jun 30, 2026:

| | Debt | Cash | FCF (qtr) | Net debt | Cash / debt |
|---|---|---|---|---|---|
| NBIS | $10,195M | $8,042M | $(3,411)M | $2,153M | 79% |
| CRWV | $51,613M | $5,524M | $(5,743)M | $46,089M | 11% |

Same business model, very different points on it. CoreWeave's quarterly cash outflow is larger
than its entire cash balance. Nebius still has most of its debt covered by cash, but burned 42% of
that cash in the quarter, and its debt went $49.5M (FY2024) → $4,973M (FY2025) → $10,195M here.

**Why NBIS has no multi-year series anyway**: FY2021–FY2023 on that ticker are the Yandex N.V.
entity, before the Russian businesses were sold in July 2024. Total liabilities read $5,461M in
FY2023 against $294.9M in FY2024 — the divestiture, not a deleveraging. Those years are not Nebius
and must not be charted as if they were. CRWV's FY2022 is likewise a stub: operating cash flow of
$0.9M and blank balance sheet lines.

**Trap found**: kaleido fails the whole PNG render with a bare `plotly.js error` (code 525) when
the layout **title** contains an HTML entity. `&middot;` in the title killed it; the same entity in
a trace `name` and in a `hovertemplate` rendered fine. Bisected property by property. Titles stay
plain ASCII.

**Second trap**: the browser served a cached `financials.html` during verification and the new
figure was absent from the DOM while present in the served file. The no-cache meta covers the HTML
only in principle; a query string forced the reload. `bin/stamp.py` handles the assets, not the
page itself.

**Verification**: NBIS and CRWV both draw three bars with the right values, read back off the
traces (`customdata` in millions against the rendered labels). Fonts scale with the container —
at a 1262px box against a 1000px design, the 15px tick font measured 18.93px, the 16px legend
20.19px, the 13px bar text 16.41px. The legend entity decodes to "Cash & equivalents" in the DOM.
NVDA, which has no `"debt"` key, renders exactly as before with no stray element and no console
errors; CRWV's sankey still draws all 10 links and 11 nodes, so the `scaled()` change did not
regress it.

**Not done**: no other ticker got a debt chart. The two here are the names where leverage is the
story the income statement does not tell; adding it everywhere would be noise, and the key is
opt-in per statement precisely so it stays that way.

---

## 2026-10-26 — Sankey and debt chart side by side on the Financials card

**What changed**:

- `bin/debtbars.py` — design cut from 1000x560 to **330x520** and every font size retuned to the
  size it renders at in that column (title 16, x ticks 13, y ticks 11, legend 11, bar labels 11).
  The title dropped the company name, which the card header already carries. The legend no longer
  fits on one line at that width, so plotly stacks it vertically, which reads fine.
- `financials.html` — both figures now sit in a `.fin-row`; the zoom controls and hover hint moved
  below the row rather than between the two charts.
- `assets/site.css` — `.fin-row` flex rules, and the Events calendar's `.legend` block scoped to
  `#ev-body .legend`.

**Bug found by looking at the rendered page rather than the PNG**: every legend label in the debt
chart rendered in uppercase in the browser while the kaleido PNG was correct. `assets/site.css`
carried an unscoped `.legend` rule for the Events calendar with `text-transform:uppercase`, and
plotly draws its own `<g class="legend">` inside the chart SVG, so the page's CSS reached into the
chart. Walked the computed style up the ancestor chain to find where `uppercase` started —
`g.legend`, with `g.infolayer` above it still `none` — which pinned it to a class collision rather
than inheritance from the card. Scoping the rule fixed it and left the Events legend intact
(verified separately: still flex, still uppercase, still the gold swatch).

**Verification** at a 1280px viewport: row 1264px wide, sankey column 920px, debt column 330px,
same top, no page overflow. Rendered charts 918x508 and 328x517, so the two heights match within
9px. At 820px the row wraps and the charts stack, still no overflow. Legend labels read "Debt",
"Free cash flow", "Cash & equivalents" with `text-transform: none`.

**The cost, stated plainly**: the sankey now draws at about 0.54 of its design width instead of
0.74, so its 12px sub-lines render near 6.5px. That is above the 0.42 floor `assets/sankey.js`
enforces, but it is small. The zoom controls and the "open as an image" link both still work and
are the way to read it properly.

---

## 2026-10-26 — Debt and coverage chart on every statement

**Source**: stockanalysis.com quarterly balance sheet and cash flow statements, read 2026-10-26
through the site's own data endpoint rather than the rendered pages.

**What changed**:

- `bin/debtfetch.py` — new. Builds a debt/coverage spec for every item in `financials.json`,
  taking the balance sheet and cash flow column whose period end matches the quarter the card
  already shows.
- `examples/*-debt.json` and `charts/*-debt.json` — **65 specs and 65 figures**.
- `financials.json` — a `"debt"` key and a coverage note on all 65.
- `bin/debtbars.py` — now currency-aware, and picks its axis unit (M / B / T) from the largest bar.
- `wiki/sankey-income-statement.md`, `wiki/index.md` — the bulk pipeline documented.

**How the data is read**: stockanalysis.com has no financials API — every endpoint shape I tried
returned `{"status":404}`. The pages are SvelteKit, so the data is at
`/<path>/financials/<statement>/__data.json?p=quarterly`. That returns devalue's flattened format:
a `data` array in which every integer is an index back into the same array, so it needs hydrating
before anything can be read out of it. Once hydrated, `financialData` holds every line as a list
parallel to `datekey`. The fields used are `debt`, `cashneq` and `fcf`, with `ncfo + capex` as the
fallback when `fcf` is absent.

This beat fetching 132 rendered pages: it is one request per statement, returns exact unrounded
figures, and cannot misread a table.

**Verification**: the extractor was checked against figures obtained independently. NBIS and CRWV
matched the numbers gathered by hand earlier in the day to the dollar. GOOG's Q2 FY26 free cash
flow (−$5,855M, from $39,069M operating less $44,924M capex) and SNDK's FQ4 FY26 (+$7,083M) were
re-fetched from the rendered pages and both matched exactly.

Then every card was driven in the browser: all 66 chips clicked, the right card shown each time,
a debt chart present on exactly the 65 that carry the key, none on the one that does not, and no
console errors. Currency and unit selection spot-checked across the five currencies —
`NT$818.4B / NT$476.6B / NT$3.6T` for TSM, `₩21.1T / ₩54.7T / ₩26.8T` for SKHY, `€2.0B / €11.4B /
€8.0B` for ASML, `C$378M / -C$146M / C$398M` for MDA, and `$2.2M / -$25.7M / $28.9M` for ARQQ.

**One ticker has no chart: Nintendo (7974).** Its quarterly cash flow statement on stockanalysis
carries three fields — `datekey`, `fiscalYear`, `fiscalQuarter` — and no cash flow lines at all,
because Japanese filers report cash flow semi-annually rather than quarterly. There is no free cash
flow figure for the quarter to set the balance sheet against, and using the half-year or annual
figure would describe a different period from the income statement beside it. The card carries a
note saying so instead.

**Two verification traps, both mine rather than the page's**:

- The first sweep reported a debt chart on all 66 cards including Nintendo. The chip list is
  rebuilt by `renderFin()` on every render, so the node references captured at the start went
  stale after the first click and every later click did nothing — the card sat on META while the
  loop believed it was advancing. Caught by also recording the ticker the card was actually
  showing, which is worth doing in any sweep like this. Re-querying the chips each iteration gave
  the real result.
- `currency_of` first read the filed currency from the sankey spec, which gave TSM "$". There are
  two TSM specs — `tsm-q3-fy26.json` in USD and `tsm-q3-fy26-filed.json` in NT$ — and the
  published chart uses the filed one. It now reads the currency from the card's own KPI values,
  which cannot go stale relative to what the card displays.

**What the charts show, across the book**: free cash flow is negative for the whole neocloud and
pre-revenue end — CRWV −$5.7B, NBIS −$3.4B, ASTS −$695M, HUT −$585M — and also, for one quarter,
for three of the largest names, where capex has overtaken operating cash flow: GOOG −$5.9B, AMZN
−$8.8B, ORCL −$5.4B, SPCX −$10.0B. Against those, MU generated $32.9B of free cash flow in a single
quarter and holds $38.4B of cash against $5.2B of debt.

**Not done**: no PNG fallbacks for these. The page renders them live and `drawDebt` has no raster
path, so the two debt PNGs copied into `assets/financials/` earlier were removed rather than left
unreferenced.

---

## 2026-10-26 — Tooltips on the debt and coverage bars

**What changed**: every bar on every debt chart now explains itself on hover, with the actual
figures. No change to the charts themselves.

- `bin/debtfetch.py` — also captures the component lines behind each bar: the debt breakdown
  (`debtc`, `currentPortDebt`, `debtnc`, `currentCapLeases`, `capitalLeases`), the cash lines that
  sit *outside* cash and equivalents (`investmentsc`, `restrictedCash`), and `ncfo` / `capex`.
  Anything the components do not account for is shown as `Other`, never dropped.
- `bin/debtbars.py` — builds a column-aligned monospace block per bar and renders it through
  `hovertemplate="%{customdata}"`.
- `examples/*-debt.json`, `charts/*-debt.json` — all 65 refetched and re-rendered.
- `assets/sankey.js` — chart JSON is now fetched with `cache: "no-store"`.

The free cash flow tooltip is the one that prompted this, and reads:

```
Free cash flow · Q2 FY26

Operating cash flow    $2,246M
Capital expenditure   -$5,657M
------------------------------
Free cash flow        -$3,411M
```

**Entity rules, now fully mapped.** Three different behaviours in one library:

| Where | HTML entity | What to use |
|---|---|---|
| layout title | kills the whole kaleido render (`plotly.js error` 525) | plain ASCII |
| legend / trace name | decoded correctly | either |
| hover text | **not** decoded — `&middot;` renders literally | literal characters |

The hover case was found by reading the rendered tooltip back out of the DOM rather than trusting
the JSON. `&#160;` is the exception and is required: plotly collapses runs of ordinary spaces in
hover text, so the columns only line up with non-breaking spaces and a monospace `hoverlabel` font.

**Cache fix**: `assets/sankey.js` fetched `charts/<stem>.json` with no cache directive. A
regenerated chart keeps its filename, so a returning visitor could have been shown last month's
figures with nothing to indicate it. Now `cache: "no-store"`; the module's in-memory Map still
means one fetch per chart per page load.

**My checker was wrong before the data was.** The first validation pass reported 45 of 65 charts
failing to foot, including NBIS as `[2246, 5657, 3411]`. The figures were right — 2,246 − 5,657 =
−3,411 — and the regex was wrong: its leading `(-?)` was unanchored, so the match began at the
currency symbol and the minus sign was never captured. Rewritten to split each line on the
non-breaking spaces and parse the trailing token. On the corrected check all 65 pass: debt
components sum to the debt total, operating cash flow plus capex equals free cash flow, and every
total matches its spec.

Worth keeping as a habit: a validator that fails almost everything is usually itself the bug, and
the cheapest test is to do one case by hand.

---

## 2026-10-26 — Hover detail on the income statement charts

**What changed**: every node and band on all 66 Sankeys now explains itself on hover. No change to
any chart's appearance or figures.

- `bin/sankey.py` — `node_tips()` and `link_tips()`, plus a monospace `hoverlabel`. Built entirely
  from the existing specs; no new data was fetched.
- `charts/*.json` — all 66 re-rendered.
- `examples/superseded/` — new, with the stale USD TSM spec moved into it and a README saying why.

**What a node now says**: its amount, its share of revenue, and its share of gross profit where
that means anything. The gross profit line is offered only to nodes reachable from the gross
profit node in the link graph, so cost of revenue — which sits above gross profit — does not get
a "% of gross profit" reading that would be nonsense.

**What a band now says**: its share of its source, e.g. `Revenue → Cost of revenue · 23% of
Revenue`. Suppressed where a node has a single outgoing band, since 100% tells the reader nothing.

**Derived lines are now labelled as derived.** Four node names are computed so the statement foots
and were previously indistinguishable from filed figures:

| Node | Derivation |
|---|---|
| Cost of revenue | revenue less reported gross profit |
| Operating expenses | gross profit less operating profit |
| Interest & other (, net) | net profit plus tax, less operating profit |
| Non-operating & tax, net | charges less operating expenses |

**A real bug this surfaced, worth more than the feature.** Re-rendering every spec in a loop
silently replaced TSMC's published chart with the wrong currency. `bin/sankey.py` names its output
from the spec's `ticker` and `period`, not from the filename, so both `examples/tsm-q3-fy26.json`
(USD, transcribed from the reference image, long superseded) and `examples/tsm-q3-fy26-filed.json`
(NT$, filed, what the card's KPIs use) write `charts/TSM-Q3-FY26.json`. `examples/*.json` sorts
`-filed` first, so the stale USD spec ran last and won. The chart would have read `$1.9B` for a
segment whose card KPI says `NT$1,494.2B` for revenue.

Caught by diffing the rendered chart rather than trusting the loop's exit status. Superseded specs
now live in `examples/superseded/`, out of the glob, with a README explaining the collision.
Renaming alone would not have helped — the collision is on spec contents, not filenames.

**Verification**: all 66 charts checked programmatically — node and link tooltip arrays present and
the right length, both hovertemplates replaced, no raw HTML entities, node labels still empty so
plotly draws no glyphs on the bars. Then hovered in the browser: a node gave
`Gross profit · Q2 FY26 / amount $448.7M / % of revenue 77.1%` in the monospace font, and a band
gave `Revenue → Cost of revenue / $133.6M · 23% of Revenue`. No console errors.

Note that `Plotly.Fx.hover` does not drive a sankey trace — it is not cartesian — so the check had
to use a real pointer over the node rect's measured position.

**Still to do**: year-over-year per node, which needs the prior-year column fetched per ticker and
a rule for the five charts built from filings rather than the aggregator, where the two bases
disagree on opex and operating income.

---

## 2026-10-26 — Year over year on the income statement hovers

**What changed**:

- `bin/sadata.py` — new. The stockanalysis data endpoint and the devalue hydrator, factored out of
  `bin/debtfetch.py` so both fetchers share one copy.
- `bin/yoyfetch.py` — new. Writes a `prior` block into each income statement spec, keyed by the
  node name the chart draws.
- `bin/sankey.py` — nodes with a prior figure gain `year ago` and `year over year` rows.
- `examples/*.json`, `charts/*.json` — all 66 updated and re-rendered.

**The design decision worth keeping: each line polices itself.** Five charts were built from
filings rather than the aggregator, and on those the two sources disagree about where some costs
sit. A growth figure from the wrong basis would contradict the bar it is attached to. Instead of
maintaining a list of exceptions, the year-ago figure is kept only when the source's **current**
quarter for that line matches what the chart already draws, within 1%.

The rule found every known disagreement without being told about any of them — NBIS's R&D, SG&A
and operating expenses, Meta's operating expenses and operating income — and several nobody had
noticed, including NVDA's SG&A, DELL's R&D and SG&A, GE's and IBM's cost of revenue, and PHM's
gross profit, cost of revenue and operating profit. Those are worth a look on their own: they say
the aggregator and the filing classify those lines differently.

**A second rule drops a line whose sign changed.** NBIS's "Net loss" node was a $584.4M net
*profit* a year earlier, on the Yandex disposal; a percentage across that flip is meaningless.
Ten tickers have at least one such line, mostly miners and loss-makers that crossed zero.

Result: 443 of the nodes across 66 charts carry a year-ago figure.

**A bug in my own code, caught by checking a refusal rather than trusting it.** SKHY came back with
zero usable lines, reported as a basis mismatch. It was not: SK Hynix files in **trillions** of
won, the spec carries `"unit": "T"`, and my divisor handled only `M` and `B`, defaulting everything
else to millions. Every SKHY line therefore looked a million times off. Fixed to a
`{"M": 1e6, "B": 1e9, "T": 1e12}` map, after which SKHY took seven lines.

The lesson is that a self-policing rule hides its own bugs: a silent refusal looks exactly like a
correct refusal. The two zero-row tickers were the only ones worth investigating, and one of them
was mine.

**Nintendo is the genuine refusal.** Its chart is in USD, built from the NTDOY ADR; the Tokyo
listing's data is in yen; and NTDOY publishes no income statement at that endpoint. Nothing on a
matching basis exists, so it gets no growth rows at all.

**Verification**: 66 charts re-rendered, then checked programmatically — every node carrying a
`year ago` row also carries a `year over year` row, and the blocks are still padded. Then hovered
in the browser: `Operating profit · Q2 FY27 / amount $63.7B / year ago $28.4B / year over year
+124% / % of revenue 66.2% / % of gross profit 88.3%`. No console errors.

---

## 2026-10-26 — Correction: the NBIS reclassification is not share-based compensation

The entries above, and `wiki/nebius-q2-fy26.md` and `wiki/favorites-financials.md`, said the
~$174.6M that stockanalysis.com moves out of NBIS's product development and SG&A was "almost
certainly share-based compensation". That was asserted without checking.

**Share-based compensation was $102.5M** in Q2 FY26 (`sbcomp`, stockanalysis cash flow statement;
$26.2M in the year-ago quarter). It therefore accounts for at most 59% of the gap and is not the
explanation on its own. What the rest is has not been established.

Nothing downstream changes: the chart follows the filing either way, and the basis check in
`bin/yoyfetch.py` excludes those lines from year-over-year on the arithmetic, not on the
explanation. The three pages have been corrected to say the reclassification is unidentified.
This log is append-only, so the earlier entries stand as written.

---

## 2026-10-26 — Share-based compensation on the hovers

**What changed**:

- `bin/yoyfetch.py` — also reads `sbcomp` from the cash flow statement for the matching quarter
  and writes it to each spec as `stock_comp`.
- `bin/sankey.py` — the pooled cost node ("Operating expenses", or "Costs & charges" in the loss
  layout) gains a `stock comp` row and a line saying what it spans.
- `examples/*.json`, `charts/*.json` — all 66 updated and re-rendered. 60 carry a figure; the
  rest report no `sbcomp`.

**Placed deliberately on one node, not on R&D and SG&A.** The original plan was to put it on both
of those. That would have been wrong: the cash flow statement reports share-based compensation as
a single company-wide number, and the income statement spreads it across cost of revenue, R&D and
SG&A without disclosing the split. A figure on R&D would read as R&D's share of it, which is not
something this source knows. It sits once, on the pooled node, with the note "stock comp is
company-wide and spans cost of revenue, R&D and SG&A".

Worth reading against the bar it sits on: NVDA's operating expenses are $8.4B and **$2.0B of that
is stock comp**, just under a quarter. SPCX reports $2,363M, PLTR $265M on a much smaller base.

**Verification**: all 66 re-rendered and checked programmatically — the stock comp row appears on
exactly one node per chart, and always on the pooled one. Hovered in the browser on NVDA:
`Operating expenses · Q2 FY27 / amount $8.4B / year ago $5.4B / year over year +56% / % of revenue
8.7% / % of gross profit 11.7% / stock comp $2.0B`, then the two notes.

---

## 2026-10-26 — Call Sheet removed

**What changed**: `tracker.html` deleted, and the `Call Sheet` nav tab removed from the five
shared-CSS pages (`heatmap.html`, `catalysts.html`, `brief.html`, `events.html`,
`financials.html`). The site is five tabs again.

The page held its predictions inline, in a `<script type="application/json" id="records">` block
— twelve calls on NOW, MSFT and MU dated 2026-08-15, by Kevin, ChatGPT, Claude and Gemini, all
still `actualPrice: null`. Nothing else read that block and no `*.json` in the repo fed it, so
deleting the file removes the only copy in the working tree. Git history keeps it:
`git show HEAD~1:tracker.html` (or whichever commit precedes this one) brings it back whole.

`Site.nav()` highlights the current tab by walking `nav.tabs a.tab` in the DOM, so dropping a
link needed no change in `assets/site.js`.

---

## 2026-10-26 — Revenue segment splits on 27 more charts

**What changed**: 40 of the 66 statements carried the placeholder note *"Single revenue bar — no
segment split was pulled for this name"*. That line said nothing about whether the company
publishes a split. All 40 are now resolved: **27 gained a reported split** and the other 13 say on
the card why there is none. The Financials page now stands at **53 of 66 charts with a segment
split**.

**Where the figures came from**, and why one of them contradicts an older rule here:

- `bin/segfetch.py` (new) reads stockanalysis's `revenue-by-segment` **data endpoint**,
  `__data.json?p=quarterly`. The rendered page of that name is still unusable — annual figures, as
  recorded in [[sankey-income-statement]] — but the endpoint behind it carries a `quarterly` array
  keyed by period end. It supplied ASML, BA, BKSY, MSTR, NOW, PHM, PLTR, RIOT and RKLB.
- `bin/edgar.py` (new) fetches a single note out of an SEC filing. EDGAR renders every note as its
  own small `R##.htm` report and `FilingSummary.xml` names them, so a disaggregation note comes
  down on its own instead of inside a 3MB 10-Q. This supplied COIN, FLY, HD, HIVE, IONQ, LUNR,
  MARA, MRVL, PL, QBTS, RDW, RGTI, SNOW and VOYG.
- `bin/segapply.py` (new) holds the figures that had to be read by hand — the three above plus
  COHR, GE and T from their 8-K exhibits, and MDA from its own release, since MDA Space files in
  Canada and has no SEC disaggregation note.
- `bin/segnotes.py` (new) rewrites the card note from the spec, so the note and the chart cannot
  drift apart.

**The trap in the endpoint, and the guard that caught it.** It buckets every filer into *calendar*
quarters, so a fiscal-quarter filer's own period end is not in it: HD (Aug 2), MRVL (Aug 1), SNOW
(Jul 31) and T (Sep 30) each came back a quarter short, and SMCI a full year short. Matching on the
nearest date would have hung the wrong quarter's split on the chart without a word. The guard is
the sum instead — a split is written only when the segments add up to the revenue the chart already
draws, within 0.5% — and a wrong quarter does not foot. Those five went to the filings instead.

**A rounding bug the sum check also caught.** Rigetti's three reported lines are $4,098K, $952K and
$88K. At the one decimal the chart draws they become 4.1 + 1.0 + 0.1 = $5.2M against $5.1M of
revenue — $0.1M of revenue Rigetti never reported, purely from rounding each line up. The two
service lines are shown as one, labelled "Research, services & access", and the card says so. The
check compares values **as the chart will round them** for exactly this reason.

**A correction.** The audit on 2026-10-19 recorded IONQ as hand-verified to publish no split. That
was wrong: IonQ's 10-Q disaggregates revenue into quantum hardware $46.5M and platform, consulting
and support $33.6M. Both now show. SMCI and CRWV were rechecked and do hold — Supermicro's FY26
10-K gives net sales by geography only, and so does CoreWeave's 10-Q.

**AT&T's segment table, open since the bulk pass, is now on the chart.** It was unreachable then
because AT&T restructured its segments in Q1 2026: the old Communications / Mobility / Business
Wireline names no longer exist. Q3 FY26 is Advanced Connectivity $29.5B, Legacy $1.5B, Latin
America $1.2B.

**Not blindly trusted**: the endpoint's figures were checked against the companies' own releases
for PLTR (Government $990M +79%, Commercial $945M +110%) and BA (BCA $11,751M, BDS $7,483M, BGS
$5.3B), and BKSY's three segment names were confirmed against its 10-Q segment note rather than
taken from the aggregator's labels. RGTI's labels came from the aggregator as "Other" for what the
filing calls sales of quantum computers and components; the filing's wording is used.

**Growth rates off a near-zero base** read as noise — Intuitive Machines' commercial line would
print "+3047% Y/Y". Above 999% the chart shows "from $2.1M a year ago" instead, which says the same
thing and says it better. Affects LUNR, RDW and FLY.

**Verification**: all 27 charts re-rendered with no validator warnings — the "segments vs revenue"
identity is one of the five it checks — and nine were opened in the browser (T, HD, LUNR, GE, COIN,
MDA, QBTS, HUT, RGTI), confirming the live chart draws the new bars and the card note matches.

**Noted, not fixed**: on HD and several others the "Cost of revenue" label sits under its own node
rectangle and the value is partly covered. It predates this change — the published PNG has it too —
and is a layout problem for the renderer, not the data. Also SKHY's Q2 FY26 statement shows ₩79.3T
of revenue with ₩93.8T of net profit, net profit above revenue on ₩62.1T of non-operating income;
the figures agree with the aggregator but the shape is odd enough to be worth a look.

---

## 2026-10-26 — Earnings: actual against estimate, on 63 cards

**What changed**: a third figure on each Financials card. One column per quarter — a filled dot for
what the company earned, a hollow one for what the street expected, a hairline joining the pair —
four reported quarters and the one still ahead, which carries a consensus and no actual. Full
description in [[earnings-surprise-chart]].

- `bin/epsfetch.py` (new) — Nasdaq's `earnings-surprise`, `earnings-forecast` and `earnings-date`
  endpoints, which carry Zacks' consensus, into `examples/<t>-eps.json`.
- `bin/epsdots.py` (new) — the figure, same JSON pipeline as the sankey and the debt bars.
- `bin/epsnotes.py` (new) — links the chart on the card and writes the note.
- `financials.html`, `assets/site.css`, `assets/sankey.js` — a third figure slot, and marker sizes
  now scale with the rest of the figure.

**63 of 66 cards carry it.** Nintendo (7974) is not on Nasdaq, Arqit has no surprise history
published, and Xanadu has no reported quarters. Those three draw nothing rather than an empty
frame.

**The basis warning is the point of the note.** The sankey on the same card is GAAP, from the
filing. This chart is adjusted EPS, the basis the street scores against. The two differ by whatever
a company excludes, and for some names that is most of the number — NBIS reports -$0.12 adjusted
against a GAAP loss of a different size entirely. For a foreign filer it is also the ADR's earnings
per share in US dollars: TSM files in New Taiwan dollars and charts at $4.60 per ADR. Both facts
are in the card note and the hover.

**A guard that was wrong, and how it showed.** The fetcher asks Nasdaq for the company name first
and refuses the ticker if the name does not match the card — tickers are reused, and a chart drawn
from another company's earnings would look entirely plausible. The first run rejected 21 of 66, and
18 of those were the guard's fault, not the data's: it split names on whitespace without stripping
punctuation, so "Tesla, Inc." tokenised as `tesla,` and matched nothing. Every *Name, Inc.* on the
list failed. Two further shapes failed honestly — a short card name that shares no word with the
registered one (AMD against Advanced Micro Devices, IBM against International Business Machines,
TSMC against Taiwan Semiconductor Manufacturing, SpaceX against Space Exploration Technologies),
and "Nu Holdings", which reduced to an empty set because `nu` is two letters and `holdings` is a
noise word.

It now recognises a name four ways — a shared word, one word prefixing another, the card's name
matching the registered name's initials, or equal first tokens. Checked against decoys before
rerunning: MDA Space against Medallia, Planet Labs against Pitney Bowes, Firefly against Fly
Leasing and Nebius against Nuveen are all still refused.

**A rejection that looks like a refusal is worth re-reading.** This is the second time a
self-policing rule here has hidden its own bug — the first was `yoyfetch.py` silently skipping SK
Hynix because its divisor had no entry for trillions. A guard that refuses 21 names needs its
refusals read one by one, because a correct refusal and a broken test look identical from outside.

**Layout**: the sankey now has a 760px floor, so on a 1440px screen the debt bars sit beside it and
the earnings dots wrap underneath; past about 1900px all three share a row. Without the floor
`min-width:0` let the sankey collapse to 2px the moment a third chart joined. Checked at 375px too:
no horizontal page scroll.

**Verification**: 63 rendered with no validator warnings — a quarter is either reported, with both
figures, or ahead with no actual, and nothing in between is drawn. Five cards opened in the browser
(NVDA, TSM, 7974, NBIS, RGTI): three figures each except Nintendo, which draws one. Hovers read
back live, both the reported dot (`Sep '26 · reported Oct 15, 2026 / actual $4.60 / estimate $4.45
/ surprise +$0.15 (+3%)`) and the unreported one (`Dec '26 · not reported yet / consensus $5.22 /
range $5.12 to $5.52 / estimates 6 (5 up in 4 weeks) / no actual yet`).

---

## 2026-10-26 — P/E and dividend on the card KPIs

**What changed**: two more tiles above every statement — `P/E` showing trailing and forward side by
side, and `Dividend` showing the yield with the annual rate under it. `bin/pefetch.py` (new) writes
both from stockanalysis.com's quote data (`peRatio`, `forwardPE`, `dividend`, `exDividendDate`),
the same source the heatmap's forward P/E column uses. All 66 cards updated, no failures.

**These two do not belong to the quarter the rest of the card describes.** The other four KPIs come
from one filed statement and never change; these are measured against the share price and are stale
the moment they are written. So they share one note that carries the date, and `financials.json`
gains a `marketAsOf` stamp:

> Market figures as of Oct 26, 2026: P/E 11.0 trailing, 8.3 forward; dividend $2.83 a year, 6.57%
> yield, last ex-dividend Oct 9, 2026. Both are measured against the share price, so unlike the
> other figures on this card they move every session and are not from the filing.

**What reads as missing, and why.** A loss-maker has no meaningful trailing P/E and a company with
no positive forward estimate has no forward one; both print `n/a` rather than a negative number,
because a negative P/E is not a cheap stock, just a loss. 24 of the 66 pay a dividend and 42 read
"None" — a fact about the company rather than a gap in the data.

**A bug of mine, caught by reading the output rather than the exit status.** The quote hands the
dividend over as one preformatted string, `"$2.83 (6.57%)"`, which this parses rather than prints.
The parser defaulted a missing currency symbol to `$` — and Nintendo's comes through as
`162.00 (1.91%)` with no symbol at all, so the card briefly showed a **$162** dividend for what is
¥162. The symbol now comes from the quote's own `curr.dividend` code, with the code itself as the
fallback; nothing is assumed. Nintendo reads ¥162.00, and it is the only non-dollar dividend on the
page — SKHY, TSM and ASML all quote theirs in dollars per ADR.

**Verification**: all 66 refetched after the fix, then VZ opened in the browser — six tiles on one
row at 1440px, `Revenue $34.3B · Gross margin 62% · Operating margin 23% · Net profit $3.8B · P/E
11.0 · 8.3 · Dividend 6.57%`. Loss-making cards carry five, since they have no operating margin
tile to begin with.

---

## 2026-10-27 — Added V (Visa) to the watchlist

**Sources**: stockanalysis.com's V quote page and quote data, read 2026-10-27 (forward P/E 26.75,
trailing 34.21, earnings date Oct 27, 2026, ex-dividend Aug 11, 2026). Contract id from the IBKR
connector's `search_contracts`. The earnings fact is Visa's own fiscal Q4 2026 release, filed as an
8-K on 2026-10-27 (`sec.gov/Archives/edgar/data/1403161/000140316126000126/v-20261027.htm`).

**What changed**:

- `watchlist.json` — `V` added after NU, tags `Fintech`, forward P/E 26.75. 101 symbols to 102,
  favorites unchanged at 15. `Fintech` is the ranked tag the heatmap already uses for COIN, MFH and
  NU, so Visa reads as Fintech there rather than needing a new category.
- `ibkr-conids.json` — `V` conid 49462172, NYSE, "VISA INC-CLASS A SHARES". The file's note said
  every id was resolved on 2026-09-28, which stopped being true when NBIS was added on the 26th;
  it now records both later additions.
- The IBKR watchlist "Stock KB Heatmap" (id 100) — V appended. That API is full-replace, so all 99
  existing instruments were resubmitted with it and the result read back: 100 instruments, every
  original intact and in its original order.

**Nothing added to `events.json`, and that is the file's own rule.** Both dates the source
publishes for V are in the past: Visa reported fiscal Q4 2026 after the close *today*, and the
ex-dividend date on the quote page is Aug 11, 2026. The file carries only future-dated ticker
events and omits passed ones rather than estimating a next date, so V has no entry until a
confirmed one is published. (Visa's board raised the quarterly dividend 16% to $0.780 per share in
that release, so the next ex-dividend date will be a new figure, not the one on the quote page.)

**Caveat worth knowing before reading the heatmap's P/E colouring**: `watchlist.json` carries one
`peAsOf` stamp for the whole file, and it still says Sep 01, 2026. V's 26.75 was read today, so the
file now holds one figure fresher than its own stamp. The heatmap prints that stamp under the P/E
view, which means it currently understates how fresh V's number is rather than overstating it. A
full refresh is a separate job — `quotes.py --pe` still reads the watchlist out of an inline block
in `heatmap.html` that no longer exists, so that path needs fixing before it can run.

**Not done**: no income statement chart. Visa is not on the Financials tab, so there is no Sankey,
no debt bars and no earnings-surprise dots for it — only the heatmap, and the Catalysts and Events
pages once it has something to show. No order placed, staged or cancelled.

---

## 2026-10-27 — Added VRT (Vertiv Holdings) to the watchlist

**Sources**: stockanalysis.com's VRT quote data, read 2026-10-27 (forward P/E 26.32, trailing
47.20, $11.48B of trailing revenue, ex-dividend Sep 14, 2026). Contract id from the IBKR
connector's `search_contracts`. The earnings date is Vertiv's own announcement of 2026-10-14:
third-quarter 2026 results before market open on Wednesday, October 28, 2026
(`investors.vertiv.com/news/news-details/2026/Vertiv-Announces-Date-of-Third-Quarter-2026-Earnings-Release-and-Conference-Call/`).

**What changed**:

- `watchlist.json` — `VRT` inserted after NBIS, tags `AI Infra / Data Center / Hardware`, forward
  P/E 26.32. 102 symbols to 103, favorites unchanged at 15. It reads as AI Infra on the board,
  which is the highest-ranked tag it holds. Vertiv sells the power and cooling the racks sit in, so
  it belongs beside CRWV and NBIS rather than in Industrials with GE.
- `ibkr-conids.json` — `VRT` conid 402783527, NYSE, "VERTIV HOLDINGS CO-A". `search_contracts`
  returns four VRT rows: the US primary listing, a Mexican and a Canadian cross-listing of the same
  company, and Virtus Health in Australia. The US NYSE row is the one taken.
- The IBKR watchlist "Stock KB Heatmap" (id 100) — VRT inserted after NBIS, mirroring the file's
  order. Full-replace API again, so all 100 existing instruments were resubmitted and read back:
  101 instruments, every original intact and in order.
- `events.json` — VRT earnings at 2026-10-28, sorted into place after SKHY. The note records that
  this entry was added by hand from Vertiv's announcement rather than by the refresh job, because
  that job cannot run (see below).

**A date conflict, resolved toward the company.** Vertiv's own release says October 28 before the
open. One third-party calendar (Bullstory) lists October 20. The company's announcement wins; the
aggregator is wrong, not early.

**Why the event went in by hand.** `quotes.py --events` is a full rewrite: it keeps only the macro
and Fed entries plus whatever it refetches, so running it for one ticker would delete every other
ticker's events. It also still reads the watchlist out of an inline `<script id="watchlist">` block
in `heatmap.html` that no longer exists — the watchlist moved to `watchlist.json`. Both the `--pe`
and `--events` paths in that file are broken the same way and need fixing before either can run
again.

**Verification**: heatmap served locally — 103 tiles, VRT reading `VRT · AI INFRA · $208.56
· +4.39%` with `VRT -- AI Infra, Data Center, Hardware` on its hover. Events page shows
`VRT earnings` under the 28th, beside the FOMC decision and GOOG, MSFT, NOW and SKHY.

**Not done**: no income statement chart — Vertiv is not on the Financials tab. No order placed,
staged or cancelled.

---

## 2026-10-27 — Visa's fiscal Q4 2026 charted; the first split that could not be drawn

**Source**: Visa 8-K exhibit 99.1, filed 2026-10-27, the quarter ended September 30, 2026
(`sec.gov/Archives/edgar/data/0001403161/000140316126000126/q42026earningsrelease.htm`). Debt,
cash and free cash flow from stockanalysis.com; street consensus from the Nasdaq/Zacks endpoints;
both read 2026-10-27.

**What changed**: `examples/v-q4-fy26.json`, `charts/V-Q4-FY26.json` and
`assets/financials/V-Q4-FY26.png`; `examples/v-debt.json`, `examples/v-eps.json` and their charts;
a `V` entry in `financials.json`, 66 statements to 67; `wiki/visa-q4-fy26.md` (new);
`wiki/index.md` and `wiki/favorites-financials.md` counts.

**The quarter**: $12,139M of net revenue (+13% Y/Y), $4,877M of operating expenses, $7,262M of
operating income (60% margin), $98M of non-operating income, $1,358M of tax and $6,002M of net
income (49% margin). GAAP EPS $3.19; non-GAAP $3.48.

**Two structural things about Visa that the chart had to deal with.**

*No cost of revenue.* Visa publishes none — the statement runs net revenue straight into operating
expenses. Gross profit therefore equals revenue and the card's gross margin tile reads **100%**,
which is literal rather than a missing line. Nu Holdings is the same shape.

*A revenue split that exists and still cannot be drawn.* Visa reports one operating segment and
disaggregates revenue by category, but every category is stated **gross of client incentives**:
service $5,255M, data processing $6,245M, international transaction $4,115M, other $1,647M, less
client incentives of $5,123M, giving $12,139M. The four positive categories sum to $17,262M — a
total Visa never reports — and the incentives are a deduction from revenue, not a segment. A
sankey cannot draw a negative band, and drawing the four alone would put $17.3B of segments
against a $12.1B revenue bar, which is exactly what the sum check exists to catch. So the chart
draws one `Net revenue` bar and the card carries the whole table. **This is a third case, distinct
from "no split published" and from "split not fetched":** the split is real, published and
unusable as bands. Said so on the card in those words rather than letting it read as either of the
other two.

Worth watching: client incentives are 30% of gross revenue and grew 21% against 13% growth in net
revenue.

**Two fixes to the tooling, both found by looking at the rendered image.**

1. `bin/sankey.py` drew a `Cost of revenue ($0M)` label with no bar under it whenever a company
   has no cost line. The node and its label are now created only when the figure rounds to
   something. This also cleans up the NU chart, which has carried that stray label since it was
   built.
2. The first render lost the left-hand segment label **entirely**. The note read "after $5,123M of
   client incentives", which made the label block wider than the 300px left margin, and plotly
   drops an annotation that does not fit rather than clipping it. Shortened to "net of client
   incentives" and it came back. This is the **second** time that trap has cost a label — NBIS lost
   its largest segment's label the same way on 2026-10-26 — and the lesson is the same: the
   validator proves the figures conserve and says nothing about whether the text survived.

**One hardcoded phrase corrected.** `bin/epsnotes.py` wrote "four reported quarters and the one
ahead" into every card. Visa's chart carries five, because the quarter the statement covers
reported today while the vendor's surprise row for it had not published yet — so the Sep '26
actual is Visa's own non-GAAP $3.48 against the $3.43 Zacks consensus, and the spec's source line
says exactly that. The note now counts what the spec holds.

**Verification**: validator silent on all three charts; PNG read at full size — no crossed bands,
no clipped text, five opex leaves overlapped so the seven filed expense lines were grouped into
four; the page served locally shows the V chip, three charts, six KPI tiles, no horizontal
overflow, and hover readouts carrying the year-ago column from the release
(`Operating expenses $4,877M, year ago $4,576M, +7%`).

**Also**: `bin/pefetch.py` re-run across all 67 cards so the `marketAsOf` stamp and every card's
market note agree on Oct 27, 2026. 25 of the 67 now pay a dividend.

---

## 2026-10-27 — Vertiv Q2 2026 charted, and the cost-of-revenue label fixed on every card

**Source**: Vertiv Holdings 8-K exhibit 99.1, filed 2026-07-29, the quarter ended June 30, 2026
(`sec.gov/Archives/edgar/data/1674101/000162828026050323/q22026exhibit991vrt07292026.htm`). Debt,
cash and free cash flow from stockanalysis.com; street consensus from the Nasdaq/Zacks endpoints;
both read 2026-10-27.

**What changed**: `examples/vrt-q2-fy26.json`, `charts/VRT-Q2-FY26.json`,
`assets/financials/VRT-Q2-FY26.png`, the debt and eps specs and their charts, a `VRT` entry in
`financials.json` (67 statements to 68), `wiki/vertiv-q2-fy26.md` (new), and counts in
`wiki/index.md` and `wiki/favorites-financials.md`. Plus every chart re-rendered — see below.

**The quarter**: $3,274.3M of net sales (+24% Y/Y), $2,039.4M of cost of sales, $637.9M of
operating profit (19% margin) and $497.8M of net income (15% margin). The three reportable
segments are geographic and foot exactly: Americas $2,070.8M (+29.2%), Asia Pacific $719.9M
(+28.5%), EMEA $483.6M (+1.7%). The Americas alone is $468.5M of the $636.2M of growth, and
$124.1M of that was acquisitions, leaving 21.1% organic.

**Deliberately one quarter stale, and the card says so.** Vertiv releases Q3 2026 before the open
on Oct 28, 2026 — tomorrow. Q2 is the latest statement it has filed, so that is what is charted,
with a card note stating the position rather than letting the card look current.

**A disagreement inside one filing.** The income statement splits the quarter into $2,646.7M of
products and $627.6M of services; the segment table splits the same total into $2,606.4M of
products and $667.9M of "services & spares". The $40.3M difference is spares, grouped one way in
one table and the other way in the other. Both foot to $3,274.3M. The card quotes the segment
table and names the gap.

**The renderer fix, and it was not new.** The `Cost of revenue` label is drawn below its node, and
that node is the bottom of a *full* column, so its bar reaches the floor of the sankey — the label
landed **on the bar**. VRT's `($2,039M)` was half hidden behind the red rectangle. So were DELL's
`($37.1B)`, HD's `($32.4B)`, SMCI's, TSLA's, PHM's, GE's and MDA's, in every published PNG. I had
noticed this on HD days ago and recorded it as "pre-existing" without fixing it, which is how it
survived.

Nothing flows *out* of a cost node, so the space to its right is always empty. The label now sits
there. **All 68 charts were re-rendered** so the placement is consistent across the page, and the
PNGs recopied; the loss-layout charts are unchanged in appearance.

**The lesson, repeated**: the validator checks that the figures conserve and says nothing about
whether the text is readable. Both defects fixed today — the dropped annotation on V and this one —
were visible only by opening the image. "Pre-existing" is not a status that fixes anything.

**Verification**: validator silent on all three VRT charts; the PNG read at full size; the page
served locally shows 68 chips, the VRT card with three charts, six KPI tiles, no horizontal
overflow, and segment hovers carrying the right percentages (Americas 63.3%, Asia Pacific 22.0%,
EMEA 14.8%).

---

## 2026-10-27 — Event calendar refreshed for all 103 symbols, and its chips now open the statement

**Source**: stockanalysis.com quote pages, read 2026-10-27 through `quotes.py --events`.

**Both refresh jobs in `quotes.py` were dead, and in the same way.** `refresh_pe()` and
`refresh_events()` each read the watchlist out of an inline `<script id="watchlist">` block in
`heatmap.html`. That block stopped existing when the tabs were split into separate pages and the
list moved to `watchlist.json`; neither function had been run since. Both now read
`watchlist.json`, and `--pe` writes its values back there with the `peAsOf` stamp instead of
rewriting a block inside a page.

**`--events` was also destructive by design.** It rebuilt the file from whatever it had just
fetched plus the macro and Fed entries, so `quotes.py --events VRT` would have deleted every other
ticker's events. It now keeps the future-dated events of symbols the run did not ask about, so a
one-symbol refresh touches one symbol. That is why VRT's Oct 28 entry went in by hand earlier
today; it would not have to now.

**The refresh**: 103 symbols read, 59 events in the file — 40 earnings, 5 ex-dividend, 14 macro
and Fed. 43 tickers carry a date. 50 published dates were already in the past and were omitted
rather than estimated, which is the file's own rule.

Two symbols have no quote page at all: VFTNX, a mutual fund, and BCII. MFH's published date is
August 2023 and was dropped as stale.

**One disappearance worth recording.** The previous calendar (generated Oct 19) carried SKHY
earnings on Oct 28. The source now publishes **no** earnings date for SKHY, so the refresh dropped
it. That is the rule working, not a bug, but it means the Oct 28 cluster is GOOG, MSFT, NOW and
VRT, plus the FOMC decision — SK Hynix is no longer on the calendar until a date is published
again. V's Oct 27 entry is kept because it is today's date, and Visa did report tonight.

**Clicking a ticker now opens its income statement.** On the Events page a chip with a ticker
becomes a link to `financials.html?t=<TICKER>`; macro, Fed and corporate chips stay plain. Only
the 68 tickers that actually have a card are linked — the page fetches `financials.json` for that
list, and if that fetch fails the calendar still draws, just without links, so the nicety cannot
break the calendar.

`financials.html` learned to read `?t=` (and a `#TICKER` hash), selects that card, and scrolls to
it. A ticker with no card does **not** silently show someone else's statement: the page falls back
to the first card and says so in the status line, "no card for SPY - showing NVDA instead".
Clicking a chip on that page also writes the ticker into the URL, so any card can now be linked to
directly.

**Verification**: served locally — 27 linked chips and 7 plain ones in the month view, status
reading "40 earnings - 5 ex-dividend - 14 macro/Fed"; the VRT chip opens the VRT card with all
three charts drawn; `?t=SPY` shows the fallback message; clicking a chip on the Financials page
rewrites the URL to that ticker.

## 2026-10-28 — Added the power and nuclear fuel names: CEG, VST, CCJ, LEU, GEV

**Source**: no new document. IBKR `search_contracts` for the contract ids,
stockanalysis.com quote pages for forward P/E and the event dates.

Five names added to `watchlist.json`, 103 symbols to 108. All five are power generation or nuclear
fuel — the group the AI data centre build-out buys its electricity and enriched uranium from:

| Ticker | Company | Conid | Forward P/E | Tags |
|---|---|---|---|---|
| CEG | Constellation Energy | 538132976 (NASDAQ) | 20.92 | Nuclear, Power, Energy |
| VST | Vistra Corp | 254457731 (NYSE) | 14.46 | Nuclear, Power, Energy |
| CCJ | Cameco Corp | 1447060 (NYSE) | 53.71 | Uranium, Energy |
| LEU | Centrus Energy (Class A) | 168391375 (NYSE) | 38.35 | Uranium, Energy |
| GEV | GE Vernova | 691984365 (NYSE) | 43.02 | Power, Industrials, Energy |

All five resolved to their US primary listing. Each symbol returns several contracts — CEG alone
matches a Mexican line, a Challenger Energy, a 2x ETF, a Cerro Grande Mining and a Swiss USD line —
so the match was made on description, not on the first row.

**Two new sector tags, and a label that would have gone wrong without them.** The heatmap's sector
label is the highest-ranked tag a ticker holds, from the `SECTORS` list. `Power` and `Uranium` were
not in that list, and `Energy` outranked `Nuclear`, so all five tiles would have read **Energy** —
the same label as XLE, which is an oil and gas ETF. `Nuclear` now sits ahead of `Energy`, with
`Uranium` and `Power` beside it. The five tiles read Nuclear, Nuclear, Uranium, Uranium and Power.

One existing tile changed with it: **URA** (ETF, Nuclear, Energy) now reads **Nuclear** instead of
Energy. For a uranium miners ETF that is the better label, but it is a change to a tile nobody
asked about, so it is recorded here.

**`SECTORS` is duplicated.** The same list and the same `sectorRank` / `sectorLabel` functions
exist twice — in `assets/site.js`, which `catalysts.html` uses through `Site.sectorLabel`, and
again inline in `heatmap.html`, which uses its own local copy even though it loads `site.js`. Both
copies were byte-identical before this change and both were edited. A future edit to one alone will
silently relabel one page and not the other.

**The stale P/E stamp is gone.** `watchlist.json` still carried `"peAsOf": "Sep 01, 2026"`. With
`quotes.py --pe` working again, a full `--all` pass was run: 108 symbols, 66 values written, 47 of
them different from the September figures, and nothing lost — the pass keeps the old value for any
symbol the source has no forward P/E for. The file now holds a P/E for 67 of 108, up from 48 of
103, and `peAsOf` reads Oct 28, 2026 truthfully. The other 41 are ETFs, funds and companies with no
positive forward estimate, which have no meaningful forward P/E rather than a missing one.

**Calendar**: `quotes.py --events CEG VST CCJ LEU GEV` — the non-destructive version, so the other
103 symbols' dates were untouched. GEV Oct 28, CCJ Oct 30, LEU Nov 4, VST Nov 6, CEG Nov 9. The
file now carries 61 events: 43 earnings, 4 ex-dividend, 14 macro and Fed, across 45 tickers. The
counts moved by less than the five additions because two earnings dates and one ex-dividend date
sat on Oct 27 and have now aged out of the file, which is the rule working.

**GEV reported this morning**, before this was written. This was written at 9:43 a.m. ET with the
market open and GEV down 6.1% on the session, so that is an intraday move and not a close. The
calendar shows the event; there is no card to open for it.

**No Financials cards yet.** None of the five has an income statement chart, so their calendar
chips are plain text rather than links — which is the honest behaviour the chip linking was built
for, now exercised by five names on its first day. All five file real statements and are
chartable.

**Verification**: served locally — 108 tiles on the heatmap, all five priced, reading Nuclear,
Nuclear, Uranium, Uranium and Power; URA reads Nuclear and XLE still reads Energy. The Events month
view shows GEV, CCJ, LEU and VST as plain chips with no `href` (CEG is November, outside the
month), status "43 earnings · 4 ex-dividend · 14 macro/Fed". The IBKR watchlist was read back after
the edit: 106 instruments, the five new ones appended, nothing dropped.

**The IBKR watchlist is two names short of the repo.** It holds 106 instruments where
`ibkr-conids.json` has 108 symbols: **BITF** and **MFH** have conids in the repo but are not in the
broker's list, and were already absent before this change. Left as found rather than silently
added, since why they are missing is not known.

**`wiki/index.md` said 53 of the 68 charts carry a segment split.** Counted from the specs it is
54, which is what `favorites-financials.md` already said — the index line was not updated when
Vertiv was charted. Corrected.

## 2026-10-28 — Every name that reported today, charted: GOOG, MSFT, NOW, VRT and a first card for GEV

**Sources**: the five companies' own Item 2.02 8-K exhibits filed October 28, 2026, plus GE
Vernova's 10-Q of the same date. Market figures and balance sheet columns from stockanalysis.com,
read 2026-10-28.

The event calendar had five names reporting today. All five had filed by mid-morning, so all five
are now charted on their just-reported quarter. The Financials tab goes from 68 cards to 69.

| Ticker | Was | Now | Revenue | Y/Y | Operating margin | Net |
|---|---|---|---|---|---|---|
| GOOG | Q2 FY26 | Q3 FY26 | $127,577M | +25% | 32% | $26,468M, **−24%** |
| MSFT | FQ4 FY26 | FQ1 FY27 | $92,279M | +19% | 50% | $36,629M, +32% |
| NOW | Q2 FY26 | Q3 FY26 | $4,106M | +21% | 9% | $277M, **−45%** |
| VRT | Q2 FY26 | Q3 FY26 | $4,312.8M | +61% | 23% | $764.5M, +92% |
| GEV | — | Q3 FY26 | $12,642M | +27% | 11% | $1,289M, +185% |

**Two of the five grew revenue and shrank profit, for opposite reasons.** Alphabet's operating
income rose 30% while net income fell 24%, entirely from a $20,980M swing in other income — from
+$12,759M a year ago to −$8,221M. Nothing operating changed. ServiceNow's fall is the opposite: it
is above the line, in cost of subscription revenue, which rose 58% against 21% subscription revenue
growth and took gross margin from 77.3% to 70.5%. Both cards say which it is, because a net margin
read alone would mislead in both directions.

**GE Vernova is the first card in this repo built from a 10-Q.** Its earnings release is organised
around adjusted EBITDA and carries segment cost of revenues but no consolidated profit and loss
statement, so there was nothing in the 8-K exhibit to chart. The 10-Q filed the same morning has
one. `bin/edgar.py GEV R2` prints it on its own, which is what that script exists for.

**Microsoft recast its segments, from three to two.** Productivity & Business Processes,
Intelligent Cloud and More Personal Computing are gone; the reportable segments are now Agents and
Infra ($76,795M) and Devices and Consumer ($15,484M). Two bands say almost nothing about a 19%
quarter, so the card draws the eight product and service offering lines Microsoft reports
alongside, which foot to the same $92,279M: Azure $33,165M (+48%), Microsoft 365 cloud $27,778M,
productivity and server licensing, search and advertising, XBOX, industry solutions, Windows OEM
and devices, frontier and support services. Prior-year figures are Microsoft's own recast ones.

**Eight segments is a layout limit, found by looking.** The validator printed no warnings on the
first MSFT render. The image showed every segment's "% of revenue" line sitting on the next
segment's name — eight blocks share about 90 pixels each in the left column, and a four-line block
does not fit. The ratio line was dropped on that card; the Y/Y stayed, because that is what the
quarter is about. `wiki/sankey-income-statement.md` already said a label carries at most two
sub-lines; this is the first card that had to obey it. **Three sessions running, every layout
defect has been invisible to the validator and obvious in the image.**

**Three cards have no debt chart.** `bin/debtfetch.py` refused GOOG, MSFT and NOW: the data source
has no balance sheet or cash flow column for 2026-09-30 yet, hours after the releases, and the
builder will not pair a June balance sheet with a September income statement. It was run twice,
twenty minutes apart, with the same result. The stale June specs were deleted rather than left to
render beside the new statements, each card carries a note saying the chart is pending and why,
and `debtfetch.py` will pick them up on the next run. VRT and GEV went through and have theirs.

**The earnings-surprise rows are a quarter behind too.** Nasdaq's endpoints still show Jun '26 as
the last reported quarter for all five, with Sep '26 as the estimate ahead, so each card's EPS
chart shows a consensus for the quarter its own income statement already covers. That is the same
state Visa's card was in yesterday, and `bin/epsnotes.py` words it correctly.

**One spec per ticker, enforced by deletion.** `bin/segapply.specs()` maps ticker to spec by
walking `examples/*.json` sorted, last one wins. With both `msft-fq1-fy27.json` and
`msft-fq4-fy26.json` on disk, `fq4-fy26` sorts last and would have shadowed the new quarter for
every tool that uses that map. Nothing broke today — `segnotes.py` only rewrites placeholder
notes — but the four superseded specs were deleted, along with the superseded chart JSON and PNGs,
and the repo is back to one spec per ticker. Git history keeps the old ones.

**Arithmetic corrected in my own drafts before they shipped**: Vertiv "12% above the guidance
midpoint" was 15%; the products/services spares gap was $43.3M, not $43.2M; GE Vernova's net cash
is five times gross debt, not six — cash is six times gross debt, net cash is five.
`wiki/index.md` also still said 53 of the charts carry a segment split; it is 55 of 69 now.

**Verification**: served locally — all five cards draw, headings read Alphabet · Q3 FY26,
Microsoft · FQ1 FY27, ServiceNow · Q3 FY26, Vertiv Holdings · Q3 FY26 and GE Vernova · Q3 FY26;
VRT and GEV show three live charts each, GOOG, MSFT and NOW show two plus the pending-debt note;
the status line reads 69 statements; `?t=GEV` deep-links to the new card. Every sankey was opened
as an image and checked for crossing bands, labels on bars and clipped text.

## 2026-10-28 — Alphabet's debt chart, built from the filing instead of waiting

**Source**: Alphabet 8-K exhibit 99.1, Oct 28, 2026 — the condensed consolidated balance sheet and
statement of cash flows (source: sec.gov/Archives/edgar/data/1652044/000165204426000080/googexhibit991q32026.htm).

The GOOG card shipped a few hours ago with no debt and coverage chart, because `bin/debtfetch.py`
could not find a 2026-09-30 column at the data vendor. A third run still could not, and the SEC's
own XBRL company-concept API has nothing newer than 2026-06-30 for Alphabet either — the detail
arrives with the 10-Q, which is not filed yet. So the figures were read from the release.

| Bar | Q3 FY26 |
|---|---|
| Debt | $141,917M |
| Cash & equivalents | $56,334M |
| Free cash flow | **−$9,065M** |

Net debt $85,583M, with a further $208,764M of marketable securities beside the cash. Free cash
flow is negative because capital expenditure was $51,355M against $42,290M of operating cash flow.
Long-term debt went from $46,547M at Dec 31, 2025 to $125,102M at Sep 30, 2026; the quarter alone
brought $28.7B of senior unsecured notes and $12.4B raised through an at-the-market equity program.

**The bar is understated and the card says so.** Alphabet's condensed balance sheet does not break
out the current portion of long-term debt or the current operating lease liability — both sit
inside accrued expenses and other current liabilities. The bar is non-current debt only:
$125,102M of long-term debt plus $16,815M of long-term operating leases. At Jun 30, 2026 the two
missing lines were $1,999M and $3,446M, so the shortfall is about 4%.

**A hand-built spec must not freeze.** `bin/debtfetch.py` skips any ticker that already has a spec
unless named or given `--all`, so a spec written by hand would have blocked the complete one
forever — the same shadowing trap recorded earlier today for `segapply.specs()`. The spec carries
`"partial": true`, and `debtfetch.py` now treats a partial spec as missing and retries it on every
run, printing `~ GOOG: partial spec on disk, retrying`. It will overwrite this file with the real
balance sheet when the vendor has one.

**MSFT and NOW are still without theirs, and both are now reachable.** Microsoft filed a 10-Q today
and the SEC XBRL API carries its 2026-09-30 balance sheet in full. ServiceNow's 8-K exhibit carries
a balance sheet, and XBRL has its cash and lease liabilities at 2026-09-30. Neither was built here;
this entry records that the data exists so the next run does not repeat the search.

**Verification**: served locally — the GOOG card draws three charts, the pending-debt note is gone,
the understated-bar note is on the card, and the debt figure reads $141,917M. The bar image was
opened: the negative free cash flow bar draws below the axis with its label clear of it.

## 2026-10-28 — Microsoft's and ServiceNow's debt charts, and a stray gridline under every all-positive one

**Sources**: Microsoft 10-Q filed Oct 28, 2026 — balance sheet, cash flow statement and the
supplemental lease note (`bin/edgar.py MSFT R73`). ServiceNow 8-K exhibit 99.1 of the same date —
condensed balance sheet and statement of cash flows.

The last two cards missing a debt chart now have one, read from the filings for the same reason
Alphabet's was: the data vendor still has no 2026-09-30 column. Unlike Alphabet's, **both of these
are complete** — every line the vendor's own composition uses is published, so neither spec is
marked partial.

| | Debt | Cash | Free cash flow | Net debt |
|---|---|---|---|---|
| MSFT FQ1 FY27 | $133,931M | $20,281M | $18,633M | $113,650M |
| NOW Q3 FY26 | $8,415M | $2,393M | $748M | $6,022M |

**Microsoft's debt is mostly leases.** $10,763M current and $87,687M long-term, against $4,391M of
current and $31,090M of long-term borrowings. Finance lease liabilities alone are $70,973M. Those
figures are not on the face of the balance sheet — the current portions sit inside "other current
liabilities" and the finance leases inside "other long-term liabilities" — so they come from the
lease note. The composition was checked against the vendor's own Jun 30 spec before use: current
leases $9,683M = operating $5,393M + finance $4,290M, long-term $78,836M = $16,532M + $62,304M.
Both foot exactly, so the Sep 30 figures are built the same way.

**ServiceNow's debt is new.** At Dec 31, 2025 it carried $1,491M of long-term debt and no
short-term debt; it now carries $5,438M and $2,086M, having raised $3,943M of senior notes and
spent $9,167M on business combinations over the nine months. Goodwill went from $3,578M to
$10,012M in the same period.

**A gridline nobody asked for.** The first MSFT render drew a labelled **−20B** line under three
bars that never go negative. `bin/debtbars.py` padded the axis 16% below the lower bound, and with
`lo = 0` that reached a whole tick. Dropping the pad to zero removed the label but crowded the
quarter label against the baseline, so an all-positive chart now keeps a thin 4% skirt: plotly
spaces ticks at roughly an eighth of the range or wider, so 4% can never reach the first negative
one. A chart with negative free cash flow still gets the full pad, because something is drawn there.

This only ever showed when the pad happened to reach a tick, which is why it survived 65 cards.
The four other charts touched today were re-rendered; the rest keep their old padding until they
are next rendered, which changes nothing about their figures.

**Only one card on the Financials tab now has no debt chart**: 7974, Nintendo, which has not had
one since it was charted.

**Verification**: served locally — both cards draw three charts, the pending-debt notes are gone,
MSFT reads $133,931M and NOW reads $8,415M. Both bar images were opened: no negative gridline, the
quarter label clear of the axis.

---

## 2026-10-28 — the earnings charts were comparing two different things

Kevin noticed the actual-vs-estimate chart "is not updated" after the five Oct 28 reports. It is
not: every one of those five still shows Jun '26 as its newest reported quarter. But the reason is
not this repo, and chasing it turned up something worse.

**The vendor is the one that is behind, not `epsfetch.py`.** All five endpoints were queried live:
Nasdaq's surprise table still ends at Jun 2026 for NOW, GOOG, MSFT, VRT and GEV, and Sep 2026 is
still sitting in the *forecast* table hours after all five reported. A refetch today writes
byte-identical files. NOW's earnings-date endpoint is blank too -- "our vendor, Zacks Investment
Research, hasn't provided us with the upcoming earnings report date." Zacks posts the surprise row
a day or two after the print, so the charts fill themselves in without intervention.

**The real defect: a GAAP actual scored against an adjusted consensus.** The two sides of a row
come back as one pair with no statement of basis, and they are not always on the same one. Alphabet
Jun '26 read **$9.11 actual against $2.88 expected -- a 216% beat**. The $9.11 is Alphabet's real
GAAP diluted EPS, but about **$6.26 of it was an unrealised gain on equity securities** that the
consensus never included; on a like-for-like basis the quarter was roughly level. GE Vernova's
Dec '25 row does the same thing with the Prolec remeasurement gain: $13.39 against $3.05.

So the Financials page was publishing a 216% beat where the company roughly matched. The figures
were both real; the subtraction between them was not.

**A third basis, which is why NOW looked wrong.** ServiceNow Q2 FY26: the company reported **$0.29
GAAP** and **$0.90 non-GAAP**; the vendor's actual is **$0.31**. It matches neither. Zacks computes
its own normalised EPS, and for some names it lands away from both of the company's own figures.
That is why the card's "Sep '26 consensus $0.56" matches neither the $1.02 the press quoted (the
company's non-GAAP basis) nor the $0.27 GAAP actual. The series is internally consistent, so it is
still publishable -- but the card used to call it "adjusted EPS as the street scores it", which was
simply false. That claim is gone.

**The rule.** There is no basis field to read, so a pair is judged on its own plausibility: a
profitable company does not miss or beat its own consensus by half. Both sides must be positive,
because a loss maker crossing zero makes the ratio meaningless rather than wrong -- MSTR's
-$38.25 against -$3.41 is arithmetic, not a bad figure.

    gap >= $0.15  and  gap / estimate > 0.40     ->  basisUnverified

Calibrated against all 255 stored rows: it flags **15 rows on 11 cards** -- CRM, DELL, GEV, GOOG,
INTC, ORCL, SKHY, SMCI, SNDK, SPCX, TSLA -- and leaves 240 alone. The $0.15 floor is what keeps
DDOG's $0.17-against-$0.06 out of it; a 183% "beat" on an eleven-cent gap is uninformative either
way, but it is not evidence of a mixed basis.

A flagged pair is still drawn -- both figures are real -- but the chart stops asserting that the
distance between them means anything: **the joining hairline goes dotted, the surprise row
disappears from the hover, and the card's note says why.** `bin/epsdots.py` prints a `~` line for
each one so a render says which cards carry them.

**Same lesson as the sankey labels and the stray gridline, third time now.** The validator checks
that a reported quarter has both figures present. Both were present. Nothing in this repo could
have caught a number that is correct, well-formed, and measuring something else -- only reading it
against the filing did.

**Not a restatement**: ServiceNow filed an 8-K/A for Q3 FY26 (`erq3fy262.htm`). Every figure in it
matches the original -- revenue $4,106M, operating income $385M, net income $277M, GAAP EPS $0.27,
non-GAAP $1.00, cRPO $13.65B. It also confirms the **five-for-one stock split**, which is why the
per-share figures on that card are small against the historical ones.

**Housekeeping**: five background shells had been spinning since this morning. Each waits on
`pgrep -f epsfetch.py` (or `pefetch.py`) from inside a shell whose own command line contains that
string, so `pgrep -f` matches the waiter itself and the loop can never exit. Killed. The pattern
that works is `pgrep -f "[e]psfetch.py"`.

**Verification**: served locally. 15 rows withhold the surprise figure and carry the basis warning;
240 still show theirs -- MSFT Jun '26 still reads `+$0.53 (+13%)`. The Alphabet image was opened:
Mar '26 and Jun '26 join with a dotted line, Sep '25 and Dec '25 stay solid.

---

## 2026-10-28 — IREN added: a quarter that is never filed on its own

Kevin asked to add IREN. Watchlist, conid, income statement, earnings and debt charts, wiki page.
The Financials tab goes from 69 cards to 70.

**IREN's fiscal year ends June 30, so its fourth quarter is reported nowhere.** A December-year
company files a Q4 8-K; a June-year company's fourth quarter exists only inside the annual figures.
So this card is the first in the repo built by **subtraction**: the twelve months in the FY26 10-K
minus the nine months in the 10-Q to Mar 31, 2026.

That has to prove itself before it can be published, and it does, three ways: revenue comes to
exactly $137,225K, pretax to $(691,968)K, net to $(683,999)K, and the two segments foot to revenue
to the dollar. An aggregator reading the same two filings independently reports $137.23M,
$(691.97)M and $(684.00)M. The year-ago column is derived the same way so the Y/Y is like for like.

**AI Cloud passed Bitcoin Mining.** $70.5M against $66.7M, 51.4% of revenue against 3.7% a year
ago, +913% Y/Y while mining fell 63%. Total revenue still fell 27%, because mining lost $113.6M of
quarterly revenue and AI Cloud added only $63.6M. A transition, not yet a replacement. Over the
full fiscal year AI Cloud was $128.8M against mining's $578.2M, so the crossover is a quarter-end
event rather than a year-long trend.

**Two things on this card would mislead if left to stand alone**, and both are called out:

*The 76% gross margin is not comparable to anything else on the page.* IREN reports cost of
revenue **exclusive of D&A**, and D&A was $112.1M against $33.3M of cost of revenue -- more than
three times larger. For a bitcoin miner the depreciation of the hardware *is* the cost of
production. Carrying it above the line would put gross profit at a loss. The figure is faithful to
the filing and comparable to nothing.

*The loss is one charge.* Impairment of assets was $450.4M -- 62% of the $724.3M of operating
expenses and 328% of revenue. Without it the operating loss is around $170M. `mkspec.py` would have
buried this inside a single $596.0M bar called "Other operating", because it only knows R&D, SG&A
and a remainder. The bar was split by hand into SG&A, D&A, impairment and a net other, so the chart
shows what actually happened. Rounding the four parts individually summed to 596.1 against a true
596.020, and the 0.1 was taken off the smallest and most aggregated line rather than off the
impairment or D&A, which are single reported figures.

**The balance sheet is the company.** $7,839.5M of debt against $5,895.6M of cash, net debt
$1,943.9M. Free cash flow -$167.1M: $1,811.1M of operating cash flow against **$1,978.2M of capex**
-- about fourteen times the quarter's revenue, spent in the same three months.

**This is not the most recent quarter that exists.** IREN had not filed its FQ1 FY27 10-Q for the
September quarter when this was built; last year's landed Nov 6. So the card is the most recent
quarter *on file*, and says so.

**Heatmap tile**: tagged `AI Infra, Data Center, Crypto, Mining`, so it reads **AI Infra** -- the
highest-ranked tag wins. That is a judgement call: AI Cloud is now the majority of revenue, but
IREN is still a bitcoin miner converting its own sites. Dropping `AI Infra` would move it to
Data Center, which is where HUT sits.

**A gap in my own earlier work, found while updating the index**: the five wiki pages written
earlier today -- Alphabet, Microsoft, ServiceNow, Vertiv Q3 and GE Vernova -- were never added to
`wiki/index.md`'s Companies list. Only its counts had been updated. All five are listed now,
with IREN.

**Verification**: served locally. The chip appears, the header reads FQ4 FY26 quarter ended
Jun 30 2026, all three charts draw, and the KPIs read $137.2M / 76% / ($620.4M) / ($684.0M).
The sankey image was opened: no crossed bands, no clipped labels, flows proportional. The debt
image was opened: the negative free cash flow bar draws below the baseline with the quarter label
clear of it.

**IREN's next report has a confirmed date.** The event refresh that ran alongside the card came
back with Nov 5, 2026 for IREN, so the card and the page now cite that instead of hedging off last
year's Nov 6 filing. The derived FQ4 FY26 card is superseded in about a week by a quarter that is
actually filed. The same refresh rewrote the whole calendar: 49 upcoming ticker events, 57
published dates already past and omitted rather than estimated, 14 macro and Fed entries kept.

## 2026-10-28 — a skill for adding a ticker, and the brief job pointed back at a file that exists

**Source**: none — this is workflow, not a filing.

**What changed**: new skill `.claude/skills/add-ticker/SKILL.md`. Adding a ticker touches seven
places and the order between them is a dependency chain, not a preference: the Financials
pipeline reads `financials.json`, and the IBKR and events steps read `watchlist.json`. That order
lived only in my head and in the shape of past runs. It is written down now.

The seven: the heatmap tile in `watchlist.json`, the IBKR watchlist in `ibkr-conids.json` plus the
connector, the Financials card, `events.json`, `news.json` for catalysts, `brief.json` for the
Morning Brief, and the wiki. Four of the seven are unconditional; the card depends on the ticker
being chartable at all, and the last two apply only to favorites.

**It delegates rather than duplicates.** The income statement half is still
`income-statement-chart`'s job — sourcing, the mandatory segment split, `mkspec.py`, `sankey.py`,
the five-identity validator. `add-ticker` calls it and then does the three things that come after
it and read what it wrote: `debtfetch.py`/`debtbars.py`, `epsfetch.py`/`epsdots.py`/`epsnotes.py`,
and `pefetch.py`.

**Both skills answered to "add NVDA", which is one trigger too many.** `income-statement-chart`'s
description has been narrowed to charting an existing ticker and nothing else, and now points at
`add-ticker` for a new name. `add-ticker` owns "add <TICKER>".

**A break found while writing step 6.** `bin/morning-brief.sh` told the 6am job that the watchlist
"lives in heatmap.html in the JSON block with id=`watchlist`". That block has not existed since
the site was split into five pages and the watchlist moved to `watchlist.json` — `grep -c` returns
0. So the job was being sent to a source that is gone, and the step the skill describes as
automatic, a favorite reaching `brief.json`'s `favorites[]` by way of `"fav": true`, was not
reliably automatic at all. The prompt now names `watchlist.json` and says to read favorites from
it so a new one is picked up without editing the prompt again.

**Two things the skill records because they are not visible from the code.** The ranked `SECTORS`
list exists twice — `assets/site.js` and inline in `heatmap.html` — so a genuinely new sector has
to be added to both or the two pages disagree about what a tile is. And `edit_watchlist` is
full-replace: writing just the new symbol deletes the other 108.

**Verification**: both skills' frontmatter parses and both are listed. `bash -n bin/morning-brief.sh`
passes. Every figure quoted in the skill was checked against the repo rather than recalled —
15 favorites of 109 symbols, 70 cards against 70 tracked income-statement PNGs and 206 tracked
chart JSONs, `ibkrWatchlist` id 100, BITF and MFH carrying explicit `UNRESOLVED` notes.

## 2026-10-28 — the published heatmap could not price anything, and why the fix is a file

**Problem**: https://kevinyang13.github.io/stock-kb/heatmap.html painted its 109 tiles and then sat
on "0 of 109 priced, retrying 109..." forever. Deployment was not at fault: the live `heatmap.html`
was byte-identical to the local one and the live `watchlist.json` carried all 109 symbols.

The page fetches quotes from the browser, and **every quote feed refuses a cross-origin request
from the Pages origin**. Probed from the live page itself, all six throw `TypeError: Failed to
fetch`: stockanalysis.com, Yahoo query1 and query2, Stooq, Nasdaq and CNBC. A control fetch to
api.github.com from the same page returns 200, so cross-origin itself is fine — these six
specifically refuse browsers. The in-page fallback, `fetch("api/quotes?...")`, is the `quotes.py`
proxy, which only exists when `quotes.py` is the server, so on Pages it 404s. No source at all.

It works from localhost, which is why this went unnoticed: stockanalysis.com allowlists localhost
and 127.0.0.1, and still prices 105 of 109 there.

**A correction worth recording**: CNBC was going to be the fix, on the strength of it answering
`curl` with `access-control-allow-origin: *`. It does — to curl. A real browser gets an Akamai
block page instead ("Access Denied ... errors.edgesuite.net"), which carries no CORS header, so
the browser reports it as a CORS failure. Verified twice: `fetch()` from the page throws, and a
tab navigated straight at the URL renders the Access Denied page. **curl is not a valid test for
whether a browser can read an endpoint.** The CNBC work was written, tested and thrown away.

**What landed**

- `prices.json` — a committed snapshot the page reads as its price source. Shape, so that anything
  able to reach a feed can write it: `generated` (ISO 8601), `generatedLabel`, `source`, and
  `quotes` as `[{t, price, pct}]`. A symbol the writer could not price is **left out**, never
  written with a null, so a gap reads as "no quote" rather than as a price of nothing. The file
  ships empty: no writer exists yet, and the choice of feed is still open.
- `assets/site.js` — `Site.prices()` is now the one entry point. It paints the snapshot first, so
  the page never hangs on "loading", then upgrades it with a live fetch where one is reachable. A
  snapshot is labelled with **its own timestamp and age** ("4h old"), never the time it was read,
  so a stale snapshot cannot pass for live. With neither snapshot nor live source the page says
  "prices unavailable" and names which half failed.
- `fromStockAnalysis` now gives up instead of retrying when *nothing* answered. The two retry waves
  exist for rate-limiting, and a CORS wall is not rate-limiting: on Pages they were six seconds of
  waiting for the same nothing.
- The quote code was **duplicated** in `heatmap.html` and `assets/site.js`. The copy in
  `heatmap.html` is gone; it and `catalysts.html` both call `Site.prices` now.

**Verification**: all three branches exercised in the browser. Live on localhost — 105 of 109,
labelled `source: stockanalysis.com`. Snapshot with the live fetch stubbed out — `live: false`,
the snapshot's own label and age, and BITF correctly absent rather than nulled. Empty and missing
`prices.json` with no live source — `hits: 0` and "prices unavailable". Catalysts renders day
moves as before.

**Still open**: nothing writes `prices.json`. Kevin chose IBKR as the feed, but the connector is a
claude.ai connector rather than a local MCP server, so the headless `claude -p` that launchd runs
cannot reach it, and `get_price_snapshot` takes one symbol per call — 109 calls, no batching. The
file format is deliberately writer-agnostic so that decision stays open.

## 2026-10-29 — four of the five names that reported today, charted from their own filings

**Sources**: Sandisk 8-K ex-99.1, Amazon 8-K ex-99.1, Intel 8-K ex-99.1 and Coinbase's 10-Q, all
filed Oct 29, 2026. Strategy's 8-K ex-99.1 of the same date was read and deliberately not charted.

**What changed**: SNDK, AMZN, INTC and COIN moved off the June quarter and onto the one they
reported this afternoon. All four statements were read from the filing rather than the aggregator,
which has no column for these period ends yet. Four new wiki pages, listed in the index.

**Every segment split foots exactly.** Sandisk's three end markets to $11,031M, Amazon's seven
product lines to $201,944M, Coinbase's three revenue sources to $1,215.6M. Intel's do not and
cannot: it reports business-unit revenue **inclusive of intersegment sales**, so Intel Products
$15.4B plus Foundry $6.7B plus All Other $0.7B is $22.8B against $16.5B consolidated, with $(6.3)B
of eliminations. The card draws CCPG and DCAI as reported and carries Foundry-external-and-other as
the $1,113M residual, which also absorbs the rounding — the 8-K gives business units to $0.1B only.

**Three of the four quarters are stories about where profit sits, not how much there is.**

- **Amazon**: operating income +61%, net income **−2%**. The year-ago quarter had $10,748M of
  non-operating income; this one had a $1,207M expense. Operating income is the comparable figure.
- **Coinbase**: operating income $61.7M, net income $718.7M. $715.0M of the difference is a mark on
  crypto Coinbase holds for its own account. The 59% net margin is a balance sheet, not a business.
- **Intel**: net margin 21% against a 15% operating margin, because $1,460M of the profit is equity
  gains plus interest and other. Net income fell 18% while operating income rose 269%.
- **Sandisk** is the exception and still carries a caveat: $513M of its $539M non-operating line is
  a gain on equity securities. Its real figure is $8,780M of operating income on revenue that grew
  378% while cost of revenue grew 2%.

**Strategy (MSTR) was read and not charted, on purpose.** Q3 revenue was $125.4M and operating
income was $20,909.8M, because a **$20,912.4M gain on digital assets is reported inside operating
expenses**. Excluding it, gross profit of $89.6M against $92.2M of cash opex is a $2.6M operating
loss. A Sankey conserves flow, so an operating profit 167 times revenue cannot be drawn without
recasting Strategy's own operating income line into a non-operating one. The Q2 FY26 card, which used the loss layout because that quarter's digital-asset move was a
charge rather than a gain, stays up. This needs a decision about recasting before it can be charted.

**Two things on these cards are honestly stale and say so.** The debt chart is still the prior
quarter: `debtfetch.py` reported "no column for 2026-10-02" and the like for all four, and the
releases give cash flow year to date rather than for the quarter, so a quarterly free-cash-flow bar
could not be read from them either. And the earnings chart does not yet carry today's print — the
vendor still shows Jun '26 as the most recent actual. Each card now names the reported GAAP EPS and
the consensus beside it **without scoring a surprise**, because the two are not on the same basis.
That is the rule commit a19008c put in; this is the first time it has been applied by hand.

**Verification**: every spec rendered with no validator warnings and all four images were opened
and checked — no crossed bands, no clipped labels, flows proportional. `financials.json` parses.
The SNDK card was loaded in the browser: chip, header "FQ1 FY27 quarter ended Oct 2, 2026 · 8-K
filed Oct 29, 2026", KPIs $11,031M / 85% / 80% / $8,101M, and the live chart draws.

## 2026-10-29 — Events calendar: a window that starts behind today

**Source**: nyse.com/markets/hours-calendars (read 2026-10-29) for the market closures. Ticker
dates from stockanalysis.com via `quotes.py --events`.

The Events tab opened on the current calendar month, drawn as a fixed 42-cell grid anchored on the
1st. On Oct 29 that showed Sep 27 – Nov 7: one week of November, and nothing of the back half of
the month. The request was a window running from Oct 26 through the whole of November.

**The page now draws an arbitrary span rather than a month.** `renderMonth` became `renderSpan`,
which takes two inclusive calendar days, widens them out to whole weeks, and computes its own cell
count. `spanFor()` names the windows: "This month" is unchanged, and the new default, **"This week
+ next month"**, runs from the Sunday of the current week to the last day of the following month —
Oct 25 to Nov 30 today. It is deliberately not anchored on the 1st. The week behind today holds the
quarter that just reported, and reading it beside what is still scheduled is the point of the page;
a month view drops those the moment the month turns.

Three things had to change with it:

- **Cell counting is calendar arithmetic, not clock arithmetic.** `(last - start) / 86400000` is an
  hour out across the November 1 DST change, which rounds to a 43rd cell and breaks the
  seven-column grid for the rest of the year. `dayDiff()` subtracts `Date.UTC(y, m, d)` triples
  instead. This is the same trap the file's existing `parseDay()` comment warns about, in a
  different place.
- **`out` now means outside the window**, not "a different month from today" — otherwise the
  default view dimmed all of November.
- **The day number names its month** on the 1st and on the opening cell, because a window can run
  across three months and a bare "3" is then ambiguous.

The status line now reads the window it is showing (`Oct 25 – Nov 30`) and counts only the events
inside it, with the fetch date moved to the end as "dates as of". It previously counted the whole
file, which includes December, and so described a calendar the reader could not see.

**The refresher had to change first, or the widened window would have been empty behind today.**
`refresh_events()` dropped every date earlier than today. That rule exists because the source
publishes one date per field with no flag saying whether it is the next one or the last one — but
the ambiguity only runs forward. A future date may be a stale leftover; **a past date is a fact**,
the day the company reported. So `KEEP_PAST_DAYS = 10` now bounds how far back the calendar keeps
one, and a past date already in the file survives even when the run refreshes that symbol: the
source swaps in the next date as soon as a company reports, and the day it actually reported is
then unrecoverable from the feed. Without that, this run would have deleted the Oct 28 and Oct 29
earnings — GOOG, MSFT, NOW, GEV, SKHY, VRT, then AMZN, INTC, COIN, MSTR, SNDK — the week the
window was widened to show.

**The refresh then put 17 more events on the calendar**, 49 ticker entries to 66. The week behind
today filled in: VZ on Oct 26, BA and V on Oct 27, and the ASML, GEV and V ex-dividends — all
dates the old rule had thrown away. The one that matters most is **INTU on Nov 19**, which had no
calendar entry at all; it is a favorite and the employer, and the Morning Brief covers it every
day.

**Six favorites still have no earnings entry and none was invented.** TSLA (Oct 21), META (Oct 21)
and SPCX (Oct 20) are in the file but fall behind the default window, which opens on Oct 25 — the
month view shows them. **MU, SMH and NBIS return no earnings date from the source at all.** SMH is
an ETF and has none to give. MU and NBIS should have one, so that is either a parse miss in
`cell()` or a field the source is not publishing for them; it needs a look rather than a guess.
NBIS is the live one — a favorite with an open position and a Q3 report due in November that the
calendar cannot currently show.

**Four market closures added** as a new curated `holiday` type, which `quotes.py` preserves and
never fetches: Thanksgiving (Nov 26, closed), the day after (Nov 27, 1:00 pm ET), Christmas Eve
(Dec 24, 1:00 pm ET) and Christmas Day (Dec 25, closed). The chip is deliberately colourless and
italic so a closure reads as an absence of trading rather than as another event competing with the
earnings around it.

## 2026-10-29 — A share-ownership donut on every Financials card

**Sources**: SEC Form 13F data set covering filings received June–August 2026, holdings as of
**June 30, 2026** (source: sec.gov/data-research/sec-markets-data/form-13f-data-sets), and
stockanalysis.com's statistics endpoint. Full method in [[share-ownership-donut]].

A fourth chart now sits beside the sankey: four slices of the whole share count — index and ETF
managers, other institutions, insiders, and the residual everyone else — with the institutional
total in the hole. **Hovering either institutional slice names its five largest holders**, each as
a percentage of all shares outstanding, read from that manager's own 13F. 66 of the 70 cards have
one.

**It takes two sources, and that is the whole design.** A raw 13F sum is not an ownership
percentage: managers with shared investment discretion report the same shares twice, so adding the
table up for NVIDIA gives **24.8bn shares against 24.1bn outstanding**, 103% of the company — and
11.2bn of those shares are filed under `DFND`, the code for exactly that shared discretion. So the
slice sizes come from stockanalysis's institutional and insider percentages, which are a netted
pair leaving an honest residual, and the filings supply the ratio inside the institutional slice
and the names. Dividing one 13F total by another cancels most of the double counting. The two are
on different dates and both cards and wiki say so.

**The filings had to be checked before they could be used.** The largest single reported holding
of NVIDIA in this data set is **7.0bn shares by a state teachers' pension fund** — 29% of the
company, and about four times that fund's entire portfolio. Nobody rejects an implausible 13F. A
naive top-five would have published it at number one, on a public site.

The check uses the only other number in the table. A filer reports both a share count and a market
value, so `VALUE / SSHPRNAMT` is an implied price, and for a real filing it is the period-end
price: every honest NVIDIA filer implies **$200.09**, the pension fund implies **$0.005**. One
deliberate exemption — Form 13F moved `VALUE` from thousands to whole dollars in 2023 and a
minority still file the old way, implying exactly the price over a thousand. T. Rowe Price is one;
its **share count is right**, so it is kept. 113 of NVIDIA's 5,927 filings were dropped.

**The same test identifies the company.** Filers type the issuer name freehand, so a name match
alone can land on the wrong CUSIP. A candidate is accepted only once its filers imply the price
this ticker actually closed at on the period end, read from its own history — a wrong company
fails immediately.

**The passive split is an editorial call and is labelled as one.** A 13F says what a manager holds
and never why; BlackRock files one covering iShares and its active mandates together, with no field
separating them. So the list in `bin/passive-managers.json` is conservative — FMR, JPMorgan, Morgan
Stanley, Goldman, Capital Research, T. Rowe and Invesco are all counted as **active**, which
understates the index share rather than overstating it. The list is a data file, not code, so it
can be audited and argued with.

**Four cards have no donut and each refusal is right**: Nintendo (7974) has no US statistics page;
ARQQ and PHM report institutional plus insider percentages that exceed 100%, leaving no honest
residual; SKHY had not listed by June 30, so no 13F names it. The generator reports and skips
rather than drawing a slice it cannot support.

**Verification**: all 66 specs rendered with zero validator warnings — the validator checks that
the slices sum to 100%, that none is negative, and that no named holder owns more than the group
it sits in. The NVDA and DELL cards were opened in the browser and hovered; DELL's 47.1% insider
slice is Michael Dell and reads correctly, as do GOOG at 9.8%, AMZN at 8.9% and META at 13.4%.
Checked at phone width: the donut goes full-width and its legend wraps to two columns.

One fix found on the way: `own` was first written into `financials.json` as a path. `Sankey.load()`
takes a **stem** and builds `charts/<stem>.json` itself, so the page asked for
`charts/charts/NVDA-own.json.json` and the figure silently removed itself. The debt and earnings
charts have always used stems; this one now does too.

## 2026-10-29 — A local-only Holdings page

**Sources**: none — this page holds nothing but figures typed into it, plus live prices from the
`quotes.py` proxy.

A scenario table for positions actually held: shares and cost basis down the left, then a group of
three columns per scenario — price per share, position value, profit or loss — and a totals row.
Every price cell is editable, scenarios can be added and removed, and the arithmetic is the
obvious one: `shares × price`, against `shares × basis`.

**It is deliberately not part of the published site.** `holdings.html` and `holdings.json` both
went into `.gitignore` **before either file was created**, so neither can be committed by accident.
This repository is public and GitHub Pages serves it; a commit would publish position sizes and
cost basis to the world. Nothing about the page or its data is in this log beyond that.

The page's state lives in the browser's `localStorage`, not in the file. `holdings.json` is only
the seed it reads the first time. **Export** downloads a replacement for that file and **Reset to
file** throws the browser copy away — a browser cannot write to disk, and a write endpoint on a
local HTTP server was not worth the risk for this.

Two small design decisions worth keeping:

- **A blank price cell means "unchanged from cost", not zero.** Typing a price into one row of a
  new scenario and leaving the rest empty used to show every other position wiped out, which is a
  frightening and useless number. The fallback is the cost basis, so a half-filled scenario still
  totals to something honest.
- **The table rebuilds on `change`, not on `input`.** Redrawing every keystroke moved the caret
  out of the cell being typed in.

**`quotes.py` now serves the rest of the local site, not just the heatmap.** The live-price button
calls `api/quotes`, and every quote feed refuses a cross-origin call — which is the entire reason
that proxy exists — so the page has to be served from the same origin as it. Static files are
served from a **whitelist of extensions**, and each path is resolved and required to sit inside the
repo, so `../../.ssh/id_rsa` cannot walk out of it. Verified: `/../../../etc/passwd` and its
URL-encoded form both 404, as do `.gitignore` and `quotes.py`; `assets/site.css` and
`holdings.json` serve. The server still binds 127.0.0.1 only.

This is also the first time prices have worked anywhere in this repo since the Pages origin
started refusing every feed — `python3 quotes.py` then
`http://localhost:8090/holdings.html` priced all three positions on the first try.

**One thing to flag rather than fix.** The page does not reproduce the down-case total of the
spreadsheet it was modelled on. One position's value in that column was computed on a smaller
share count than the share count on its own row, which every other cell in the sheet uses. The
page derives every scenario from the single share count per position, so it cannot reproduce a
figure built on two. Whether the sheet's share count or its down case is the wrong one is the
owner's call, not this repo's. Figures withheld here on purpose: this log is published.

## 2026-10-29 — The earnings charts now refresh on a schedule

**Source**: Nasdaq earnings-surprise and analyst-forecast endpoints (Zacks consensus), via
`bin/epsfetch.py`.

The actual-vs-estimate dots were never on any schedule. `bin/morning-brief.sh` runs every weekday
at 6am and regenerated `brief.json` and nothing else, so the EPS charts only moved when the fetcher
was run by hand. That is why the four cards shipped earlier today all carried the note "the vendor
still shows Jun '26 as the most recent actual" — the vendor posts a quarter's actual a day or two
after the company reports, and by then nothing was looking.

Refetching proved the data had been sitting there: **30 of 70 cards had new figures**, a backlog
going back weeks. GOOG now carries its Sep '26 quarter — **$2.12 actual against $2.94 expected, a
28% miss** — where the chart previously stopped at June.

`bin/epsrefresh.py` is what the 6am job now calls, before the brief. It commits and pushes only
when something moved. Two things it does that `epsfetch.py --all` does not:

- **Redraws only the cards whose figures changed.** Re-rendering 70 charts a morning would churn
  70 files in git for nothing.
- **Keeps the previous `source` line when the numbers are unchanged.** Every spec records the date
  it was read, so a refetch rewrites all 70 specs daily even when not one figure moved. The read
  date is only interesting on a spec whose numbers it explains, so an unchanged spec keeps the date
  it already had and stays out of the diff.

**Two bugs found by looking at the output rather than the exit code.**

The first was a gap: comparing each spec only against this run's own snapshot meant a spec updated
by anything else — `epsfetch.py` by hand, the add-ticker skill — would leave a stale chart behind
permanently, with nothing to notice. A chart older than its spec is now redrawn too.

The second was caused by the fix, and took two goes to kill. `epsfetch.py` rewrites every spec it
touches, new read date and all, so by the time the mtime test ran, every spec was newer than its
chart and the first full run redrew **67 of 70** — exactly the churn the script exists to avoid.
Git showed it was wasteful rather than wrong: only 30 of those 67 charts differed by a byte.

Moving the mtime check to before the fetch did not fix it either, and the verification run that
was supposed to prove it was itself invalid — it had a `git stash` and `stash pop` immediately
before it, which rewrites every modified file with a fresh mtime in arbitrary order. That accident
found the real flaw: **`morning-brief.sh` runs `git pull` before the refresh**, and a pull resets
mtimes the same way, so on any morning the repo had moved the job would have redrawn all 70 charts
and committed them.

So staleness is **content, not time**. `epsdots.py` stamps a `specDigest` into each chart naming
the figures it was drawn from, and `epsrefresh.py` compares that. A pull, a checkout or a `touch`
cannot fake it, and because the digest ignores the read-date line it is immune to that churn by
construction — which let the before-the-fetch snapshot be deleted again. Verified by touching all
67 specs to the current time: 0 charts considered stale.

**The browser side was already correct** and needed nothing. `Sankey.load()` fetches with
`cache: "no-store"`, with a comment saying why: a regenerated chart keeps its filename, so a cached
copy would show last month's figures with no way to tell.

**An estimate with no actual meant two different things and drew identically.** A quarter can be
unreported, or reported with the vendor not yet having posted the figure — Zacks runs a day or
more behind a results release. The second case put an apparently untouched earnings chart beside
an income statement already showing that quarter's results, which reads as a broken page. Checked
at the source: Nasdaq's newest SNDK row is still **Jun 2026, reported 8/5/2026**, and its
earnings-date endpoint says Zacks has not supplied a date. The pipeline was right; the vendor is
behind.

So a pending quarter the company has already reported is now labelled **"reported / awaiting
vendor"** on the chart, with a hover that says the actual is withheld rather than guessed. The
test reuses `events.json`, which since this morning keeps a ticker's earnings date for ten days
after it passes: an earnings date later than anything the vendor has posted means the vendor is
behind. It flagged exactly the five names that reported on Oct 29 — AMZN, COIN, INTC, MSTR, SNDK —
and none of the five that reported on Oct 28, whose actuals the vendor already carries.

**The actual was deliberately not taken from the 8-K.** It is on the same card, in the income
statement. But the estimate dots are the street's adjusted EPS and the filing's figure is GAAP;
plotting one against the other is what commit a19008c forbids, and it would manufacture a large
beat or miss out of a basis mismatch. An empty column that explains itself is the honest answer.

**The refresh was also hiding its own failures.** It printed only the fetcher's summary line, so
a run reported "failed 3" without naming them — and the failure lines go to stderr, which exits
zero and was being dropped. A daily job that will not say which tickers failed is how this rotted
in the first place. They are now printed. The three are permanent and legitimate: Nintendo (7974)
is a Japanese listing absent from Nasdaq's US endpoints, ARQQ has no earnings-surprise record, and
XNDU has no reported quarters yet.

**Noticed, not fixed.** 25 cards carry a reported surprise above 100% in absolute terms, and MSTR
has one at 7,754%. Most are arithmetic rather than error — a loss-maker whose consensus is near
zero produces an explosive percentage from a one-cent miss — but it is not a figure worth printing,
and whether to suppress it below some consensus floor is a decision rather than a bug fix. The dots
themselves show both numbers and remain honest.

## 2026-10-30 — LLY and HOOD added to the site

Added **Eli Lilly (LLY)** and **Robinhood Markets (HOOD)** to the watchlist and the Financials tab.
Neither is a favorite, so neither enters the Catalysts sweep or the Morning Brief. Cards:
[[eli-lilly-q3-fy26]] and [[robinhood-q3-fy26]]. The tab now carries 72 statements.

**A new sector.** Nothing in the ranked `SECTORS` list covered a drug manufacturer, so `Pharma` was
added at rank 30, between `Homebuilder` and the fund block. That list exists twice — `assets/site.js`
and inline in `heatmap.html` — and both copies were edited; they are verified identical, 37 entries
each. HOOD is tagged `Fintech` only: tagging it `Crypto` as well would have been true but would have
labelled the tile "Crypto", because Crypto outranks Fintech.

**The vendor moved Lilly's IPR&D charge below the operating line.** stockanalysis reports $13,092M of
operating income for Lilly's Q3 FY26; the 8-K reports $8,608M. The $4,484M difference is the $4,181M
acquired IPR&D charge plus a $303M impairment, which Lilly includes in operating income and the
vendor does not. A card built on the vendor's figure would have shown a 54% operating margin for a
quarter the company reports at 35%. The card follows the filing. This is the Meta trap again, and it
is now the second recorded instance, which suggests checking the operating line against the filing
whenever a quarter carries a large one-off charge.

**Robinhood files no gross profit line.** Its statement runs net revenues, then operating expenses,
then operating income. The card uses brokerage and transaction expense ($68M) as the cost line — the
convention [[coinbase-q3-fy26]] already uses — which means the 95% gross margin on that card is a
construction of the chart rather than a reported figure. The card says so.

**One debt chart was generated and thrown away.** `bin/debtfetch.py` produced a Robinhood chart
showing $22.6B of debt against $685M of quarterly operating profit. $19,480M of that is *securities
loaned* — collateralised stock lending, matched by securities borrowed and user assets on the other
side — which the vendor's balance sheet maps into short-term debt. Robinhood's actual long-term
borrowings are $2,660M. The chart was deleted and the card says why. COIN, NU and V show no such
distortion, so this is specific to a broker running a large lending book. Lilly's debt chart was
skipped by the fetcher itself: no cash and equivalents figure for the Sep 30, 2026 column.

**Two rendering defects, both caught by looking at the PNG rather than the validator.** The validator
passed clean on a first draft of both charts in which the largest revenue segment had no label at
all — Lilly's Cardiometabolic Health at 81% of revenue, Robinhood's Transaction-based at 61%. Long
`note` strings pushed the whole annotation block off the left edge of the canvas and plotly dropped
it silently. Shortening the notes fixed it. Separately, splitting Robinhood's operating expenses into
the 10-Q's five lines made the right-hand labels collide; they are drawn as three.

**Not done.** Neither ticker has an ownership donut — that needs a ~400MB Form 13F data set pulled
and deleted, and it was not pulled in this pass. Neither was added to `ibkr-conids.json`: the IBKR
connector is not present in the session at all, so no contract id could be resolved, and a conid is
not something to guess. Both are gaps to close, not figures to fill in.
