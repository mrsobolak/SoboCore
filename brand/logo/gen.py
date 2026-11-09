import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', 'fonts')
OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)

_fonts = {}
def font(name):
    if name not in _fonts:
        _fonts[name] = TTFont(os.path.join(FONTS, name))
    return _fonts[name]

def kern_pairs(f):
    """Flat kerning from GPOS pair adjustment (format 1 only, enough for Latin)."""
    pairs = {}
    try:
        gpos = f['GPOS'].table
    except KeyError:
        return pairs
    for lookup in gpos.LookupList.Lookup:
        for st in lookup.SubTable:
            if lookup.LookupType == 9:
                st = st.ExtSubTable
            if getattr(st, 'LookupType', lookup.LookupType) != 2:
                continue
            if st.Format == 1:
                for i, first in enumerate(st.Coverage.glyphs):
                    for pvr in st.PairSet[i].PairValueRecord:
                        v = pvr.Value1.XAdvance if pvr.Value1 and hasattr(pvr.Value1, 'XAdvance') else 0
                        if v:
                            pairs.setdefault((first, pvr.SecondGlyph), v)
            elif st.Format == 2:
                cd1, cd2 = st.ClassDef1.classDefs, st.ClassDef2.classDefs
                for first in st.Coverage.glyphs:
                    c1 = cd1.get(first, 0)
                    rec1 = st.Class1Record[c1]
                    for second, c2 in list(cd2.items()):
                        v = rec1.Class2Record[c2].Value1
                        v = v.XAdvance if v and hasattr(v, 'XAdvance') else 0
                        if v:
                            pairs.setdefault((first, second), v)
    return pairs

_kern = {}
def text_path(text, fontname, size, x=0, y=0, tracking=0):
    """Return (svg path d, advance width) for text drawn with baseline at (x,y)."""
    f = font(fontname)
    if fontname not in _kern:
        _kern[fontname] = kern_pairs(f)
    kern = _kern[fontname]
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    upm = f['head'].unitsPerEm
    s = size / upm
    pen = SVGPathPen(gs)
    cx = x
    prev = None
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            cx += size * 0.3
            prev = None
            continue
        if prev is not None:
            cx += kern.get((prev, g), 0) * s
        tp = TransformPen(pen, (s, 0, 0, -s, cx, y))
        gs[g].draw(tp)
        cx += gs[g].width * s + tracking
        prev = g
    return pen.getCommands(), cx - x

def text_width(text, fontname, size, tracking=0):
    return text_path(text, fontname, size, tracking=tracking)[1]

HEAVY = 'LibreFranklin-ExtraBold.ttf'
MED = 'LibreFranklin-Medium.ttf'
OS = 'OpenSans-SemiBold.ttf'

# ---------------------------------------------------------------- marks
def defs_common():
    return '''
  <radialGradient id="orbG" cx="50%" cy="38%" r="68%">
    <stop offset="0" stop-color="#b9f08a"/>
    <stop offset=".45" stop-color="#5fc23f"/>
    <stop offset=".8" stop-color="#2a8f2a"/>
    <stop offset="1" stop-color="#1b6a1e"/>
  </radialGradient>
  <linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".92"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="rimDark" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2d7a2a"/>
    <stop offset="1" stop-color="#0f4512"/>
  </linearGradient>
  <linearGradient id="arrowW" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff"/>
    <stop offset="1" stop-color="#e3f3dc"/>
  </linearGradient>
  <radialGradient id="shadow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#000" stop-opacity=".38"/>
    <stop offset="1" stop-color="#000" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="inkBlue" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2b4f8f"/>
    <stop offset="1" stop-color="#15305e"/>
  </linearGradient>
  <linearGradient id="inkGreen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#3f9a2e"/>
    <stop offset="1" stop-color="#1f6a1f"/>
  </linearGradient>
  <linearGradient id="glassTile" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#5a7fb8"/>
    <stop offset=".5" stop-color="#20406f"/>
    <stop offset="1" stop-color="#0d2246"/>
  </linearGradient>
  <linearGradient id="tileGloss" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".55"/>
    <stop offset="1" stop-color="#fff" stop-opacity=".06"/>
  </linearGradient>
  <linearGradient id="leaf" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#c8f58f"/>
    <stop offset=".5" stop-color="#63c73d"/>
    <stop offset="1" stop-color="#2a8a28"/>
  </linearGradient>
  <linearGradient id="chipBody" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f6f8fb"/>
    <stop offset="1" stop-color="#c9d3e2"/>
  </linearGradient>
'''

def arrow_s(scale=1.0, cx=0, cy=0, fill='url(#arrowW)', sw=17, r=38, gap_deg=28, head=24, halfw=18):
    """Two chasing arrows forming an S (recycle motif). Centered at (cx,cy)."""
    # geometry in local coords, then scaled & translated
    d = r + 4            # centre offset of each loop from the midpoint
    g = math.radians(gap_deg)
    # top loop: centre (0,-d). start a bit clockwise past 6 o'clock, run clockwise to 2 o'clock
    sx, sy = -r*math.sin(g), -d + r*math.cos(g)
    end_ang = 60
    ex, ey = r*math.sin(math.radians(end_ang)), -d - r*math.cos(math.radians(end_ang))
    top = f'M{sx:.2f},{sy:.2f} A{r},{r} 0 1 1 {ex:.2f},{ey:.2f}'
    # bottom loop is the 180deg rotation
    bot = f'M{-sx:.2f},{-sy:.2f} A{r},{r} 0 1 1 {-ex:.2f},{-ey:.2f}'
    tri = f'M{-halfw},0 L{halfw},0 L0,{head} Z'
    rot_top = -(90 - end_ang)   # tangent direction at end
    return f'''<g transform="translate({cx},{cy}) scale({scale})">
    <g fill="none" stroke="{fill}" stroke-width="{sw}">
      <path d="{top}"/><path d="{bot}"/>
    </g>
    <g fill="{fill}">
      <path transform="translate({ex:.2f},{ey:.2f}) rotate({rot_top})" d="{tri}"/>
      <path transform="translate({-ex:.2f},{-ey:.2f}) rotate({rot_top+180})" d="{tri}"/>
    </g>
  </g>'''

def orb(cx, cy, R, inner=None):
    """XP-style glossy green orb with a recycle-S inside."""
    inner = inner or (lambda: arrow_s(scale=R/120, cx=cx, cy=cy))
    return f'''
  <ellipse cx="{cx}" cy="{cy + R*0.92}" rx="{R*0.9}" ry="{R*0.22}" fill="url(#shadow)"/>
  <circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#rimDark)"/>
  <circle cx="{cx}" cy="{cy}" r="{R*0.93}" fill="url(#orbG)"/>
  <ellipse cx="{cx}" cy="{cy - R*0.52}" rx="{R*0.74}" ry="{R*0.38}" fill="url(#gloss)" opacity=".85"/>
  <path d="M{cx - R*0.78},{cy + R*0.42} A{R*0.9},{R*0.9} 0 0 0 {cx + R*0.78},{cy + R*0.42}" fill="none" stroke="#dfffd0" stroke-opacity=".45" stroke-width="{R*0.06}" stroke-linecap="round"/>
  {inner()}
  <circle cx="{cx}" cy="{cy}" r="{R*0.93}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="{R*0.03}"/>
  <ellipse cx="{cx - R*0.3}" cy="{cy - R*0.62}" rx="{R*0.22}" ry="{R*0.1}" fill="#fff" fill-opacity=".55" transform="rotate(-20 {cx - R*0.3} {cy - R*0.62})"/>'''

def chip_tile(cx, cy, S):
    """Vista glass tile with a recycled CPU chip and a sprouting leaf."""
    r = S*0.18
    x, y = cx - S/2, cy - S/2
    c = S*0.5
    pin = S*0.045
    pins = []
    for i in range(5):
        t = x + S*0.30 + i*(S*0.10)
        pins.append(f'<rect x="{t:.1f}" y="{y+S*0.17:.1f}" width="{pin:.1f}" height="{S*0.10:.1f}"/>')
        pins.append(f'<rect x="{t:.1f}" y="{y+S*0.73:.1f}" width="{pin:.1f}" height="{S*0.10:.1f}"/>')
        u = y + S*0.30 + i*(S*0.10)
        pins.append(f'<rect x="{x+S*0.17:.1f}" y="{u:.1f}" width="{S*0.10:.1f}" height="{pin:.1f}"/>')
        pins.append(f'<rect x="{x+S*0.73:.1f}" y="{u:.1f}" width="{S*0.10:.1f}" height="{pin:.1f}"/>')
    # leaf: grows from chip's upper-right corner
    lx, ly = cx + S*0.14, cy - S*0.14
    L = S*0.34
    leaf = f'''<g transform="translate({lx:.1f},{ly:.1f}) rotate(-35)">
      <path d="M0,0 C{L*0.1:.1f},{-L*0.9:.1f} {L*0.75:.1f},{-L*1.05:.1f} {L:.1f},{-L*0.98:.1f} C{L*0.98:.1f},{-L*0.35:.1f} {L*0.6:.1f},{L*0.05:.1f} 0,0 Z" fill="url(#leaf)" stroke="#1d5f1c" stroke-width="{S*0.018:.1f}"/>
      <path d="M{L*0.08:.1f},{-L*0.04:.1f} L{L*0.86:.1f},{-L*0.86:.1f}" fill="none" stroke="#1d5f1c" stroke-opacity=".55" stroke-width="{S*0.014:.1f}"/>
    </g>'''
    return f'''
  <ellipse cx="{cx}" cy="{cy + S*0.56}" rx="{S*0.5}" ry="{S*0.12}" fill="url(#shadow)"/>
  <rect x="{x}" y="{y}" width="{S}" height="{S}" rx="{r}" fill="#0b1b3a"/>
  <rect x="{x+S*0.025}" y="{y+S*0.025}" width="{S*0.95}" height="{S*0.95}" rx="{r*0.9}" fill="url(#glassTile)"/>
  <path d="M{x+S*0.06},{y+S*0.42} Q{cx},{y+S*0.30} {x+S*0.94},{y+S*0.42} L{x+S*0.94},{y+S*0.16} Q{x+S*0.94},{y+S*0.05} {x+S*0.84},{y+S*0.05} L{x+S*0.16},{y+S*0.05} Q{x+S*0.06},{y+S*0.05} {x+S*0.06},{y+S*0.16} Z" fill="url(#tileGloss)"/>
  <g fill="#dfe8f5">{''.join(pins)}</g>
  <rect x="{x+S*0.26}" y="{y+S*0.26}" width="{S*0.48}" height="{S*0.48}" rx="{S*0.05}" fill="url(#chipBody)" stroke="#8fa3c2" stroke-width="{S*0.012}"/>
  <rect x="{x+S*0.34}" y="{y+S*0.34}" width="{S*0.32}" height="{S*0.32}" rx="{S*0.03}" fill="none" stroke="#9fb2cf" stroke-width="{S*0.012}"/>
  <circle cx="{cx - S*0.12}" cy="{cy + S*0.12}" r="{S*0.025}" fill="#7f94b5"/>
  {leaf}
  <rect x="{x+S*0.025}" y="{y+S*0.025}" width="{S*0.95}" height="{S*0.95}" rx="{r*0.9}" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="{S*0.014}"/>'''

def wordmark(x, y, size, stack=True, dark=True, tracking_t=None):
    """'Sobolak' heavy + 'Technologies' medium. Returns (svg, width, height)."""
    top_fill = 'url(#inkBlue)' if dark else '#fff'
    sub_fill = 'url(#inkGreen)' if dark else '#d8f2c8'
    d1, w1 = text_path('Sobolak', HEAVY, size, x, y, tracking=-size*0.012)
    sub = size*0.355
    tr = tracking_t if tracking_t is not None else sub*0.21
    d2, w2 = text_path('TECHNOLOGIES', MED, sub, x + size*0.02, y + sub*1.25, tracking=tr)
    svg = f'<path d="{d1}" fill="{top_fill}"/>\n  <path d="{d2}" fill="{sub_fill}"/>'
    return svg, max(w1, w2), size*0.75 + sub*1.25

def svg_doc(w, h, body, bg=None):
    bgrect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>{defs_common()}</defs>
{bgrect}
{body}
</svg>'''

# ---------------------------------------------------------------- lockups
def write(name, doc):
    p = os.path.join(OUT, name)
    with open(p, 'w') as fh:
        fh.write(doc)
    print('wrote', p)

def concept_a(dark=True, bg=None):
    R = 110
    wm, ww, wh = wordmark(0, 0, 118, dark=dark)
    # measure then place
    W = 2*R + 48 + ww + 60
    H = 2*R + 70
    cx, cy = 30 + R, H/2 - 10
    tx = 2*R + 30 + 44
    ty = cy + 118*0.75/2 - 118*0.355*1.25/2 + 6
    body = orb(cx, cy, R) + f'\n  <g transform="translate({tx},{ty})">{wordmark(0,0,118,dark=dark)[0]}</g>'
    return svg_doc(int(W), int(H), body, bg)

def concept_a_stacked(dark=True, bg=None):
    R = 150
    wm, ww, wh = wordmark(0, 0, 150, dark=dark)
    W = max(2*R, ww) + 120
    H = 2*R + 60 + wh + 70
    cx = W/2
    body = orb(cx, 40 + R, R)
    body += f'\n  <g transform="translate({cx - ww/2},{2*R + 40 + 60 + 150*0.72})">{wm}</g>'
    return svg_doc(int(W), int(H), body, bg)

def concept_b(dark=True, bg=None):
    S = 220
    wm, ww, wh = wordmark(0, 0, 118, dark=dark)
    W = S + 48 + ww + 60
    H = S + 70
    cx, cy = 30 + S/2, H/2 - 8
    tx = S + 30 + 44
    ty = cy + 118*0.75/2 - 118*0.355*1.25/2 + 6
    body = chip_tile(cx, cy, S) + f'\n  <g transform="translate({tx},{ty})">{wm}</g>'
    return svg_doc(int(W), int(H), body, bg)

def concept_c(dark=True, bg=None):
    """Wordmark-led: SOBOLAK in caps, the second O replaced with a small recycle orb."""
    size = 150
    # build "SOB" + orb + "LAK" with the orb as the O
    d1, w1 = text_path('SOB', HEAVY, size, 0, 0, tracking=size*0.03)
    d2, w2 = text_path('LAK', HEAVY, size, 0, 0, tracking=size*0.03)
    o_w = text_width('O', HEAVY, size)
    R = o_w*0.52
    gap = size*0.03
    x_orb = w1 + gap + R
    x2 = x_orb + R + gap
    total = x2 + w2
    sub = size*0.30
    d3, w3 = text_path('TECHNOLOGIES', MED, sub, 0, 0, tracking=sub*0.42)
    top_fill = 'url(#inkBlue)' if dark else '#fff'
    sub_fill = 'url(#inkGreen)' if dark else '#d8f2c8'
    W = total + 100
    H = size + sub*2.6 + 70
    ox, oy = 50, 50 + size*0.72
    body = f'''<g transform="translate({ox},{oy})">
    <path d="{d1}" fill="{top_fill}"/>
    <g transform="translate({x2},0)"><path d="{d2}" fill="{top_fill}"/></g>
    {orb(x_orb, -size*0.36, R)}
    <g transform="translate({(total - w3)/2},{sub*1.9})"><path d="{d3}" fill="{sub_fill}"/></g>
  </g>'''
    return svg_doc(int(W), int(H), body, bg)

def mark_only_a():
    R = 120
    return svg_doc(2*R+40, 2*R+56, orb(R+20, R+20, R))

def mark_only_b():
    S = 240
    return svg_doc(S+40, S+70, chip_tile(S/2+20, S/2+20, S))

if __name__ == '__main__':
    write('A-orb-horizontal.svg', concept_a())
    write('A-orb-horizontal-dark.svg', concept_a(dark=False, bg='#0f2a4f'))
    write('A-orb-stacked.svg', concept_a_stacked())
    write('A-mark.svg', mark_only_a())
    write('B-chip-horizontal.svg', concept_b())
    write('B-chip-horizontal-dark.svg', concept_b(dark=False, bg='#0f2a4f'))
    write('B-mark.svg', mark_only_b())
    write('C-wordmark.svg', concept_c())
    write('C-wordmark-dark.svg', concept_c(dark=False, bg='#0f2a4f'))
