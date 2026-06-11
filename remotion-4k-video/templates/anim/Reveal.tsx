// 复制到 <remotion>/src/deck/anim/Reveal.tsx
// 便捷包裹组件。已有元素优先直接用 useReveal hook 套 style(不多包 DOM)；
// 需要给一段内容整体加入场时用 <Reveal>。
import { type CSSProperties, type ReactNode } from "react";
import { useReveal, type RevealOpts } from "./useReveal";

export function Reveal({
  children,
  style,
  className,
  as: As = "div",
  ...opts
}: RevealOpts & {
  children: ReactNode;
  style?: CSSProperties;
  className?: string;
  as?: "div" | "span";
}) {
  const anim = useReveal(opts);
  return (
    <As className={className} style={{ ...style, ...anim }}>
      {children}
    </As>
  );
}
