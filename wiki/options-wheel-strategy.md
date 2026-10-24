# Options Wheel Strategy

**Summary**: Kevin's cash-secured put strategy — sell puts into weakness on five familiar names, avoid assignment where possible, and write covered calls if assigned. This page records the rules, the arithmetic the income target implies, and the factual checklist used to judge an entry.

**Sources**: Strategy as stated by the user, 2026-10-24. Prices and technicals computed from stockanalysis.com daily history, cross-checked against the IBKR connector (MU close $877.55 matched to the cent on both). Option quotes from IBKR snapshots taken 2026-10-24. Earnings dates and P/E from stockanalysis.com.

**Last updated**: 2026-10-24

---

## What this page is and is not

This page records **your** rules and the **factual** readings those rules refer to. It is not a
recommendation to enter any particular trade, and I am not a licensed financial advisor. The
numbers below are arithmetic and market data; which trade to place, if any, is your call.

## The strategy, as stated

1. **Sell cash-secured puts.** Avoid getting assigned as much as possible.
2. **If assigned, sell covered calls** against the shares.
3. **Wait for weakness before selling the put** — especially after consecutive down days or a crash.
4. **Only names you know**: [[micron-fq4-fy26]] (MU), SMH, MSFT, GOOG, TSLA.

Capital: **$300,000**. Income target: **$3,000 per week**.

This is the wheel. The thing that makes it safe is the fourth rule plus one unstated condition:
**you must be willing to own the stock at the strike.** A cash-secured put is a limit buy order you
get paid to place. If that is not true for a given strike, the trade is a naked short-vol bet
wearing a wheel costume.

## What the income target requires

| | |
|---|---|
| $3,000 / week | **1.00% of capital per week** |
| × 52 | $156,000 / year |
| on $300,000 | **52% a year on full capital** |
| over a 27-day cycle | $11,571, or **3.86% per cycle** |

That is the bar. Here is what the market actually paid on **2026-10-24**, from live quotes on MU —
your highest-premium name, at 49% realised volatility — for the Nov 20 expiry, 27 days out, with MU
at $877.55 (source: IBKR snapshot, bid side):

| Strike | OTM | Bid | Premium | Collateral | Per cycle | **Per week** | Annualised |
|---|---|---|---|---|---|---|---|
| 800 | −8.8% | $21.20 | $2,120 | $80,000 | 2.65% | **0.69%** | 36% |
| 760 | −13.4% | $12.55 | $1,255 | $76,000 | 1.65% | **0.43%** | 22% |
| 720 | −18.0% | $7.35 | $735 | $72,000 | 1.02% | **0.26%** | 14% |

**The target needs 1.00% per week. The most aggressive of those three pays 0.69%.**

Put the whole $300,000 into the best-paying line — three MU 800 puts, $240,000 of collateral, every
dollar of it in one semiconductor name — and it produces **$1,649 a week, 55% of the goal**. At the
760 strike it is $976 a week, 33%.

So the target is not reachable on $300,000 under these rules at current volatility. To close the gap
you would have to do one of these, and each one costs something:

- **Sell closer to the money.** Raises assignment odds — directly against rule 1.
- **Sell shorter-dated.** Weeklies collect more per day but gamma rises into expiry, so the
  near-the-money ones flip to assignment fast.
- **Use margin.** Turns a cash-secured put into a naked put. Loses the "I'll just own it" floor.
- **Accept less.** $1,500–1,800 a week is roughly what $300,000 supports at 25–35% annualised on
  collateral, keeping strikes 8–10% out.
- **Wait for higher volatility.** Premium scales with IV, which is the one input that moves on its
  own. Your rule 3 already points this way: crashes are when puts pay.

That last one is worth sitting with, because it is the version of your own strategy that resolves
the conflict. Income is lumpy by design — big in panics, thin in calm tape. A flat $3,000 every week
asks a volatility-selling strategy to behave like a bond.

## The central tension

> "Avoid getting assigned as much as possible" and "$3,000 per week" pull the same lever in
> opposite directions.

Every dollar of extra premium is bought with assignment probability. There is no strike that pays
more without being more likely to be hit — that is what the option market prices. Choose which one
is the real constraint:

- **Income is the constraint** → accept assignment as a normal outcome, not a failure, and lean on
  the covered-call leg to keep earning. The wheel is designed for this.
- **Avoiding assignment is the constraint** → accept roughly 0.25–0.5% per week, which is
  $750–$1,500 on $300,000.

Trying to hold both produces the worst version: strikes close enough to get assigned, in names
chosen for premium rather than for willingness to own.

## Entry checklist for a sell-put

Six factual checks, built from your own rules. None is a verdict — they are the conditions your
rules refer to, so you can see which ones hold.

| # | Check | Why it is on the list |
|---|---|---|
| 1 | **Familiar name** | Your rule 4. MU, SMH, MSFT, GOOG, TSLA. |
| 2 | **Consecutive down closes** (≥2) | Your rule 3 — the explicit trigger. |
| 3 | **RSI(14) below ~35** | Confirms the drop is extended rather than a single red day. Wilder's RSI, not the simple-average variant. |
| 4 | **Price below SMA20 / SMA50** | You are selling into a dip, not chasing strength. |
| 5 | **Price still above SMA200** | The falling-knife guard. A dip inside an uptrend is a different trade from a broken trend, and this is the check that protects rule 1. |
| 6 | **No earnings before expiry** | The single largest assignment risk. An earnings gap is the one move a strike 10% out does not protect against. |

Checks 2–4 say *the stock has fallen*. Checks 5–6 say *and it is likely to stop*. Rule 3 only gives
you the first half; the second half is what keeps assignment rare.

**Choosing the strike**: the 50-day and 200-day moving averages are the natural anchors, because
they are where the dip either holds or does not. ATR% tells you what a normal day is worth — a
strike less than one ATR away is inside the noise.

## Current readings — 2026-10-24

Close of **2026-10-23**. RSI is Wilder's; RV20 is 20-day realised volatility, annualised; "run" is
consecutive closes in one direction (source: stockanalysis.com daily history).

| | Price | 21d% | Run | RSI | vs SMA20 | vs SMA50 | vs SMA200 | Off 52w high | ATR% | RV20 |
|---|---|---|---|---|---|---|---|---|---|---|
| **MU** | $877.55 | −18.8% | +1 | 38 | −11.1% | −10.7% | **+19.9%** | −30.1% | 5.5% | **49%** |
| **SMH** | $527.20 | −12.2% | +1 | 33 | −10.0% | −8.3% | **+2.3%** | −21.5% | 3.3% | 34% |
| **MSFT** | $524.51 | +5.3% | +1 | 53 | −0.4% | +3.2% | **+20.2%** | −5.3% | 2.2% | 20% |
| **GOOG** | $317.28 | −6.4% | **−4** | 31 | −6.6% | −6.6% | **−6.5%** | −21.6% | 2.7% | 20% |
| **TSLA** | $372.22 | −1.5% | −2 | 52 | +0.6% | +2.3% | **−3.7%** | −25.4% | 3.4% | 37% |

Moving averages, as strike anchors:

| | SMA20 | SMA50 | SMA200 | 52w range |
|---|---|---|---|---|
| MU | 986.70 | 982.73 | 732.10 | 192.59 – 1255.00 |
| SMH | 585.54 | 575.09 | 515.44 | 315.05 – 671.83 |
| MSFT | 526.70 | 508.43 | 436.51 | 349.20 – 553.72 |
| GOOG | 339.53 | 339.58 | 339.44 | 252.77 – 404.47 |
| TSLA | 369.87 | 363.77 | 386.35 | 297.38 – 498.83 |

### Catalysts

| | Next earnings | Trailing P/E | Forward P/E |
|---|---|---|---|
| MU | Sep 30, 2026 (reported) | 11.81 | **4.97** |
| SMH | n/a — ETF | 29.13 | 16.87 |
| MSFT | **Oct 28, 2026 — 4 days** | 29.22 | 26.54 |
| GOOG | **Oct 28, 2026 — 4 days** | 15.92 | 23.39 |
| TSLA | Oct 21, 2026 (reported) | 408.95 | 174.59 |

(source: stockanalysis.com, 2026-10-24)

### How the five score against your own checklist

| | 1 Familiar | 2 Down run | 3 RSI<35 | 4 Below MAs | 5 Above SMA200 | 6 No earnings |
|---|---|---|---|---|---|---|
| MU | yes | **no** (+1) | no (38) | yes | **yes** (+19.9%) | yes |
| SMH | yes | **no** (+1) | yes (33) | yes | **yes** (+2.3%) | yes (ETF) |
| MSFT | yes | no (+1) | no (53) | no | yes | **no — Oct 28** |
| GOOG | yes | **yes (−4)** | yes (31) | yes | **no** (−6.5%) | **no — Oct 28** |
| TSLA | yes | yes (−2) | no (52) | no | **no** (−3.7%) | yes |

Reading it straight:

- **GOOG is the only name firing your actual trigger** — four consecutive down closes, RSI 31. It
  also fails both guards: it is 6.5% *below* its 200-day, and it reports in four days. Selling a put
  into earnings is the highest assignment-risk moment there is, and the one your rule 1 is least
  equipped to survive.
- **MU is the deepest drawdown** (−30% from its high) and pays by far the most premium (49% RV). But
  it rose 2.5% on the 23rd, so your consecutive-down-days condition is not active, and it sits 20%
  above its 200-day — the dip has not reached the trend yet.
- **SMH passes the most checks** — oversold, below both short MAs, still above its 200-day, no
  single-name earnings gap. Note what that actually buys you, below.
- **MSFT shows no setup at all** by your rules: RSI 53, only 5.3% off its high, and earnings in four
  days.
- **TSLA** has cleared its earnings but is below its 200-day with RSI 52 — neither oversold nor in a
  confirmed uptrend.

Two things worth flagging that the table does not show:

**MU and SMH are the same bet.** SMH holds MU at 4.59% and NVDA at 20.92% (source:
stockanalysis.com ETF holdings). Selling puts on both is not diversification — it is one
semiconductor position in two tickers, and both would be assigned in the same selloff. With $300,000
you can hold roughly three MU-sized positions, so concentration is the binding risk here, not
strike selection.

**GOOG's forward P/E (23.39) is above its trailing P/E (15.92)**, which implies the market expects
earnings to *fall*. That usually signals a one-off gain in the trailing twelve months rather than a
real decline. **Needs verification** against the filing before you read anything into it.

## The assignment leg: covered calls

If a put is assigned you own 100 shares at the strike and switch to selling calls. Three things
decide whether this leg works:

- **Write above your cost basis.** Strike minus premium received is your real basis. A call written
  below it converts a paper loss into a realised one if called away.
- **The premium drops.** You were assigned because the stock fell, which means the strike you would
  happily write is now further away and pays less. Expect the covered-call leg to earn less per week
  than the put leg did.
- **Capital is now locked in shares, not cash.** 100 MU at $800 is $80,000 that can no longer be
  rotated. With $300,000 and MU-sized positions, **one assignment takes about a third of the book
  out of circulation** until the shares are called away.

That last point is the one that interacts with the income target. Assignments do not just pause
income — they reduce the capital available to generate it, exactly when premium is richest.

## Position sizing with $300,000

At current prices, one contract of collateral at a strike roughly 9% out:

| | Spot | ~9% OTM strike | Collateral | Max positions on $300k |
|---|---|---|---|---|
| MU | $877.55 | ~800 | $80,000 | 3 |
| SMH | $527.20 | ~480 | $48,000 | 6 |
| MSFT | $524.51 | ~477 | $47,700 | 6 |
| GOOG | $317.28 | ~289 | $28,900 | 10 |
| TSLA | $372.22 | ~339 | $33,900 | 8 |

MU alone consumes a third of the account per contract. That is the real constraint on this
strategy at this capital level — not which strike, but how few independent positions $300,000 buys
in names trading at $300–900 a share.

## Related pages

- [[micron-fq4-fy26]] — MU's most recent quarter, the fundamentals behind the name
- [[favorites-financials]] — income statements for the watchlist
- [[sankey-income-statement]] — how the financial charts are built
- `heatmap.html`, `catalysts.html` — the live price and catalyst pages
