# Stamps out the static pages. Run: python3 tools/build_pages.py
# Every page is a full HTML 4.01 file with the player chrome built from tables and sliced GIFs.
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

PAGES = [
  # file, nav id, nav label, window title, status text
  ('index.html',    'nowplaying', 'Now Playing',          'Sobolak Technologies',                         'Album: Sobolak Technologies &middot; Michigan &middot; Est. 2024'),
  ('about.html',    'guide',      'Media Guide',          'About - Sobolak Technologies',                 'Media Guide &middot; About the company'),
  ('recycle.html',  'copycd',     'Copy from CD',         'Chipset Recycling - Sobolak Technologies',     'Copy from CD &middot; Chipset recycling'),
  ('products.html', 'library',    'Media Library',        'Products - Sobolak Technologies',              'Media Library &middot; Products'),
  ('status.html',   'radio',      'Radio Tuner',          'Status - Sobolak Technologies',                'Radio Tuner &middot; Service status'),
  ('contact.html',  'device',     'Copy to CD or Device', 'Contact - Sobolak Technologies',               'Copy to CD or Device &middot; Contact'),
  ('skins.html',    'skins',      'Skin Chooser',         'Skin Chooser - Sobolak Technologies',          'Skin Chooser'),
]
NAV_ALT = {'nowplaying':'Now Playing','guide':'Media Guide','copycd':'Copy from CD','library':'Media Library','radio':'Radio Tuner','device':'Copy to CD or Device','skins':'Skin Chooser'}

ROADMAP = [
  ('The idea', 'now', 'index.html'),
  ('Chipset recycling', 'plan', 'recycle.html'),
  ('Motherboard schematic', 'design', 'products.html'),
  ('3D model', 'soon', 'products.html'),
  ('Prototype', 'later', 'status.html'),
  ('First units', 'TBA', 'contact.html'),
]

HEAD = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>{title}</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="description" content="Sobolak Technologies, Michigan. A recycled handheld desktop built on a custom motherboard that rescues chipsets from dead laptops. Coming soon.">
<meta name="keywords" content="Sobolak Technologies, recycled computers, handheld desktop, chipset recycling, Michigan, e-waste, custom motherboard">
<meta name="author" content="Sobolak Technologies">
<meta name="viewport" content="width=800">
<link rel="shortcut icon" href="favicon.ico">
<link rel="stylesheet" href="style.css" type="text/css">
<script language="JavaScript" type="text/javascript">
<!--
// rollovers for the task pane
var navImgs = new Array('nowplaying','guide','copycd','library','radio','device','skins');
var pre = new Array();
for (var i = 0; i < navImgs.length; i++) {{
  pre[i] = new Image(110, 36);
  pre[i].src = 'images/nav_' + navImgs[i] + '_over.gif';
}}
function swap(name, state) {{
  if (document.images && document.images[name] && document.images[name].alt != 'current') {{
    document.images[name].src = 'images/nav_' + name + '_' + state + '.gif';
  }}
}}
function trOver(name) {{ if (document.images) document.images[name].src = 'images/' + name + '_over.gif'; }}
function trOut(name)  {{ if (document.images) document.images[name].src = 'images/' + name + '.gif'; }}
// the little clock in the status line
var t0 = new Date();
function tick() {{
  var s = Math.floor((new Date() - t0) / 1000);
  var m = Math.floor(s / 60); s = s % 60;
  var txt = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
  if (document.getElementById) document.getElementById('clock').innerHTML = txt;
  setTimeout('tick()', 1000);
}}
//-->
</script>
</head>
<body bgcolor="#2f5f9e" background="images/desktop_bg.gif" text="#ffffff" link="#39e639" vlink="#39e639" alink="#ffffff" onLoad="tick()" topmargin="24" marginheight="24">

<!-- ================= the player window ================= -->
<table width="780" border="0" cellpadding="0" cellspacing="0" align="center" bgcolor="#2a52a8" style="border: 1px solid #1d3f8a;">

<!-- title bar -->
<tr>
  <td height="30" background="images/titlebar_bg.gif">
    <table width="100%" border="0" cellpadding="0" cellspacing="0">
    <tr>
      <td width="8"><img src="images/spacer.gif" width="8" height="1" alt=""></td>
      <td width="16"><img src="images/icon16.gif" width="16" height="16" alt=""></td>
      <td width="6"><img src="images/spacer.gif" width="6" height="1" alt=""></td>
      <td class="wintitle">Sobolak Technologies</td>
      <td align="right" nowrap>
        <a href="javascript:void(0)" onClick="alert('Minimize? This is a web page. Nice try.')"><img src="images/tb_min.gif" width="21" height="21" border="0" alt="Minimize"></a><img src="images/spacer.gif" width="2" height="1" alt=""><a href="javascript:void(0)" onClick="alert('It is already as big as it gets. 780 pixels.')"><img src="images/tb_max.gif" width="21" height="21" border="0" alt="Maximize"></a><img src="images/spacer.gif" width="2" height="1" alt=""><a href="javascript:window.close()"><img src="images/tb_close.gif" width="21" height="21" border="0" alt="Close"></a>
      </td>
      <td width="5"><img src="images/spacer.gif" width="5" height="1" alt=""></td>
    </tr>
    </table>
  </td>
</tr>

<!-- menu bar -->
<tr>
  <td height="22" background="images/menubar_bg.gif" class="menubar">
    <img src="images/spacer.gif" width="6" height="1" alt=""><a href="index.html" class="menu"><u>F</u>ile</a><a href="about.html" class="menu"><u>V</u>iew</a><a href="products.html" class="menu"><u>P</u>lay</a><a href="recycle.html" class="menu"><u>T</u>ools</a><a href="contact.html" class="menu"><u>H</u>elp</a>
  </td>
</tr>

<!-- body: task pane | viewer | playlist -->
<tr>
  <td background="images/frame_bg.gif">
    <table width="100%" border="0" cellpadding="0" cellspacing="6">
    <tr>
      <!-- task pane -->
      <td width="110" valign="top">
        <img src="images/spacer.gif" width="110" height="4" alt=""><br>
{nav}
        <br><br><br><br><br>
        <img src="images/pane_logo.gif" width="100" height="62" alt="Sobolak Technologies" style="margin-left: 5px;">
      </td>

      <!-- viewer -->
      <td valign="top" bgcolor="#000000" style="border: 1px solid #1d3f8a;">
        <table width="100%" border="0" cellpadding="0" cellspacing="0">
        <tr>
          <td align="right" style="padding: 4px 6px 0 0;"><a href="{prev}"><img src="images/vt_prev.gif" width="18" height="18" border="0" alt="Previous"></a> <a href="{next}"><img src="images/vt_next.gif" width="18" height="18" border="0" alt="Next"></a> <a href="#roadmap"><img src="images/vt_list.gif" width="18" height="18" border="0" alt="Roadmap"></a></td>
        </tr>
        <tr>
          <td valign="top" style="padding: 0 14px 12px 14px;">
'''

PLAYLIST_AND_REST = '''
          </td>
        </tr>
        </table>
      </td>

      <!-- playlist -->
      <td width="188" valign="top">
        <a name="roadmap"></a>
        <img src="images/pl_header.gif" width="188" height="20" alt="Roadmap"><br>
        <img src="images/spacer.gif" width="1" height="4" alt=""><br>
        <table width="188" border="0" cellpadding="6" cellspacing="0" bgcolor="#000000" style="border: 1px solid #1d3f8a;" height="{plh}">
        <tr>
          <td valign="top" class="playlist">
            <span class="plhead">&#9662; The Recycled Handheld Desktop</span><br>
            <table border="0" cellpadding="1" cellspacing="0" width="100%" style="margin-left: 8px;">
{roadmap}
            </table>
          </td>
        </tr>
        </table>
        <div align="right" class="playlist" style="padding-top: 4px;">Total Time: TBA</div>
      </td>
    </tr>
    </table>
  </td>
</tr>

<!-- status line -->
<tr>
  <td height="20" bgcolor="#000000" style="border-top: 1px solid #1d3f8a;">
    <table width="100%" border="0" cellpadding="0" cellspacing="0">
    <tr>
      <td class="status" style="padding-left: 14px;"><img src="images/play_green.gif" width="10" height="10" alt="">&nbsp; {status}</td>
      <td class="status" align="right" style="padding-right: 12px;"><span id="clock">00:00</span></td>
    </tr>
    </table>
  </td>
</tr>

<!-- transport -->
<tr>
  <td height="60" background="images/transport_bg.gif">
    <table width="100%" border="0" cellpadding="0" cellspacing="0">
    <tr>
      <td width="8"><img src="images/spacer.gif" width="8" height="1" alt=""></td>
      <td width="56"><a href="index.html" onMouseOver="trOver('tr_pause')" onMouseOut="trOut('tr_pause')"><img name="tr_pause" src="images/tr_pause.gif" width="54" height="54" border="0" alt="Pause"></a></td>
      <td width="34"><a href="index.html" onMouseOver="trOver('tr_stop')" onMouseOut="trOut('tr_stop')"><img name="tr_stop" src="images/tr_stop.gif" width="32" height="32" border="0" alt="Stop"></a></td>
      <td width="30"><a href="{prev}" onMouseOver="trOver('tr_prev')" onMouseOut="trOut('tr_prev')"><img name="tr_prev" src="images/tr_prev.gif" width="28" height="28" border="0" alt="Previous"></a></td>
      <td width="30"><a href="{next}" onMouseOver="trOver('tr_next')" onMouseOut="trOut('tr_next')"><img name="tr_next" src="images/tr_next.gif" width="28" height="28" border="0" alt="Next"></a></td>
      <td width="30"><a href="javascript:void(0)" onClick="alert('There is no sound. It is a web page.')" onMouseOver="trOver('tr_mute')" onMouseOut="trOut('tr_mute')"><img name="tr_mute" src="images/tr_mute.gif" width="28" height="28" border="0" alt="Mute"></a></td>
      <td width="14"><img src="images/spacer.gif" width="14" height="1" alt=""></td>
      <td>
        <table width="100%" border="0" cellpadding="0" cellspacing="0">
        <tr>
          <td width="{seekpct}%" height="6" background="images/seek_fill.gif"><img src="images/spacer.gif" width="1" height="6" alt=""></td>
          <td width="16"><img src="images/seek_knob.gif" width="16" height="16" alt=""></td>
          <td height="6" background="images/seek_bg.gif"><img src="images/spacer.gif" width="1" height="6" alt=""></td>
        </tr>
        </table>
      </td>
      <td width="24"><img src="images/spacer.gif" width="24" height="1" alt=""></td>
      <td width="72">
        <table width="72" border="0" cellpadding="0" cellspacing="0">
        <tr>
          <td width="44" height="6" background="images/seek_fill.gif"><img src="images/spacer.gif" width="1" height="6" alt=""></td>
          <td width="16"><img src="images/seek_knob.gif" width="16" height="16" alt=""></td>
          <td height="6" background="images/seek_bg.gif"><img src="images/spacer.gif" width="1" height="6" alt=""></td>
        </tr>
        </table>
      </td>
      <td width="14"><img src="images/spacer.gif" width="14" height="1" alt=""></td>
    </tr>
    </table>
  </td>
</tr>
</table>

<!-- footer -->
<table width="780" border="0" cellpadding="0" cellspacing="0" align="center">
<tr>
  <td align="center" class="footer" style="padding-top: 14px;">
    <a href="index.html">Now Playing</a> | <a href="about.html">About</a> | <a href="recycle.html">Recycling</a> | <a href="products.html">Products</a> | <a href="status.html">Status</a> | <a href="contact.html">Contact</a> | <a href="skins.html">Skins</a><br>
    <img src="images/spacer.gif" width="1" height="6" alt=""><br>
    Sobolak Technologies &middot; Michigan, United States &middot; Last updated November 8, 2026<br>
    Best viewed at 1024&times;768 with the speakers on. No cookies, no trackers, no server-side anything.
  </td>
</tr>
</table>
<br>
</body>
</html>
'''

# -------------------------------------------------------------- page bodies
HOME = '''
            <span class="artist">Sobolak Technologies</span><br>
            <span class="track">The Recycled Handheld Desktop (coming soon)</span><br>
            <img src="images/spacer.gif" width="1" height="6" alt=""><br>
            <table width="100%" border="0" cellpadding="0" cellspacing="0" style="border: 1px solid #1b2a4a;" bgcolor="#000000">
            <tr><td align="center"><img src="images/vis.gif" width="420" height="230" alt="Sobolak Technologies"></td></tr>
            </table>
            <img src="images/spacer.gif" width="1" height="8" alt=""><br>
            <table width="100%" border="0" cellpadding="10" cellspacing="0" bgcolor="#060f22" style="border: 1px solid #2c4a8a;">
            <tr><td class="body">
              A handheld desktop with a screen. Inside, a motherboard we design ourselves so that chipsets pulled from dead laptops can be used again.<br><br>
              There is no 3D model yet. There is an idea we are serious about, a room of old hardware in Michigan, and one person working on it.
            </td></tr>
            </table>
            <img src="images/spacer.gif" width="1" height="8" alt=""><br>
            <table width="100%" border="0" cellpadding="0" cellspacing="0">
            <tr>
              <td class="visname" valign="bottom">Ambience: <b>Water</b></td>
              <td align="right"><img src="images/sticker.gif" width="212" height="34" alt="Look into the e-waste"></td>
            </tr>
            </table>
'''

ABOUT = '''
            <h1>About Sobolak Technologies</h1>
            <p class="lead">An independent technology company in Michigan, United States. Founded 2024. Privately held, no investors, one person on staff.</p>
            <p class="body">We have started over before. This time the work is hardware: computers built from parts the rest of the industry has written off. Earlier projects are retired and not coming back, and the pages about them have come down. This site is about what comes next.</p>
            <h2>What we care about</h2>
            <ul class="body">
              <li><b>Own the hardware.</b> If it runs on someone else's machine, it is on loan.</li>
              <li><b>Nothing is scrap until it fails a test.</b> A ten-year-old CPU still does what it did on day one.</li>
              <li><b>Built to last.</b> Repairable, documented, and boring in the good way.</li>
              <li><b>Say so.</b> If something is an idea, we call it an idea. No fake launch dates.</li>
            </ul>
            <table border="0" cellpadding="4" cellspacing="0" class="props" width="90%">
              <tr><td class="key" width="34%">Location</td><td class="body">Michigan, United States</td></tr>
              <tr><td class="key">Founded</td><td class="body">2024</td></tr>
              <tr><td class="key">Type</td><td class="body">Independent, privately held</td></tr>
              <tr><td class="key">Investors</td><td class="body">None</td></tr>
              <tr><td class="key">Staff</td><td class="body">One, the founder</td></tr>
              <tr><td class="key">Current focus</td><td class="body">The recycled handheld desktop and its motherboard</td></tr>
            </table>
'''

RECYCLE = '''
            <h1>Chipset recycling</h1>
            <p class="lead">Every dead laptop has a CPU, memory and a chipset that still work. The board they are soldered to is what died. We are designing a board they can live on instead.</p>
            <h2>How it is meant to work</h2>
            <ol class="body">
              <li>Old laptops come in. We pull the processor, memory and supporting chips and test them.</li>
              <li>Working parts go onto the Sobolak motherboard, a design of ours that accepts several generations of chipsets rather than one.</li>
              <li>The board goes into the handheld desktop: a small box with a screen, a keyboard port, and a desktop operating system. Not a phone. A computer you can hold.</li>
              <li>The rest is recycled properly, not landfilled.</li>
            </ol>
            <h2>Status of the program</h2>
            <p class="body">Not open. We are not taking machines yet, and we will not ask anyone to ship hardware to us until there is a board to put it on. When the program opens, it opens here first.</p>
            <table border="0" cellpadding="8" cellspacing="0" bgcolor="#ffffe1" width="100%" style="border: 1px solid #9b9b6d;">
              <tr><td class="note"><b>Note</b>&nbsp; This is a design-stage project. The motherboard is a schematic, not a product.</td></tr>
            </table>
'''

PRODUCTS = '''
            <h1>Media Library</h1>
            <p class="lead">Everything we are working on, in one list. Nothing on this page can be bought or pre-ordered yet.</p>
            <table border="0" cellpadding="5" cellspacing="1" width="100%" bgcolor="#27385c">
              <tr bgcolor="#1a2744"><th align="left" class="th">Title</th><th align="left" class="th">Type</th><th align="left" class="th">Status</th><th align="left" class="th">Date</th></tr>
              <tr bgcolor="#0d1626"><td class="body">Recycled Handheld Desktop</td><td class="body">Hardware</td><td class="body"><font color="#d9ff6a"><b>Coming soon</b></font></td><td class="body">TBA</td></tr>
              <tr bgcolor="#101b2e"><td class="body">Sobolak Recycle Motherboard</td><td class="body">Hardware</td><td class="body">In design</td><td class="body">TBA</td></tr>
              <tr bgcolor="#0d1626"><td class="body">Chipset Recycling Program</td><td class="body">Service</td><td class="body">Planned</td><td class="body">TBA</td></tr>
              <tr bgcolor="#101b2e"><td class="body">Refurbished Computers</td><td class="body">Store</td><td class="body">Planned</td><td class="body">TBA</td></tr>
            </table>
            <p class="small">Retired products are not listed. They are retired.</p>
'''

STATUS = '''
            <h1>Status</h1>
            <p class="lead">The whole board. Short on purpose.</p>
            <table border="0" cellpadding="5" cellspacing="1" width="100%" bgcolor="#27385c">
              <tr bgcolor="#1a2744"><th align="left" class="th">Station</th><th align="left" class="th">Signal</th><th align="left" class="th">Note</th></tr>
              <tr bgcolor="#0d1626"><td class="body">This website</td><td class="body"><font color="#39e639">&#9679;</font> Online</td><td class="body">Static files. If you can read this, it works.</td></tr>
              <tr bgcolor="#101b2e"><td class="body">Servers</td><td class="body"><font color="#39e639">&#9679;</font> Online</td><td class="body">Our own hardware in Michigan.</td></tr>
              <tr bgcolor="#0d1626"><td class="body">Handheld desktop</td><td class="body"><font color="#f0b019">&#9679;</font> Design</td><td class="body">Idea stage. No 3D model yet.</td></tr>
              <tr bgcolor="#101b2e"><td class="body">Recycle motherboard</td><td class="body"><font color="#f0b019">&#9679;</font> Design</td><td class="body">Schematic stage.</td></tr>
              <tr bgcolor="#0d1626"><td class="body">Recycling intake</td><td class="body"><font color="#777777">&#9679;</font> Closed</td><td class="body">Opens when there is a board to put parts on.</td></tr>
              <tr bgcolor="#101b2e"><td class="body">Staff</td><td class="body">1</td><td class="body">The founder. Replies are slow. They do come.</td></tr>
            </table>
            <p class="small">Last checked: November 2026. Updated by hand.</p>
'''

CONTACT = '''
            <h1>Contact</h1>
            <p class="lead">There is no public inbox yet. Setting one up before there is something to say would just mean a slower reply.</p>
            <ul class="body">
              <li><b>Code and updates:</b> <a href="https://github.com/mrsobolak">github.com/mrsobolak</a></li>
              <li><b>Recycling intake:</b> closed until the motherboard exists. Please do not ship hardware.</li>
              <li><b>Press, partners, parts:</b> check back. When there is an address, it goes here.</li>
            </ul>
            <table border="0" cellpadding="8" cellspacing="0" bgcolor="#ffffe1" width="100%" style="border: 1px solid #9b9b6d;">
              <tr><td class="note"><b>Tip</b>&nbsp; Bookmark this page. Everything new shows up in <a href="index.html" style="color: #0a3fb0;">Now Playing</a> first.</td></tr>
            </table>
'''

SKINS = '''
            <h1>Skin Chooser</h1>
            <p class="lead">One skin is installed: Luna Blue. It is the good one.</p>
            <p class="body">Olive Green and Silver were considered and rejected. A Sobolak Lime skin in the logo colours may show up later. There is no button here because there is nothing for it to do yet, and we would rather not put a button on a page that does nothing.</p>
            <table border="0" cellpadding="6" cellspacing="6">
              <tr>
                <td bgcolor="#0a5fe8" width="120" height="44" align="center" class="body" style="border: 1px solid #ffffff;"><b>Luna Blue</b><br><font size="1">installed</font></td>
                <td bgcolor="#333333" width="120" height="44" align="center" class="small" style="border: 1px solid #555555;">Olive Green<br>not installed</td>
                <td bgcolor="#333333" width="120" height="44" align="center" class="small" style="border: 1px solid #555555;">Silver<br>not installed</td>
                <td bgcolor="#333333" width="120" height="44" align="center" class="small" style="border: 1px solid #555555;">Sobolak Lime<br>someday</td>
              </tr>
            </table>
'''

BODIES = {'index.html': HOME, 'about.html': ABOUT, 'recycle.html': RECYCLE, 'products.html': PRODUCTS, 'status.html': STATUS, 'contact.html': CONTACT, 'skins.html': SKINS}

def nav_html(active):
    out = []
    for fname, nid, label, _, _ in PAGES:
        if nid == active:
            out.append(f'        <img name="{nid}" src="images/nav_{nid}_on.gif" width="110" height="36" alt="current" title="{label}"><br><img src="images/spacer.gif" width="1" height="3" alt=""><br>')
        else:
            out.append(f'        <a href="{fname}" onMouseOver="swap(\'{nid}\',\'over\'); window.status=\'{label}\'; return true;" onMouseOut="swap(\'{nid}\',\'off\'); window.status=\'\'; return true;"><img name="{nid}" src="images/nav_{nid}_off.gif" width="110" height="36" border="0" alt="{label}"></a><br><img src="images/spacer.gif" width="1" height="3" alt=""><br>')
    return '\n'.join(out)

def roadmap_html(fname):
    rows = []
    marked = False
    for title, when, target in ROADMAP:
        cur = (target == fname and not marked)
        if cur: marked = True
        if cur:
            rows.append(f'              <tr bgcolor="#0e2e63"><td class="plcur" nowrap>&#9654; {title}</td><td class="plcur" align="right">{when}</td></tr>')
        else:
            rows.append(f'              <tr><td class="playlist" nowrap><a href="{target}" class="pl">&bull; {title}</a></td><td class="playlist" align="right">{when}</td></tr>')
    return '\n'.join(rows)

for i, (fname, nid, label, title, status) in enumerate(PAGES):
    prev = PAGES[(i - 1) % len(PAGES)][0]
    nxt = PAGES[(i + 1) % len(PAGES)][0]
    seek = int(i / (len(PAGES) - 1) * 100)
    html = HEAD.format(title=title, nav=nav_html(nid), prev=prev, next=nxt)
    html += BODIES[fname]
    html += PLAYLIST_AND_REST.format(roadmap=roadmap_html(fname), status=status, prev=prev, next=nxt, seekpct=max(seek, 1), plh=478 if fname == 'index.html' else 300)
    with open(os.path.join(ROOT, fname), 'w') as fh:
        fh.write(html)
    print('wrote', fname)
