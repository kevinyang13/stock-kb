# Xanadu Quantum Q3 FY26

**Summary**: Xanadu Quantum's third quarter 2026 (quarter ended September 30, 2026): $1.3M of revenue, up 32% year over year, against $35.8M of operating expenses -- a $34.6M operating loss and a $32.2M net loss. R&D alone is twenty times the quarter's revenue. The loss per share fell from $0.36 to $0.11, but only because the share count went from 55.8M to 304.9M in the March 2026 reverse recapitalization.

**Sources**: Xanadu Quantum Technologies 6-K, consolidated statements of operations and comprehensive loss for the three and nine months ended September 30, 2026, furnished November 12, 2026. Market figures are stockanalysis.com's, read November 12, 2026.

**Last updated**: 2026-11-12

---

## Income statement

Three months ended September 30, in thousands of USD (source: 6-K, consolidated statements of
operations and comprehensive loss).

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| **Revenue** | **1,305** | **987** | **+32%** |
| Cost of revenue (excl. D&A) | (94) | (52) | +81% |
| Research and development | (25,560) | (15,301) | +67% |
| General and administrative | (9,150) | (4,002) | +129% |
| Sales and marketing | (900) | (263) | +242% |
| Depreciation and amortization | (1,740) | (1,707) | +2% |
| Other operating (income) expense, net | 1,512 | (358) | n/m |
| **Total operating expenses** | **(35,932)** | **(21,683)** | **+66%** |
| **Loss from operations** | **(34,627)** | **(20,696)** | +67% |
| Interest income (expense), net | 2,272 | 334 | +580% |
| Other income (expense), net | 159 | 64 | +148% |
| **Total other income, net** | **2,431** | **398** | **+511%** |
| **Net loss** | **(32,196)** | **(20,298)** | **+59%** |

No tax line in either period.

## The percentages on this chart read in the thousands

R&D is **1,969% of revenue**. G&A is 700%. That is not a formatting error and it is not a cost
problem -- it is what a pre-commercial company with a revenue line looks like when every expense
band is expressed as a share of revenue, which is how every card on the Financials tab draws them.
The comparison that means something here is cash against burn, not any margin.

## One band on the chart is a netting

The filing shows **"Other operating (income) expense, net"** as a credit of $1,512K sitting inside
operating expenses. A negative band cannot be drawn in a sankey, so the chart folds it into
depreciation and amortization and labels the result **"D&A, net of credits" ($0.2M)**: $1,740K of
D&A less the $1,512K credit. Both components are in the table above. The alternative -- dropping
the credit -- would have left the statement not footing, which is the one thing
[[sankey-income-statement]] does not allow.

Over the nine months that same line is a **$7,236K credit**, so it is not a one-quarter artefact.

Cost of revenue is stated **exclusive of** the depreciation and amortization shown below it, so the
93% gross margin is not comparable with a card whose cost of revenue carries D&A.

## Loss per share fell because the share count rose

| | Q3 FY26 | Q3 FY25 |
|---|---|---|
| Net loss | $32.2M | $20.3M |
| Weighted-average shares | 304,940,693 | 55,822,815 |
| **Loss per share** | **$(0.11)** | **$(0.36)** |

The loss grew 59%. The loss per share fell 69%. Both are true, and the reason is the **reverse
recapitalization completed March 26, 2026**, in which Xanadu Quantum Technologies Limited became
the parent of Old Xanadu and the former SPAC. Per-share figures for prior periods have been
retroactively recast, but the share count itself is not comparable, so the per-share trend says
nothing about the business.

## Non-operating income flips sign over nine months

The quarter shows **$2.4M of non-operating income**, essentially net interest on the cash the
recapitalization raised. The nine-month figure is a **$7.0M net expense**, because of a $7.8M loss
on earn-out share liabilities and a $1.9M loss on derivative instruments booked earlier in the
year. A reader annualizing this quarter's non-operating line would get the sign wrong.

## Cash and burn

Cash and equivalents **$286.5M** at September 30, from $16.2M at the start of the year -- $337.8M
raised in financing against $51.9M used in operations and $16.0M in investing, over nine months.
Stock-based compensation is $11.6M for the nine months against $2.8M a year ago; the filing gives
no quarterly split, so none is shown.

## What this card does not carry

- **The debt chart is a quarter behind.** `bin/debtfetch.py` refused the September 30 column
  because the vendor publishes no quarterly free cash flow for it, so the bars still show Q2 FY26
  ($59.1M of debt, $312.8M of cash). Nothing was hand-filled.
- **No earnings chart at all** for this ticker, and `bin/epsfetch.py` is returning HTTP 403 for
  every ticker in any case. See [[earnings-surprise-chart]].
- **P/E** reads n/a both ways: the last twelve months are a loss and there is no positive forward
  estimate.

## Related pages
- [[sankey-income-statement]]
- [[d-wave-quantum-q3-fy26]]
- [[earnings-surprise-chart]]
- [[share-ownership-donut]]
