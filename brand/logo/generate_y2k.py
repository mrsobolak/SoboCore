import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import text_path, text_width, svg_doc as _svg, arrow_s
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out2')
os.makedirs(OUT, exist_ok=True)

MICH = 'Michroma.ttf'          # Eurostile-extended feel (VAIO / FÖTUS / Skechers)
AUDIO = 'Audiowide.ttf'        # Toonami / Walkman-ish
COMF = 'Comfortaawght700.ttf'  # blobby rounded (PSone)
EXOI = 'Exo2italwght1900.ttf'  # heavy italic (racing sticker)
SYNC = 'Syncopatewght700.ttf'  # wide caps

DEFS = '''
  <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff"/>
    <stop offset=".42" stop-color="#cfd6de"/>
    <stop offset=".5" stop-color="#6b7684"/>
    <stop offset=".52" stop-color="#9aa5b2"/>
    <stop offset=".8" stop-color="#e6ebf0"/>
    <stop offset="1" stop-color="#8f9aa7"/>
  </linearGradient>
  <linearGradient id="limeChrome" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f4ffd0"/>
    <stop offset=".45" stop-color="#b9ee3c"/>
    <stop offset=".5" stop-color="#4c8f0e"/>
    <stop offset=".53" stop-color="#8ccc22"/>
    <stop offset="1" stop-color="#e2ff9a"/>
  </linearGradient>
  <linearGradient id="limeFlat" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#d9ff6a"/>
    <stop offset="1" stop-color="#7fc41a"/>
  </linearGradient>
  <linearGradient id="steelDark" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#5c6670"/>
    <stop offset=".5" stop-color="#1e252c"/>
    <stop offset="1" stop-color="#3a434c"/>
  </linearGradient>
  <linearGradient id="navy" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1f3f7a"/>
    <stop offset="1" stop-color="#0b1b3c"/>
  </linearGradient>
  <linearGradient id="silverBar" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f7f9fb"/>
    <stop offset="1" stop-color="#b7c0ca"/>
  </linearGradient>
  <radialGradient id="limeOrb" cx="35%" cy="30%" r="75%">
    <stop offset="0" stop-color="#f3ffc4"/>
    <stop offset=".4" stop-color="#b6ec33"/>
    <stop offset="1" stop-color="#3d7d0a"/>
  </radialGradient>
  <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#ffffff"/>
    <stop offset=".5" stop-color="#b9ee3c"/>
    <stop offset="1" stop-color="#3d7d0a"/>
  </linearGradient>
  <linearGradient id="glossTop" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".85"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
'''

def svg_doc(w, h, body, bg=None):
    doc = _svg(w, h, body, bg)
    return doc.replace('<defs>', '<defs>' + DEFS, 1)

def write(name, doc):
    p = os.path.join(OUT, name)
    open(p, 'w').write(doc); print('wrote', name)

def outlined(d, fill, strokes):
    """paint a path with stacked outlines: strokes = [(color, width), ...] outermost first"""
    out = ''
    for col, w in strokes:
        out += f'<path d="{d}" fill="{col}" stroke="{col}" stroke-width="{w}" stroke-linejoin="round"/>\n'
    out += f'<path d="{d}" fill="{fill}"/>'
    return out

# ----------------------------------------------------------------- Y2K-1: chrome extended wordmark + orbit ring
def y2k_wordmark(dark=False):
    size = 150
    d1, w1 = text_path('SOBOLAK', MICH, size, 0, 0, tracking=size*0.02)
    sub = size*0.22
    d2, w2 = text_path('TECHNOLOGIES', MICH, sub, 0, 0, tracking=sub*0.55)
    W, H = w1 + 160, size + 200
    ox, oy = 80, 95 + size*0.75
    # orbit ring swoops behind the wordmark, through the first O (Kazaa-style)
    o_x = ox + text_width('S', MICH, size, tracking=size*0.02) + text_width('O', MICH, size)/2
    o_y = oy - size*0.38
    ring = f'''<g transform="translate({o_x:.1f},{o_y:.1f}) rotate(-28)">
      <ellipse rx="{size*1.05:.1f}" ry="{size*0.36:.1f}" fill="none" stroke="url(#ring)" stroke-width="{size*0.085:.1f}"/>
      <ellipse rx="{size*1.05:.1f}" ry="{size*0.36:.1f}" fill="none" stroke="#1d3f05" stroke-opacity=".7" stroke-width="{size*0.085+6:.1f}" style="mix-blend-mode:multiply" transform="translate(0,2)" opacity="0"/>
    </g>'''
    # ring front half (drawn over text): clip to lower half of ellipse
    ring_front = f'''<g transform="translate({o_x:.1f},{o_y:.1f}) rotate(-28)">
      <path d="M{-size*1.05:.1f},0 A{size*1.05:.1f},{size*0.36:.1f} 0 0 0 {size*1.05:.1f},0" fill="none" stroke="url(#ring)" stroke-width="{size*0.085:.1f}"/>
    </g>'''
    fill = 'url(#chrome)'
    text_strokes = [('#0b1b3c' if not dark else '#000', size*0.09), ('#ffffff' if not dark else '#dfe6ee', size*0.045)]
    body = f'''{ring}
  <g transform="translate({ox},{oy})">
    {outlined(d1, fill, text_strokes)}
  </g>
  {ring_front}
  <g transform="translate({ox + (w1-w2)/2:.1f},{oy + sub*1.9:.1f})">
    <path d="{d2}" fill="{'#0b1b3c' if not dark else '#d9ff6a'}"/>
  </g>'''
  
    return svg_doc(int(W), int(H), body, '#0d1620' if dark else None)

# ----------------------------------------------------------------- Y2K-2: racing sticker badge
def sticker(dark_bg=None):
    size = 118
    d1, w1 = text_path('SOBOLAK', EXOI, size, 0, 0, tracking=size*0.015)
    sub = size*0.27
    d2, w2 = text_path('TECHNOLOGIES', SYNC, sub, 0, 0, tracking=sub*0.22)
    pad = 54
    emblem_w = 150
    W = pad + emblem_w + 40 + w1 + pad + 40
    H = 270
    body = ''
    # badge: rounded, skewed rectangle, 3 outlines like Ventura/Flux stickers
    skew = 10
    bx, by, bw, bh = 20, 24, W - 40, 200
    r = 46
    rect = lambda inset, fill, stroke, sw: f'<rect x="{bx+inset}" y="{by+inset}" width="{bw-2*inset}" height="{bh-2*inset}" rx="{max(r-inset,8)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    badge = f'''<g transform="translate({W/2},{by+bh/2}) skewX(-{skew}) translate({-W/2},{-(by+bh/2)})">
    {rect(0, '#0b1b3c', '#0b1b3c', 0)}
    {rect(7, 'url(#silverBar)', 'none', 0)}
    {rect(16, 'url(#limeFlat)', '#0b1b3c', 4)}
    <rect x="{bx+16}" y="{by+16}" width="{bw-32}" height="{bh*0.42}" rx="{r-16}" fill="url(#glossTop)" opacity=".55"/>
    <rect x="{bx+16}" y="{by+bh-16-58}" width="{bw-32}" height="58" fill="#0b1b3c"/>
    <path d="M{bx+16},{by+bh-16-58} h{bw-32}" stroke="#fff" stroke-width="3"/>
    <rect x="{bx+16}" y="{by+bh-16-58}" width="{bw-32}" height="58" rx="0" fill="none"/>
  </g>'''
    body += badge
    # emblem: recycle-S in a chrome disc
    ex, ey = pad + emblem_w/2 + 6, by + 70
    body += f'''<g>
    <circle cx="{ex}" cy="{ey}" r="52" fill="#0b1b3c"/>
    <circle cx="{ex}" cy="{ey}" r="46" fill="url(#chrome)"/>
    <circle cx="{ex}" cy="{ey}" r="38" fill="url(#navy)"/>
    {arrow_s(scale=0.36, cx=ex, cy=ey, fill='#d9ff6a', sw=19, head=26, halfw=20)}
  </g>'''
    # name
    tx = pad + emblem_w + 30
    ty = by + 70 + size*0.33
    body += f'''<g transform="translate({tx},{ty})">
    {outlined(d1, '#ffffff', [('#0b1b3c', size*0.11)])}
  </g>'''
    # sub on the bar (bar is skewed; place text unskewed for legibility)
    body += f'''<g transform="translate({(W - w2)/2 + 8:.1f},{by+bh-16-58+40})">
    <path d="{d2}" fill="#d9ff6a"/>
  </g>'''
    return svg_doc(int(W), int(H), body, dark_bg)

# ----------------------------------------------------------------- Y2K-3: blob mark (PSone / Walkman) + rounded lowercase
def blob(dark=False):
    """Thick rounded chasing-arrows S as a single black (or lime) glyph."""
    fill = '#111' if not dark else '#d9ff6a'
    size = 128
    d1, w1 = text_path('sobolak', COMF, size, 0, 0, tracking=-size*0.02)
    sub = size*0.26
    d2, w2 = text_path('technologies', COMF, sub, 0, 0, tracking=sub*0.12)
    R = 92
    W = 2*R + 60 + w1 + 90
    H = 2*R + 80
    cx, cy = 40 + R, H/2
    mark = arrow_s(scale=R/120*1.05, cx=cx, cy=cy, fill=fill, sw=30, r=36, gap_deg=34, head=30, halfw=27)
    # round the stroke caps by re-emitting with linecap round: patch the generated group
    mark = mark.replace('stroke-width="30"', 'stroke-width="30" stroke-linecap="round"').replace(f'fill="{fill}">', f'fill="{fill}" stroke="{fill}" stroke-width="6" stroke-linejoin="round">')
    tx = 40 + 2*R + 50
    ty = cy + size*0.22
    body = f'''{mark}
  <g transform="translate({tx},{ty})"><path d="{d1}" fill="{fill}"/></g>
  <g transform="translate({tx + 6},{ty + sub*1.5:.1f})"><path d="{d2}" fill="{fill}" opacity=".75"/></g>'''
    return svg_doc(int(W), int(H), body, '#0d1620' if dark else None)

def blob_mark(dark=False):
    fill = '#111' if not dark else '#d9ff6a'
    R = 120
    mark = arrow_s(scale=R/120*1.05, cx=R+20, cy=R+20, fill=fill, sw=30, r=36, gap_deg=34, head=30, halfw=27)
    mark = mark.replace('stroke-width="30"', 'stroke-width="30" stroke-linecap="round"').replace(f'fill="{fill}">', f'fill="{fill}" stroke="{fill}" stroke-width="6" stroke-linejoin="round">')
    return svg_doc(2*R+40, 2*R+40, mark, '#0d1620' if dark else None)

# ----------------------------------------------------------------- Y2K-4: Xbox-style lime chrome mark + outlined extended type
def lime_x(dark=True):
    size = 126
    d1, w1 = text_path('SOBOLAK', MICH, size, 0, 0, tracking=size*0.03)
    R = 112
    W = 2*R + 60 + w1 + 80
    H = 2*R + 90
    cx, cy = 40 + R, H/2
    # the chasing-S rendered in lime chrome with a dark bevel edge
    s_dark = arrow_s(scale=R/120*1.0, cx=cx+3, cy=cy+5, fill='#1d3f05', sw=30, head=30, halfw=26)
    s_lime = arrow_s(scale=R/120*1.0, cx=cx, cy=cy, fill='url(#limeChrome)', sw=28, head=28, halfw=24)
    glow = f'<circle cx="{cx}" cy="{cy}" r="{R*0.95}" fill="url(#limeOrb)" opacity=".16"/>' if dark else ''
    tx = 40 + 2*R + 40
    ty = cy + size*0.36
    fill = 'url(#limeChrome)'
    body = f'''{glow}{s_dark}{s_lime}
  <g transform="translate({tx},{ty})">
    {outlined(d1, fill, [('#0a2a00' if dark else '#0b1b3c', size*0.07)])}
  </g>'''
    return svg_doc(int(W), int(H), body, '#0d1620' if dark else None)

if __name__ == '__main__':
    write('Y1-chrome-wordmark.svg', y2k_wordmark())
    write('Y1-chrome-wordmark-dark.svg', y2k_wordmark(dark=True))
    write('Y2-sticker.svg', sticker())
    write('Y3-blob-horizontal.svg', blob())
    write('Y3-blob-horizontal-dark.svg', blob(dark=True))
    write('Y3-blob-mark.svg', blob_mark())
    write('Y4-lime-chrome-dark.svg', lime_x())
    write('Y4-lime-chrome.svg', lime_x(dark=False))
