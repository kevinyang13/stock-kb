# Centrus Energy Q3 FY26

**Summary**: Centrus Energy's third quarter 2026 (quarter ended September 30, 2026): $55.5M of revenue, down 26% year over year, a **gross loss of $10.6M**, and GAAP net income of $31.6M that comes entirely from a $46.4M gain on remeasuring warrant liabilities. The gross loss is why Centrus has **no Financials card** — it is the one gate in [[sankey-income-statement]] that nothing can work around.

**Sources**: Centrus Energy 8-K exhibit 99.1, third quarter 2026 results, filed November 4, 2026 (source: ex991-10q2026_11x04.htm). Prior-period figures are the three months ended September 30, 2025 as quoted in the same release.

**Last updated**: 2026-11-04

---

## Why there is no chart

`bin/sankey.py` draws revenue splitting into gross profit and cost of revenue. When cost of
revenue exceeds revenue there is no gross profit to split out, and the chart would have to draw a
negative band. The skill's chartable gate names this case directly — alongside SPCE, QUBT and CAN
— and the answer is to say so rather than to force a layout.

Full statement, in millions of USD (source: ex991-10q2026_11x04.htm):

| Line | Q3 FY26 | Q3 FY25 | 9M FY26 | 9M FY25 |
|---|---|---|---|---|
| Separative work units | 14.1 | 10.7 | 155.7 | 187.7 |
| Uranium | 17.7 | 34.1 | 74.1 | 34.1 |
| Technical solutions | 23.7 | 30.1 | 78.5 | 80.7 |
| **Total revenue** | **55.5** | **74.9** | **308.3** | **302.5** |
| Cost of sales — SWU and uranium | (38.7) | (52.6) | (157.2) | (147.7) |
| Cost of sales — technical solutions | (27.4) | (26.6) | (80.3) | (72.3) |
| **Gross (loss) profit** | **(10.6)** | **(4.3)** | **70.8** | **82.5** |
| Advanced technology costs | (4.7) | (1.7) | (34.4) | (8.0) |
| Selling, general and administrative | (13.2) | (9.5) | (49.4) | (31.2) |
| Amortization of intangible assets | (1.2) | (1.1) | (5.5) | (5.9) |
| **Operating (loss) income** | **(29.7)** | **(16.6)** | **(18.5)** | **37.4** |
| Gain on change in fair value of warrant liability | 46.4 | — | 46.4 | — |
| Investment income | 16.9 | 12.9 | 50.2 | 28.2 |
| Interest expense | (3.9) | (3.4) | (12.1) | (9.9) |
| Nonoperating pension components | (1.0) | (1.0) | (3.0) | (2.9) |
| **Income (loss) before income taxes** | **28.7** | **(8.0)** | **62.8** | **64.6** |
| Income tax benefit (expense) | 2.9 | 11.9 | (4.4) | (4.6) |
| **Net income** | **31.6** | **3.9** | **58.4** | **60.0** |

Both quarters needed something below the operating line to reach net income. This year it is the
warrant gain; a year ago the quarter was a **$8.0M pretax loss** turned into $3.9M of net income
by an $11.9M tax benefit.

**The gross loss is a quarterly artefact, not an annual one.** Over nine months Centrus is gross
*profitable* — $70.8M on $308.3M of revenue, a 23% margin. Centrus says its LEU customers carry
annual rather than quarterly purchase commitments, so the gross result swings with which
contracts happen to deliver in a given three months. The chartable gate is applied to the quarter
a card would draw, so the quarter is what blocks it; an annual card would not be blocked.

The gross loss **widened 147%** year over year while revenue fell 26%. Centrus is on the heatmap
([[index]] records the October 28, 2026 addition of the power and nuclear-fuel names) and on the
events calendar; its chip is plain text rather than a link, which is the honest behaviour for a
ticker with no card.

## Revenue by segment

| Segment | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| LEU | 31.8 | 44.8 | −29% |
| Technical Solutions | 23.7 | 30.1 | −21% |
| **Total** | **55.5** | **74.9** | **−26%** |

Within LEU, the decline is uranium, not enrichment: **uranium revenue fell $16.4M** on lower
volume, while **SWU revenue rose $3.4M** on 19% more units sold at a 10% higher average price.
That is a better mix than the headline suggests — enrichment, the business Centrus is building
for, grew.

Both segments lost money at the gross line:

| Segment gross result | Q3 FY26 | Q3 FY25 |
|---|---|---|
| LEU | (6.9) | (7.8) |
| Technical Solutions | (3.7) | 3.5 |

The LEU gross loss narrowed. Technical Solutions went from a $3.5M profit to a $3.7M loss, which
Centrus attributes to the HALEU Operation Contract with the Department of Energy.

## Net income of $31.6M is a warrant mark

Centrus is explicit about the bridge (source: ex991-10q2026_11x04.htm). Net income rose $27.7M
year over year, driven by:

| | $M |
|---|---|
| Gain on fair value adjustment of warrant liabilities | +46.4 |
| Higher investment income | +4.0 |
| Lower income tax benefit | −9.0 |
| Larger gross loss | −6.3 |
| Higher SG&A | −3.7 |
| Higher advanced technology costs | −3.0 |

GAAP EPS was $1.53 basic and $1.41 diluted. Centrus's own **non-GAAP adjusted figure is a net
loss of $9.4M**, or $(0.46) per share, against adjusted net income of $5.2M a year ago — so the
adjusted and GAAP lines point in opposite directions, and the adjusted one is the one that tracks
the operations.

A warrant-liability remeasurement driving GAAP net income is the same mechanic as AMD's $1,097M
warrant charge in [[amd-q3-fy26]], running the other way.

## Backlog, and the part of it the DOE has signalled it will not fund

Total backlog is **$7.0 billion** at September 30, 2026, extending to 2040:

- **LEU segment $6.2B**, including roughly $5.4B of *contingent* LEU and HALEU sales commitments
  tied to building production capacity at Piketon, Ohio — $5.1B of that under definitive
  agreements. Contingent means tied to operational milestones, not firm orders.
- **Technical Solutions $0.8B**, funded and unfunded amounts plus unexercised options.

The release states plainly that **the proposed DOE fiscal 2027 budget does not fund further
operation of the HALEU cascade** under the HALEU Operation Contract — approximately $0.8 billion
of the Technical Solutions backlog — and that DOE has communicated it does not currently intend
to exercise further options under that contract. Technical Solutions backlog and the contract
behind this quarter's segment loss are substantially the same thing.

## Operational milestones and outlook

Centrus reports three things delivered ahead of its year-end target: completed manufacturing and
began shipping centrifuges from Oak Ridge, finalised contracts with all supply chain deemed
critical, and completed the first certified-for-construction package. It also closed the
acquisition of Westerman.

Full-year 2026 guidance: **revenue $450M–$500M** and total capital deployment of $350M–$500M.
Operationally, at least 100 net new hires at Oak Ridge and at least 175 at Piketon, raised from
100.

Nine-month revenue is **$308.3M**, so the $450M–$500M full-year range implies a fourth quarter of
**$141.7M–$191.7M** — between two and a half and three and a half times the $55.5M just reported.
The guidance was reaffirmed in this release rather than revised, so the lumpiness of the LEU
delivery schedule is doing that work.

## Related pages
- [[sankey-income-statement]]
- [[favorites-financials]]
- [[amd-q3-fy26]]
- [[index]]
