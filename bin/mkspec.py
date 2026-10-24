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

def make(t, company, period, end, rev, yoy, cor, rd, sga, opex, op, pretax, tax, net,
         unit=None, dec=None, other_opex_name="Other operating", cur="$", gross=None):
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
        unit, dec = ("B", 1) if abs(rev) >= 20000 else ("M", 0)
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
        "segments": [{"name": "Total revenue", "value": r(rev),
                      **({"yoy": round(yoy)} if yoy is not None else {}),
                      "note": "not split by segment", "color": "#e8502a"}],
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
