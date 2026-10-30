#!/usr/bin/env python3
"""Serve heatmap.html and proxy stock quotes for its Reload button.

A page opened straight from disk cannot fetch Google Finance, Yahoo or
Stooq: none of them send CORS headers, so the browser blocks the call.
This server sits on the same origin as the page and does the fetching
itself, which sidesteps the problem entirely.

    python3 quotes.py            # then open http://localhost:8090
    python3 quotes.py --pe       # fill in missing forward P/E (resumable)
    python3 quotes.py --pe --all # refetch every forward P/E
    python3 quotes.py --pe RKLB MU  # refetch just these
    python3 quotes.py --events   # refresh earnings/ex-dividend dates

Sources are tried in order until one answers. Add your own by writing a
function that takes a list of symbols and returns {symbol: (price, pct)}.
"""

import json
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PORT = 8090
HERE = Path(__file__).resolve().parent
PAGE = HERE / "heatmap.html"

# What the static handler will serve. A whitelist rather than a guess: this
# process can read the whole repo, and nothing outside this list needs to
# reach a browser.
TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
    ".ico": "image/x-icon",
}
TIMEOUT = 12

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


class Throttled(Exception):
    """The site is refusing us, as opposed to the symbol having no data."""


def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/json,text/plain,*/*",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        if e.code in (403, 429):
            raise Throttled(f"HTTP {e.code}")
        raise

    # Cloudflare answers 200 with an interstitial as often as it answers 429.
    if "Just a moment" in body[:600] or "challenge-platform" in body[:2000]:
        raise Throttled("challenge page")
    return body


def from_cnbc(symbols):
    """CNBC's public quote service. Batches many symbols per call, covers
    ETFs, mutual funds and thin OTC names, and needs no key. This is the
    one source that answered reliably when Yahoo, Stooq and Google did not."""
    out = {}
    for i in range(0, len(symbols), 40):
        chunk = symbols[i:i + 40]
        url = ("https://quote.cnbc.com/quote-html-webservice/restQuote/"
               "symbolType/symbol?symbols=" + "|".join(chunk) +
               "&requestMethod=itv&exthrs=1&fund=1&output=json")
        try:
            payload = json.loads(get(url))["FormattedQuoteResult"]["FormattedQuote"]
        except Exception:
            continue

        for q in payload:
            sym = (q.get("symbol") or "").upper()
            try:
                last = float(str(q.get("last")).replace(",", ""))
                prev = float(str(q.get("previous_day_closing")).replace(",", ""))
            except (TypeError, ValueError):
                continue
            if sym and prev:
                out[sym] = (last, (last - prev) / prev * 100)
    return out


def from_nasdaq(symbols):
    """Nasdaq's quote endpoint. One call per symbol and it wants to be told
    whether the symbol is a stock or an ETF, so it is the backup."""
    out = {}
    lock = threading.Lock()

    def one(sym):
        for cls in ("stocks", "etf"):
            try:
                data = json.loads(get(
                    f"https://api.nasdaq.com/api/quote/{sym}/info?assetclass={cls}"
                ))["data"]
                prim = data["primaryData"]
                last = float(prim["lastSalePrice"].replace("$", "").replace(",", ""))
                pct = float(prim["percentageChange"].replace("%", ""))
            except Exception:
                continue
            with lock:
                out[sym] = (last, pct)
            return

    threads = [threading.Thread(target=one, args=(s,)) for s in symbols]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return out


def from_yahoo(symbols):
    """One chart call per symbol. Frequently answers 429 to non-residential
    addresses, so it sits below CNBC."""
    out = {}
    lock = threading.Lock()

    def one(sym):
        url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
               f"{urllib.parse.quote(sym)}?interval=1d&range=5d")
        try:
            meta = json.loads(get(url))["chart"]["result"][0]["meta"]
            price = meta.get("regularMarketPrice")
            prev = meta.get("chartPreviousClose") or meta.get("previousClose")
            if price is None or not prev:
                return
            with lock:
                out[sym] = (float(price), (float(price) - float(prev)) / float(prev) * 100)
        except Exception:
            return

    threads = [threading.Thread(target=one, args=(s,)) for s in symbols]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return out


SOURCES = [("cnbc", from_cnbc), ("nasdaq", from_nasdaq), ("yahoo", from_yahoo)]


def extended(symbols, pause=0.0):
    """Pre-market and after-hours marks, where the session is running.

    None of the price sources above carries an extended-hours quote.
    stockanalysis's quote endpoint does: `ep` is the extended price, `ecp` its
    percent move off the regular close, `eu` the stamp it was read at, `es`
    which session it is, and `ms` whether the regular market is open. They are
    null while the regular session is trading, which is correct rather than a
    failure -- there is no after-hours price at noon.

    One request per symbol, so this is only worth doing for a short list.
    """
    out = {}

    def one(sym):
        try:
            req = urllib.request.Request(
                f"https://stockanalysis.com/api/quotes/s/{sym.lower()}",
                headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=12) as r:
                d = (json.loads(r.read().decode("utf-8", "replace"))
                     .get("data") or {})
        except Exception:
            return
        if not d.get("e") or d.get("ep") in (None, ""):
            with lock:
                out[sym] = {"marketState": d.get("ms")}
            return
        with lock:
            out[sym] = {
                "extPrice": d.get("ep"),
                "extPct": d.get("ecp"),
                "extAsOf": d.get("eu"),
                "extSession": d.get("es"),
                "marketState": d.get("ms"),
            }

    lock = threading.Lock()
    threads = [threading.Thread(target=one, args=(s,)) for s in symbols]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return out


def collect(symbols):
    """Try each source, keep whatever it returns, and pass the still-missing
    symbols to the next one. Reports every source that contributed."""
    found, used, missing = {}, [], list(symbols)

    for name, fn in SOURCES:
        if not missing:
            break
        try:
            got = fn(missing)
        except Exception:
            got = {}
        if got:
            used.append(f"{name} ({len(got)})")
            found.update(got)
            missing = [s for s in missing if s not in found]

    # Extended-hours marks come from a different feed and are additive: a
    # failure here must not cost the regular quote that was already found.
    try:
        ext = extended([s for s in symbols if s in found])
    except Exception:
        ext = {}

    quotes = []
    for s in symbols:
        if s in found:
            price, pct = found[s]
            q = {"symbol": s, "price": round(price, 2), "pct": round(pct, 2)}
            q.update(ext.get(s) or {})
            quotes.append(q)
        else:
            quotes.append({"symbol": s, "error": "not found"})

    return quotes, ", ".join(used) or "no source answered", missing


# ---------------------------------------------------------------- forward P/E

PAGE_FILE = HERE / "heatmap.html"
WATCHLIST_FILE = HERE / "watchlist.json"


def watchlist():
    """The symbol list. It used to live in an inline <script id="watchlist">
    block in heatmap.html; it moved to watchlist.json when the tabs were split
    into separate pages, and both refresh jobs here kept reading the block that
    no longer exists."""
    return json.loads(WATCHLIST_FILE.read_text())


def forward_pe(symbols, pause=2.0):
    """Read forward P/E off stockanalysis.com's statistics page. There is no
    API for it, and the page is same-origin-only for a browser, so this runs
    here.

    Deliberately slow: one request at a time with a pause between. Fetching
    these in parallel trips Cloudflare, which then rate-limits the whole
    domain for a while -- including the quote API the heatmap needs. Values
    move on earnings and estimate revisions, so a slow refresh is fine.

    ETFs, funds and companies with no positive forward estimate legitimately
    have no value; those come back missing rather than wrong."""
    out = {}

    for i, sym in enumerate(symbols, 1):
        found = False

        # The quote page carries the metric table; the statistics page omits
        # Forward PE for plenty of symbols that do publish one.
        for path in ("stocks", "etf"):
            try:
                html = get(f"https://stockanalysis.com/{path}/{sym.lower()}/")
            except Throttled as e:
                print(f"  [{i}/{len(symbols)}] {sym}: blocked ({e}) -- stopping")
                return out, True
            except Exception:
                continue          # this path does not exist for this symbol

            m = re.search(r"Forward PE.*?</td>\s*<td[^>]*>(.*?)</td>", html, re.S)
            if not m:
                # ETFs list a trailing, portfolio-weighted PE and no forward one.
                print(f"  [{i}/{len(symbols)}] {sym}: no forward PE on page")
                found = True
                break

            raw = re.sub(r"<[^>]+>", "", m.group(1)).strip().replace(",", "")
            try:
                out[sym] = float(raw)
                print(f"  [{i}/{len(symbols)}] {sym}: {out[sym]}")
            except ValueError:
                # "n/a" -- no positive forward estimate to divide by
                print(f"  [{i}/{len(symbols)}] {sym}: {raw or 'n/a'}")
            found = True
            break

        if not found:
            print(f"  [{i}/{len(symbols)}] {sym}: no page")

        time.sleep(pause)

    return out, False


def refresh_pe():
    """Write fresh forward P/E values into watchlist.json."""
    doc = watchlist()

    # Resumable: only ask for symbols we do not already have, unless told
    # to refetch everything. A stopped run can simply be run again.
    everything = "--all" in sys.argv
    named = [a.upper() for a in sys.argv[1:] if not a.startswith("-")]

    if named:
        todo = [q["t"] for q in doc["symbols"] if q["t"] in named]
    else:
        todo = [q["t"] for q in doc["symbols"] if everything or "pe" not in q]
    if not todo:
        print("every symbol already has a P/E -- use --pe --all to refetch")
        return

    print(f"reading forward P/E for {len(todo)} symbols (slow by design)...")
    pe, throttled = forward_pe(todo)

    for q in doc["symbols"]:
        if q["t"] in pe:
            q["pe"] = pe[q["t"]]

    # the file carries fav/sector flags as well as tags, so it is written back
    # whole rather than rebuilt from the few fields this function touches
    doc["peAsOf"] = datetime.now().strftime("%b %d, %Y")
    WATCHLIST_FILE.write_text(
        json.dumps(doc, indent=1, ensure_ascii=False) + "\n")

    total = sum(1 for q in doc["symbols"] if "pe" in q)
    print(f"\nadded {len(pe)}; file now has P/E for {total} of {len(doc['symbols'])}")
    if throttled:
        print("stopped early on rate limiting -- wait a few minutes, run again to resume")


# ------------------------------------------------------------------- events

EVENTS_FILE = HERE / "events.json"

# How far back the calendar keeps a date that has already happened.
#
# The source publishes one date per field and gives no flag saying whether it
# is the next one or the last one. That ambiguity only applies forward: a date
# in the FUTURE may be a real schedule or a stale leftover, but a date in the
# PAST is a plain fact -- the company reported that day. The Events page opens
# on a window that starts before today, so recent past dates are kept to fill
# it and older ones are dropped. A past date already in the file is also kept
# even when this run refreshed that symbol, because the source replaces the
# field with the next date as soon as a company reports and the day it
# actually reported is then unrecoverable from the feed.
KEEP_PAST_DAYS = 10

# Types that are not tied to a ticker and are curated by hand, never fetched.
CURATED = ("fed", "macro", "corporate", "holiday")


def cell(html, label):
    """Pull the value cell that follows a labelled metric on a quote page."""
    m = re.search(re.escape(label) + r".*?</td>\s*<td[^>]*>(.*?)</td>", html, re.S)
    if not m:
        return None
    val = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return val or None


def ticker_events(symbols, pause=2.0):
    """Earnings and ex-dividend dates from each quote page.

    The site publishes one date per field and it is the NEXT one when a date
    is confirmed, otherwise the LAST one. There is no flag saying which, so
    the caller keeps only dates in the future and treats the rest as history
    rather than guessing at a schedule."""
    out, throttled = {}, False

    for i, sym in enumerate(symbols, 1):
        got = None
        for path in ("stocks", "etf"):
            try:
                html = get(f"https://stockanalysis.com/{path}/{sym.lower()}/")
            except Throttled as e:
                print(f"  [{i}/{len(symbols)}] {sym}: blocked ({e}) -- stopping")
                return out, True
            except Exception:
                continue

            got = {"earnings": cell(html, "Earnings Date"),
                   "exdiv": cell(html, "Ex-Dividend Date")}
            break

        if got:
            out[sym] = got
            print(f"  [{i}/{len(symbols)}] {sym}: earnings={got['earnings']} exdiv={got['exdiv']}")
        else:
            print(f"  [{i}/{len(symbols)}] {sym}: no page")

        time.sleep(pause)

    return out, throttled


def refresh_events():
    """Refresh events.json with every future-dated ticker event we can see.

    Macro, Fed and corporate entries are preserved. So are the ticker events
    of symbols this run did not ask about: naming a few symbols refreshes
    those and leaves the rest of the calendar alone. Rewriting the whole file
    from a one-symbol run used to delete every other ticker's events."""
    doc = watchlist()

    named = [a.upper() for a in sys.argv[1:] if not a.startswith("-")]
    symbols = [q["t"] for q in doc["symbols"] if not named or q["t"] in named]
    favs = {q["t"] for q in doc["symbols"] if q.get("fav")}

    print(f"reading event dates for {len(symbols)} symbols (slow by design)...")
    found, throttled = ticker_events(symbols)

    today = datetime.now().date()
    floor = today - timedelta(days=KEEP_PAST_DAYS)
    events = []
    stale = 0

    for sym, rec in found.items():
        for kind, label in (("earnings", "Earnings"), ("exdiv", "Ex-dividend")):
            raw = rec.get(kind)
            if not raw or raw.lower() in ("n/a", "-"):
                continue
            try:
                when = datetime.strptime(raw, "%b %d, %Y").date()
            except ValueError:
                continue
            if when < floor:
                stale += 1
                continue
            events.append({
                "date": when.isoformat(),
                "type": kind,
                "ticker": sym,
                "title": f"{sym} {label.lower()}",
                "fav": sym in favs,
            })

    keep, other, past = [], [], []
    if EVENTS_FILE.exists():
        old = json.loads(EVENTS_FILE.read_text())
        asked = set(symbols)
        seen = {(e["date"], e["type"], e.get("ticker")) for e in events}
        for e in old.get("events", []):
            key = (e["date"], e["type"], e.get("ticker"))
            if e["type"] in CURATED:
                keep.append(e)
            elif key in seen:
                continue                 # this run found it again
            elif floor.isoformat() <= e["date"] < today.isoformat():
                past.append(e)           # already happened: a fact, see KEEP_PAST_DAYS
            elif e.get("ticker") not in asked and e["date"] >= today.isoformat():
                other.append(e)          # a symbol this run did not refresh

    events.extend(keep)
    events.extend(other)
    events.extend(past)
    events.sort(key=lambda e: (e["date"], e.get("ticker") or ""))

    EVENTS_FILE.write_text(json.dumps({
        "generated": datetime.now().isoformat(timespec="seconds"),
        "generatedLabel": datetime.now().strftime("%b %d, %Y"),
        "note": (f"Ticker dates are the one date the source publishes per symbol. "
                 f"A future date is the next scheduled report; a past date is the day "
                 f"the company last reported, kept for {KEEP_PAST_DAYS} days so the "
                 f"calendar is not blank behind today. A symbol whose published date "
                 f"is older than that has no confirmed next date and is omitted rather "
                 f"than estimated. Macro, Fed and market-holiday entries are curated "
                 f"by hand."),
        "events": events,
    }, indent=1, ensure_ascii=False) + "\n")

    ticker_events_kept = len([e for e in events if e["type"] in ("earnings", "exdiv")])
    print(f"\nwrote {ticker_events_kept} ticker events "
          f"({stale} published dates older than {KEEP_PAST_DAYS} days, omitted); "
          f"kept {len(keep)} curated, {len(other)} not refreshed, "
          f"{len(past)} already-reported")
    if throttled:
        print("stopped early on rate limiting -- run again to resume")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))

    def send(self, code, body, ctype):
        raw = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def static(self, path):
        """Serve a file from the repo, or None if it is not one to serve.

        The server binds 127.0.0.1, but a path arriving over HTTP is still
        untrusted input: resolve it and require the result to be inside the
        repo, so "../../.ssh/id_rsa" cannot walk out of it.
        """
        rel = path.lstrip("/")
        if not rel:
            return None
        target = (HERE / rel).resolve()
        try:
            target.relative_to(HERE)
        except ValueError:
            return None                       # escaped the repo
        if not target.is_file() or target.suffix.lower() not in TYPES:
            return None
        return target

    def do_GET(self):
        url = urlparse(self.path)

        if url.path in ("/", "/heatmap.html"):
            if not PAGE.exists():
                return self.send(404, f"{PAGE.name} not found next to quotes.py", "text/plain")
            return self.send(200, PAGE.read_text(), "text/html; charset=utf-8")

        if url.path == "/api/quotes":
            raw = parse_qs(url.query).get("symbols", [""])[0]
            symbols = [s.strip().upper() for s in raw.split(",") if s.strip()]
            if not symbols:
                return self.send(400, json.dumps({"error": "no symbols"}), "application/json")

            print(f"  fetching {len(symbols)} symbols...")
            quotes, source, missing = collect(symbols)
            if missing:
                print(f"  no data for: {', '.join(missing)}")

            return self.send(200, json.dumps({
                "quotes": quotes,
                "source": source,
                "asOf": datetime.now().strftime("%b %d, %Y at %-I:%M %p"),
            }), "application/json")

        # Everything else is the rest of the local site: the other pages, the
        # stylesheet, the chart JSON. Served from here so a page that needs
        # /api/quotes is on the same origin as it -- every quote feed refuses
        # a cross-origin call, which is the whole reason this server exists.
        target = self.static(url.path)
        if target:
            ctype = TYPES[target.suffix.lower()]
            return self.send(200, target.read_bytes(), ctype)

        self.send(404, "not found", "text/plain")


if __name__ == "__main__":
    if "--pe" in sys.argv:
        refresh_pe()
        sys.exit(0)

    if "--events" in sys.argv:
        refresh_events()
        sys.exit(0)

    print(f"heatmap:  http://localhost:{PORT}")
    print(f"holdings: http://localhost:{PORT}/holdings.html  (live prices work here)")
    print(f"quotes:   http://localhost:{PORT}/api/quotes?symbols=AAPL,MSFT")
    print("ctrl-c to stop\n")
    try:
        ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
