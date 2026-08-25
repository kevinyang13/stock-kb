#!/usr/bin/env python3
"""Serve heatmap.html and proxy stock quotes for its Reload button.

A page opened straight from disk cannot fetch Google Finance, Yahoo or
Stooq: none of them send CORS headers, so the browser blocks the call.
This server sits on the same origin as the page and does the fetching
itself, which sidesteps the problem entirely.

    python3 quotes.py            # then open http://localhost:8090
    python3 quotes.py --pe       # fill in missing forward P/E (resumable)
    python3 quotes.py --pe --all # refetch every forward P/E

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
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PORT = 8090
HERE = Path(__file__).resolve().parent
PAGE = HERE / "heatmap.html"
TIMEOUT = 12

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/json,text/plain,*/*",
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


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

    quotes = []
    for s in symbols:
        if s in found:
            price, pct = found[s]
            quotes.append({"symbol": s, "price": round(price, 2), "pct": round(pct, 2)})
        else:
            quotes.append({"symbol": s, "error": "not found"})

    return quotes, ", ".join(used) or "no source answered", missing


# ---------------------------------------------------------------- forward P/E

PAGE_FILE = HERE / "heatmap.html"


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
        for path in ("stocks", "etf"):
            try:
                html = get(f"https://stockanalysis.com/{path}/{sym.lower()}/statistics/")
            except Exception:
                continue

            if "Just a moment" in html[:400] or len(html) < 8000:
                print(f"  [{i}/{len(symbols)}] {sym}: rate limited -- stopping here")
                return out, True

            m = re.search(r"Forward PE.{0,400}?>([\d.]+)<", html, re.S)
            if m:
                out[sym] = float(m.group(1))
                print(f"  [{i}/{len(symbols)}] {sym}: {out[sym]}")
                break
        else:
            print(f"  [{i}/{len(symbols)}] {sym}: none published")

        time.sleep(pause)

    return out, False


def refresh_pe():
    """Rewrite the watchlist block in heatmap.html with fresh P/E values."""
    src = PAGE_FILE.read_text()
    block = re.search(r'(id="watchlist">)(.*?)(</script>)', src, re.S)
    doc = json.loads(block.group(2))

    # Resumable: only ask for symbols we do not already have, unless told
    # to refetch everything. A stopped run can simply be run again.
    everything = "--all" in sys.argv
    todo = [q["t"] for q in doc["symbols"] if everything or "pe" not in q]
    if not todo:
        print("every symbol already has a P/E -- use --pe --all to refetch")
        return

    print(f"reading forward P/E for {len(todo)} symbols (slow by design)...")
    pe, throttled = forward_pe(todo)

    for q in doc["symbols"]:
        if q["t"] in pe:
            q["pe"] = pe[q["t"]]

    lines = []
    for q in doc["symbols"]:
        pe_part = ' "pe": %s,' % q["pe"] if "pe" in q else ""
        lines.append('    { "t": %-8s%s "tags": %s }' % (
            '"%s",' % q["t"], pe_part, json.dumps(q["tags"])))

    body = '\n{\n  "name": %s,\n  "peAsOf": %s,\n  "symbols": [\n%s\n  ]\n}\n' % (
        json.dumps(doc["name"]),
        json.dumps(datetime.now().strftime("%b %d, %Y")),
        ",\n".join(lines))

    PAGE_FILE.write_text(src[:block.start(2)] + body + src[block.end(2):])

    total = sum(1 for q in doc["symbols"] if "pe" in q)
    print(f"\nadded {len(pe)}; file now has P/E for {total} of {len(doc['symbols'])}")
    if throttled:
        print("stopped early on rate limiting -- wait a few minutes, run again to resume")


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

        self.send(404, "not found", "text/plain")


if __name__ == "__main__":
    if "--pe" in sys.argv:
        refresh_pe()
        sys.exit(0)

    print(f"heatmap:  http://localhost:{PORT}")
    print(f"quotes:   http://localhost:{PORT}/api/quotes?symbols=AAPL,MSFT")
    print("ctrl-c to stop\n")
    try:
        ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
