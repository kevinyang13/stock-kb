# Options Strategies

**Summary**: Twelve option structures mapped onto a single five-point scale of how far and
which way the stock moves. The scale, not the structure, is the starting point: pick the
number first, then the structure that expresses it.

**Sources**: Strategy chart supplied by the user, 2026-11-14 (three images: an eleven-payoff
grid, an expected-move band chart, and a worked example of the four questions). The synthetic
long is the one structure **not** from that chart — it was added on request on 2026-11-23 and
its legs were written to the same illustrative $100 stock. Payoff figures are computed by
`options.html` from the legs in `options.json`; no figure on the page or this one is quoted
from a vendor.

**Last updated**: 2026-11-23

---

## The −2 to +2 scale

The scale measures a move in **expected moves**, which is the options market's own forecast
of a one-standard-deviation range to expiry — not a guess about percentage. On the
illustrative $100 stock used throughout, one band is $5 (source: options.json).

| | Name | Band | Roughly |
|---|---|---|---|
| **−2** | Hard down | below −2σ | 2.5% |
| **−1** | Drift down | −2σ to −1σ | 13.5% |
| **0** | Goes nowhere | inside ±1σ | **68%** |
| **+1** | Drift up | +1σ to +2σ | 13.5% |
| **+2** | Hard up | above +2σ | 2.5% |

The probabilities are the normal-distribution figures the band chart is drawn from (source:
user-supplied band chart, which labels 68.24% inside the first band and 15.86% in each outer
region). Real return distributions have fatter tails than this, so the outer numbers
understate how often −2 and +2 actually happen.

**The asymmetry is the lesson.** 0 is the single most likely outcome by a wide margin, and
only three of the twelve structures are paid for it. Every bought option is a bet against
the base case.

## The four questions

Each structure answers the same four (source: user-supplied worked example):

1. **What is the trade?** Which legs, in which direction.
2. **Debit or credit?** Does money leave or arrive when it is opened.
3. **What is the outlook?** One of −2, −1, 0, +1, +2.
4. **Why would I use it?** What it does that a simpler position does not.

## The twelve, by outlook

| Outlook | Debit (pay to open) | Credit (paid to open) |
|---|---|---|
| **−2** | [[#long-put]], [[#long-straddle]], [[#long-strangle]] | — |
| **−1** | [[#bear-put-spread]] | — |
| **0** | [[#calendar-spread]], [[#protective-put]] (as a hedge) | [[#covered-call]], [[#cash-secured-put]], [[#iron-condor]] |
| **+1** | [[#bull-call-spread]], [[#synthetic-long]] | — |
| **+2** | [[#long-call]], [[#synthetic-long]], [[#long-straddle]], [[#long-strangle]] | — |

Every credit structure on the site sits at **0**. That is not a coincidence: selling premium
is a bet that nothing much happens, which is why it wins often and why the losses, when they
come, are larger than the wins.

## Computed figures

`options.html` derives each curve, break-even and extreme from the legs rather than drawing
them, on the illustrative $100 stock (source: options.json):

| Structure | Flow | Max gain | Max loss | Break-even |
|---|---|---|---|---|
| Long call | debit | unlimited | −$350 | $103.50 |
| Long put | debit | +$9,660 | −$340 | $96.60 |
| Covered call | credit | +$700 | −$9,800 | $98.00 |
| Cash secured put | credit | +$220 | −$9,280 | $92.80 |
| Protective put | debit | unlimited | −$680 | $101.80 |
| Synthetic long | debit | unlimited | −$10,010 | $100.10 |
| Bull call spread | debit | +$760 | −$240 | $102.40 |
| Bear put spread | debit | +$760 | −$240 | $97.60 |
| Iron condor | credit | +$210 | −$290 | $92.90 / $107.10 |
| Long straddle | debit | unlimited | −$690 | $93.10 / $106.90 |
| Long strangle | debit | unlimited | −$420 | $90.80 / $109.20 |
| Calendar spread | debit | +$100 | −$160 | $91.64 / $108.36 |

**Only the upside is ever unlimited.** A stock cannot go below zero, so the loss on long
shares or a short put is large but bounded — the covered call's −$9,800 is the stock going to
zero, not an open-ended risk. Unlimited loss appears only where a call is net short and
uncovered, which none of these twelve are.

**Every four-figure maximum loss on the page is a stock position in disguise** — the covered
call and the cash-secured put own or owe stock, and the synthetic long's −$10,010 is the short
put being assigned at $100 with the stock at zero. The flow label does not predict the size of
the risk: the synthetic long is a *debit* structure with the largest maximum loss of the
twelve. That is also the honest reading of a covered call: a long stock position with a small
income stream, and the income does not protect it.

## The synthetic long is the parity check

A long call and a short put at the same strike have the same payoff as 100 shares, because
put–call parity says so: call − put = stock − strike, discounted. On the illustrative stock
the $100 call costs $3.50 and the $100 put pays $3.40, so the pair opens for a $10 debit and
breaks even at $100.10 rather than $100.00 (source: options.json). That ten-dollar gap is the
whole economic difference between holding the structure and holding $10,000 of stock, and it
is the carry the market is charging to defer the purchase.

Two consequences worth stating plainly:

- **The leverage is in the cash, not in the payoff.** The slope is exactly 1.0 against the
  stock everywhere — no convexity, no decay working for or against the position on net.
- **The short put makes the downside the stock's.** A −2 costs what owning the shares costs,
  and a broker margins it that way. Nothing about the structure reduces risk; it defers
  paying for it.

## The calendar spread is the exception

Eleven of the twelve curves are terminal payoff arithmetic and settle on one date. A calendar
has two expiries, so it has no terminal payoff at all. What `options.html` draws is the
position's **value at the front expiry**: the short leg settles at intrinsic, the long leg
keeps whatever time value remains, and the intrinsic cancels, leaving remaining time value
minus the debit. The tent's height and width depend on implied volatility in the back month,
which is an estimate. Its **maximum loss is exactly the debit paid**, which is not an
estimate (source: options.json).

The page labels this curve on its face rather than letting it sit beside eleven computed ones
looking equally settled.

## Related pages

- [[options-wheel-strategy]] — the cash-secured put / covered call wheel these structures are used in
- [[favorites-financials]]
- [[index]]
