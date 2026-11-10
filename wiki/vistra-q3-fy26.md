# Vistra Q3 FY26

**Summary**: Vistra's third quarter 2026 (quarter ended September 30, 2026): $6,347M of revenue, up 28% year over year, $1,706M of operating income and $1,140M of net income. The data vendor reports $1,975M of operating income because it leaves a $269M impairment out of operating expenses entirely. This is the first VST card on the Financials tab.

**Sources**: Vistra 10-Q for the quarter ended September 30, 2026, filed November 9, 2026 (source: sec.gov, accession 0001692819-26-000025) — condensed consolidated statements of operations (R2), disaggregation of revenue note (R46) and segment note (R94). Market figures from stockanalysis.com, November 9, 2026.

**Last updated**: 2026-11-09

---

## Income statement

Three months ended September 30, in millions of US dollars.

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| **Operating revenues** | **6,347** | **4,971** | **+27.7%** |
| Fuel, purchased power costs, and delivery fees | (2,530) | (2,370) | +7% |
| Operating costs | (683) | (655) | +4% |
| Depreciation and amortisation | (711) | (460) | **+55%** |
| Selling, general, and administrative | (448) | (444) | +1% |
| **Impairment of long-lived assets** | **(269)** | (5) | n/m |
| **Operating income** | **1,706** | **1,037** | **+65%** |
| Other income, net | 44 | 105 | −58% |
| Interest expense and related charges | (254) | (286) | −11% |
| **Net income before income taxes** | **1,496** | **856** | +75% |
| Income tax expense | (356) | (204) | +75% |
| **Net income attributable to Vistra** | **1,140** | **652** | **+75%** |
| Cumulative dividends on preferred stock | (48) | (48) | — |
| **Net income attributable to common stock** | **1,092** | **604** | +81% |

Diluted earnings per share **$3.23** on 337,852,657 shares.

## This card follows the filing, not the aggregator

stockanalysis reports **$1,975M** of operating income for this quarter. The 10-Q reports
**$1,706M**.

The difference is exactly **$269M** — the impairment of long-lived assets, which the vendor
leaves out of operating expenses altogether. Its total operating expenses of $4,372M are the
filed $4,641M less the impairment.

| | filed | as the vendor has it |
|---|---|---|
| Operating income | **$1,706M** | $1,975M |
| Operating margin | **27%** | 31% |

This is the same failure mode as [[cloudflare-q3-fy26]], where an $11.0M restructuring charge was
moved below the line, and as the Meta case recorded in [[sankey-income-statement]], where a
$9,890M charge produced $22,878M of vendor operating income against the 8-K's $12,988M. The
chart here draws the impairment as its own band so the charge is visible rather than netted
away.

[[constellation-energy-q3-fy26]], filed the same day, has a smaller version of the same problem.

## No gross profit line, so the chart builds one

| | |
|---|---|
| Revenue | $6,347M |
| Cost of revenue (fuel, purchased power, delivery fees) | $2,530M |
| **Gross profit (derived)** | **$3,817M — 60%** |

Utilities do not report gross profit and Vistra does not. That 60% is a construction of this
card and **is not comparable with the other cards on the Financials tab**. The same caveat
applies to [[constellation-energy-q3-fy26]].

## Revenue by type

| Type | Q3 FY26 | Q3 FY25 | Y/Y | Share |
|---|---|---|---|---|
| Retail energy charge — ERCOT | $3,007M | $2,698M | +11% | 47% |
| Retail energy charge — Northeast/Midwest | $1,331M | $1,054M | +26% | 21% |
| Wholesale generation revenue from ISO/RTO | $1,226M | $683M | **+79%** | 19% |
| Capacity and other wholesale contracts | $428M | $343M | +25% | 7% |
| Hedging and PTC revenues, net | $355M | $193M | +84% | 6% |
| **Total** | **$6,347M** | **$4,971M** | **+28%** | 100% |

The first four lines are the 10-Q's revenue-from-contracts disaggregation, which sums to
$5,992M, and the fifth is its "total other revenues" line of $355M. Together they foot to total
revenue to the dollar.

## The segment table is not the split to use

Vistra's reportable segments — Retail, Texas, East, West, Asset Closure — sum to **$9,632M**
against $6,347M of revenue, because **$3,285M of intersegment sales** are eliminated below them.
Retail buys power from the generation segments and both sides are counted.

A split that overstates revenue by 52% is not a split. The disaggregation note foots without
eliminations and is what this card draws. This is worth recording because the segment table is
the more obvious place to look and is the wrong one here.

## Where the operating margin goes

Revenue grew 28% and operating income grew 65%, which looks like clean operating leverage. Two
lines complicate it:

- **Depreciation and amortisation rose 55%** to $711M, roughly twice the rate of revenue
- the **$269M impairment**, against $5M a year ago

Both are inside the filed operating result. Strip the impairment and operating income would be
$1,975M — which is precisely the figure the vendor publishes, and precisely why this card does
not.

## What this card does not carry

- **No debt chart.** `bin/debtfetch.py` matches the balance-sheet column to the period the
  income statement draws, and the vendor publishes no cash and equivalents figure for VST at
  September 30, 2026. It is reported and skipped rather than drawn from the wrong quarter.
- **No post-result earnings surprise.** The vendor's surprise series still ends at Jun '26.
- **No ownership donut**, for the reason given on [[constellation-energy-q3-fy26]]. See
  [[share-ownership-donut]].
- **P/E 18.1 trailing and 14.2 forward**, market cap $45.45B, dividend $0.92 a year for a 0.69%
  yield — all as of November 9, 2026 and all measured against the share price.

## Related pages
- [[constellation-energy-q3-fy26]]
- [[sankey-income-statement]]
- [[favorites-financials]]
- [[cloudflare-q3-fy26]]
- [[ai-data-center-buildout]]
- [[earnings-surprise-chart]]
- [[share-ownership-donut]]
