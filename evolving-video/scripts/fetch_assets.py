# -*- coding: utf-8 -*-
"""Download + verify + downscale public-domain assets for a piece.
Usage:  python fetch_assets.py manifest.json  outdir  [maxpx]
manifest.json = [{"name":"01_x.jpg","url":"https://...","license":"PD/NASA"}, ...]
Verifies each file is real image bytes (not an HTML error page) and decodes, then
downscales >maxpx (default 2560) with ffmpeg/lanczos. Prints a report; NON-zero exit
if any asset failed so the agent knows to route around it.
IMPORTANT: downloading is not enough — the agent must still EYEBALL each image for
correct CONTENT (a valid jpg can be the wrong nebula — see LEDGER)."""
import sys, json, os, subprocess, urllib.request

import shutil as _sh
FF = _sh.which("ffmpeg") or "ffmpeg"; FP = _sh.which("ffprobe") or "ffprobe"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 evolving-video/1.0"

manifest = json.load(open(sys.argv[1], encoding="utf-8"))
outdir = sys.argv[2]; maxpx = int(sys.argv[3]) if len(sys.argv) > 3 else 2560
os.makedirs(outdir, exist_ok=True)

def dims(p):
    try:
        return subprocess.check_output([FP,"-v","error","-select_streams","v:0",
            "-show_entries","stream=width,height","-of","csv=s=x:p=0",p]).decode().strip()
    except Exception: return ""

fails = []
for a in manifest:
    name, url = a["name"], a["url"]; dst = os.path.join(outdir, name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        data = urllib.request.urlopen(req, timeout=120).read()
        if len(data) < 4000 or data[:15].lstrip()[:1] in (b"<", b"{"):
            raise ValueError(f"looks like an error page ({len(data)}B)")
        open(dst, "wb").write(data)
    except Exception as e:
        print(f"  ✗ {name}: {e}"); fails.append(name); continue
    d = dims(dst)
    if not d:
        print(f"  ✗ {name}: does not decode"); fails.append(name); os.remove(dst); continue
    # downscale if large
    w = int(d.split("x")[0]); h = int(d.split("x")[1])
    if max(w, h) > maxpx:
        tmp = dst + ".s.jpg" if dst.lower().endswith((".jpg",".jpeg")) else dst + ".s.png"
        subprocess.run([FF,"-y","-loglevel","error","-i",dst,"-vf",
            f"scale='min({maxpx},iw)':'min({maxpx},ih)':force_original_aspect_ratio=decrease:flags=lanczos",
            "-q:v","3",tmp], check=True, stdin=subprocess.DEVNULL)
        os.replace(tmp, dst); d = dims(dst)
    print(f"  ✓ {name}: {d}  ({len(data)//1024}KB→{os.path.getsize(dst)//1024}KB)  [{a.get('license','?')}]  {url}")

print(f"\n{len(manifest)-len(fails)}/{len(manifest)} ok" + (f"  FAILED: {fails}" if fails else ""))
print("⚠️  Now EYEBALL each image (remotion still / open) — a valid file can be the wrong content.")
sys.exit(1 if fails else 0)
