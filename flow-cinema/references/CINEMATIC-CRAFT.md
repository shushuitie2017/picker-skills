# CINEMATIC-CRAFT — the engagement grammar (read at PLAN time, before any prompt)

This is the layer that makes a viewer KEEP WATCHING. The 9-act spine (FILM-FRAMEWORK) decides
*what each act is about*; the 镜头类型参考 dictionary defines *what a shot is*; THIS file decides
*which shot/move/cut/length to use for a given beat, and how to not be boring*. Vocabulary →
grammar. Every rule below is a decision rule, not a definition.

> Origin: distilled from the 凡人修仙传 director's own opening design (see
> your own deconstruction notes (per FILM-DECONSTRUCTION.md)) + StudioBinder shot/angle/transition/rhythm guides +
> Google's Veo 3.1 DoP prompting guide. Genre anchor = xianxia donghua.

---

## §1 The engagement contract — 5 non-negotiables per act
Before filling a shot-list table, the act MUST contain ALL FIVE. (These map 1:1 to RUBRIC dim 6
and the SKILL DESIGN gate. Missing any → redesign before spending credits.)
1. **A 3-second hook** — opens on a DETAIL or CONFLICT that plants a question, NOT an empty
   establishing landscape (§2).
2. **≥1 character CU/MCU** — at least one intimate, emotional close-up; not all wide/environment.
3. **A visual contrast or escalation** — light/dark, scale, motion, warm/cool, or weak/strong;
   the act's theme is SHOWN, not only narrated (§7).
4. **Pacing variation** — shots are TRIMMED to varied edit-lengths (not all flat 8s) (§6).
5. **One highlight moment** — a single designed, screenshot-able beat the viewer remembers (§7).

> Hard truth from the A1 failure: an act can be technically perfect (clean, consistent, pretty)
> and still be GARBAGE if it lacks these five. Technical polish is the floor, not the goal.

---

## §2 Opening hook (0-10s) — rules, not vocabulary
**Rule H1 — open on a detail/conflict, reveal the world second.** 凡人修仙传 does NOT cold-open on
a world panorama; it opens on a character's predicament + a question. The epic wide is the *payoff*
to the hook, never the cold open.
**Rule H2 — a question legible in 3 seconds.** In-medias-res / cold open. The first 3s must make the
viewer ask "who/what/why?" (e.g., a hand crushed under a shadow → "who is being crushed by this
world?"). No exposition, no title card (titles go to POST).
**Rule H3 — a pattern-break in beat 1.** A distinct sound (breath, sword-scrape, heartbeat) or a
sudden motion/contrast hits before/with the first visual, recruiting attention by surprise.

Decision table — act type → opening shot:
| act type | WRONG cold open | RIGHT hook |
|----------|-----------------|------------|
| epic-world establishing (A1) | wide of clouds/mountains | ECU of a detail that *implies* the world's stakes (a mortal hand, a falling object), THEN reveal the wide as payoff |
| character daily-life (A2) | wide of village | CU of the character mid-action/yearning (eyes to horizon) |
| event/turn (A3) | wide of location | insert of the object/gesture that triggers the turn |
| crisis (A6) | wide of battlefield | CU of fear/a crack/blood, then pull out to the disaster |

---

## §3 Shot-size rhythm & coverage
**Rule C1 — the per-scene coverage spine:** ESTABLISH (WS) → ACTION (MS) → PUNCTUATION (CU) →
REACTION (MCU) → CONSEQUENCE (insert/ECU). Every scene touches **≥3 of these sizes**.
**Rule C2 — a wide never stays without a CU payoff in the same beat.** A wide "earns" its screen
time only if a close-up validates why we needed it. (A1's sin: 4 wides in a row, zero CU for 40s.)
**Rule C3 — never two identical 景别 back-to-back** unless a deliberate jump-cut effect.
**Rule C4 — reaction shots.** After an action/reveal, cut to a face reacting. Emotion lives in
reactions, not in the spectacle itself.
**Rule C5 — 180° line + eyelines.** Keep characters on consistent screen sides; matched eyelines so
two shots feel like one space. (RainLib 4C: Clear, Concise, Consistent, Progressive.)
景别 ladder (from 镜头类型参考): EWS·WS·MS·MCU·CU·ECU. Tighter = more intimate/emotional.

---

## §4 Camera movement ↔ emotion map
| move | emotion | use for |
|------|---------|---------|
| push-in (dolly-in) | intensify, obsession, rising stakes | climactic emotion; reveal a face's feeling |
| pull-out (dolly-out) | isolation, helplessness, scale reveal | after intensity: show how small they are |
| slow pan | guided discovery | reveal/link two subjects |
| whip pan (fast) | urgency, shock | cut to a threat; energy spike |
| crane up | grandeur, transcendence | magic/world reveal |
| crane down | defeat, descent, smallness | press a character down; "蝼蚁" |
| handheld | urgency, chaos, subjectivity | chase, fear, POV |
| static (locked) | tension, dread, authority | someone watching; ominous hold |
**Rule M1 — never repeat the same move twice in a row.** Alternate (push → static → pull → whip) to
*create* rhythm.
**Rule M2 — power dynamics via PAIRED opposing angles.** Low-angle on the strong + high-angle on the
weak, intercut. (凡人修仙传's 仰视→平视 between 韩立 & 墨大夫 = power shift staged purely by angle.)
Angle→emotion: low=power/threat · high=weakness/被碾 · eye-level=equal/intimacy · dutch=unease ·
overhead=fate/insignificance · aerial=awe (but as hook-payoff, not cold open).

---

## §5 Transition taxonomy + Flow implementation
| transition | emotion / use | Flow technique that implements it |
|------------|---------------|-----------------------------------|
| hard cut | momentum, shock; default | just concat clips in post |
| match cut (graphic) | metaphor/theme link (shadow→cloud, blade→moon) | 保存帧 both frames → 帧-interpolation (PROVEN) OR cut on a matching shape |
| match cut (action) | seamless flow | prev-clip LAST frame = next-clip 起始 frame (PROVEN continuity) |
| smash cut | whiplash (peace→violence) | hard cut + opposing energy/audio |
| J-cut (audio leads) | anticipation | POST: next scene's sound starts before its picture |
| L-cut (audio trails) | lingering mood | POST: prior scene's sound continues over next picture |
| invisible cut | hide the edit | cut on a movement/whip/wipe-by |
| dissolve / 渐黑 | time/place change | POST `xfade` (NEVER chained `fade=in:st=T` — see TECHNIQUES RETIRED) |
**Rule T1 — pick the transition for the EMOTION, then implement with the matching technique above.**
**Rule T2 — the 穿越/世界跳跃** = 保存帧 起始(A-end)+结束(B-start) interpolation with a morph prompt
(PROVEN: 地铁→白金灵光→山门).

---

## §6 Pacing & rhythm — the trim model (THE fix for "all flat 8s")
Clips GENERATE at 8s but are **TRIMMED in post** to varied EDIT lengths. Plan the edit-length per
shot in the shot-list table's 剪辑时长 column; generation length stays 8s.
| role | edit length | when |
|------|-------------|------|
| hook | 2-3s | the opening sting |
| baseline | 4-6s | normal flow |
| tension | 2-3s | building toward a peak (progressively SHORTEN cuts) |
| peak/insert | 1-2s | the strike / the reveal punctuation |
| release/landing | 5-8s | breathing room after intensity |
**Rule P1 — tension build = progressively shorter cuts; release = longer holds.** The eye *feels*
the wave without knowing why.
**Rule P2 — 先沉后燃 (xianxia convention):** an opening may hold longer, contemplative shots — but
ONLY if each carries a motivated move/composition (§3-4); never a static flat空镜.
ffmpeg trim is free (proven concat/`-ss/-t` recut). A1's mistake was shipping every clip at 8s.

---

## §7 Conflict in every frame + the highlight moment
**Rule E1 — every shot passes the test: "does this contain a problem, choice, or emotional shift?"**
If a shot is pure pretty information with no tension, redesign it (add a struggling figure, an
ominous element, a contrast).
**Rule E2 — visual-contrast axes:** light/dark · scale (tiny figure vs vast) · motion/stillness ·
warm/cool · strong/weak. SHOW the theme via contrast. (凡人修仙传 rule: "仙凡 = 蝼蚁" is staged by
low-angle immortal + high-angle crushed mortal, NOT spoken by narration.)
**Rule E3 — emotional throughline:** shots 1→N show a *progression* of feeling (fear→resolve→
realization), not random pretty moments.
**Rule E4 — exactly one designed highlight per scene** — the screenshot moment (an ECU of eyes
opening, a hand reaching, a blade catching light). Build the scene to deliver it.
**Rule E5 — 留白 composition (xianxia signature):** large negative space, subject placed off-center
and small inside a vast environment = the mortal-among-immortals smallness. Don't fill the frame.

---

## §8 Veo prompt layer-cake (upgrades the FILM-FRAMEWORK formula)
Build each prompt in this order, then append the locked no-text/no-voice clause:
1. **SCENE** — where/when/weather/mood ("abandoned Taoist temple, pre-dawn fog, cold blue light")
2. **CHARACTER** — who + emotion **through ACTION, not adjectives** ("trembling hands, knuckles
   white, jaw clenched" — NOT "determined/sad")
3. **ACTION** — verbs, what physically happens ("claws the wet earth; a shadow sweeps over; freezes")
4. **CAMERA** — framing(景别) + angle + ONE movement + timing ("low-angle ECU, slow 3s push-in")
5. **LIGHT** — source/color/drama ("golden qi-light clashing with cold dawn; harsh shadows")
**Rule V1 — emotion through action**, always. Veo renders literal physical descriptions.
**Rule V2 — ONE camera move per shot.** Veo degrades on stacked moves.
**Rule V3 — name the pose/mechanics, not the concept** (TECHNIQUES: 御剑 = "feet on the blade").
**Rule V4 — keep the no-text + (usually) no-voice clause** unless it's a voiced 角色-dialogue shot
(then drop no-voice and attach the 角色 — PROVEN path).
Flat vs engaging (same subject):
- ❌ "a beautiful mountain" → ✓ "low-angle ECU: a mortal's mud-caked hand; a flying-sword immortal's
  shadow sweeps across it; the hand freezes. 3s static-to-push. cold dawn, a blade of gold cutting in."

---

## Quick checklist (run before locking any act's shot list)
- [ ] Row 1 is a hook (detail/conflict + question in 3s), not an empty wide
- [ ] ≥1 character CU/MCU, early
- [ ] Theme is SHOWN via contrast/paired-angles, not only narrated
- [ ] No two identical 景别 back-to-back; coverage spine touched (≥3 sizes/scene)
- [ ] No camera move repeated twice in a row; power beats use paired low/high angles
- [ ] 剪辑时长 planned per shot (varied; tension shortens, release lengthens)
- [ ] Exactly one designed highlight moment
- [ ] Each prompt = layer-cake, emotion-via-action, one move per shot
