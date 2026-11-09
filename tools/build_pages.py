# Stamps out the static pages. Run: python3 tools/build_pages.py
# Every page is a full HTML 4.01 file with the player chrome built from tables and sliced GIFs.
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

PAGES = [
  # file, nav id, nav label, window title, status text
  ('index.html', 'nowplaying', 'Now Playing', 'Sobolak Technologies - The Sobolak Laptop, coming 2029', 'Album: The Sobolak Laptop &middot; coming 2029'),
  ('about.html', 'guide',      'Media Guide', 'Who we are - Sobolak Technologies',                     'Media Guide &middot; Who we are'),
]
NAV_ALT = {'nowplaying':'Now Playing','guide':'Media Guide','copycd':'Copy from CD','library':'Media Library','radio':'Radio Tuner','device':'Copy to CD or Device','skins':'Skin Chooser'}

ROADMAP = [
  ('The idea', '2026', 'index.html'),
  ('Motherboard design', 'next', 'index.html'),
  ('First prototype', 'then', 'index.html'),
  ('Beta units', 'later', 'index.html'),
  ('The Sobolak Laptop', '2029~', 'index.html'),
]

HEAD = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>{title}</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="description" content="Sobolak Technologies, Michigan. The Sobolak Laptop: a handheld desktop with desktop power, built from recycled parts on our own motherboard. Coming 2029.">
<meta name="keywords" content="Sobolak Technologies, Sobolak Laptop, handheld desktop, recycled computers, Michigan, custom motherboard, 2029">
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
    <img src="images/spacer.gif" width="6" height="1" alt=""><a href="index.html" class="menu"><u>F</u>ile</a><a href="about.html" class="menu"><u>V</u>iew</a><a href="index.html" class="menu"><u>P</u>lay</a><a href="about.html" class="menu"><u>T</u>ools</a><a href="about.html" class="menu"><u>H</u>elp</a>
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
            <span class="plhead">&#9662; The Sobolak Laptop</span><br>
            <table border="0" cellpadding="1" cellspacing="0" width="100%" style="margin-left: 8px;">
{roadmap}
            </table>
          </td>
        </tr>
        </table>
        <div align="right" class="playlist" style="padding-top: 4px;">Total Time: 2029~</div>
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
    <a href="index.html">The Sobolak Laptop</a> | <a href="about.html">Who we are</a> | <a href="https://github.com/mrsobolak">GitHub</a><br>
    <img src="images/spacer.gif" width="1" height="6" alt=""><br>
    Sobolak Technologies &middot; Michigan, United States &middot; Last updated November 9, 2026<br>
    Built in Michigan from recycled parts. Best viewed at 1024&times;768 with the speakers on.
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
            <span class="track">The Sobolak Laptop (coming 2029~)</span><br>
            <img src="images/spacer.gif" width="1" height="6" alt=""><br>
            <table width="100%" border="0" cellpadding="0" cellspacing="0" style="border: 1px solid #1b2a4a;" bgcolor="#000000">
            <tr><td align="center"><img src="images/vis.gif" width="420" height="230" alt="Sobolak Technologies"></td></tr>
            </table>
            <img src="images/spacer.gif" width="1" height="8" alt=""><br>
            <table width="100%" border="0" cellpadding="10" cellspacing="0" bgcolor="#060f22" style="border: 1px solid #2c4a8a;">
            <tr><td class="body">
              <span class="lead"><b>Desktop power at your fingertips. Recycled, saving the planet.</b></span><br><br>
              The Sobolak Laptop is a handheld desktop. It is thick and heavy on purpose. Inside is a full-power desktop processor and memory, pulled from recycled desktop computers and put onto a motherboard we design ourselves, in a case we make ourselves. Expect about three to four hours on the battery, because it runs real desktop chips.<br><br>
              It is either ours or it is not ours. No rebadged boards, no bought-in modules. It boots to a Sobolak screen, ships with Windows 10, and you can put whatever you like on it after that.<br><br>
              <b>Where it stands:</b> it is an idea we are serious about. The board design has not started. We are aiming for 2029, give or take, and we will not put a fake date on it to look busy.
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
            <h1>Who we are</h1>
            <p class="lead">Sobolak Technologies is an independent technology company in Michigan, United States, founded in 2024. One person, no investors, no outside money.</p>
            <p class="body">Today we refurbish and resell computers, build gaming PCs, and fix laptops. That work pays for the thing we actually want to make: the <a href="index.html">Sobolak Laptop</a>, a handheld desktop built from recycled parts on our own motherboard, due around 2029.</p>
            <h2>What we believe</h2>
            <ul class="body">
              <li><b>It is either ours or it is not ours.</b> We design the board and make the case. Nothing rebadged.</li>
              <li><b>Nothing is scrap until it fails a test.</b> A ten-year-old desktop CPU still does what it did on day one. We put it back to work.</li>
              <li><b>Big and heavy is fine.</b> Power first. The battery is sized to match, not the other way round.</li>
              <li><b>Screws, not glue.</b> Ribbon cables, replaceable parts, and a machine you can open.</li>
              <li><b>Say so.</b> If something is an idea, we call it an idea. No fake launch dates.</li>
            </ul>
            <table border="0" cellpadding="4" cellspacing="0" class="props" width="90%">
              <tr><td class="key" width="34%">Location</td><td class="body">Michigan, United States</td></tr>
              <tr><td class="key">Founded</td><td class="body">2024</td></tr>
              <tr><td class="key">Type</td><td class="body">Independent, privately held</td></tr>
              <tr><td class="key">Investors</td><td class="body">None</td></tr>
              <tr><td class="key">Staff</td><td class="body">One, the founder</td></tr>
              <tr><td class="key">Doing now</td><td class="body">Refurbishing, resale, repair, gaming PC builds</td></tr>
              <tr><td class="key">Building next</td><td class="body">The Sobolak Laptop, coming 2029~</td></tr>
              <tr><td class="key">Code</td><td class="body"><a href="https://github.com/mrsobolak">github.com/mrsobolak</a></td></tr>
            </table>
'''

BODIES = {'index.html': HOME, 'about.html': ABOUT}

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
    html += PLAYLIST_AND_REST.format(roadmap=roadmap_html(fname), status=status, prev=prev, next=nxt, seekpct=max(seek, 1), plh=520 if fname == 'index.html' else 420)
    with open(os.path.join(ROOT, fname), 'w') as fh:
        fh.write(html)
    print('wrote', fname)
