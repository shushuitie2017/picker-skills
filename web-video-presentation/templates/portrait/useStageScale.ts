import { useEffect, useState } from "react";

/**
 * PORTRAIT (9:16) variant. Compute the scale needed to fit a 1080x1920 stage
 * inside the current viewport, leaving `marginX` / `marginY` of breathing room
 * around it (so absolutely-positioned UI like the progress bar isn't cropped).
 *
 * Margins are tighter than landscape because portrait is usually viewed in a
 * tall, narrow window where height is the binding constraint.
 */
export function useStageScale(
  baseW = 1080,
  baseH = 1920,
  marginX = 40,
  marginY = 60,
) {
  const [scale, setScale] = useState(1);

  useEffect(() => {
    function update() {
      const usefulW = Math.max(180, window.innerWidth - marginX * 2);
      const usefulH = Math.max(320, window.innerHeight - marginY * 2);
      setScale(Math.min(usefulW / baseW, usefulH / baseH));
    }
    update();
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, [baseW, baseH, marginX, marginY]);

  return scale;
}
