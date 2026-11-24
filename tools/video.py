#!/usr/bin/env python3
"""Baut die Scroll-Videos für ein Filmkapitel (nie hochskalieren, nie verkleinern am Desktop).

Start: python3 tools/video.py <roh.mp4> <kapitel> <datei>
  kapitel = Section-id (flamme | oefen | karriere)  -> Schlüssel in FR_VID
  datei   = Name unter site/assets/vid/ (flamme | showroom | karriere)
Ziel:  <datei>.mp4    Desktop: volle Quellauflösung, All-Intra, max. 30 fps
       <datei>-p.mp4  Handy hochkant: Mittelausschnitt 3:4 in voller Quellhöhe
       <datei>-m.mp4  Handy quer: ganzes Bild, max. 1280 breit
All-Intra = jedes Bild ein Keyframe, damit Scrollen vor und zurück ohne Ruckeln springt.
Trägt das Kapitel in tools/vid.json ein; danach `python3 tools/assets.py` für img.js.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "assets", "vid")
os.makedirs(OUT, exist_ok=True)


def size(src):
    o = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0",
                                 "-show_entries", "stream=width,height", "-of", "csv=p=0", src]).decode()
    return tuple(int(x) for x in o.strip().split(",")[:2])


def enc(src, dst, vf, crf):
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", src, "-an",
                           "-vf", vf + ",fps=30,format=yuv420p",
                           "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-tune", "film",
                           "-g", "1", "-keyint_min", "1", "-sc_threshold", "0",
                           "-movflags", "+faststart", dst])
    print("ok", os.path.basename(dst), os.path.getsize(dst) // 1024, "KB")


def main():
    src, key, name = sys.argv[1], sys.argv[2], sys.argv[3]
    w, h = size(src)
    pw = (h * 3 // 4) // 2 * 2
    enc(src, os.path.join(OUT, name + ".mp4"), "scale=%d:%d" % (w // 2 * 2, h // 2 * 2), 20)
    enc(src, os.path.join(OUT, name + "-p.mp4"), "crop=%d:%d:(iw-%d)/2:0" % (pw, h // 2 * 2, pw), 21)
    mw = min(1280, w) // 2 * 2
    enc(src, os.path.join(OUT, name + "-m.mp4"), "scale=%d:-2" % mw, 22)
    vp = os.path.join(ROOT, "tools", "vid.json")
    vid = json.load(open(vp)) if os.path.exists(vp) else {}
    vid[key] = {"src": name, "w": w, "h": h}
    json.dump(vid, open(vp, "w"), indent=1)


if __name__ == "__main__":
    main()
