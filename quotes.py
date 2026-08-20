#!/usr/bin/env python3
"""Serve heatmap.html and proxy stock quotes for its Reload button.

A page opened straight from disk cannot fetch Google Finance, Yahoo or
Stooq: none of them send CORS headers, so the browser blocks the call.
This server sits on the same origin as the page and does the fetching
itself, which sidesteps the problem entirely.

    python3 quotes.py            # then open http://localhost:8090

Sources are tried in order until one answers. Add your own by writing a
function that takes a list of symbols and returns {symbol: (price, pct)}.
"""

import json
import sys
import threading
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
    print(f"heatmap:  http://localhost:{PORT}")
    print(f"quotes:   http://localhost:{PORT}/api/quotes?symbols=AAPL,MSFT")
    print("ctrl-c to stop\n")
    try:
        ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
