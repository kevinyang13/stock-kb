#!/usr/bin/env python3
"""Version the shared CSS and JS links in every page.

The pages carry no-cache meta tags, but those only cover the HTML -- a browser
still serves assets/site.css and assets/site.js from its own cache, so a style
or script change can sit invisible behind a stale copy. Appending ?v=<stamp>
makes each edit a new URL. Run this after changing anything under assets/.

    python3 bin/stamp.py
"""
import re
import sys
from pathlib import Path

ASSETS = ("site.css", "site.js", "sankey.js")


def stamp() -> str:
    """The working tree's newest asset mtime, as a short digits-only token."""
    newest = max(Path("assets", a).stat().st_mtime for a in ASSETS
                 if Path("assets", a).exists())
    return str(int(newest))


def main() -> int:
    if not Path("assets").is_dir():
        sys.exit("run me from the repo root")
    v = stamp()
    pat = re.compile(r'(assets/(?:' + "|".join(map(re.escape, ASSETS)) + r'))(\?v=\d+)?')
    touched = []
    for page in sorted(Path(".").glob("*.html")):
        src = page.read_text()
        out = pat.sub(lambda m: f"{m.group(1)}?v={v}", src)
        if out != src:
            page.write_text(out)
            touched.append(page.name)
    print(f"stamp {v} -> {', '.join(touched) if touched else 'no change'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
