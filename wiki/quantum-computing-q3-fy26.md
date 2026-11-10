# Quantum Computing Inc Q3 FY26

**Summary**: Quantum Computing Inc's third quarter 2026 (quarter ended September 30, 2026): $9.500M of revenue against $9.072M of cost of revenue, a gross profit of $0.428M, a $28.6M operating loss and a $15.1M net loss. This is the first QUBT card on the Financials tab — the company was excluded until now because cost of revenue exceeded revenue, and this quarter it stopped doing so.

**Sources**: Quantum Computing Inc 10-Q for the quarter ended September 30, 2026, filed November 9, 2026 (source: sec.gov, accession 0001628280-26-072119) — condensed consolidated statements of operations (R4) and the segment reporting note (R44). Market figures from stockanalysis.com, November 9, 2026.

**Last updated**: 2026-11-09

---

## Income statement

Three months ended September 30, in thousands of US dollars.

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| **Revenue** | **9,500** | **384** | **+2374%** |
| Cost of revenue | (9,072) | (258) | n/m |
| **Gross profit** | **428** | **126** | +240% |
| Research and development | (8,336) | (4,509) | +85% |
| Sales and marketing | (5,263) | (787) | +569% |
| General and administrative | (15,414) | (5,234) | +195% |
| **Total operating expenses** | **(29,013)** | **(10,530)** | +176% |
| **Loss from operations** | **(28,585)** | **(10,404)** | worse |
| Interest and other income | 13,047 | 3,544 | +268% |
| Interest expense | (65) | (4) | n/m |
| Change in fair value of derivative liability | 458 | 9,246 | −95% |
| **Net loss** | **(15,145)** | **2,382** | n/m |

Diluted loss per share $(0.07) on 225,443,000 shares. Income tax provision was nil.

## The gate this card just crossed

QUBT has been off the Financials tab since the tab was built. The reason is recorded in
[[sankey-income-statement]] and in the chart skill's own exclusion list: **cost of revenue
exceeded revenue**, so gross profit was negative and there was no flow for a Sankey to draw.
SPCE and CAN are still excluded for the same reason, and HIVE joined them this quarter: its
September 10-Q reports a gross LOSS of $24.7M, because HIVE puts depreciation inside cost of
sales.

In the September quarter gross profit turned positive — **$0.428M on $9.500M**, a 4.5% margin.
That is enough to draw, and the band on the chart is a hairline because that is honestly how
large it is.

**One quarter does not make the year.** For the nine months to September 30, 2026 gross profit
is still negative: $18.742M of revenue against $20.201M of cost of revenue, a gross loss of
$1.459M. If the fourth quarter looks like the first two, the card comes back off the tab.

## Revenue went up 24 times, and the percentage says nothing

Revenue grew from $0.384M to $9.500M. The +2374% on the chart is arithmetically correct and
close to meaningless — a company billing less than four hundred thousand dollars a quarter can
produce almost any growth rate.

The dollar figures are the ones to read. $9.5M of quarterly revenue is a real business starting;
a 2374% growth rate is a base effect.

## Interest income is thirty times gross profit

| | Q3 FY26 |
|---|---|
| Gross profit | $0.4M |
| Interest and other income | **$13.0M** |

The company earns thirty times more from the cash it has raised than from selling anything. That
is why the chart needs a second inflow: charges of $29.0M exceed gross profit plus the net loss,
so $13.5M of non-operating income is drawn as its own source rather than as a negative charge.

It also means the net loss of $15.1M is roughly half the operating loss of $28.6M, and the gap
is interest on the balance sheet rather than anything the business did.

## No segment split

QUBT reports a **single reportable segment**, so there is nothing to break revenue into. The
segment note disaggregates costs — salaries $15.2M, professional services and legal fees $7.8M,
stock-based compensation $2.1M, rent and facilities $3.6M — but not revenue.

This is a genuine absence, not an unfetched split, and the card says so rather than implying the
data was unavailable.

## What this card does not carry

- **No debt chart.** The vendor's balance sheet has no September 30, 2026 column for QUBT — the
  nearest is June 30, 2026, a quarter away — so `bin/debtfetch.py` reported and skipped it
  rather than drawing last quarter's balance sheet beside this quarter's income statement.
- **No post-result earnings surprise.** The vendor's surprise series still ends at Jun '26.
- **No ownership donut**, for the reason given on [[constellation-energy-q3-fy26]].
- **No trailing or forward P/E** — the last twelve months are a loss. Market cap $1.55B as of
  November 9, 2026.

## Related pages
- [[sankey-income-statement]]
- [[favorites-financials]]
- [[constellation-energy-q3-fy26]]
- [[earnings-surprise-chart]]
