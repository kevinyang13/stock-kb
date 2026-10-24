#!/usr/bin/env python3
"""Turn a row of income statement figures into a sankey spec.

Picks the profit or loss layout automatically and derives the lines the
chart needs, so every statement foots:

    other  = pretax - operating      (bundles interest, FX, investment gains)
    profit layout: net = operating + other - tax
    loss layout:   gross + net_loss = opex + below-the-line charges
"""
import json, sys
from pathlib import Path

PALETTE = ["#e8502a", "#1b1b7a", "#c8a020", "#f0a030", "#6cb6e8", "#7cd07c"]


def _segments(segs, r, rev, yoy, ticker, allowed, dec):
    """Revenue must be broken out by reported segment. A single bar is a
    fallback for companies that publish no split, not a default."""
    if not segs:
        if not allowed:
            print(f"  ! {ticker}: NO SEGMENT SPLIT. Pull the segment table from the company's own "
                  f"release and pass segments=[...]. If the company genuinely publishes none, "
                  f"pass no_segment_split=True and say so on the card.", file=sys.stderr)
        return [{"name": "Total revenue", "value": r(rev),
                 **({"yoy": round(yoy)} if yoy is not None else {}),
                 "note": "company publishes no segment split" if allowed else "not split by segment",
                 "color": PALETTE[0]}]
    out, total = [], 0.0
    for i, sg in enumerate(segs):
        v = r(sg["value"])
        total += v
        out.append({"name": sg["name"], "value": v,
                    **({"yoy": round(sg["yoy"])} if sg.get("yoy") is not None else {}),
                    "note": sg.get("note") or f"{sg['value'] / rev * 100:.0f}% of revenue",
                    "color": sg.get("color", PALETTE[i % len(PALETTE)])})
    drift = total - r(rev)
    if abs(drift) > max(0.15, 0.005 * abs(r(rev))):
        print(f"  ! {ticker}: segments sum to {total:,.{dec}f} vs revenue {r(rev):,.{dec}f} "
              f"(drift {drift:+,.{dec}f}) -- wrong period or wrong lines?", file=sys.stderr)
    return out


def make(t, company, period, end, rev, yoy, cor, rd, sga, opex, op, pretax, tax, net,
         unit=None, dec=None, other_opex_name="Other operating", cur="$", gross=None,
         segments=None, no_segment_split=False):
    # Sources often report a cost of revenue that does not reconcile with their
    # own gross profit -- there are cost lines between the two. Trust the
    # reported subtotals and derive the bridging lines, so the chart always
    # conserves: cost of revenue is everything above gross profit, and "other"
    # is everything between operating and net profit besides tax.
    gross = gross if gross is not None else rev - cor
    cor = rev - gross
    opex = gross - op
    other = net + tax - op
    # money reads better in billions once revenue clears ~$20bn
    if unit is None:
        if abs(rev) >= 20000:
            unit, dec = "B", 1
        elif abs(rev) >= 1000:
            unit, dec = "M", 0
        else:
            # a $13.5M company rounded to $14M loses the margin entirely
            unit, dec = "M", 1
    k = 1000.0 if unit == "B" else 1.0
    r = lambda v: round(v / k, dec)

    items = []
    if rd:  items.append({"name": "R&D", "value": r(rd)})
    if sga: items.append({"name": "SG&A", "value": r(sga)})
    rest = opex - (rd or 0) - (sga or 0)
    if abs(rest) > max(1.0, 0.002 * rev):
        items.append({"name": other_opex_name, "value": r(rest)})
    if not items:
        items = [{"name": "Operating expenses", "value": r(opex)}]

    spec = {
        "company": company, "ticker": t, "period": period,
        "currency": cur, "unit": unit, "decimals": dec,
        "revenue": r(rev), "revenue_yoy": round(yoy) if yoy is not None else None,
        "segments": _segments(segments, r, rev, yoy, t, no_segment_split, dec),
        "cost_of_revenue": r(cor), "gross_profit": r(gross),
        "width": 1700, "height": 940,
    }
    if net >= 0:
        spec.update({"opex_total": r(opex), "opex_items": items,
                     "operating_profit": r(op), "other": r(other),
                     "tax": r(tax), "net_profit": r(net)})
    else:
        # loss layout: revenue plus the loss funds every charge
        loss = -net
        charges = r(gross) + r(loss)
        below = round(charges - sum(i["value"] for i in items), dec)
        spec.update({"opex_items": items, "net_loss": r(loss)})
        if below >= 0:
            spec["below_line"] = [{"name": "Non-operating & tax, net", "value": below}]
        else:
            # charges exceed gross profit plus the loss: non-operating income
            # covered the difference, so it is a second source, not a charge
            spec["other_income"] = -below
    return spec

if __name__ == "__main__":
    rows = json.load(open(sys.argv[1]))
    for row in rows:
        s = make(**row)
        f = Path("examples") / f"{s['ticker'].lower()}-{s['period'].lower().replace(' ', '-')}.json"
        json.dump(s, open(f, "w"), indent=1)
        print(f"{s['ticker']:6}{'loss' if 'net_loss' in s else 'profit':7}{f}")
