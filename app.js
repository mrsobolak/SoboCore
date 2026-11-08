/* Sobolak Technologies — WMP-style site. Plain JS, no dependencies. */
(function () {
  'use strict';
  var wmp = document.getElementById('wmp');
  var screens = Array.prototype.slice.call(document.querySelectorAll('.screen'));
  var order = screens.map(function (s) { return s.id; });
  var tasks = Array.prototype.slice.call(document.querySelectorAll('.task'));
  var plItems = Array.prototype.slice.call(document.querySelectorAll('#pl-list li'));
  var stText = document.getElementById('st-text');
  var stTime = document.getElementById('st-time');
  var seekFill = document.getElementById('seek-fill');
  var seekKnob = document.getElementById('seek-knob');
  var btnPlay = document.getElementById('btn-play');
  var current = 'now-playing';
  var plPick = null;
  plItems.forEach(function (li) { li.querySelector('a').addEventListener('click', function () { plPick = li; }); });
  var playing = true;

  /* ---------- storage that may not exist ---------- */
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function save(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  /* ---------- sections ---------- */
  function show(id, push) {
    if (order.indexOf(id) < 0) id = 'now-playing';
    current = id;
    screens.forEach(function (s) { s.hidden = s.id !== id; });
    tasks.forEach(function (t) { t.classList.toggle('active', t.getAttribute('data-section') === id); });
    document.getElementById('viewer').classList.toggle('is-page', id !== 'now-playing');
    var marked = false;
    plItems.forEach(function (li) {
      var a = li.querySelector('a');
      var hit = !marked && a.getAttribute('data-section') === id && (plPick === null || plPick === li);
      if (hit) marked = true;
      li.classList.toggle('current', hit);
    });
    plPick = null;
    var el = document.getElementById(id);
    var title = el.getAttribute('data-title') || id;
    document.title = (id === 'now-playing' ? '' : title + ' · ') + 'Sobolak Technologies';
    stText.textContent = id === 'now-playing'
      ? 'Album: Sobolak Technologies · Michigan · Est. 2024'
      : title + ' · Sobolak Technologies';
    var i = order.indexOf(id);
    var pct = order.length > 1 ? (i / (order.length - 1)) * 100 : 0;
    seekFill.style.width = pct + '%';
    seekKnob.style.left = pct + '%';
    if (push !== false && location.hash !== '#' + id) {
      if (history.replaceState) history.replaceState(null, '', '#' + id); else location.hash = id;
    }
    if (id !== 'now-playing') el.scrollTop = 0;
    if (id === 'now-playing') resize();
  }
  function step(d) {
    var i = order.indexOf(current);
    show(order[(i + d + order.length) % order.length]);
  }
  window.addEventListener('hashchange', function () { show(location.hash.slice(1) || 'now-playing', false); });

  /* ---------- menus ---------- */
  var menus = Array.prototype.slice.call(document.querySelectorAll('.menu'));
  function closeMenus() { menus.forEach(function (m) { m.classList.remove('open'); m.querySelector('.menu-btn').setAttribute('aria-expanded', 'false'); }); }
  menus.forEach(function (m) {
    var b = m.querySelector('.menu-btn');
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = m.classList.contains('open');
      closeMenus();
      if (!open) { m.classList.add('open'); b.setAttribute('aria-expanded', 'true'); }
    });
    m.addEventListener('mouseenter', function () {
      if (menus.some(function (x) { return x.classList.contains('open'); })) { closeMenus(); m.classList.add('open'); b.setAttribute('aria-expanded', 'true'); }
    });
  });
  document.addEventListener('click', closeMenus);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenus(); });

  /* ---------- actions ---------- */
  function setPlaying(p) {
    playing = p;
    var ic = btnPlay.querySelector('span');
    ic.className = p ? 'ic-pause' : 'ic-play';
    btnPlay.setAttribute('aria-label', p ? 'Pause' : 'Play');
    if (p) loop();
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-action]');
    if (!t) return;
    var a = t.getAttribute('data-action');
    switch (a) {
      case 'playpause': setPlaying(!playing); break;
      case 'stop': setPlaying(false); show('now-playing'); break;
      case 'prev': step(-1); break;
      case 'next': step(1); break;
      case 'mute': wmp.classList.toggle('muted'); document.getElementById('btn-mute').setAttribute('aria-label', wmp.classList.contains('muted') ? 'Unmute' : 'Mute'); break;
      case 'toggle-playlist': wmp.classList.toggle('no-playlist'); resize(); break;
      case 'toggle-taskbar': wmp.classList.toggle('no-taskpane'); resize(); break;
      case 'vis-prev': setVis(visIndex - 1); break;
      case 'vis-next': setVis(visIndex + 1); break;
      case 'close':
        wmp.classList.add('minimized');
        document.querySelector('.titlebar-text').textContent = 'Sobolak Technologies (click to restore)';
        break;
    }
    closeMenus();
  });
  document.querySelector('.tb-close').addEventListener('click', function () {
    wmp.classList.add('minimized');
    document.querySelector('.titlebar-text').textContent = 'Sobolak Technologies (click to restore)';
  });
  document.querySelector('.tb-min').addEventListener('click', function () {
    wmp.classList.toggle('minimized');
  });
  document.querySelector('.tb-max').addEventListener('click', function () {
    wmp.classList.toggle('maximized'); resize();
  });
  document.querySelector('.titlebar').addEventListener('click', function (e) {
    if (e.target.closest('.tb')) return;
    if (wmp.classList.contains('minimized')) {
      wmp.classList.remove('minimized');
      document.querySelector('.titlebar-text').textContent = 'Sobolak Technologies';
      resize();
    }
  });

  /* ---------- skins ---------- */
  var skinBtns = Array.prototype.slice.call(document.querySelectorAll('.skin'));
  function setSkin(name) {
    document.body.setAttribute('data-skin', name);
    skinBtns.forEach(function (b) { b.classList.toggle('active', b.getAttribute('data-skin') === name); });
    save('sobolak-skin', name);
  }
  skinBtns.forEach(function (b) { b.addEventListener('click', function () { setSkin(b.getAttribute('data-skin')); }); });
  setSkin(load('sobolak-skin') || 'luna');

  /* ---------- clock ---------- */
  var t0 = Date.now();
  setInterval(function () {
    var s = Math.floor((Date.now() - t0) / 1000);
    var m = Math.floor(s / 60); s = s % 60;
    stTime.textContent = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
  }, 1000);

  /* ---------- visualizer ---------- */
  var canvas = document.getElementById('vis');
  var ctx = canvas.getContext('2d');
  var W = 0, H = 0, dpr = 1;
  var visNames = ['Water', 'Swirl', 'Bars', 'Orbit'];
  var visIndex = 0;
  var visNameEl = document.getElementById('vis-name');
  function setVis(i) { visIndex = (i + visNames.length) % visNames.length; visNameEl.textContent = visNames[visIndex]; save('sobolak-vis', visIndex); }
  setVis(parseInt(load('sobolak-vis') || '0', 10) || 0);

  function resize() {
    var r = canvas.parentNode.getBoundingClientRect();
    if (!r.width) return;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = Math.floor(r.width); H = Math.floor(r.height);
    canvas.width = W * dpr; canvas.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  window.addEventListener('resize', resize);

  var t = 0, raf = 0;
  function draw() {
    if (!W || !H) return;
    var cx = W / 2, cy = H * 0.5, R = Math.min(W, H) * 0.42;
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, W, H);
    var k = visIndex;
    if (k === 0) { // Water: layered ripples with a bright core
      var g = ctx.createRadialGradient(cx, cy, 0, cx, cy, R * 1.4);
      g.addColorStop(0, 'rgba(190,210,255,0.95)'); g.addColorStop(0.25, 'rgba(70,90,230,0.7)'); g.addColorStop(0.6, 'rgba(20,20,120,0.45)'); g.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      ctx.lineWidth = 1.2;
      for (var i = 0; i < 9; i++) {
        var ph = (t * 0.6 + i * 0.7) % 6.283;
        var rr = R * (0.15 + i * 0.11) + Math.sin(ph) * 6;
        ctx.beginPath();
        for (var a = 0; a <= 6.3; a += 0.05) {
          var wob = Math.sin(a * 7 + t * 2 + i) * 4 + Math.sin(a * 13 - t * 1.3) * 3;
          var x = cx + Math.cos(a) * (rr + wob) * 1.35, y = cy + Math.sin(a) * (rr + wob) * 0.75;
          if (a === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.strokeStyle = 'rgba(' + (150 + i * 10) + ',' + (170 + i * 8) + ',255,' + (0.55 - i * 0.05) + ')';
        ctx.stroke();
      }
      // horizontal light smear
      var g2 = ctx.createLinearGradient(0, cy, W, cy);
      g2.addColorStop(0, 'rgba(255,255,255,0)'); g2.addColorStop(0.5, 'rgba(255,255,255,0.35)'); g2.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = g2; ctx.fillRect(0, cy - 2 + Math.sin(t) * 2, W, 3);
    } else if (k === 1) { // Swirl: rotating arms
      ctx.save(); ctx.translate(cx, cy);
      for (var j = 0; j < 60; j++) {
        var ang = j * 0.35 + t * 0.8, rad = (j / 60) * R * 1.3;
        var x2 = Math.cos(ang) * rad * 1.3, y2 = Math.sin(ang) * rad * 0.8;
        var s = 2 + (j / 60) * 9;
        ctx.fillStyle = 'rgba(' + (120 + j * 2) + ',' + (160 + j) + ',255,' + (0.9 - j / 70) + ')';
        ctx.beginPath(); ctx.arc(x2, y2, s, 0, 6.283); ctx.fill();
      }
      ctx.restore();
    } else if (k === 2) { // Bars: WMP spectrum bars, fake signal
      var n = 48, bw = W / n;
      for (var b = 0; b < n; b++) {
        var v = Math.abs(Math.sin(b * 0.37 + t * 3) * 0.5 + Math.sin(b * 0.11 - t * 1.7) * 0.5);
        var h = v * H * 0.75 + 4;
        var gg = ctx.createLinearGradient(0, H - h, 0, H);
        gg.addColorStop(0, '#dff3ff'); gg.addColorStop(0.3, '#4fa0ff'); gg.addColorStop(1, '#0b2a8a');
        ctx.fillStyle = gg;
        ctx.fillRect(b * bw + 1, H - h, bw - 2, h);
      }
    } else { // Orbit: the logo ring, as particles
      ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.45);
      for (var p = 0; p < 140; p++) {
        var aa = p / 140 * 6.283 + t * 0.5;
        var ex = Math.cos(aa) * R * 1.35, ey = Math.sin(aa) * R * 0.42;
        var depth = (Math.sin(aa) + 1) / 2;
        ctx.fillStyle = 'rgba(' + Math.floor(170 + depth * 50) + ',' + Math.floor(220 + depth * 30) + ',' + Math.floor(90 + depth * 60) + ',' + (0.35 + depth * 0.65) + ')';
        ctx.beginPath(); ctx.arc(ex, ey, 1.5 + depth * 3, 0, 6.283); ctx.fill();
      }
      ctx.restore();
    }
  }
  function loop() {
    cancelAnimationFrame(raf);
    if (!playing) return;
    t += 0.016;
    draw();
    raf = requestAnimationFrame(loop);
  }
  document.addEventListener('visibilitychange', function () { if (!document.hidden && playing) loop(); });

  /* ---------- boot ---------- */
  show(location.hash.slice(1) || 'now-playing', false);
  resize();
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) { playing = false; draw(); setPlaying(false); }
  else loop();
})();
