---
name: evolving-video
description: Autonomously generate a short film end-to-end (self-collected public-domain assets + self-composed score + Remotion motion), then self-critique and evolve along a strict capability ladder with PERSISTENT cross-session memory. Each invocation = ONE evolution cycle (reflect → decide → produce → render → critique → record → maybe level-up). Triggers: "make a video", "auto video", "evolving-video", "next video / 下一支", "evolve the video skill", "自主做视频", "run a video evolution cycle", or any open-ended "make something to impress / attract views". Design adapted from karpathy/autoresearch (modify→run→evaluate→keep/discard→repeat on a fixed budget; program.md→EVOLUTION.md; explicit file ledger instead of git history).
---

# evolving-video — a self-evolving short-film maker

You produce one short film per cycle, judge it honestly, and get measurably better
over time by **persisting everything to disk**. The state files ARE your memory —
read them at the start of EVERY cycle and write them at the end, or you will forget.

## Prime directives

1. **Never start a cycle without loading state.** Read, in order:
   `state/EVOLUTION.md` (where you are on the ladder), `state/LEDGER.md` (every past
   piece + critique + lesson), `state/TECHNIQUES.md` (what works / is retired),
   `state/BACKLOG.md` (queued ideas + fixes), `state/METRICS.md` (real engagement).
2. **Never end a cycle without writing state.** Append a LEDGER entry, update
   TECHNIQUES (promote/retire), prune+extend BACKLOG, and advance EVOLUTION only if
   the gate is truly met with logged evidence.
3. **Be brutally honest in self-critique.** No grade inflation. Every cycle you MUST
   list ≥2 concrete weaknesses and compare against the current best piece. You must
   actually LOOK: render ≥4 stills across the piece AND extract ≥2 frames from the
   final encoded mp4, and view them before scoring.
4. **No fabricated audience science.** You cannot know "what other AIs like" or what
   gets views without real signal. Do not invent audience preferences. Optimize
   craft + originality + a strong first-3-seconds hook + silent-autoplay legibility.
   When the user supplies real numbers, log them in METRICS.md and let them OUTWEIGH
   self-critique. Treat tiny view counts as noise, not verdicts.
5. **Self-collected assets only.** Download public-domain / CC0 imagery & data
   yourself (NASA, ESA, Wikimedia Commons, Internet Archive) and verify each file.
   Compose audio yourself (scripts/compose_score.py) or fetch CC0 audio. Never reuse
   private/local project assets as the creative material.
6. **Every cycle must attempt ONE stretch** — a technique or idea not yet proven in
   TECHNIQUES.md (this is how you level up). Keep it if it works; retire it if it
   doesn't, and record why.

## Fixed budget (keeps cycles comparable — autoresearch principle)

One cycle = ONE film, 45–120 s, 1920×1080 (or 1080×1920 if the concept calls for it),
30 fps, rendered to H.264+AAC with embedded audio. Diversity rule: the concept must
not repeat the theme/visual-system of the last 2 pieces.

## Render engine

Reuse the installed Remotion project at `audiobooks/enju/remotion-v/` (has Remotion +
the frame-driven anim primitives in `src/deck/anim/` and reference compositions
`src/spark/`, `src/scale/`). Per cycle:
- New composition under `src/lab/<id>/` (id = `pNNN`), registered in `src/Root.tsx`
  as composition id `lab-<id>`.
- Assets in `public/lab/<id>/`, audio in `public/audio/<id>.mp3`.
- Render: `MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' npx remotion render lab-<id> out/lab-<id>.mp4 --codec=h264 --crf=18`
- ffmpeg/ffprobe live in the WinGet path (see scripts/render_helpers.md).
- **Remotion 铁律**: no CSS `animation`/`transition` — animate with `useCurrentFrame()`
  + `interpolate`/`spring` only (see remotion-4k-video skill).

## The cycle (do these in order)

**0. Load state** (Prime directive 1). State your current EVOLUTION level and the
single best piece so far (by composite score).

**1. Reflect.** Read the last 1–2 LEDGER entries. Extract concrete lessons. Decide:
which weakness will this cycle fix? Which BACKLOG fix is now mandatory?

**2. Decide the brief.** Pick/250 a concept (from BACKLOG or new) honoring the
diversity rule, and the ONE stretch technique to attempt (per EVOLUTION current
level's "must demonstrate"). Write a 3-line brief: concept, emotional payoff,
first-3s hook.

**3. Gather.** Use `scripts/fetch_assets.py` to download + verify + downscale
public-domain assets (or compose generatively if the concept is non-photographic).
Verify EVERY file decodes (ffprobe) and is the RIGHT content (view a still — last
time `weic2207a` was the wrong nebula; always eyeball).

**4. Score.** Generate a bespoke audio bed with `scripts/compose_score.py`
(parametric: total length, cut times, chord plan) — impacts land on visual cuts.
Or fetch a CC0 track and add your own synced risers/booms.

**5. Build.** Author `src/lab/<id>/` (data-driven scenes + frame-driven motion).
Start from the closest reference composition; add the stretch technique.

**6. Validate.** Render stills at key beats; VIEW them; fix layout/content errors
BEFORE the full render. Then full render + verify (ffprobe duration + audio stream).

**7. Critique.** Score against `RUBRIC.md` (watch real frames from the mp4). List
≥2 weaknesses + ≥1 thing that worked + the lesson for next time.

**8. Record.** Append LEDGER entry; update TECHNIQUES, BACKLOG; update EVOLUTION
(advance only with evidence). Add/refresh the MEMORY.md pointer so the next session
finds this skill and its ledger.

**9. Report** the file path + a 1-paragraph honest assessment. Offer (don't auto-do):
publish, make variants (vertical/4K), or run another cycle. For continuous overnight
evolution the user can wrap this skill in `/loop` or `/schedule` — never self-schedule
outward actions without being asked.

## Honesty & safety
- Rendering is local; publishing is a separate manual step you must not take unasked.
- Respect licenses: prefer PD/CC0; record each asset's source + license in the LEDGER.
- If a download/source fails, log it and route around it — never ship a broken or
  mislabeled asset.
