# Nebius Group Q3 FY26

**Summary**: Nebius Group's third quarter 2026 (quarter ended September 30, 2026): $980.8M of revenue, up 571% year over year, and the first quarter of positive income from operations -- $50.4M against a $130.2M loss a year ago. The net line is still a $37.5M loss, and what sits between the two is the whole story: $112.5M of interest expense and a $49.5M induced conversion charge.

**Sources**: Nebius Group 6-K exhibit 99.1, Q3 2026 results, furnished November 12, 2026, and the unaudited condensed consolidated financial statements furnished the same day (segments note). Market figures are stockanalysis.com's, read November 12, 2026.

**Last updated**: 2026-11-12

---

## Income statement

Three months ended September 30, in millions of USD (source: 6-K exhibit 99.1, unaudited condensed
consolidated statements of operations).

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| **Revenues** | **980.8** | **146.1** | **+571%** |
| Cost of revenues | (219.7) | (42.9) | +412% |
| **Gross profit** (derived) | **761.1** | **103.2** | **+638%** |
| Product development | (118.6) | (44.9) | +164% |
| Sales, general and administrative | (237.4) | (89.5) | +165% |
| Depreciation and amortization | (354.7) | (99.0) | +258% |
| **Income / (loss) from operations** | **50.4** | **(130.2)** | n/m |
| Interest income | 30.2 | 6.2 | +387% |
| Interest expense | (112.5) | (14.7) | +665% |
| Income / (loss) from equity method investments | (2.8) | (7.5) | n/m |
| Induced conversion expense | (49.5) | — | n/m |
| Other income, net | 21.5 | 26.3 | -18% |
| **Loss before income taxes** | **(62.7)** | **(119.9)** | n/m |
| Income tax benefit | 25.2 | 0.3 | n/m |
| **Net loss from continuing operations** | **(37.5)** | **(119.6)** | **-69%** |

Diluted loss per share $0.13 against $0.50, on 298.0M weighted-average shares against 241.1M.

Every operating line here **excludes** depreciation and amortization, which the filing presents
separately and the chart draws as its own band. The 78% gross margin is therefore not comparable
with a card whose cost of revenue carries D&A -- the same caution [[iren-fq1-fy27]] carries.

## The operating line turned, and the net line did not

This is the first quarter in which Nebius earned money from operations. It did not come from
margin discipline on the way down -- cost of revenues grew 412% and SG&A 165% -- but from revenue
growing 571% against a cost base that was already mostly fixed:

| | Q3 FY25 | Q3 FY26 |
|---|---|---|
| Cost of revenues | 29% of revenue | 22% |
| Product development | 31% | 12% |
| Sales, general and administrative | 61% | 24% |
| Depreciation and amortization | 68% | 36% |
| **Total operating costs** | **189%** | **95%** |

Depreciation at 36% of revenue is still the single largest charge on the statement -- nearly ten
times the net loss. It is the cost of the GPUs, and it will keep growing: capital expenditure was
**$7,300.4M in the quarter**, more than seven times the revenue it currently serves.

## What turned the operating profit back into a loss

| | $M |
|---|---|
| Income from operations | 50.4 |
| Interest expense | (112.5) |
| Induced conversion expense | (49.5) |
| Interest income | 30.2 |
| Other income, net | 21.5 |
| Loss from equity method investments | (2.8) |
| Income tax benefit | 25.2 |
| **Net loss** | **(37.5)** |

The chart draws these as one **$87.9M "Non-operating & tax, net"** band, because the loss layout
has one slot for everything below the operating line. The composition matters though: the $49.5M
induced conversion expense is a one-off, while the $112.5M of interest expense is the running cost
of $14.2B of debt and will not go away. Strip the one-off and the quarter is roughly breakeven at
the net line.

## Segments

| | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| Nebius AI cloud | 973.8 | 131.1 | **+643%** |
| TripleTen | 9.0 | 16.2 | -44% |
| Avride | 1.3 | 0.2 | +550% |
| Total segment revenues | 984.1 | 147.5 | +567% |
| Eliminations | (3.3) | (1.4) | |
| **Total revenues** | **980.8** | **146.1** | **+571%** |

The AI cloud business is 99% of the group. On the chart its bar is drawn at **$970.5M**, its
reported figure less the group's $3.3M of intersegment eliminations, so the three bars foot to
consolidated revenue -- the same convention [[nebius-q2-fy26]] used. The filing reports
eliminations as one group-level line and does not attribute them to a segment, so putting them
against the cloud business is this chart's choice rather than the company's.

TripleTen is shrinking (-44%) and Avride is immaterial. Neither changes the picture; both lose
money at the adjusted EBITDA line (-$6.9M and -$45.5M), against the cloud business's +$518.2M.

## Balance sheet

| | Sep 30, 2026 | Dec 31, 2025 |
|---|---|---|
| Cash and cash equivalents | 7,425.6 | 3,678.1 |
| Property and equipment, net | 19,341.9 | 5,553.3 |
| Total assets | 38,744.1 | 12,430.6 |
| Debt (current + non-current) | 14,190.8 | 4,127.7 |
| Deferred revenue, non-current | 7,963.7 | 1,302.0 |
| Total shareholders' equity | 12,299.2 | 4,594.0 |

Total assets tripled in nine months. The **$7,963.7M of non-current deferred revenue** is worth
noticing on its own: it is customer cash already received for capacity not yet delivered, which is
a liability on the balance sheet and a funding source in practice.

## What this card does not carry

- **The debt chart is a quarter behind.** `bin/debtfetch.py` refused the September 30 column
  because the vendor has not published a balance sheet for it, so the bars still show Q2 FY26. The
  filing's own figures are in the table above; nothing was hand-filled.
- **The earnings chart predates this report.** `bin/epsfetch.py` is returning HTTP 403 for every
  ticker, so it could not be refreshed. See [[earnings-surprise-chart]].
- **P/E** is measured against the share price and moves every session. The trailing figure is
  inflated by the equity revaluation gains booked earlier in the year, not by operating earnings.

Toloka remains in discontinued operations after the 2025 investment transaction and is not part of
this statement.

## Related pages
- [[nebius-q2-fy26]]
- [[ai-data-center-buildout]]
- [[sankey-income-statement]]
- [[coreweave-q3-fy26]]
- [[iren-fq1-fy27]]
- [[earnings-surprise-chart]]
