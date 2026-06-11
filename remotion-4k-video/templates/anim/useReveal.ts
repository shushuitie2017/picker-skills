// 复制到 <remotion>/src/deck/anim/useReveal.ts
// 帧驱动入场动画原语 —— Remotion 官方做法(useCurrentFrame + interpolate / spring)。
//
// 每个 beat 是独立 <Sequence>，useCurrentFrame() 在 Sequence 内从 0 重新计，
// 正好等于网页版该 beat「挂载后经过的毫秒」。于是把原 CSS 的 delay/duration/ease
// 原样搬进来即可与 presentation/ 一致；区别只是这里逐帧精确、渲染不闪烁。
import { type CSSProperties } from "react";
import {
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { EASE, type EaseName } from "./easing";

/** Sequence 内局部毫秒。 */
function useLocalMs(): number {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (frame / fps) * 1000;
}

/** 0→1 的缓动进度，delay/dur 单位 ms，两端 clamp。自定义动画(width/height/drift)用它。 */
export function useProgress(
  delayMs: number,
  durMs: number,
  ease: EaseName = "quart",
): number {
  const t = useLocalMs();
  return interpolate(t, [delayMs, delayMs + durMs], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE[ease],
  });
}

export type RevealKind =
  | "rise" // opacity + 上移
  | "fade" // 纯 opacity
  | "slideX" // opacity + 横移
  | "growX" // scaleX 0→1(origin left)
  | "wipe"; // clip-path 自左向右

export interface RevealOpts {
  kind: RevealKind;
  delay?: number; // ms
  dur?: number; // ms
  ease?: EaseName;
  dist?: number; // rise=起始translateY；slideX=起始translateX(负=从右进)
}

/** 返回可直接铺到元素上的 style；同名属性会覆盖该元素原 CSS 的动画态。 */
export function useReveal(opts: RevealOpts): CSSProperties {
  const { kind, delay = 0, dur = 700, ease = "quart", dist = 16 } = opts;
  const p = useProgress(delay, dur, ease);
  switch (kind) {
    case "fade":
      return { opacity: p };
    case "rise":
      return { opacity: p, transform: `translateY(${(1 - p) * dist}px)` };
    case "slideX":
      return { opacity: p, transform: `translateX(${(1 - p) * dist}px)` };
    case "growX":
      return { transform: `scaleX(${p})`, transformOrigin: "left" };
    case "wipe":
      return { clipPath: `inset(0 ${(1 - p) * 100}% 0 0)` };
  }
}

/** 超调盖章/弹入(scale-in / pop-in / *-stamp)。用 spring 模拟超调。from=起始 scale。 */
export function useStamp(opts: {
  delay?: number; // ms
  from?: number; // 起始 scale
  rotate?: number; // 固定旋转角(deg)，盖章常带 -3~-4deg
  damping?: number;
  stiffness?: number;
}): CSSProperties {
  const { delay = 0, from = 0.6, rotate = 0, damping = 12, stiffness = 140 } =
    opts;
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const delayFrames = (delay / 1000) * fps;
  const s = spring({
    frame: frame - delayFrames,
    fps,
    config: { damping, stiffness },
  });
  const scale = interpolate(s, [0, 1], [from, 1]);
  const rot = rotate ? ` rotate(${rotate}deg)` : "";
  return {
    opacity: interpolate(s, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
    transform: `scale(${scale})${rot}`,
  };
}

/** SVG 描边(draw / curve-path)：返回 dasharray/offset。length=原 stroke-dasharray。 */
export function useDraw(opts: {
  delay?: number;
  dur?: number;
  length: number;
  ease?: EaseName;
}): CSSProperties {
  const { delay = 0, dur = 1600, length, ease = "quart" } = opts;
  const p = useProgress(delay, dur, ease);
  return { strokeDasharray: length, strokeDashoffset: (1 - p) * length };
}
