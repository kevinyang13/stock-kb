#!/usr/bin/env python3
"""Read one note out of a filing, without downloading the filing.

    python3 bin/edgar.py SNOW                 # list the revenue notes
    python3 bin/edgar.py SNOW R39             # print that note as rows
    python3 bin/edgar.py SNOW R39 --accn ...  # from a specific filing

EDGAR renders every statement and note of a filing as its own small R##.htm
report, and FilingSummary.xml names them. So a company's revenue
disaggregation note -- which is where the segment, product-line or end-market
split actually lives -- can be fetched on its own, instead of pulling a 3MB
10-Q and hoping the right table survives the trip.

This is the fallback for names bin/segfetch.py cannot reach. Figures read here
go into bin/segapply.py, which checks them against the chart before writing.
"""
import html
import json
import re
import sys
import urllib.request

UA = "stock-kb research (kevinyang13@gmail.com)"
TIMEOUT = 30
WANT = re.compile(r"disaggregat|revenue by|revenue from external|segment|"
                  r"net sales|product line|end market", re.I)
# the definition and reference boilerplate EDGAR appends under every table
STOP = re.compile(r"^X$|- Definition|Namespace Prefix")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


_tickers = None


def cik_for(sym):
    global _tickers
    if _tickers is None:
        _tickers = json.loads(get("https://www.sec.gov/files/company_tickers.json"))
    for row in _tickers.values():
        if row["ticker"].upper() == sym.upper():
            return f"{row['cik_str']:010d}"
    raise LookupError(f"{sym}: no CIK -- not an SEC filer?")


def filings(sym, forms=("10-Q", "10-K", "20-F", "6-K")):
    cik = cik_for(sym)
    r = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik}.json"))["filings"]["recent"]
    out = [(f, d, a.replace("-", ""))
           for f, d, a in zip(r["form"], r["filingDate"], r["accessionNumber"])
           if f in forms]
    return cik, out


def notes(cik, accn):
    """[(short name, R##.htm url)] for the revenue-ish notes in one filing."""
    base = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accn}"
    xml = get(base + "/FilingSummary.xml")
    out = []
    for m in re.finditer(r"<Report[^>]*>(.*?)</Report>", xml, re.S):
        name = re.search(r"<ShortName>(.*?)</ShortName>", m.group(1), re.S)
        fn = re.search(r"<HtmlFileName>(.*?)</HtmlFileName>", m.group(1), re.S)
        if name and fn and WANT.search(name.group(1)):
            out.append((name.group(1).strip(), f"{base}/{fn.group(1).strip()}"))
    return base, out


def rows(url):
    doc = get(url)
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", doc, re.S | re.I):
        cells = [re.sub(r"<[^>]+>", " ", c) for c in
                 re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S | re.I)]
        cells = [re.sub(r"\s+", " ", html.unescape(c).replace("\xa0", " ")).strip()
                 for c in cells]
        line = " | ".join(c for c in cells if c)
        if not line:
            continue
        if STOP.search(line):
            break
        out.append(line)
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return
    sym = args[0]
    accn = None
    if "--accn" in sys.argv:
        accn = sys.argv[sys.argv.index("--accn") + 1].replace("-", "")
    cik, fil = filings(sym)
    if accn is None:
        accn = next(a for _, _, a in fil)
    if len(args) == 1:
        for form, date, a in fil[:6]:
            print(f"{form:5} {date} {a}")
        base, hits = notes(cik, accn)
        print(f"\nnotes in {accn}:")
        for name, url in hits:
            print(f"  {url.rsplit('/', 1)[1]:10} {name}")
        return
    base = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accn}"
    page = args[1] if args[1].endswith(".htm") else args[1] + ".htm"
    for line in rows(f"{base}/{page}"):
        print(line)


if __name__ == "__main__":
    main()
