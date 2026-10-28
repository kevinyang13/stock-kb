# Watchlist Financials

**Summary**: The Financials tab carries an income statement chart for every name in the watchlist that files one — 67 statements, each the company's most recent reported quarter, plus Nintendo.

**Sources**: stockanalysis.com quarterly income statement pages for most names; Micron's Form 8-K, CoreWeave's results release and Nebius's 6-K exhibit 99.1 for those three.

**Last updated**: 2026-10-26

---

## Coverage

Of the 101 names on the watchlist:

| | Count | Why |
|---|---|---|
| Charted | 65 | files an income statement |
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

## Nebius: the second source disagreement, and a segment split

NBIS joined the watchlist on 2026-10-26 and its Q2 FY26 chart was built from the **6-K exhibit
99.1**, not the aggregator. stockanalysis.com reports operating income of **−$1.3M**; the filing
reports a loss from operations of **−$175.9M**. The gap is roughly $174.6M the aggregator moves out
of product development and SG&A. What that reclassification consists of has **not** been
established — share-based compensation was $102.5M that quarter, under 60% of the gap. Revenue, gross profit, net loss and EPS agree on both sources.

That makes two names where the aggregator's operating income does not match the filing — Meta above
and Nebius here. Both times the filing was right and the aggregator's number looked too clean.

Nebius does carry a reported segment split, so it is charted with three revenue bars rather than
one. The $3.6M of intersegment eliminations is netted against the AI cloud bar so the three foot to
revenue; the reported segment figure is $574.9M. Full detail in [[nebius-q2-fy26]].

## Caveats that apply to these charts

**Two of the six KPI tiles are not from the filing.** P/E and dividend are measured against
today's share price, so they move every session while the other four never change. `bin/pefetch.py`
writes them from stockanalysis.com's quote data and stamps the date on the card note and on
`marketAsOf` in `financials.json`; re-run it whenever the figures look stale.

A loss-maker has no meaningful trailing P/E and a company with no positive forward estimate has no
forward one — both read `n/a` rather than a negative number, since a negative P/E is not a cheap
stock, just a loss. 25 of the 67 pay a dividend; the rest read "None", which is a fact about the
company, not a gap in the data.


**Segment splits are now required for new charts** — see [[sankey-income-statement]] and the
`income-statement-chart` skill. The backlog left by the bulk watchlist pass has been filled in:
**53 of the 67 charts now carry a reported split**, and the 14 that do not each say on the card why.
Visa is the only one of those 14 whose split exists but cannot be drawn: its categories are gross of
client incentives and sum to a total it never reports — see [[visa-q4-fy26]].

Those 13 are ARQQ, ASTS, CLSK, CRWV, DDOG, HUT, INFQ, NET, NU, OUST, SKHY, SMCI and XNDU. Most
report one segment and disclose revenue by geography only. Two are worth naming:

- **HUT** does report three segments — Compute $72.5M, Digital Infrastructure $33.0M, Power $5.5M —
  but intersegment eliminations are $36.0M against $74.9M of revenue, so the three cannot be drawn
  as bars that foot. The card gives the gross figures instead.
- **NU** is charted on the aggregator's net revenue line, which no reported split adds up to.

**IONQ was previously recorded here as publishing no split. That was wrong** — its 10-Q
disaggregates revenue into quantum hardware and platform/consulting/support, $46.5M and $33.6M for
Q2 FY26, and the chart now shows both. SMCI and CRWV were checked again and do hold: Supermicro's
FY26 10-K gives net sales by geography only, and CoreWeave the same.

**Nine of the original twelve carry a reported segment split**: NVDA, MSFT, GOOG, MU, SNDK, TSM, TSLA, QCOM and INTU.

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
- [[nebius-q2-fy26]]
