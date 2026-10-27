# Sankey Income Statement

**Summary**: How to produce an App-Economy-Insights-style Sankey income statement chart for any stock symbol, from gathering the quarterly figures through rendering and verifying the image.

**Sources**: Three reference infographics supplied by the user (SpaceX Q3 FY26, TSMC Q3 FY26, Alphabet Q1 FY26, all by App Economy Insights). Rendering details verified by building and running `bin/sankey.py` against the TSMC reference.

**Last updated**: 2026-10-23

---

## What this chart is

A left-to-right Sankey diagram of one quarter's income statement. Revenue segments flow into a single revenue trunk, which splits into profit (green, flowing right) and cost (red, flowing down and right). Each node carries its dollar value, a margin or share-of-revenue figure, and a year-over-year change.

The format is readable because it keeps one rule: **every flow conserves value**. Width is proportional to dollars, so the eye reads the cost structure without reading any number.

## Prerequisites

```bash
pip install plotly "kaleido==0.2.1"
```

The kaleido version matters. Plotly 5.x cannot drive kaleido 1.x — `fig.write_image()` raises `ValueError` and tells you to install the package you already installed. Pin `0.2.1` (source: verified in this repo, 2026-10-22).

## Step 1 — gather the numbers

You need one quarter of figures for the symbol. Good sources, in order of reliability:

1. **The company's own press release or 10-Q.** Authoritative, and the segment names match what the company actually reports.
2. **stockanalysis.com/stocks/{ticker}/financials/** — a usable quarterly income statement, same source the rest of this repo scrapes.
3. **The IBKR connector** — useful for price and company structure, but note it exposes **no income-statement tool**. Do not plan on it for this chart.

Collect:

- Revenue by segment, and each segment's Y/Y change
- Total revenue and its Y/Y change
- Cost of revenue, gross profit
- Operating expense total and its components (R&D, S&M, G&A, or SG&A)
- Operating profit
- Interest and other income, tax, net profit

Segments are the part that varies most by company. Alphabet reports Search / YouTube / Network / Play / Cloud; TSMC reports by platform (HPC, Smartphones, IoT, Automotive); SpaceX in the reference is split Space / Connectivity / Super Intelligence. Use whatever the company actually discloses rather than forcing a house taxonomy.

## Step 2 — break revenue out by segment — required

**Every chart must split total revenue into the company's reported segments.** A single "Total
revenue" bar is a fallback for companies that publish no split, not a default.

1. Find the segment table in the company's **own** quarterly release. Search
   `"<Company> <quarter> results segment revenue"` and prefer the 8-K or IR page.
2. **Validate before using it.** The segments must sum to revenue within about 0.5%. If they do
   not, you have the wrong period or the wrong line items. `bin/mkspec.py` checks this and warns.
3. If the company genuinely publishes no split, pass `no_segment_split=True` and say so plainly on
   the card: *"No segment split: the release does not break revenue out."* Never let a missing
   fetch look like a missing disclosure.
4. Never invent segment names or values.

**Do not use `stockanalysis.com/stocks/<ticker>/metrics/revenue-by-segment/`.** Its figures are
annual even with `?p=quarterly`. NVDA's two segments there sum to $303B against $96.2B of quarterly
revenue — the error is large and silent.

Segments that have been verified against revenue, as examples of the shapes you will meet: Micron
by business unit, Alphabet's six lines, Qualcomm's QCT sub-streams plus QTL and a residual, SanDisk
by end market, TSMC as rounded platform percentages applied to revenue, Nintendo's two.

## Step 3 — write the spec

Create a JSON file. All money values are **positive**, including costs — the renderer decides direction and colour.

| Field | Type | Notes |
|---|---|---|
| `company`, `ticker`, `period` | string | `period` becomes part of the title and filename |
| `currency`, `unit` | string | Default `$` and `B` |
| `revenue`, `revenue_yoy` | number | `revenue_yoy` in percent |
| `segments[]` | list | `name`, `value`, optional `yoy`, `note`, `color` |
| `cost_of_revenue`, `gross_profit` | number | |
| `opex_total`, `opex_items[]` | number, list | Items are `name` + `value` |
| `operating_profit` | number | |
| `other`, `tax`, `net_profit` | number | `other` is interest and other income |
| `width`, `height` | number | Optional; default 1500 × 880 |

A full worked example is in `examples/tsm-q3-fy26.json`. `bin/mkspec.py` will build the spec for you from a row of figures and pick the profit or loss layout automatically.

## Step 4 — render

```bash
python3 bin/sankey.py examples/tsm-q3-fy26.json --png
```

Writes `out/{TICKER}-{PERIOD}.html` and, with `--png`, a 2× PNG beside it. Drop `--png` and open the HTML if you want the interactive hover values.

## Step 5 — verify before publishing

The script prints a warning to stderr for every identity that does not foot:

```
! net profit = operating - tax + other: 23.90 vs 23.60 (drift +0.30)
```

It checks five identities: segments sum to revenue, gross = revenue − cost, operating = gross − opex, net = operating − tax + other, and opex items sum to the opex total. Tolerance is 0.15 in whatever unit you are using.

**Drift is normal and is not automatically a bug.** Published figures are rounded to one decimal, and companies park real items outside the line items you charted — equity-method income, minority interest, currency effects. The TSMC reference itself does not foot: its own numbers give $23.6B where it prints $23.9B. Decide whether the gap is rounding or a line item you have missed, and say which in the caption if it matters.

Then look at the picture and check:

- No label is clipped at the left or right edge — widen `margin` if a long segment name is cut
- No stage label sits on top of its own bar
- Flow widths look proportional; a segment that is 2% of revenue should be a hairline
- Green only ever flows rightward into profit; red only ever branches away into cost

## Design conventions

Read off the three reference images:

**Columns**, left to right: revenue segments → revenue trunk → gross profit / cost of revenue → operating profit / operating expenses → net profit / tax / opex components.

**Palette** (approximated from the references by eye, not sampled):

| Role | Colour |
|---|---|
| Title navy | `#17496b` |
| Profit node | `#1a9641` |
| Profit link | `rgba(166,217,166,0.80)` |
| Cost node | `#c81e1e` |
| Cost link | `rgba(240,160,152,0.80)` |
| Revenue / segment node | `#111111` |
| Segment link | `rgba(140,140,140,0.65)` |
| Background | `#f2f2f2` |

Segment nodes in the TSMC reference are individually coloured; in the SpaceX reference they are all black. Either reads fine.

**Labels** are drawn as annotations rather than Plotly node labels, because each one needs three lines at three sizes. Plotly's built-in node labels cannot do this.

| Line | Size | Colour |
|---|---|---|
| Node name | 15px bold | the node's own colour |
| Money figure | **19px bold** | the node's own colour |
| Margin, share, Y/Y | 12px | `#555` grey |

The money figure is the line the eye goes to, so it is the largest thing in the label and it
carries the colour: green reads as profit, red as cost, black as revenue, before any number is
read. Costs are written in parentheses — `($7.2B)` — not with a minus sign.

Keep the sub-lines to two. The money figure plus one ratio fits beside a bar; a third line grows
the block until it collides with whatever is below it. The loss layout used to carry a "funds the
gap" third line on the net-loss node and it overlapped the cost-of-revenue bar once the money line
went to 19px.

**Extras** in the references that this script does not generate: company logos beside segment names, and the rounded black KPI chips in the lower right (Starlink subscribers, launch count). Add those in an image editor, or extend the script with `layout.images` and `shapes`.

## Loss-making quarters

A profitable statement conserves as revenue → profit + costs. A loss does not: costs exceed revenue, so the shortfall has to come from somewhere. Put `net_loss` in the spec (plus a `below_line` list for interest and tax) and the script switches to a layout where the net loss is drawn as a red source feeding the expense pool — which is what a loss literally is, spending funded by capital rather than sales.

The identity it checks is:

```
gross profit + net loss == operating expenses + below-the-line charges
```

`examples/crwv-q2-fy26.json` is a worked example: CoreWeave's $1,696M gross profit plus a $626M net loss funds $2,322M of charges, and it balances exactly. Note that CoreWeave's own "total operating expenses" line includes cost of revenue — read the statement's own subtotals before assuming a layout.

Use `"unit": "M"` with `"decimals": 0` for companies where billions would round the interesting numbers away. CoreWeave's $49M operating loss disappears entirely at one decimal place in billions.

## Avoiding overlap

Three failure modes produce a chart that is technically correct and visually unreadable. All three
have happened.

**Crossing bands.** Plotly stacks the links into a node in *declaration order*, not by the vertical
position of their sources. If three sources feed one pool, declare their links in the same
top-to-bottom order as their `y` values. A mismatch makes the bands cross over each other, which
reads as though value is flowing backwards.

**Nodes parked in a corridor.** A node placed at an `x` between two columns that are linked to each
other will sit underneath that band. The loss layout originally put the net-loss and non-operating
income nodes at `x=0.37`, directly in the path of the revenue → cost-of-revenue link. Either put
such a node in an existing column, or give it a column of its own that nothing traverses.

**Labels on their own bar.** A node whose value is a large share of its column is drawn tall, and a
label centred on it lands inside it. Options, in order of preference: anchor the label to the left
of the column (`xa="right"`), give a pure-sink node its own column so there is space beneath it, or
pin the label to a fixed `y` clear of the diagram. Stage headers live above the diagram entirely —
that is what `DOM_TOP` is for.

**Check the picture, every time.** The validator proves the numbers conserve. It says nothing about
whether the chart can be read. Open the PNG before publishing and confirm: no band crosses another,
no label touches a bar, no text is clipped at an edge.

## Precision

Pick the unit from the size of the statement, and keep one decimal where it matters:

| Revenue | Unit |
|---|---|
| ≥ 20,000M | billions, 1dp |
| 1,000–20,000M | millions, 0dp |
| < 1,000M | millions, **1dp** |

A $13.5M company rounded to `$14M` showed a 14% gross margin where the real figure was 16%. For
small caps the decimal is the difference between a right answer and a wrong one.

## Rendering live in the browser

The chart is a Plotly figure either way; the PNG is just that figure flattened by kaleido at the
last step. `--json` skips the flattening and writes the figure itself to `charts/{TICKER}-{PERIOD}.json`,
which the Financials page renders with plotly.js.

```bash
python3 bin/sankey.py examples/nvda-q2-fy27.json --json --png
```

Measured on NVDA Q2 FY27: **12KB of JSON against a 395KB PNG**, about 90ms to render. Across all 65
statements that is 888KB instead of 22MB, and the page fetches one at a time.

What the live path gains: **hover gives every band and bar its exact value**, in the statement's own
currency and precision. That matters because the labels are deliberately sparse — two sub-lines
maximum, and hairline flows carry no label at all.

Three things make it work:

1. **Python keeps the layout.** `assets/sankey.js` does not compute positions. It takes the figure
   as built and rescales it, because every margin and font size in that JSON is a pixel value
   against a fixed design width. `--json` pops `width`/`height` into a `design` block for exactly
   this. A plain `responsive: true` would keep the 300px left and 270px right margins on an 800px
   page and squeeze five columns into the 230px left over.
2. **Node names ride in `customdata`, not `node.label`.** A populated `label` makes plotly draw node
   text, which leaves a visible glyph beside every bar — a transparent `textfont` does not suppress
   it. The label stays empty and the annotations do all the drawing.
3. **Below a 0.42 scale the chart stops shrinking and pans instead.** Squeezing a five-column
   diagram into 390px gives roughly 7px text. It fits and cannot be read. Horizontal scroll is the
   honest answer until there is a stacked layout for narrow screens.

The PNG is still generated, and the page falls back to it if the JSON or plotly itself fails to
arrive. Keep both.

### Zoom

A plotly sankey is not a cartesian plot, so it has **no native zoom** — `scrollZoom` and `dragmode`
do nothing. Zoom is therefore a re-render at a larger scale: `draw(div, fig, zoom)` passes
`container width x zoom` into the same scaling path, and whatever no longer fits is panned. A CSS
transform would have been less code and would have blurred the type; re-laying out keeps the text
sharp and the hover hit-boxes true.

Controls on the Financials page: a `− / Fit / +` pill stepping through
0.5, 0.75, 1, 1.5, 2, 2.5, 3; ⌘/ctrl + scroll (which is also what a trackpad pinch sends);
drag to pan; double-click to refit. Zooming keeps whatever is at the anchor point — the cursor, or
the middle of the view — under the same point afterwards.

Four traps, all of which bit:

1. **`Plotly.react` corrupts a resized sankey.** It moves the node rectangles but leaves the link
   paths on their old geometry, so every band disappears or lands in the wrong place. Use
   `Plotly.newPlot`. At this size it still redraws in well under 500ms.
2. **A flex child shrinks.** `.fin-fig` is a flex row, so the zoomed chart was squeezed straight
   back to the container width. `.fin-chart` needs `flex: 0 0 auto`.
3. **A flex child stretches.** `align-items` defaults to `stretch`, so once the box had a capped
   height the chart was squashed vertically to match it. `.fin-fig` needs `align-items: flex-start`.
4. **The page grows instead of the box.** Without a cap, a 3x chart makes the page three times
   taller and the zoom controls scroll away from the chart. The box takes `max-height: 78vh` while
   panning and becomes a window.

A press that never travels more than 4px stays a click, so hover still works while drag-to-pan is
armed.

### Cache-stamping the assets

The pages carry no-cache meta tags, but those cover only the HTML. A browser will still serve
`assets/site.css` and `assets/site.js` from its own cache, so a style change can sit invisible
behind a stale copy — this has now cost two debugging sessions. After editing anything under
`assets/`, run:

```bash
python3 bin/stamp.py
```

It rewrites every page's asset links to `?v=<newest asset mtime>`, which makes each edit a new URL.

## Known limitations of `bin/sankey.py`

- `arrangement="fixed"` is required. With `"snap"`, Plotly overrides the `y` positions and the profit and cost branches swap sides.
- Node `y` is top-down inside the sankey domain; annotation `y` is bottom-up across the whole canvas. The `py()` helper converts between them. Mixing the two silently puts labels in the wrong place.
- The diagram is confined to the lower 86% of the canvas (`DOM_TOP`) so stage labels have somewhere to sit.
- A tax *benefit* is handled: a negative `tax` draws a green Tax benefit node flowing into net profit rather than a charge out of operating profit. SPCX Q3 FY26 is the worked example.
- Segment label text extends into the left margin. Very long names need `margin.l` raised past 300.
- Negative gross profit cannot be drawn at all — revenue does not cover cost of revenue, so there is
  no flow. SPCE, QUBT and CAN are excluded for this reason.

## Related automation

`.claude/skills/income-statement-chart/SKILL.md` encodes this whole procedure, including the
chartable/not-chartable gate and the source traps, so a bare ticker is enough to trigger it.

## What the hover says

Every node and every band carries a hover block, built by `node_tips()` and `link_tips()` in
`bin/sankey.py` from the spec alone.

A node gives its amount, its share of revenue, and — for anything gross profit pays for — its
share of gross profit. That last line is offered only to nodes **reachable from the gross profit
node** in the link graph: cost of revenue sits above gross profit, so "% of gross profit" there
would be nonsense.

Two nodes on every chart are computed rather than filed, and the hover now says so:

| Node | Derivation |
|---|---|
| Cost of revenue | revenue less reported gross profit |
| Operating expenses | gross profit less operating profit |
| Interest & other (, net) | net profit plus tax, less operating profit |
| Non-operating & tax, net | charges less operating expenses |

A band says what share of its source it carries — `Revenue → Cost of revenue · 23% of Revenue` —
so the widths read as proportions. A node with only one outgoing band always carries 100% of
itself, so that case is suppressed.

Blocks use `&#160;` padding and a monospace `hoverlabel` font, exactly as the debt chart does, and
literal characters rather than HTML entities: plotly does not decode entities in hover text.

**Year over year comes from `bin/yoyfetch.py`**, which writes a `prior` block into each spec
keyed by the node name the chart draws, read from the same stockanalysis data endpoint.

Five charts were built from filings rather than the aggregator, and on those the two sources
disagree about where some costs sit, so a growth figure from the wrong basis would contradict the
bar it is attached to. Rather than maintaining a list of exceptions, **each line polices itself**:
the year-ago figure is kept only when the source's *current* quarter for that line matches what
the chart already draws, within 1%. Where it does not, the node simply gets no growth row.

That rule caught every known disagreement without being told about any of them — NBIS's R&D, SG&A
and operating expenses (the share-based compensation reclassification), and Meta's operating
expenses and operating income (the $9,890M charge). It also catches cases nobody had noticed, such
as NVDA's SG&A.

A second rule drops a line whose **sign changed**: NBIS's "Net loss" node was a $584.4M net
*profit* a year earlier, on the Yandex disposal, and a percentage across that flip is meaningless.

Across the 66 charts, 443 nodes carry a year-ago figure. Nintendo gets none: its chart is in USD
from the ADR, the Tokyo listing's data is in yen, and the ADR publishes no income statement at that
endpoint — so the basis check refuses all of it, correctly.

**Trap: two specs can write the same chart.** `bin/sankey.py` names its output from the spec's own
`ticker` and `period`, not from the filename, so `examples/tsm-q3-fy26.json` and
`examples/tsm-q3-fy26-filed.json` both wrote `charts/TSM-Q3-FY26.json`. A loop over
`examples/*.json` rendered whichever sorted last — the superseded USD one — and silently replaced
the published NT$ chart. Superseded specs now live in `examples/superseded/`, which the loops do
not touch.

## A second chart on the same pipeline

`bin/debtbars.py` emits the debt/coverage bars that sit under the Sankey on the NBIS and CRWV
cards — debt, free cash flow and cash for the quarter the card covers, in the style of the
App-Economy-Insights "Debt level and coverage" panel. It writes the same figure JSON with
`--json`, carrying the same `design` width and height, so `assets/sankey.js` renders it unchanged.

Two things that had to be added for it:

- `scaled()` now also scales `xaxis`/`yaxis` tick fonts, the legend font and trace `textfont`.
  A sankey has none of those, so the additions are guarded and change nothing for the Sankey.
- The chart type is opt-in per statement: a `"debt"` key in the `financials.json` item naming the
  chart stem. Without it the card renders exactly as before.

**Trap**: kaleido fails the entire PNG render with a bare `plotly.js error` (code 525) if the
layout **title** contains an HTML entity such as `&middot;`. The same entity is fine in a trace
name or a hovertemplate. Keep titles plain.

Free cash flow is usually negative for these names, so the chart has a zero line and bars below it.
Bar labels switch to millions below $1bn, because a $49.5M bar labelled `$0.0B` says nothing.

**Every statement carries one.** `bin/debtfetch.py` builds the specs in bulk: for each item in
`financials.json` it reads the quarterly balance sheet and cash flow statement from
stockanalysis.com's SvelteKit data endpoint and takes the column whose period end matches the one
the card already shows, so the bars and the income statement always describe the same quarter.

```bash
python3 bin/debtfetch.py              # anything without a spec yet
python3 bin/debtfetch.py --all        # refetch everything
python3 bin/debtfetch.py NBIS CRWV    # just these
```

The endpoint is `/<path>/financials/<statement>/__data.json?p=quarterly`, which returns SvelteKit's
flattened payload — a `data` array where every integer is an index back into the same array, so it
has to be hydrated before use. The three fields are `debt`, `cashneq` and `fcf`; where `fcf` is
missing it is derived as `ncfo + capex` (capex is already signed negative).

Nothing is guessed. A ticker whose column cannot be matched within 7 days, or whose lines are
missing, is reported and skipped. A null total debt is only read as zero when every debt component
is also null — a missing total with components present is a gap, not a debt-free balance sheet.

**Each bar carries its own breakdown as a tooltip**, so the figure can be checked without opening
a filing: the debt bar lists current portion, long-term and leases; the free cash flow bar shows
operating cash flow less capital expenditure footing to the total; the cash bar names what is
*not* in it, such as short-term investments and restricted cash. `bin/debtfetch.py` captures the
component lines, and anything the components do not account for is shown as `Other` rather than
quietly dropped.

The blocks are column-aligned with `&#160;` and a monospace `hoverlabel` font, because plotly
collapses runs of ordinary spaces in hover text.

**Trap, and the opposite of the title trap above**: plotly decodes HTML entities in a legend name
but **not** in hover text, where `&middot;` renders literally as "&middot;". Hover text uses
literal characters instead. So: no entities in a layout title (kaleido dies), entities fine in a
legend name, literal characters in hover text.

**Currency comes from the card's own KPI values**, not from the sankey spec. Reading it from the
spec picked up a stale USD file for TSM, which has both a NT$ spec and a superseded USD one. The
chart picks its axis unit from the largest bar — M, B or T — so TSMC reads in NT$ trillions and
Arqit in single-digit millions, while each bar label still steps down to whatever unit keeps it
meaningful.

**The two charts share one row.** `.fin-row` is a flex row: the sankey takes `flex:1 1 620px`, the
debt bars `flex:0 1 330px`. Below roughly 950px of card width the row wraps and the two stack, so
narrow screens are unaffected. The debt chart's design width of 330px is deliberately close to the
column it lands in, which is why its font sizes are the sizes it actually renders at — a design
much wider than its column would scale every label down.

**Trap**: plotly draws its own `<g class="legend">` inside the chart SVG, and `assets/site.css` had
an unscoped `.legend` rule for the Events calendar carrying `text-transform:uppercase`. It reached
into the chart and uppercased every legend label on the Financials page, while the PNG from kaleido
looked correct — the collision only exists in the browser. The rule is now scoped to
`#ev-body .legend`. Worth checking any other generic class name against what plotly emits.

## Related pages

- [[income-statement-basics]]
- [[watchlist-heatmap]]
- [[data-sources]]
