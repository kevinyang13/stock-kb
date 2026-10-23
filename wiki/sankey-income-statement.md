# Sankey Income Statement

**Summary**: How to produce an App-Economy-Insights-style Sankey income statement chart for any stock symbol, from gathering the quarterly figures through rendering and verifying the image.

**Sources**: Three reference infographics supplied by the user (SpaceX Q3 FY26, TSMC Q3 FY26, Alphabet Q1 FY26, all by App Economy Insights). Rendering details verified by building and running `bin/sankey.py` against the TSMC reference.

**Last updated**: 2026-10-22

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

## Step 2 — write the spec

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

A full worked example is in `examples/tsm-q3-fy26.json`.

## Step 3 — render

```bash
python3 bin/sankey.py examples/tsm-q3-fy26.json --png
```

Writes `out/{TICKER}-{PERIOD}.html` and, with `--png`, a 2× PNG beside it. Drop `--png` and open the HTML if you want the interactive hover values.

## Step 4 — verify before publishing

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

**Labels** are drawn as annotations rather than Plotly node labels, because each one needs three lines at two sizes: a bold name, the dollar value, then margin or share and Y/Y in small grey. Plotly's built-in node labels cannot do this.

**Extras** in the references that this script does not generate: company logos beside segment names, and the rounded black KPI chips in the lower right (Starlink subscribers, launch count). Add those in an image editor, or extend the script with `layout.images` and `shapes`.

## Loss-making quarters

A profitable statement conserves as revenue → profit + costs. A loss does not: costs exceed revenue, so the shortfall has to come from somewhere. Put `net_loss` in the spec (plus a `below_line` list for interest and tax) and the script switches to a layout where the net loss is drawn as a red source feeding the expense pool — which is what a loss literally is, spending funded by capital rather than sales.

The identity it checks is:

```
gross profit + net loss == operating expenses + below-the-line charges
```

`examples/crwv-q2-fy26.json` is a worked example: CoreWeave's $1,696M gross profit plus a $626M net loss funds $2,322M of charges, and it balances exactly. Note that CoreWeave's own "total operating expenses" line includes cost of revenue — read the statement's own subtotals before assuming a layout.

Use `"unit": "M"` with `"decimals": 0` for companies where billions would round the interesting numbers away. CoreWeave's $49M operating loss disappears entirely at one decimal place in billions.

## Known limitations of `bin/sankey.py`

- `arrangement="fixed"` is required. With `"snap"`, Plotly overrides the `y` positions and the profit and cost branches swap sides.
- Node `y` is top-down inside the sankey domain; annotation `y` is bottom-up across the whole canvas. The `py()` helper converts between them. Mixing the two silently puts labels in the wrong place.
- The diagram is confined to the lower 86% of the canvas (`DOM_TOP`) so stage labels have somewhere to sit.
- A tax *benefit* rather than a tax expense is still not handled. The SpaceX reference shows one flowing into net profit, which needs the link reversed.
- Segment label text extends into the left margin. Very long names need `margin.l` raised past 300.

## Related pages

- [[income-statement-basics]]
- [[watchlist-heatmap]]
- [[data-sources]]
