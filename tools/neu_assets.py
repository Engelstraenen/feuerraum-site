#!/usr/bin/env python3
"""Neubau 26.11.2026: Dreamina-/sjinn-Bilder einsortieren, nachschärfen, als WebP ausgeben.

Start: python3 tools/neu_assets.py
1) holt ~/Downloads/dreamina-*-FEnn ….png  -> assets-roh/neu/FEnn.png (neueste je ID)
   und assets-roh/neu/FEnn-4k.(png|jpg) hat Vorrang (sjinn 4K)
2) Unsharp-Mask (radius 1.6, 70 %, threshold 2), Original bleibt unverändert
3) site/assets/img/<name>.webp (volle Breite, max 3840) + <name>-m.webp (1280)
   FE16: Magenta freistellen -> ofen-frei.png
Schreibt tools/schaerfe_neu.json (Laplace-Varianz vorher/nachher).
"""
import glob, json, os, re, shutil
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "assets-roh", "neu")
OUT = os.path.join(ROOT, "site", "assets", "img")
NAMES = {"FE01": "hero", "FE02": "explode", "FE03": "stil", "FE04": "feuer", "FE05": "speicher", "FE06": "raum",
         "FE07": "werkstatt", "FE08": "abend", "FE09": "kachelofen", "FE10": "grundofen-bau", "FE11": "abnahme",
         "FE12": "ausstellung", "FE13": "brennstoffe", "FE14": "glas", "FE15": "rohr", "FE16": "ofen-frei", "FE17": "mat-speckstein", "FE18": "mat-keramik", "FE19": "mat-stahl", "FE20": "mat-putz",
         "FE21": "schritt-beratung", "FE22": "schritt-aufmass", "FE23": "schritt-abstimmung", "FE24": "schritt-feuer"}
os.makedirs(RAW, exist_ok=True); os.makedirs(OUT, exist_ok=True)


def lap(im):
    a = np.asarray(im.convert("L").resize((1280, int(1280 * im.height / im.width))), dtype=np.float32)
    l = a[1:-1, 1:-1] * 4 - a[:-2, 1:-1] - a[2:, 1:-1] - a[1:-1, :-2] - a[1:-1, 2:]
    return float(l.var())


def key_magenta(im):
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mag = np.clip(((r + b) / 2 - g - 60) / 80, 0, 1)
    alpha = (1 - mag) * 255
    spill = np.clip(((r + b) / 2 - g) / 255, 0, 1) * (alpha < 250)
    rgba = np.dstack([np.clip(r - spill * 60, 0, 255), g, np.clip(b - spill * 60, 0, 255), alpha]).astype(np.uint8)
    out = Image.fromarray(rgba, "RGBA")
    bbox = out.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()
    return out.crop(bbox) if bbox else out


def holen():
    for f in sorted(glob.glob(os.path.expanduser("~/Downloads/dreamina-*.png")), key=os.path.getmtime):
        m = re.search(r"-(FE\d\d) ", os.path.basename(f))
        if m:
            shutil.move(f, os.path.join(RAW, m.group(1) + ".png")); print("geholt", m.group(1))


def main():
    holen()
    log = {}
    for fid, name in NAMES.items():
        src = None
        for c in (f"{fid}-4k.png", f"{fid}-4k.jpg", f"{fid}.png"):
            if os.path.exists(os.path.join(RAW, c)):
                src = os.path.join(RAW, c); break
        if not src:
            continue
        dst = os.path.join(OUT, name + (".png" if fid == "FE16" else ".webp"))
        if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
            continue
        im = Image.open(src).convert("RGB")
        if fid == "FE16":
            k = key_magenta(im).filter(ImageFilter.UnsharpMask(1.2, 50, 2))
            k.thumbnail((900, 1600)); k.save(dst, optimize=True); print("frei", name, k.size); continue
        v0 = lap(im)
        sh = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2))
        v1 = lap(sh)
        big = sh.copy(); big.thumbnail((3840, 3840), Image.LANCZOS)
        big.save(dst, "WEBP", quality=84, method=6)
        sm = sh.copy(); sm.thumbnail((1280, 1280), Image.LANCZOS)
        sm.save(os.path.join(OUT, name + "-m.webp"), "WEBP", quality=80, method=6)
        log[name] = {"px": im.size, "lap_vorher": round(v0), "lap_nachher": round(v1)}
        print(name, im.size, round(v0), "->", round(v1))
    p = os.path.join(ROOT, "tools", "schaerfe_neu.json")
    old = json.load(open(p)) if os.path.exists(p) else {}
    old.update(log); json.dump(old, open(p, "w"), indent=1)


if __name__ == "__main__":
    main()
