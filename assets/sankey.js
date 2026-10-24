// Renders an income statement Sankey from the figure JSON that bin/sankey.py
// emits with --json. Python owns the layout; this file only rescales it to the
// container, because every margin and font size in that JSON is in pixels
// against a fixed design width.
const Sankey = (() => {
  const MIN_SCALE = 0.42;   // below this the 12px sub-lines stop being readable

  function scaled(fig, px) {
    const s = Math.max(MIN_SCALE, Math.min(1, px / fig.design.width));
    const f = JSON.parse(JSON.stringify({ data: fig.data, layout: fig.layout }));

    for (const k of ['l', 'r', 't', 'b']) f.layout.margin[k] *= s;
    f.layout.title.font.size *= s;

    for (const a of f.layout.annotations || []) {
      a.font.size *= s;
      // the sub-lines set their own size inline, so scale those too
      a.text = a.text.replace(/font-size:([\d.]+)px/g,
        (_, n) => `font-size:${(n * s).toFixed(1)}px`);
    }
    for (const t of f.data) {
      if (!t.node) continue;
      t.node.pad *= s;
      t.node.thickness *= s;
    }

    f.layout.width = fig.design.width * s;
    f.layout.height = fig.design.height * s;
    return f;
  }

  function draw(div, fig) {
    const box = div.parentElement;
    const px = box.clientWidth;
    const f = scaled(fig, px);
    // Below MIN_SCALE the chart stops shrinking and the box pans instead --
    // squeezing a five-column diagram into 390px makes the text unreadable
    // long before it makes it fit.
    const pans = f.layout.width > px + 1;
    box.style.overflowX = pans ? 'auto' : 'hidden';
    // centring a panned chart starts it half-scrolled, mid-diagram
    box.style.justifyContent = pans ? 'flex-start' : 'center';
    return Plotly.react(div, f.data, f.layout, {
      displayModeBar: false,
      responsive: false,   // we do our own scaling, pixel margins need it
      doubleClick: false,
    });
  }

  // Draws fig into div and keeps it sized to its parent. Mounting twice on the
  // same div replaces the first mount rather than stacking observers on it.
  function mount(div, fig) {
    unmount(div);
    draw(div, fig);
    let w = div.parentElement.clientWidth;
    const obs = new ResizeObserver(() => {
      const now = div.parentElement.clientWidth;
      if (Math.abs(now - w) < 8) return;   // ignore the reflow we just caused
      w = now;
      draw(div, fig);
    });
    obs.observe(div.parentElement);
    div._sankeyObs = obs;
  }

  function unmount(div) {
    if (div._sankeyObs) { div._sankeyObs.disconnect(); delete div._sankeyObs; }
    if (div.data) Plotly.purge(div);
  }

  const cache = new Map();

  async function load(stem) {
    if (!cache.has(stem)) {
      const r = await fetch(`charts/${stem}.json`);
      if (!r.ok) throw new Error(`${stem}: HTTP ${r.status}`);
      cache.set(stem, await r.json());
    }
    return cache.get(stem);
  }

  return { mount, unmount, load, draw };
})();
