#!/usr/bin/env python3
"""Put the market figures -- P/E and dividend -- on each Financials card.

    python3 bin/pefetch.py             # every card
    python3 bin/pefetch.py NVDA NBIS   # just these

The other four KPIs on a card come from one filed quarter and never change.
These two do not belong to that quarter at all: both are measured against
today's share price, so they move every session and are stale the moment they
are written. That is why one note carries the date for both, and why this is a
separate script rather than something folded into the statement pipeline.

Figures come from stockanalysis.com's quote data (`peRatio`, `forwardPE`,
`dividend`, `exDividendDate`) -- the same source the heatmap's forward P/E
column uses.

A company with no positive earnings has no meaningful trailing P/E, and one
with no positive forward estimate has no forward P/E. Those read "n/a" rather
than a negative number, which is what a negative P/E would be: not a cheap
stock, just a loss. A company that pays nothing reads "None", which is a fact
about the company rather than a gap in the data.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sadata import UA, hydrate, path_for

HERE = Path(__file__).resolve().parent.parent
PAUSE = 0.7
TIMEOUT = 25
LABEL = "P/E"
DIV = "Dividend"
NOTE = "Market figures as of"
OLD_NOTE = "P/E as of"       # what this script wrote before dividends joined


# What the quote reports the dividend in. Nintendo's comes through as
# "162.00 (1.91%)" with no symbol at all, and defaulting that to a dollar sign
# turned a yen dividend into a dollar one on the card.
SYMBOLS = {"USD": "$", "JPY": "\u00a5", "KRW": "\u20a9", "EUR": "\u20ac",
           "GBP": "\u00a3", "TWD": "NT$", "CAD": "C$", "HKD": "HK$",
           "CNY": "\u00a5", "BRL": "R$", "ILS": "\u20aa", "INR": "\u20b9"}


def quote_data(sym):
    """(the quote block, the currency its dividend is quoted in)."""
    url = f"https://stockanalysis.com/{path_for(sym)}/__data.json"
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        doc = json.loads(r.read().decode("utf-8", "replace"))
    quote, code = None, None
    for n in doc.get("nodes") or []:
        if isinstance(n, dict) and n.get("type") == "data":
            d = hydrate(n["data"])
            if not isinstance(d, dict):
                continue
            if "peRatio" in d:
                quote = d
            info = d.get("info")
            if isinstance(info, dict) and isinstance(info.get("curr"), dict):
                code = info["curr"].get("dividend") or info["curr"].get("main")
    if quote is None:
        raise LookupError(f"{sym}: no quote data")
    return quote, code


def ratio(v):
    """A P/E only means anything when both halves are positive."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if f > 0 else None


def fmt(v):
    return "n/a" if v is None else f"{v:,.1f}"


def dividend(q, code):
    """(annual rate, yield) out of "$2.83 (6.57%)", or (None, None).

    The quote carries it as one preformatted string, so it is parsed rather
    than trusted: anything that does not match the shape is treated as no
    dividend rather than printed raw into a KPI tile."""
    m = re.match(r"\s*([^\d\s]*)\s*([\d.,]+)\s*\(([\d.]+)%\)",
                 str(q.get("dividend") or ""))
    if not m:
        return None, None
    # a missing symbol is taken from the quote's own currency, never assumed
    cur = m.group(1) or SYMBOLS.get(code or "", (code + " ") if code else "")
    rate, yld = m.group(2).replace(",", ""), m.group(3)
    try:
        return f"{cur}{float(rate):,.2f}", float(yld)
    except ValueError:
        return None, None


def main():
    args = {a.upper() for a in sys.argv[1:] if not a.startswith("--")}
    doc = json.loads((HERE / "financials.json").read_text())
    today = datetime.now().strftime("%b %-d, %Y")
    ok = failed = 0

    for item in doc["items"]:
        t = item["t"]
        if args and t.upper() not in args:
            continue
        try:
            q, code = quote_data(t)
        except (urllib.error.URLError, LookupError, ValueError, KeyError) as e:
            print(f"  ! {t}: {e}", file=sys.stderr)
            failed += 1
            time.sleep(PAUSE)
            continue

        trail, fwd = ratio(q.get("peRatio")), ratio(q.get("forwardPE"))
        hl = item.get("highlights") or []
        tile = {"k": LABEL,
                "v": f"{fmt(trail)} · {fmt(fwd)}",
                "s": "trailing · forward"}
        rate, yld = dividend(q, code)
        ex = str(q.get("exDividendDate") or "").strip()
        ex = ex if ex and ex.lower() != "n/a" else None
        div_tile = ({"k": DIV, "v": f"{yld:,.2f}%", "s": f"{rate} a year"}
                    if rate and yld is not None
                    else {"k": DIV, "v": "None", "s": "no dividend paid"})

        for t_ile in (tile, div_tile):
            at = next((i for i, h in enumerate(hl) if h.get("k") == t_ile["k"]),
                      None)
            if at is None:
                hl.append(t_ile)
            else:
                hl[at] = t_ile
        item["highlights"] = hl

        bits = []
        if trail is None:
            bits.append("no trailing P/E: the last twelve months are a loss")
        if fwd is None:
            bits.append("no forward P/E: no positive forward estimate")
        div_s = (f"dividend {rate} a year, {yld:,.2f}% yield"
                 + (f", last ex-dividend {ex}" if ex else "")
                 if rate and yld is not None else "pays no dividend")
        note = (f"{NOTE} {today}: P/E {fmt(trail)} trailing, {fmt(fwd)} forward"
                + (f" ({'; '.join(bits)})" if bits else "")
                + f"; {div_s}. Both are measured against the share price, so "
                  "unlike the other figures on this card they move every "
                  "session and are not from the filing "
                  "(source: stockanalysis.com).")
        notes = item.get("notes") or []
        nat = next((i for i, n in enumerate(notes)
                    if n.startswith(NOTE) or n.startswith(OLD_NOTE)), None)
        if nat is None:
            notes.append(note)
        else:
            notes[nat] = note
        item["notes"] = notes

        print(f"{t:6} trailing {fmt(trail):>7}  forward {fmt(fwd):>7}  "
              f"dividend {(rate or 'none'):>7}"
              + (f" {yld:,.2f}%" if yld is not None else ""))
        ok += 1
        time.sleep(PAUSE)

    doc["marketAsOf"] = today
    doc.pop("peAsOf", None)
    (HERE / "financials.json").write_text(
        json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print(f"\nupdated {ok}  failed {failed}")


if __name__ == "__main__":
    main()
