# Redwire Q3 FY26

**Summary**: Redwire's third quarter 2026 (quarter ended September 30, 2026): $109.0M of revenue, up 5.4% year over year, a **32.3% gross margin that is the highest the company has reported**, and a $23.2M net loss narrowed from $41.2M. Revenue barely grew; cost of sales fell 15%. Space passed Defense Tech to become the larger segment again.

**Sources**: Redwire 8-K exhibit 99.1, Q3 2026 results, filed November 4, 2026 (source: exhibit991redwire09302026e.htm). Prior-period figures are the September 30, 2025 column of the same release.

**Last updated**: 2026-11-04

---

## Income statement

Three months ended September 30, in thousands of USD (source: exhibit991redwire09302026e.htm).

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| **Revenues** | **109,035** | **103,432** | **+5.4%** |
| Cost of sales | (73,813) | (86,622) | **−15%** |
| **Gross profit** | **35,222** | **16,810** | **+110%** |
| Selling, general and administrative | (46,161) | (50,285) | −8% |
| Transaction expenses | (934) | (684) | +37% |
| Research and development | (14,396) | (7,693) | +87% |
| **Operating loss** | **(26,269)** | **(41,852)** | −37% |
| Interest income (expense), net | 2,653 | (6,282) | n/m |
| Other income (expense), net | 21 | 13,844 | n/m |
| **Loss before income taxes** | **(23,595)** | **(34,290)** | −31% |
| Income tax benefit (expense) | 417 | (6,862) | n/m |
| **Net loss** | **(23,178)** | **(41,152)** | **−44%** |

Basic and diluted loss per share $(0.09) against $(0.29), on a share count that grew 72% to
250.1M.

## The improvement is margin, not volume

Revenue grew 5.4% — the slowest of the four cards refreshed on November 4, against
[[qualcomm-fq4-fy26]] at −8%, [[datadog-q3-fy26]] at +35% and [[coherent-fq1-fy27]] at +50%.
What changed is the cost side:

| | Q3 FY26 | Q3 FY25 |
|---|---|---|
| Revenue | $109.0M | $103.4M |
| Cost of sales | $73.8M | $86.6M |
| **Gross margin** | **32.3%** | 16.3% |

**Cost of sales fell $12.8M while revenue rose $5.6M.** Gross profit therefore more than doubled
on 5% more revenue. Redwire's own headline calls these record gross margins, and against the
28% of last quarter and 16% of a year ago that holds.

Redwire also reports an Adjusted Gross Margin, which strips purchase-accounting adjustments out
of cost of sales. The card uses the GAAP figure throughout.

## Space and Defense Tech have swapped back

| Segment | Q3 FY26 | share | Q3 FY25 | Y/Y |
|---|---|---|---|---|
| Space | 61,266 | 56% | 46,548 | **+32%** |
| Defense Tech | 47,769 | 44% | 56,884 | **−16%** |
| **Total** | **109,035** | **100%** | **103,432** | **+5.4%** |

On the previous card (Q2 FY26) Defense Tech was the larger of the two at $61.9M against Space's
$55.2M. One quarter later the order is reversed. Segment Adjusted EBITDA is positive for both —
Space $2.8M (from $(1.9)M) and Defense Tech $7.2M — for $10.0M in total against $4.6M a year ago.

## Why the chart's non-operating income is $3.1M

Redwire uses the **loss layout**: gross profit plus the net loss plus non-operating income fund
every charge on the right. $35.2M + $23.2M + $3.1M = $61.5M of charges.

The $3.1M pools three below-the-line items, because they all fund the same charges:

| | $M |
|---|---|
| Interest income, net | 2.653 |
| Income tax benefit | 0.417 |
| Other income, net | 0.021 |
| **Total** | **3.091** |

Net interest flipped sign: it was a **$6.3M expense** a year ago and is a **$2.7M income** now,
because Redwire paid down debt and raised cash. A year ago the below-the-line total also included
$13.8M of other income, which is why the loss narrowed by less than the operating improvement
would suggest.

## A $0.9M band that the script drops

`bin/mkspec.py` only draws a third operating-expense band when it exceeds the larger of $1M or
0.2% of revenue. Redwire's **transaction expenses of $0.934M** fall just under that floor, so the
script folded them into the non-operating residual and the chart read "Non-operating income
$2.2M" — a figure that is not any line in the filing, being the true $3.1M less a $0.9M operating
cost.

The band was put back by hand and the residual restored to $3.1M. The floor is the right default
for keeping tiny bands off a chart, but it is silent, and when the loss layout computes the
residual by subtraction a dropped band lands in the wrong place rather than simply disappearing.

## What this card does not carry

- **The debt chart still shows Q2 FY26.** The vendor has no September 30, 2026 balance sheet
  column, so `bin/debtfetch.py` skipped the quarter rather than matching one 92 days away.
  Redwire's own balance sheet gives **$47.0M of debt** ($4.5M short-term, $42.5M long-term) plus
  $3.2M of notes payable to sellers, against **$488.9M of cash, equivalents and restricted cash**
  at September 30, 2026 — up from $95.2M at December 31, 2025, against $85.2M of debt then.
  Redwire is comfortably in net cash.
- **Free cash flow was −$66.4M for the quarter** (operating cash flow −$63.6M less $2.8M of
  capital expenditure), against −$27.8M a year ago. The gross-margin improvement has not reached
  the cash statement.
- **The earnings chart's Sep '26 column has no actual.** Redwire reported hours before this page
  was written and the vendor has not posted its figure. The consensus shown is $(0.10) from 4
  analysts, against GAAP diluted EPS of $(0.09).
- **No P/E, trailing or forward.** The last twelve months are a loss and there is no positive
  forward estimate, so both read `n/a`, which is correct rather than missing.
- **The loss layout's labels collide.** On this chart the "Net loss" and "Cost of revenue" labels
  sit on top of their own bars and clip their figures. It is a known `bin/sankey.py` defect that
  the Q2 FY26 card shipped with as well; it is recorded rather than worked around in the data.

## Related pages
- [[sankey-income-statement]]
- [[favorites-financials]]
- [[ouster-q3-fy26]]
- [[qualcomm-fq4-fy26]]
- [[earnings-surprise-chart]]
- [[share-ownership-donut]]
