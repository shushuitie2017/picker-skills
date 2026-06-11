# Render helpers (Remotion engine = audiobooks/enju/remotion-v)

ffmpeg/ffprobe:
`<your-ffmpeg-install>/bin/{ffmpeg,ffprobe} — resolved from PATH by the scripts`

Score for piece <id>:
```
cd audiobooks/enju/remotion-v
D:/GPT-SoVITS/venv/Scripts/python.exe ../../../.claude/skills/evolving-video/scripts/compose_score.py /tmp/<id>.json public/audio/<id>.wav
ffmpeg -y -i public/audio/<id>.wav -codec:a libmp3lame -q:a 2 public/audio/<id>.mp3 && rm public/audio/<id>.wav
```

Assets:
```
python .../scripts/fetch_assets.py /tmp/<id>_manifest.json public/lab/<id> 2560   # eyeball after!
```

Build: new composition `src/lab/<id>/<Name>.tsx` (start from src/scale or src/spark);
embed audio with `<Audio src={staticFile("audio/<id>.mp3")} />`; register in src/Root.tsx
as `<Composition id="lab-<id>" .../>`. Remotion 铁律: frame-driven motion only.

Validate (cheap, BEFORE full render):
```
export REMOTION_LANG=zh   # harmless; some comps read it
MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' npx remotion still lab-<id> out/lab/<id>_fNNN.png --frame=NNN
```
View ≥4 stills across the timeline; fix layout/content BEFORE rendering 1000s of frames.

Full render + verify:
```
MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' npx remotion render lab-<id> out/lab-<id>.mp4 --codec=h264 --crf=18
ffprobe -v error -show_entries format=duration -show_entries stream=codec_type,width,height,channels -of default=noprint_wrappers=1 out/lab-<id>.mp4
ffmpeg -y -ss <t> -i out/lab-<id>.mp4 -frames:v 1 out/lab/<id>_verify.png   # CRITIQUE on real frames, ×2
```
Gotchas (hard-won): `MSYS_NO_PATHCONV=1` is mandatory on Git-Bash or `--base`/paths
mangle; pipe long renders to a log + poll; the mp4 isn't valid until ffprobe reports a
full duration (encode pass runs after frame render); 1080p ≈ fast, true-4K ≈ ~1s/frame.
