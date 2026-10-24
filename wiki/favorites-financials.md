# Watchlist Financials

**Summary**: The Financials tab carries an income statement chart for every name in the watchlist that files one — 65 statements, each the company's most recent reported quarter, plus Nintendo.

**Sources**: stockanalysis.com quarterly income statement pages for most names; Micron's Form 8-K and CoreWeave's results release for those two.

**Last updated**: 2026-10-22

---

## Coverage

Of the 100 names on the watchlist:

| | Count | Why |
|---|---|---|
| Charted | 64 | files an income statement |
| ETFs and funds | 25 | a fund holds securities; it has no revenue or margin |
| Shells / no usable filing | 6 | CLBR, CCXI, BITF, BCII, MFH, XNET |
| Excluded, negative gross profit | 3 | SPCE, QUBT, CAN — cost of revenue exceeds revenue, so there is no flow to draw |
| Excluded, pre-revenue | 1 | HQ reports no revenue line at all |

Nintendo is charted too, though it is not on the watchlist.

## The original fourteen

| Ticker | Quarter | Period end | Layout |
|---|---|---|---|
| NVDA | Q2 FY27 | Jul 26, 2026 | profit |
| QCOM | FQ3 FY26 | Jun 28, 2026 | profit |
| GOOG | Q2 FY26 | Jun 30, 2026 | profit |
| MU | FQ4 FY26 | Sep 3, 2026 | profit |
| SNDK | FQ4 FY26 | Jul 3, 2026 | profit |
| TSM | Q3 FY26 | Sep 30, 2026 | profit (NT$) |
| TSLA | Q3 FY26 | Sep 30, 2026 | profit |
| INTU | FQ4 FY26 | Jul 31, 2026 | profit |
| SMCI | FQ4 FY26 | Jun 30, 2026 | profit |
| IONQ | Q2 FY26 | Jun 30, 2026 | loss |
| MSFT | FQ4 FY26 | Jun 30, 2026 | profit |
| META | Q3 FY26 | Sep 30, 2026 | profit |
| SPCX | Q3 FY26 | Sep 30, 2026 | profit (tax benefit) |
| CRWV | Q2 FY26 | Jun 30, 2026 | loss |

## SMH has no income statement

SMH is the VanEck Semiconductor ETF. A fund holds securities; it does not sell anything, so there is no revenue, no cost of revenue and no margin to chart. It stays on the heatmap and in the brief, but it cannot appear here.

## Meta's operating income does not match stockanalysis

Meta's Q3 FY26 chart uses the filed figure of **$12,988M**. stockanalysis.com reports operating income of **$22,878M** for the same quarter, because it places a $9,890M operating charge below the operating line. Revenue less cost of revenue less R&D, marketing/G&A and that charge gives $12,988M, which is what the 8-K reports as income from operations. The chart follows the filing.

This is the first case where the two sources disagree on a headline line, not just on rounding. Worth checking the filing rather than the aggregator whenever operating income looks too clean.

## Caveats that apply to these charts

**Nine of the twelve now carry a reported segment split**: NVDA, MSFT, GOOG, MU, SNDK, TSM, TSLA, QCOM and INTU. Three do not — SMCI (Supermicro's release does not split server/storage systems from subsystems), IONQ and CRWV (both report a single revenue line) — and those show one revenue bar.

Each split was validated against the revenue total before use. Four footed exactly (MSFT, GOOG, QCOM, SNDK); TSLA is out by $44M on $28.0B and TSM by NT$0.1B, both rounding. Two segment values are **derived rather than reported**: TSMC publishes platform mix only as rounded percentages, which the chart applies to revenue, and Intuit's Global Business Solutions is shown as the remainder so its two segments foot.

Note that stockanalysis.com's `revenue-by-segment` page is **not** usable for this — its figures are annual even under `?p=quarterly`, and NVDA's two segments there sum to $303B against $96.2B of quarterly revenue. Segments came from each company's own release instead.

**Quarters are not aligned.** Fiscal calendars differ — NVDA's Q2 FY27 ended in July, MU's FQ4 FY26 in September, TSLA's Q3 in September. Comparing margins across the charts is fair; comparing "the same quarter" is not.

**TSMC is in New Taiwan dollars**, as filed. Its margins are comparable with the rest; its absolute figures are not.

**Alphabet's 94% net margin is not an operating result.** A $99.0B gain on sale of investments sits in the interest and other line. Operating margin was 34%.

**Other income is derived**, as pretax income minus operating income, rather than taken as a reported line. This makes every statement foot exactly, but it bundles interest, investment gains and any other non-operating items into one figure.

**IonQ's tax line was a benefit**, not an expense. The loss layout cannot draw a negative cost, so it is folded into the non-operating line and the label says "Non-operating & tax, net".

## Related pages

- [[sankey-income-statement]]
- [[micron-fq4-fy26]]
- [[coreweave-q2-fy26]]
