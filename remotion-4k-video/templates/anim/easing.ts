// 复制到 <remotion>/src/deck/anim/easing.ts
// 把 deck 主题(base.css 的 --ease-*)的 4 条 cubic-bezier 映射成 Remotion Easing。
// 章节入场动画原样沿用这些缓动，保证与网页版 presentation/ 视觉一致。
// 若你的主题 bezier 值不同，把 base.css 里 --ease-* 的值同步到这里。
import { Easing } from "remotion";

export const EASE = {
  quart: Easing.bezier(0.19, 1, 0.22, 1), // --ease-quart：默认入场(出多入少)
  expo: Easing.bezier(0.86, 0, 0.07, 1), // --ease-expo：生长(rule/strike/line)
  soft: Easing.bezier(0.4, 0, 0.1, 1), // --ease-soft：漂移/柔和
  overshoot: Easing.bezier(0.34, 1.56, 0.64, 1), // --ease-overshoot：超调(控制点 y>1)
} as const;

export type EaseName = keyof typeof EASE;
