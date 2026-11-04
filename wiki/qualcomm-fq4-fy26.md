# Qualcomm FQ4 FY26

**Summary**: Qualcomm's fourth quarter of fiscal 2026 (quarter ended September 27, 2026): $10,322M of revenue, **down 8% year over year**, a 51% GAAP gross margin, $1,356M of operating income and $1,251M of net income. Handsets fell 26% while Automotive passed $2B in a quarter for the first time, up 89%. The quarter a year ago was a GAAP net loss, so several year-over-year comparisons on this card are deliberately blank.

**Sources**: Qualcomm 8-K exhibit 99.1, fourth quarter and fiscal 2026 results, filed November 4, 2026 (source: qcom092726erex991.htm). Prior-period figures are the September 28, 2025 column of the same release.

**Last updated**: 2026-11-04

---

## Income statement

Three months ended, in millions of USD (source: qcom092726erex991.htm).

| Line | FQ4 FY26 | FQ4 FY25 | Y/Y |
|---|---|---|---|
| Equipment and services | 8,893 | 9,674 | −8% |
| Licensing | 1,429 | 1,596 | −10% |
| **Total revenues** | **10,322** | **11,270** | **−8%** |
| Cost of revenues | (5,084) | (5,033) | +1% |
| **Gross profit** | **5,238** | **6,237** | **−16%** |
| Research and development | (2,684) | (2,370) | +13% |
| Selling, general and administrative | (963) | (910) | +6% |
| Other | (235) | (39) | n/m |
| **Total costs and expenses** | **(8,966)** | **(8,352)** | **+7%** |
| **Operating income** | **1,356** | **2,918** | **−54%** |
| Interest expense | (170) | (171) | −1% |
| Investment and other (expense) income, net | (13) | 224 | n/m |
| **Income before income taxes** | **1,173** | **2,971** | **−61%** |
| Income tax benefit (expense) | 78 | (6,088) | n/m |
| **Net income** | **1,251** | **(3,117)** | n/m |

Diluted EPS $1.17 against $(2.89). Non-GAAP diluted EPS $2.17 against $3.00.

## The only card on the tab with revenue going backwards

Revenue fell 8% and gross profit fell 16%, so the decline compounds down the statement. The
cause is one revenue stream:

| QCT revenue stream | FQ4 FY26 | share of QCT | FQ4 FY25 | Y/Y |
|---|---|---|---|---|
| Handsets | 5,137 | 57% | 6,961 | **−26%** |
| Automotive | 1,990 | 22% | 1,053 | **+89%** |
| IoT | 1,888 | 21% | 1,807 | +4% |
| **Total QCT** | **9,015** | **100%** | **9,821** | **−8%** |

Handsets were 71% of QCT a year ago and are 57% now. Automotive passed **$2B in a quarter for
the first time**; Automotive and IoT together grew 36% and are 38% of total company revenue.

By reportable segment:

| Segment | Revenue | EBT | EBT margin | a year ago |
|---|---|---|---|---|
| QCT | 9,015 | 2,142 | 24% | 29% |
| QTL | 1,304 | 918 | 70% | 72% |

QSI and other is the $3M residual to the $10,322M total, which is why it appears on the chart as
a hairline rather than a band.

## GAAP revenue is *lower* than non-GAAP revenue

This is the opposite of the usual direction and worth stating plainly: non-GAAP revenue for the
quarter was **$10,442M against GAAP $10,322M**. The $120M difference is a payment to a customer
arising from a recent legal settlement, which is netted against revenue under GAAP and added back
in the non-GAAP presentation (source: qcom092726erex991.htm).

Every other adjustment on the card's chart runs the familiar way: $873M of share-based
compensation and $537M of other items separate GAAP operating income of $1,356M from non-GAAP
$2,769M.

## Gross margin, and why Qualcomm says it will stay under pressure

| | FQ4 FY26 | FQ4 FY25 |
|---|---|---|
| Gross margin | **50.7%** | 55.3% |
| Operating margin | 13.1% | 25.9% |
| Net margin | 12.1% | n/m (loss) |

The release is unusually direct about the cause: *"The semiconductor industry is experiencing a
broad-based increase in input costs across wafer fabrication, assembly, test, advanced packaging,
memory and other materials"*, and Qualcomm says it is raising product prices in response, with
**the full benefit expected only in the second half of fiscal 2027** (source:
qcom092726erex991.htm). Memory appearing in that list connects this card to
[[micron-fq4-fy26]] and [[sandisk-fq1-fy27]] from the other side of the same cycle.

The $235M band the chart draws as **Restructuring** is the statement's own "Other" operating
line, which the release identifies as restructuring and restructuring-related charges. A year ago
that line was $39M.

## Below the operating line, and why the year-ago comparisons are blank

Income tax was a **$78M benefit** rather than a charge, so on the Sankey it flows *into* net
profit. That is the second tax benefit among the four cards built on November 4, alongside
[[coherent-fq1-fy27]].

A year ago the same quarter was a **GAAP net loss of $3,117M**, on a $6,088M income tax charge.
A percentage change measured against a negative base is not meaningful, so the chart's year-ago
hovers carry revenue, gross profit, operating profit, R&D and SG&A but deliberately omit net
profit and tax. The release's own "+140%" for net income is a change in sign, not a growth rate.

## Fiscal 2026, and a trailing P/E that is a denominator effect

| | FY26 | FY25 |
|---|---|---|
| Revenues | 43,120 | 44,284 |
| Operating income | 8,658 | 12,355 |
| **GAAP diluted EPS** | **$12.70** | $5.01 |
| Non-GAAP diluted EPS | $10.54 | $12.03 |

GAAP EPS is *higher* than non-GAAP for the full year, which almost never happens. The reason is a
**$5.7 billion income tax benefit from releasing a valuation allowance** in the second quarter of
fiscal 2026, as Qualcomm now expects to realise its existing federal deferred tax assets.

That one item is also why the card's trailing P/E reads **13.7** on November 4 against a forward
P/E of 17.1. The trailing multiple is low because the denominator carries a one-off tax benefit,
not because the price moved. Measured against fiscal 2026 non-GAAP EPS of $10.54, the same share
price is roughly 16.5x.

## What this card does not carry

- **The debt chart still shows FQ3 FY26.** The vendor has no September 27, 2026 balance sheet
  column, so `bin/debtfetch.py` skipped the quarter rather than matching one 91 days away.
  Qualcomm's own release gives **$15,112M of total debt** ($2,492M short-term, $12,620M
  long-term) against $4,636M of cash and equivalents plus $3,045M of marketable securities at
  September 27, 2026. Short-term debt went from zero a year earlier to $2,492M.
- **The earnings chart's Sep '26 column has no actual.** Qualcomm reported hours before this page
  was written and the vendor has not posted its figure. The consensus shown is $1.68; Qualcomm's
  non-GAAP diluted EPS was $2.17 and GAAP $1.17 — a card where picking the wrong basis changes
  the verdict completely. See [[earnings-surprise-chart]].
- **Stock compensation** of $873M is reported company-wide and spread across cost of revenues,
  R&D and SG&A without Qualcomm saying how, so the chart puts it on the pooled
  operating-expenses node only.

## Guidance

FQ1 FY27: revenue $10.4B–$11.2B, QCT $9.0B–$9.6B, QTL $1.3B–$1.5B, GAAP diluted EPS $1.03–$1.23
and non-GAAP $2.15–$2.35. For fiscal 2027 Qualcomm projects non-handset revenue growth of **more
than 60%** and reiterates a **$5B data centre revenue target**.

## Related pages
- [[sankey-income-statement]]
- [[favorites-financials]]
- [[coherent-fq1-fy27]]
- [[amd-q3-fy26]]
- [[micron-fq4-fy26]]
- [[earnings-surprise-chart]]
- [[share-ownership-donut]]
