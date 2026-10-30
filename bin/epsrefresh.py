#!/usr/bin/env python3
"""Refresh the earnings actual-vs-estimate charts, and redraw only what moved.

    python3 bin/epsrefresh.py            # every card
    python3 bin/epsrefresh.py SNDK AMZN  # just these

The charts went stale on their own: the vendor posts a quarter's actual a day
or so after the company reports, so a card built on results day shows the
prior quarter as the most recent dot and silently stays that way until someone
re-runs the fetcher by hand. This is what the daily job calls so that does not
happen.

Two things it does that a plain `epsfetch.py --all` does not:

- **It only redraws what changed.** Re-rendering 70 charts a day would churn
  70 files in git for nothing.
- **It keeps the old `source` line when the figures are unchanged.** Every
  spec records the date it was read, so refetching rewrites all 70 specs each
  morning even when not one number moved. The read date is only interesting on
  a spec whose numbers it explains, so an unchanged spec keeps the date it
  already had and stays out of the diff.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXAMPLES = ROOT / "examples"


def digest(path):
    """The spec's figures, with the read date left out.

    `source` carries "read <date>", which changes on every run. Comparing it
    would make every card look like it moved.
    """
    try:
        spec = json.loads(path.read_text())
    except (OSError, ValueError):
        return None, None
    src = spec.pop("source", None)
    return json.dumps(spec, sort_keys=True), src


def stale(ticker, spec_path):
    """Is the drawn chart missing, or older than the spec it is drawn from?"""
    chart = ROOT / "charts" / f"{ticker}-eps.json"
    if not chart.exists():
        return True
    return chart.stat().st_mtime < spec_path.stat().st_mtime


def specs(only):
    for p in sorted(EXAMPLES.glob("*-eps.json")):
        t = p.name[:-len("-eps.json")].upper()
        if not only or t in only:
            yield t, p


def run(args):
    r = subprocess.run([sys.executable] + args, cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + r.stderr)
    return r


def main():
    only = {a.upper() for a in sys.argv[1:] if not a.startswith("-")}

    before = {t: digest(p) for t, p in specs(only)}
    # Staleness has to be read BEFORE the fetch. epsfetch.py rewrites every
    # spec it touches, new read date and all, so after it has run every spec
    # is newer than its chart and an mtime test would redraw all 70 every day.
    was_stale = {t for t, p in specs(only) if stale(t, p)}

    args = ["bin/epsfetch.py"] + (sorted(only) if only else ["--all"])
    print(f"fetching {'the named cards' if only else 'every card'} ...")
    r = run(args)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(no output)")

    changed, restored = [], 0
    for t, p in specs(only):
        now_data, now_src = digest(p)
        was_data, was_src = before.get(t, (None, None))
        if now_data is None:
            continue
        # A spec can also be updated by something other than this script --
        # epsfetch.py run by hand, or the add-ticker skill. Comparing only
        # against this run's own snapshot would leave that chart stale for
        # good, so a chart that was older than its spec when this started is
        # redrawn whatever moved it.
        if t in was_stale:
            changed.append((t, p))
            continue
        if was_data is not None and now_data == was_data and was_src:
            # same figures: put the old read date back so git sees no change
            spec = json.loads(p.read_text())
            if spec.get("source") != was_src:
                spec["source"] = was_src
                p.write_text(json.dumps(spec, indent=1) + "\n")
                restored += 1
            continue
        changed.append((t, p))

    for t, p in changed:
        out = run(["bin/epsdots.py", str(p.relative_to(ROOT)), "--json"])
        tail = [l for l in out.stdout.splitlines() if "warning" in l]
        print(f"  redrew {t}" + (f"  {tail[-1]}" if tail else ""))

    if changed:
        run(["bin/epsnotes.py"])
        print(f"\n{len(changed)} chart(s) redrawn: "
              + ", ".join(t for t, _ in changed))
    else:
        print("\nno figures moved")
    print(f"{restored} spec(s) left alone with their previous read date")


if __name__ == "__main__":
    main()
