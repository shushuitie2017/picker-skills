# MODEL-USAGE — becoming expert at the local AI video model (AnimateDiff/diffusers on 2080 Ti)

> ⚠️ STATUS (2026-06-04): the user STOPPED using this local model and DELETED its files —
> `D:/Wan2GP/` (install + venv + `_learn_*.py` + `learn/r1…r13` outputs) and `D:/hf_home/` (weights)
> are GONE. These NOTES are kept intentionally as the learning record. To use the model again you'd
> re-clone/reinstall and re-download dreamshaper-8 + animatediff-adapter-v1-5-3 + swin2SR. The
> voice model `D:/GPT-SoVITS/` is UNRELATED and was kept. Honest bottom line below still stands:
> usage mastered; output plateaus ~5/10 at SD1.5 tier.

MISSION (user-set 2026-06-04): run a multi-round autonomous learning loop to MASTER using
this model, enriching this doc with proven recipes, until **expert level**. Every round's
outputs go to **D:** (`D:/Wan2GP/learn/rN/`) — NEVER C (C is full). Judge every result with
the FIXED eval (RUBRIC.md: blind external critic + adversarial gates; no self-inflation).

## How each round works (the loop reads this and continues)
1. Read this doc → find CURRENT round + its hypothesis.
2. Run ONE experiment (a `_learn_rN.py`, model loaded once, outputs → `D:/Wan2GP/learn/rN/`).
3. Extract frames; run the BLIND critic subagent (compare variants / vs prior best). Verdict OVERRIDES me.
4. Log: hypothesis → what changed → blind verdict → KEEP/DISCARD + why → update "Proven recipes".
5. Advance CURRENT round; ScheduleWakeup to continue. One task at a time, no monitor-shell swarm.

## Environment (fixed)
venv `D:/Wan2GP/venv` (torch 2.7.1+cu128, diffusers 0.36). Env: `HF_HOME=D:/hf_home
HF_HUB_DISABLE_SYMLINKS=1`. Base SD1.5 = `Lykon/dreamshaper-8`; motion = `guoyww/animatediff-motion-adapter-v1-5-3`.
ffmpeg at WinGet path (`.../Gyan.FFmpeg_.../ffmpeg-8.1-full_build/bin/ffmpeg.exe`; NOT on bash PATH).
Realistic ceiling (honest): SD1.5 tier; SOTA quality needs cloud/bigger-VRAM.
⚠️ **VRAM hygiene (2080 Ti 11 GB):** the 16-frame temporal-attention peak can OOM if a desktop app
spikes VRAM mid-run (R13 OOM'd at 1.7 GB baseline used — transient). Always set
`pipe.vae.enable_slicing(); pipe.enable_attention_slicing()` + env `PYTORCH_CUDA_ALLOC_CONF=
expandable_segments:True`. If OOM persists, just re-run (it's usually a transient spike, not a true cap).

## ⚠️ BIGGEST LESSON (R5) — JUDGE MOTION, NOT STILLS. STILLS LIE.
The "best" jelly = 7.5/10 as a still but **3/10 in MOTION** (blind filmstrip verdict): bells
morph & change count frame-to-frame, creatures pop in/out, identity flickers, structural seam =
classic AI "boiling". **vid2vid on 16 replicated-still frames has NO temporal anchor → it boils.**
Implication: R2/R4 still-scores OVERSTATE real video quality. From now on EVERY eval uses a
time-spaced filmstrip (motion), not a single frame. The failing axis is MOTION COHERENCE, not
still prettiness — that's where expert effort must go (proper img2vid: SparseCtrl/IPAdapter to
anchor identity, or text2vid which uses the trained motion prior).

## ★★ THE WINNING MOTION RECIPE (R6) — text2vid + forgiving setup = 8/10 coherent motion
Blind filmstrip compare: **text2vid (AnimateDiffPipeline, trained motion prior) = 8/10 stable drift
("would read as real footage in a fast scroll"); vid2vid-on-still = 2/10 boil.** USE TEXT2VID for
motion, NOT vid2vid-on-replicated-still. PLUS the setup that makes motion stable:
- **dark / low-detail background** (nothing to boil; hides artifacts)
- **a SINGLE luminous subject** (not frame-filling busy high-freq detail — that's the worst case)
- **gentle/slow motion** intent + FreeInit(3) for temporal coherence + rich prompt + super-res finish.
TENSION to solve later (R7): text2vid is generic (no real asset). Distinctive + coherent-motion
together needs SparseCtrl/IPAdapter (anchor a real image into the motion prior).

## ★★★ THE BOTTLENECK MOVED (R7) — TECHNIQUE is ~solved; CONCEPT now caps the score.
Synthesis short (3 luminous creatures, dark bg, slow-mo, crossfades) blind-scored **4/10** — but
the breakdown is the lesson: **craft/execution = 6/10** (clean 9:16, no seams, passes realism
sniff test) yet **the IDEA = generic** ("atmospheric wallpaper, not content… ambient montages
don't get shared"). So mastering the model's *operation* is necessary but NOT sufficient.
RULES for any real piece from here:
- **ONE iconic, instantly-legible subject** — not a montage. Subject legibility VARIES by prompt:
  the jellyfish (clear bell silhouette) read as a creature; "siphonophore"/"comb jelly" rendered as
  abstract light-curtains. Pick the subject the model draws unambiguously.
- **Open on a REVEAL HOOK in the first ~1.5s** (tight→wide, dark→ignite, "wait, what is that?").
- **Deliver a payoff**, don't just sustain a mood. Mood = swipe; payoff = watch/share.
- Monochrome-on-black flatters realism (hides artifacts) but also reads as screensaver — needs the
  hook/payoff to escape "filler".

## ★★★★ THE OUTPUT CEILING (R9) — it's CONTENT, not edit. Structure 7/10, content 2/10.
Aggressive structural reveal (true black → ignite → 4×→1× pull → resolve) blind-scored: the REVEAL
STRUCTURE = **7/10** ("earns a 1.5s stop, helps vs a flat shot") but the RESOLVED SUBJECT = **2/10**
("dye/fluid-sim, not a creature; detached mushroom blob = pure fluid-sim behavior") → overall 3/10.
CONCLUSION: editing/structure is ~solved and NOT the bottleneck; the **model's content is**. At
SD1.5/AnimateDiff tier, **translucent/diffuse glow subjects (jelly, siphonophore, comb jelly, ink)
ALL read as fluid-sims** — because that's what a diffuse diffusion blob IS. No edit lifts that.
STRATEGIC PIVOT (R10): stop forcing translucent "creatures"; discover what THIS model renders
*convincingly* — either (a) OPAQUE, structured subjects (koi/moth/lantern) with legible anatomy, or
(b) EMBRACE the abstract — frame "liquid light / ink bloom" as deliberate ART judged on beauty, not
realism (sidesteps the credibility-killer axis entirely). Let the model's real strengths pick.

## ★★★★★ THE BREAKTHROUGH INSIGHT (R10) — MATCH SUBJECT TO THE MODEL: it does STILLNESS, not motion.
Blind-ranked 4 subjects: **MOTH 8/8 (WINNER) > KOI 7/6 > LANTERN 7/5 > INKBLOOM 6/3.** The moth
("real macro photo, anatomically coherent, rock-stable, only a subtle wing-tilt — zero morphing")
won because the model's WEAKNESS (can't do big motion) became the AESTHETIC. Koi "cheats motion"
(pans instead of swims, fins smear); lantern's hero balloons in size; inkbloom boils ("flicker
disguised as art"). RULE: pick a subject whose believable state is **near-motionless** (perched
moth breathing, a calm macro portrait, a still object with one tiny live detail) — **opaque &
structured, clean macro, single subject**. Then the only motion is small + coherent = passes as
real. This is the route past the content ceiling. Translucent/diffuse glow = avoid (fluid-sim).

## ★ NEAR-MILESTONE (R11) — moth short = 5/10. CONTENT CEILING BROKEN; remaining gap = motion payoff.
The moth short "passes as real photography at scroll speed" (realism solved by the subject-model
match). Capped at 5 by TWO craft issues, both fixable: (1) the push-in was too weak (fade-in
brightening masked it → read as an exposure ramp, not a zoom); (2) NO micro-event — "calm only works
if ONE micro-motion rewards the patience; stability without payload = boring". So a calm
living-photograph needs: a CONFIDENT push-in (end ≈1.4–1.5× tighter) + ONE perceptible micro-beat
at the apex (a wing-breath/antenna twitch — surface the model's own subtle motion by slowing LESS).
Score arc: montage 4 → reveal 3 → aggressive-reveal 3 → moth 5 (the jump = fixing CONTENT).

## ★ R12 — moth v2 = 4/10 (push-in FIXED; the wall is now SOURCE MOTION, not the edit).
Confident push-in worked ("legible & intentional"); coherence clean. But the apex payoff still
absent — "Ken Burns on a still, the live wing beat never arrives". You CANNOT edit-in a living beat
that isn't in the source clip. Also realism-critic NOISE confirmed again: R11 critic "passes as real
photo", R12 critic "clocks AI in <1s, painterly flat wing" — SAME footage. Treat absolute-realism
scores as ±2–3 noisy; trust the structural notes (motion/payoff), not the realism number.
KEY HYPOTHESIS surfaced: **FreeInit(3) over-STABILIZES → that's why a perched subject has ~zero
motion.** The model's motion is BIMODAL (big=boils / perched+FreeInit=static); the "subtle live"
middle a living-photograph needs may require LESS FreeInit + a motion-forward prompt.

## CURRICULUM (toward expert)  ·  CURRENT = R13 (test FreeInit↓ + motion prompt → get a real subtle wing beat)
- **R1 — quality levers:** FreeInit on/off, steps, prompt/negative quality. Does FreeInit cut the mush/warble? worth 3× compute?
- **R2 — image-to-video (THE unlock):** animate a REAL distinctive still (dandelion古图 / Haeckel jelly) via vid2vid (AnimateDiffVideoToVideoPipeline, static→frames, low strength) and/or IPAdapter. Goal: motion on the REAL asset, not generic text-gen.
- **R3 — prompt/seed/guidance tuning** for a target look; build a prompt formula.
- **R4 — AnimateDiff-Lightning** (8GB, few-step) — speed vs quality tradeoff on this GPU.
- **R5 — motion control:** motion LoRA / context length / camera intent (not random drift).
- **R6 — structure/style control:** ControlNet / IPAdapter conditioned on real PD images.
- **R7 — finishing:** real upscale (not just minterpolate) + grade for crispness.
- **R8 — synthesis:** produce one short that the BLIND critic scores clearly above your current baseline.

## EXPERT CRITERIA (when to declare done)
(a) Proven recipes below cover img2vid, quality (FreeInit/steps), motion control, finishing.
(b) A produced short gets a blind-critic score ≥ 6/10 with concrete reasons.
(c) I can state, per technique, the cost (VRAM/time/disk) and when to use it.

## Proven recipes (grows each round)
- **PROMPT SPECIFICITY is the #1 quality lever** (R1, blind-verified). Generic "X in golden
  light" → mush (4/10). A precise prompt — subject + **macro/scale** + per-detail ("individual
  pappus spokes", textures) + **light** ("backlit rim light, volumetric rays") + **lens**
  ("35mm, shallow DOF, cinematic") → resolved detail (8/10). Always write rich, specific prompts.
- **Steps 30 + FreeInit(num_iters=3, butterworth)** noticeably sharpens/coheres vs 22+none
  (cost: ~3× compute from FreeInit). Use for hero shots; skip for drafts.
- **Framing by role:** for a TEXT-OVERLAY background, prefer a **silhouette / big negative-space**
  composition (clean, won't shimmer); for a HERO shot, use detailed macro — BUT high-freq detail
  can **boil/shimmer between frames** in AnimateDiff (verify motion, not just a still).
- Strong NEGATIVE prompt helps: "low/worst quality, blurry, watermark, text, deformed, mutated,
  oversaturated, jpeg artifacts, cartoon".
- **IMG2VID on a REAL distinctive asset BEATS generic text-gen** (R2, blind-verified: real-Haeckel-
  animated 6/10 vs generic-dandelion 4/10 = "platonic generic AI clip, zero authorship"). The
  real-asset path has authorship/an idea → more stop-scroll. THIS is the direction.
- **vid2vid strength sweet spot = ~0.70–0.75; NEVER below 0.7** (R3 blind-verified: 0.60/0.65 =
  noise-mush blob-rows 3/10; 0.70 = the ONLY coherent one, clear bell+tentacles, 7/10; 0.75 =
  coherent but muddy center on busy source). The replicated-still init needs ≥0.7 denoise or it
  stays noise. Distinctive non-default palette (cyan-on-cream) reads deliberate → lean into it.
- **FINISHING with Swin2SR super-res WORKS** (R4, blind+metric-verified): a x2 Swin2SR pass
  (`caidas/swin2SR-classical-sr-x2-64` via transformers) lifted crispness 5/10→7.5/10 (+53%
  gradient / +45% HF energy), resolving strands/structure, NO halos or smoothing. Always do a
  super-res finishing pass on AnimateDiff output. Caveat: detail is SYNTHESIZED (perceived, not
  true fidelity) — fine for feeds. ⚠️ BUG: Swin2SR output came out SQUARE (1040×1040) from a
  512×768 input — it mangled aspect. FIX in production: pad to a window-multiple keeping aspect,
  or crop the result back to 2:3, don't trust raw output dims.
- **Source choice matters:** busy multi-subject plates → muddy/structureless center. Use a
  CLEAN single-subject crop with a clear focal point.

## Round log
- **R1 DONE** (quality levers). Blind verdict C≫B>A: rich-macro-prompt+30steps+FreeInit = 8/10
  detail vs generic 22-step baseline = 4/10 mush. Lessons → Proven recipes above. KEEP all.
- **R2 DONE** — img2vid on real Haeckel jelly. Blind: real-asset 6/10 > generic 4/10 (KEEP the
  direction). s0.5=noise, s0.75=coherent-but-muddy-center. Lessons → Proven recipes.
- **R3 DONE** — strength sweep. Blind: 0.70 only coherent (7/10); 0.60/0.65 noise (3/10). Sweet
  spot ≥0.70. KEEP. Recurring weakness = softness.
- **R4 DONE** — Swin2SR x2 finishing. Blind+metrics: 5→7.5/10 crisp (+50% edge/HF), no halos. KEEP
  as finishing pass. Bug: squished aspect to square → fix in prod. 
- **R5 DONE — PIVOTAL.** Motion filmstrip blind verdict 3/10: vid2vid-on-still BOILS (morph/
  flicker/seam). Stills lied. New rule: evaluate motion via filmstrip always. (See BIG LESSON above.)
- **R6 DONE — SOLVED MOTION.** Blind filmstrip compare: TEXT2VID = **8/10** ("would read as real
  footage in a fast scroll", single stable identity, trackable tentacles) vs vid2vid-on-still = 2/10
  (boil). Winning recipe locked (see ★★ above). KEEP text2vid as the default for motion.
- **R7 DONE — TECHNIQUE SOLVED, CONCEPT IS NOW THE WALL.** Built the synthesis short
  (`D:/Wan2GP/learn/r7/short.mp4`, 12.8s, 3 creatures, slow-mo+crossfade; aspect bug FIXED →
  1024×1536 clean). Blind: **4/10** — craft 6/10 but idea generic ("wallpaper, not content"). The
  winning *recipe* held (clips look real, motion coherent, framing clean); the *editorial* failed.
  KEEP the recipe; the gap is concept (see ★★★ above). Honest: 4 < 6, NOT expert yet.
- **R8 DONE — 3/10. Two findings.** Built `reveal.mp4` (single jelly, dark→ignite fade, 1.6×→1.0×
  zoom-out, 7s). Blind: 3/10, "same as the montage". (1) **A timid reveal = no reveal**: 1.6×→1.0×
  is imperceptible; a real reveal must WITHHOLD — true black ~1.5s, ignite a point, pull ~4×→1× so
  the subject resolves only at ~3–4s. I hadn't actually tested a real reveal. (2) **Realism is noisy
  & capped**: R6 critic said this same jelly 8/10 "passes as real"; R8 critic said "dye/ink-sim,
  credibility killer". Both fair — motion is coherent, but ABSOLUTE realism at SD1.5 tier reads as
  "sim" to a hostile eye. A cosmetic hook adds 0. KEEP the recipe; the open question is whether a
  STRUCTURAL reveal can carry a piece despite the realism ceiling.
- **R9 DONE — 3/10. CEILING ISOLATED = CONTENT, not edit.** Built `reveal2.mp4` (aggressive reveal,
  8.6s). Self-checked filmstrip first (reveal now reads — fixed R8's timidity). Blind: structure
  7/10, resolved subject 2/10 ("fluid-sim, not creature") → 3/10. The edit is solved; the model's
  content is the wall (see ★★★★ above). KEEP the reveal-structure recipe as proven.
- **R10 DONE — BREAKTHROUGH.** 4-subject blind rank: MOTH 8/8 WINNER (see ★★★★★ above). Found the
  rule: match subject to the model (stillness, opaque/structured, near-motionless). KEEP.
- **R11 DONE — 5/10, best yet.** Moth short (dark→ignite + push-in). Realism "passes as real photo
  at scroll speed" → CONTENT CEILING BROKEN by the subject-model match. Capped at 5 by weak push-in
  + no payoff beat (see ★ R11 above).
- **R12 DONE — 4/10.** moth v2: push-in fix CONFIRMED working; coherence clean; but apex payoff
  (live wing beat) still missing — source-motion problem, not editable. Realism-critic noise
  re-confirmed (±2–3). Surfaced FreeInit-over-stabilizes hypothesis (see ★ R12 above). KEEP push-in.
- **R13 STARTED** — generation experiment for the MISSING payoff: regen the moth with a motion-forward
  prompt ("wings slowly opening and closing, gently fluttering") at FreeInit num_iters **1 vs 0(off)**
  + a FreeInit=3 control — blind-compare which has a VISIBLE yet still COHERENT wing beat (not boiling).
  If one works → build moth v3 → retest ≥6. Outputs → `D:/Wan2GP/learn/r13/`.
