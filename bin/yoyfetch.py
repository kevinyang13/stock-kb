#!/usr/bin/env python3
"""Add year-ago figures to the income statement specs, for the chart hovers.

    python3 bin/yoyfetch.py            # every spec
    python3 bin/yoyfetch.py NBIS TSM   # just these

Writes a `prior` block into each `examples/<ticker>-<period>.json`, keyed by
the node name the chart draws.

The figures come from stockanalysis.com, but five charts were built from
filings instead, and on those the two sources disagree about where some costs
sit -- stockanalysis puts roughly $174.6M of NBIS share-based compensation
below the operating line, so its R&D reads $75.1M against the filing's
$191.0M. A year-over-year number from the wrong basis would contradict the
bar it is attached to.

So each line polices itself: the year-ago figure is kept only when the
source's *current* quarter for that line matches what the chart already
draws. Where the bases differ, the line simply gets no growth row.
"""
import json
import re
import sys
import time
import urllib.error
from datetime import date, datetime, timedelta
from pathlib import Path

from sadata import financial_data

HERE = Path(__file__).resolve().parent.parent
PAUSE = 0.7

# Chart node name -> the field stockanalysis uses. Segment nodes are not here:
# segment splits come from each company's own release, not from this source.
FIELDS = {
    "Revenue": "revenue",
    "Gross profit": "gp",
    "Cost of revenue": "cor",
    "R&D": "rnd",
    "SG&A": "sgna",
    "Depreciation & amortization": "depAmorEbitda",
    "Operating expenses": "opex",
    "Operating profit": "opinc",
    "Net profit": "netinc",
    "Net loss": "netinc",
    "Tax": "taxexp",
}


def spec_value(spec, name):
    """What the chart draws for this node, in the spec's own unit."""
    direct = {
        "Revenue": "revenue", "Gross profit": "gross_profit",
        "Cost of revenue": "cost_of_revenue",
        "Operating profit": "operating_profit", "Net profit": "net_profit",
        "Net loss": "net_loss", "Tax": "tax", "Operating expenses": "opex_total",
    }
    if name in direct and spec.get(direct[name]) is not None:
        return spec[direct[name]]
    if name == "Operating expenses":
        items = spec.get("opex_items") or []
        return sum(i["value"] for i in items) or None
    for i in spec.get("opex_items") or []:
        if i["name"] == name:
            return i["value"]
    return None


def columns(fd, want):
    """(this quarter, the same quarter a year earlier) as column indexes."""
    keys = fd.get("datekey") or []
    dates = []
    for k in keys:
        try:
            dates.append(date.fromisoformat(k))
        except (ValueError, TypeError):
            dates.append(None)
    cur = next((i for i, d in enumerate(dates) if d == want), None)
    if cur is None:
        near = [(abs(d - want), i) for i, d in enumerate(dates) if d]
        if not near or min(near)[0] > timedelta(days=7):
            raise LookupError(f"no column for {want}")
        cur = min(near)[1]

    # prefer the same fiscal quarter one year back; fall back on the date
    fq, fy = fd.get("fiscalQuarter") or [], fd.get("fiscalYear") or []
    if cur < len(fq) and cur < len(fy):
        try:
            tgt = str(int(fy[cur]) - 1)
            for i in range(len(dates)):
                if i < len(fq) and fq[i] == fq[cur] and fy[i] == tgt:
                    return cur, i
        except (TypeError, ValueError):
            pass
    back = dates[cur] - timedelta(days=365)
    near = [(abs(d - back), i) for i, d in enumerate(dates) if d and i != cur]
    if near and min(near)[0] <= timedelta(days=20):
        return cur, min(near)[1]
    raise LookupError(f"no year-ago column for {want}")


def build(spec, want):
    fd = financial_data(spec["ticker"], "income-statement")
    cur, ago = columns(fd, want)
    # specs come in millions, billions or trillions of the filed currency --
    # SK Hynix files in trillions of won, and defaulting it to millions made
    # every line look like a basis mismatch
    div = {"M": 1e6, "B": 1e9, "T": 1e12}[spec.get("unit", "M")]
    dec = spec.get("decimals", 1)

    prior, skipped, flipped = {}, [], []
    names = ([n for n in FIELDS if spec_value(spec, n) is not None] +
             [i["name"] for i in spec.get("opex_items") or []
              if i["name"] in FIELDS])
    for name in dict.fromkeys(names):
        col = fd.get(FIELDS[name]) or []
        if cur >= len(col) or ago >= len(col):
            continue
        now, was = col[cur], col[ago]
        if now is None or was is None:
            continue
        mine = spec_value(spec, name)
        # the chart draws costs and losses as positive magnitudes while the
        # source signs them, so work out the convention from this quarter and
        # apply the same one to the year-ago figure
        factor = 1 if (now >= 0) == (mine >= 0) else -1
        now_s, was_s = now * factor, was * factor
        tol = max(0.15 if div == 1e6 else 0.02, abs(mine) * 0.01)
        if abs(now_s / div - mine) > tol:
            skipped.append(name)      # different basis: see the module docstring
            continue
        if (was_s > 0) != (now_s > 0):
            # the line changed sign -- NBIS's "net loss" node was a $584.4M
            # net profit a year earlier, on the Yandex disposal. A percentage
            # across that is meaningless, so the node gets no growth row.
            flipped.append(name)
            continue
        prior[name] = round(was_s / div, dec)
    return prior, skipped, flipped


def main():
    args = {a.upper() for a in sys.argv[1:] if not a.startswith("--")}
    items = {i["t"]: i for i in
             json.loads((HERE / "financials.json").read_text())["items"]}

    specs = {}
    for p in sorted((HERE / "examples").glob("*.json")):
        if p.name.endswith("-debt.json"):
            continue
        try:
            s = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        if "revenue" in s and "ticker" in s:
            specs[s["ticker"]] = (p, s)

    ok = failed = 0
    for t, (p, spec) in specs.items():
        if args and t.upper() not in args:
            continue
        item = items.get(t)
        if not item:
            continue
        m = re.search(r"([A-Z][a-z]{2} \d{1,2}, \d{4})", item.get("periodEnd", ""))
        if not m:
            print(f"  ! {t}: no date in {item.get('periodEnd')!r}", file=sys.stderr)
            failed += 1
            continue
        want = datetime.strptime(m.group(1), "%b %d, %Y").date()
        try:
            prior, skipped, flipped = build(spec, want)
        except (urllib.error.URLError, LookupError, ValueError, KeyError) as e:
            print(f"  ! {t}: {e}", file=sys.stderr)
            failed += 1
        else:
            if prior:
                spec["prior"] = prior
            else:
                spec.pop("prior", None)
            p.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
            ok += 1
            bits = []
            if skipped:
                bits.append(f"different basis: {', '.join(skipped)}")
            if flipped:
                bits.append(f"changed sign: {', '.join(flipped)}")
            note = f"  (no growth row -- {'; '.join(bits)})" if bits else ""
            print(f"{t:6} {len(prior)} line(s){note}")
        time.sleep(PAUSE)
    print(f"\nupdated {ok}  failed {failed}")


if __name__ == "__main__":
    main()
