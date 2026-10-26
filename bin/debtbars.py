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
    ("cash", "Cash &amp; equivalents", "#4a79dc"),
]
INK = "#12312c"
# Narrow on purpose: this sits beside the sankey in one row, so the design
# width is roughly the column it lands in and the font sizes below are the
# sizes it actually renders at.
DESIGN = (330, 520)


def money(m):
    """A bar label, in whatever unit keeps it meaningful."""
    sign = "-" if m < 0 else ""
    a = abs(m)
    if a >= 1000:
        return f"{sign}${a / 1000:,.1f}B"
    if a >= 100:
        return f"{sign}${a:,.0f}M"
    return f"{sign}${a:,.1f}M"


def build(spec):
    periods = spec["periods"]
    labels = [p["label"] for p in periods]
    fig = go.Figure()

    for key, name, color in SERIES:
        vals = [p[key] for p in periods]
        fig.add_bar(
            name=name,
            x=labels,
            y=[v / 1000 for v in vals],          # the axis is in billions
            marker=dict(color=color, line=dict(width=0)),
            text=[money(v) for v in vals],
            # negative bars read better with the figure on the outside, which
            # is what "auto" gets wrong when a bar is tall and the label short
            textposition="outside",
            textfont=dict(size=11, color=INK),
            cliponaxis=False,
            customdata=vals,
            hovertemplate="<b>%{x} &middot; " + name + "</b><br>"
                          "$%{customdata:,.1f}M<extra></extra>",
        )

    lo = min(0.0, min(p["fcf"] for p in periods) / 1000)
    hi = max(max(p[k] for k, _, _ in SERIES) for p in periods) / 1000
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
            ticksuffix="B",
            showline=False, ticks="",
        ),
        legend=dict(
            orientation="h", x=0.5, xanchor="center", y=-0.14, yanchor="top",
            font=dict(size=11, color=INK),
            bgcolor="rgba(0,0,0,0)", borderwidth=0,
            traceorder="normal", itemwidth=30,
        ),
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
        print(f'{q["label"]}: debt ${q["debt"]:,.1f}M | cash ${q["cash"]:,.1f}M | '
              f'FCF ${q["fcf"]:,.1f}M | net debt ${net:,.1f}M')
    print(f"{warn} warning(s)")


if __name__ == "__main__":
    main()
