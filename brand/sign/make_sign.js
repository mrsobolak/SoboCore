// Builds the booth sign in every size. Run: node brand/sign/make_sign.js
// Change SLOGAN / TAGLINE below and run it again to reprint with new wording.
const { chromium } = require('playwright');
const fs = require('fs');
const os = require('os');
const path = require('path');

const SLOGAN = 'Refurbished laptops, desktops &amp; more';
const TAGLINE = 'Tested by hand. Cheaper than eBay.';
const WEB = 'sobolak.org';

const ROOT = path.resolve(__dirname, '..', '..');
const OUT = __dirname;

// name, width and height in inches, theme
const SIZES = [
  ['sobolak-sign-banner-5x3ft-60x36in', 60, 36, 'dark'],
  ['sobolak-sign-banner-3x1.6ft-36x19.2in', 36, 19.2, 'dark'],
  ['sobolak-sign-banner-48x24in', 48, 24, 'dark'],
  ['sobolak-sign-poster-36x24in', 36, 24, 'dark'],
  ['sobolak-sign-letter-11x8.5in', 11, 8.5, 'light'],
];

function page(w, h, theme) {
  const logoFile = theme === 'dark' ? 'sobolak-logo-dark-transparent.svg' : 'sobolak-logo-light-transparent.svg';
  const logo = fs.readFileSync(path.join(ROOT, 'brand/logo/final', logoFile), 'utf8')
    .replace(/<svg([^>]*?)\swidth="[^"]*"\sheight="[^"]*"/, '<svg$1');
  const font = (f) => 'file://' + path.join(ROOT, 'assets/fonts', f);
  const wide = w / h > 1.7;
  return `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: Michroma; src: url("${font('michroma.woff2')}") format("woff2"); }
@font-face { font-family: "Source Sans 3"; src: url("${font('source-sans-3.woff2')}") format("woff2"); font-weight: 200 900; }
@page { size: ${w}in ${h}in; margin: 0; }
* { box-sizing: border-box; margin: 0; }
html, body { width: ${w}in; height: ${h}in; }
body { --h: ${h}in; --w: ${w}in; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.sign {
  width: var(--w); height: var(--h);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  overflow: hidden; position: relative;
}
.dark .sign { background: radial-gradient(70% 85% at 50% 40%, #1b4687 0%, #10264a 45%, #0d1620 100%); color: #fff; }
.light .sign { background: #fff; color: #0d1620; }
.bar { position: absolute; left: 0; right: 0; height: calc(var(--h) * .022); }
.bar.top { top: 0; } .bar.bottom { bottom: 0; }
.dark .bar { background: linear-gradient(90deg, #3a7a0c, #a8e61d 30%, #e4ff9a 50%, #a8e61d 70%, #3a7a0c); }
.light .bar { background: linear-gradient(90deg, #3a7a0c, #7fc41a 30%, #a8e61d 50%, #7fc41a 70%, #3a7a0c); }
.logo { width: ${wide ? 76 : 88}%; line-height: 0; }
.logo svg { width: 100%; height: auto; display: block; }
.fit { white-space: nowrap; }
.slogan {
  margin-top: calc(var(--h) * ${wide ? .03 : .05});
  font-family: Michroma, sans-serif; text-transform: uppercase; letter-spacing: .1em;
  font-size: 40px;
}
.dark .slogan { color: #b8f02f; }
.light .slogan { color: #2f6b08; }
.rule {
  width: 46%; height: calc(var(--h) * .006); margin: calc(var(--h) * .04) 0 calc(var(--h) * .035);
  border-radius: 99in;
}
.dark .rule { background: linear-gradient(90deg, rgba(255,255,255,0), #dfe5ec 30%, #ffffff 50%, #dfe5ec 70%, rgba(255,255,255,0)); }
.light .rule { background: linear-gradient(90deg, rgba(13,22,32,0), #8f9aa7 30%, #55627a 50%, #8f9aa7 70%, rgba(13,22,32,0)); }
.tag { font-family: "Source Sans 3", sans-serif; font-weight: 600; font-size: 40px; }
.web {
  position: absolute; bottom: calc(var(--h) * .06); left: 0; right: 0; text-align: center;
  font-family: Michroma, sans-serif; letter-spacing: .08em; font-size: calc(var(--h) * .034);
}
.dark .web { color: #cfd9e6; }
.light .web { color: #55627a; }
</style></head><body class="${theme}">
<div class="sign">
  <div class="bar top"></div>
  <div class="logo">${logo}</div>
  <div class="slogan fit" data-fit="${wide ? .74 : .86}">${SLOGAN}</div>
  <div class="rule"></div>
  <div class="tag fit" data-fit="${wide ? .46 : .6}">${TAGLINE}</div>
  <div class="web">${WEB}</div>
  <div class="bar bottom"></div>
</div>
<script>
// scale each line so it fills its share of the sign width
document.fonts.ready.then(function () {
  var W = document.querySelector('.sign').getBoundingClientRect().width;
  document.querySelectorAll('.fit').forEach(function (el) {
    var target = W * parseFloat(el.dataset.fit);
    var size = parseFloat(getComputedStyle(el).fontSize);
    el.style.fontSize = (size * target / el.getBoundingClientRect().width) + 'px';
  });
  document.body.dataset.ready = '1';
});
</script></body></html>`;
}

(async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'sobolak-sign-'));
  const browser = await chromium.launch();
  for (const [name, w, h, theme] of SIZES) {
    const file = path.join(tmp, name + '.html');
    fs.writeFileSync(file, page(w, h, theme));
    const ctx = await browser.newContext({
      viewport: { width: Math.round(w * 96), height: Math.round(h * 96) },
    });
    const p = await ctx.newPage();
    await p.goto('file://' + file);
    await p.waitForFunction(() => document.body.dataset.ready === '1');
    await p.pdf({ path: path.join(OUT, name + '.pdf'), width: w + 'in', height: h + 'in', printBackground: true, pageRanges: '1' });
    await ctx.close();
    console.log('built', name);
  }
  await browser.close();
  fs.rmSync(tmp, { recursive: true, force: true });
})();
