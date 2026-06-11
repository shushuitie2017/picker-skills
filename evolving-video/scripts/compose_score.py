# -*- coding: utf-8 -*-
"""Parametric bespoke score generator for evolving-video.
Edit CONFIG (or pass a JSON path as argv[1]) per piece, then:
  D:/GPT-SoVITS/venv/Scripts/python.exe compose_score.py [config.json] [out.wav]
Produces a stereo wav: evolving detuned pads + bell motif + sub-booms & risers on
each cut + pseudo-reverb. Encode to mp3 with ffmpeg afterwards. (numpy only.)
Proven recipe — see TECHNIQUES.md."""
import sys, json, wave, numpy as np

CONFIG = {
    "sr": 44100,
    "total": 84.0,
    "cuts": [11, 22, 34, 44, 55, 67],        # impact times (s) — MUST match the edit's cuts
    # sections: [start, dur, [chord freqs Hz], gain]; overlap → crossfade
    "sections": [
        [0,  13, [110.00, 164.81, 220.00, 261.63, 329.63], 0.16],
        [11, 13, [87.31, 130.81, 220.00, 261.63, 349.23], 0.17],
        [22, 14, [73.42, 110.00, 174.61, 293.66, 440.00], 0.16],
        [34, 12, [65.41, 98.00, 130.81, 164.81, 196.00], 0.18],
        [44, 13, [98.00, 146.83, 196.00, 246.94, 293.66], 0.18],
        [55, 14, [65.41, 130.81, 164.81, 196.00, 261.63, 329.63], 0.22],
        [67, 17, [55.00, 110.00, 164.81, 261.63], 0.17],
    ],
    "motif": [659.25, 523.25, 392.00],        # bell phrase (Hz)
    "motif_starts": [2.5, 13.5, 24.5, 35.5, 46, 57],
    "shimmer_window": [55, 74],               # bright high stack window (climax)
    "out": "score.wav",
}
if len(sys.argv) > 1 and sys.argv[1].endswith(".json"):
    CONFIG.update(json.load(open(sys.argv[1], encoding="utf-8")))
OUT = sys.argv[2] if len(sys.argv) > 2 else CONFIG["out"]

SR = CONFIG["sr"]; TOTAL = CONFIG["total"]; cuts = CONFIG["cuts"]
N = int(TOTAL * SR); t = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)

def env_section(start, dur, fade=2.2):
    e = np.zeros(N); s0 = int(start*SR); s1 = min(N, int((start+dur)*SR))
    seg = np.ones(s1-s0); fn = min(int(fade*SR), (s1-s0)//2)
    seg[:fn] *= np.linspace(0,1,fn)**1.5; seg[-fn:] *= np.linspace(1,0,fn)**1.5
    e[s0:s1] = seg; return e

def voice(freq, amp, pan):
    sig = sum(np.sin(2*np.pi*freq*d*t) for d in (0.997,1.0,1.003))/3.0
    sig += 0.18*np.sin(2*np.pi*2*freq*t)
    sig *= 1 + 0.10*np.sin(2*np.pi*0.06*t + freq); sig *= amp
    return sig*(1-pan), sig*pan

for st,du,freqs,g in CONFIG["sections"]:
    e = env_section(st,du)
    for j,f in enumerate(freqs):
        pan = j/max(1,len(freqs)-1); vl,vr = voice(f, g/len(freqs), pan)
        L += vl*e; R += vr*e

def bell(at,freq,amp=0.13,dec=2.4,pan=0.5):
    n0=int(at*SR)
    if n0>=N: return
    tt=np.arange(N-n0)/SR; env=np.exp(-tt/dec)
    s=(np.sin(2*np.pi*freq*tt)+0.4*np.sin(2*np.pi*2*freq*tt))*env*amp
    L[n0:]+=s*(1-pan); R[n0:]+=s*pan
for k,st in enumerate(CONFIG["motif_starts"]):
    for m,f in enumerate(CONFIG["motif"]):
        bell(st+m*0.9, f, amp=0.12+0.02*k, pan=0.35+0.3*(m%2))

def boom(at,amp=0.5,dec=2.6):
    n0=int(at*SR); tt=np.arange(N-n0)/SR; env=np.exp(-tt/dec)
    s=(np.sin(2*np.pi*44*tt)+0.5*np.sin(2*np.pi*88*tt))*env*amp
    a=int(0.012*SR); s[:a]*=np.linspace(0,1,a); L[n0:]+=s; R[n0:]+=s
def riser(at_end,dur=2.6,amp=0.13):
    n1=int(at_end*SR); n0=max(0,n1-int(dur*SR)); tt=np.arange(n1-n0)/SR
    sweep=np.sin(2*np.pi*(120+780*(tt/dur)**2)*tt)
    nz=np.cumsum(np.random.default_rng(7).standard_normal(n1-n0)); nz/=np.max(np.abs(nz))+1e-9
    env=(tt/dur)**2.2*amp; s=(0.6*sweep+0.4*nz)*env; L[n0:n1]+=s; R[n0:n1]+=s
for c in cuts:
    riser(c); boom(c, amp=0.62 if c==cuts[-1] else 0.5)
boom(0.2, amp=0.34, dec=3.0)

w0,w1 = CONFIG["shimmer_window"]
sh=sum(np.sin(2*np.pi*f*t) for f in (523.25,659.25,783.99,1046.5))/4
shimmer=np.clip((t-w0)/7,0,1)*np.clip((w1-t)/7,0,1)
L+=sh*shimmer*0.05; R+=sh*shimmer*0.05

def reverb(buf):
    out=buf.copy()
    for ms,g in ((83,.28),(127,.2),(191,.14),(50,.18)):
        d=int(ms/1000*SR); out[d:]+=buf[:-d]*g
    return out
L=reverb(L); R=reverb(R)
L=np.tanh(L*1.1); R=np.tanh(R*1.1)
pk=max(np.max(np.abs(L)),np.max(np.abs(R)),1e-9); L*=0.89/pk; R*=0.89/pk
fi=int(1.5*SR); fo=int(4.5*SR)
for ch in (L,R):
    ch[:fi]*=np.linspace(0,1,fi); ch[-fo:]*=np.linspace(1,0,fo)**1.4
pcm=(np.stack([L,R],1)*32767).astype(np.int16)
with wave.open(OUT,"wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print(f"wrote {OUT}: {TOTAL}s, cuts {cuts}")
