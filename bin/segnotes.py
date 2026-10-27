#!/usr/bin/env python3
"""Keep each Financials card's segment note in step with its chart.

Every card used to carry "Single revenue bar -- no segment split was pulled
for this name", which says nothing about whether the company publishes one.
This replaces that line with either the split the chart now draws, or the
reason there is none, taken from bin/segapply.NONE.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from segapply import NONE, specs

HERE = Path(__file__).resolve().parent.parent
OLD = ("Single revenue bar", "No segment split")


def money(v, cur, unit, dec):
    return f"{cur}{v:,.{dec}f}{unit}"


def note_for(spec):
    segs = spec.get("segments") or []
    cur, unit = spec.get("currency", "$"), spec.get("unit", "M")
    dec = spec.get("decimals", 1)
    if len(segs) < 2:
        why = NONE.get(spec["ticker"])
        return f"No segment split: {why}" if why else None
    bits = []
    for s in segs:
        bit = f"{s['name']} {money(s['value'], cur, unit, dec)}"
        if s.get("yoy") is not None:
            bit += f" ({s['yoy']:+.0f}%)"
        elif s.get("note", "").startswith("from "):
            bit += f" ({s['note']})"
        bits.append(bit)
    out = "Segments: " + ", ".join(bits) + "."
    if spec.get("segment_source"):
        out += f" Source: {spec['segment_source']}."
    return out


def main():
    dry = "--dry-run" in sys.argv
    have = specs()
    doc = json.loads((HERE / "financials.json").read_text())
    changed = 0
    for item in doc["items"]:
        got = have.get(item["t"])
        if not got:
            continue
        note = note_for(got[1])
        if not note:
            continue
        notes = item.get("notes") or []
        # Only the placeholder line is replaced. A card that already carries a
        # hand-written "Segments:" note says more than this can generate --
        # NBIS's explains how intersegment eliminations are netted -- so those
        # are left alone.
        at = next((i for i, n in enumerate(notes) if n.startswith(OLD)), None)
        if at is None:
            continue
        if notes[at] == note:
            continue
        notes[at] = note
        item["notes"] = notes
        changed += 1
        print(f"{item['t']:6} {note[:140]}")
    if not dry:
        (HERE / "financials.json").write_text(
            json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print(f"\n{'would update' if dry else 'updated'} {changed} card(s)")


if __name__ == "__main__":
    main()
