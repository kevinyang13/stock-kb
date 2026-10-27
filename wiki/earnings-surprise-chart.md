# Earnings Surprise Chart

**Summary**: The actual-vs-estimate EPS chart on each Financials card — what the company earned
against what the street expected, four reported quarters and the one still ahead — and the one
thing about it that is easy to read wrong.

**Sources**: Nasdaq's `earnings-surprise`, `earnings-forecast` and `earnings-date` endpoints, which
carry Zacks' consensus. Built by `bin/epsfetch.py`, drawn by `bin/epsdots.py`.

**Last updated**: 2026-10-26

---

## What it shows

One column per quarter. A filled dot is what the company actually earned, a hollow one is what the
street expected, and a hairline joins the pair, so the gap between them is what the eye lands on.
The rightmost column is the quarter that has not been reported yet: consensus only, no actual.

Hovering a reported dot gives the date it was reported, both figures and the surprise in dollars
and percent. Hovering the unreported one gives the consensus, the high-to-low range of estimates,
how many analysts are in it, how many revised up or down in the last four weeks, and when the
report is due.

## The catch: this is not the EPS the statement beside it is built from

The income statement Sankey on the same card is GAAP, from the company's own filing. This chart is
**adjusted** EPS, the basis the street scores against. The two differ by whatever a company excludes
— stock compensation, impairments, one-off gains — and for some names that is most of the number.
Rigetti, MicroStrategy and the miners are the extreme cases.

So the two numbers on one card are not comparable, and reading the surprise as a beat against the
filed result would be wrong. Both the hover and the card note say this.

A second basis difference, for foreign filers: this is the **ADR's** earnings per share in US
dollars, whatever currency the statement itself is filed in. TSM's statement is in New Taiwan
dollars and its chart is in dollars per ADR.

## How it is built

```bash
python3 bin/epsfetch.py              # every card without a spec yet
python3 bin/epsfetch.py NBIS NVDA    # just these
python3 bin/epsfetch.py --all        # refetch everything
python3 bin/epsdots.py examples/nbis-eps.json --json --png
python3 bin/epsnotes.py              # link the chart and write the card note
```

`epsfetch` reads three endpoints per ticker and refuses anything it cannot stand behind:

- it asks Nasdaq for the company name first and **skips the ticker if the name does not match the
  card**. Tickers are reused across exchanges, and a chart drawn from another company's earnings
  would look entirely plausible. MDA is the live example — MDA Space on Nasdaq, but the symbol has
  belonged to others.
- a quarter is either reported, with both an actual and an estimate, or it is ahead, with no
  actual. `epsdots.validate` refuses anything in between, so an unreported quarter can never pick
  up an actual from a stale row.
- a filer with no Nasdaq listing is skipped outright, not approximated. 63 of the 66 cards
  carry the chart; Nintendo (7974) is not on Nasdaq, Arqit (ARQQ) has no surprise history
  published, and Xanadu (XNDU) has no reported quarters yet.

## Layout

The card now carries three figures. The sankey has a floor of 760px, so on a 1440px screen the
debt bars sit beside it and the earnings dots wrap underneath; past about 1900px all three share a
row. Without that floor the sankey collapsed to nothing the moment a third chart joined the row.

`assets/sankey.js` scales scatter marker sizes along with the fonts and margins. Bar traces carry a
marker with no `size`, so the scaling is guarded on that.

## Related pages
- [[sankey-income-statement]]
- [[favorites-financials]]
