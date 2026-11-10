# Rigetti Computing Q3 FY26

**Summary**: Rigetti's third quarter 2026 (quarter ended September 30, 2026): revenue **fell** 28% to $1.41M, the operating loss widened to $33.2M, and the net loss came in at $3.1M only because a $25.3M non-cash warrant gain absorbed almost all of it.

**Sources**: Rigetti Computing 10-Q for the quarter ended September 30, 2026, filed November 10, 2026 (source: sec.gov, accession 0001104659-26-125161) — condensed consolidated statements of operations (R4) and the revenue disaggregation note (R54). Market figures from stockanalysis.com, November 10, 2026.

**Last updated**: 2026-11-10

---

## Income statement

Three months ended September 30, in thousands of US dollars.

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| **Revenue** | **1,411** | **1,947** | **−27.5%** |
| Cost of revenue | (554) | (1,543) | −64% |
| **Total gross profit** | **857** | **404** | +112% |
| Research and development | (25,495) | (15,020) | +70% |
| Selling, general and administrative | (8,548) | (5,933) | +44% |
| **Total operating expenses** | **(34,043)** | **(20,953)** | +62% |
| **Loss from operations** | **(33,186)** | **(20,549)** | worse |
| Interest income | 4,758 | 5,598 | −15% |
| Change in fair value of derivative warrant liabilities | **25,291** | **(181,955)** | n/m |
| Change in fair value of earn-out liabilities | — | (4,062) | n/m |
| **Total other income (expense), net** | **30,049** | **(180,419)** | n/m |
| **Net loss before income taxes** | **(3,137)** | **(200,968)** | — |
| Provision for income taxes | — | — | — |
| **Net loss** | **(3,137)** | **(200,968)** | — |

Nine months to September 30, 2026: revenue $10.9M against $5.2M, net loss $22.6M against
$198.0M.

## The headline net loss is a warrant revaluation, not an operating result

$3.1M of net loss against $201.0M a year ago looks like a transformation. It is not one.

| | Q3 FY25 | Q3 FY26 |
|---|---|---|
| Revenue | $1.95M | **$1.41M** |
| Operating loss | $(20.5)M | **$(33.2)M** |
| Warrant fair value change | **$(182.0)M charge** | **$25.3M gain** |
| Net loss | $(201.0)M | $(3.1)M |

The two outer rows move in opposite directions. **Revenue fell and the operating loss grew by
62%**; what shrank was a non-cash mark on derivative warrant liabilities, which swung by $207M
between the two quarters. Add $4.8M of interest income and the $30.0M of non-operating income
covers 91% of the operating loss.

The chart draws this honestly — the green "Non-operating income $30.05M" band is more than
thirty times the size of the gross profit band feeding the same column. Anyone reading the net
loss alone would reach the wrong conclusion about the quarter.

This is the same accounting shape that keeps IONQ off the Financials tab (see
[[favorites-financials]]), with one difference that matters: Rigetti's net line is still a **loss**, so the loss
layout can draw it. IONQ's warrant swing was large enough to push net income positive under an
operating loss, which the profit layout cannot represent.

## Revenue fell, because no systems were sold

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| Collaborative research and professional services | 1,265 | 1,896 | −33% |
| Access to quantum computing systems | 146 | 51 | +186% |
| Sales of quantum computers and components | **—** | — | — |
| **Total** | **1,411** | **1,947** | −27.5% |

The two lines foot to total revenue to the dollar (source: 10-Q revenue disaggregation note).

Rigetti sold **no quantum computers or components** in the quarter. The nine-month column
carries $7.144M of system sales, all of it recognised in earlier quarters of 2026 and all of it
at a point in time. The services business, which is what recurs, shrank by a third.

## Basic and diluted EPS differ by 8x

Basic loss per share was **$(0.01)**; diluted was **$(0.08)**. The gap is the warrant gain: for
the diluted calculation it is reversed, which lifts the loss available to common stockholders
from $3.137M to **$28.428M**. Basic weighted-average shares were 336,411,000.

Where a card quotes one EPS figure for a company with live warrants, check which one.

## A note on precision

This card is drawn in millions at **two** decimals rather than the usual one. At one decimal
the $0.857M of gross profit rounds to $0.9M against $1.4M of revenue, which reads as a **64%**
margin against the filed **61%** — the rounding trap recorded in the `income-statement-chart`
skill, hit here for real.

## What this card does not have

- **No debt chart.** The vendor has no September 30, 2026 balance-sheet column yet; the nearest
  is June 30. `bin/debtfetch.py` reported and skipped rather than putting a June balance sheet
  beside a September income statement.
- **No post-result EPS surprise.** The vendor's earnings endpoint returned HTTP 403 on the
  refresh, so the Sep '26 point is still the pre-announcement consensus of $(0.07).

## Related pages
- [[favorites-financials]]
- [[sankey-income-statement]]
- [[d-wave-quantum-q3-fy26]]
