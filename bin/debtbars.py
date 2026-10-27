#!/usr/bin/env python3
"""Turn a debt/coverage spec into the grouped bar figure the Financials page draws.

Three bars for the quarter the card is about: debt carried, free cash flow
generated, cash held. Debt and cash are balance sheet stocks read at the
quarter end; free cash flow is the flow over that quarter.

    python3 bin/debtbars.py examples/nbis-debt.json --json --png

Spec figures are in millions, as the filings report them. The axis is in
billions; individual bar labels switch to millions below $1bn, because a
$49.5M bar labelled "$0.0B" says nothing.
"""
import json
import sys
from pathlib import Path

import plotly.graph_objects as go

SERIES = [
    ("debt", "Debt", "#e8537f"),
    ("fcf", "Free cash flow", "#2ab7ca"),
    ("cash", "Cash \u0026 equivalents", "#4a79dc"),
]
INK = "#12312c"
# Narrow on purpose: this sits beside the sankey in one row, so the design
# width is roughly the column it lands in and the font sizes below are the
# sizes it actually renders at.
DESIGN = (330, 520)


# Spec figures are in millions of the filed currency.
TIERS = [(1e6, "T"), (1e3, "B"), (0, "M")]


def unit_for(vals):
    """One unit for the axis, taken from the largest bar."""
    top = max(abs(v) for v in vals) if vals else 0
    for cut, u in TIERS:
        if top >= cut:
            return u, (cut or 1.0)
    return "M", 1.0


def money(m, cur="$"):
    """A bar label, in whatever unit keeps it meaningful. A $49.5M bar in a
    chart scaled to billions must not read "$0.0B"."""
    sign = "-" if m < 0 else ""
    a = abs(m)
    for cut, u in TIERS:
        if a >= cut:
            v = a / cut if cut else a
            return f"{sign}{cur}{v:,.1f}{u}" if (cut or a < 100) \
                else f"{sign}{cur}{v:,.0f}{u}"
    return f"{sign}{cur}{a:,.1f}M"


NBSP = "&#160;"       # plotly collapses runs of ordinary spaces in hover text
RULE = "-"            # the subtotal rule, one monospace cell per character


def block_unit(vals):
    """One unit for a whole tooltip block, so its lines stay comparable.
    Millions until the numbers get unwieldy, which keeps the common case
    reading the way a filing does."""
    top = max((abs(v) for v in vals), default=0)
    if top < 1e5:
        return "M", 1.0
    if top < 1e8:
        return "B", 1e3
    return "T", 1e6


def fmt_in(v, cur, unit, div):
    a = abs(v) / div
    dec = 0 if a >= 100 else 1
    return f"{'-' if v < 0 else ''}{cur}{a:,.{dec}f}{unit}"


def hover(title, rows, total, cur, notes=()):
    """A monospace, column-aligned breakdown for one bar's tooltip."""
    unit, div = block_unit([v for _, v in rows] + [total[1]] +
                           [v for _, v in notes])
    body = [(l, fmt_in(v, cur, unit, div)) for l, v in rows]
    foot = (total[0], fmt_in(total[1], cur, unit, div))
    tail = [(l, fmt_in(v, cur, unit, div)) for l, v in notes]

    lw = max(len(l) for l, _ in body + [foot] + tail)
    vw = max(len(v) for _, v in body + [foot] + tail)
    line = lambda l, v: l + NBSP * (lw - len(l) + 3 + vw - len(v)) + v

    out = [f"<b>{title}</b>", ""]
    out += [line(l, v) for l, v in body]
    if body:
        out.append(RULE * (lw + 3 + vw))
    out.append(f"<b>{line(*foot)}</b>")
    if tail:
        out += ["", "<i>not in this bar</i>"] + [line(l, v) for l, v in tail]
    return "<br>".join(out)


def tooltip(p, key, name, cur):
    """What this bar is made of. Debt and cash are balance sheet figures at
    the period end; free cash flow is the period's own flow."""
    rows = [(d["label"], d["value"]) for d in p.get(f"{key}_parts") or []]
    notes = ()
    if key == "cash":
        rows, notes = [], tuple((d["label"], d["value"])
                                for d in p.get("cash_parts") or [])
    return hover(f"{name} \u00b7 {p['label']}", rows, (name, p[key]),
                 cur, notes)


def build(spec):
    periods = spec["periods"]
    labels = [p["label"] for p in periods]
    cur = spec.get("currency", "$")
    unit, div = unit_for([p[k] for p in periods for k, _, _ in SERIES])
    fig = go.Figure()

    for key, name, color in SERIES:
        vals = [p[key] for p in periods]
        tips = [tooltip(p, key, name, cur) for p in periods]
        fig.add_bar(
            name=name,
            x=labels,
            y=[v / div for v in vals],
            marker=dict(color=color, line=dict(width=0)),
            text=[money(v, cur) for v in vals],
            # negative bars read better with the figure on the outside, which
            # is what "auto" gets wrong when a bar is tall and the label short
            textposition="outside",
            textfont=dict(size=11, color=INK),
            cliponaxis=False,
            customdata=tips,
            hovertemplate="%{customdata}<extra></extra>",
        )

    lo = min(0.0, min(p["fcf"] for p in periods) / div)
    hi = max(max(p[k] for k, _, _ in SERIES) for p in periods) / div
    pad = (hi - lo) * 0.16

    fig.update_layout(
        # No HTML entities in the title: kaleido fails the whole render with a
        # bare "plotly.js error" on one here, though they are fine in trace
        # names and hovertemplates.
        title=dict(
            # the card header already names the company
            text="<b>Debt level and coverage</b>",
            x=0.5, xanchor="center", y=0.95,
            font=dict(size=16, color="#0f3b47"),
        ),
        barmode="group",
        bargap=0.24,
        bargroupgap=0.08,
        xaxis=dict(
            tickfont=dict(size=13, color=INK),
            showgrid=False, showline=False, ticks="",
        ),
        yaxis=dict(
            range=[lo - pad, hi + pad],
            tickfont=dict(size=11, color="#667"),
            gridcolor="#dcdcdc", zerolinecolor="#9aa", zerolinewidth=2,
            ticksuffix=unit,
            showline=False, ticks="",
        ),
        legend=dict(
            orientation="h", x=0.5, xanchor="center", y=-0.14, yanchor="top",
            font=dict(size=11, color=INK),
            bgcolor="rgba(0,0,0,0)", borderwidth=0,
            traceorder="normal", itemwidth=30,
        ),
        hoverlabel=dict(align="left", bgcolor="#fbfbfb",
                        bordercolor="#c9c9c9",
                        font=dict(family="SFMono-Regular, Menlo, Consolas, "
                                         "monospace", size=12, color=INK)),
        plot_bgcolor="#f2f2f2",
        paper_bgcolor="#f2f2f2",
        margin=dict(l=46, r=16, t=62, b=104),
        width=DESIGN[0], height=DESIGN[1],
    )
    return fig


def validate(spec):
    """The chart must not imply a coverage the figures do not support."""
    warn = 0
    for p in spec["periods"]:
        for k, name, _ in SERIES:
            if k not in p:
                print(f"  ! {spec['ticker']} {p['label']}: missing {k}", file=sys.stderr)
                warn += 1
        if p.get("debt", 0) < 0 or p.get("cash", 0) < 0:
            print(f"  ! {spec['ticker']} {p['label']}: debt and cash cannot be "
                  f"negative", file=sys.stderr)
            warn += 1
    return warn


def main():
    spec = json.load(open(sys.argv[1]))
    stem = f"{spec['ticker']}-debt"
    warn = validate(spec)
    fig = build(spec)

    Path("out").mkdir(exist_ok=True)
    fig.write_html(f"out/{stem}.html", include_plotlyjs="cdn")
    print(f"wrote out/{stem}.html")

    if "--json" in sys.argv:
        charts = Path("charts")
        charts.mkdir(exist_ok=True)
        j = fig.to_plotly_json()
        lay = j["layout"]
        # the browser rescales margins and fonts off these, so hand them over
        # as data rather than leaving them baked into a fixed-size layout
        j["design"] = {"width": lay.pop("width"), "height": lay.pop("height")}
        p = charts / f"{stem}.json"
        p.write_text(json.dumps(j, separators=(",", ":"), default=str))
        print(f"wrote {p}")

    if "--png" in sys.argv:
        fig.write_image(f"out/{stem}.png", scale=2)
        print(f"wrote out/{stem}.png")

    for q in spec["periods"]:
        net = q["debt"] - q["cash"]
        c = spec.get("currency", "$")
        print(f'{q["label"]}: debt {c}{q["debt"]:,.1f}M | cash {c}{q["cash"]:,.1f}M | '
              f'FCF {c}{q["fcf"]:,.1f}M | net debt {c}{net:,.1f}M')
    print(f"{warn} warning(s)")


if __name__ == "__main__":
    main()
