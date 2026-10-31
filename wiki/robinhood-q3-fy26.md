# Robinhood Q3 FY26

**Summary**: Robinhood's third quarter 2026 (quarter ended September 30, 2026): $1,424M of total net revenues, up 12% year over year, operating income of $685M — a 48% operating margin — and consolidated net income of $476M, of which $468M is attributable to Robinhood. Revenue hit a record, but net income fell 14% and diluted EPS fell 16%, because operating expenses grew 16% and other income swung to a $60M expense.

**Sources**: Robinhood Markets Form 10-Q for the quarter ended September 30, 2026, filed October 28, 2026, and the Q3 2026 results release of October 27, 2026. Market figures from stockanalysis.com.

**Last updated**: 2026-10-30

---

## Income statement

Three months ended September 30, in millions of USD (source: 10-Q, R4).

| Line | Q3 FY26 | Q3 FY25 | Y/Y |
|---|---|---|---|
| Transaction-based revenues | 867 | 730 | +19% |
| Net interest revenues | 415 | 456 | −9% |
| Other revenues | 142 | 88 | +61% |
| **Total net revenues** | **1,424** | **1,274** | **+12%** |
| Brokerage and transaction | (68) | (56) | +21% |
| Technology and development | (254) | (237) | +7% |
| Operations | (79) | (33) | +139% |
| Provision for credit losses | (71) | (26) | +173% |
| Marketing | (104) | (102) | +2% |
| General and administrative | (163) | (185) | −12% |
| **Total operating expenses** | **(739)** | **(639)** | **+16%** |
| **Operating income** | **685** | **635** | **+8%** |
| Other income (expense), net | (60) | (1) | n/m |
| **Income before income taxes** | **625** | **634** | **−1%** |
| Provision for income taxes | (149) | (78) | +91% |
| **Net income** | **476** | **556** | **−14%** |
| Less: attributable to non-controlling interests | 8 | — | n/m |
| **Net income attributable to Robinhood** | **468** | **556** | **−16%** |

Diluted EPS $0.51 against $0.61.

## Record revenue, lower profit

Every revenue line except net interest grew, and total net revenues set a record. Net income still
fell 14%. Three things account for it, none of them revenue:

- **Operating expenses grew 16% against 12% revenue growth.** The growth is concentrated in two
  lines: operations ($33M → $79M) and the provision for credit losses ($26M → $71M), the latter
  tracking the growing credit card book. G&A actually fell 12%.
- **Other income swung from −$1M to −$60M**, wiping out most of the $50M of operating-income growth.
- **The tax provision nearly doubled**, from $78M to $149M, on essentially flat pretax income — the
  effective rate went from 12.3% to 23.8%.

So pretax income was down 1% and net income down 14% on record revenue. The headline "record
revenue" and the EPS decline are both true and describe different lines.

## Net interest fell while transaction revenue carried the quarter

Transaction-based revenue grew 19% to $867M **despite crypto revenue falling 55% to $120M** —
event contracts, options and equities more than replaced it. Net interest fell 9% to $415M on lower
securities lending activity and falling short-term rates, partly offset by a larger
interest-earning asset base.

Transaction-based revenue is now 61% of the total against 57% a year ago.

## How the card draws a brokerage

Robinhood files **no gross profit line**. Its statement runs total net revenues, then total
operating expenses, then operating income. The [[sankey-income-statement]] card needs a cost line,
so it uses **brokerage and transaction expense ($68M)** — the one directly variable cost — as cost
of revenue, the same convention [[coinbase-q3-fy26]] uses with transaction expense.

The consequence is that the card's **95% gross margin is a construction of the chart, not a figure
Robinhood reports**, and it is not comparable to a product company's gross margin. The card says so
in its notes.

The card's "Marketing, ops & credit" band bundles marketing $104M, operations $79M and the credit
loss provision $71M, which the 10-Q lists separately. They are combined only because five separate
opex labels collide at the chart's right edge.

The card draws **net profit as $476M**, the consolidated figure, so that the chart's single
non-operating band equals the filing's own $60M other expense exactly. The $8M attributable to
non-controlling interests, and the $468M that reaches Robinhood's shareholders, are stated in the
notes rather than drawn.

## Why there is no debt chart

`bin/debtfetch.py` produced one and it was discarded. The vendor's balance sheet maps Robinhood's
**$19,480M of securities loaned into short-term debt**, which would have drawn $22.6B of "debt"
against $685M of quarterly operating profit.

Securities loaned is collateralised stock lending, matched by $4,781M of securities borrowed and by
user-held assets on the other side of the balance sheet. It is not borrowing. Robinhood's actual
long-term borrowings at September 30, 2026 were **$2,660M**, against $5,829M of cash and a further
$13,443M of cash segregated for users.

No comparable distortion appears on [[coinbase-q3-fy26]], NU or V, whose debt charts show genuine
corporate borrowings. This is specific to a broker that runs a large securities-lending book.

## Related pages

- [[sankey-income-statement]]
- [[coinbase-q3-fy26]]
- [[earnings-surprise-chart]]
- [[eli-lilly-q3-fy26]]
