# 帧驱动动画（Remotion 入场动画的正确做法）

> 本文件是本 skill 的核心知识。读完即可把任意 web-video-presentation 风格的
> deck（CSS @keyframes 入场动画）正确地搬进 Remotion，使渲染出的视频
> 与网页版逐句显影/盖章/错峰一致，而不是「太快 + 没渐变」。

## 1. 为什么 CSS 动画在 Remotion 里不播

Remotion 渲染是**非线性逐帧**的：它把页面时钟冻结、跳到某一帧、re-render React、截图。
CSS `animation` / `transition` 依赖真实墙钟时间推进，墙钟被冻结 ⇒
- `animation: x 700ms ... both/forwards` → 每帧都停在动画的**最终态**（fill 把末态回填）。
  视觉上：内容在每个 beat 第 0 帧就**全部出现**，之后静止。
- `transition` + 状态恒定（如 `<MaskReveal show>` 的 show 恒为 true）→ 没有状态翻转，**transition 永不触发**。

用户的两个抱怨其实是**同一个 bug**：
- 「没有渐变」= 动画从不播放。
- 「太快」= 缺少 0.7~1.6s 的逐句展开来牵引视线（音频锁定的总时长其实没变）。

❌ **不要**用 `document.getAnimations().forEach(a=>{a.pause();a.currentTime=t})` 这类 scrub hack——
Remotion 官方明确警告非 `useCurrentFrame()` 驱动的动画会闪烁；且 transition 这样也救不回来。

✅ **官方做法**：所有动画用 `useCurrentFrame()` + `interpolate()` / `spring()` 帧驱动。

## 2. 关键洞察：Sequence 局部帧 == 网页版挂载时间

`Deck` 把每个 beat 渲成独立 `<Sequence from durationInFrames>`。
`useCurrentFrame()` 在 Sequence **内部从 0 重新计**。
所以 `t = frame/fps*1000`（ms）正好等于网页版「该 beat 挂载后经过的时间」。
→ 把原 CSS 的 `delay / duration / ease` **原样**搬进帧驱动原语，视觉就与网页版一致。

## 3. 原语库（templates/anim/）

复制 `templates/anim/{easing.ts,useReveal.ts,Reveal.tsx}` → `<remotion>/src/deck/anim/`，
复制 `templates/MaskReveal.tsx` → 覆盖 `<remotion>/src/deck/components/MaskReveal.tsx`。

- `EASE.{quart,expo,soft,overshoot}` —— `Easing.bezier(...)`，映射自主题 `base.css` 的 4 条 cubic-bezier。
  （若主题不同，把 base.css 里 `--ease-*` 的 bezier 值同步到 easing.ts。）
- `useProgress(delayMs, durMs, ease="quart") → number 0..1`：通用缓动进度（两端 clamp）。基础件，自定义动画用它。
- `useReveal({kind, delay=0, dur=700, ease="quart", dist=16}) → CSSProperties`：
  - `rise`   → `opacity:p, translateY((1-p)*dist)`（dist = keyframe 起始 translateY 像素）
  - `slideX` → `opacity:p, translateX((1-p)*dist)`（dist = 起始 translateX；从左进用负值，如 -16）
  - `fade`   → `opacity:p`
  - `growX`  → `scaleX(p)`，`transform-origin:left`
  - `wipe`   → `clip-path: inset(0 (1-p)*100% 0 0)`（文字自左向右擦出）
- `useStamp({delay=0, from=0.6, rotate=0, damping=12, stiffness=140}) → CSSProperties`：
  `spring()` 超调缩放 + opacity（+固定 rotate）。用于 *-stamp / scale-in / pop-in（盖章、徽记弹入）。
  `from` = keyframe 起始 scale（如盖章常从 1.5 或 1.6 收到 1；pop-in 从 0.6 长到 1）。
- `useDraw({delay=0, dur=1600, length, ease="quart"}) → {strokeDasharray, strokeDashoffset}`：
  SVG 描边（stroke-dashoffset length→0）。`length` = 原 CSS 的 `stroke-dasharray` 值。

## 4. React hooks 铁律（最容易踩）

章节组件按 `step` **提前 return**（`if (step===0) return ...`）。
因此**绝不能**在章节组件顶层、或 `.map()` 回调里直接调上面的 hook（违反 rules-of-hooks）。

✅ **把每个动画元素拆成一个小子组件**，hook 写在子组件里：
```tsx
function CdBook() {
  return <img className="cd-book" src={asset("cover.jpg")}
    style={useReveal({ kind:"rise", delay:0, dur:1200, dist:26 })} />;
}
// 错峰列表 → 带 index 的子组件，在 map 里渲染它（不是在 map 里调 hook）
function CdChainNode({ i, ... }) {
  return <span style={useReveal({ kind:"slideX", delay:500+i*360, dur:520, dist:-16 })}>...</span>;
}
{nodes.map((n,i)=> <CdChainNode key={i} i={i} .../>)}
```
SVG 描边、自定义 width/height/drift 同理：子组件里调 `useProgress`/`useDraw`，把算出的值写进 `style`。

## 5. 动画词汇 → 原语映射

| 原 CSS @keyframes 类型 | 原语 |
|---|---|
| opacity + translateY 上移（*-rise, *-fade 带位移）| `useReveal('rise', dist=位移px)` |
| 纯 opacity（*-fade）| `useReveal('fade')` |
| opacity + translateX（*-node-in, *-row-in）| `useReveal('slideX', dist=起始X，左进为负)` |
| 超调缩放盖章（*-stamp, scale-in, pop-in）| `useStamp({delay, from=起始scale, rotate})` |
| width 0→目标（strike, fork-grow, rail-fill）| 子组件 `useProgress` + inline `width: calc(目标 * p)` 或 `${目标*p}px` |
| height 0→目标（line-grow）| `useProgress` + inline `height: ${目标*p}px` |
| SVG 描边（draw / curve-path）| `useDraw({delay,dur,length=dasharray})` 套到 `<path>` |
| clip-path 文字擦出（MaskReveal）| 已封装：直接用 `<MaskReveal show delay duration>`，无需改调用处 |
| 多属性漂移（drift：translate+scale+rotate+opacity）| `useProgress` + 手写 `transform: translate((1-p)*dx,(1-p)*dy) scale(0.96+0.04p) rotate(...)` |
| 旋转+缩放同时入场（如太极 taiji-in）| `useProgress` 手写 `transform: rotate(插值) scale(插值)`（**别**用 useStamp，它会覆盖旋转）|
| 无限装饰（flip-pulse 等）| 低优先：`const dx=Math.sin(frame/(fps*周期)*2π)*幅度` 驱动；或直接静置（去掉动画）|

## 6. before / after（以 coldopen 为范例）

```tsx
// BEFORE：CSS 驱动（Remotion 里定格在最终态）
<img className="cd-book" src={asset("cover.jpg")} />
// .cd-book { animation: cd-rise 1200ms var(--ease-quart) both; }
// @keyframes cd-rise { from{opacity:0;transform:translateY(26px)} to{opacity:1;transform:translateY(0)} }

// AFTER：帧驱动
function CdBook(){ return <img className="cd-book" src={asset("cover.jpg")}
  style={useReveal({kind:"rise",delay:0,dur:1200,dist:26})} />; }
// CSS 里删掉 .cd-book 的 animation 与 @keyframes cd-rise
```

盖章：
```tsx
// .cd-seal { animation: cd-stamp 600ms var(--ease-overshoot) 1100ms both; } // 1.5→1 收
function CdSeal(){ return <span className="cd-seal" style={useStamp({delay:1100,from:1.5,rotate:-3})}>金<br/>泉</span>; }
```

width 生长（strike）：
```tsx
function CdStrike({delay}:{delay:number}){
  const p = useProgress(delay,500,"expo");
  return <i className="cd-strike" style={{ width:`calc((100% + 12px) * ${p})` }} />;
}
```

SVG 描边（closing 贝尔曲线）：
```tsx
function ClCurvePath(){ // 原 stroke-dasharray:900
  return <path className="cl-curve-path" d="..." style={useDraw({delay:100,dur:1600,length:900})} />;
}
```

## 7. CSS 清理规则

对被原语接管的元素，在该章节 `*.css` 里：
- **删**：`animation:` 简写、对应 `@keyframes`、动画态初始值（`opacity:0`、`transform:scaleX(0)`、`width:0`、`height:0`、`stroke-dasharray/offset` 初值、入场用的初始 transform）。
- **留**：布局/定位/字体/配色/阴影、以及**静止态** transform（如分叉线 `rotate(-26deg)` 是常态外观，不是入场动画——保留）。
- 共享 `animations.css` 里 `.mask-reveal` 改成只留 `display:inline-block`（动画态由组件 inline 控制）；`rise-in/scale-in/...` 等未被引用的 keyframes 可留可删（不影响）。
- 完事 grep 自检：章节目录里 `animation:` / `@keyframes` 应只剩**注释**命中。

## 8. 验证

每改完一章立刻抽帧（4K still 慢，务必 `--scale=0.25`）：
```bash
.claude/skills/remotion-4k-video/scripts/verify_stills.sh <comp-id> <frame> [frame...]
```
- 定位某步起帧：看 `timeline.ts` 的 `STEPS[i].fromFrame`（或在 Remotion Studio 时间轴上读）。
- 采样「起帧 +10 / +20 / +30」帧：应看到 wipe 自左推进、rise 上移中、错峰元素**依次**出现、盖章 spring 收口；
  delay 未到的元素应**还没出现**。若起始即定格 → 该元素还在用 CSS 动画，回去清理。
- 成片渲完后，**从 mp4 直接抽帧**再确认一次（不只看 still）：
  `ffmpeg -ss <秒> -i out/<id>-4k.mp4 -frames:v 1 -vf scale=960:-1 chk.png`

## 9. 踩坑速记
- `useStamp` 只输出 `scale(+rotate)`：若元素入场同时要转特定角度（非固定常态角），改用 `useProgress` 手写 transform，别用 useStamp（会覆盖旋转）。
- `overshoot` bezier 控制点 y>1，`interpolate` 输出会 >1（即超调），可用；更自然的弹性优先 `spring()`（useStamp）。
- `width: calc((100% + 12px) * p)` 这种「百分比 × 进度」用 CSS `calc` 字符串拼 `p` 最稳（纯 JS 算不出百分比）。
- 只改 remotion 副本，**不要**把帧驱动改动同步回 `presentation/`（网页版靠墙钟跑 CSS 动画，本就正常）。
- 时长别手填：永远用 `gen_timeline.py` 从 mp3 实测（音频锁定 = 音画同步的根本）。
