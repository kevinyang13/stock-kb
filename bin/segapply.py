#!/usr/bin/env python3
"""Write a hand-sourced revenue split into an income statement spec.

bin/segfetch.py covers the names stockanalysis's segment endpoint can reach.
This covers the rest, where the figures had to come from the filer itself --
the quarter's own 10-Q disaggregation note (fetched through EDGAR's rendered
R##.htm reports), the 8-K exhibit, or the company's release for a filer that
is not with the SEC.

Each entry carries the current and year-ago figure, in millions of the
currency the chart already draws, so the growth row is computed rather than
copied. Values are checked as the chart will round them: the rounded segments
must add up to the revenue the chart already shows.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent

# The segment colours the hand-built charts already use, in the order they
# were used there, so a fetched split looks like the rest of the page.
PALETTE = ["#e8502a", "#1b1b7a", "#c8a020", "#f0a030", "#6cb6e8",
           "#7cd07c", "#2f9e6e"]

# ticker -> (source note, [(segment, this quarter, year ago or None)])
# Figures in millions of the spec's own currency.
DATA = {
 "T": ("AT&T 3Q26 earnings release, Exhibit 99.1 to the 8-K filed 2026-10-21", [
     ("Advanced Connectivity", 29481, 27503),
     ("Legacy", 1519, 2013),
     ("Latin America", 1240, 1095)]),
 "GE": ("GE Aerospace 3Q26 earnings release, Exhibit 99.1", [
     ("Commercial Engines & Services", 10342, 8521),
     ("Defense & Propulsion Tech", 3469, 3251),
     ("Insurance & other", 307, 409)]),
 "COHR": ("Coherent FQ4 FY26 earnings release, Exhibit 99.1", [
     ("Datacenter & Communications", 1615.0, 1018.3),
     ("Industrial", 430.5, 511.1)]),
 "SNOW": ("Snowflake 10-Q, quarter ended Jul 31 2026, disaggregation note", [
     ("Product", 1491.861, 1090.496),
     ("Professional services & other", 54.932, 54.473)]),
 "COIN": ("Coinbase 10-Q, quarter ended Jun 30 2026, revenue by source", [
     ("Transaction revenue", 599.156, 764.270),
     ("Subscription & services", 555.145, 632.243)]),
 "IONQ": ("IonQ 10-Q, quarter ended Jun 30 2026, disaggregation note", [
     ("Quantum hardware", 46.467, 14.066),
     ("Platform, consulting & support", 33.583, 6.628)]),
 "LUNR": ("Intuitive Machines 10-Q, quarter ended Jun 30 2026, by customer", [
     ("Civil", 76.281, 46.509),
     ("Commercial", 66.279, 2.106),
     ("National security", 60.852, 1.698),
     ("Grant revenue", 2.756, None)]),
 "MARA": ("MARA 10-Q, quarter ended Jun 30 2026, disaggregation note", [
     ("Block rewards", 156.492, 218.309),
     ("Mining participant", 12.767, 11.024),
     ("Other", 4.578, 4.944),
     ("Transaction fees", 1.044, 3.044)]),
 "MRVL": ("Marvell 10-Q, quarter ended Aug 1 2026, net revenue by end market", [
     ("Data center", 2171.5, 1490.5),
     ("Communications & other", 567.8, 515.6)]),
 "PL": ("Planet Labs 10-Q, quarter ended Jul 31 2026, revenue by customer", [
     ("Defense & intelligence", 80.995, 41.909),
     ("Commercial", 17.559, 15.051),
     ("Civil government", 17.498, 16.426)]),
 "QBTS": ("D-Wave 10-Q, quarter ended Jun 30 2026, disaggregation note", [
     ("QCaaS", 1.860, 1.241),
     ("Professional services", 0.929, 0.785),
     ("System sales", 0.255, 1.025)]),
 "RDW": ("Redwire 10-Q, quarter ended Jun 30 2026, segment reporting note", [
     ("Defense Tech", 61.882, 5.078),
     ("Space", 55.192, 56.682)]),
 "FLY": ("Firefly Aerospace 10-Q, quarter ended Jun 30 2026, disaggregation", [
     ("Spacecraft solutions", 108.283, 9.200),
     ("Launch services", 9.400, 6.349)]),
 "HD": ("Home Depot 10-Q, quarter ended Aug 2 2026, net sales by segment", [
     ("Hardlines", 14445, 14127),
     ("Building Materials", 14432, 14225),
     ("Décor", 13929, 13805),
     ("Other", 5055, 3120)]),
 "HIVE": ("HIVE Digital 10-Q, quarter ended Jun 30 2026, segmented information", [
     ("Digital currency mining", 72.060, 40.797),
     ("HPC hosting", 7.060, 4.814)]),
 "VOYG": ("Voyager Technologies 10-Q, quarter ended Jun 30 2026, net sales note", [
     ("U.S. government", 49.148, 42.070),
     ("Commercial", 3.601, 3.564)]),
 "MDA": ("MDA Space Q2 2026 results release, revenue by business area", [
     ("Satellite Systems", 336.1, 232.6),
     ("Robotics & Space Operations", 99.5, 88.0),
     ("Geointelligence", 63.0, 52.7)]),
 # The filing splits the service side in two -- collaborative research and
 # professional services $952K, access to quantum systems $88K -- but at the
 # one decimal this chart draws they round to 1.0 and 0.1, which adds $0.1M of
 # revenue the company did not report. Shown as one service line instead.
 "RGTI": ("Rigetti 10-Q, quarter ended Jun 30 2026, disaggregation note; the "
          "two service lines (research and professional services $952K, access "
          "to quantum systems $88K) are shown as one", [
     ("Quantum computers & parts", 4.098, None),
     ("Research, services & access", 1.040, 1.801)]),
}

# Names that keep a single revenue bar, and why. The skill asks for this to be
# said on the card rather than left to look like a split nobody fetched.
NONE = {
 "ARQQ": "Arqit reports one segment and gives no revenue split in its interim results.",
 "ASTS": "AST SpaceMobile's 10-Q carries no revenue disaggregation -- one line, one segment.",
 "CLSK": "CleanSpark reports one segment, bitcoin mining, and splits no revenue out of it.",
 "CRWV": "CoreWeave discloses revenue by geography only; no product or segment split.",
 "DDOG": "Datadog discloses revenue by geography only; no product or segment split.",
 "HUT": ("Hut 8 reports Power, Digital Infrastructure and Compute, but intersegment "
         "eliminations are $36.0M against $74.9M of revenue, so the three do not add "
         "up to the bar: gross segment revenue was Compute $72.5M, Digital "
         "Infrastructure $33.0M, Power $5.5M."),
 "INFQ": "Infleqtion discloses revenue by geography and by government share only.",
 "NET": "Cloudflare discloses revenue by geography and sales channel only.",
 "NU": ("Nu Holdings' chart is built on the aggregator's net revenue line, which no "
        "reported split adds up to."),
 "OUST": "Ouster reports one segment and discloses revenue by geography only.",
 "SKHY": "SK Hynix reports a single semiconductor segment.",
 "SMCI": "Super Micro's FY26 10-K discloses net sales by geography only.",
 "XNDU": "Xanadu gives no revenue split in its interim results.",
}


def specs():
    out = {}
    for p in sorted((HERE / "examples").glob("*.json")):
        if p.name.endswith("-debt.json"):
            continue
        try:
            s = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        if "revenue" in s and "ticker" in s:
            out[s["ticker"]] = (p, s)
    return out


def main():
    args = {a.upper() for a in sys.argv[1:] if not a.startswith("--")}
    dry = "--dry-run" in sys.argv
    have = specs()
    ok = bad = 0

    for t, (src, rows) in DATA.items():
        if args and t not in args:
            continue
        if t not in have:
            print(f"  ! {t}: no spec")
            bad += 1
            continue
        p, spec = have[t]
        # the figures are in millions; the spec may draw billions or trillions
        div = {"M": 1, "B": 1e3, "T": 1e6}[spec.get("unit", "M")]
        dec = spec.get("decimals", 1)

        segs = []
        for name, now, was in rows:
            v = round(now / div, dec)
            if abs(v) < 10 ** -dec / 2:
                continue                      # a band of zero width
            seg = {"name": name, "value": v}
            if was:
                g = round((now / was - 1) * 100)
                # A segment coming off a near-zero base prints "+3484% Y/Y",
                # which says less than the figure it grew from.
                if g > 999:
                    seg["note"] = (f"from {spec.get('currency', '$')}"
                                   f"{was / div:,.{dec}f}{spec.get('unit', 'M')}"
                                   " a year ago")
                else:
                    seg["yoy"] = g
            segs.append(seg)
        segs.sort(key=lambda s: -s["value"])
        for i, seg in enumerate(segs):
            seg["color"] = PALETTE[i % len(PALETTE)]

        total = round(sum(s["value"] for s in segs), dec)
        slack = max(abs(spec["revenue"]) * 0.005, 10 ** -dec)
        if abs(total - spec["revenue"]) > slack:
            print(f"  ! {t}: segments round to {total:,.{dec}f} against the "
                  f"chart's {spec['revenue']:,.{dec}f}")
            bad += 1
            continue

        shown = ", ".join(f"{s['name']} {s['value']:,.{dec}f}" for s in segs)
        print(f"{t:6} {len(segs)}: {shown}")
        if not dry:
            spec["segments"] = segs
            spec["segment_source"] = src
            p.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
        ok += 1

    print(f"\n{'checked' if dry else 'wrote'} {ok}  rejected {bad}")


if __name__ == "__main__":
    main()
