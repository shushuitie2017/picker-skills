# FILM-FRAMEWORK — the planning/creative layer

A canonical, professional film-production framework. flow-cinema's CREATIVE
layer follows this structure; the Slate/Flow PLAYBOOK is only the EXECUTION layer.
**If you keep a film project folder, treat it as the source of truth**; this file is the
distilled method so the skill is self-contained.

## Canonical directory layout (scaffold every film like this)
```
<project>/film/
  HOME.md                      # dashboard: logline, theme, phase checklist, nav, act table
  9幕结构总览.md                # the narrative framework + per-act shot-need tables
  镜头类型参考.md               # shot-language vocabulary (景别 + 叙事功能镜头)
  素材生成指南.md               # prompt formula, 运镜/风格 banks, naming convention
  AI配音指南.md                 # per-character voice design + emotion tags + 台词 list
  00_故事/世界观/…              # world bible
  00_故事/角色/NN_名字_角色.md   # character cards (see template below)
  00_故事/大纲/故事大纲.md       # 9-act plot
  01_镜头清单/A1_序章.md … A9_终章.md   # per-act shot-list TABLES (the production unit)
  02_分镜脚本/分镜模板.md        # storyboard template
  03_素材/{视频,旁白,音效}/      # generated assets land here, named by convention
```

## The 9-act narrative spine (序章→终章)
Based on One Piece pacing × Hollywood 3-act. Each act needs 5–15 clips (3–10 s):
1. **A1 序章** — world & tone (make the world legible in 3 s). 大远景/远景/核心符号.
2. **A2 日常** — protagonist's origin: who they are + what they want (eyes-to-horizon).
3. **A3 事件** — the irreversible turn (sacrifice/loss + 觉悟 + 誓言).
4. **A4 冒険** — leave home, new world, meet companions, team freeze-frame.
5. **A5 试炼** — escalating trials, small wins, signature-line beats.
6. **A6 危机** — lose everything, the emotional nadir (the 全片情感高潮).
7. **A7 觉醒** — rise from the low, new power/resolve, montage, reunion.
8. **A8 决战** — final duel, callback flashbacks, ultimate strike.
9. **A9 终章** — new equilibrium, growth-arc contrast, horizon, fade.

**One flow-cinema cycle = ONE act** (its 5–15 shots), not the whole film. This keeps
cycles comparable (autoresearch budget) and lets you cast/review/record per act.

## Shot-list table = the production unit (fill, then generate)
Each `01_镜头清单/AN_*.md` holds a table you fill BEFORE generating:
```
序号 | 景别 | 运镜情绪 | 剪辑时长 | 内容 | AI Prompt | 状态
01  | ECU | 推近=压迫 | 3s·钩子 | 凡人之手被剑影笼罩… | low-angle ECU, … | ⬜
```
- **运镜情绪** = the camera move + the emotion it serves (CINEMATIC-CRAFT §4).
- **剪辑时长** = the planned EDIT length + role (钩子·基线·紧张·高潮·释放, CINEMATIC-CRAFT §6).
  Clips still GENERATE at 8s; you TRIM to this length in post — varied lengths make rhythm.
状态 flow: ⬜ 未生成 → 🟡 生成中 → 🟢 已完成 → ✅ 已剪入. Update it as you generate.
景别 codes: EWS 大远景 · WS 远景 · MS 中景 · MCU 中近景 · CU 特写 · ECU 大特写 ·
ACTION 动作 · MONTAGE 蒙太奇.

## Per-scene coverage pattern (don't ship a row of wides)
Each scene's shots should touch the spine ESTABLISH(WS) → ACTION(MS) → PUNCTUATION(CU) →
REACTION(MCU) → CONSEQUENCE(insert/ECU) — **≥3 sizes per scene**, never two identical 景别
back-to-back, a wide always paid off by a CU. **Canonical anti-pattern (the bland-A1 sin):
four wide/establishing shots in a row with no close-up.** See CINEMATIC-CRAFT §3.

## Prompt formula (every shot) — the layer-cake
Build in this ORDER, then append STYLE SUFFIX + the locked no-text/no-voice clause:
`SCENE(where/when/mood) + CHARACTER(emotion via ACTION, not adjectives) + ACTION(verbs) +
CAMERA(景别 + angle + ONE move + timing) + LIGHT(source/color/drama)`
(legacy short form `[画面]+[景别]+[运镜]+[光线]+[风格]` still maps onto this — the upgrade is
**emotion-through-action**, **one camera move per shot**, and naming the angle. CINEMATIC-CRAFT §8.)
- **运镜 bank**: static/locked · dolly/push in · pull back · orbit · top-down ·
  low-angle (英雄感) · tracking · crane up · handheld · slow zoom.
- **风格 bank**: cinematic+film grain · anime/cel shading · photoreal 35mm · fantasy
  ethereal glow · post-apoc muted · warm nostalgic soft focus · dark moody noir.
- **叙事功能镜头** (use deliberately for beats): 宣言镜头 (shout to sky, backlight) ·
  大泪目 (streams of tears, mouth open) · 名场面一击 (charge→strike→impact 3-shot
  sequence) · 出航 (ship into sunrise) · 背影群像 (silhouettes facing horizon) · 对峙
  (two facing, wind, tense) · 走马灯闪回 (warm 2s quick cuts) · 反派登场 (aftermath→
  boots→face reveal) · 宴会 (warm feast) · 无声镜头 (silent beat at peak emotion).

## Character bible → consistency
Each character card carries an **外貌 AI-prompt block** + **各阶段变化** (wardrobe/look
per act). Lock the protagonist via Flow's 角色 feature using that 外貌 block (cast once,
reuse every shot) and re-cast/adjust wardrobe at the act where 各阶段变化 changes
(e.g. 林远 A2 灰蓝粗布 → A4 深蓝行者服 → A7 白衬墨蓝+五色灵光 → A8 破损染血). Character
drift is the #1 defect → never generate a protagonist shot without the cast character.

## Asset naming convention (download to 03_素材/视频/)
`[幕]_[序号]_[景别]_[描述].mp4` → e.g. `A1_01_EWS_世界全景_金色黎明.mp4`,
`A6_05_MS_崩溃大哭_雨中.mp4`. Keep the table 序号 and the filename 序号 in sync.

## Audio / dubbing (post — see AI配音指南)
Veo clips are generated SILENT of speech (ambient only). In post, dub PER CHARACTER with
a CONSISTENT voice each: design a 声线 per role (年龄/音色/语速/性格), generate with
GPT-SoVITS (clone) / Qwen3-TTS (text-described voice) / Fish Audio (emotion tags like
`(determined, powerful)…` / `(crying, broken)…`). Narrator = calm documentary-epic
mid-age male. Name `[角色]_[幕]_[序号]_[情感].wav`. Pull台词 from each act's shot list.
This realizes flow-cinema's "one consistent voice in post" rule, extended to a full cast.

## How flow-cinema uses this
Planning a film = author/extend the `film/` bible (world + characters + 9-act shot
lists). Producing = per act: cast characters (角色) → fill the shot-list prompts with the
formula → generate via the Flow PLAYBOOK loop → update 状态 → review vs RUBRIC →
download by naming convention → record in state. Post = assemble + per-character dub +
title/subtitle cards + BGM/音效 per the act's 后期笔记.
