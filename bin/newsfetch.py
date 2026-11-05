#!/usr/bin/env python3
"""Pull recent headlines for the watchlist's favorites, for the Catalysts tab.

    python3 bin/newsfetch.py                 # every favorite, last 7 days
    python3 bin/newsfetch.py --days 3        # a tighter window
    python3 bin/newsfetch.py SNDK NBIS       # just these

The Catalysts tab renders `news.json`, which is normally written by a cloud
routine. That routine fails on an egress block -- the cloud environment cannot
reach the quote and news sources -- so the tab went sixteen days stale without
anything saying so. This is the local path: the same vendor feed, fetched from
a machine that can actually reach it.

It writes `out/news-raw.json`, NOT `news.json`. The published file carries a
written summary per ticker, and a summary is a judgement about what moved and
why -- so the fetch and the writing are two steps on purpose. Nothing here
invents a headline, and nothing downstream should either: an invented catalyst
on a public page is indistinguishable from a fetched one.
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sadata import UA, hydrate, path_for

HERE = Path(__file__).resolve().parent.parent
PAUSE = 0.7
TIMEOUT = 25


def news_for(sym):
    """The vendor's news list for one ticker, newest first."""
    url = f"https://stockanalysis.com/{path_for(sym)}/__data.json"
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        doc = json.loads(r.read().decode("utf-8", "replace"))
    for n in doc.get("nodes") or []:
        if isinstance(n, dict) and n.get("type") == "data":
            d = hydrate(n["data"])
            if isinstance(d, dict) and isinstance(d.get("news"), dict):
                items = d["news"].get("data")
                if isinstance(items, list):
                    return items
    return []


def when(item):
    """The item's timestamp, or None. A story with no date is not usable."""
    raw = str(item.get("time") or "").replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--per", type=int, default=6,
                    help="how many stories to keep per ticker")
    a = ap.parse_args()

    wl = json.loads((HERE / "watchlist.json").read_text())
    want = {t.upper() for t in a.tickers}
    syms = [q["t"] for q in wl["symbols"]
            if (q["t"].upper() in want if want else q.get("fav"))]

    cutoff = datetime.now(timezone.utc) - timedelta(days=a.days)
    out, empty, failed = {}, [], 0

    for t in syms:
        try:
            items = news_for(t)
        except (urllib.error.URLError, ValueError, KeyError) as e:
            print(f"  ! {t}: {e}", file=sys.stderr)
            failed += 1
            time.sleep(PAUSE)
            continue
        keep = []
        for it in items:
            ts = when(it)
            if ts is None or ts < cutoff:
                continue
            keep.append({
                "title": it.get("title"),
                "source": it.get("source"),
                "time": it.get("time"),
                "ago": it.get("ago"),
                "text": (it.get("text") or "")[:400],
                "url": it.get("url"),
            })
            if len(keep) >= a.per:
                break
        if keep:
            out[t] = keep
            print(f"{t:6} {len(keep):>2} stories, newest {keep[0]['ago']}")
        else:
            empty.append(t)
        time.sleep(PAUSE)

    (HERE / "out").mkdir(exist_ok=True)
    path = HERE / "out" / "news-raw.json"
    path.write_text(json.dumps({
        "fetched": datetime.now().astimezone().replace(microsecond=0).isoformat(),
        "windowDays": a.days,
        "tickers": out,
        "nothingInWindow": empty,
    }, indent=1, ensure_ascii=False) + "\n")

    print(f"\n{len(out)} with news, {len(empty)} quiet"
          + (f" ({', '.join(empty)})" if empty else "")
          + f", {failed} failed -> {path}")


if __name__ == "__main__":
    main()
