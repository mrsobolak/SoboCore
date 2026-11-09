import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import text_path, text_width
from gen2 import svg_doc, MICH, outlined
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'final')
os.makedirs(OUT, exist_ok=True)

NAVY = '#0d1620'
EXTRA = '''
  <linearGradient id="ringLime" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#f6ffd6"/>
    <stop offset=".35" stop-color="#c6f14a"/>
    <stop offset=".65" stop-color="#7fc41a"/>
    <stop offset="1" stop-color="#3a7a0c"/>
  </linearGradient>
  <linearGradient id="chromeHi" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".9"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <filter id="softShadow" x="-10%" y="-20%" width="120%" height="160%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="6"/>
    <feOffset dy="8" result="b"/>
    <feComponentTransfer><feFuncA type="linear" slope=".55"/></feComponentTransfer>
    <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="limeGlow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="10"/>
  </filter>
'''
def doc(w, h, body, bg=None):
    return svg_doc(w, h, body, bg).replace('<defs>', '<defs>' + EXTRA, 1)

def write(name, d):
    open(os.path.join(OUT, name), 'w').write(d); print('wrote', name)

def fit_tracking(text, fontname, size, target_w):
    base = text_width(text, fontname, size, tracking=0)
    return (target_w - base) / (len(text) - 1)

def lockup(mode='dark', bg=True, stacked=False):
    """mode: dark | light | white (one colour) | black (one colour)"""
    size = 150
    tr = size*0.02
    d1, w1 = text_path('SOBOLAK', MICH, size, 0, 0, tracking=tr)
    sub = size*0.25
    tr2 = fit_tracking('TECHNOLOGIES', MICH, sub, w1*0.84)
    d2, w2 = text_path('TECHNOLOGIES', MICH, sub, 0, 0, tracking=tr2)
    cap = size*0.72
    # ring around the first O
    s_w = text_width('S', MICH, size, tracking=0) + tr
    o_w = text_width('O', MICH, size, tracking=0)
    o_cx = s_w + o_w/2
    o_cy = -cap/2
    rx, ry, rot = o_w*1.4, cap*0.34, -24
    sw = size*0.075

    one_colour = mode in ('white', 'black')
    ink = '#ffffff' if mode in ('dark', 'white') else '#0b1b3c'
    lime = '#d9ff6a' if mode in ('dark', 'white') else '#4c8f0e'
    if mode == 'black': ink = '#111'; lime = '#111'
    if mode == 'white': lime = '#fff'
    ring_fill = 'url(#ringLime)' if not one_colour else ink
    ring_edge = '#1d3f05' if not one_colour else None

    def ring_half(front):
        # local coords: ellipse centred at origin, rotated. back = upper arc, front = lower arc
        sweep = 0 if front else 1
        d = f'M{-rx:.1f},0 A{rx:.1f},{ry:.1f} 0 0 {sweep} {rx:.1f},0'
        g = f'<g transform="translate({o_cx:.1f},{o_cy:.1f}) rotate({rot})">'
        if ring_edge:
            g += f'<path d="{d}" fill="none" stroke="{ring_edge}" stroke-width="{sw+5:.1f}" stroke-linecap="butt"/>'
        g += f'<path d="{d}" fill="none" stroke="{ring_fill}" stroke-width="{sw:.1f}"/>'
        if not one_colour:
            g += f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="{sw*0.25:.1f}" transform="translate(0,{-sw*0.28:.1f})"/>'
        return g + '</g>'

    if one_colour:
        word = f'<path d="{d1}" fill="{ink}"/>'
    else:
        strokes = [('#000' if mode == 'dark' else '#0b1b3c', size*0.09), ('#eef2f6', size*0.04)]
        word = outlined(d1, 'url(#chrome)', strokes)
        # top highlight sweep on the chrome (clipped to glyphs)
        word += f'<clipPath id="wclip"><path d="{d1}"/></clipPath><rect x="-10" y="{-cap:.1f}" width="{w1+20:.1f}" height="{cap*0.32:.1f}" fill="url(#chromeHi)" clip-path="url(#wclip)" opacity=".7"/>'

    ring_back, ring_front = ring_half(False), ring_half(True)
    glow = ''
    if mode == 'dark':
        glow = f'<g filter="url(#limeGlow)" opacity=".35">{ring_half(True)}{ring_half(False)}</g>'

    shadow_filter = ' filter="url(#softShadow)"' if not one_colour else ''
    pad = 80
    if not stacked:
        W, H = int(w1 + 2*pad + 40), int(size + 2*pad + 40)
        ox, oy = pad + 20, pad + 20 + cap
        body = f'''<g transform="translate({ox},{oy})">
    {glow}{ring_back}
    <g{shadow_filter}>{word}</g>
    {ring_front}
    <g transform="translate({(w1-w2)/2:.1f},{sub*2.05:.1f})"><path d="{d2}" fill="{lime}"/></g>
  </g>'''
    else:
        W, H = int(w1 + 2*pad + 40), int(size + 2*pad + 40)
        ox, oy = pad + 20, pad + 20 + cap
        body = f'''<g transform="translate({ox},{oy})">
    {glow}{ring_back}
    <g{shadow_filter}>{word}</g>
    {ring_front}
    <g transform="translate({(w1-w2)/2:.1f},{sub*2.05:.1f})"><path d="{d2}" fill="{lime}"/></g>
  </g>'''
    bgcol = None
    if bg:
        bgcol = NAVY if mode in ('dark', 'white') else '#ffffff'
        if mode == 'black': bgcol = '#ffffff'
    return doc(W, H, body, bgcol)

def icon(mode='dark', bg=True, size=512):
    """The orbit O as a standalone mark / favicon."""
    s = size
    fs = s*0.54
    dO, wO = text_path('O', MICH, fs, 0, 0)
    cap = fs*0.72
    cx, cy = s/2, s/2
    rx, ry, rot = wO*1.28, cap*0.4, -28
    sw = fs*0.1
    one = mode in ('white', 'black')
    ink = '#fff' if mode in ('dark', 'white') else '#111'
    ring_fill = 'url(#ringLime)' if not one else ink
    def half(front):
        sweep = 0 if front else 1
        d = f'M{-rx:.1f},0 A{rx:.1f},{ry:.1f} 0 0 {sweep} {rx:.1f},0'
        g = f'<g transform="translate({cx},{cy}) rotate({rot})">'
        if not one:
            g += f'<path d="{d}" fill="none" stroke="#1d3f05" stroke-width="{sw+5:.1f}"/>'
        g += f'<path d="{d}" fill="none" stroke="{ring_fill}" stroke-width="{sw:.1f}"/>'
        if not one:
            g += f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="{sw*0.25:.1f}" transform="translate(0,{-sw*0.28:.1f})"/>'
        return g + '</g>'
    if one:
        letter = f'<path d="{dO}" fill="{ink}"/>'
    else:
        letter = outlined(dO, 'url(#chrome)', [('#000' if mode == 'dark' else '#0b1b3c', fs*0.09), ('#eef2f6', fs*0.04)])
    body = f'''{half(False)}
  <g transform="translate({cx - wO/2:.1f},{cy + cap/2:.1f})"{' filter="url(#softShadow)"' if not one else ''}>{letter}</g>
  {half(True)}'''
    bgcol = None
    if bg:
        bgcol = NAVY if mode in ('dark', 'white') else '#fff'
    if bg and mode == 'dark':
        body = f'<rect width="{s}" height="{s}" rx="{s*0.18}" fill="{NAVY}"/>' + body
        bgcol = None
    return doc(s, s, body, bgcol)

if __name__ == '__main__':
    write('sobolak-logo-dark.svg', lockup('dark'))
    write('sobolak-logo-dark-transparent.svg', lockup('dark', bg=False))
    write('sobolak-logo-light.svg', lockup('light'))
    write('sobolak-logo-light-transparent.svg', lockup('light', bg=False))
    write('sobolak-logo-onecolour-white.svg', lockup('white', bg=False))
    write('sobolak-logo-onecolour-black.svg', lockup('black', bg=False))
    write('sobolak-icon-dark.svg', icon('dark'))
    write('sobolak-icon-light.svg', icon('light'))
    write('sobolak-icon-onecolour-white.svg', icon('white', bg=False))
    write('sobolak-icon-onecolour-black.svg', icon('black', bg=False))
