#!/usr/bin/env python3
"""Attach a verified segment split to an existing spec and re-render.

    python3 bin/addsegs.py segs.json

segs.json: {"<spec file>": {"note": "...", "segments": [["Name", value, yoy|null, "note"|null], ...]}}
Values are in the spec's own unit. Warns if they do not sum to revenue.
"""
import json, subprocess, sys
from pathlib import Path

PALETTE = ["#e8502a", "#1b1b7a", "#c8a020", "#f0a030", "#6cb6e8", "#7cd07c"]

for path, info in json.load(open(sys.argv[1])).items():
    p = Path(path)
    s = json.load(open(p))
    rev, dec = s["revenue"], s.get("decimals", 1)
    out, total = [], 0.0
    for i, (name, val, yoy, note) in enumerate(info["segments"]):
        total += val
        out.append({"name": name, "value": val,
                    **({"yoy": round(yoy)} if yoy is not None else {}),
                    "note": note or f"{val / rev * 100:.0f}% of revenue",
                    "color": PALETTE[i % len(PALETTE)]})
    drift = total - rev
    flag = "" if abs(drift) <= max(0.15, 0.005 * abs(rev)) else f"  !! DRIFT {drift:+,.{dec}f}"
    s["segments"] = out
    json.dump(s, open(p, "w"), indent=1)
    r = subprocess.run(["python3", "bin/sankey.py", str(p), "--png"],
                       capture_output=True, text=True)
    warn = "".join(l for l in r.stderr.splitlines(keepends=True) if l.strip().startswith("!"))
    print(f"{s['ticker']:6}{len(out)} segs  sum={total:,.{dec}f} rev={rev:,.{dec}f}{flag}  {warn.strip()}")
