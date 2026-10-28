#!/usr/bin/env python3
"""Point each Financials card at its earnings chart, and say what it is.

Adds `eps` to the item in financials.json wherever examples/<t>-eps.json
exists, and a note that this chart is adjusted EPS against the street's
consensus -- a different basis from the GAAP income statement beside it. Two
EPS figures on one card invite exactly the wrong comparison, so the card says
which is which.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
HEAD = "Earnings chart:"


def money(v):
    """"$-0.12" puts the sign in the wrong place for a loss."""
    return f"{'-' if v < 0 else ''}${abs(v):,.2f}"


def note_for(spec):
    done, ahead = spec["reported"], spec.get("ahead") or []
    last = done[-1]
    d = last["actual"] - last["estimate"]
    pct = last.get("surprisePct")
    word = "beat" if d > 0 else ("missed" if d < 0 else "met")
    swing = (f"{word} by ${abs(d):,.2f}" if d else "came in level with")
    if pct is not None and d:
        swing += f" ({pct:+.0f}%)"
    # the count is not always four: V carries five, because the quarter the
    # card's statement covers reported before the vendor's surprise row did
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
             7: "seven", 8: "eight"}
    n = words.get(len(done), str(len(done)))
    tail = "and the one ahead" if ahead else "with none yet ahead"
    out = (f"{HEAD} adjusted EPS against the street's consensus, {n} reported "
           f"quarter{'' if len(done) == 1 else 's'} {tail}. "
           f"{last['label']}: {money(last['actual'])} "
           f"actual against {money(last['estimate'])} expected, {swing}.")
    if ahead:
        nxt = ahead[0]
        out += f" {nxt['label']} consensus is {money(nxt['estimate'])}"
        if nxt.get("analysts"):
            out += f" from {nxt['analysts']} analysts"
        if nxt.get("due"):
            out += f", due {nxt['due']}"
        out += "."
    out += (" This is adjusted EPS, not the GAAP figure the income statement "
            "is built from, and for a foreign filer it is the ADR's earnings "
            f"per share in US dollars. Source: {spec['source']}")
    return out


def main():
    dry = "--dry-run" in sys.argv
    doc = json.loads((HERE / "financials.json").read_text())
    added = noted = 0
    for item in doc["items"]:
        p = HERE / "examples" / f"{item['t'].lower()}-eps.json"
        if not p.exists():
            continue
        spec = json.loads(p.read_text())
        if not (spec.get("reported") or []):
            continue
        stem = f"{item['t']}-eps"
        if item.get("eps") != stem:
            item["eps"] = stem
            added += 1
        note = note_for(spec)
        notes = item.get("notes") or []
        at = next((i for i, n in enumerate(notes) if n.startswith(HEAD)), None)
        if at is None:
            notes.append(note)
            item["notes"] = notes
            noted += 1
        elif notes[at] != note:
            notes[at] = note
            noted += 1
    if not dry:
        (HERE / "financials.json").write_text(
            json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print(f"{'would link' if dry else 'linked'} {added}  notes {noted}")


if __name__ == "__main__":
    main()
