# FILM-DECONSTRUCTION — study real films, extract rules, feed the craft bank

The craft layer (`CINEMATIC-CRAFT.md`) gets SHARPER by deconstructing real films/scenes and
distilling reusable rules. This is the input pipeline for that layer — the "learn from a film"
workflow the user asked for. Run it to refill the craft bank with concrete, genre-matched grammar.

## When to run
- The user shares a film / scene / reference clip ("学这部片的开场").
- Proactively once every few cycles to keep the craft bank fresh and genre-anchored (xianxia).
- Before re-storyboarding a weak act — deconstruct a strong analogue first.

## How to source references (read-only; never touch the user's account)
1. **WebSearch / WebFetch** for existing shot-by-shot analyses (this is abundant online — "X 开场
   分镜 分析", "X opening shot breakdown", "X cinematography analysis", director interviews). The
   director's own words on their opening design are the most authoritative source (see the
   凡人修仙传 杨阳 interview in your own deconstruction notes (per FILM-DECONSTRUCTION.md)).
2. **Canonical craft corpus** (stable, importable): StudioBinder (camera-shots / shot-angles /
   transitions / rhythmic-editing / lighting), Google's official Veo 3.1 DoP prompting guide,
   Save-the-Cat 15-beat, RainLib/AI-Storyboard 4C framework.
3. If the user supplies a clip/URL, deconstruct THAT (frame extraction if they give a file).
4. Optional: the NotebookLM workflow (CLAUDE.md) can summarize a YouTube scene's beats/transitions
   — but camera angles need a visual analysis source, not just a transcript.

## Shot-by-shot deconstruction template (fill while studying)
| # | 时码 | 景别 | 角度 | 运镜 | 光线 | 切入 | 切出 | 为何有效 | 情绪 |
|---|------|------|------|------|------|------|------|----------|------|
| 1 | 0:00 | ECU | low | static→push | cold+gold rim | — | hard cut | opens on a detail, plants a question | dread |
Capture: what the OPENING shot is (almost never a flat wide), how shot SIZES alternate, where the
CUs/reactions land, how camera MOVES map to emotion, what TRANSITIONS connect beats, how shot
LENGTHS vary (the pacing curve), and the one HIGHLIGHT moment.

## Extract 3-5 reusable RULES (the point of the exercise)
Turn observations into decision rules, e.g. from 凡人修仙传:
- "opens on a character's predicament + a question, not a world panorama" → a HOOK rule.
- "low-angle on the strong + high-angle on the weak, intercut" → a power-dynamics rule.
- "every quiet shot still has a motivated move / 留白 composition" → a no-dead-shot rule.
Write **structural** rules into `references/CINEMATIC-CRAFT.md` (the grammar); write **tactical**
Flow-specific ones into `state/TECHNIQUES.md` (EXPERIMENTAL → PROVEN once they land in a film).

## Apply-back loop (autoresearch)
1. Save the deconstruction as `film/99_参考/<片名>_拆解.md` (table + extracted rules + sources).
2. Pick ≥1 extracted rule to TEST in the next cycle's shot list.
3. Generate, judge on the new RUBRIC, log keep/discard in `state/LEDGER.md`.
4. Promote rules that improved the engagement score; retire ones that didn't.

> One deconstruction already done: your own deconstruction notes (per FILM-DECONSTRUCTION.md) (杨阳 opening design +
> the 5 rules now encoded in CINEMATIC-CRAFT). Use it as the format exemplar.
