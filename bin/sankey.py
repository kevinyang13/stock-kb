#!/usr/bin/env python3
"""Render an App-Economy-Insights-style income statement Sankey.

    python3 bin/sankey.py examples/tsm-q3-fy26.json          # -> out/TSM-Q3-FY26.html
    python3 bin/sankey.py examples/tsm-q3-fy26.json --png    # also writes .png (needs kaleido)

Input is a JSON spec; see wiki/sankey-income-statement.md for the schema.
All money values are in the same unit (billions by default) and POSITIVE,
including costs -- the renderer decides direction and colour.
"""

import json
import sys
from pathlib import Path

import plotly.graph_objects as go

# Palette eyeballed from the reference infographics.
INK = "#17496b"        # title navy
PROFIT = "#1a9641"     # green nodes
PROFIT_LINK = "rgba(166,217,166,0.80)"
COST = "#c81e1e"       # red nodes
COST_LINK = "rgba(240,160,152,0.80)"
NEUTRAL = "#111111"    # revenue + segment nodes
NEUTRAL_LINK = "rgba(140,140,140,0.65)"
BG = "#f2f2f2"

# Column positions. Plotly needs 0 < x < 1 strictly.
X = {"segment": 0.01, "revenue": 0.26, "gross": 0.48, "op": 0.70, "leaf": 0.99}


def money(v, unit="B", cur="$", dec=1):
    return f"{cur}{v:,.{dec}f}{unit}"


def pct(v):
    return f"{v:+.0f}%" if v is not None else ""


def validate(spec, rev, cor, gross, opex, opex_items, op, tax, other, net, tol=None):
    """Warn when the statement does not foot. Rounded inputs rarely balance
    exactly, so this reports drift rather than refusing to draw."""
    tol = tol if tol is not None else max(0.15, 0.005 * abs(rev))
    issues = []
    seg_sum = sum(s["value"] for s in spec["segments"])
    checks = [
        ("segments vs revenue", seg_sum, rev),
        ("gross profit = revenue - cost", gross, rev - cor),
        ("operating profit = gross - opex", op, gross - opex),
        ("net profit = operating - tax + other", net, op - tax + other),
    ]
    if opex_items:
        checks.append(("opex items vs opex total", sum(i["value"] for i in opex_items), opex))
    for name, got, want in checks:
        if abs(got - want) > tol:
            issues.append(f"  ! {name}: {got:,.2f} vs {want:,.2f} (drift {got - want:+.2f})")
    return issues


def build(spec):
    cur, unit = spec.get("currency", "$"), spec.get("unit", "B")
    dec = spec.get("decimals", 1)
    segs = spec["segments"]
    rev = spec["revenue"]
    cor = spec["cost_of_revenue"]
    gross = spec.get("gross_profit", rev - cor)
    opex_items = spec.get("opex_items", [])
    opex = spec.get("opex_total", sum(i["value"] for i in opex_items))
    op = spec.get("operating_profit", gross - opex)
    tax = spec.get("tax", 0.0)
    other = spec.get("other", 0.0)
    net = spec.get("net_profit", op - tax + other)

    for line in validate(spec, rev, cor, gross, opex, opex_items, op, tax, other, net):
        print(line, file=sys.stderr)

    labels, colors, xs, ys = [], [], [], []

    def node(label, color, x, y):
        labels.append(label); colors.append(color); xs.append(x); ys.append(y)
        return len(labels) - 1

    # left column: revenue segments, stacked top to bottom
    seg_ids = []
    n = max(len(segs), 1)
    for i, s in enumerate(segs):
        y = (i + 0.5) / n
        seg_ids.append(node(s["name"], s.get("color", NEUTRAL), X["segment"], y))

    rev_id = node("Revenue", NEUTRAL, X["revenue"], 0.5)
    gross_id = node("Gross profit", PROFIT, X["gross"], 0.30)
    cor_id = node("Cost of revenue", COST, X["gross"], 0.80)
    op_id = node("Operating profit", PROFIT, X["op"], 0.20)
    opex_id = node("Operating expenses", COST, X["op"], 0.60)
    net_id = node("Net profit", PROFIT, X["leaf"], 0.12)

    links = []

    def link(s, t, v, color):
        if v and v > 0:
            links.append((s, t, v, color))

    for sid, s in zip(seg_ids, segs):
        link(sid, rev_id, s["value"], NEUTRAL_LINK)
    link(rev_id, gross_id, gross, PROFIT_LINK)
    link(rev_id, cor_id, cor, COST_LINK)
    link(gross_id, op_id, op, PROFIT_LINK)
    link(gross_id, opex_id, opex, COST_LINK)

    opex_leaf = []
    for i, item in enumerate(opex_items):
        y = 0.52 + (i + 0.5) * (0.46 / max(len(opex_items), 1))
        iid = node(item["name"], COST, X["leaf"], min(y, 0.96))
        link(opex_id, iid, item["value"], COST_LINK)
        opex_leaf.append((iid, item))

    other_node = tax_node = othercost_node = taxben_node = None
    if other > 0:
        other_node = node("Interest & other", PROFIT, X["op"], 0.04)
        link(other_node, net_id, other, PROFIT_LINK)
    if tax > 0:
        tax_node = node("Tax", COST, X["leaf"], 0.26)
        link(op_id, tax_node, tax, COST_LINK)
    if other < 0:
        # net interest expense -- a charge taken out of operating profit
        othercost_node = node("Interest & other, net", COST, X["leaf"], 0.38)
        link(op_id, othercost_node, -other, COST_LINK)
    if tax < 0:
        # a tax benefit adds to profit, so it flows in rather than out
        taxben_node = node("Tax benefit", PROFIT, X["op"], 0.10)
        link(taxben_node, net_id, -tax, PROFIT_LINK)
    link(op_id, net_id, op - max(tax, 0.0) + min(other, 0.0), PROFIT_LINK)

    DOM_TOP = 0.77          # sankey occupies the lower 77%; stage labels live above it
    fig = go.Figure(go.Sankey(
        domain=dict(x=[0, 1], y=[0, DOM_TOP]),
        arrangement="fixed",
        node=dict(label=["" for _ in labels],   # labels drawn as annotations instead
                  color=colors, x=xs, y=ys,
                  pad=26, thickness=22,
                  line=dict(width=0)),
        link=dict(source=[l[0] for l in links], target=[l[1] for l in links],
                  value=[l[2] for l in links], color=[l[3] for l in links]),
    ))

    # Text is drawn by hand so each node can carry value + margin + Y/Y.
    # Annotation y uses paper coords, same bottom-up origin as node y above.
    ann = []

    def label(x, y, head, sub=(), color=INK, size=16, xa="center", va="middle"):
        txt = f"<b>{head}</b>"
        for line in [l for l in sub if l]:
            txt += f"<br><span style='font-size:12px;color:#555'>{line}</span>"
        ann.append(dict(x=x, y=y, text=txt, showarrow=False, align=xa,
                        xanchor=xa, yanchor=va,
                        font=dict(size=size, color=color),
                        xref="paper", yref="paper"))

    def py(node_y):
        """node y (0=top, within domain) -> paper y (0=bottom, whole canvas)"""
        return (1.0 - node_y) * DOM_TOP

    def m(v):
        return money(v, unit, cur, dec)

    def yoy(v, suffix=" Y/Y"):
        return f"{pct(v)}{suffix}" if v is not None else ""

    for sid, s_ in zip(seg_ids, segs):
        label(X["segment"] - 0.015, py(ys[sid]), s_["name"],
              [m(s_["value"]), yoy(s_.get("yoy")), s_.get("note", "")],
              color="#111", xa="right")

    label(X["revenue"], 0.895, "Revenue",
          [m(rev), yoy(spec.get("revenue_yoy"))], color="#111", va="bottom")
    label(X["gross"], 0.895, "Gross profit",
          [m(gross), f"{gross / rev * 100:.0f}% margin"], color=PROFIT, va="bottom")
    label(X["gross"], py(ys[cor_id]) - 0.13, "Cost of revenue",
          [f"({m(cor)})"], color=COST)
    label(X["op"], 0.895, "Operating profit",
          [m(op), f"{op / rev * 100:.0f}% margin"], color=PROFIT, va="bottom")
    label(X["op"], 0.045, "Operating expenses",
          [f"({m(opex)})"], color=COST)
    label(1.015, py(ys[net_id]), "Net profit",
          [m(net), f"{net / rev * 100:.0f}% margin"], color=PROFIT, xa="left")

    for item_id, item in opex_leaf:
        label(1.015, py(ys[item_id]), item["name"],
              [f"({m(item['value'])})",
               f"{item['value'] / rev * 100:.0f}% of revenue"], color=COST, xa="left")
    if tax > 0:
        label(1.015, py(ys[tax_node]), "Tax", [f"({m(tax)})"], color=COST, xa="left")
    if other < 0:
        label(1.015, py(ys[othercost_node]), "Interest & other, net",
              [f"({m(-other)})", f"{-other / rev * 100:.0f}% of revenue"], color=COST, xa="left")
    if tax < 0:
        label(X["op"], py(ys[taxben_node]) + 0.055, "Tax benefit", [m(-tax)], color=PROFIT, va="bottom")
    if other > 0:
        label(X["op"], 1.015, "Interest & other",
              [m(other)], color=PROFIT, va="bottom")

    fig.update_layout(
        title=dict(y=0.995, yanchor='top', text=f"<b>{spec['company']} {spec['period']} Income Statement</b>",
                   x=0.5, xanchor="center", font=dict(size=40, color=INK)),
        annotations=ann,
        paper_bgcolor=BG, plot_bgcolor=BG,
        width=spec.get("width", 1500), height=spec.get("height", 880),
        margin=dict(l=300, r=270, t=185, b=70),
        font=dict(family="Helvetica Neue, Arial, sans-serif"),
    )
    return fig, dict(revenue=rev, gross=gross, op=op, net=net)


def build_loss(spec):
    """Layout for a loss-making quarter.

    A profitable statement conserves as revenue -> profit + costs. A loss does
    not: costs exceed revenue, so the shortfall has to come in from somewhere.
    Here the net loss is drawn as a red source feeding the expense pool, which
    is what a loss literally is -- spending funded by capital rather than sales.

        gross profit + net loss == operating expenses + below-the-line charges
    """
    cur, unit = spec.get("currency", "$"), spec.get("unit", "B")
    dec = spec.get("decimals", 1)
    segs = spec["segments"]
    rev = spec["revenue"]
    cor = spec["cost_of_revenue"]
    gross = spec.get("gross_profit", rev - cor)
    opex_items = spec.get("opex_items", [])
    below = spec.get("below_line", [])
    net_loss = spec["net_loss"]
    # some loss makers have non-operating income offsetting part of the burn,
    # which makes charges exceed gross profit + net loss. It is a second source.
    other_income = spec.get("other_income", 0.0)

    leaves = opex_items + below
    funded = gross + net_loss + other_income
    spent = sum(i["value"] for i in leaves)
    if abs(funded - spent) > 0.15:
        print(f"  ! loss layout does not balance: gross {gross:,.2f} + net loss {net_loss:,.2f}"
              f" = {funded:,.2f} vs charges {spent:,.2f}", file=sys.stderr)

    labels, colors, xs, ys = [], [], [], []

    def node(label, color, x, y):
        labels.append(label); colors.append(color); xs.append(x); ys.append(y)
        return len(labels) - 1

    seg_ids = []
    n = max(len(segs), 1)
    for i, sg in enumerate(segs):
        seg_ids.append(node(sg["name"], sg.get("color", NEUTRAL), X["segment"], (i + 0.5) / n))

    rev_id = node("Revenue", NEUTRAL, X["revenue"], 0.42)
    gross_id = node("Gross profit", PROFIT, X["gross"], 0.08)
    cor_id = node("Cost of revenue", COST, 0.40, 0.84)
    # the loss gets its own column: when it dwarfs revenue it would
    # otherwise swamp the gross/cost column and bury their labels
    loss_id = node("Net loss", COST, X["gross"], 0.66)
    pool_id = node("Costs & charges", COST, X["op"], 0.42)

    links = []

    def link(a, b, v, c):
        if v and v > 0:
            links.append((a, b, v, c))

    for sid, sg in zip(seg_ids, segs):
        link(sid, rev_id, sg["value"], NEUTRAL_LINK)
    link(rev_id, gross_id, gross, PROFIT_LINK)
    link(rev_id, cor_id, cor, COST_LINK)
    # declaration order must match top-to-bottom node order or the bands cross
    inc_id = node("Non-operating income", PROFIT, X["gross"], 0.32) if other_income > 0 else None
    link(gross_id, pool_id, gross, PROFIT_LINK)
    if inc_id is not None:
        link(inc_id, pool_id, other_income, PROFIT_LINK)
    link(loss_id, pool_id, net_loss, COST_LINK)

    leaf_ids = []
    for i, item in enumerate(leaves):
        y = (i + 0.5) / max(len(leaves), 1)
        lid = node(item["name"], COST, X["leaf"], y)
        link(pool_id, lid, item["value"], COST_LINK)
        leaf_ids.append((lid, item))

    DOM_TOP = 0.77
    fig = go.Figure(go.Sankey(
        domain=dict(x=[0, 1], y=[0, DOM_TOP]),
        arrangement="fixed",
        node=dict(label=["" for _ in labels], color=colors, x=xs, y=ys,
                  pad=26, thickness=22, line=dict(width=0)),
        link=dict(source=[l[0] for l in links], target=[l[1] for l in links],
                  value=[l[2] for l in links], color=[l[3] for l in links]),
    ))

    ann = []

    def label(x, y, head, sub=(), color=INK, size=16, xa="center", va="middle"):
        txt = f"<b>{head}</b>"
        for line in [l for l in sub if l]:
            txt += f"<br><span style='font-size:12px;color:#555'>{line}</span>"
        ann.append(dict(x=x, y=y, text=txt, showarrow=False, align=xa,
                        xanchor=xa, yanchor=va, font=dict(size=size, color=color),
                        xref="paper", yref="paper"))

    def py(node_y):
        return (1.0 - node_y) * DOM_TOP

    def m(v):
        return money(v, unit, cur, dec)

    for sid, sg in zip(seg_ids, segs):
        sub = [m(sg["value"])]
        if sg.get("yoy") is not None:
            sub.append(f"{pct(sg['yoy'])} Y/Y")
        if sg.get("note"):
            sub.append(sg["note"])
        label(X["segment"] - 0.015, py(ys[sid]), sg["name"], sub, color="#111", xa="right")

    label(X["revenue"], 0.895, "Revenue",
          [m(rev), f"{pct(spec.get('revenue_yoy'))} Y/Y" if spec.get("revenue_yoy") is not None else ""],
          color="#111", va="bottom")
    label(X["gross"], 0.895, "Gross profit",
          [m(gross), f"{gross / rev * 100:.0f}% margin"], color=PROFIT, va="bottom")
    label(0.40, py(ys[cor_id]) - 0.115, "Cost of revenue", [f"({m(cor)})"], color=COST)
    label(X["gross"] - 0.015, py(ys[loss_id]), "Net loss",
          [f"({m(net_loss)})", f"{net_loss / rev * 100:.0f}% of revenue", "funds the gap"],
          color=COST, xa="right")
    if inc_id is not None:
        label(X["gross"] - 0.015, py(ys[inc_id]), "Non-operating income", [m(other_income)],
              color=PROFIT, xa="right")
    label(X["op"], 0.895, "Costs & charges", [f"({m(spent)})"], color=COST, va="bottom")

    for lid, item in leaf_ids:
        label(1.015, py(ys[lid]), item["name"],
              [f"({m(item['value'])})", f"{item['value'] / rev * 100:.0f}% of revenue"],
              color=COST, xa="left")

    fig.update_layout(
        title=dict(y=0.995, yanchor="top",
                   text=f"<b>{spec['company']} {spec['period']} Income Statement</b>",
                   x=0.5, xanchor="center", font=dict(size=40, color=INK)),
        annotations=ann, paper_bgcolor=BG, plot_bgcolor=BG,
        width=spec.get("width", 1700), height=spec.get("height", 940),
        margin=dict(l=300, r=270, t=185, b=120),
        font=dict(family="Helvetica Neue, Arial, sans-serif"),
    )
    return fig, dict(revenue=rev, gross=gross, net_loss=net_loss, charges=spent)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    spec = json.loads(Path(sys.argv[1]).read_text())
    fig, totals = (build_loss(spec) if spec.get("net_loss") is not None else build(spec))
    out = Path("out"); out.mkdir(exist_ok=True)
    stem = f"{spec.get('ticker', spec['company'])}-{spec['period']}".replace(" ", "-")
    html = out / f"{stem}.html"
    fig.write_html(html, include_plotlyjs="cdn")
    print(f"wrote {html}")
    if "--png" in sys.argv:
        try:
            fig.write_image(out / f"{stem}.png", scale=2)
            print(f"wrote {out / (stem + '.png')}")
        except Exception as e:
            print(f"PNG export unavailable ({e.__class__.__name__}): pip install kaleido")
    print("totals:", {k: round(v, 2) for k, v in totals.items()})


if __name__ == "__main__":
    main()
