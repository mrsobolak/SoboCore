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

## Y2K set (`logo/y2k`)

Second round, modelled on 1999 to 2002 logo language: wide Eurostile-style caps,
chrome bevels, lime and silver, racing-sticker badges, orbit swooshes, blobby rounded type.

- **Y1 — Chrome wordmark.** SOBOLAK in Michroma (Eurostile Extended feel) with a chrome fill,
  dark outline, and a lime orbit ring swooping through the first O.
- **Y2 — Sticker.** Skewed racing-sticker badge with triple outline, heavy italic SOBOLAK,
  recycle-S emblem in a chrome disc, TECHNOLOGIES on a navy bar.
- **Y3 — Circuit.** SOBOLAK built from PCB traces on a grid, PS2-logo style, with solder pads
  at the open trace ends. Blue and lime versions. Ties to the custom recycled-chipset motherboard.
- **Y4 — Chrome emblem.** A 3D extruded S with a chrome face and lime extrusion inside a tilted chrome
  oval ring, SOBOLAK in wide caps below. Skechers / Xbox lane.
- **Y5 — Bar.** Heavy italic SOBOLAK, black with white inline, on a slanted black bar with a white
  border. Toonami lane. TECHNOLOGIES right-aligned under a lime rule.

Round 1 blob and lime-chrome concepts were dropped. Y1 and Y2 are the current contenders.

Extra faces: Michroma, Audiowide, Comfortaa Bold, Exo 2 Black Italic, Syncopate Bold (all SIL OFL).
Regenerate with `python3 logo/generate_y2k.py` for Y1/Y2 and `python3 logo/generate_round3.py` for Y3 to Y5.
