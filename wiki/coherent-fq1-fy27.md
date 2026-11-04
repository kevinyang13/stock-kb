# Coherent FQ1 FY27

**Summary**: Coherent's first quarter of fiscal 2027 (quarter ended September 30, 2026): $2,370.3M of revenue, up 50% year over year, a 39.1% gross margin, $377.9M of operating income and $381.6M of net earnings. Datacenter & Communications grew 79% and is now 82% of the company; Industrial fell 15%. Net earnings exceed pretax income because income tax was a benefit.

**Sources**: Coherent 8-K exhibit 99.1, first quarter fiscal 2027 results, filed November 4, 2026 (source: d176836dex991.htm). Prior-period figures are the September 30, 2025 column of the same release.

**Last updated**: 2026-11-04

---

## Income statement

Three months ended, in millions of USD (source: d176836dex991.htm).

| Line | FQ1 FY27 | FQ1 FY26 | Y/Y |
|---|---|---|---|
| **Revenues** | **2,370.3** | **1,581.4** | **+49.9%** |
| Cost of goods sold | (1,442.6) | (1,002.2) | +44% |
| **Gross profit** | **927.7** | **579.2** | **+60%** |
| Research and development | (236.6) | (154.9) | +53% |
| Selling, general and administrative | (304.7) | (252.1) | +21% |
| Restructuring charges | (8.6) | (19.3) | −55% |
| Impairment of assets held-for-sale | — | (9.1) | n/m |
| Gain on sale of business | — | 115.2 | n/m |
| **Total operating expenses** | **(549.9)** | **(320.2)** | **+72%** |
| **Operating income** | **377.9** | **259.1** | **+46%** |
| Interest expense | (46.3) | (58.7) | −21% |
| Other income, net | 27.2 | 16.5 | +65% |
| **Earnings before income taxes** | **358.8** | **216.9** | **+65%** |
| Income taxes | 22.8 | 8.3 | n/m |
| **Net earnings** | **381.6** | **225.2** | **+69%** |
| Less: net loss attributable to non-controlling interests | 3.1 | 1.2 | n/m |
| **Net earnings attributable to Coherent Corp.** | **384.7** | **226.3** | **+70%** |
| Less: dividends on preferred stock | — | 33.5 | n/m |

## The release's columns are not in the order they look

The three quarterly columns run **September 30 2026, June 30 2026, September 30 2025** — last
quarter sits *between* the two year-over-year columns. The year-ago comparative is the **third**
column, not the second. This is the same trap that [[ouster-q3-fy26]] carries in a different
order, and it is worth checking on every release rather than per filer.

## One segment is the whole story

| Segment | FQ1 FY27 | share | FQ1 FY26 | Y/Y |
|---|---|---|---|---|
| Datacenter & Communications | 1,951.7 | **82%** | 1,090.0 | **+79%** |
| Industrial | 418.6 | 18% | 491.4 | **−15%** |
| **Total** | **2,370.3** | **100%** | **1,581.4** | **+49.9%** |

Datacenter & Communications was 69% of revenue a year ago. It added $861.7M of revenue while
Industrial lost $72.8M — so the segment that is growing added more than the entire company's
year-over-year increase, and Industrial subtracted from it.

## Margins

| | FQ1 FY27 | FQ4 FY26 | FQ1 FY26 |
|---|---|---|---|
| Revenue | $2,370M | $2,046M | $1,581M |
| Gross margin | **39.1%** | 38.5% | 36.6% |
| Operating margin | 15.9% | 12.4% | 16.4% |
| Operating expenses | $550M | $533M | $320M |

Gross margin improved sequentially and year over year. Operating margin is *below* where it was a
year ago, but that comparison is distorted: the year-ago operating expense subtotal of $320.2M
included a **$115.2M gain on the sale of a business**, which reduced expenses and lifted operating
income. Against last quarter — a cleaner comparison — operating margin went from 12.4% to 15.9%.

That is why the chart's year-ago hover is reliable for the operating-expense *total* but not band
for band: the composition changed.

## GAAP against non-GAAP

Non-GAAP operating income was **$550.3M (23.2% margin)** against GAAP $377.9M. The $172.4M gap
reconciles exactly (source: d176836dex991.htm):

| | $M |
|---|---|
| Share-based compensation | 73.2 |
| Amortization of acquired intangibles | 69.5 |
| Restructuring charges | 8.6 |
| Integration, site consolidation and other | 21.2 |
| **Total** | **172.4** |

Acquired-intangible amortization is the largest single piece after stock compensation and will
recur until the intangibles are fully amortized — it was $69.5M in this quarter and $69.5M a year
ago.

## Tax was a benefit, and net earnings have two versions

Income tax was a **$22.8M benefit**, so on the Sankey it flows *into* net profit rather than out
of it. The same thing happened at [[qualcomm-fq4-fy26]] in the same week, for unrelated reasons.

Two net figures appear in the release and the card uses the first:

- **$381.6M** — consolidated net earnings, which is what the statement foots to and what the
  chart draws
- **$384.7M** — net earnings attributable to Coherent Corp., after adding back a $3.1M loss
  attributable to non-controlling interests. A year ago a further $33.5M of preferred dividends
  sat below that line; this quarter there are none.

## What this card does not carry

- **The debt chart still shows FQ4 FY26.** The vendor has no September 30, 2026 balance sheet
  column, so `bin/debtfetch.py` skipped the quarter rather than matching one 92 days away.
  Coherent's own balance sheet gives **$4,000.6M of debt** ($19.9M current portion, $3,980.7M
  long-term) against $1,552.9M of cash and equivalents, $200.0M of short-term investments and
  $44.6M of restricted cash at September 30, 2026 — against $3,222.2M of debt and $1,162.0M of
  cash at June 30, 2026. Both debt and cash rose over the quarter.
- **The earnings chart's Sep '26 column has no actual.** Coherent reported hours before this page
  was written and the vendor has not posted its figure. The consensus shown is $1.78.
- **P/E and dividend** are measured against the share price as of November 4, 2026 and move every
  session. Coherent pays no dividend.

## Guidance

FQ2 FY27: revenue **$2.55B–$2.75B**, non-GAAP gross margin 40%–42%, total operating expenses
$430M–$450M, a non-GAAP tax rate of 18%–20% and non-GAAP EPS of $2.28–$2.48.

Coherent also published targets beyond the quarter: a first **$3 billion revenue quarter by the
end of fiscal 2027**, fiscal 2027 pro forma revenue growth above 60%, a first $4 billion quarter
in fiscal 2028, and a new gross margin target of a first quarter above **45% non-GAAP before the
end of calendar 2028**.

## Related pages
- [[sankey-income-statement]]
- [[favorites-financials]]
- [[qualcomm-fq4-fy26]]
- [[ouster-q3-fy26]]
- [[earnings-surprise-chart]]
- [[share-ownership-donut]]
