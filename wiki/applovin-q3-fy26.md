# AppLovin Q3 FY26

**Summary**: AppLovin's third quarter 2026 (quarter ended September 30, 2026): $2,184.8M of revenue, up 55% year over year, an 89.0% gross margin, $1,709.0M of operating income and $1,438.9M of net income. Operating margin 78% and net margin 66% are the highest of the 77 cards on the Financials tab. The company now files a single reportable segment -- the Apps business that was the second one was sold to Tripledot on June 30, 2025.

**Sources**: AppLovin 10-Q for the quarter ended September 30, 2026, filed November 4, 2026 (source: accession 0001751008-26-000069) -- the condensed consolidated statements of operations, the condensed consolidated balance sheets, the discontinued operations note and the segment note. Quarterly free cash flow and the market figures are stockanalysis.com's, read November 11, 2026.

**Last updated**: 2026-11-11

---

## Income statement

Three months ended September 30, in thousands of USD (source: 10-Q, condensed consolidated
statements of operations).

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| **Revenue** | **2,184,815** | **1,405,045** | **+55%** |
| Cost of revenue | (240,765) | (174,855) | +38% |
| **Gross profit** (derived) | **1,944,050** | **1,230,190** | **+58%** |
| Research and development | (101,817) | (43,852) | **+132%** |
| Sales and marketing | (68,803) | (48,575) | +42% |
| General and administrative | (64,462) | (58,756) | +10% |
| **Total operating expenses** | **(235,082)** | **(151,183)** | **+56%** |
| **Income from operations** | **1,708,968** | **1,079,007** | **+58%** |
| Interest expense | (51,066) | (51,429) | -1% |
| Other income (expense), net | 86,032 | (6,632) | n/m |
| **Total other income (expense), net** | **34,966** | **(58,061)** | n/m |
| **Income before income taxes** | **1,743,934** | **1,020,946** | **+71%** |
| Provision for income taxes | (305,032) | (185,401) | +65% |
| **Net income from continuing operations** | **1,438,902** | **835,545** | **+72%** |
| Loss from discontinued operations | 0 | 0 | -- |
| **Net income** | **1,438,902** | **835,545** | **+72%** |

Diluted EPS $4.30 against $2.45, on 334.8M diluted shares against 341.0M -- the share count is
1.8% lower year over year, so EPS grew faster than net income.

**The filing publishes no gross profit line.** Cost of revenue is filed; gross profit on the chart
is revenue less cost of revenue, which is the convention [[sankey-income-statement]] uses on every
card. Operating expenses are drawn as the filing's own three lines rather than as one SG&A band,
the same treatment as [[datadog-q3-fy26]].

## One segment, because the other one was sold

AppLovin reports **one operating segment and one reportable segment** (source: 10-Q, segment
note). The chart's single "Advertising" bar is therefore a filed fact, not a gap -- the distinction
[[sankey-income-statement]] insists on, and the opposite of a card whose split was simply never
fetched.

The second segment is gone rather than missing. On **June 30, 2025** AppLovin completed the sale of
the subsidiaries operating its Apps business to Tripledot for **$715.6M** -- $430.6M of cash and
596.9M Tripledot ordinary shares valued at $285.0M, about 22% of Tripledot, carried as an equity
method investment. The company derecognised $591.2M of net assets and booked a $106.2M pre-tax gain
after $18.3M of transaction costs (source: 10-Q, discontinued operations note).

Everything the Apps business did now sits in discontinued operations, including a $188.9M goodwill
impairment and the $99.4M nine-month loss in the 2025 comparative. **Both columns of the table
above are continuing operations**, so the +55% revenue growth is like for like.

## What the segment note discloses instead of a split

A single-segment filer still has to disclose its significant expense categories. AppLovin's, for
the quarter (source: 10-Q, schedule of segment reporting information, in thousands):

| | Q3 FY26 | Q3 FY25 |
|---|---|---|
| Revenue | 2,184,815 | 1,405,045 |
| Datacenter costs | (194,630) | (141,046) |
| Personnel-related expenses | (52,996) | (50,011) |
| Stock-based compensation | (84,165) | (33,767) |
| Amortization, depreciation and write-offs | (34,190) | (34,978) |
| Interest expense | (51,066) | (51,429) |
| Other expenses | (23,834) | (72,868) |
| Provision for income taxes | (305,032) | (185,401) |
| **Net income from continuing operations** | **1,438,902** | **835,545** |

**Datacenter cost is the business's one real variable cost**: $194.6M, 81% of the $240.8M cost of
revenue and 8.9% of revenue. It grew 38% against revenue's 55%, which is the whole of the
gross-margin expansion -- 87.6% a year ago to 89.0% now. The same inference-cost question the
[[ai-data-center-buildout]] page tracks from the supply side shows up here as a cost line that
grows slower than the revenue it serves.

Stock-based compensation is **$84.2M, 3.9% of revenue**, and it more than doubled.

## Margins

| Margin | Q3 FY26 | Q3 FY25 |
|---|---|---|
| Gross | 89.0% | 87.6% |
| Operating | 78.2% | 76.8% |
| **Net** | **65.9%** | **59.5%** |

Unlike [[datadog-q3-fy26]] or [[alphabet-q3-fy26]], the net margin here is **not** flattered by a
non-operating item: the $35.0M between operating and pretax profit is 1.6% of revenue, and the
17.5% effective tax rate is low but unremarkable. The 78% operating margin is the business.

R&D more than doubled, $101.8M against $43.9M, and is now the largest operating expense. Sales and
marketing is **$68.8M on $2,184.8M of revenue -- 3.1%**, which is what a model-driven ad network
looks like next to a sales-led software company: [[datadog-q3-fy26]] spends 25% of revenue on the
same line.

## Balance sheet

Long-term debt **$3,516.1M** against cash and equivalents of **$3,173.7M** -- net debt $342.4M
(source: 10-Q, condensed consolidated balance sheets). Both figures are the filing's own. Free cash
flow of $1,428.8M for the quarter is stockanalysis's quarterly derivation, because the 10-Q's cash
flow statement is cumulative for the nine months; one quarter of it covers four times the net debt.

Interest expense has been flat near $51M a quarter for five quarters, so the debt is fixed-rate and
untouched.

## What this card does not carry

- **No earnings chart.** `bin/epsfetch.py` returned HTTP 403 for every ticker on November 11, 2026,
  not just this one -- the Nasdaq surprise and consensus endpoints were refusing this host. Nothing
  was written rather than hand-filled. See [[earnings-surprise-chart]].
- **No ownership donut.** That needs an unpacked SEC Form 13F data set, which is deliberately not in
  the repository. See [[share-ownership-donut]].
- **P/E** is measured against the share price as of November 11, 2026 and moves every session: 27.1
  trailing, 20.6 forward, on a $134.11B market cap. AppLovin pays no dividend.

## Related pages
- [[sankey-income-statement]]
- [[datadog-q3-fy26]]
- [[alphabet-q3-fy26]]
- [[ai-data-center-buildout]]
- [[earnings-surprise-chart]]
- [[share-ownership-donut]]
