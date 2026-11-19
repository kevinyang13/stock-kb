# Options Simulator

**Summary**: A browser-side option pricer behind the Simulator tab. Takes a symbol, a price,
an expiry and a volatility, applies any of ten strategy templates or a hand-built set of
legs, and draws the P/L against that symbol's own price range.

**Sources**: Strategy templates are read from `options.json`, the same file behind
[[options-strategies]]. Symbol list from `watchlist.json`. No price feed: the price is typed
in, because `prices.json` carries no snapshot.

**Last updated**: 2026-11-14

---

## What it computes, and with what

Two different kinds of number sit on this page, and the page keeps them apart:

| | How it is produced | How far to trust it |
|---|---|---|
| Payoff at expiry, break-evens, max gain and loss | Arithmetic on the legs | Exact |
| The dashed "today" curve, every premium marked *model* | Black–Scholes on the entered vol | An estimate |

Black–Scholes here is European exercise with no dividend, so an American put near expiry and
anything crossing a dividend will be off. The premium column is editable for exactly this
reason: paste a real mid and the payoff arithmetic becomes real too.

## Strikes travel between symbols

Templates do not carry strikes. `options.json` draws every structure on a $100 stock whose
expected move is $5, so a strike in that file is really an **offset in expected moves** — the
covered call's $105 means "one expected move up." The simulator converts: it computes this
symbol's own expected move from the volatility and days entered, `S × IV × √(T)`, places each
strike at the same offset and rounds to a plausible increment.

That is why the same template produces a $1,065 call on an $885 stock at 70% vol and a $320
call on a $292 stock at 32% vol. The structure is the same shape; the strikes are this name's.

## Collateral is not a separate figure

An earlier version showed collateral beside max loss and was wrong twice over: it treated
every short put as needing the full strike in cash, which overstated an iron condor's
requirement by $26,500 against $2,500, and it paired long legs against short ones in the
wrong direction, so both debit spreads came out either unsecured or fully secured.

It was then removed rather than fixed, because **on a defined-risk structure the broker's
requirement is the maximum loss** — an iron condor's is the wider wing less the credit, a cash
secured put's is the strike less the credit — and the page already states the maximum loss
exactly. What remains is the one requirement the payoff does not imply: the cost of shares a
structure needs you to hold.

## Filling from IBKR

**The browser cannot reach IBKR.** The connector is a tool Claude holds, not an endpoint this
page can call, and there is no API server behind this site — `/api/quotes` has always 404'd on
the Holdings tab for the same reason. So the button is a **load, not a fetch**: Claude pulls
through the connector, writes `chains.json`, and the page reads it. The button shows the
snapshot's age rather than implying it is live, and it only appears on localhost, because
`chains.json` is in `.gitignore` and does not exist on the published site.

It fills three things:

| | Where it comes from |
|---|---|
| **Price** | the underlying's last close |
| **Expiry** | the real expiration dates for that contract |
| **Implied vol** | the broker's own midpoint IV, or solved from the at-the-money straddle |

**Volatility is taken from the broker where the snapshot carries it, and solved where it does
not.** `get_price_snapshot` does return `option_midpoint_iv` and `option_greeks` on an option
contract — an earlier version of this page assumed it did not, and bisected Black–Scholes for
every symbol. NVDA was pulled with those fields and carries a call IV of 116% and a put IV of
115% straight from the desk, so nothing is solved for it. The three symbols pulled before that
(NBIS, GOOG, SNDK) have no IV in the file and still go through the solver, which bisects on the
call mid and the put mid separately and averages, reporting both so the disagreement is visible.
On NBIS both sides solved to 122% — agreeing to the point, which is evidence the inputs are
consistent. On SNDK they came out 101% and 124%, which is the weekend's wide quotes showing
through, and the kind of gap a broker IV does not have.

**It solves against the close, not the after-hours print.** The option marks and the stock
mark carry different timestamps: NBIS's options were quoted at Friday's close with the stock
at $115.88, while the stock snapshot is an after-hours $112.80. Put-call parity holds at
$115.88 and fails badly at $112.80, so the close is what the chain was priced against and the
close is what the solver uses. Both timestamps are kept in the file.

**Real strikes beat a guessed ladder.** Before the chain is loaded the page rounds strikes to
an increment guessed from the price, which put GOOG on 5.00 when it really lists 2.50 — the
templates were placing legs on contracts that do not exist. A loaded chain supplies its own
increment and its own strike list, and the ladder is cleared the moment the symbol changes.

A real ladder is not always evenly spaced, which is the other thing a guess cannot know. NVDA's
Nov 20 chain runs 1.00 apart from 131 to 150 and 2.50 apart from 152.5 up. A strangle on it
places its legs at 175 and 138 — one strike out of each band — because the page snaps to the
nearest listed strike before it falls back to an increment.

## Known limits

- **No calendar or diagonal.** Both need two expiries and this page prices one, so they are
  left out of the template list rather than drawn wrong. [[options-strategies]] carries the
  calendar, labelled as a shape rather than a settlement.
- **No early assignment.** The page warns when a structure holds a short leg, because American
  exercise can end a position before the curve it draws ever happens.
- **No live quotes.** Price and volatility are typed in.

## Related pages

- [[options-strategies]] — the eleven structures and the −2 to +2 scale this page's bands come from
- [[options-wheel-strategy]]
- [[index]]
