#!/usr/bin/env python3
"""Build the earnings-surprise spec for each statement on the Financials page.

    python3 bin/epsfetch.py              # every card without a spec yet
    python3 bin/epsfetch.py NBIS NVDA    # just these
    python3 bin/epsfetch.py --all        # refetch everything

Four reported quarters -- what the company earned against what the street
expected -- plus the consensus for the quarter it has not reported yet. The
figures come from Nasdaq's own endpoints, which carry Zacks' consensus:

    /api/company/<sym>/earnings-surprise     reported: actual, consensus, %
    /api/analyst/<sym>/earnings-forecast     ahead: consensus, range, revisions
    /api/analyst/<sym>/earnings-date         when the next one lands

Two things to keep in mind, both of which the card says out loud:

* this is **adjusted** EPS as the street scores it, not the GAAP EPS the
  income statement chart beside it is built from -- they differ by whatever a
  company excludes, and for some names that is most of the number
* for a foreign filer it is the **ADR's** earnings per share in US dollars,
  whatever currency the statement itself is filed in

A ticker that is not on Nasdaq, or whose company name there does not match
the card, is skipped rather than charted from someone else's numbers.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
PAUSE = 0.6
TIMEOUT = 25
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
KEEP = 4          # reported quarters on the chart
AHEAD = 1         # unreported quarters on the chart

# words that say nothing about which company this is
NOISE = re.compile(r"\b(inc|corp|corporation|co|ltd|limited|plc|nv|n\.v|sa|"
                   r"ag|holdings?|group|class|common|stock|shares?|ordinary|"
                   r"american|depositary|registry|new|york|the|technologies|"
                   r"company)\b", re.I)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def api(sym, path):
    d = get(f"https://api.nasdaq.com/api/{path}")
    if (d.get("status") or {}).get("rCode") != 200 or not d.get("data"):
        raise LookupError(f"{sym}: nothing at {path}")
    return d["data"]


def key_words(name):
    # strip punctuation first: "Tesla, Inc." tokenised as "tesla," matches
    # nothing, and that rejected two dozen perfectly good names
    clean = re.sub(r"[^a-z0-9 ]+", " ", (name or "").lower())
    return [w for w in NOISE.sub(" ", clean).split()
            if len(w) > 2 and not w.isdigit()]


def initials(name):
    clean = re.sub(r"[^a-z0-9 ]+", " ", (name or "").lower())
    return "".join(w[0] for w in clean.split())


def same_company(ours, theirs):
    """Nasdaq is asked by ticker, and tickers are reused -- the card has to
    recognise the name that comes back before any of its figures are used.

    The card's names are short ("AMD", "SpaceX", "TSMC") and Nasdaq's are the
    full registered ones, so an exact match is no test at all. Four ways to
    recognise a name, and nothing else passes."""
    a, b = key_words(ours), key_words(theirs)
    if set(a) & set(b):                                   # a shared word
        return True
    for x in a:                                           # Space / SpaceX
        for y in b:
            if len(x) >= 4 and len(y) >= 4 and (x.startswith(y) or y.startswith(x)):
                return True
    ours_raw = re.sub(r"[^a-z0-9]+", "", (ours or "").lower())
    if ours_raw and initials(theirs).startswith(ours_raw):  # AMD, IBM, TSMC
        return True
    first = lambda n: re.sub(r"[^a-z0-9]+", " ", (n or "").lower()).split()
    fa, fb = first(ours), first(theirs)
    return bool(fa and fb and fa[0] == fb[0] and len(fa[0]) > 1)  # "Nu Holdings"


def num(v):
    if v in (None, "", "N/A"):
        return None
    try:
        return float(str(v).replace("$", "").replace(",", ""))
    except ValueError:
        return None


# A row's actual and its consensus are served as one pair, but they are not
# guaranteed to share a basis: Nasdaq has handed back a GAAP actual against an
# adjusted consensus more than once, and the resulting "surprise" is then an
# artefact of the mismatch rather than a result. Alphabet's Jun 2026 row is
# $9.11 against $2.88 -- a 216% beat -- because $6.26 of that EPS was an
# unrealised gain on equity securities that the consensus never included; on
# the same basis the quarter was roughly level. GE Vernova's Dec 2025 row does
# the same thing with the Prolec remeasurement gain.
#
# There is no field that states the basis, so the pair is judged on its own
# plausibility: a profitable company does not miss or beat its own consensus by
# half. Both sides must be positive, because a loss maker crossing zero makes
# the ratio meaningless rather than wrong -- an actual of -$38.25 against
# -$3.41 is arithmetic, not a bad figure.
BASIS = ("EPS as the vendor scores it -- usually the street's adjusted figure, "
         "which is not the GAAP EPS the income statement is built from. The "
         "feed states no basis and has mixed GAAP actuals with adjusted "
         "consensus, so a pair that cannot be shown to share one is marked "
         "basisUnverified and carries no surprise figure.")

MISMATCH_REL = 0.40     # gap against the estimate
MISMATCH_ABS = 0.15     # and at least this many cents, so rounding is not it


def basis_unverified(actual, estimate):
    """True when the pair cannot be shown to share a basis, so no surprise
    figure may be published for it."""
    if actual is None or estimate is None:
        return False
    if actual <= 0 or estimate <= 0:
        return False
    gap = abs(actual - estimate)
    return gap >= MISMATCH_ABS and gap / estimate > MISMATCH_REL


def label_of(fiscal_end):
    """'Jun 2026' -> "Jun '26". The card's own period names are fiscal and do
    not line up across companies; the quarter end does."""
    try:
        d = datetime.strptime(fiscal_end.strip(), "%b %Y")
    except (ValueError, AttributeError):
        return (fiscal_end or "").strip()
    return f"{d:%b} '{d:%y}"


def when(s):
    try:
        return datetime.strptime(s.strip(), "%m/%d/%Y")
    except (ValueError, AttributeError):
        return None


def sort_key(fiscal_end):
    try:
        return datetime.strptime(fiscal_end.strip(), "%b %Y")
    except (ValueError, AttributeError):
        return datetime.min


def build(item):
    sym = item["t"]
    info = api(sym, f"quote/{sym}/info?assetclass=stocks")
    theirs = info.get("companyName") or ""
    if not same_company(item.get("company"), theirs):
        raise LookupError(f"{sym}: Nasdaq has {theirs!r}, the card has "
                          f"{item.get('company')!r}")

    rows = (api(sym, f"company/{sym}/earnings-surprise")
            .get("earningsSurpriseTable") or {}).get("rows") or []
    done = []
    for r in sorted(rows, key=lambda r: sort_key(r.get("fiscalQtrEnd", ""))):
        act, est = num(r.get("eps")), num(r.get("consensusForecast"))
        if act is None or est is None:
            continue
        rep = when(r.get("dateReported"))
        row = {
            "label": label_of(r.get("fiscalQtrEnd")),
            "quarterEnd": (r.get("fiscalQtrEnd") or "").strip(),
            "reported": f"{rep:%b %-d, %Y}" if rep else None,
            "actual": round(act, 4),
            "estimate": round(est, 4),
            "surprise": round(act - est, 4),
            "surprisePct": num(r.get("percentageSurprise")),
        }
        if basis_unverified(act, est):
            row["basisUnverified"] = True
        done.append(row)
    if not done:
        raise LookupError(f"{sym}: no reported quarters")
    done = done[-KEEP:]

    ahead = []
    try:
        fc = (api(sym, f"analyst/{sym}/earnings-forecast")
              .get("quarterlyForecast") or {}).get("rows") or []
    except (urllib.error.URLError, LookupError, ValueError):
        fc = []
    seen = {p["quarterEnd"] for p in done}
    for r in fc:
        end = (r.get("fiscalEnd") or "").strip()
        est = num(r.get("consensusEPSForecast"))
        if end in seen or est is None or sort_key(end) <= sort_key(done[-1]["quarterEnd"]):
            continue
        ahead.append({
            "label": label_of(end),
            "quarterEnd": end,
            "estimate": round(est, 4),
            "high": num(r.get("highEPSForecast")),
            "low": num(r.get("lowEPSForecast")),
            "analysts": r.get("noOfEstimates"),
            "up": r.get("up"),
            "down": r.get("down"),
        })
        if len(ahead) >= AHEAD:
            break

    due = None
    try:
        txt = api(sym, f"analyst/{sym}/earnings-date").get("announcement") or ""
        m = re.search(r"([A-Z][a-z]{2} \d{1,2}, \d{4})", txt)
        due = m.group(1) if m else None
    except (urllib.error.URLError, LookupError, ValueError):
        pass
    if ahead and due:
        ahead[0]["due"] = due

    return {
        "ticker": sym,
        "company": item["company"],
        "currency": "$",
        "basis": BASIS,
        "source": ("Nasdaq earnings surprise and analyst forecast endpoints "
                   "(Zacks consensus), read " +
                   datetime.now().strftime("%b %-d, %Y") + "."),
        "reported": done,
        "ahead": ahead,
    }


def main():
    args = {a.upper() for a in sys.argv[1:] if not a.startswith("--")}
    refetch = "--all" in sys.argv
    items = json.loads((HERE / "financials.json").read_text())["items"]

    ok = skipped = failed = 0
    for item in items:
        t = item["t"]
        if args and t.upper() not in args:
            continue
        out = HERE / "examples" / f"{t.lower()}-eps.json"
        if out.exists() and not refetch and not args:
            skipped += 1
            continue
        try:
            spec = build(item)
        except (urllib.error.URLError, LookupError, ValueError, KeyError) as e:
            print(f"  ! {e}", file=sys.stderr)
            failed += 1
        else:
            out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
            last = spec["reported"][-1]
            nxt = spec["ahead"][0]["estimate"] if spec["ahead"] else None
            print(f"{t:6} {len(spec['reported'])}q  last {last['label']}: "
                  f"actual {last['actual']:+.2f} vs {last['estimate']:+.2f}"
                  + (f"  next {nxt:+.2f}" if nxt is not None else "  next --"))
            ok += 1
        time.sleep(PAUSE)

    print(f"\nwrote {ok}  skipped {skipped}  failed {failed}")


if __name__ == "__main__":
    main()
