#!/usr/bin/env python3
"""Read a statement from stockanalysis.com's own data endpoint.

There is no financials API -- every documented shape answers {"status":404}.
The pages are SvelteKit, so the data sits at

    /<path>/financials/<statement>/__data.json?p=quarterly

in devalue's flattened format: a `data` array in which every integer is an
index back into the same array. It has to be hydrated before anything can be
read out of it. Once hydrated, `financialData` holds each line as a list
parallel to `datekey`.

One request per statement, exact unrounded figures, and no table to misparse.
"""
import json
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
TIMEOUT = 25

# Everything else resolves to /stocks/<ticker>/. Nintendo is not a US listing.
PATHS = {"7974": "quote/tyo/7974"}


def hydrate(flat):
    """Decode the flattened payload: every int indexes back into `flat`."""
    seen = {}

    def walk(i):
        if isinstance(i, str):
            return i
        if not isinstance(i, int) or i < 0:
            return None               # -1 undefined, -2 hole, and friends
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


def path_for(sym):
    return PATHS.get(sym, "stocks/" + sym.lower())


def financial_data(sym, statement, period="quarterly"):
    """The hydrated `financialData` block for one statement."""
    url = (f"https://stockanalysis.com/{path_for(sym)}"
           f"/financials/{statement}/__data.json?p={period}")
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        doc = json.loads(r.read().decode("utf-8", "replace"))
    for n in doc.get("nodes") or []:
        if isinstance(n, dict) and n.get("type") == "data":
            d = hydrate(n["data"])
            if isinstance(d, dict) and "financialData" in d:
                return d["financialData"]
    raise LookupError(f"{sym}: no financialData in {statement}")
