#!/usr/bin/env python3
"""Turn an ownership spec into the share-register donut the Financials page draws.

Four slices that sum to the whole share count: index and ETF managers, other
institutions, insiders, and the residual everyone else. Hovering a slice names
the five largest holders inside it, with each one's percentage of shares
outstanding, read from that manager's own Form 13F.

    python3 bin/ownpie.py examples/nvda-own.json --json --png

A donut rather than a pie on purpose: the hole carries the institutional total,
which is the one figure a reader wants without hovering anything, and the four
slices are easier to compare as arc lengths than as wedges meeting at a point.
"""
import json
import re
import sys
from pathlib import Path

import plotly.graph_objects as go

INK = "#12312c"

# Index and active institutions are the two halves of one number, so they are
# two weights of one hue; insiders and retail are their own colours. The order
# is the order the slices are drawn, clockwise from the top.
COLOR = {
    "index": "#2f6fb5",
    "active": "#7fb2e0",
    "insiders": "#e0b25c",
    "retail": "#9ec9ad",
}

# Sits beside the sankey, so the design width is roughly the column it lands
# in and the font sizes below are the sizes it actually renders at.
DESIGN = (380, 520)


# Every hover line has to fit the column the chart sits in, about 360px wide.
# Plotly does not wrap hover text -- it draws exactly the lines it is given and
# the figure clips whatever runs past its edge -- so the lines are kept short
# here rather than left to the browser.
def detail(spec, key):
    """The hover body for one slice: who is in it, or why no one is named."""
    top = (spec.get("top") or {}).get(key) or []
    if top:
        lines = [f"{h['pct']:5.2f}%  {short(h['name'])}" for h in top]
        return ("Largest holders, % of all<br>shares outstanding (13F):<br>"
                + "<br>".join(lines))
    if key == "insiders":
        return ("Officers, directors and 10%<br>"
                "owners, from Forms 3, 4 and 5.<br>"
                "Not named on this card.")
    if key == "retail":
        return ("Everyone filing no 13F:<br>"
                "individuals, and managers under<br>"
                "the $100M threshold.<br>"
                "A residual, not a filed figure.")
    return "No 13F filer in this group."


# SEC appends a filer's state of organisation to the name on some forms.
STATE_SUFFIX = re.compile(r"\s*/[A-Z]{2}/\s*$")


def short(name, width=24):
    """Filer names are typed freehand and some run very long."""
    n = STATE_SUFFIX.sub("", " ".join(name.split()))
    return n if len(n) <= width else n[:width - 1] + "…"


def build(spec):
    slices = spec["slices"]
    labels = [s["label"] for s in slices]
    values = [s["pct"] for s in slices]
    colors = [COLOR[s["key"]] for s in slices]
    custom = [detail(spec, s["key"]) for s in slices]

    inst = sum(s["pct"] for s in slices if s["key"] in ("index", "active"))

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        customdata=custom,
        sort=False,                    # the spec's order is the reading order
        direction="clockwise",
        rotation=0,
        hole=0.52,
        marker=dict(colors=colors, line=dict(color="#f2f2f2", width=2)),
        textinfo="percent",
        textposition="inside",
        insidetextorientation="horizontal",
        textfont=dict(size=13, color="#ffffff"),
        hovertemplate=("<b>%{label}</b>  %{value:.1f}% of shares"
                       "<br>%{customdata}<extra></extra>"),
    ))

    fig.update_layout(
        # No HTML entities in the title: kaleido fails the whole render on one
        # here, though they are fine in trace names and hovertemplates.
        title=dict(
            text="<b>Who owns the shares</b>",
            x=0.5, xanchor="center", y=0.95,
            font=dict(size=16, color="#0f3b47"),
        ),
        annotations=[dict(
            text=(f"<b>{inst:.0f}%</b><br>"
                  f"<span style='font-size:10px'>institutional</span>"),
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=22, color="#0f3b47"),
            align="center",
        )],
        showlegend=True,
        legend=dict(
            orientation="h", x=0.5, xanchor="center", y=-0.06, yanchor="top",
            font=dict(size=11, color=INK),
            bgcolor="rgba(0,0,0,0)", borderwidth=0,
            traceorder="normal", itemwidth=30,
        ),
        hoverlabel=dict(align="left", bgcolor="#fbfbfb",
                        bordercolor="#c9c9c9",
                        font=dict(family="SFMono-Regular, Menlo, Consolas, "
                                         "monospace", size=11, color=INK)),
        plot_bgcolor="#f2f2f2",
        paper_bgcolor="#f2f2f2",
        margin=dict(l=16, r=16, t=62, b=118),
        width=DESIGN[0], height=DESIGN[1],
    )
    return fig


def validate(spec):
    """The donut must describe a whole share register and nothing else."""
    warn = 0
    t = spec["ticker"]
    pcts = [s["pct"] for s in spec["slices"]]

    total = sum(pcts)
    if abs(total - 100.0) > 0.05:
        print(f"  ! {t}: slices sum to {total:.3f}%, not 100%", file=sys.stderr)
        warn += 1

    for s in spec["slices"]:
        if s["pct"] < 0:
            print(f"  ! {t}: {s['key']} is negative ({s['pct']:.2f}%)",
                  file=sys.stderr)
            warn += 1

    # A named holder cannot own more of the company than its whole group does.
    for key in ("index", "active"):
        group = next((s["pct"] for s in spec["slices"] if s["key"] == key), 0)
        named = (spec.get("top") or {}).get(key) or []
        if named and named[0]["pct"] > group + 0.05:
            print(f"  ! {t}: {named[0]['name']} holds {named[0]['pct']:.2f}% "
                  f"but {key} is only {group:.2f}%", file=sys.stderr)
            warn += 1
        if any(h["pct"] > 50 for h in named):
            print(f"  ! {t}: a single 13F filer holds over half the company; "
                  f"check the filing", file=sys.stderr)
            warn += 1

    if not spec.get("sharesOut"):
        print(f"  ! {t}: no shares outstanding", file=sys.stderr)
        warn += 1
    return warn


def main():
    spec = json.load(open(sys.argv[1]))
    stem = f"{spec['ticker']}-own"
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

    for s in spec["slices"]:
        print(f"  {s['label']:24s} {s['pct']:6.2f}%")
    print(f"{spec['filers']:,} filers kept, {spec['dropped']} dropped, "
          f"13F as of {spec['asOf13F']}")
    print(f"{warn} warning(s)")


if __name__ == "__main__":
    main()
