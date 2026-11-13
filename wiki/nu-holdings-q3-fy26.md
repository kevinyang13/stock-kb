# Nu Holdings Q3 FY26

**Summary**: Nu Holdings' third quarter 2026 (quarter ended September 30, 2026): $5,820.4M of revenue, up 39% year over year, $2,436.9M of gross profit, $1,358.6M of operating profit and $1,091.6M of net income. Net income grew 39% while pretax income grew only 21%, and the difference is a tax rate that fell from 29.9% to 19.2%. This is also the first Nu card to draw a revenue split.

**Sources**: Nu Holdings 6-K, unaudited interim condensed consolidated statements of income for the three and nine months ended September 30, 2026, furnished November 12, 2026, reviewed by KPMG Auditores Independentes. Market figures are stockanalysis.com's, read November 12, 2026.

**Last updated**: 2026-11-12

---

## Income statement

Three months ended September 30, in thousands of USD (source: 6-K, statements of income). Nu
reports in US dollars, so nothing here is converted.

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| Interest income and gains net of losses | 5,003,316 | 3,577,478 | +40% |
| Fee and commission income | 817,048 | 595,238 | +37% |
| **Total revenue** | **5,820,364** | **4,172,716** | **+39%** |
| Interest and other financial expenses | (1,571,596) | (1,275,711) | +23% |
| Transactional expenses | (143,383) | (104,990) | +37% |
| Expected credit loss | (1,668,487) | (977,483) | **+71%** |
| **Total cost of services provided** | **(3,383,466)** | **(2,358,184)** | **+43%** |
| **Gross profit** | **2,436,898** | **1,814,532** | **+34%** |
| Customer support and operations | (223,252) | (174,843) | +28% |
| General and administrative | (590,713) | (349,262) | +69% |
| Marketing | (126,082) | (70,340) | +79% |
| Other expenses | (160,024) | (129,895) | +23% |
| Other income | 21,807 | 27,267 | -20% |
| **Total operating expenses** | **(1,078,264)** | **(697,073)** | **+55%** |
| Share of loss in associates | (8,341) | (1,170) | n/m |
| **Income before income taxes** | **1,350,293** | **1,116,289** | **+21%** |
| Income taxes | (258,735) | (333,611) | **-22%** |
| **Net income** | **1,091,558** | **782,678** | **+39%** |

Diluted EPS $0.2235 against $0.1595, on 4,881M weighted-average diluted shares.

## The split was always filed

This card previously drew a single "Total revenue" bar, and the note said no reported split added
up to the aggregator's net revenue line. Built from the filing instead, the split is there and
foots to the dollar:

| | Q3 FY26 | share |
|---|---|---|
| Interest income and gains net of losses | 5,003.3 | 86% |
| Fee and commission income | 817.0 | 14% |
| **Total** | **5,820.4** | **100%** |

That is the same correction [[datadog-q3-fy26]] and [[cloudflare-q3-fy26]] got, and for the same
reason: the figure the vendor charted was not the figure the company reports.

## "Gross margin" means something different here

Nu is a bank. Its cost of revenue is not the cost of making anything:

| | $M | share of cost |
|---|---|---|
| Expected credit loss | 1,668.5 | 49% |
| Interest and other financial expenses | 1,571.6 | 46% |
| Transactional expenses | 143.4 | 4% |

The 42% gross margin is a **net interest and fee margin after credit losses**. It is not comparable
with a gross margin elsewhere on the Financials tab, where that line measures the cost of
delivering a product. The same caveat the tab applies to [[visa-q4-fy26]], which reports no cost of
revenue at all, applies here in the opposite direction.

It also means almost nothing sits below the operating line. The chart's "Interest & other, net"
charge of $8.3M is the share of loss in associates, and that is all -- the interest expense a
manufacturer would show down there is inside cost of revenue, because for a bank it *is* cost of
revenue.

## Credit loss is the line to watch

Expected credit loss grew **71%** against revenue's 39%, and is now **29% of revenue** against 23%
a year ago. It is the fastest-growing line on the statement and the largest single component of
cost. Gross profit still grew 34%, so the margin absorbed it -- but it absorbed it, rather than
being unaffected by it.

## Net income grew twice as fast as pretax income

| | Q3 FY26 | Q3 FY25 |
|---|---|---|
| Income before income taxes | 1,350.3 | 1,116.3 |
| Income taxes | (258.7) | (333.6) |
| **Effective tax rate** | **19.2%** | **29.9%** |
| Net income | 1,091.6 | 782.7 |

Pretax income grew 21%. Net income grew 39%. The gap is entirely the tax rate, worth roughly $120M
to the quarter. A reader comparing net income year over year is reading a tax outcome as much as an
operating one -- the same distinction [[alphabet-q3-fy26]] and [[palantir-q3-fy26]] needed, though
here it is the tax line rather than an investment gain.

## Balance sheet

Total assets $87,428.6M, up from $74,893.9M at year-end. Cash and equivalents $13,772.3M.
Borrowings and financing $4,980.1M. Customer **deposits of $47,486.8M** are the real funding base
and are not debt in the sense the debt chart means.

## What this card does not carry

- **The debt chart is a quarter behind.** `bin/debtfetch.py` refused the September 30 column -- the
  vendor has not published a balance sheet for it -- so the bars still show Q2 FY26. The filing's
  own figures are above; nothing was hand-filled.
- **The earnings chart predates this report.** `bin/epsfetch.py` is returning HTTP 403 for every
  ticker. See [[earnings-surprise-chart]].
- **P/E** is measured against the share price and moves every session.

## Related pages
- [[sankey-income-statement]]
- [[datadog-q3-fy26]]
- [[cloudflare-q3-fy26]]
- [[visa-q4-fy26]]
- [[alphabet-q3-fy26]]
- [[palantir-q3-fy26]]
- [[earnings-surprise-chart]]
