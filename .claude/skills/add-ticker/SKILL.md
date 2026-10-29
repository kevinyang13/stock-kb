---
name: add-ticker
description: >
  Add a stock ticker to Stock Signal Desk end to end: the heatmap watchlist, the IBKR
  watchlist, a full Financials card (income statement Sankey + debt chart + earnings chart
  + P/E and dividend), the events calendar, and -- when the ticker is a favorite -- the
  Catalysts and Morning Brief tabs. Use whenever a ticker is given with intent to put it on
  the site: "add IREN", "add CEG to the watchlist", "put VRT on the site", "track GEV",
  "add NVDA as a favorite". For a chart on an existing ticker and nothing else, use
  income-statement-chart instead.
---

# Add a ticker

Puts one new symbol everywhere it belongs in `~/dev/stock-kb`. The site is **public** with
GitHub Pages live, so everything written here is world-readable the moment it is pushed.

Seven places a ticker can land. Do them in this order — the Financials pipeline reads
`financials.json`, and the IBKR and events steps read `watchlist.json`, so the order is a
dependency chain, not a preference.

| # | Place | File | Always? |
|---|---|---|---|
| 1 | Heatmap tile | `watchlist.json` | yes |
| 2 | IBKR watchlist | `ibkr-conids.json` + connector | yes |
| 3 | Financials card | `financials.json`, `examples/`, `charts/`, `assets/financials/` | only if chartable |
| 4 | Events calendar | `events.json` | yes |
| 5 | Catalysts | `news.json` | favorites only |
| 6 | Morning Brief | `brief.json` | favorites only |
| 7 | Wiki | `wiki/` + `index.md` + `log.md` | yes |

## Step 0 — Ask what you cannot infer

Two things decide the shape of the work and neither can be guessed from the symbol:

- **Is it a favorite?** Favorites get `"fav": true`, which is what puts them in the Morning
  Brief's `favorites[]` and in the Catalysts sweep. 15 of 109 are favorites — it is a
  deliberately short list, so do not set it because the name looks important.
- **What is it?** The tags drive the heatmap's sector label and its category chips.

If the user's request does not say, ask once, then do the whole run without stopping again.

## Step 1 — Heatmap tile (`watchlist.json`)

```json
{"t": "IREN", "tags": ["AI Infra", "Data Center", "Crypto", "Mining"]}
```

Fields: `t` the symbol, `tags` a list, optional `sector` to override the label, optional
`fav`, optional `pe` (step 3 writes that, not you).

**The tile's label is the highest-ranked tag it carries**, against the ranked `SECTORS` list.
That list exists **twice** — `assets/site.js` around line 32 and inline in `heatmap.html`
around line 157. A tag that is in neither still labels the tile, but sorts last and gets no
chip. If you add a genuinely new sector, add it to **both** copies or the two pages disagree.

Rank is why tag order inside the entry does not matter but tag *choice* does: `AI Infra`
outranks `Data Center`, so IREN reads "AI Infra" even though it is listed first by accident.
When the ranking picks a tag that is true but not what the company *is* — MU carries
`AI Infra` but makes memory — set `sector` explicitly and it wins outright.

Insert near its peers rather than appending; the default sort is watchlist order, so the file
*is* the board's layout.

## Step 2 — IBKR watchlist (`ibkr-conids.json` + connector)

Resolve the contract id with the IBKR connector's `search_contracts`, then add it:

```json
"IREN": {"conid": 526906130, "ex": "NASDAQ", "desc": "IREN LTD"}
```

Append to the `note` field how and when it was resolved — that note is the only provenance
these ids have.

Then update the live watchlist (`ibkrWatchlist` names it: id `100`, "Stock KB Heatmap").
Three traps, all of which have bitten:

- `edit_watchlist` is **full replace**, not append. Read the current list, add one, write the
  whole thing back. Writing just the new symbol deletes the other 108.
- it takes `id` as a **string**, and contract ids go in as `contract_id_ex`, stringified
- `get_price_snapshot` takes **`contract_id`**, singular — not an array, not `contract_ids`

Read the watchlist back afterwards and confirm the count went up by one. It is allowed to be
a little short of `watchlist.json` (BITF and MFH have never resolved); note the gap, do not
chase it.

**Never place, modify or cancel an order.** `create_order_instruction` exists in the toolset
and is not part of this workflow.

## Step 3 — Financials card

### 3a. The chartable gate

Do not build a card, and say why, for: an ETF or fund (SMH, SPY — holds securities, files no
income statement), a shell with no usable filing (CLBR, BITF), negative gross profit (SPCE,
QUBT), pre-revenue (HQ), or a private company (no filings exist at all). Steps 1, 2, 4 and 7
still apply — the ticker gets a tile and a calendar, just no card.

### 3b. Income statement

Invoke the **`income-statement-chart`** skill. It owns sourcing the quarterly figures, the
mandatory revenue-by-segment split, `bin/mkspec.py`, `bin/sankey.py --json --png`, the
five-identity validator and the `financials.json` entry. Do not reimplement any of it here.

It ends with the card in `financials.json`, which the next three scripts read.

### 3c. Debt chart

```bash
python3 bin/debtfetch.py IREN      # spec from the balance sheet + cash flow
python3 bin/debtbars.py examples/iren-debt.json --json --png
```

`debtfetch.py` matches the balance-sheet column to the period end the card already shows, so
the bars and the income statement always describe the same quarter. A ticker whose column
cannot be matched is **reported and skipped** rather than written with a hole in it — if it
skips, the card simply has no debt chart. Do not hand-fill it.

### 3d. Earnings chart

```bash
python3 bin/epsfetch.py IREN                       # four reported quarters + next consensus
python3 bin/epsdots.py examples/iren-eps.json --json --png
python3 bin/epsnotes.py                            # points the card at it, says what it is
```

This is the **vendor's** EPS against the **vendor's** consensus — usually adjusted, which is a
different basis from the GAAP income statement sitting beside it on the same card. Two EPS
figures on one card invite exactly the wrong comparison, which is why `epsnotes.py` writes the
warning and why `epsfetch.py` marks any pair it cannot show to share a basis as
`basisUnverified` and withholds its surprise figure. Leave that machinery alone.

### 3e. P/E and dividend

```bash
python3 bin/pefetch.py IREN
```

These two KPIs are measured against today's price, not the filed quarter, so they are stale
the moment they are written and carry their own as-of note. A company with no positive
earnings reads `n/a`, which is correct, not a failure.

### 3f. Who owns the shares

```bash
python3 bin/ownfetch.py --data <13f-dir> IREN
python3 bin/ownpie.py examples/iren-own.json --json
```

`<13f-dir>` is an unpacked SEC Form 13F data set, about 400MB and deliberately **not** in the
repo: download the newest quarter from
https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets, point at it, delete it
afterwards. A new set appears roughly six weeks after each quarter end, so the donut is always
a quarter or so behind the income statement beside it. That is inherent to the form.

The slice sizes come from stockanalysis and the holder names from the filings, for reasons
[[share-ownership-donut]] sets out. Two things will stop it, both correctly:

- **the two vendor percentages add to more than 100%**, leaving no honest residual (ARQQ, PHM)
- **no price on or before the 13F period end**, which means the stock had not listed yet, so
  no 13F names it either (SKHY)

Neither is a bug to work around. Leave the card without a donut and say so in the notes.

### 3g. What gets committed

`charts/*.json` is what the page actually fetches and is tracked — income statement, debt,
earnings and ownership alike. Under `assets/financials/` **only the income-statement PNG is
tracked** (70 cards, 70 PNGs); the debt, earnings and ownership PNGs are local fallbacks and
stay out.

## Step 4 — Events calendar

```bash
python3 quotes.py --events
```

Rewrites `events.json` with every earnings and ex-dividend date it can see, preserving the
curated entries — macro, Fed, corporate and market holidays — which are never fetched. It prints
how many published dates it dropped as too old; that is normal, not data loss.

The source gives one date per field with no flag saying whether it is the next one or the last
one. A **future** date is therefore a schedule that may be stale; a **past** date is a fact, the
day the company reported. Past dates are kept for `KEEP_PAST_DAYS` (10) so the Events page's
default window, which opens on the start of this week, is not blank behind today. A past date
already in the file survives even when the run refreshes that symbol, because the source swaps in
the next date the moment a company reports and the day it actually reported is then gone from the
feed.

**A date it cannot confirm is left out, never estimated.** If the new ticker's next report is
not in the output, say so on the card rather than reasoning from last year's filing date.

## Step 5 — Catalysts, if it is a favorite

Catalysts render `news.json`, which is produced by a scheduled **cloud routine** that is
currently failing on an egress block (`bin/README.md` has the detail) — the cloud environment
cannot reach the quote and news sources. So:

- a new favorite needs nothing written into `news.json` by hand; it is swept automatically
  once the routine runs
- never hand-write a catalyst entry. `news.json` carries summaries and real headlines with
  outlet attribution, and an invented one would be indistinguishable from a fetched one on a
  public page

If the user wants the tab current now, regenerate it rather than editing it, and say plainly
that the tab is stale until then.

## Step 6 — Morning Brief, if it is a favorite

`brief.json`'s `favorites[]` is filled from `"fav": true` in `watchlist.json`, so **step 1
already did this** — the 6am weekday launchd job (`bin/morning-brief.sh`) picks it up on its
next run. Nothing to edit.

Two names are hard-coded into that job's prompt instead of coming from the watchlist: the
`holdings` section always covers INTU, MSFT and MC. Adding a favorite does not change that;
adding a *holding* means editing the prompt in `bin/morning-brief.sh`.

That job writes no trade recommendations, option structures, strikes or position sizing, by
design. Keep it that way — it is personalized investment advice and must stay off the site.

## Step 7 — Wiki, verify, commit

Per `CLAUDE.md`, which governs everything here:

- a company page at `wiki/<ticker>-<period>.md`, lowercase with hyphens, in the standard page
  format (Summary / Sources / Last updated / content / Related pages)
- every factual claim carries its source; contradictions between sources get stated, not
  resolved silently
- add the page to the **Companies** section of `wiki/index.md` with a one-line description,
  and update its chart and split counts
- update `wiki/favorites-financials.md`'s counts
- append to `wiki/log.md` — it is **append-only**
- never touch anything in `raw/`

Then:

```bash
python3 bin/stamp.py          # only if anything under assets/ changed
python3 -m http.server 8099   # then open heatmap.html and financials.html
```

Check in the browser before committing: the tile appears with the right sector label, the
card's live chart draws and its hover values are right, no broken images, no horizontal
overflow. `stamp.py` matters because the pages' no-cache meta tags cover only the HTML — a
stale cached stylesheet hides a change completely.

Commit messages end with:

```
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

## Traps

- **Aggregators disagree with filings.** Follow the filing. stockanalysis put a $9,890M Meta
  charge below the operating line and reported $22,878M of operating income against the 8-K's
  $12,988M.
- **A fiscal-year-end quarter is never filed on its own.** A June-year company's Q4 exists
  only as the 10-K annual minus the last 10-Q nine-month column. That is a legitimate card but
  it must say on its face that it is derived, and it must prove itself — revenue, pretax and
  net all footing, and the segments footing to revenue to the dollar.
- **Cost of revenue "exclusive of D&A"** makes a gross margin that is not comparable to the
  other cards. Say so on the card. IREN's 76% becomes a gross *loss* with D&A above the line.
- **One-off gains and charges.** A $99B paper gain or a $450M impairment describes an event,
  not a business. Say so beside the KPI rather than letting it stand alone.
- **Precision under $1bn of revenue**: millions at one decimal. `$13.5M` rounded to `$14M`
  turned a 16% gross margin into 14%.
- **Non-USD filings** stay in the filed currency unless asked to convert.
- **`pgrep -f` matches its own waiter.** A shell whose command line contains the pattern
  matches itself and the loop never exits. Use `pgrep -f "[e]psfetch.py"`.
- **No personalized investment advice**, anywhere on the site or in the response. Directional
  tables are research framing, not a recommendation.
- **Never fabricate** a figure, headline, segment or catalyst. A gap gets stated as a gap.
