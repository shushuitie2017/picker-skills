#!/usr/bin/env bash
# 抽帧验证：渲染若干单帧确认入场动画在 Remotion 里逐帧推进（而非起始即定格）。
# 4K still 慢，固定 --scale=0.25 出小图，肉眼即可判断 wipe/rise/错峰/盖章是否在动。
#
# 用法（在 <remotion_dir> 下运行）:
#   verify_stills.sh <comp-id> <frame> [frame...]
# 例:
#   verify_stills.sh sanen-zh 10 20 30 371 398
#
# 定位某步起帧：看 src/timeline.ts 的 STEPS[i].fromFrame，采样「起帧 +10/+20/+30」。
# 输出到 out/chk-f<frame>.png，看完可删。
set -euo pipefail

COMP="${1:?需要 composition id}"; shift
[ "$#" -ge 1 ] || { echo "至少给一个帧号"; exit 1; }

for F in "$@"; do
  npx remotion still "$COMP" "out/chk-f${F}.png" --frame="$F" --scale=0.25 >/dev/null 2>&1 \
    && echo "✓ frame $F -> out/chk-f${F}.png" \
    || echo "✗ frame $F 渲染失败"
done
