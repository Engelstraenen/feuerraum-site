#!/usr/bin/env python3
"""Holt fertige sjinn-Bilder und baut die Web-Bilder.

Start: python3 tools/assets.py [urls.json]
  urls.json = {"FRA-01": "https://…jpg", …} (aus SB.harvest2() im sjinn-Tab)
Quelle:  assets-roh/4k/<name>.jpg (4K von sjinn, 5504x3072 bzw. 3:4)
Ziel:    site/assets/img/<name>.webp (3840 breit) + <name>-m.webp (1800 breit)
         x-ofen: Magenta freistellen -> PNG mit Alpha (1100 / 600 breit)
Schreibt site/assets/js/img.js (FR_IMG Maße, FR_VID Videos) + version.txt und setzt ?v= in index.html.
Cache: unveränderte Quellen werden nicht neu geöffnet (Dropbox lädt sonst jedes Mal nach).
"""
import json
import os
import re
import subprocess
import sys
import time

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "assets-roh", "4k")
OUT = os.path.join(ROOT, "site", "assets", "img")
CACHE = os.path.join(ROOT, "tools", "img_cache.json")
NAMES = {"FRA-01": "f1-kalt", "FRA-02": "f1-warm", "FRA-03": "s-showroom", "FRA-04": "o-kaminofen", "FRA-05": "o-kamineinsatz",
         "FRA-06": "o-pelletofen", "FRA-07": "o-kachelofen", "FRA-08": "o-gaskamin", "FRA-09": "q-altbau", "FRA-10": "q-neubau",
         "FRA-11": "q-wohnung", "FRA-12": "r-ofen", "FRA-13": "c-check", "FRA-14": "p-sommer", "FRA-15": "k-azubi",
         "FRA-16": "e-ecke", "FRA-17": "b-beratung", "FRA-18": "x-ofen"}
os.makedirs(RAW, exist_ok=True)
os.makedirs(OUT, exist_ok=True)


def fetch(urls):
    for k, u in urls.items():
        n = NAMES.get(k)
        if not n:
            continue
        dst = os.path.join(RAW, n + ".jpg")
        if os.path.exists(dst):
            continue
        subprocess.check_call(["curl", "-sSf", "-o", dst, u])
        print("geladen", k, n)


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


def main():
    if len(sys.argv) > 1:
        fetch(json.load(open(sys.argv[1])))
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    info = {}
    for fn in sorted(os.listdir(RAW)):
        if not fn.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            continue
        name, p = os.path.splitext(fn)[0], os.path.join(RAW, fn)
        mt = os.path.getmtime(p)
        c = cache.get(name)
        if c and c["mt"] == mt and os.path.exists(os.path.join(OUT, name + ("-m.png" if c.get("png") else "-m.webp"))):
            info[name] = {k: v for k, v in c.items() if k != "mt"}
            continue
        im = Image.open(p)
        if name == "x-ofen":
            cut = key_magenta(im)
            for suf, w in (("", 1100), ("-m", 600)):
                cut.resize((w, round(cut.height * w / cut.width)), Image.LANCZOS).save(os.path.join(OUT, name + suf + ".png"), optimize=True)
            info[name] = {"w": cut.width, "h": cut.height, "png": True}
        else:
            rgb = im.convert("RGB")
            for suf, w, q in (("", 3840, 82), ("-m", 1800, 78)):
                r = rgb.resize((w, round(rgb.height * w / rgb.width)), Image.LANCZOS) if rgb.width > w else rgb
                r.save(os.path.join(OUT, name + suf + ".webp"), "WEBP", quality=q, method=6)
            info[name] = {"w": im.width, "h": im.height}
        cache[name] = dict(info[name], mt=mt)
        print("ok", name, im.size)
    json.dump(cache, open(CACHE, "w"))
    vp = os.path.join(ROOT, "tools", "vid.json")
    vid = json.load(open(vp)) if os.path.exists(vp) else {}
    v = int(time.time())
    info["_v"] = v
    vid["_v"] = v
    open(os.path.join(ROOT, "site", "assets", "js", "img.js"), "w").write(
        "window.FR_IMG=%s;\nwindow.FR_VID=%s;\n" % (json.dumps(info), json.dumps(vid)))
    open(os.path.join(ROOT, "site", "version.txt"), "w").write(str(v))
    ip = os.path.join(ROOT, "site", "index.html")
    h = open(ip).read()
    h = re.sub(r"v!=='\d+'", "v!=='%d'" % v, h)
    h = re.sub(r"\?v=\d+\"", '?v=%d"' % v, h)
    open(ip, "w").write(h)
    print("img.js geschrieben, Stand", v, "Bilder:", len(info) - 1)


if __name__ == "__main__":
    main()
