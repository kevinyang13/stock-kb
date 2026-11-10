# CoreWeave Q3 FY26

**Summary**: CoreWeave's third quarter 2026 (quarter ended September 30, 2026): $3,661M of revenue, up 168% year over year, and the first positive operating quarter the Financials card has shown — $207M of operating income on a 6% margin. The $709M net loss is financing: interest expense, net was $846M.

**Sources**: CoreWeave Form 8-K exhibit 99.1, results for the quarter ended September 30, 2026, filed November 10, 2026 (source: sec.gov, accession 0001769628-26-000461) — consolidated statements of operations and the non-GAAP reconciliations. Market figures from stockanalysis.com, November 10, 2026.

**Last updated**: 2026-11-10

---

## Income statement

Three months ended September 30, in millions of US dollars, as the company reports them.

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| **Revenue** | **3,661** | **1,365** | **+168.2%** |
| Cost of revenue | (1,183) | (369) | +221% |
| **Gross profit (derived)** | **2,478** | **996** | +149% |
| Technology and infrastructure | (2,025) | (747) | +171% |
| Sales and marketing | (58) | (45) | +29% |
| General and administrative | (188) | (152) | +24% |
| **Total operating expenses** | **(3,454)** | **(1,313)** | +163% |
| **Operating income** | **207** | **52** | +298% |
| Interest expense, net | (846) | (310) | +173% |
| Other income, net | 13 | 21 | −38% |
| **Loss before income taxes** | **(626)** | **(237)** | worse |
| Provision for (benefit from) income taxes | (83) | 127 | n/m |
| **Net loss** | **(709)** | **(110)** | worse |

Diluted loss per share $(1.27) on 559 million weighted-average shares.

Nine months to September 30, 2026: revenue $8,314M against $3,559M, operating income $14M
against $44M, net loss $2,075M against $715M.

## Gross profit here is derived, and the margin is not comparable

CoreWeave publishes **no gross profit line**. Cost of revenue is one of four items inside
total operating expenses of $3,454M. The $2,478M of gross profit and the 68% margin on the
card and in the table above are revenue less cost of revenue, computed here, not reported
(source: 8-K exhibit 99.1, November 10, 2026).

That matters more than the usual derivation caveat, because of where the fleet cost sits.
**Technology and infrastructure was $2,025M, 55% of revenue** — the cost of running the data
centres. It is outside cost of revenue. Counted above the line, the gross margin would be
**12%**, not 68%.

This is the same shape as IREN's "cost of revenue exclusive of D&A", noted in
[[favorites-financials]]: a gross margin that is arithmetically correct and not comparable
with the other cards. Read the operating line instead.

## The operating line turned positive; the loss is financing

| | Q2 FY26 | Q3 FY26 |
|---|---|---|
| Revenue | $2,575M | $3,661M |
| Operating income (loss) | $(49)M | **$207M** |
| Net loss | $(626)M | $(709)M |

Revenue grew **more than $1B sequentially**. Operating income crossed into profit — the
company says adjusted operating margin reached double digits "a quarter ahead of plan."

And the net loss still widened, because the gap between the two lines is debt service.
Interest expense, net was **$846M** this quarter against $310M a year ago, and tax took a
further $83M despite a pretax loss. Q4 interest expense is guided to **$1.05–1.15B** — more
again than this quarter's.

So the chart's shape is unusual and worth reading carefully: the loss layout draws gross
profit plus the net loss funding every charge, and the right-hand "Non-operating & tax, net"
bar of $916M is larger than three of the four operating expense lines put together.

## Backlog and guidance

- Revenue backlog approximately **$132.5B** at September 30, against roughly $104B at June 30.
- FY26 revenue guidance raised to **$13.0–13.3B**.
- FY26 adjusted operating income guidance raised to **$1.275–1.375B**, a 26% increase at the
  midpoint on the prior guidance.
- Exit-2026 annualised run-rate revenue guidance raised to **$20–21B**.
- FY26 capex now **$37–39B**, the low end raised, because infrastructure is being delivered to
  customers sooner than planned.
- Active power over **1.7 GW**, more than 200 MW added in the quarter and the footprint doubled
  since the start of the year. Contracted power over 4.6 GW.

Backlog is the company's own definition and includes amounts beyond remaining performance
obligations — see the footnote in the release. It is not a GAAP measure.

## No segment split

CoreWeave discloses revenue by geography only. There is no product or segment breakdown in the
release, which is why the chart draws a single revenue bar. This was checked again this quarter
and still holds — see [[favorites-financials]].

## What this card does not have

- **No debt chart.** `bin/debtfetch.py` matches the balance-sheet column to the period the card
  covers, and the vendor has no September 30, 2026 column yet. The company filed after the close
  on the day the card was built. The Q2 FY26 card's figures — $51.6B of debt against $5.5B of
  cash — are the last charted ones.
- **No post-result EPS surprise.** The vendor's earnings endpoint returned HTTP 403 on the
  refresh, so the Sep '26 point on the earnings chart is still the pre-announcement consensus of
  $(1.45).

## Related pages
- [[favorites-financials]]
- [[sankey-income-statement]]
- [[nebius-q2-fy26]]
