// 覆盖 <remotion>/src/deck/components/MaskReveal.tsx（Remotion 副本，勿动 presentation 副本）
// clip-path 文字 wipe(自左向右)的帧驱动版：用 useCurrentFrame 逐帧精确、渲染不闪烁。
// 接口与网页版 presentation/ 副本一致(show/delay/duration)，故各章节调用处无需改动。
import type { CSSProperties, ReactNode } from "react";
import { useProgress } from "../anim/useReveal";

interface Props {
  show: boolean;
  delay?: number;
  duration?: number;
  className?: string;
  children: ReactNode;
}

export function MaskReveal({
  show,
  delay = 0,
  duration = 700,
  className,
  children,
}: Props) {
  const p = useProgress(delay, duration, "quart");
  const cls = ["mask-reveal", className].filter(Boolean).join(" ");
  const style: CSSProperties = {
    display: "inline-block",
    clipPath: show ? `inset(0 ${(1 - p) * 100}% 0 0)` : "inset(0 100% 0 0)",
  };
  return (
    <span className={cls} style={style}>
      {children}
    </span>
  );
}
