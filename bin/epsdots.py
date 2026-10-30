#!/usr/bin/env python3
"""Turn an earnings spec into the actual-vs-estimate figure the cards draw.

    python3 bin/epsdots.py examples/nbis-eps.json --json --png

One column per quarter: a filled dot for what the company actually earned, a
hollow one for what the street expected, and a hairline joining the pair so
the gap between them is the thing the eye lands on. The last column is the
quarter that has not been reported yet, so it carries an estimate and no
actual.

This is adjusted EPS from the street's own scorecard, not the GAAP EPS behind
the income statement on the same card. bin/epsfetch.py writes that warning
into the spec and it is repeated in the hover, because two EPS figures on one
card invite exactly the wrong comparison.
"""
import json
import sys
from pathlib import Path

import plotly.graph_objects as go

ACTUAL = "#2ab7ca"
ESTIMATE = "#8d939c"
INK = "#12312c"
# Sits beside the sankey and the debt bars, so the design width is roughly
# the column it lands in and these font sizes are the rendered sizes.
DESIGN = (430, 320)

NBSP = "&#160;"       # plotly collapses runs of ordinary spaces in hover text


def money(v, cur="$"):
    if v is None:
        return "--"
    return f"{'-' if v < 0 else ''}{cur}{abs(v):,.2f}"


def signed(v, cur="$"):
    if v is None:
        return "--"
    return f"{'+' if v >= 0 else '-'}{cur}{abs(v):,.2f}"


def block(title, rows, notes=()):
    rows = [(l, v) for l, v in rows if v is not None]
    lw = max((len(l) for l, _ in rows), default=0)
    vw = max((len(v) for _, v in rows), default=0)
    line = lambda l, v: l + NBSP * (lw - len(l) + 3 + vw - len(v)) + v
    out = [f"<b>{title}</b>", ""] + [line(l, v) for l, v in rows]
    for n in notes:
        out += ["", n]
    return "<br>".join(out)


def beat(p):
    """How the quarter landed, in the words a reader would use -- or nothing,
    when the two figures cannot be shown to share a basis. Subtracting an
    adjusted consensus from a GAAP actual produces a number that looks like a
    result and is not one, so the chart declines to print it."""
    if p.get("basisUnverified"):
        return None
    d = p["actual"] - p["estimate"]
    pct = p.get("surprisePct")
    tail = f" ({pct:+.0f}%)" if pct is not None else ""
    return signed(d) + tail


BASIS_WARN = ("<i>actual and estimate may be on different bases;</i><br>"
              "<i>no surprise figure is shown</i>")


def reported_tip(p, cur, which):
    rows = [("actual", money(p["actual"], cur)),
            ("estimate", money(p["estimate"], cur)),
            ("surprise", beat(p))]
    head = p["label"] + (f" · reported {p['reported']}" if p.get("reported")
                         else " · reported")
    if which == "estimate":
        head = f"{p['label']} · street estimate"
    notes = (BASIS_WARN,) if p.get("basisUnverified") else ()
    return block(head, rows, notes)


def ahead_tip(p, cur):
    rows = [("consensus", money(p["estimate"], cur))]
    if p.get("low") is not None and p.get("high") is not None:
        rows.append(("range", f"{money(p['low'], cur)} to {money(p['high'], cur)}"))
    if p.get("analysts"):
        revs = []
        if p.get("up"):
            revs.append(f"{p['up']} up")
        if p.get("down"):
            revs.append(f"{p['down']} down")
        tail = f"  ({', '.join(revs)} in 4 weeks)" if revs else ""
        rows.append(("estimates", f"{p['analysts']}{tail}"))
    if p.get("due"):
        rows.append(("due", p["due"]))
    return block(f"{p['label']} · not reported yet", rows,
                 ("<i>no actual yet</i>",))


def build(spec):
    cur = spec.get("currency", "$")
    done, ahead = spec["reported"], spec.get("ahead") or []
    labels = [p["label"] for p in done] + [p["label"] for p in ahead]

    fig = go.Figure()

    # The hairline first, so both dots sit on top of it. It is what the eye
    # reads as "the gap", so a pair whose basis is unverified gets a dotted
    # one instead -- the two figures are still drawn, but the chart stops
    # asserting that the distance between them means anything.
    for unverified, dash in ((False, "solid"), (True, "dot")):
        gx, gy = [], []
        for p in done:
            if bool(p.get("basisUnverified")) is not unverified:
                continue
            gx += [p["label"], p["label"], None]
            gy += [p["actual"], p["estimate"], None]
        if not gx:
            continue
        fig.add_scatter(
            x=gx, y=gy, mode="lines", showlegend=False, hoverinfo="skip",
            line=dict(color="#c2c7cd", width=1, dash=dash),
        )

    fig.add_scatter(
        name="Estimate",
        x=labels,
        y=[p["estimate"] for p in done] + [p["estimate"] for p in ahead],
        mode="markers",
        marker=dict(size=13, color="rgba(0,0,0,0)",
                    line=dict(color=ESTIMATE, width=2)),
        customdata=[reported_tip(p, cur, "estimate") for p in done]
                   + [ahead_tip(p, cur) for p in ahead],
        hovertemplate="%{customdata}<extra></extra>",
    )
    fig.add_scatter(
        name="Actual",
        x=[p["label"] for p in done],
        y=[p["actual"] for p in done],
        mode="markers",
        marker=dict(size=13, color=ACTUAL, line=dict(color=ACTUAL, width=0)),
        customdata=[reported_tip(p, cur, "actual") for p in done],
        hovertemplate="%{customdata}<extra></extra>",
    )

    vals = [v for p in done for v in (p["actual"], p["estimate"])] + \
           [p["estimate"] for p in ahead] + \
           [v for p in ahead for v in (p.get("low"), p.get("high")) if v is not None]
    lo, hi = min(vals), max(vals)
    pad = max((hi - lo) * 0.28, 0.08)

    fig.update_layout(
        # Plain ASCII in the title: kaleido fails the whole render on an HTML
        # entity here, though they are fine in trace names and hovertemplates.
        title=dict(
            text="<b>Earnings: actual vs estimate</b>",
            x=0.5, xanchor="center", y=0.95,
            font=dict(size=16, color="#0f3b47"),
        ),
        xaxis=dict(
            type="category",
            # Pin the quarter order. A category axis otherwise takes its order
            # from the order the categories first appear across the traces,
            # and the hairlines joining each pair are emitted grouped rather
            # than chronologically -- so adding a quarter could silently
            # reorder the axis. It did: six charts were drawing their quarters
            # out of sequence, GOOG as Dec '25, Sep '26, Mar '26, Jun '26.
            categoryorder="array",
            categoryarray=labels,
            tickfont=dict(size=12, color=INK),
            showgrid=False, showline=False, ticks="",
        ),
        yaxis=dict(
            range=[lo - pad, hi + pad],
            tickfont=dict(size=11, color="#667"),
            # "$-0.50" puts the sign in the wrong place; d3's currency format
            # gives "-$0.50", which is how the figure is read aloud
            tickformat="$.2f" if cur == "$" else None,
            tickprefix=None if cur == "$" else cur,
            gridcolor="#dcdcdc", zerolinecolor="#9aa", zerolinewidth=2,
            showline=False, ticks="",
        ),
        legend=dict(
            orientation="h", x=0.5, xanchor="center", y=-0.16, yanchor="top",
            font=dict(size=11, color=INK),
            bgcolor="rgba(0,0,0,0)", borderwidth=0,
            traceorder="reversed", itemwidth=30,
        ),
        hoverlabel=dict(align="left", bgcolor="#fbfbfb", bordercolor="#c9c9c9",
                        font=dict(family="SFMono-Regular, Menlo, Consolas, "
                                         "monospace", size=12, color=INK)),
        hovermode="closest",
        plot_bgcolor="#f2f2f2",
        paper_bgcolor="#f2f2f2",
        margin=dict(l=52, r=18, t=60, b=74),
        width=DESIGN[0], height=DESIGN[1],
    )
    return fig


def axis_order(fig, labels):
    """The drawn axis must run in the spec's order, oldest quarter first.

    Checked rather than trusted: this was wrong on six charts and nothing
    caught it, because a scrambled time axis still renders perfectly.
    """
    drawn = []
    for tr in fig.data:
        for x in (tr.x or []):
            if x is not None and x not in drawn:
                drawn.append(x)
    pinned = list(fig.layout.xaxis.categoryarray or [])
    return drawn[:len(labels)] == labels or pinned == labels


def validate(spec):
    """Nothing on this chart may be implied. A quarter is either reported --
    actual and estimate both present -- or it is ahead, with no actual."""
    warn = 0
    for p in spec.get("reported") or []:
        if p.get("actual") is None or p.get("estimate") is None:
            print(f"  ! {spec['ticker']} {p.get('label')}: reported quarter "
                  f"missing a figure", file=sys.stderr)
            warn += 1
    for p in spec.get("ahead") or []:
        if "actual" in p:
            print(f"  ! {spec['ticker']} {p.get('label')}: an unreported "
                  f"quarter cannot have an actual", file=sys.stderr)
            warn += 1
    if not (spec.get("reported") or []):
        print(f"  ! {spec['ticker']}: nothing reported", file=sys.stderr)
        warn += 1
    # Not a warning: the pair is drawn, only its surprise figure is withheld.
    # Printed so a run says which cards are carrying one.
    for p in spec.get("reported") or []:
        if p.get("basisUnverified"):
            print(f"  ~ {spec['ticker']} {p.get('label')}: basis unverified "
                  f"({p['actual']:+.2f} vs {p['estimate']:+.2f}), surprise "
                  f"withheld", file=sys.stderr)
    return warn


def main():
    spec = json.load(open(sys.argv[1]))
    stem = f"{spec['ticker']}-eps"
    warn = validate(spec)
    fig = build(spec)

    labels = ([p["label"] for p in (spec.get("reported") or [])] +
              [p["label"] for p in (spec.get("ahead") or [])])
    if not axis_order(fig, labels):
        print(f"  ! {spec['ticker']}: quarters would draw out of order",
              file=sys.stderr)
        warn += 1

    Path("out").mkdir(exist_ok=True)
    fig.write_html(f"out/{stem}.html", include_plotlyjs="cdn")

    if "--json" in sys.argv:
        charts = Path("charts")
        charts.mkdir(exist_ok=True)
        j = fig.to_plotly_json()
        lay = j["layout"]
        j["design"] = {"width": lay.pop("width"), "height": lay.pop("height")}
        (charts / f"{stem}.json").write_text(
            json.dumps(j, separators=(",", ":"), default=str))

    if "--png" in sys.argv:
        fig.write_image(f"out/{stem}.png", scale=2)

    last = spec["reported"][-1]
    print(f"{spec['ticker']:6} {last['label']} actual {last['actual']:+.2f} vs "
          f"{last['estimate']:+.2f}  ({warn} warning(s))")


if __name__ == "__main__":
    main()
