---
name: income-statement-chart
description: >
  Build an income statement Sankey chart for a stock symbol and publish it to the Financials page
  of Stock Signal Desk. Covers sourcing the quarterly figures, the mandatory revenue-by-segment
  breakdown, rendering with bin/sankey.py, validation, and adding the entry to financials.json.

  Use whenever a ticker is given with intent to chart or add its financials: "add NVDA", "generate
  the financial for CRWV", "do the income statement for Nintendo", "chart META", "add this to the
  Financials tab".
---

# Income Statement Chart

Produces one Sankey per company-quarter for the Financials page. Repo: `~/dev/stock-kb`.

## Step 0 — Is this chartable?

Do not chart, and say why:

| Case | Test | Example |
|---|---|---|
| ETF or fund | holds securities, files no income statement | SMH, SPY, IBIT |
| Shell / no filing | no usable statement published | CLBR, CCXI, BITF |
| Negative gross profit | cost of revenue exceeds revenue | SPCE, QUBT, CAN |
| Pre-revenue | no revenue line at all | HQ |
| Private company | no filings exist | Anthropic, OpenAI |

A private company has no audited statement. Reported run-rate and valuation are **not** an income
statement — do not build a chart that would sit next to filed ones looking equally authoritative.

## Step 1 — Core P&L

```
https://stockanalysis.com/stocks/<ticker>/financials/income-statement/?p=quarterly
```

That path carries the full line-by-line statement. The `/financials/` overview page has only
headline rows — do not use it.

Pull: quarter label, period end, revenue, revenue YoY %, gross profit, R&D, SG&A, total operating
expenses, operating income, pretax income, income tax, net income.

Prefer the company's own 8-K or results release when available; it has beaten the aggregator before
(see Traps).

## Step 2 — Revenue by segment — REQUIRED

**Every chart must break total revenue into reported segments.** A single "Total revenue" bar is a
fallback, not a default, and is only acceptable when the company genuinely publishes no split.

1. Search for the segment table in the company's own quarterly release, e.g.
   `"<Company> <quarter> results segment revenue"`.
2. **Validate before use**: the segments must sum to revenue within ~0.5%. If they do not, you have
   the wrong period or the wrong line items.
3. If the company publishes no split, say so explicitly on the card:
   `"No segment split: <company> does not break revenue out in its release."`
   Never imply a split was unavailable when it was simply not fetched.
4. Never invent segment names or values.

**Do not use** `stockanalysis.com/stocks/<t>/metrics/revenue-by-segment/`. Its figures are annual
even with `?p=quarterly` — NVDA's two segments there sum to $303B against $96.2B of quarterly
revenue.

## Step 3 — Build the spec

`bin/mkspec.py` takes a row of figures and emits a spec, choosing the profit or loss layout:

```bash
python3 bin/mkspec.py /tmp/rows.json
```

Pass `segments` as a list of `{"name", "value", "yoy", "note"}`. It **warns if segments are
missing**. Schema and field reference: `wiki/sankey-income-statement.md`.

Two lines are always derived so the statement foots:
- cost of revenue = revenue − reported gross profit
- non-operating ("other") = net + tax − operating

## Step 4 — Render and validate

```bash
python3 bin/sankey.py examples/<ticker>-<period>.json --json --png
```

`--json` writes the live figure the Financials page renders; `--png` writes the raster fallback.
Always produce both.

**The validator must print no warnings.** It checks five identities. A warning means the figures are
wrong or a line is missing — fix the data, never widen the tolerance.

**Then look at the image.** The validator proves the numbers conserve; it says nothing about
readability. Confirm all four:

- no band crosses another
- no label sits on a bar
- no text is clipped at an edge
- flow widths look proportional
- every money figure reads at 19px in its node's colour — green profit, red cost, black revenue
- the live chart renders on the Financials page and its hover values are right

Labels carry at most two sub-lines: the money figure, then one ratio. A third line grows the block
until it hits whatever sits below it.

If bands cross, the links into a shared node were declared in a different order from their vertical
positions — plotly stacks by declaration order. If a band runs through a node, that node is parked
in a corridor between two linked columns; move it into a column or give it one of its own.

## Step 5 — Publish

Copy the PNG to `assets/financials/`. `charts/{TICKER}-{PERIOD}.json` is written in place and needs
no copying — the page fetches it from there. Add an entry to `financials.json` with ticker, company,
period, periodEnd, img, source, sourceUrl, four highlight KPIs and notes. Notes must state the
segment split, anything derived, and any non-USD currency.

If you changed anything under `assets/`, run `python3 bin/stamp.py` — the pages' no-cache meta tags
cover only the HTML, and a stale cached stylesheet will hide your change completely.

Verify in the browser (`python3 -m http.server 8099`, then `financials.html`) — the chip appears,
the live chart draws, hover values are right, no horizontal overflow. Then update `wiki/log.md` and
commit.

## Traps

- **Sources disagree with themselves.** Reported cost of revenue often does not reconcile with
  reported gross profit (GE off by $1,020M, IBM by $114M). Trust the subtotals, derive the bridge.
- **Aggregators disagree with filings.** stockanalysis gave Meta Q3 FY26 operating income of
  $22,878M against the 8-K's $12,988M, because it puts a $9,890M charge below the line. Follow the
  filing.
- **Tax can be a benefit** (negative), which flows *into* net profit — SPCX.
- **Other income can be negative** (net interest expense), a charge off operating profit — INTU, SMCI.
- **Loss makers with non-operating income** need the `other_income` source or the loss layout cannot
  balance — MSTR.
- **Non-USD filings** stay in the filed currency unless asked to convert. If converting, record the
  rate, its date and two independent sources, and keep the filed figures in the notes — Nintendo.
- **Precision on small caps.** Under $1bn of revenue, use millions at one decimal. `$13.5M` rounded
  to `$14M` turned a 16% gross margin into 14%.
- **Alphabet-style distortions**: a one-off investment gain can push net margin far above operating
  margin. Say so on the card rather than letting the KPI stand alone.
