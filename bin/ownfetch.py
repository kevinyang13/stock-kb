#!/usr/bin/env python3
"""Build the share-ownership spec behind the pie on each Financials card.

Two sources, each used for what only it can give:

- **Slice sizes** come from stockanalysis's statistics endpoint, which
  publishes "Owned by Institutions (%)" and "Owned by Insiders (%)" as a
  netted, mutually consistent pair. The residual to 100% is everyone else.
- **The split inside the institutional slice, and the holder names in the
  tooltip,** come from the SEC's own Form 13F data set -- every institutional
  manager's filed position, primary source.

Mixing them is deliberate. A raw 13F sum is not a clean ownership percentage:
managers with shared discretion report the same shares twice, so summing the
table gives NVDA 24.8bn shares against 24.1bn outstanding. The vendor pair is
internally consistent and sums to 100%; the filings are the only place the
holders are named. The card says which number came from where.

    python3 bin/ownfetch.py --data <dir>            # every card
    python3 bin/ownfetch.py --data <dir> NVDA MU    # just these

<dir> is an unpacked SEC Form 13F data set:
https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets
It needs INFOTABLE.tsv, COVERPAGE.tsv and SUBMISSION.tsv. The set is ~400MB
unpacked and is not kept in the repo -- download it, point at it, delete it.

Nothing is guessed. A ticker whose CUSIP cannot be resolved, or whose numbers
do not reconcile, is reported and skipped.
"""
import argparse
import collections
import csv
import json
import re
import statistics
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAUSE = 0.7

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
SEC_UA = "stock-kb research kevinyang13@gmail.com"

# A filer's reported VALUE divided by its reported share count should come out
# at the period-end price. Filings that miss by more than this are not trusted.
PRICE_TOL = 0.06
# Form 13F moved VALUE from thousands of dollars to whole dollars in 2023 and
# a minority of filers still report the old way. Their share counts are fine,
# so they are kept rather than dropped -- see keep_filing().
THOUSANDS = 1000.0
TOP_N = 5


# ------------------------------------------------------------------ vendor

def hydrate(flat):
    """devalue's flattened payload: every int indexes back into the array."""
    seen = {}

    def walk(i):
        if isinstance(i, str):
            return i
        if not isinstance(i, int) or i < 0:
            return None
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


def statistics_block(sym):
    """`shares` from the statistics page: outstanding, insider %, institution %."""
    url = f"https://stockanalysis.com/stocks/{sym.lower()}/statistics/__data.json"
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:
        doc = json.loads(r.read().decode("utf-8", "replace"))
    for n in doc.get("nodes") or []:
        if isinstance(n, dict) and n.get("type") == "data":
            d = hydrate(n["data"])
            if isinstance(d, dict) and "shares" in d:
                return {row["id"]: row for row in d["shares"]["data"]}
    raise LookupError(f"{sym}: no shares block")


def num(block, key):
    """The unrounded `hover` figure, which carries more digits than `value`."""
    row = block.get(key)
    if not row:
        return None
    raw = str(row.get("hover") or row.get("value") or "").replace(",", "")
    raw = raw.replace("%", "").strip()
    try:
        return float(raw)
    except ValueError:
        return None


# --------------------------------------------------------------- 13F data

def load_filings(data_dir):
    """accession -> (manager name, period) for the latest period in the set.

    Amendments that restate a filing replace it; amendments that only add
    holdings are kept alongside the original, which is what the form means.
    """
    sub = {}
    with open(data_dir / "SUBMISSION.tsv", newline="", encoding="utf-8",
              errors="replace") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            sub[row["ACCESSION_NUMBER"]] = (row["CIK"], row["PERIODOFREPORT"],
                                            row["SUBMISSIONTYPE"],
                                            row["FILING_DATE"])
    periods = collections.Counter(v[1] for v in sub.values())
    period = max(periods, key=lambda p: (count_rank(p), periods[p]))

    cover = {}
    with open(data_dir / "COVERPAGE.tsv", newline="", encoding="utf-8",
              errors="replace") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            cover[row["ACCESSION_NUMBER"]] = (row["FILINGMANAGER_NAME"],
                                              row["AMENDMENTTYPE"] or "")

    # one filing per manager: the newest restatement if there is one
    best = {}
    for acc, (cik, per, typ, filed) in sub.items():
        if per != period or not typ.startswith("13F-HR"):
            continue
        name, amd = cover.get(acc, ("", ""))
        if amd.upper().startswith("NEW HOLDINGS"):
            best[acc] = (name, acc)          # additive: stands on its own
            continue
        prev = best.get(cik)
        if prev is None or filed >= prev[0]:
            best[cik] = (filed, name, acc)

    out = {}
    for k, v in best.items():
        if len(v) == 2:
            out[v[1]] = v[0]
        else:
            out[v[2]] = v[1]
    return out, period


def count_rank(period):
    """Sort 'DD-MON-YYYY' chronologically without a locale-dependent parse."""
    mon = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
           "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    try:
        d, m, y = period.split("-")
        return (int(y), mon.index(m.upper()) + 1, int(d))
    except Exception:
        return (0, 0, 0)


def scan_holdings(data_dir, cusips):
    """Per CUSIP: {accession: [shares, value]} for ordinary long stock only.

    Puts, calls and principal-amount lines are excluded: the pie is about who
    owns the shares, and an option position is not ownership of them.
    """
    want = set(cusips)
    agg = {c: collections.defaultdict(lambda: [0, 0.0]) for c in want}
    with open(data_dir / "INFOTABLE.tsv", newline="", encoding="utf-8",
              errors="replace") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            c = row["CUSIP"]
            if c not in want or row["PUTCALL"] or row["SSHPRNAMTTYPE"] != "SH":
                continue
            a = agg[c][row["ACCESSION_NUMBER"]]
            try:
                a[0] += int(row["SSHPRNAMT"] or 0)
                a[1] += float(row["VALUE"] or 0)
            except ValueError:
                continue
    return agg


def resolve_cusips(data_dir, names):
    """ticker -> candidate CUSIPs, by matching the issuer name filers wrote.

    Filers type the issuer name freehand, so this is a loose match that is
    allowed to return several candidates. It is never the last word: the
    caller keeps a candidate only once its filers' implied price agrees with
    the ticker's own price, which a wrong company's CUSIP will not do.
    """
    pats = {t: re.compile(r"\b" + re.escape(n.upper()), re.I)
            for t, n in names.items()}
    hits = {t: collections.Counter() for t in names}
    with open(data_dir / "INFOTABLE.tsv", newline="", encoding="utf-8",
              errors="replace") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["PUTCALL"] or row["SSHPRNAMTTYPE"] != "SH":
                continue
            iss = row["NAMEOFISSUER"].upper()
            for t, pat in pats.items():
                if pat.match(iss):
                    hits[t][row["CUSIP"]] += 1
    return {t: [c for c, _ in h.most_common(4)] for t, h in hits.items()}


def keep_filing(shares, value, price):
    """Is this filing's share count usable?

    The share count is the figure the pie needs, and VALUE is the only thing
    in the table that can check it. A filing passes if its implied price is
    the period-end price, or that price over a thousand -- the pre-2023 unit,
    which says nothing about the shares. Anything else is a broken row: one
    pension fund reported 7.0bn NVDA shares, 29% of the company and four times
    its own total fund, and a naive top-five would have published it.
    """
    if shares <= 0 or price <= 0:
        return False
    implied = value / shares
    for scale in (1.0, THOUSANDS):
        if abs(implied * scale - price) <= PRICE_TOL * price:
            return True
    return False


def close_on(sym, iso):
    """The ticker's own close on `iso`, or the last session before it.

    This is what makes the CUSIP match safe. A freehand issuer-name match can
    land on the wrong company; that company's filers will imply its own share
    price, not this ticker's, and the candidate is dropped.
    """
    url = (f"https://stockanalysis.com/stocks/{sym.lower()}"
           f"/history/__data.json?period=Monthly")
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:
        doc = json.loads(r.read().decode("utf-8", "replace"))
    for n in doc.get("nodes") or []:
        if isinstance(n, dict) and n.get("type") == "data":
            d = hydrate(n["data"])
            if isinstance(d, dict) and isinstance(d.get("data"), dict):
                rows = d["data"].get("data") or []
                on = [r for r in rows if r.get("t") and r["t"] <= iso]
                if on:
                    return float(max(on, key=lambda r: r["t"])["c"])
    raise LookupError(f"{sym}: no price on or before {iso}")


def iso_period(period):
    mon = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
           "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    d, m, y = period.split("-")
    return f"{int(y):04d}-{mon.index(m.upper()) + 1:02d}-{int(d):02d}"


def is_passive(name, prefixes):
    up = name.upper().lstrip()
    return any(up.startswith(p) for p in prefixes)


def build(sym, company, cusips, agg, filings, period, prefixes):
    """One ticker's spec, or a reason it cannot be built."""
    iso = iso_period(period)
    price = close_on(sym, iso)

    # Pick the candidate CUSIP whose filers imply this ticker's own price.
    chosen, kept = None, None
    for c in cusips:
        rows = agg.get(c) or {}
        good = {a: v for a, v in rows.items()
                if a in filings and keep_filing(v[0], v[1], price)}
        if not good:
            continue
        if chosen is None or len(good) > len(kept):
            chosen, kept = c, good
    if not chosen:
        raise LookupError(f"no CUSIP whose filers imply a "
                          f"${price:,.2f} share on {iso}")

    dropped = len([a for a in (agg[chosen] or {}) if a in filings]) - len(kept)

    holders = []
    for acc, (sh, _val) in kept.items():
        holders.append((filings[acc], sh))
    holders.sort(key=lambda h: -h[1])

    total = sum(sh for _n, sh in holders)
    passive = sum(sh for n, sh in holders if is_passive(n, prefixes))
    if total <= 0:
        raise LookupError("no usable 13F shares")

    return {
        "cusip": chosen,
        "price": price,
        "asOf": iso,
        "filers": len(kept),
        "dropped": dropped,
        "shares13f": total,
        "passive13f": passive,
        "holders": [{"name": n, "shares": sh,
                     "passive": is_passive(n, prefixes)}
                    for n, sh in holders[:12]],
    }


def spec_for(sym, company, thirteenf, stats):
    """Turn the two sources into the four slices the pie draws."""
    out_shares = num(stats, "sharesout")
    inst = num(stats, "sharesInstitutions")
    insiders = num(stats, "sharesInsiders")
    if out_shares is None or inst is None:
        raise LookupError("statistics page has no shares outstanding "
                          "or institutional percentage")
    insiders = insiders or 0.0

    retail = 100.0 - inst - insiders
    if retail < 0:
        raise LookupError(f"institutions {inst:.2f}% + insiders "
                          f"{insiders:.2f}% exceed 100%; no honest residual")

    share_passive = thirteenf["passive13f"] / thirteenf["shares13f"]
    index_pct = inst * share_passive
    active_pct = inst - index_pct

    def pct_of_out(sh):
        return 100.0 * sh / out_shares

    return {
        "ticker": sym,
        "company": company,
        "sharesOut": out_shares,
        "asOf13F": thirteenf["asOf"],
        "cusip": thirteenf["cusip"],
        "filers": thirteenf["filers"],
        "dropped": thirteenf["dropped"],
        "slices": [
            {"key": "index", "label": "Index & ETF managers",
             "pct": index_pct},
            {"key": "active", "label": "Other institutions",
             "pct": active_pct},
            {"key": "insiders", "label": "Insiders", "pct": insiders},
            {"key": "retail", "label": "Retail & other", "pct": retail},
        ],
        "top": {
            "index": [{"name": h["name"], "pct": pct_of_out(h["shares"])}
                      for h in thirteenf["holders"] if h["passive"]][:TOP_N],
            "active": [{"name": h["name"], "pct": pct_of_out(h["shares"])}
                       for h in thirteenf["holders"] if not h["passive"]][:TOP_N],
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True,
                    help="unpacked SEC Form 13F data set directory")
    ap.add_argument("tickers", nargs="*")
    args = ap.parse_args()

    data_dir = Path(args.data)
    items = json.loads((ROOT / "financials.json").read_text())
    if isinstance(items, dict):
        items = items.get("items") or []
    want = [t.upper() for t in args.tickers]
    items = [i for i in items if not want or i["t"].upper() in want]
    if not items:
        sys.exit("no matching cards in financials.json")

    prefixes = json.loads((HERE / "passive-managers.json").read_text())["prefixes"]

    print(f"reading {data_dir} ...")
    filings, period = load_filings(data_dir)
    print(f"  {len(filings):,} filings for {period}")

    names = {i["t"]: i["company"] for i in items}
    print("resolving CUSIPs by issuer name (one pass over INFOTABLE) ...")
    cands = resolve_cusips(data_dir, names)
    every = sorted({c for cs in cands.values() for c in cs})
    print(f"  {len(every)} candidate CUSIPs")

    print("reading holdings (second pass) ...")
    agg = scan_holdings(data_dir, every)

    outdir = ROOT / "examples"
    ok = skipped = 0
    for i in items:
        sym, company = i["t"], i["company"]
        try:
            stats = statistics_block(sym)
            time.sleep(PAUSE)
            tf = build(sym, company, cands.get(sym) or [], agg, filings,
                       period, prefixes)
            time.sleep(PAUSE)
            spec = spec_for(sym, company, tf, stats)
        except Exception as e:
            print(f"  ! {sym}: {e}")
            skipped += 1
            continue

        p = outdir / f"{sym.lower()}-own.json"
        p.write_text(json.dumps(spec, indent=1) + "\n")
        sl = {s["key"]: s["pct"] for s in spec["slices"]}
        print(f"  {sym:6s} index {sl['index']:5.1f}%  active {sl['active']:5.1f}%  "
              f"insiders {sl['insiders']:5.2f}%  retail {sl['retail']:5.1f}%  "
              f"({spec['filers']:,} filers, {spec['dropped']} dropped)")
        ok += 1

    print(f"\nwrote {ok} specs, skipped {skipped}")


if __name__ == "__main__":
    main()
