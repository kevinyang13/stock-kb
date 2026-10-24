// Renders an income statement Sankey from the figure JSON that bin/sankey.py
// emits with --json. Python owns the layout; this file only rescales it to the
// container, because every margin and font size in that JSON is in pixels
// against a fixed design width.
//
// Zoom re-renders at a larger scale rather than scaling the pixels of a drawn
// chart: a plotly sankey is not a cartesian plot, so it has no native zoom, and
// a CSS transform would blur the type. Re-laying it out keeps the text sharp
// and the hover hit-boxes true.
const Sankey = (() => {
  const MIN_SCALE = 0.42;   // below this the 12px sub-lines stop being readable
  const MAX_SCALE = 3.5;    // past this a single band fills the viewport
  const FIT = 1;            // zoom 1 == fit the container's width
  const STEPS = [0.5, 0.75, FIT, 1.5, 2, 2.5, 3];
  const PAN_SLOP = 4;       // px of movement before a press becomes a drag

  function scaled(fig, px) {
    const s = Math.max(MIN_SCALE, Math.min(MAX_SCALE, px / fig.design.width));
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

  // The scale a zoom of 1 lands on, i.e. the chart fitted to the box.
  function fitScale(fig, box) {
    return Math.max(MIN_SCALE,
      Math.min(MAX_SCALE, box.clientWidth / fig.design.width));
  }

  function draw(div, fig, zoom) {
    const box = div.parentElement;
    const z = zoom == null ? (div._sankeyZoom || FIT) : zoom;
    div._sankeyZoom = z;
    div._sankeyFig = fig;

    const f = scaled(fig, box.clientWidth * z);
    // Whatever does not fit is panned rather than shrunk further. Squeezing a
    // five-column diagram into 390px makes the text unreadable long before it
    // makes it fit, and that is also what zooming in asks for.
    const pansX = f.layout.width > box.clientWidth + 1;
    box.style.overflowX = pansX ? 'auto' : 'hidden';
    // centring a panned chart starts it half-scrolled, mid-diagram
    box.style.justifyContent = pansX ? 'flex-start' : 'center';
    // Zoomed in, the box becomes a window: without a cap the page itself grows
    // to 3x chart height and the controls scroll away from the chart.
    box.style.maxHeight = pansX ? '78vh' : '';
    box.style.overflowY = pansX ? 'auto' : '';
    box.classList.toggle('is-panning', pansX);

    // newPlot, not react: on a sankey, react moves the node rects but leaves the
    // link paths on their old geometry, so a resize or zoom loses every band.
    return Plotly.newPlot(div, f.data, f.layout, {
      displayModeBar: false,
      responsive: false,   // we do our own scaling, pixel margins need it
      doubleClick: false,
    });
  }

  // Re-renders at `z`, keeping whatever sits at `anchor` (box-relative px,
  // default the middle of the view) under the same point afterwards.
  function setZoom(div, z, anchor) {
    const fig = div._sankeyFig;
    if (!fig) return Promise.resolve();
    const box = div.parentElement;
    z = Math.max(STEPS[0], Math.min(STEPS[STEPS.length - 1], z));

    const ax = anchor ? anchor.x : box.clientWidth / 2;
    const ay = anchor ? anchor.y : box.clientHeight / 2;
    const wasW = div.clientWidth || box.clientWidth;
    const wasH = div.clientHeight || box.clientHeight;
    const fx = (box.scrollLeft + ax) / wasW;
    const fy = (box.scrollTop + ay) / wasH;

    return Promise.resolve(draw(div, fig, z)).then(() => {
      box.scrollLeft = fx * div.clientWidth - ax;
      box.scrollTop = fy * div.clientHeight - ay;
      if (div._sankeyOnZoom) div._sankeyOnZoom(z, zoomState(div));
    });
  }

  function zoomState(div) {
    const z = div._sankeyZoom || FIT;
    return {
      zoom: z,
      atMin: z <= STEPS[0] + 1e-6,
      atMax: z >= STEPS[STEPS.length - 1] - 1e-6,
      atFit: Math.abs(z - FIT) < 1e-6,
      // what the chart is actually drawn at, which the fit may have clamped
      scale: div._sankeyFig
        ? Math.min(MAX_SCALE, fitScale(div._sankeyFig, div.parentElement) * z)
        : z,
    };
  }

  function step(div, dir, anchor) {
    const z = div._sankeyZoom || FIT;
    const next = dir > 0
      ? STEPS.find(s => s > z + 1e-6)
      : [...STEPS].reverse().find(s => s < z - 1e-6);
    return setZoom(div, next == null ? z : next, anchor);
  }

  function anchorOf(box, ev) {
    const r = box.getBoundingClientRect();
    return { x: ev.clientX - r.left, y: ev.clientY - r.top };
  }

  // Wheel-zoom, drag-to-pan and double-click-to-fit, all on the box.
  function wireGestures(div) {
    const box = div.parentElement;

    const onWheel = (ev) => {
      // plain scrolling still scrolls; zoom needs the usual modifier, which is
      // also what a trackpad pinch sends
      if (!ev.ctrlKey && !ev.metaKey) return;
      ev.preventDefault();
      const z = div._sankeyZoom || FIT;
      setZoom(div, z * (ev.deltaY < 0 ? 1.12 : 1 / 1.12), anchorOf(box, ev));
    };

    let from = null;
    const onDown = (ev) => {
      if (ev.button !== 0 || !box.classList.contains('is-panning')) return;
      from = { x: ev.clientX, y: ev.clientY,
               left: box.scrollLeft, top: box.scrollTop, dragging: false };
    };
    const onMove = (ev) => {
      if (!from) return;
      const dx = ev.clientX - from.x, dy = ev.clientY - from.y;
      // a press that never travels is a click, and hover must still work
      if (!from.dragging && Math.hypot(dx, dy) < PAN_SLOP) return;
      from.dragging = true;
      box.classList.add('is-dragging');
      box.scrollLeft = from.left - dx;
      box.scrollTop = from.top - dy;
    };
    const onUp = () => { from = null; box.classList.remove('is-dragging'); };

    box.addEventListener('wheel', onWheel, { passive: false });
    box.addEventListener('pointerdown', onDown);
    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', onUp);
    box.addEventListener('dblclick', () => setZoom(div, FIT));

    return () => {
      box.removeEventListener('wheel', onWheel);
      box.removeEventListener('pointerdown', onDown);
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
    };
  }

  // Draws fig into div and keeps it sized to its parent. Mounting twice on the
  // same div replaces the first mount rather than stacking observers on it.
  // `onZoom(z, state)` fires whenever the zoom changes, for a controls strip.
  function mount(div, fig, onZoom) {
    unmount(div);
    div._sankeyZoom = FIT;
    div._sankeyOnZoom = onZoom || null;
    draw(div, fig, FIT);

    let w = div.parentElement.clientWidth;
    const obs = new ResizeObserver(() => {
      const now = div.parentElement.clientWidth;
      if (Math.abs(now - w) < 8) return;   // ignore the reflow we just caused
      w = now;
      draw(div, fig);
    });
    obs.observe(div.parentElement);
    div._sankeyObs = obs;
    div._sankeyUnwire = wireGestures(div);
    if (onZoom) onZoom(FIT, zoomState(div));
  }

  function unmount(div) {
    if (div._sankeyObs) { div._sankeyObs.disconnect(); delete div._sankeyObs; }
    if (div._sankeyUnwire) { div._sankeyUnwire(); delete div._sankeyUnwire; }
    delete div._sankeyFig;
    delete div._sankeyOnZoom;
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

  return { mount, unmount, load, draw, setZoom, step, zoomState, FIT, STEPS };
})();
