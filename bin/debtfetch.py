#!/usr/bin/env python3
"""Build a debt/coverage spec for every statement on the Financials page.

For each item in financials.json this reads the quarterly balance sheet and
cash flow statement from stockanalysis.com and pulls the column whose period
end matches the one the card already shows, so the bars and the income
statement always describe the same quarter.

    python3 bin/debtfetch.py            # every item that has no spec yet
    python3 bin/debtfetch.py NBIS CRWV  # just these
    python3 bin/debtfetch.py --all      # refetch everything

Nothing is guessed. A ticker whose column cannot be matched, or whose lines
are missing, is reported and skipped rather than written with a hole in it.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
PAUSE = 0.7          # polite, and enough to stay under the rate limiter
TIMEOUT = 25

# Everything else resolves to /stocks/<ticker>/. Nintendo is not a US listing.
PATHS = {"7974": "quote/tyo/7974"}

# The chart's three series, as stockanalysis names them.
F_DEBT, F_CASH, F_FCF = "debt", "cashneq", "fcf"


def hydrate(flat):
    """Decode SvelteKit's flattened __data.json: every int indexes back in."""
    seen = {}

    def walk(i):
        if isinstance(i, str):
            return i
        if not isinstance(i, int) or i < 0:
            return None               # -1 undefined, -2 hole, and friends
        if i in seen:
            return seen[i]
        v = flat[i]
        if isinstance(v, list):
            out = []
            seen[i] = out
            out.extend(walk(x) for x in v)
            return out
        if isinstance(v, dict):
            out = {}
            seen[i] = out
            for k, j in v.items():
                out[k] = walk(j)
            return out
        seen[i] = v
        return v

    return walk(0)


def fetch(sym, statement):
    url = (f"https://stockanalysis.com/{PATHS.get(sym, 'stocks/' + sym.lower())}"
           f"/financials/{statement}/__data.json?p=quarterly")
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        doc = json.loads(r.read().decode("utf-8", "replace"))
    for n in doc.get("nodes") or []:
        if isinstance(n, dict) and n.get("type") == "data":
            d = hydrate(n["data"])
            if isinstance(d, dict) and "financialData" in d:
                return d["financialData"]
    raise LookupError(f"{sym}: no financialData in {statement}")


def period_end(item):
    m = re.search(r"([A-Z][a-z]{2} \d{1,2}, \d{4})", item.get("periodEnd", ""))
    if not m:
        raise ValueError(f"{item['t']}: cannot read a date from "
                         f"{item.get('periodEnd')!r}")
    return datetime.strptime(m.group(1), "%b %d, %Y").date()


def column(fd, want, sym):
    """Index of the column for `want`, allowing a few days of drift between
    the filing's period end and the aggregator's."""
    keys = fd.get("datekey") or []
    dates = []
    for k in keys:
        try:
            dates.append(date.fromisoformat(k))
        except (ValueError, TypeError):
            dates.append(None)        # the TTM column, on annual pages
    for i, d in enumerate(dates):
        if d == want:
            return i
    near = [(abs(d - want), i) for i, d in enumerate(dates) if d]
    if near:
        gap, i = min(near)
        if gap <= timedelta(days=7):
            return i
        raise LookupError(f"{sym}: no column for {want}; nearest is "
                          f"{dates[i]} ({gap.days}d away)")
    raise LookupError(f"{sym}: no dated columns at all")


def at(fd, field, i):
    col = fd.get(field)
    if not isinstance(col, list) or i >= len(col):
        return None
    return col[i]


def build(item, currency):
    sym = item["t"]
    want = period_end(item)
    bs = fetch(sym, "balance-sheet")
    time.sleep(PAUSE)
    cf = fetch(sym, "cash-flow-statement")

    bi, ci = column(bs, want, sym), column(cf, want, sym)

    cash = at(bs, F_CASH, bi)
    if cash is None:
        raise LookupError(f"{sym}: no cash and equivalents for {want}")

    debt = at(bs, F_DEBT, bi)
    if debt is None:
        # a genuinely debt-free balance sheet has no debt lines at all; a
        # missing total with components present is a gap, not a zero
        parts = [at(bs, f, bi) for f in
                 ("debtc", "currentPortDebt", "currentCapLeases",
                  "debtnc", "capitalLeases")]
        if any(p for p in parts):
            raise LookupError(f"{sym}: no total debt for {want} but components "
                              f"are present: {parts}")
        debt = 0

    ocf, capex = at(cf, "ncfo", ci), at(cf, "capex", ci)
    fcf = at(cf, F_FCF, ci)
    if fcf is None:
        if ocf is None or capex is None:
            raise LookupError(f"{sym}: no free cash flow for {want}")
        fcf = ocf + capex         # capex is already negative

    # What each bar is made of, for its tooltip. Only lines the source
    # actually carries; anything the components do not account for is shown
    # as a residual rather than quietly dropped.
    def parts(pairs, total):
        out = [(label, v) for label, f in pairs
               for v in [at(bs, f, bi) or 0] if v]
        rest = total - sum(v for _, v in out)
        if out and abs(rest) > max(1e5, abs(total) * 0.005):
            out.append(("Other", rest))
        return [{"label": l, "value": round(v / 1e6, 1)} for l, v in out]

    debt_parts = parts([("Short-term debt", "debtc"),
                        ("Current portion", "currentPortDebt"),
                        ("Long-term debt", "debtnc"),
                        ("Current leases", "currentCapLeases"),
                        ("Long-term leases", "capitalLeases")], debt)
    cash_parts = []
    for label, f in (("Short-term investments", "investmentsc"),
                     ("Restricted cash (separate)", "restrictedCash")):
        v = at(bs, f, bi)
        if v:
            cash_parts.append({"label": label, "value": round(v / 1e6, 1)})

    m = lambda v: round(v / 1e6, 1)
    flow = "half year" if "half year" in item.get("periodEnd", "") else "quarter"
    return {
        "ticker": sym,
        "company": item["company"],
        "currency": currency,
        "unit": "millions",
        "window": f"The {flow} the Financials card covers: {item['period']}, "
                  f"{item['periodEnd']}.",
        "source": f"stockanalysis.com quarterly balance sheet and cash flow "
                  f"statement, column {want.isoformat()}. Debt and cash are "
                  f"balance sheet stocks at the period end; free cash flow is "
                  f"that {flow}'s flow.",
        "periods": [{
            "label": item["period"],
            "debt": m(debt), "fcf": m(fcf), "cash": m(cash),
            "debt_parts": debt_parts,
            "cash_parts": cash_parts,
            "fcf_parts": ([{"label": "Operating cash flow", "value": m(ocf)}]
                          if ocf is not None else [])
                         + ([{"label": "Capital expenditure", "value": m(capex)}]
                            if capex is not None else []),
        }],
    }


def currency_of(item):
    """Keep the filed currency. The card's own KPI values carry it -- reading
    it from the sankey spec instead picked up a stale file for TSM, which has
    both a NT$ spec and a superseded USD one."""
    for h in item.get("highlights") or []:
        m = re.match(r"\s*([^\d\s.,()-]+)", str(h.get("v", "")))
        if m:
            return m.group(1)
    return "$"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    refetch = "--all" in sys.argv

    doc = json.loads((HERE / "financials.json").read_text())
    items = doc["items"]
    if args:
        want = {a.upper() for a in args}
        items = [i for i in items if i["t"].upper() in want]

    ok, failed, skipped = [], [], []
    for item in items:
        out = HERE / "examples" / f"{item['t'].lower()}-debt.json"
        if out.exists() and not refetch and not args:
            skipped.append(item["t"])
            continue
        try:
            spec = build(item, currency_of(item))
        except (urllib.error.URLError, LookupError, ValueError, KeyError) as e:
            failed.append((item["t"], str(e)))
            print(f"  ! {e}", file=sys.stderr)
        else:
            out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
            q = spec["periods"][0]
            ok.append(item["t"])
            print(f"{item['t']:6} {spec['currency']}{q['debt']:>12,.1f}M debt  "
                  f"{spec['currency']}{q['cash']:>12,.1f}M cash  "
                  f"{spec['currency']}{q['fcf']:>12,.1f}M fcf")
        time.sleep(PAUSE)

    print(f"\nwrote {len(ok)}  skipped {len(skipped)}  failed {len(failed)}")
    for t, e in failed:
        print(f"  FAILED {t}: {e}")


if __name__ == "__main__":
    main()
