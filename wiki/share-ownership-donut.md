# Share Ownership Donut

**Summary**: The "Who owns the shares" chart on each Financials card: four slices of the whole
share count, with each institutional slice naming its five largest holders on hover. Slice sizes
come from stockanalysis, the holder names from the SEC's own Form 13F data set, and this page
explains why it has to be both.

**Sources**: SEC Form 13F data sets (source: sec.gov/data-research/sec-markets-data/form-13f-data-sets),
stockanalysis.com statistics endpoint. Built 2026-10-29 from the set covering filings received
June–August 2026, which reports holdings as of **June 30, 2026**.

**Last updated**: 2026-10-29

---

## What the chart says

Four slices that add to the entire share count:

| Slice | What it is | Where it comes from |
|---|---|---|
| Index & ETF managers | managers whose 13F book is predominantly index funds and ETFs | institutional % × the passive share of the 13F total |
| Other institutions | every other 13F filer | institutional % − the above |
| Insiders | officers, directors and 10% owners | stockanalysis, from Forms 3, 4 and 5 |
| Retail & other | everyone filing no 13F | the residual to 100% |

The hole carries the institutional total, which is the one figure most readers want without
hovering anything. Hovering either institutional slice names its five largest holders, each as a
percentage of all shares outstanding, read from that manager's own filing.

## Why two sources

Only the filings name the holders, and only the vendor gives a percentage that is safe to put in
a pie. Each is used for what the other cannot do.

**A raw 13F sum is not an ownership percentage.** Managers with shared investment discretion
report the same shares more than once, so adding the table up for NVIDIA gives **24.8bn shares
against 24.1bn outstanding** — 103% of the company. The error is structural, not a few bad rows:
11.2bn of those shares are filed under `DFND`, the code for discretion shared with another
manager who is also reporting them.

So the slice sizes use stockanalysis's "Owned by Institutions (%)" and "Owned by Insiders (%)",
which are a netted, internally consistent pair that leaves an honest residual. The 13F data sets
the **ratio** inside the institutional slice and supplies the **names**. Dividing one 13F total by
another cancels most of the double counting, because dual-reported shares inflate numerator and
denominator alike.

The two are on different dates — the vendor percentages are current, the holdings are June 30 —
and the card says so rather than implying one basis.

## The filings have to be checked before they are used

A 13F is typed by the filer and nobody rejects an implausible one. The largest single reported
holding of NVIDIA in this data set is **7.0bn shares by a state teachers' pension fund**: 29% of
the company, and at the June 30 price about four times that fund's entire portfolio. A naive
"top five holders" would have published it at number one.

`bin/ownfetch.py` tests every filing against the only other number in the table. A filer reports
both a share count and a market value, so the implied price is `VALUE / SSHPRNAMT`, and for a real
filing it comes out at the period-end price. For NVIDIA on June 30 the honest filers all imply
**$200.09**. The pension fund implies **$0.005**.

The test has one deliberate exemption. Form 13F moved `VALUE` from thousands of dollars to whole
dollars in 2023, and a minority of filers still report the old way — T. Rowe Price implies exactly
$0.20009, which is the price over a thousand. Their **share count is correct**, so the filing is
kept. Anything that matches neither the price nor the price over a thousand is dropped. For NVIDIA
that is 113 filings of 5,927.

**The median implied price is also what identifies the company.** Filers type the issuer name
freehand, so a name match alone can land on the wrong CUSIP. A candidate CUSIP is accepted only
once its filers imply the price this ticker actually closed at on the period end, read from its
own history. A wrong company fails that test on the spot.

## What the passive split is, and is not

A 13F says what a manager holds and never why. An index fund's shares and a stock-picker's shares
arrive in the same table under the same name, and BlackRock files **one** 13F covering iShares and
its active mandates together. No field separates them.

So "Index & ETF managers" is an assignment **by manager, not by mandate**, made from a list in
`bin/passive-managers.json`. The list is deliberately conservative: a name is on it only if its
13F book is overwhelmingly passive vehicles. Houses running large active and passive books side by
side — FMR, JPMorgan, Morgan Stanley, Goldman, Capital Research, T. Rowe, Invesco — are left off
and counted as active, so the chart **understates** the index share rather than overstating it.

Edit that file rather than the code, and say in the commit why a name moved.

## What it leaves out

- **Options are excluded.** Puts and calls are dropped: the chart is about who owns the shares,
  and an option position is not ownership of them.
- **Insiders may be counted twice.** A venture firm that is both a 10% owner and a 13F filer
  appears in both slices. It is rare among the names on the Financials tab and is not corrected.
- **The 13F lags.** Holdings are as of the quarter end before the filing deadline, so the chart is
  always at least six weeks behind and usually more. The September 30, 2026 filings are due
  November 14, 2026.
- **Managers under $100M do not file**, so they fall into "Retail & other" alongside individuals.
  That slice is not purely retail and the hover says so.

## Related pages

- [[sankey-income-statement]]
- [[earnings-surprise-chart]]
- [[favorites-financials]]
