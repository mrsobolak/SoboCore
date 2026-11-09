# Sobolak Technologies — brand assets

Logo concepts for the recycled-hardware era. XP/Vista-era gloss, drawn as plain vector SVG.
Wordmark text is converted to paths, so the SVGs need no fonts installed.

## Concepts

- **A — Orb.** Glossy green orb with two chasing arrows forming an S (recycle motif).
  `A-mark`, `A-orb-horizontal`, `A-orb-horizontal-dark`, `A-orb-stacked`.
- **B — Chip tile.** Vista-style glass tile, a CPU package with a leaf sprouting from it.
  `B-mark`, `B-chip-horizontal`, `B-chip-horizontal-dark`.
- **C — Wordmark.** SOBOLAK in caps with the second O replaced by the small orb.
  `C-wordmark`, `C-wordmark-dark`.

Each SVG has a matching 2x transparent PNG. `contact-sheet.png` shows everything at once.

## Type

- Sobolak: Libre Franklin ExtraBold (open-source cousin of Franklin Gothic, the Windows XP brand face)
- TECHNOLOGIES: Libre Franklin Medium, letter-spaced
- Font files are in `../fonts` (SIL Open Font License)

## Colours

- XP green: `#b9f08a` → `#5fc23f` → `#2a8f2a` → `#1b6a1e`
- Ink blue: `#2b4f8f` → `#15305e`
- Ink green: `#3f9a2e` → `#1f6a1f`
- Vista glass: `#5a7fb8` → `#20406f` → `#0d2246`

## Regenerating

```
pip install fonttools
python3 logo/generate.py
```

## Final logo (`logo/final`)

**Chosen:** the Y2K chrome wordmark with the lime orbit ring. SOBOLAK in Michroma with a
horizon-line chrome fill, dark outline and pale inline, a lime chrome ring orbiting the first O
(back half behind the letters, front half in front), TECHNOLOGIES letter-spaced in lime below.

Files:

- `sobolak-logo-dark` — primary, on navy `#0d1620`. Use this one by default.
- `sobolak-logo-dark-transparent` — same artwork, no background, for dark surfaces.
- `sobolak-logo-light` / `-light-transparent` — for white or pale surfaces.
- `sobolak-logo-onecolour-white` / `-black` — flat single colour for embossing, print, laser etching.
- `sobolak-icon-*` — the orbit O on its own, as app icon and favicon. Same four colour modes.
- `favicon/icon-{16..512}.png` — rendered from the dark icon.

Each SVG has a matching 2x PNG. Regenerate with `python3 logo/generate_final.py`.

Colours: navy `#0d1620`, lime `#d9ff6a` (text) and `#c6f14a` to `#3a7a0c` (ring),
chrome `#ffffff` / `#cfd6de` / `#6b7684` / `#e6ebf0`, outline `#000` on dark or `#0b1b3c` on light.

## Y2K set (`logo/y2k`) — earlier rounds

Y1 chrome wordmark (became the final) and Y2 racing sticker are kept here.
Rounds with the blob, lime chrome, circuit, chrome emblem and bar concepts were dropped.

Extra faces: Michroma, Audiowide, Comfortaa Bold, Exo 2 Black Italic, Syncopate Bold (all SIL OFL).
Regenerate with `python3 logo/generate_y2k.py` for Y1/Y2 and `python3 logo/generate_round3.py` for Y3 to Y5.
