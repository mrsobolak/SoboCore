// Builds the letter-size handout. Run: node brand/flyer/make_flyer.js
// Edit the wording in the HTML below and run it again to reprint.
const { chromium } = require('playwright');
const fs = require('fs');
const os = require('os');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const OUT = path.join(__dirname, 'sobolak-flyer-letter.pdf');

const EMAIL = 'sobosobolak@gmail.com';
const WEB = 'sobolak.org';

const logo = fs.readFileSync(path.join(ROOT, 'brand/logo/final/sobolak-logo-light-transparent.svg'), 'utf8')
  .replace(/<svg([^>]*?)\swidth="[^"]*"\sheight="[^"]*"/, '<svg$1');
const qr = fs.readFileSync(path.join(__dirname, 'qr-sobolak-org.svg'), 'utf8');
// the laptop and desktop drawings come straight from the website
const sprite = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8').match(/<svg class="sprite"[\s\S]*?<\/symbol>\s*<\/svg>/)[0];
const font = (f) => 'file://' + path.join(ROOT, 'assets/fonts', f);

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Sobolak Technologies</title><style>
@font-face { font-family: Michroma; src: url("${font('michroma.woff2')}") format("woff2"); }
@font-face { font-family: "Source Sans 3"; src: url("${font('source-sans-3.woff2')}") format("woff2"); font-weight: 200 900; }
@page { size: 8.5in 11in; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 8.5in; height: 11in; }
body {
  font: 400 10.6pt/1.42 "Source Sans 3", sans-serif; color: #142033; background: #fff;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
.sprite { position: absolute; width: 0; height: 0; overflow: hidden; }
.page { width: 8.5in; height: 11in; padding: .45in .55in .4in; display: flex; flex-direction: column; }
.bar { flex: none; height: .09in; border-radius: 1in; background: linear-gradient(90deg, #3a7a0c, #7fc41a 30%, #a8e61d 50%, #7fc41a 70%, #3a7a0c); }

.head { text-align: center; padding-top: .1in; }
.logo { width: 4.3in; margin: 0 auto; line-height: 0; }
.logo svg { width: 100%; height: auto; display: block; }
.slogan { margin-top: .02in; font: 400 10.4pt/1.2 Michroma, sans-serif; letter-spacing: .1em; text-transform: uppercase; color: #2f6b08; }

h1 { margin-top: .15in; text-align: center; font: 400 19pt/1.2 Michroma, sans-serif; letter-spacing: -.01em; color: #0d1b30; }
h1 span { color: #2f6b08; }
.lede { margin-top: .06in; text-align: center; font-size: 11pt; color: #3d4a61; white-space: nowrap; }

h2 { font: 400 11.4pt/1.2 Michroma, sans-serif; color: #0d1b30; margin-bottom: .08in; }
section { margin-top: .18in; }

.sell { display: grid; grid-template-columns: 1fr 1fr; gap: .16in; }
.card { display: grid; grid-template-columns: 1.5in 1fr; align-items: center; border: 1px solid #c3cddb; border-radius: .12in; overflow: hidden; }
.card .art { align-self: stretch; display: flex; align-items: center; background: linear-gradient(#cfe3fb, #f3f8ff); padding: .06in; border-right: 1px solid #d5dde8; --shell: #262a32; --deck: #343943; }
.card svg { width: 100%; height: .92in; display: block; }
.card div.txt { padding: .1in .13in; }
.card b { display: block; font-size: 12pt; color: #0a1220; }
.card span { color: #55627a; font-size: 10pt; line-height: 1.35; display: block; }
.also { margin-top: .09in; text-align: center; color: #3d4a61; }
.also b { color: #0a1220; }

.cols { display: grid; grid-template-columns: 1fr 1fr; gap: .3in; }
ul, ol { list-style: none; }
.reasons li { position: relative; padding: 0 0 .075in .2in; }
.reasons li::before { content: ""; position: absolute; left: 0; top: .052in; width: .09in; height: .09in; border-radius: 50%; background: #7fc41a; border: 1px solid #2f6b08; }
.reasons b, .steps b { color: #0a1220; }
.reasons span, .steps span { color: #55627a; }
.steps { counter-reset: s; }
.steps li { counter-increment: s; position: relative; padding: 0 0 .075in .3in; }
.steps li::before {
  content: counter(s); position: absolute; left: 0; top: .01in; width: .2in; height: .2in; border-radius: 50%;
  background: linear-gradient(#b9ea3c, #7cc318); border: 1px solid #2f6b08; color: #0f2e05;
  font: 400 7.5pt/.19in Michroma, sans-serif; text-align: center;
}

.about { border-top: 1px solid #c3cddb; padding-top: .15in; margin-bottom: .16in; }
.about p { color: #3d4a61; }
.about p + p { margin-top: .06in; }
.about b { color: #0a1220; }

.contact {
  margin-top: auto; display: grid; grid-template-columns: 1fr auto; align-items: center; gap: .25in;
  padding: .17in .22in; border-radius: .14in; color: #fff;
  background: linear-gradient(#17294a, #0b1424);
}
.contact h2 { color: #fff; font-size: 14pt; margin-bottom: .04in; }
.contact p { color: #d5deea; }
.contact .mail { margin-top: .05in; font-size: 14.5pt; font-weight: 700; color: #b8f02f; }
.contact .web { font: 400 9.5pt/1.3 Michroma, sans-serif; letter-spacing: .06em; color: #fff; margin-top: .03in; }
.qr { width: 1.02in; text-align: center; }
.qr svg { width: 1.02in; height: 1.02in; display: block; border-radius: .05in; }
.fine { margin-top: .07in; text-align: center; font-size: 7pt; color: #7b8799; }
</style></head><body>
${sprite}
<div class="page">
  <div class="bar"></div>

  <div class="head">
    <div class="logo">${logo}</div>
    <div class="slogan">Refurbished laptops, desktops &amp; more</div>
  </div>

  <h1>Good computers. <span>Cheaper than eBay.</span></h1>
  <p class="lede">Used business computers with years left in them, tested and cleaned by hand in Michigan and sold direct.</p>

  <section>
    <h2>What we sell</h2>
    <div class="sell">
      <div class="card">
        <div class="art"><svg viewBox="12 4 216 140" role="img" aria-label="Laptop"><use href="#art-laptop" width="240" height="150"/></svg></div>
        <div class="txt"><b>Refurbished laptops</b><span>The tough business models that offices retire early. Ready to use the day you get it.</span></div>
      </div>
      <div class="card">
        <div class="art"><svg viewBox="66 6 108 138" role="img" aria-label="Desktop computer"><use href="#art-sff" width="240" height="150"/></svg></div>
        <div class="txt"><b>Refurbished desktops</b><span>Office desktops that still have plenty to give. A lot of computer for the money.</span></div>
      </div>
    </div>
    <p class="also"><b>Also on the bench:</b> laptop repairs, and gaming PCs built to order around your budget.</p>
  </section>

  <section class="cols">
    <div>
      <h2>Why it costs less</h2>
      <ul class="reasons">
        <li><b>No marketplace cut.</b> <span>eBay charges sellers a fee on every sale, and sellers build that into the price. We sell direct, so it comes off yours.</span></li>
        <li><b>No warehouse.</b> <span>2 men and a van. There is not much overhead to pay for.</span></li>
        <li><b>Nothing is scrap until it fails a test.</b> <span>Most retired office computers are fine. If it passes, it gets sold instead of shredded.</span></li>
      </ul>
    </div>
    <div>
      <h2>Before a machine gets sold</h2>
      <ol class="steps">
        <li><b>Tested.</b> <span>Processor, memory, drive, screen, keyboard, ports, battery. If something fails, it gets fixed or it does not get sold.</span></li>
        <li><b>Opened and cleaned.</b> <span>Dust out, case wiped down.</span></li>
        <li><b>Wiped and reinstalled.</b> <span>The last owner's data is erased and Windows goes back on fresh.</span></li>
        <li><b>Graded honestly.</b> <span>You hear about the wear before you pay.</span></li>
      </ol>
    </div>
  </section>

  <section class="about">
    <h2>About us</h2>
    <p><b>2 men and a van. Aka 2 guys.</b> Sobolak Technologies is an independent technology company in Michigan, founded in 2024. No investors and no outside money.</p>
    <p>Every sale goes toward the thing we actually want to make: <b>the Sobolak Laptop</b>, a handheld desktop built from recycled parts on our own motherboard. Coming 2029~.</p>
  </section>

  <div class="contact">
    <div>
      <h2>Want one?</h2>
      <p>Tell us what you need and what you can spend.</p>
      <p class="mail">${EMAIL}</p>
      <p class="web">${WEB}</p>
    </div>
    <div class="qr">${qr}</div>
  </div>
  <p class="fine">eBay is a trademark of eBay Inc. We are not affiliated with eBay.</p>
</div>
<script>document.fonts.ready.then(function () { document.body.dataset.ready = '1'; });</script>
</body></html>`;

(async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'sobolak-flyer-'));
  const file = path.join(tmp, 'flyer.html');
  fs.writeFileSync(file, html);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 816, height: 1056 } });
  await page.goto('file://' + file);
  await page.waitForFunction(() => document.body.dataset.ready === '1');
  const fit = await page.evaluate(() => {
    const p = document.querySelector('.page');
    return { overflow: p.scrollHeight - p.clientHeight, gap: Math.round(document.querySelector('.contact').getBoundingClientRect().top - document.querySelector('.about').getBoundingClientRect().bottom) };
  });
  console.log('page overflow px:', fit.overflow, '| space above contact box px:', fit.gap);
  await page.pdf({ path: OUT, width: '8.5in', height: '11in', printBackground: true });
  await browser.close();
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log('built', path.basename(OUT));
})();
