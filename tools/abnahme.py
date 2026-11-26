#!/usr/bin/env python3
"""Abnahme FEUERRAUM Neubau: je Storyboard-Panel (konzepte/neu/2-einzelteile.png, 3x3) das Panel groß
+ Seite Laptop (1600x900) + Handy (390x844) an derselben Stelle.
Start: python3 tools/abnahme.py [port] -> abnahme/<n>-{storyboard,desktop,handy}.jpg
Vorlage ASTREIN/KEHRWERK tools/abnahme.py."""
import asyncio, os, sys
from playwright.async_api import async_playwright
from PIL import Image
PORT = sys.argv[1] if len(sys.argv) > 1 else '4460'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'abnahme'); os.makedirs(OUT, exist_ok=True)
SB = 'konzepte/neu/2-einzelteile.png'
# (Name, Abschnitt-id, Anteil, Modus) Modus 'stage' = sticky Bühne (Anteil des Scrollwegs), sonst Anteil der Höhe
PANELS = [('Ein Ofen. Sieben Schichten.', 'start', .0, 'stage'), ('Explosionsansicht', 'start', .86, 'stage'),
          ('Ein Ofen. Ihr Stil.', 'stil', .05, ''), ('Brennraum / Sekundärluft', 'feuer', .05, ''),
          ('Stein speichert Zeit.', 'speicher', .0, ''), ('Passt er rein?', 'platz', .05, ''),
          ('Welcher Ofen passt zu Ihnen?', 'rechner', .02, ''), ('Wir bauen ihn wieder zusammen.', 'handwerk', .0, ''),
          ('Echte Momente. Lange Wärme.', 'ausstellung', .0, '')]


async def main():
    im = Image.open(os.path.join(ROOT, SB)).convert('RGB'); W, H = im.size; pw, ph = W / 3, H / 3
    for i in range(9):
        r, c = divmod(i, 3); im.crop((int(c * pw), int(r * ph), int((c + 1) * pw), int((r + 1) * ph))).save(f'{OUT}/{i+1}-storyboard.jpg', quality=88)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for tag, w, h, mob in (('desktop', 1600, 900, False), ('handy', 390, 844, True)):
            pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2 if mob else 1, is_mobile=mob, has_touch=mob)
            await pg.goto(f'http://localhost:{PORT}/', wait_until='networkidle'); await pg.wait_for_timeout(2500)
            for i, (name, sid, t, mode) in enumerate(PANELS):
                if mode == 'stage':
                    js = f"(()=>{{const s=document.getElementById('{sid}');scrollTo(0,s.offsetTop+(s.offsetHeight-innerHeight)*{t})}})()"
                else:
                    js = f"(()=>{{const s=document.getElementById('{sid}');scrollTo(0,s.getBoundingClientRect().top+scrollY+s.offsetHeight*{t})}})()"
                await pg.evaluate(js); await pg.wait_for_timeout(2200)
                await pg.screenshot(path=f'{OUT}/{i+1}-{tag}.jpg', type='jpeg', quality=82)
            await pg.close()
        await b.close()
    print('ok', OUT)

asyncio.run(main())
