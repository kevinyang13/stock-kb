# AMD Q3 FY26

**Summary**: AMD's third quarter 2026 (quarter ended September 26, 2026): $13,377M of revenue, up 45% year over year, a 54% GAAP gross margin and $2,832M of operating income. Data Center revenue nearly doubled to $8,546M. GAAP net income of $2,428M is the net of two large offsetting items that have nothing to do with operations — a $1,097M charge for remeasuring customer warrants and a $555M income tax *benefit*.

**Sources**: AMD 8-K exhibit 99.1, Q3 2026 results, filed November 3, 2026 (source: q32026991.htm). Prior-period figures are the September 27, 2025 column of the same release.

**Last updated**: 2026-11-03

---

## Income statement

Three months ended, in millions of USD (source: q32026991.htm).

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| **Net revenue** | **13,377** | **9,246** | **+45%** |
| Cost of sales | (5,910) | (4,206) | +41% |
| Amortization of acquisition-related intangibles | (257) | (260) | −1% |
| **Total cost of sales** | **(6,167)** | **(4,466)** | **+38%** |
| **Gross profit** | **7,210** | **4,780** | **+51%** |
| Research and development | (2,803) | (2,139) | +31% |
| Marketing, general and administrative | (1,298) | (1,069) | +21% |
| Amortization of acquisition-related intangibles | (277) | (302) | −8% |
| **Total operating expenses** | **(4,378)** | **(3,510)** | **+25%** |
| **Operating income** | **2,832** | **1,270** | **+123%** |
| Interest expense | (62) | (37) | +68% |
| Other income (expense), net | (902) | 82 | n/m |
| **Income before taxes and equity income** | **1,868** | **1,315** | **+42%** |
| Income tax provision (benefit) | 555 | (153) | n/m |
| Equity income in investee | 5 | 10 | −50% |
| **Net income** | **2,428** | **1,243** | **+95%** |

Diluted EPS $1.46 against $0.75. Non-GAAP diluted EPS $2.09 against $1.20.

## The gross margin on this card is 54%, not 56%

Three different gross margins can be quoted for this quarter and all three are defensible:

| Basis | Gross profit | Margin |
|---|---|---|
| GAAP, as AMD's statement reports it | 7,210 | **54%** |
| Revenue less the "Cost of sales" line only | 7,467 | 56% |
| AMD's own non-GAAP | 7,483 | 56% |

AMD splits cost of sales into two rows and subtotals them, so the $257M of acquisition-related
intangible amortization is *inside* total cost of sales and inside the reported gross profit of
$7,210M. A source that picks up only the first row gets $7,467M and a 56% margin, which coincides
closely with the non-GAAP figure while not being it.

The previous card for this ticker (Q2 FY26) carried the 56% version. This card follows the 8-K's
own subtotals throughout, which is the rule in [[sankey-income-statement]]: trust the subtotals,
derive the bridge.

## Segments

| Segment | Q3 FY26 | share | Q3 FY25 | Y/Y |
|---|---|---|---|---|
| Data Center | 8,546 | 64% | 4,341 | **+97%** |
| Client | 2,949 | 22% | 2,750 | +7% |
| Embedded | 1,109 | 8% | 857 | +29% |
| Gaming | 773 | 6% | 1,298 | **−40%** |
| **Total** | **13,377** | **100%** | **9,246** | **+45%** |

AMD reports three segments; Client and Gaming are one reportable segment, disclosed with its two
businesses underneath. The chart draws the four lines because the reportable segment moves in two
directions at once: Client and Gaming fell 8% overall while Client itself grew 7%, the whole decline
being Gaming's semi-custom and graphics revenue.

Segment operating income tells the same story more sharply: Data Center $2,882M against $1,074M a
year ago, while "All other" — unallocated amortization, stock compensation and acquisition costs —
is a $1,076M charge.

## Why net margin is 18% when operating margin is 21%

$959M of net non-operating expense sits between operating income and net income:

| | $M |
|---|---|
| Change in fair value of warrant liability | (1,097) |
| Gains on long-term investments, net | 67 |
| Rest of "other income (expense), net" | 128 |
| **Other income (expense), net, as reported** | **(902)** |
| Interest expense | (62) |
| Equity income in investee | 5 |
| **Total between operating income and net income** | **(959)** |

The first three rows are AMD's own reconciliation items; the $128M residual is derived, being the
reported $(902)M less the two named pieces.

The warrant charge is the quarterly remeasurement of warrants AMD issued to certain customers. AMD
states it is driven by changes in AMD's own share price and other valuation assumptions — so it is a
mark on AMD's stock, not a result of the quarter's trading. The cash flow statement carries a
matching non-cash item of $1,179M for warrants issued to customers.

The tax line runs the other way. AMD recorded a **$555M income tax benefit** rather than a charge,
so on the Sankey it flows *into* net profit instead of out of it. The GAAP-to-non-GAAP bridge adds
back a $1,073M income tax provision adjustment alongside the $1,097M warrant charge: the two are
substantially the same event seen from both sides of the tax line.

Net of all this, GAAP net income grew 95% while operating income grew 123%.

## Guidance

Fourth quarter revenue of approximately $17 billion, ±3% — a midpoint of +66% year over year and
+27% sequentially, with non-GAAP gross margin of approximately 55%.

## What this card does not carry

- **The debt chart still shows Q2 FY26.** The vendor has no September 26, 2026 balance sheet
  column, so `bin/debtfetch.py` skipped the quarter rather than matching one 91 days away. AMD's own
  release gives $7,079M of total debt, $15,776M of cash and short-term investments, and $554M of
  free cash flow for the quarter — against $3,226M of debt and $13,111M of cash a quarter earlier.
  Total debt more than doubled in the quarter.
- **The earnings chart's Sep '26 column has no actual.** AMD reported hours before this page was
  written and the vendor has not posted its figure. The consensus shown is $1.68; AMD's non-GAAP
  diluted EPS was $2.09.
- **Stock compensation** of $523M is reported company-wide and spread across cost of sales, R&D and
  MG&A without AMD saying how, so the chart puts it on the pooled operating-expenses node only.

## Related pages
- [[sankey-income-statement]]
- [[favorites-financials]]
- [[micron-fq4-fy26]]
- [[intel-q3-fy26]]
- [[earnings-surprise-chart]]
- [[share-ownership-donut]]
