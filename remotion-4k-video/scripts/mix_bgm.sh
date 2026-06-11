#!/usr/bin/env bash
# 给已渲染的 4K 视频垫一层很轻的 BGM（主要压噪底，不盖人声）。
# video 流直接 copy（不重编码）⇒ 4K 画质/颜色逐帧不变；只重编码音频。
#
# 用法:
#   mix_bgm.sh <video.mp4> <bgm.(mp3|wav)> <out.mp4> [volume] [fadein] [fadeout]
# 默认: volume=0.08  fadein=2  fadeout=3
#   更轻 0.05 / 稍明显 0.12
#
# 行为:
#   - BGM 比视频长 → amix duration=first 自动截断到视频末；短 → -stream_loop -1 循环。
#   - 人声保持原音量（amix normalize=0，避免被混音压低）。
#   - 结尾 fadeout（自动按视频时长定位起点）。
set -euo pipefail

VIDEO="${1:?需要 video.mp4}"
BGM="${2:?需要 bgm 文件}"
OUT="${3:?需要 out.mp4}"
VOL="${4:-0.08}"
FIN="${5:-2}"
FOUT="${6:-3}"

# 找 ffmpeg / ffprobe（PATH 优先，WinGet 兜底）
FF="$(command -v ffmpeg || true)"
FP="$(command -v ffprobe || true)"
if [ -z "$FF" ]; then
  FF="$(ls "$HOME"/AppData/Local/Microsoft/WinGet/Packages/*/*/bin/ffmpeg.exe 2>/dev/null | head -1 || true)"
  FP="$(ls "$HOME"/AppData/Local/Microsoft/WinGet/Packages/*/*/bin/ffprobe.exe 2>/dev/null | head -1 || true)"
fi
[ -n "$FF" ] || { echo "ffmpeg 未找到"; exit 1; }

DUR="$("$FP" -v error -show_entries format=duration -of csv=p=0 "$VIDEO")"
FOUT_ST="$(awk -v d="$DUR" -v f="$FOUT" 'BEGIN{printf "%.2f", d-f}')"

echo "video=$DUR s  bgm vol=$VOL  fadein=${FIN}s fadeout=${FOUT}s@${FOUT_ST}s"

"$FF" -y -i "$VIDEO" -stream_loop -1 -i "$BGM" \
  -filter_complex \
  "[1:a]volume=${VOL},afade=t=in:st=0:d=${FIN},afade=t=out:st=${FOUT_ST}:d=${FOUT}[bg];\
[0:a][bg]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -movflags +faststart \
  "$OUT" -loglevel error -stats

echo "✓ $OUT"
