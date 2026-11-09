// Renders the sliced graphics for the site. Run: node tools/make_images.js
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const OUT = path.join(__dirname, '..', 'images');
fs.mkdirSync(OUT, { recursive: true });
const FONT = `font-family: 'DejaVu Sans', Verdana, Tahoma, sans-serif;`;

async function shot(page, html, w, h, file, transparent) {
  await page.setViewportSize({ width: w, height: h });
  await page.setContent(`<html><body style="margin:0;${transparent ? 'background:transparent' : ''}">${html}</body></html>`);
  await page.screenshot({ path: path.join(OUT, file), omitBackground: !!transparent, clip: { x: 0, y: 0, width: w, height: h } });
}

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: 1 });

  // --- title bar slice (1px wide), menubar slice, pane slice, transport slice
  await shot(p, `<div style="width:4px;height:30px;background:linear-gradient(180deg,#3b8bff 0%,#0a5fe8 12%,#0a5fe8 60%,#0046d5 100%)"></div>`, 4, 30, 'titlebar_bg.png');
  await shot(p, `<div style="width:4px;height:22px;background:linear-gradient(180deg,#eef3fe,#d5e0f6)"></div>`, 4, 22, 'menubar_bg.png');
  await shot(p, `<div style="width:4px;height:60px;background:linear-gradient(180deg,#cfd9ee 0%,#9fb3dc 55%,#7d95c9 100%);border-top:1px solid #fff"></div>`, 4, 60, 'transport_bg.png');
  await shot(p, `<div style="width:4px;height:400px;background:linear-gradient(180deg,#5d86d6,#2a52a8)"></div>`, 4, 400, 'frame_bg.png');

  // --- title bar buttons
  const tb = (bg, inner) => `<div style="width:21px;height:21px;border-radius:3px;border:1px solid #fff;box-sizing:border-box;background:${bg};position:relative;box-shadow:inset 0 0 0 1px rgba(0,0,0,.25)">${inner}</div>`;
  const blue = 'linear-gradient(180deg,#5f9bff 0%,#2f6fe8 45%,#1757d6 55%,#4b86f5 100%)';
  await shot(p, tb(blue, `<div style="position:absolute;left:5px;top:13px;width:8px;height:3px;background:#fff"></div>`), 21, 21, 'tb_min.png', true);
  await shot(p, tb(blue, `<div style="position:absolute;left:5px;top:5px;width:9px;height:8px;border:2px solid #fff;border-top-width:3px;box-sizing:border-box"></div>`), 21, 21, 'tb_max.png', true);
  await shot(p, tb('linear-gradient(180deg,#e7786a 0%,#d8452f 45%,#b9301f 55%,#c33a2a 100%)', `<div style="position:absolute;left:4px;top:8px;width:11px;height:3px;background:#fff;transform:rotate(45deg)"></div><div style="position:absolute;left:4px;top:8px;width:11px;height:3px;background:#fff;transform:rotate(-45deg)"></div>`), 21, 21, 'tb_close.png', true);

  // --- nav buttons (text baked in), 3 states
  const nav = [['nowplaying','Now<br>Playing'],['guide','Media<br>Guide'],['copycd','Copy<br>from CD'],['library','Media<br>Library'],['radio','Radio<br>Tuner'],['device','Copy to CD<br>or Device'],['skins','Skin<br>Chooser']];
  const states = {
    off: ['linear-gradient(180deg,#4a74cc,#2e55ad)', '#fff', '#7ea0e3'],
    over: ['linear-gradient(180deg,#5f8ae0,#3a63bb)', '#ffcc44', '#9db9ee'],
    on: ['linear-gradient(180deg,#ffffff,#e3ebfb)', '#0b2a6f', '#ffffff'],
  };
  for (const [id, label] of nav) for (const [st, [bg, col, line]] of Object.entries(states)) {
    await shot(p, `<div style="width:110px;height:36px;box-sizing:border-box;background:${bg};border:1px solid ${line};border-left:0;border-right-color:#1d3f8a;border-radius:0 4px 4px 0;box-shadow:inset 0 1px 0 rgba(255,255,255,.25);color:${col};${FONT}font-size:11px;font-weight:bold;line-height:1.15;padding:5px 6px 0 8px">${label}</div>`, 110, 36, `nav_${id}_${st}.png`, true);
  }

  // --- transport buttons
  const rnd = (size, inner, over) => `<div style="width:${size}px;height:${size}px;border-radius:50%;box-sizing:border-box;border:1px solid #fff;background:radial-gradient(circle at 40% 30%,${over ? '#ffffff,#d6e2ff 70%' : '#f7f9ff,#b8c7e8 70%'});box-shadow:0 0 0 2px #2f5fc8,0 2px 3px rgba(0,0,0,.35),inset 0 -2px 3px rgba(0,0,0,.15);position:relative;margin:4px">${inner}</div>`;
  const c = (w, h, extra) => `<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:${w}px;height:${h}px;${extra}"></div>`;
  const ic = '#1a2e66';
  const icons = {
    play: [46, c(0, 0, `border-left:14px solid ${ic};border-top:8px solid transparent;border-bottom:8px solid transparent;margin-left:2px`)],
    pause: [46, c(12, 14, `border-left:4px solid ${ic};border-right:4px solid ${ic};box-sizing:border-box`)],
    stop: [24, c(8, 8, `background:${ic}`)],
    prev: [20, c(0, 0, `border-top:4px solid transparent;border-bottom:4px solid transparent;border-right:6px solid ${ic};box-shadow:-3px 0 0 -1px ${ic}`)],
    next: [20, c(0, 0, `border-top:4px solid transparent;border-bottom:4px solid transparent;border-left:6px solid ${ic};box-shadow:3px 0 0 -1px ${ic}`)],
    mute: [20, c(5, 6, `background:${ic};border-radius:1px 0 0 1px;margin-left:-3px`) + c(0, 0, `border-top:5px solid transparent;border-bottom:5px solid transparent;border-right:5px solid ${ic};margin-left:3px`)],
  };
  for (const [name, [size, inner]] of Object.entries(icons)) {
    await shot(p, rnd(size, inner, false), size + 8, size + 8, `tr_${name}.png`, true);
    await shot(p, rnd(size, inner, true), size + 8, size + 8, `tr_${name}_over.png`, true);
  }
  await shot(p, `<div style="width:4px;height:6px;background:linear-gradient(180deg,#5f6f93,#8e9dbf 60%,#a9b7d6)"></div>`, 4, 6, 'seek_bg.png');
  await shot(p, `<div style="width:4px;height:6px;background:linear-gradient(180deg,#7fb4ff,#2a6cff)"></div>`, 4, 6, 'seek_fill.png');
  await shot(p, `<div style="width:14px;height:14px;border-radius:50%;background:radial-gradient(circle at 40% 30%,#fff,#c6d2ec 75%);border:1px solid #5e74a8;box-sizing:border-box;box-shadow:0 1px 2px rgba(0,0,0,.4);margin:1px"></div>`, 16, 16, 'seek_knob.png', true);
  // small round viewer buttons
  for (const [name, glyph] of [['vt_prev','&lsaquo;'],['vt_next','&rsaquo;'],['vt_list','&equiv;']]) {
    await shot(p, `<div style="width:18px;height:18px;border-radius:50%;box-sizing:border-box;border:1px solid #8ea4d8;color:#cfdcff;background:radial-gradient(circle at 40% 35%,#6f8fd8,#233f86 70%,#15285d);${FONT}font-size:13px;line-height:15px;text-align:center">${glyph}</div>`, 18, 18, `${name}.png`, true);
  }
  // playlist dropdown header
  await shot(p, `<div style="width:188px;height:20px;box-sizing:border-box;background:#fff;border:1px solid #7f9db9;${FONT}font-size:11px;line-height:18px;padding-left:4px;color:#000;position:relative">Roadmap<div style="position:absolute;right:1px;top:1px;width:15px;height:16px;background:linear-gradient(180deg,#c5d5fc,#5d85e0 60%,#3b63c7);border:1px solid #fff;border-radius:2px;color:#fff;font-size:9px;text-align:center;line-height:14px;box-sizing:border-box">&#9662;</div></div>`, 188, 20, 'pl_header.png');
  // bullets, spacer
  await shot(p, `<div style="width:5px;height:5px;border-radius:50%;background:#4fe04f;margin:2px"></div>`, 9, 9, 'bullet_green.png', true);
  await shot(p, `<div style="width:0;height:0;border-top:4px solid transparent;border-bottom:4px solid transparent;border-left:6px solid #39e639;margin:1px 2px"></div>`, 10, 10, 'play_green.png', true);
  await shot(p, `<div style="width:1px;height:1px"></div>`, 1, 1, 'spacer.png', true);
  // the sticker
  await shot(p, `<div style="display:inline-block;background:linear-gradient(90deg,#ff9f1a,#ff4f2b 50%,#ffd01a);color:#000;font-weight:bold;${FONT}font-size:10px;line-height:1.15;padding:3px 8px 2px;letter-spacing:.02em;box-shadow:0 0 0 1px #000,0 0 0 2px #ffd01a;margin:3px">SOBOLAK<br><span style="letter-spacing:.1em;color:#1a0a00">LOOK INTO THE E-WASTE</span></div>`, 212, 34, 'sticker.png', true);
  // company logo in task pane
  const icon = fs.readFileSync(path.join(__dirname, '..', 'assets', 'icon.svg'), 'utf8').replace(/width="\d+" height="\d+"/, 'width="34" height="34"');
  await shot(p, `<div style="width:100px;text-align:center;color:#fff;${FONT}font-size:10px;font-weight:bold;line-height:1.15;padding-top:2px">${icon}<br>Sobolak<br>Technologies</div>`, 100, 62, 'pane_logo.png', true);

  // --- visualizer frames (logo baked in)
  const logo = fs.readFileSync(path.join(__dirname, '..', 'assets', 'logo.svg'), 'utf8').replace(/width="\d+" height="\d+"/, 'width="300"');
  const W = 420, H = 230;
  fs.mkdirSync(path.join(OUT, 'frames'), { recursive: true });
  await p.setViewportSize({ width: W, height: H });
  await p.setContent(`<html><body style="margin:0;background:#000"><canvas id="c" width="${W}" height="${H}" style="position:absolute;left:0;top:0"></canvas><div style="position:absolute;left:0;top:8px;width:${W}px;text-align:center">${logo}</div></body></html>`);
  for (let f = 0; f < 24; f++) {
    await p.evaluate(([f, W, H]) => {
      const ctx = document.getElementById('c').getContext('2d');
      const t = f / 24 * Math.PI * 2; const cx = W / 2, cy = H * 0.56, R = Math.min(W, H) * 0.42;
      ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, R * 1.4);
      g.addColorStop(0, 'rgba(190,210,255,0.95)'); g.addColorStop(0.25, 'rgba(70,90,230,0.7)'); g.addColorStop(0.6, 'rgba(20,20,120,0.45)'); g.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      ctx.lineWidth = 1.2;
      for (let i = 0; i < 9; i++) {
        const rr = R * (0.15 + i * 0.11) + Math.sin(t + i * 0.7) * 6;
        ctx.beginPath();
        for (let a = 0; a <= 6.3; a += 0.05) {
          const wob = Math.sin(a * 7 + t * 2 + i) * 4 + Math.sin(a * 13 - t) * 3;
          const x = cx + Math.cos(a) * (rr + wob) * 1.35, y = cy + Math.sin(a) * (rr + wob) * 0.75;
          a === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.closePath(); ctx.strokeStyle = `rgba(${150 + i * 10},${170 + i * 8},255,${0.55 - i * 0.05})`; ctx.stroke();
      }
      const g2 = ctx.createLinearGradient(0, cy, W, cy); g2.addColorStop(0, 'rgba(255,255,255,0)'); g2.addColorStop(0.5, 'rgba(255,255,255,0.35)'); g2.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = g2; ctx.fillRect(0, cy - 2 + Math.sin(t) * 2, W, 3);
    }, [f, W, H]);
    await p.screenshot({ path: path.join(OUT, 'frames', `f${String(f).padStart(2, '0')}.png`), clip: { x: 0, y: 0, width: W, height: H } });
  }
  await b.close();
  console.log('images rendered');
})();
