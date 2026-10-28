#!/usr/bin/env python3
"""Point each Financials card at its earnings chart, and say what it is.

Adds `eps` to the item in financials.json wherever examples/<t>-eps.json
exists, and a note saying what the chart is: the vendor's EPS against the
vendor's consensus, usually adjusted and so a different basis from the GAAP
income statement beside it. Two EPS figures on one card invite exactly the
wrong comparison, so the card says which is which -- and where the vendor
cannot be shown to have used one basis for both sides of a pair, the card
says that too and withholds the surprise figure.
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
    # A pair the fetcher could not show to share a basis gets no verdict: the
    # two figures are stated and the comparison is left alone, because
    # "beat by $6.23" off a GAAP actual and an adjusted consensus is wrong.
    if last.get("basisUnverified"):
        swing = ("a gap the two figures cannot be compared across -- see below")
    else:
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
    out = (f"{HEAD} reported EPS against the street's consensus, {n} reported "
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
    out += (" This is the vendor's EPS, usually the street's adjusted figure "
            "rather than the GAAP one the income statement is built from, and "
            "for a foreign filer it is the ADR's earnings per share in US "
            "dollars.")
    flagged = [p["label"] for p in done if p.get("basisUnverified")]
    if flagged:
        one = len(flagged) == 1
        out += (f" The feed states no basis for either side of a pair, and it "
                f"has handed back a GAAP actual against an adjusted consensus "
                f"before, which turns the difference between them into an "
                f"artefact rather than a result. "
                f"{', '.join(flagged)} "
                f"{'cannot' if one else 'cannot'} be shown to share a basis "
                f"here, so {'that pair is' if one else 'those pairs are'} "
                f"drawn with a dotted join and no surprise figure is "
                f"published for {'it' if one else 'them'}.")
    out += f" Source: {spec['source']}"
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
