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
  // `state.reached` records whether the host answered at all, which is what
  // separates a throttled run from one the browser is not allowed to make.
  function quotePass(syms, lanes, onQuote, state) {
    var next = 0, missed = [];

    function pump() {
      if (next >= syms.length) return Promise.resolve();
      var sym = syms[next++];

      return fetch("https://stockanalysis.com/api/quotes/s/" +
                   encodeURIComponent(sym.toLowerCase()), { cache: "no-store" })
        .then(function (r) {
          if (state) state.reached = true;   // a reply, even a 404, is contact
          return r.ok ? r.json() : null;
        })
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
  //
  // Unless nothing answered at all: stockanalysis.com sends no CORS header to
  // the published origin, so from GitHub Pages every one of these requests is
  // blocked before it leaves the browser. Retrying a wall is just six seconds
  // of waiting for the same nothing, so a shutout gives up immediately.
  function fromStockAnalysis(syms, onQuote, onProgress) {
    var state = { reached: false };

    return quotePass(syms, LANES, onQuote, state)
      .then(function (missed) {
        if (!state.reached) return syms.slice();   // blocked, not throttled
        if (!missed.length) return [];
        onProgress(syms.length - missed.length, syms.length, "retrying " + missed.length);
        return wait(1500).then(function () { return quotePass(missed, 3, onQuote); });
      })
      .then(function (missed) {
        if (!missed.length) return [];
        if (!state.reached) return missed;
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

  // Live quotes, straight from the browser. Both sources only answer a page
  // served from localhost -- stockanalysis.com allowlists it, and the proxy
  // only exists when quotes.py is the server -- so on the published site
  // this returns nothing and the snapshot below is what the page shows.
  function fetchQuotes(syms, onQuote, onProgress) {
    onProgress = onProgress || function () {};
    return fromStockAnalysis(syms, onQuote, onProgress).then(function (hits) {
      if (hits) return { hits: hits, source: "stockanalysis.com" };
      return fromProxy(syms, onQuote).then(function (n) {
        return { hits: n, source: "local proxy" };
      });
    });
  }

  // prices.json: a committed snapshot, written by whatever can actually reach
  // a quote feed. Shape, so any writer can produce it:
  //
  //   { "generated": "2026-10-28T23:26:00Z",      ISO 8601, required
  //     "generatedLabel": "Oct 28, 2026, 7:26 PM EDT",   shown as-is
  //     "source": "IBKR",                         named on the page
  //     "quotes": [ { "t": "IREN", "price": 28.84, "pct": 5.1 } ] }
  //
  // A symbol the writer could not price is left out rather than written with
  // a null, so a gap reads as "no quote" instead of as a price of nothing.
  function snapshot() {
    return fetch("prices.json", { cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (doc) {
        if (!doc || !doc.quotes) return null;
        var map = {};
        (doc.quotes || []).forEach(function (q) {
          if (!q || !q.t || !isFinite(q.price)) return;
          map[String(q.t).toUpperCase()] =
            { price: Number(q.price), pct: isFinite(q.pct) ? Number(q.pct) : null };
        });
        doc.map = map;
        return doc;
      })
      .catch(function () { return null; });
  }

  // How old the snapshot is, in words, so a stale one cannot pass for live.
  function ageOf(iso) {
    var then = Date.parse(iso);
    if (!isFinite(then)) return null;
    var mins = Math.round((Date.now() - then) / 60000);
    if (mins < 2) return "just now";
    if (mins < 90) return mins + " min old";
    var hrs = Math.round(mins / 60);
    if (hrs < 36) return hrs + "h old";
    return Math.round(hrs / 24) + "d old";
  }

  // What the pages call. The snapshot paints first, so there is something on
  // screen immediately and the page never hangs on "loading"; a live fetch
  // then upgrades it where one is reachable. Never rejects -- a run that
  // priced nothing comes back as hits: 0 and says why.
  function prices(syms, onQuote, onProgress) {
    onProgress = onProgress || function () {};

    return snapshot().then(function (snap) {
      var base = null;

      if (snap) {
        var hits = 0;
        syms.forEach(function (s) {
          var q = snap.map[String(s).toUpperCase()];
          if (!q) return;
          hits++;
          onQuote(s, q.price, q.pct);
        });
        if (hits) {
          base = {
            hits: hits, live: false,
            source: snap.source || "snapshot",
            label: snap.generatedLabel || snap.generated || "snapshot",
            age: ageOf(snap.generated),
          };
          onProgress(hits, syms.length, "snapshot");
        }
      }

      // Nothing to show: say which half failed, rather than blaming the
      // snapshot for a live source's error or the other way round.
      function nothing(why) {
        return { hits: 0, live: false, source: null, label: null, age: null,
                 detail: "no snapshot in prices.json, and " + why };
      }

      return fetchQuotes(syms, onQuote, onProgress)
        .then(function (res) {
          if (res.hits) {
            return { hits: res.hits, live: true, source: res.source, label: null, age: null };
          }
          return base || nothing("no quote service this page can reach");
        })
        .catch(function (e) {
          return base || nothing("no quote service this page can reach (" +
                                 e.message + ")");
        });
    });
  }


  // the watchlist is a file now, not an inline block, so pages share one copy
  function watchlist() {
    return fetch("watchlist.json", { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error("watchlist.json " + r.status);
      return r.json();
    });
  }

  // Holdings is a local-only page: holdings.html and holdings.json are both in
  // .gitignore, because this repo is public and Pages serves it. So the tab is
  // added at runtime on localhost rather than written into every page's markup,
  // where it would ship a dead link to the live site.
  function isLocal() {
    return location.hostname === "localhost" ||
           location.hostname === "127.0.0.1" ||
           location.protocol === "file:";
  }

  function nav() {
    var tabs = document.querySelector("nav.tabs");
    if (tabs && isLocal() && !tabs.querySelector('a[href="holdings.html"]')) {
      var a = document.createElement("a");
      a.className = "tab";
      a.href = "holdings.html";
      a.textContent = "Holdings";
      tabs.appendChild(a);
    }

    var here = location.pathname.split("/").pop() || "heatmap.html";
    [].forEach.call(document.querySelectorAll("nav.tabs a.tab"), function (a) {
      a.classList.toggle("on", a.getAttribute("href") === here);
    });
  }

  return {
    esc: esc, money: money, pctText: pctText,
    peOf: peOf, sectorRank: sectorRank, sectorLabel: sectorLabel, SECTORS: SECTORS,
    quotePass: quotePass, wait: wait,
    prices: prices, snapshot: snapshot, fetchQuotes: fetchQuotes,
    fromStockAnalysis: fromStockAnalysis, fromProxy: fromProxy,
    watchlist: watchlist, nav: nav,
  };
})();
