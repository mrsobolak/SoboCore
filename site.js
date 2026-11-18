/* Sobolak Technologies: draws the shop from products.js. No build step. */
(function () {
  'use strict';

  var data = window.SOBOLAK || { store: {}, products: [] };
  var store = data.store || {};
  var products = data.products || [];

  function $(sel) { return document.querySelector(sel); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function money(n) { return '$' + Number(n).toLocaleString('en-US'); }

  /* ---------- menu ---------- */
  var toggle = $('.nav-toggle');
  var nav = $('#nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------- footer date ---------- */
  var upd = $('#updated');
  if (upd && store.updated) upd.textContent = store.updated;

  /* ---------- contact ---------- */
  function mailto(subject, body) {
    return 'mailto:' + store.email +
      '?subject=' + encodeURIComponent(subject) +
      '&body=' + encodeURIComponent(body);
  }
  var contact = $('#contact-actions');
  if (contact) {
    var html = '';
    if (store.email) {
      html += '<a class="btn btn-gel" href="' + esc(mailto('Question for Sobolak Technologies', '')) + '">Email ' + esc(store.email) + '</a>';
    }
    if (store.phone) {
      html += '<a class="btn btn-glass" href="tel:' + esc(String(store.phone).replace(/[^+\d]/g, '')) + '">Call or text ' + esc(store.phone) + '</a>';
    }
    if (!html) html = '<p class="contact-pending">Contact details are being set up. Check back shortly.</p>';
    contact.innerHTML = html;
  }

  /* ---------- shop ---------- */
  var grid = $('#grid');
  if (!grid) return;

  var ART = { laptop: 1, sff: 1, tower: 1 };
  var COLORS = { black: 1, graphite: 1, silver: 1 };

  function art(kind, label) {
    var id = 'art-' + (ART[kind] ? kind : 'laptop');
    return '<svg class="art" viewBox="0 0 240 192" role="img" aria-label="' + esc(label) + '">' +
      '<use href="#' + id + '" width="240" height="150"/>' +
      '<g mask="url(#m-fade)"><use href="#' + id + '" width="240" height="150" transform="translate(0 284) scale(1 -1)"/></g>' +
      '</svg>';
  }

  var burstPoints = (function () {
    var pts = [], n = 18;
    for (var i = 0; i < n * 2; i++) {
      var r = i % 2 ? 42 : 50;
      var a = Math.PI * i / n;
      pts.push((50 + r * Math.sin(a)).toFixed(1) + ',' + (50 - r * Math.cos(a)).toFixed(1));
    }
    return pts.join(' ');
  })();

  function buyLink(p) {
    if (p.sold) return '';
    if (p.buyUrl) return '<a class="btn btn-gel" href="' + esc(p.buyUrl) + '">Buy now</a>';
    if (store.email) {
      var subject = 'I want the ' + p.name + ' (' + p.id + ')';
      var body = 'Hi, is the ' + p.name + ' (' + p.id + ')' +
        (p.price != null ? ' at ' + money(p.price) : '') + ' still available?\n\n';
      return '<a class="btn btn-gel" href="' + esc(mailto(subject, body)) + '">' +
        (p.price != null ? 'Buy this one' : 'Ask about it') + '</a>';
    }
    return '<a class="btn btn-gel" href="#contact">' + (p.price != null ? 'Buy this one' : 'Ask about it') + '</a>';
  }

  function card(p) {
    var saving = (p.ebay && p.price != null) ? p.ebay - p.price : 0;
    var color = COLORS[p.color] ? p.color : 'black';
    var specs = (p.specs || []).map(function (row) {
      return '<div><dt>' + esc(row[0]) + '</dt><dd>' + esc(row[1]) + '</dd></div>';
    }).join('');

    var price = p.price != null
      ? '<strong>' + money(p.price) + '</strong>' + (p.ebay ? '<span>eBay <s>' + money(p.ebay) + '</s></span>' : '')
      : '<strong>' + esc(p.priceLabel || 'Ask') + '</strong>';

    return '<article class="card' + (p.sold ? ' sold' : '') + '">' +
      '<div class="stage c-' + color + '">' +
        (p.grade ? '<span class="grade">Grade ' + esc(p.grade) + '</span>' : '') +
        (saving > 0 && !p.sold
          ? '<div class="burst"><svg viewBox="0 0 100 100" aria-hidden="true"><polygon points="' + burstPoints + '" fill="url(#g-burst)" stroke="#2f6b08" stroke-width="1.5"/></svg>' +
            '<span>Save<b>' + money(saving) + '</b></span></div>'
          : '') +
        art(p.art, p.name) +
      '</div>' +
      (p.sold ? '<div class="soldstamp">Sold</div>' : '') +
      '<div class="card-body">' +
        '<h3>' + esc(p.name) + '</h3>' +
        '<dl class="specs">' + specs + '</dl>' +
        (p.note ? '<p class="note">' + esc(p.note) + '</p>' : '') +
        '<div class="buy"><div class="price">' + price + '</div>' + buyLink(p) + '</div>' +
      '</div>' +
    '</article>';
  }

  var filter = 'all';
  var sort = 'featured';
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab'));
  var sortSel = $('#sort');

  function render() {
    var list = products.filter(function (p) { return filter === 'all' || p.type === filter; });
    var order = list.map(function (p, i) { return { p: p, i: i }; });
    order.sort(function (a, b) {
      if (!!a.p.sold !== !!b.p.sold) return a.p.sold ? 1 : -1;
      if (sort === 'low') {
        var pa = a.p.price == null ? Infinity : a.p.price;
        var pb = b.p.price == null ? Infinity : b.p.price;
        if (pa !== pb) return pa - pb;
      }
      if (sort === 'save') {
        var sa = a.p.ebay && a.p.price != null ? a.p.ebay - a.p.price : -1;
        var sb = b.p.ebay && b.p.price != null ? b.p.ebay - b.p.price : -1;
        if (sa !== sb) return sb - sa;
      }
      return a.i - b.i;
    });
    grid.innerHTML = order.length
      ? order.map(function (o) { return card(o.p); }).join('')
      : '<p class="empty">Nothing in this category right now. Check back soon.</p>';
    tabs.forEach(function (t) {
      t.setAttribute('aria-pressed', t.getAttribute('data-filter') === filter ? 'true' : 'false');
    });
  }

  tabs.forEach(function (t) {
    var f = t.getAttribute('data-filter');
    var n = products.filter(function (p) { return !p.sold && (f === 'all' || p.type === f); }).length;
    var count = t.querySelector('b');
    if (count) count.textContent = n;
    t.addEventListener('click', function () { filter = f; render(); });
  });
  if (sortSel) sortSel.addEventListener('change', function () { sort = sortSel.value; render(); });

  // "Shop laptops" / "Shop desktops" buttons pick the tab, then jump to the shop
  Array.prototype.forEach.call(document.querySelectorAll('a[data-filter]'), function (a) {
    a.addEventListener('click', function () { filter = a.getAttribute('data-filter'); render(); });
  });

  var demo = $('#demo-note');
  if (demo && store.demo) demo.hidden = false;

  render();

  /* ---------- price comparison ---------- */
  var cmp = $('#compare');
  var ex = products.filter(function (p) { return !p.sold && p.ebay && p.price != null && p.ebay > p.price; })[0];
  if (cmp && ex) {
    var short = (ex.specs || []).slice(0, 3).map(function (r) { return r[1]; }).join(', ');
    cmp.innerHTML =
      '<figcaption>' + esc(ex.name) + '<span>' + esc(short) + '</span></figcaption>' +
      '<div class="bar bar-ebay"><span>eBay</span><b>' + money(ex.ebay) + '</b></div>' +
      '<div class="bar bar-us" style="--w:' + Math.round(ex.price / ex.ebay * 100) + '%"><span>Sobolak</span><b>' + money(ex.price) + '</b></div>' +
      '<p class="compare-save"><b>' + money(ex.ebay - ex.price) + '</b> stays with you. Same machine.</p>';
    cmp.hidden = false;
  }
})();
