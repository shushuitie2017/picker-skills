---
name: remotion-4k-video
description: 把一个网页版 deck（Vite+React+TS，通常由 web-video-presentation skill 产出，如 audiobooks/<id>/presentation/）用 Remotion 帧级重渲成「颜色不失真」的 4K MP4，并可选垫入很轻的 BGM。解决录屏的两大痛点：①录屏颜色失真 → Remotion 输出 sRGB 保真；②手动录屏节奏不稳 → 帧精确、音画锁定。**核心铁律：Remotion 不渲染 CSS animation/transition（逐帧渲染时页面时钟冻结，内容会在第0帧直接定格到最终态 → 表现为「太快/没渐变」）；所有入场动画必须用 useCurrentFrame()+interpolate()/spring() 帧驱动**，本 skill 提供可复用的动画原语库(useReveal/useStamp/useProgress/useDraw)与转换套路。时长 = 每步音频长度 + 120ms trail（与网页版 audio.onended+trailMs 一致，由 gen_timeline.py 从 mp3 实测生成）。触发场景：把有声书/演示 deck 渲成 4K 视频、"Remotion 视频太快/没有渐变/动画不播/颜色对但节奏不对"、给已渲染视频加淡淡的背景音乐压噪底。本项目实样：audiobooks/sanen/remotion/。
---

# Remotion 4K Video（网页 deck → 帧驱动 4K 视频 + 轻 BGM）

把一个**点击驱动的网页 deck**（web-video-presentation 产出的 Vite+React+TS 项目，
按 (chapter, step) 节拍 + 每步一段口播 mp3）用 **Remotion** 重渲成
**真 4K（3840×2160）MP4**，颜色保真、节奏与网页版一致，可选垫一层很轻的 BGM。

> 与 `web-video-presentation` 的关系：那个 skill 负责**做网页 deck**（站内可播/录屏）；
> 本 skill 负责把同一套 deck **帧级重渲成视频文件**。两者共用同一份章节/口播/主题。

## 何时用

- "把这个有声书 / deck 渲成 4K 视频"
- "Remotion 渲出来**太快 / 没有渐变 / 入场动画不播**，但颜色是对的"（→ 见下「核心铁律」）
- "录屏颜色失真，想要保真的视频母片"
- "给渲好的视频加一层淡淡的背景音乐压噪底，别盖人声"

## 核心铁律（务必先读）

**Remotion 逐帧渲染时页面时钟是冻结的，CSS `animation` / `transition` 不会播放。**
- 用 `animation: ... both/forwards` 的入场动画 → 每个 beat 第 0 帧就**定格到最终态**，内容瞬间全显。
- 用 `transition` + 恒为真的状态 → transition 永不触发。
- 症状：用户看到的「**太快**」(缺少 0.7~1.6s 逐句展开来牵引视线) +「**没有渐变**」。
- ❌ 不要用 `document.getAnimations()` 之类 scrub hack（官方警告会闪烁）。
- ✅ 官方做法：所有动画用 `useCurrentFrame()` + `interpolate()` / `spring()` 帧驱动。
  本 skill 的 `templates/anim/` 已封装好原语；见 `references/FRAME-DRIVEN-ANIMATION.md`。

**关键洞察**：每个 beat 是独立 `<Sequence>`，`useCurrentFrame()` 在 Sequence 内**从 0 重新计**，
正好等于网页版该 beat「挂载后经过的毫秒」。把原 CSS 的 `delay/duration/ease` 原样搬进原语 → 视觉与网页版一致。

## 端到端工作流

```
0. 前置：已有网页 deck(presentation/) + 每步口播 mp3（web-video-presentation 产出）
1. 建 Remotion 工程(remotion/)：Root(合成) + Deck(每步一个 Sequence + Audio) + RemotionStage(1920×1080 scale2 → 4K)
2. 复制 deck 源码进 remotion/src/deck/(自包含快照，asset() 改 staticFile)
3. 放入帧驱动原语库 templates/anim/* → src/deck/anim/；MaskReveal 换成帧驱动版
4. gen_timeline.py：从每步 mp3 实测 → segments.json + timeline.json(每步=音频+120ms)
5. 逐章把 CSS @keyframes 入场动画改成原语帧驱动(见 references)，每章 still 抽帧验证
6. 渲染：remotion render(4K h264 crf18)；核对总时长=音频锁定时长、音画同步、颜色
7. 可选：mix_bgm.sh 垫很轻的 BGM(video copy 不重编码)
```

### 1–2. Remotion 工程与 deck 快照
- 合成：`fps=30`、`3840×2160`、`durationInFrames=TOTAL`（各步帧数累加）。
- `Deck` 把 `STEPS` map 成 `<Sequence from durationInFrames>`，每个里放 `<RemotionStage><Cmp step/></RemotionStage>` + `<Audio src={staticFile(...)}/>`。
- `RemotionStage`：`AbsoluteFill` 里 1920×1080 容器 `transform: scale(2)` 铺满 4K（保持 deck 按 1080p 设计）。

> **★横屏 / 竖屏只差三处尺寸★**（其余 timeline/原语/BGM 与朝向无关，完全共用）。竖屏适配 9:16 短视频(抖音/视频号/Shorts)：
>
> | | 横屏 16:9（默认） | 竖屏 9:16 |
> |---|---|---|
> | `Root` `<Composition>` | `width={3840} height={2160}` | **`width={2160} height={3840}`** |
> | `RemotionStage` 容器 | `1920×1080` scale(2) | **`1080×1920` scale(2)** |
> | deck `base.css` `.stage-frame` | `1920×1080` | **`1080×1920`** |
> | 合成 id / 输出 | `<id>-${LANG}` | `<id>-v-${LANG}` |
>
> 竖屏 deck 的章 css 来自竖屏版式工程(如 `presentation-v/`)；**第 5.2 步「剥 animation」对竖屏同样必做**。
> 实样：横屏 `audiobooks/sanen/remotion/`(3840×2160)、竖屏 `audiobooks/sanen/remotion-v/`(2160×3840)。竖屏端到端 SOP 见 web-video-presentation skill 的 `GUJI-USE-CASES.md` §9。
- deck 源码**自包含快照**到 `remotion/src/deck/`，`asset()` 由 `import.meta.env.BASE_URL` 改成 Remotion `staticFile()`。
- `remotion.config.ts`：`Config.setVideoImageFormat("jpeg")`（更快，成片无感差异）、`Config.setConcurrency(4)`（CJK 大字体别开太高）。
- 等 webfont：`delayRender("webfonts")` → `document.fonts.ready` → `continueRender`（兜底 8s）。

### 3. 帧驱动原语库（关键）
把 `templates/anim/{easing.ts,useReveal.ts,Reveal.tsx}` 复制到 `src/deck/anim/`，
把 `templates/MaskReveal.tsx` 覆盖 `src/deck/components/MaskReveal.tsx`。原语：
- `useReveal({kind,delay,dur,ease,dist})` → CSSProperties；kind: `rise|fade|slideX|growX|wipe`
- `useStamp({delay,from,rotate})` → spring 超调（盖章/scale-in/pop-in）
- `useProgress(delay,dur,ease)` → 0..1（自定义 width/height/drift）
- `useDraw({delay,dur,length})` → SVG 描边 `{strokeDasharray,strokeDashoffset}`
- 缓动 `EASE.{quart,expo,soft,overshoot}` 映射自主题 `base.css` 的 4 条 cubic-bezier
> **React hooks 铁律**：章节组件按 `step` 提前 return，所以**不能**在章节组件顶层或 `.map()` 里直接调 hook。
> 把**每个动画元素拆成小子组件**（如 `CdBook`/`CdChainNode`），hook 写在子组件里；错峰列表用「带 index 的子组件」。

### 4. 时长（音频锁定）
`scripts/gen_timeline.py`：按章节×步顺序 ffprobe 每个 mp3，输出
`segments.json`（顺序+文本）与 `timeline.json`（每步毫秒 = 音频时长 + 120ms trail）。
`timeline.ts` 把毫秒按 `round(ms/1000*fps)` 转帧、累加得 `fromFrame/durFrames/TOTAL`。
**与网页版 `audio.onended` + `trailMs=120` 完全一致 → 节奏一致、音画同步。不要手填时长。**

### 5. 章节转换套路（机械、逐章验证）
对每个章节 `*.tsx` / `*.css`：
1. tsx：靠 CSS animation 入场的元素 → 拆小子组件 + `useReveal(...)`/`useStamp`/`useProgress`/`useDraw`。
   `MaskReveal` 用法**不用改**（组件内部已帧驱动）。错峰 `delay = base + i*step`。
2. css：删该元素的 `animation:` / `@keyframes` / 动画态初始值（`opacity:0`、`transform:scaleX(0)`、`width:0`、`stroke-dashoffset` 等）；**保留**布局/配色/字体/静止态 transform。
   > **⚠️ `animation:` 必须删干净，这不是清洁工作而是正确性**：CSS `@keyframes` 动画的级联优先级**高于 inline style**。
   > 若 deck CSS 里残留 `animation:`（典型：把网页版 deck 的 CSS **整份拷进来**、跳过本步），它会**压过**你帧驱动 `useReveal` 写的 inline `opacity` →
   > **高 `delay` 的后入场元素被卡在 `opacity:0` 静默消失**（早入场的恰好动画 seek 到末态而侥幸可见，更难发现）。症状：抽帧时整块内容/某些元素**根本不出现**，
   > 但不报错。`opacity:0`/`transform`/`width:0` 等**普通属性**会被 inline 覆盖、可不删；**唯独 `animation:` 例外**。批量剥离：`re.sub(r'\s*animation(?:-delay)?\s*:[^;}]*;','',css)`。
   > （横屏样例 deck 的章 CSS animation 计数恒为 0，就是这个原因——可 `grep -c 'animation:'` 自检。）
完整映射表与 before/after 见 `references/FRAME-DRIVEN-ANIMATION.md`。
**每改完一章立刻抽帧验证**：`scripts/verify_stills.sh <id> <frame...>`（4K still 慢，用 `--scale=0.25`）。
读 `STEPS[i].fromFrame` 定位某步起帧，采样起帧 +10/+20/+30 帧应见动画**逐帧推进、错峰**，而非起始即定格。

### 6. 渲染与核对
```bash
npx remotion render <comp-id> out/<id>-4k.mp4 --codec=h264 --crf=18
```
渲完核对：`ffprobe` 总时长 ≈ 音频锁定时长（如 sanen 190.12s）、有 aac 音轨、3840×2160；
抽帧确认动画在**成片**里也在动（从 mp4 直接抽帧，不只看 still）。

### 7. 垫 BGM（可选，压噪底）
```bash
scripts/mix_bgm.sh <video.mp4> <bgm.mp3> <out.mp4> [volume=0.08]
```
- **video 流直接 copy**，只重编码音频 → 4K 画质/颜色逐帧不变。
- BGM 很轻（默认 `volume=0.08`）、淡入 2s/淡出 3s、人声保持原音量（`amix normalize=0`）。
- BGM 比视频长则自动截断；短则脚本里 `-stream_loop -1` 循环。
- 调档：更轻 `0.05`，稍明显 `0.12`。

## 本项目实样 / 默认值
- 实样工程：`audiobooks/sanen/remotion/`（合成 id `sanen-zh`，190.12s，26 步 7 章）。
- 默认 4K / 30fps / h264 crf18 / jpeg 帧 / concurrency 4 / trail 120ms / BGM 0.08。
- 与 `web-video-presentation` skill（主题 `guji-ink`）配套；古籍用例见其 `references/GUJI-USE-CASES.md`。

## 参考
- `references/FRAME-DRIVEN-ANIMATION.md` — 铁律详解 + 原语库源码说明 + 动画词汇→原语映射 + 逐章 before/after + 踩坑。
- `templates/anim/` — 可直接复制的原语库源码（easing / useReveal / Reveal）+ 帧驱动 MaskReveal。
- `scripts/` — gen_timeline.py / mix_bgm.sh / verify_stills.sh。
