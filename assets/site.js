/* Shared helpers for the stock-kb pages.

   Each tab is its own page now, so anything more than one page needs lives
   here: HTML escaping, number formatting, sector naming, and the paced quote
   fetcher that the heatmap and catalysts pages both use.
*/
var Site = (function () {
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // A ticker shows when it carries ANY switched-on category, so picking
  // "AI" plus "Semiconductor" widens the view rather than narrowing it.
  function money(n) {
    if (n === null || n === undefined || isNaN(n)) return "--";
    return "$" + Number(n).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function pctText(p) {
    if (p === null || p === undefined || isNaN(p)) return "\u2014";
    return (p >= 0 ? "+" : "") + Number(p).toFixed(2) + "%";
  }

  function peOf(q) { return q.pe === null || q.pe === undefined ? null : q.pe; }

  // Sector reading order: the AI and silicon complex first, then the
  // machines, then what they are launched and pointed at, then the rest of
  // the book. A ticker carries several tags, so its sector is simply the
  // highest-ranked tag it holds -- NVDA reads as AI, not as Physical AI.
  var SECTORS = [
    "AI", "AI Infra", "AI Memory", "Semiconductor",
    "Robotics", "Physical AI",
    "Space", "Defense", "Aerospace",
    "Quantum",
    "Software", "Cloud", "Data Center", "Networking", "Hardware",
    "Crypto", "Mining", "Fintech",
    "Consumer Tech", "Media", "Retail",
    "Telecom", "Nuclear", "Uranium", "Power", "Energy", "Industrials",
    "Auto", "Homebuilder",
    "ETF", "Fund", "Broad Market", "Leveraged", "Private Tech", "SPAC",
    "Unclassified"
  ];

  function sectorRank(q) {
    if (q.sector) {                      // an explicit sector wins outright
      var at = SECTORS.indexOf(q.sector);
      if (at !== -1) return at;
    }
    var best = SECTORS.length;
    (q.tags || []).forEach(function (t) {
      var at = SECTORS.indexOf(t);
      if (at !== -1 && at < best) best = at;
    });
    return best;
  }

  // The label under a ticker. With categories switched on it names the one
  // that put the tile on screen, so the board explains its own filtering;
  // otherwise it names the ticker's primary sector.
  // `picked` is the heatmap's active category filter. Other pages have no
  // filter, so it defaults to empty and the ticker's own sector wins.
  function sectorLabel(q, picked) {
    picked = picked || [];
    var tags = q.tags || [];
    var pool = tags;

    // A ticker can name its own sector when the ranking would pick a tag
    // that is true but not what the company is -- MU carries AI Infra, but
    // it is a memory maker.
    if (q.sector && !picked.length) return q.sector;

    if (picked.length) {
      var hit = tags.filter(function (t) { return picked.indexOf(t) !== -1; });
      if (hit.length) pool = hit;
    }

    var best = null, bestAt = SECTORS.length + 1;
    pool.forEach(function (t) {
      var at = SECTORS.indexOf(t);
      if (at === -1) at = SECTORS.length;      // unranked tags still label
      if (at < bestAt) { bestAt = at; best = t; }
    });
    return best;
  }

  var LANES = 6;

  // One pass over a list of symbols. Anything that does not come back with a
  // price is returned as a miss rather than written off, so it can be retried.
  function quotePass(syms, lanes, onQuote) {
    var next = 0, missed = [];

    function pump() {
      if (next >= syms.length) return Promise.resolve();
      var sym = syms[next++];

      return fetch("https://stockanalysis.com/api/quotes/s/" +
                   encodeURIComponent(sym.toLowerCase()), { cache: "no-store" })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (j) {
          var d = j && j.status === 200 ? j.data : null;
          if (d && isFinite(d.p)) {
            onQuote(sym, Number(d.p), isFinite(d.cp) ? Number(d.cp) : null);
          } else {
            missed.push(sym);
          }
        })
        .catch(function () { missed.push(sym); })
        .then(pump);
    }

    var running = [];
    for (var i = 0; i < lanes; i++) running.push(pump());
    return Promise.all(running).then(function () { return missed; });
  }

  function wait(ms) {
    return new Promise(function (r) { setTimeout(r, ms); });
  }

  // A hundred symbols in quick succession can get the whole run rate-limited,
  // and a limited request looks exactly like a symbol with no data. So retry
  // the misses twice, slower and narrower each time, before calling them dry.
  function fromStockAnalysis(syms, onQuote, onProgress) {
    return quotePass(syms, LANES, onQuote)
      .then(function (missed) {
        if (!missed.length) return [];
        onProgress(syms.length - missed.length, syms.length, "retrying " + missed.length);
        return wait(1500).then(function () { return quotePass(missed, 3, onQuote); });
      })
      .then(function (missed) {
        if (!missed.length) return [];
        onProgress(syms.length - missed.length, syms.length, "retrying " + missed.length);
        return wait(4000).then(function () { return quotePass(missed, 2, onQuote); });
      })
      .then(function (missed) { return syms.length - missed.length; });
  }

  // Local fallback: quotes.py fetches server-side, where CORS never applies,
  // and covers names stockanalysis.com does not carry.
  function fromProxy(syms, onQuote) {
    return fetch("api/quotes?symbols=" + encodeURIComponent(syms.join(",")), { cache: "no-store" })
      .then(function (r) {
        if (!r.ok) throw new Error("proxy " + r.status);
        return r.json();
      })
      .then(function (data) {
        var hits = 0;
        (data.quotes || []).forEach(function (q) {
          if (!q.error) { hits++; onQuote(q.symbol, q.price, q.pct); }
        });
        return hits;
      });
  }


  // the watchlist is a file now, not an inline block, so pages share one copy
  function watchlist() {
    return fetch("watchlist.json", { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error("watchlist.json " + r.status);
      return r.json();
    });
  }

  function nav() {
    var here = location.pathname.split("/").pop() || "heatmap.html";
    [].forEach.call(document.querySelectorAll("nav.tabs a.tab"), function (a) {
      a.classList.toggle("on", a.getAttribute("href") === here);
    });
  }

  return {
    esc: esc, money: money, pctText: pctText,
    peOf: peOf, sectorRank: sectorRank, sectorLabel: sectorLabel, SECTORS: SECTORS,
    quotePass: quotePass, wait: wait,
    fromStockAnalysis: fromStockAnalysis, fromProxy: fromProxy,
    watchlist: watchlist, nav: nav,
  };
})();
