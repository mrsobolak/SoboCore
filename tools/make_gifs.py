# Turns the rendered frames into an animated GIF and the buttons into GIFs. Run: python3 tools/make_gifs.py
import glob, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, '..', 'images')

frames = [Image.open(f).convert('RGB').quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
          for f in sorted(glob.glob(os.path.join(IMG, 'frames', 'f*.png')))]
frames[0].save(os.path.join(IMG, 'vis.gif'), save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=True)
print('vis.gif', os.path.getsize(os.path.join(IMG, 'vis.gif')) // 1024, 'KB')

for f in glob.glob(os.path.join(IMG, 'frames', '*.png')):
    os.remove(f)
os.rmdir(os.path.join(IMG, 'frames'))

# buttons and chrome: GIF with transparency where the PNG had alpha
for f in glob.glob(os.path.join(IMG, '*.png')):
    im = Image.open(f)
    base = os.path.splitext(os.path.basename(f))[0]
    if im.mode == 'RGBA' and im.getextrema()[3][0] < 255:
        alpha = im.split()[3]
        rgb = im.convert('RGB').quantize(colors=255, method=Image.Quantize.MEDIANCUT)
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
        rgb.paste(255, mask)
        rgb.info['transparency'] = 255
        rgb.save(os.path.join(IMG, base + '.gif'), transparency=255, optimize=True)
    else:
        im.convert('RGB').quantize(colors=256).save(os.path.join(IMG, base + '.gif'), optimize=True)
    os.remove(f)
print('converted', len(glob.glob(os.path.join(IMG, '*.gif'))), 'gifs')
