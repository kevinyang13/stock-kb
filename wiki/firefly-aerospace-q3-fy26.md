# Firefly Aerospace Q3 FY26

**Summary**: Firefly's third quarter 2026 (quarter ended September 30, 2026): revenue almost quadrupled to $110.7M, gross margin slipped to 23%, and the operating loss widened to $101.6M on R&D and SG&A that grew faster than revenue. Backlog reached a record $1.7B.

**Sources**: Firefly Aerospace Form 8-K exhibit 99.1, results for the quarter ended September 30, 2026, filed November 10, 2026 (source: sec.gov, accession 0001860160-26-000030) — condensed consolidated statements of net loss and comprehensive loss. Market figures from stockanalysis.com, November 10, 2026.

**Last updated**: 2026-11-10

---

## Income statement

Three months ended September 30, in thousands of US dollars.

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| **Revenue** | **110,682** | **30,778** | **+259.6%** |
| Cost of sales | (85,385) | (22,288) | +283% |
| **Gross profit** | **25,297** | **8,490** | +198% |
| Research and development | (75,991) | (48,763) | +56% |
| Selling, general, and administrative | (50,884) | (21,920) | +132% |
| **Total operating expenses** | **(126,875)** | **(70,683)** | +79% |
| **Loss from operations** | **(101,578)** | **(62,193)** | worse |
| Change in fair value of warrant liability | 4,040 | **(42,150)** | n/m |
| Loss on extinguishment of debt | — | **(30,400)** | n/m |
| Interest income | 4,460 | 5,289 | −16% |
| Interest expense | (1,637) | (3,955) | −59% |
| Other income (expense), net | 559 | (3) | n/m |
| **Total other income (expense), net** | **7,422** | **(71,219)** | n/m |
| **Loss before income taxes** | **(94,156)** | **(133,412)** | — |
| Provision for income taxes | (42) | — | n/m |
| **Net loss** | **(94,198)** | **(133,412)** | — |

Loss per share $(0.56), basic and diluted, on 168,371,000 weighted-average shares.

Nine months to September 30, 2026: revenue $309.2M against $102.2M, net loss $283.2M against
$257.3M.

## Revenue nearly quadrupled; gross profit did not keep up

Revenue grew **260%** and gross profit **198%**, so the gross margin fell from 27.6% to
**22.9%**. Cost of sales grew faster than revenue — 283% against 260%.

For a company scaling spacecraft manufacturing that is unremarkable in one quarter and worth
watching across several. The Q2 FY26 card showed a 20% margin on $118M of revenue; this
quarter is 23% on $110.7M, so the trend over two quarters is up, not down, even as the
year-over-year comparison falls.

## The smaller net loss hides a wider operating loss

| | Q3 FY25 | Q3 FY26 |
|---|---|---|
| Operating loss | $(62.2)M | **$(101.6)M** |
| Warrant fair value change | $(42.2)M charge | $4.0M gain |
| Loss on extinguishment of debt | $(30.4)M | — |
| Net loss | $(133.4)M | $(94.2)M |

The net loss improved by $39.2M. The year-ago quarter carried $72.6M of one-off below-the-line
charges that are simply absent this time. **The operating loss widened by $39.4M** — R&D rose
to $76.0M from $48.8M and SG&A to $50.9M from $21.9M, the latter up 132% against revenue up
260%.

Three of the four companies that reported on November 10 and are charted here share this
shape: a net line flattered by the disappearance of a prior-year warrant charge, over an
operating line that got worse. The others are [[rigetti-q3-fy26]] and
[[d-wave-quantum-q3-fy26]].

## Backlog and the quarter's operating news

- **Record backlog of $1.7B** at quarter end, up from $1.5B at the end of Q2.
- Spacecraft cleanroom expansion completed and in operation, funded by a Texas Space Commission
  grant; it allows simultaneous assembly of up to 12 lunar landers and orbital vehicles.
- First European launch contracts signed; Alpha Block II manufacturing ramping.
- Onboarded to NASA's Spacecraft Processing Operations Contract.
- Five Moon missions running in parallel, and a strategic agreement with AST SpaceMobile — see
  [[ast-spacemobile-q3-fy26]], which reported the day before.

## No segment split on this card, and the reason is timing

The Q2 FY26 card split revenue into spacecraft solutions $108.3M and launch services $9.4M,
taken from that quarter's 10-Q. **This card has none, because the Q3 10-Q has not been filed**
— the figures here are from the Form 8-K. The split goes on when the 10-Q lands.

## A renderer note

This is the second card to need the per-spec label overrides added to `bin/sankey.py` on
November 9 for Rocket Lab. Firefly's cost-of-revenue bar is 67% of the chart's tallest column,
and both the "Cost of revenue" and "Net loss" labels landed on it. The spec carries
`cor_label` and `loss_label` offsets; the defaults are unchanged for every other card.

Two cards hitting the same clash in two days suggests the offsets should be computed from the
settled node height rather than nudged per card — see [[sankey-income-statement]].

## What this card does not have

- **No debt chart.** The vendor has no September 30, 2026 balance-sheet column yet; the nearest
  is June 30, 92 days away. `bin/debtfetch.py` reported and skipped.
- **No post-result EPS surprise.** The vendor's earnings endpoint returned HTTP 403 on the
  refresh, so the Sep '26 point is still the pre-announcement consensus of $(0.60).

## Related pages
- [[favorites-financials]]
- [[rigetti-q3-fy26]]
- [[d-wave-quantum-q3-fy26]]
- [[ast-spacemobile-q3-fy26]]
