#!/usr/bin/env python3
"""Fill in the revenue-by-segment split on the income statement specs.

    python3 bin/segfetch.py --dry-run        # report, write nothing
    python3 bin/segfetch.py PLTR NOW         # write just these

The skill forbids stockanalysis's *rendered* revenue-by-segment page, and
rightly: it shows annual figures even under ?p=quarterly, so NVDA's two
segments there sum to $303B against $96.2B of quarterly revenue. The page's
own data endpoint is a different thing -- it carries a `quarterly` array keyed
by period end, which is what this reads.

Every split still has to earn its place:

  * the column has to be the same period end the card already shows
  * the segments have to sum to the revenue the chart already draws, within
    0.5%, or the split is rejected rather than written

A rejected or missing split leaves the spec alone. Nothing is guessed, and a
company that genuinely reports no split keeps its single bar.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sadata import UA, hydrate, path_for

HERE = Path(__file__).resolve().parent.parent
PAUSE = 0.7
TIMEOUT = 25
TOL = 0.005          # segments must sum to charted revenue within 0.5%

# The segment colours the hand-built charts already use, in the order they
# were used there, so a fetched split looks like the rest of the page.
PALETTE = ["#e8502a", "#1b1b7a", "#c8a020", "#f0a030", "#6cb6e8",
           "#7cd07c", "#2f9e6e"]

# Series that are a total, a memo line or a restatement of the whole, not a
# segment of it. Summing these on top of the real segments doubles revenue.
SKIP = re.compile(r"^(total|net revenue|net sales|revenues?|consolidated"
                  r"|total revenue)s?$", re.I)


def fetch(sym):
    url = (f"https://stockanalysis.com/{path_for(sym)}"
           f"/metrics/revenue-by-segment/__data.json?p=quarterly")
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        doc = json.loads(r.read().decode("utf-8", "replace"))
    for n in doc.get("nodes") or []:
        if isinstance(n, dict) and n.get("type") == "data":
            d = hydrate(n["data"])
            if isinstance(d, dict) and "data" in d:
                inner = d["data"]
                if isinstance(inner, dict) and isinstance(inner.get("data"), dict):
                    return inner["data"].get("quarterly") or []
    raise LookupError(f"{sym}: no quarterly segment series")


def at(series, want):
    """(value, growth %) for the column whose x is `want`, or None."""
    for pt in series.get("values") or []:
        try:
            d = date.fromisoformat(pt["x"])
        except (ValueError, TypeError, KeyError):
            continue
        if abs((d - want).days) <= 7:
            return pt.get("y"), pt.get("growth")
    return None


def period_end(item):
    m = re.search(r"([A-Z][a-z]{2} \d{1,2}, \d{4})", item.get("periodEnd", ""))
    if not m:
        raise ValueError(f"cannot read a date from {item.get('periodEnd')!r}")
    return datetime.strptime(m.group(1), "%b %d, %Y").date()


def split_for(sym, want, revenue, div, dec):
    """[(name, value in the spec's unit, yoy %)] or a reason it was refused."""
    rows = []
    for s in fetch(sym):
        name = (s.get("name") or "").strip()
        if not name or SKIP.match(name):
            continue
        hit = at(s, want)
        if hit is None or hit[0] is None:
            continue
        rows.append((name, hit[0], hit[1]))
    if not rows:
        return None, "no column for this quarter"
    # The sum is the real guard. This endpoint buckets every filer into
    # calendar quarters, so a fiscal-quarter filer's own period end is simply
    # not in it -- and a column that is a different quarter will not foot
    # against the revenue the chart already draws.
    total = sum(v for _, v, _ in rows) / div
    if abs(total - revenue) > max(abs(revenue) * TOL, 10 ** -dec):
        return None, (f"sums to {total:,.{dec}f} against the chart's "
                      f"{revenue:,.{dec}f}")

    out = [(n, round(v / div, dec), None if g is None else round(g))
           for n, v, g in rows]
    # eliminations and dormant segments come back as a rounded zero; a band of
    # zero width draws nothing but still takes a label and a colour
    out = [r for r in out if abs(r[1]) >= 10 ** -dec / 2]
    neg = [n for n, v, _ in out if v < 0]
    if neg:
        return None, f"negative segment(s): {', '.join(neg)}"
    out.sort(key=lambda r: -r[1])
    return out, None


def main():
    args = {a.upper() for a in sys.argv[1:] if not a.startswith("--")}
    dry = "--dry-run" in sys.argv
    items = {i["t"]: i for i in
             json.loads((HERE / "financials.json").read_text())["items"]}

    specs = []
    for p in sorted((HERE / "examples").glob("*.json")):
        if p.name.endswith("-debt.json"):
            continue
        try:
            s = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        if "revenue" in s and "ticker" in s:
            specs.append((p, s))

    wrote, refused, missing = [], [], []
    for p, spec in specs:
        t = spec["ticker"]
        if args and t.upper() not in args:
            continue
        if not args and len(spec.get("segments") or []) > 1:
            continue                      # already split
        item = items.get(t)
        if not item:
            continue
        div = {"M": 1e6, "B": 1e9, "T": 1e12}[spec.get("unit", "M")]
        dec = spec.get("decimals", 1)
        try:
            rows, why = split_for(t, period_end(item), spec["revenue"], div, dec)
        except (urllib.error.URLError, LookupError, ValueError, KeyError) as e:
            missing.append((t, str(e)))
            print(f"{t:6} --  {e}")
        else:
            if rows is None:
                refused.append((t, why))
                print(f"{t:6} !!  {why}")
            else:
                shown = ", ".join(f"{n} {v:,.{dec}f}" for n, v, _ in rows)
                print(f"{t:6} ok  {len(rows)}: {shown}")
                if not dry:
                    spec["segments"] = [
                        {"name": n, "value": v,
                         **({"yoy": g} if g is not None else {}),
                         "color": PALETTE[i % len(PALETTE)]}
                        for i, (n, v, g) in enumerate(rows)]
                    p.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
                    wrote.append(t)
        time.sleep(PAUSE)

    print(f"\n{'would write' if dry else 'wrote'} "
          f"{len(wrote) if not dry else '-'}  "
          f"refused {len(refused)}  no data {len(missing)}")
    for t, why in refused:
        print(f"  REFUSED {t}: {why}")
    for t, why in missing:
        print(f"  NO DATA {t}: {why}")


if __name__ == "__main__":
    main()
