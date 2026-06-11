#!/usr/bin/env python3
"""从每步口播 mp3 实测时长生成 timeline.json（音频锁定 = 音画同步的根本）。

timeline.json[i] = 第 i 步音频毫秒 + trail(默认120ms)，顺序同 segments.json。
timeline.ts 再把毫秒 round(ms/1000*fps) 转帧累加。与网页版 audio.onended+trailMs 一致。

用法:
  python gen_timeline.py <remotion_dir> [--lang zh] [--trail 120] [--out PATH]

多语言：每种语言音频时长不同，需各自一份 timeline。约定 timeline.<lang>.json：
  python gen_timeline.py <remotion_dir> --lang en --out <remotion_dir>/src/timeline.en.json

约定目录（实样 audiobooks/sanen/remotion/）:
  <remotion_dir>/src/segments.json           # [{chapter, step, text, audio?}, ...] 按播放顺序
  <remotion_dir>/public/audio/<lang>/<chapter>/<step>.mp3
输出:
  <remotion_dir>/src/timeline.json           # [ms, ms, ...]

若 segments.json 不存在，可改用 --from-chapters 指定章节顺序与步数(见 --help 注释)。
"""
import argparse
import json
import os
import shutil
import subprocess
import sys


def find_ffprobe() -> str:
    p = shutil.which("ffprobe")
    if p:
        return p
    # Windows WinGet 安装路径兜底
    import glob
    base = os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Packages")
    hits = glob.glob(os.path.join(base, "**", "ffprobe.exe"), recursive=True)
    if hits:
        return hits[0]
    sys.exit("ffprobe 未找到：请安装 ffmpeg 或把 ffprobe 加入 PATH")


def dur_ms(ffprobe: str, path: str) -> float:
    out = subprocess.check_output(
        [ffprobe, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        text=True,
    ).strip()
    return float(out) * 1000.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("remotion_dir")
    ap.add_argument("--lang", default="zh")
    ap.add_argument("--trail", type=int, default=120, help="每步音频后补的 trail 毫秒")
    ap.add_argument("--out", default=None, help="输出路径(默认 <remotion_dir>/src/timeline.json)")
    args = ap.parse_args()

    rdir = os.path.abspath(args.remotion_dir)
    seg_path = os.path.join(rdir, "src", "segments.json")
    if not os.path.isfile(seg_path):
        sys.exit(f"找不到 {seg_path}（需要按播放顺序的 [{{chapter,step}}] 数组）")
    segs = json.load(open(seg_path, encoding="utf-8"))

    ffprobe = find_ffprobe()
    audio_base = os.path.join(rdir, "public", "audio", args.lang)
    ms_list, total = [], 0.0
    for s in segs:
        mp3 = os.path.join(audio_base, s["chapter"], f"{s['step']}.mp3")
        if not os.path.isfile(mp3):
            sys.exit(f"缺音频: {mp3}")
        d = dur_ms(ffprobe, mp3)
        ms = round(d + args.trail)
        ms_list.append(ms)
        total += ms
        print(f"  {s['chapter']}/{s['step']:>2}  {d:7.0f}ms + {args.trail} = {ms}ms")

    out_path = args.out or os.path.join(rdir, "src", "timeline.json")
    json.dump(ms_list, open(out_path, "w", encoding="utf-8"))
    print(f"\n写出 {out_path}：{len(ms_list)} 步，总 {total/1000:.2f}s")


if __name__ == "__main__":
    main()
