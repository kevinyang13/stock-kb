# Hut 8 Q3 FY26

**Summary**: Hut 8's third quarter 2026 (quarter ended September 30, 2026): $71.1M of revenue, **down 15% year over year**, and net income of $189.5M, of which $131.1M is attributable to Hut 8 Corp. The profit is not an operating result — $413.8M of mostly unrealized gains on digital assets sits *inside* operating expenses as a credit. **The Financials card still shows Q2 FY26 because this quarter cannot be drawn by the current renderer.**

**Sources**: Hut 8 8-K exhibit 99.1, Q3 2026 results, filed November 4, 2026 (source: tm2628741d1_ex99-1.htm). Prior-period figures are the September 30, 2025 column of the same release.

**Last updated**: 2026-11-04

---

## Why there is no chart for this quarter

The Sankey in `bin/sankey.py` draws revenue flowing into gross profit, and gross profit flowing
into operating profit and operating expenses. That requires operating profit to be **less than**
gross profit, because operating expenses are a positive outflow.

For Hut 8's third quarter it is not:

| | $M |
|---|---|
| Gross profit (revenue less cost of revenue) | 40.8 |
| **Operating income** | **318.2** |

Operating income is nearly eight times gross profit, because the operating-expense block nets to
**negative $277.4M**: a $413.8M gain on digital assets and a $3.3M gain on asset sales outweigh
$40.1M of depreciation and amortization and $99.6M of general and administrative expense. There
is no way to draw a negative expense band, and the link would simply vanish, leaving a chart
whose inflows and outflows do not match.

Moving the gain below the operating line would make it drawable in principle, but then operating
income becomes a **$95.6M loss** against positive net income — which is the same shape that
blocks the MSTR Q3 FY26 card, and is a second unsupported case rather than a workaround. It would
also contradict the filing's own presentation.

So the card keeps the Q2 FY26 chart and carries a note saying what the Q3 figures are and why
they are not drawn. The alternative — a chart that silently fails to conserve — is worse than an
openly stale one.

## Income statement

Three months ended September 30, in thousands of USD (source: tm2628741d1_ex99-1.htm).

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| Power | 1,259 | 8,367 | −85% |
| Digital Infrastructure | 1,384 | 5,107 | −73% |
| Compute | 68,428 | 70,036 | −2% |
| **Total revenue** | **71,071** | **83,510** | **−15%** |
| Cost of revenue — Power | (757) | (6,494) | −88% |
| Cost of revenue — Digital Infrastructure | (1,437) | (3,804) | −62% |
| Cost of revenue — Compute | (28,031) | (22,032) | +27% |
| **Total cost of revenue** (exclusive of D&A) | **(30,225)** | **(32,330)** | −7% |
| Depreciation and amortization | (40,146) | (27,795) | +44% |
| General and administrative | (99,555) | (25,858) | **+285%** |
| Gain on digital assets | 413,789 | 76,595 | +440% |
| Gain (loss) on sale of property and equipment | 3,273 | (1,467) | n/m |
| **Operating expenses (income), net** | **277,361** | **21,475** | n/m |
| **Operating income** | **318,207** | **72,655** | **+338%** |
| Foreign exchange gain (loss) | 392 | (1,530) | n/m |
| Interest expense | (105,512) | (8,616) | **+1,125%** |
| Interest income | 61,769 | — | n/m |
| (Loss) gain on derivatives and other financial liabilities | (62,750) | 4,930 | n/m |
| Gain on other investments | 23,686 | — | n/m |
| Equity in earnings of unconsolidated joint venture | 5,365 | 2,192 | +145% |
| **Total other expenses** | **(77,050)** | **(3,024)** | n/m |
| **Income before income taxes** | **241,157** | **69,631** | +246% |
| Income tax provision | (51,663) | (19,019) | +172% |
| **Net income** | **189,494** | **50,612** | **+274%** |
| Less: net income attributable to non-controlling interests | (58,423) | (503) | n/m |
| **Net income attributable to Hut 8 Corp.** | **131,071** | **50,109** | **+162%** |

## The gross margin is 57% only because D&A sits below it

Cost of revenue is reported **exclusive of depreciation and amortization**, which is shown
separately in operating expenses. On that basis gross profit is $40.8M and gross margin 57.5%.
Put the $40.1M of D&A back above the line and gross profit is **$0.7M — a 1.0% margin**.

This is the same trap [[iren-fq4-fy26]] carries, and it is why the existing Hut 8 card's 64%
gross margin should never be compared with a card whose cost of revenue includes depreciation.
For a business whose capital is the asset, the exclusive-of-D&A margin describes very little.

## Revenue fell, and two of three lines nearly disappeared

Power revenue fell 85% and Digital Infrastructure 73%, on cost lines that fell by similar
proportions — these look like businesses being wound down or reclassified rather than lost.
Compute, 96% of revenue, fell 2% while its cost of revenue rose 27%, so Compute's own gross
margin went from 69% to 59%.

Meanwhile **general and administrative expense nearly quadrupled**, from $25.9M to $99.6M, which
is 140% of total revenue.

## The profit is a mark, and so is much of what offsets it

| | $M |
|---|---|
| Gain on digital assets (mostly unrealized) | +413.8 |
| Interest expense | −105.5 |
| Loss on derivatives and other financial liabilities | −62.8 |
| Income tax provision | −51.7 |
| Non-controlling interests | −58.4 |
| **Everything else, net** | **−4.3** |
| **Net income attributable to Hut 8 Corp.** | **131.1** |

Interest expense went from $8.6M to $105.5M in a year — a twelvefold increase that reflects the
debt raised to build the campuses, and the single largest recurring charge on the statement.
Against that, interest income of $61.8M appears where there was none.

Hut 8's own Adjusted EBITDA, which from the June quarter **excludes** digital-asset
mark-to-market, was **$33.0M against $30.5M** a year ago. Including the mark it was $350.3M
against $109.0M. The gap between those two numbers is the whole question about this quarter.

## Capital and pipeline

- Repurchased 953,802 shares for $74.7M in the quarter, funded by selling roughly 954 Bitcoin;
  a further 2,384,677 shares for $175.3M after quarter end, completing the original $250.0M
  programme. The board raised the authorization to **$1.0 billion** on November 2, 2026.
- Terminated the undrawn $200.0M Two Prime credit facility and, after quarter end, repaid the
  $26.5M TZRC secured promissory note in full.
- Development pipeline of approximately **7,859 MW**, including 1,330 MW under construction and
  49 MW under development.

## What the card carries meanwhile

The Q2 FY26 chart, its Q2 FY26 debt bars, and an earnings chart whose Sep '26 column shows the
$(1.17) consensus with a "reported, awaiting vendor" caret — Hut 8 reported hours before this
page was written. The card's note states the Q3 figures and points here.

## Related pages
- [[sankey-income-statement]]
- [[favorites-financials]]
- [[iren-fq4-fy26]]
- [[earnings-surprise-chart]]
- [[share-ownership-donut]]
