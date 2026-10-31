# Eli Lilly Q3 FY26

**Summary**: Lilly's third quarter 2026 (quarter ended September 30, 2026): $24,397M of revenue, up 39% year over year, operating income of $8,608M — a 35% operating margin — and net income of $6,451M. Revenue growth is almost entirely Mounjaro and Zepbound; the gap between gross profit and operating income is widened by a $4,181M acquired in-process R&D charge.

**Sources**: Lilly Q3 2026 8-K sales and earnings release, filed October 29, 2026 (source: q326lillysalesandearningsp.htm), and the Form 10-Q for the quarter ended September 30, 2026 (source: lly-20260930.htm). Market figures from stockanalysis.com.

**Last updated**: 2026-10-30

---

## Income statement

Three months ended September 30, in millions of USD. Lines as the 10-Q's segment note reports them,
which carries both years (source: lly-20260930.htm, R50).

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| **Revenue** | **24,397** | **17,601** | **+39%** |
| Cost of sales | (3,933) | (3,008) | +31% |
| **Gross profit** | **20,464** | **14,593** | **+40%** |
| Research and development | (4,247) | (3,466) | +23% |
| Marketing, selling, and administrative | (3,125) | (2,741) | +14% |
| Acquired in-process research and development | (4,181) | (656) | +537% |
| Asset impairment, restructuring and other | (303) | — | n/m |
| **Operating income** | **8,608** | — | n/m |
| Net interest income (expense) | (316) | — | n/m |
| Net other income (expense) | 114 | — | n/m |
| **Income before income taxes** | **8,406** | — | n/m |
| Income tax expense | (1,955) | — | n/m |
| **Net income** | **6,451** | **5,583** | **+16%** |

Diluted EPS $7.22 reported, $7.48 non-GAAP.

The 10-Q's segment note bundles impairment, interest, other income and tax into a single "other
segment items" line of $2,460M for Q3 FY26 and $2,148M for Q3 FY25, so the prior-year split below
operating income is not disclosed quarter-on-quarter. Those cells are left empty rather than
estimated.

## The vendor and the filing disagree about operating income

stockanalysis.com reports **$13,092M** of operating income for this quarter. The 8-K reports
**$8,608M**. The difference is $4,484M, and it is entirely classification: the vendor places the
$4,181M acquired IPR&D charge and the $303M impairment *below* the operating line, while Lilly
places both *inside* operating income.

The [[sankey-income-statement]] card follows the filing. This is the same failure mode recorded for
Meta, where the vendor moved a $9,890M charge below the line and reported $22,878M of operating
income against the 8-K's $12,988M. A card built on the vendor's number would have shown a 54%
operating margin for a quarter Lilly reports at 35%.

## Acquired IPR&D is the story below the gross line

Acquired IPR&D was **$4,181M against $656M** a year earlier — worth $4.57 a share — mainly the
AtaiBeckley and Curevo acquisitions. The charges are largely non-deductible, which is why tax is
$1,955M on $8,406M of pretax income, an effective rate of 23.3% rather than something closer to the
statutory rate.

This is a real charge against a real quarter, not a presentation artifact. But it describes
transactions, not the operating business, which is why the Financials card draws it as its own
named band rather than folding it into SG&A.

## Revenue is concentrated in two drugs

Lilly runs **one reportable segment**, so the split the card draws is the 10-Q's revenue
disaggregation by therapeutic area, which foots to revenue exactly.

| Therapeutic area | Q3 FY26 | share | Y/Y |
|---|---|---|---|
| Cardiometabolic Health | 19,764 | 81% | +50% |
| Oncology | 2,600 | 11% | +8% |
| Immunology | 1,435 | 6% | +5% |
| Neuroscience | 444 | 2% | +41% |
| Other | 154 | 1% | −54% |

Within cardiometabolic health, **Mounjaro was $10,723M (+65%)** and **Zepbound $5,352M (+49%)** —
together 66% of total company revenue. Jardiance $1,578M, Trulicity $904M (falling), other
cardiometabolic $1,207M.

Geographically: US $15,136M, outside US $9,261M. Outside-US revenue grew faster (+47% against
+34%), led by Mounjaro, whose non-US revenue nearly doubled to $5,725M and now exceeds its US
revenue of $4,998M.

Lilly attributes growth to volume, partly offset by lower realized prices, and raised full-year
guidance to $91.0–92.0B.

## What this card does not carry

No debt chart. `bin/debtfetch.py` could not find a cash and equivalents figure for the
September 30, 2026 balance sheet column, and the chart is skipped rather than matched to a
different period.

No ownership donut — the Form 13F data set for the quarter had not been pulled when the card was
built. See [[share-ownership-donut]] for why that lags a quarter by construction.

## Related pages

- [[sankey-income-statement]]
- [[earnings-surprise-chart]]
- [[share-ownership-donut]]
- [[robinhood-q3-fy26]]
