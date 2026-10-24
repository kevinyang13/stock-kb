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
