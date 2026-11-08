import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import text_path, text_width, arrow_s
from gen2 import svg_doc, MICH, EXOI, SYNC, outlined
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out3')
os.makedirs(OUT, exist_ok=True)

EXTRA = '''
  <linearGradient id="ps2blue" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1d2b8f"/>
    <stop offset=".55" stop-color="#2f6fd6"/>
    <stop offset="1" stop-color="#5fd0ff"/>
  </linearGradient>
  <linearGradient id="ps2lime" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2d6a0a"/>
    <stop offset=".55" stop-color="#7fc41a"/>
    <stop offset="1" stop-color="#e2ff9a"/>
  </linearGradient>
  <linearGradient id="extrude" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#6aa51a"/>
    <stop offset="1" stop-color="#1f4a05"/>
  </linearGradient>
  <linearGradient id="chromeFace" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff"/>
    <stop offset=".46" stop-color="#d7dde4"/>
    <stop offset=".5" stop-color="#5f6a78"/>
    <stop offset=".54" stop-color="#aab4bf"/>
    <stop offset="1" stop-color="#f2f5f8"/>
  </linearGradient>
  <linearGradient id="ringChrome" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff"/>
    <stop offset=".48" stop-color="#b9c2cc"/>
    <stop offset=".52" stop-color="#58636f"/>
    <stop offset="1" stop-color="#e9edf1"/>
  </linearGradient>
  <linearGradient id="limeRing" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#4c8f0e"/>
    <stop offset=".5" stop-color="#d9ff6a"/>
    <stop offset="1" stop-color="#4c8f0e"/>
  </linearGradient>
'''
def doc(w, h, body, bg=None):
    return svg_doc(w, h, body, bg).replace('<defs>', '<defs>' + EXTRA, 1)

def write(name, d):
    open(os.path.join(OUT, name), 'w').write(d); print('wrote', name)

# ------------------------------------------------------------ Y3: circuit-trace wordmark (PS2 lane)
# letters on a 4x6 grid, y down. Each letter = list of polylines. Open ends get 'via' dots.
# letter = (list of polylines, list of via points). Only genuine trace ends get pads.
LET = {
 'S': ([[(4,0),(0,0),(0,3),(4,3),(4,6),(0,6)]], [(4,0),(0,6)]),
 'O': ([[(0,0),(4,0),(4,6),(0,6),(0,0),(0,0.01)]], []),
 'B': ([[(0,6),(0,0),(3,0),(4,1),(4,2),(3,3),(0,3)],[(3,3),(4,4),(4,5),(3,6),(0,6)]], []),
 'L': ([[(0,0),(0,6),(4,6)]], [(0,0),(4,6)]),
 'A': ([[(0,6),(0,1),(1,0),(3,0),(4,1),(4,6)],[(0,3.6),(4,3.6)]], [(0,6),(4,6)]),
 'K': ([[(0,0),(0,6)],[(4,0),(0.75,3.1)],[(1.55,2.35),(4,6)]], [(0,0),(0,6),(4,0),(4,6)]),
}
def circuit_word(word, u, sw, gapu=1.6):
    x = 0
    paths, vias = [], []
    for ch in word:
        pls, vs = LET[ch]
        for pl in pls:
            pts = [(x + px*u, py*u) for px, py in pl]
            paths.append('M' + ' L'.join(f'{px:.1f},{py:.1f}' for px, py in pts))
        vias += [(x + vx*u, vy*u) for vx, vy in vs]
        x += 4*u + gapu*u
    return paths, vias, x - gapu*u

def circuit(dark=False, lime=False):
    u = 26; sw = u*0.78
    paths, vias, w = circuit_word('SOBOLAK', u, sw)
    grad = 'url(#ps2lime)' if lime else 'url(#ps2blue)'
    sub = 30
    d2, w2 = text_path('TECHNOLOGIES', MICH, sub, 0, 0, tracking=sub*0.62)
    W, H = int(w + 160), int(6*u + 190)
    ox, oy = 80, 60
    body = f'<g transform="translate({ox},{oy})" fill="none" stroke="{grad}" stroke-width="{sw:.1f}" stroke-linejoin="miter" stroke-linecap="square">\n'
    body += ''.join(f'  <path d="{d}"/>\n' for d in paths) + '</g>\n'
    # vias: pads at open trace ends, PCB style (ring + hole)
    body += f'<g transform="translate({ox},{oy})">\n'
    for vx, vy in vias:
        body += f'  <circle cx="{vx:.1f}" cy="{vy:.1f}" r="{sw*0.8:.1f}" fill="{grad}"/><circle cx="{vx:.1f}" cy="{vy:.1f}" r="{sw*0.3:.1f}" fill="{"#0d1620" if dark else "#fff"}"/>\n'
    body += '</g>\n'
    body += f'<g transform="translate({ox + (w-w2)/2:.1f},{oy + 6*u + 78})"><path d="{d2}" fill="{"#cfe3ff" if dark else "#1d2b8f"}"/></g>'
    return doc(W, H, body, '#0d1620' if dark else None)

# ------------------------------------------------------------ Y4: 3D chrome S emblem in an oval ring (Skechers / Xbox lane)
def emblem(dark=False):
    size = 300
    dS, wS = text_path('S', EXOI, size, 0, 0)
    sub = 58
    d1, w1 = text_path('SOBOLAK', SYNC, sub, 0, 0, tracking=sub*0.12)
    sub2 = 20
    d2, w2 = text_path('TECHNOLOGIES', MICH, sub2, 0, 0, tracking=sub2*0.6)
    W, H = 760, 560
    cx, cy = W/2, 240
    rx, ry = 300, 150
    # ring: chrome oval with navy outline, tilted a touch
    ring = f'''<g transform="translate({cx},{cy}) rotate(-8)">
    <ellipse rx="{rx}" ry="{ry}" fill="none" stroke="#0b1b3c" stroke-width="34"/>
    <ellipse rx="{rx}" ry="{ry}" fill="none" stroke="url(#ringChrome)" stroke-width="24"/>
    <ellipse rx="{rx}" ry="{ry}" fill="none" stroke="#0b1b3c" stroke-width="2" transform="scale(1.02,1.045)" opacity=".0"/>
    <ellipse rx="{rx}" ry="{ry}" fill="none" stroke="url(#limeRing)" stroke-width="5" transform="scale(0.955,0.91)"/>
  </g>'''
    # extruded S: stack offset copies for depth, then chrome face with navy outline
    sx = cx - wS/2 - 6; sy = cy + size*0.36
    depth = 16
    ext = ''.join(f'<path d="{dS}" fill="url(#extrude)" stroke="#1f4a05" stroke-width="10" stroke-linejoin="round" transform="translate({sx + i*0.9:.1f},{sy + i*1.1:.1f})"/>\n' for i in range(depth, 0, -1))
    face = f'<g transform="translate({sx},{sy})">{outlined(dS, "url(#chromeFace)", [("#0b1b3c", 16), ("#eef2f6", 6)])}</g>'
    # highlight sweep on face
    body = ring + ext + face
    body += f'<g transform="translate({cx - w1/2},{cy + ry + 112})"><path d="{d1}" fill="{"#fff" if dark else "#0b1b3c"}"/></g>'
    body += f'<g transform="translate({cx - w2/2},{cy + ry + 150})"><path d="{d2}" fill="{"#d9ff6a" if dark else "#4c8f0e"}"/></g>'
    return doc(W, H, body, '#0d1620' if dark else None)

# ------------------------------------------------------------ Y5: black bar lockup (Toonami lane)
def bar(dark=False):
    size = 150
    d1, w1 = text_path('SOBOLAK', EXOI, size, 0, 0, tracking=size*0.01)
    sub = 30
    d2, w2 = text_path('TECHNOLOGIES', SYNC, sub, 0, 0, tracking=sub*0.3)
    pad = 56
    bw, bh = w1 + 2*pad, 190
    W, H = int(bw + 80), int(bh + 130)
    bx, by = 40, 30
    skew = 12
    body = f'''<g transform="translate({bx+bw/2},{by+bh/2}) skewX(-{skew}) translate({-(bx+bw/2)},{-(by+bh/2)})">
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="26" fill="#000"/>
    <rect x="{bx+8}" y="{by+8}" width="{bw-16}" height="{bh-16}" rx="20" fill="none" stroke="#fff" stroke-width="5"/>
    <rect x="{bx+8}" y="{by+8}" width="{bw-16}" height="{bh*0.42}" rx="20" fill="#fff" opacity=".06"/>
  </g>
  <g transform="translate({bx+pad},{by+bh/2 + size*0.36})">
    {outlined(d1, '#000', [('#fff', 14)])}
  </g>
  <g transform="translate({bx + bw - w2 - 10:.1f},{by + bh + 62})">
    <path d="{d2}" fill="{"#fff" if dark else "#000"}"/>
    <path d="M{-bw + w2 + 10 + 20:.1f},-11 H-24" stroke="{"#d9ff6a" if dark else "#4c8f0e"}" stroke-width="6"/>
  </g>'''
    return doc(W, H, body, '#0d1620' if dark else None)

if __name__ == '__main__':
    write('Y3-circuit.svg', circuit())
    write('Y3-circuit-dark.svg', circuit(dark=True))
    write('Y3-circuit-lime-dark.svg', circuit(dark=True, lime=True))
    write('Y4-chrome-emblem.svg', emblem())
    write('Y4-chrome-emblem-dark.svg', emblem(dark=True))
    write('Y5-bar.svg', bar())
    write('Y5-bar-dark.svg', bar(dark=True))
