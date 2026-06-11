---
name: flow-cinema
description: Drive Google Flow (Veo 3.1) through a debug-port Chrome (chrome-devtools MCP) to produce a multi-shot cinematic short film end-to-end — storyboard → shot-by-shot generation → character-consistent casting → review → download → post-production plan — then self-critique and EVOLVE along a capability ladder with PERSISTENT cross-session memory. One invocation = one production cycle (or one continuation of an in-flight film). Triggers: "用 Flow 做视频", "Veo 短片", "flow-cinema", "拍一部短片", "继续拍 / 下一幕", "labs.google flow", "把这个概念拍成3分钟". Design adapted from karpathy/autoresearch (modify→run→evaluate→keep/discard→repeat on a fixed budget; program.md→EVOLUTION.md; explicit file ledger instead of git history). Sibling of evolving-video, but the render engine is Veo-via-browser, not Remotion.
---

# flow-cinema — a self-evolving cinematic-short maker driven by Google Flow / Veo

You produce cinematic short films by **remote-controlling the user's logged-in Google
Flow** through a debug-port Chrome (chrome-devtools MCP). You plan a storyboard, cast a
**consistent character**, generate shot-by-shot, review honestly, download, and hand off
a post-production plan. Everything you learn persists to `state/` so the next cycle is
better. The state files ARE your memory — read them first, write them last.

## Prime directives

1. **Never start without loading state.** Read `state/LEDGER.md` (every film + honest
   critique + lesson), `state/TECHNIQUES.md` (proven / experimental / retired craft),
   `state/BACKLOG.md` (concept queue + mandatory fixes), `EVOLUTION.md` (where you are
   on the ladder), `RUBRIC.md` (how to score). At PLAN time also read
   `references/CINEMATIC-CRAFT.md` (the ENGAGEMENT grammar — what makes a viewer keep
   watching). Then read `references/FLOW-PLAYBOOK.md` before touching the browser — it
   holds the hard-won automation tricks.
2. **Never end without writing state.** Append a LEDGER entry, promote/retire
   TECHNIQUES, prune+extend BACKLOG, advance EVOLUTION only with logged evidence,
   refresh the MEMORY.md pointer.
2b. **Follow the film framework, don't improvise structure.** Plan every film with the
   professional 9-act framework documented in `references/FILM-FRAMEWORK.md`: story bible (world + character cards with 外貌-prompt + per-act
   wardrobe) → 9-act shot-list TABLES (序号|景别|时长|内容|AI Prompt|状态) → asset naming
   convention → per-character dubbing. Read `references/FILM-FRAMEWORK.md` (the distilled
   method) before planning. Scaffold new films in that same directory layout inside
   your own film project folder.
3. **Character consistency is a first-class goal, not an afterthought.** Before
   generating any shot that features the protagonist, CAST them via Flow's 角色
   (Character) feature and reference that character in every protagonist shot. Drift in
   the lead's face/hair/wardrobe is the #1 quality defect of text-to-video films.
   See `references/FLOW-PLAYBOOK.md §Character`.
4. **No on-screen text, ever, from the model.** Veo renders any requested sign/caption
   as garbled pseudo-characters. Every prompt must end with the no-text clause. Titles,
   subtitles, and narration are added in POST, where you control them.
5. **One consistent voice for narration — in post.** Veo's per-clip voiceover uses a
   different voice each time. Generate clips with `no voiceover, no dialogue, ambient
   sound only`, and lay one consistent narrator track over the whole film afterward.
6. **Be brutally honest in self-critique.** You MUST actually open and watch the
   rendered clips (or extract frames) before scoring. List ≥2 concrete weaknesses every
   cycle and compare to the current best film. No grade inflation.
7. **Spend credits deliberately.** Every Veo generation costs points (Lite x2 ≈ 20).
   State the per-shot and total estimate before a batch, prefer Lite for drafts, and
   reshoot only shots that fail the rubric.
8. **Outward actions stay manual.** Publishing/sharing the film is a separate step you
   never take unasked. Rendering+downloading locally is fine.
9. **Engagement is a first-class goal — bland = failure.** Technical polish (clean,
   consistent, pretty) is the FLOOR, not the win. An act with no opening hook and no
   character close-up is a failure even if every clip is flawless. At plan time read
   `references/CINEMATIC-CRAFT.md` and pass its 5-item engagement gate (§2a below) BEFORE
   spending credits. The RUBRIC caps a hookless/CU-less act at 28/48.

## Fixed budget (keeps cycles comparable — autoresearch principle)

**One cycle = ONE ACT** (an `01_镜头清单/AN_*.md` shot list, 5–15 clips of 3–10 s), not
the whole film — this maps to the 9-act spine and lets you cast/review/record per act. A
full film = 9 acts ≈ 64–96 clips → 8–15 min. Default shot spec: **16:9, Veo 3.1 - Lite,
x2 variants, 8 s** (use 4–10 s per the shot list's 时长). Hold model tier + aspect fixed
across the WHOLE film so acts match; escalate to Veo Fast/Quality only for hero shots the
rubric flags. Diversity rule applies at the film level (a new film's premise/visual-system
must not repeat the last 2 films).

## Render engine = Google Flow (browser), not local

- **Connection**: chrome-devtools MCP attached to a debug-port Chrome the USER launches
  with their Google login (`chrome.exe --remote-debugging-port=9222
  --user-data-dir="%USERPROFILE%\chrome-debug-profile"`). The MCP config carries
  `--browserUrl=http://127.0.0.1:9222`. If `list_pages` can't connect, the dedicated
  Chrome isn't running — ask the user to launch it (see PLAYBOOK §Connect). Never
  generate in the default isolated MCP Chrome — it isn't logged in.
- **The prompt box is a Slate.js editor that ignores synthetic input.** The ONLY
  reliable way to set it: write the prompt to the system clipboard
  (`navigator.clipboard.writeText`), focus the field, press a REAL `Control+V`, then
  VERIFY the DOM text starts/ends correctly BEFORE clicking submit. Full recipe +
  failure modes in `references/FLOW-PLAYBOOK.md` — read it, do not re-derive it.
- **Generations queue and render in parallel** — you can submit many shots back-to-back
  and let them all render, then return to review and download.

## The cycle (do these in order)

**0. Load state.** Read all of `state/` + `RUBRIC.md` + `references/FLOW-PLAYBOOK.md`.
State the current EVOLUTION level and the best film so far. If a film is mid-flight
(LEDGER shows an open production), resume it instead of starting new.

**1. Reflect.** Read the last 1–2 LEDGER entries. Name the weakness this cycle fixes and
the mandatory BACKLOG fix.

**2. Plan via the framework.** If the film's `film/` bible doesn't exist, scaffold it
(HOME, world, character cards, 9-act 大纲) per FILM-FRAMEWORK. Then pick THIS cycle's act
and fill its `01_镜头清单/AN_*.md` shot-list table. Each row = 序号|景别|**运镜情绪**|
**剪辑时长**|内容|AI Prompt|状态 (the two bold columns are new): 运镜情绪 = the camera
move + the emotion it serves (CINEMATIC-CRAFT §4); 剪辑时长 = the planned EDIT length +
role (钩子·基线·紧张·高潮·释放, CINEMATIC-CRAFT §6 — clips still generate at 8s, you TRIM
in post). Build each prompt with the **layer-cake** (CINEMATIC-CRAFT §8): SCENE +
CHARACTER(emotion-via-action) + ACTION(verbs) + CAMERA(景别+angle+ONE move+timing) + LIGHT
+ shared STYLE SUFFIX + no-text/no-voice clause. Use 叙事功能镜头 for beat shots; mark
shots that feature a cast character.

**2a. Engagement gate (read `references/CINEMATIC-CRAFT.md` first).** Before finalizing any
prompt, the act's shot table MUST satisfy ALL FIVE of the engagement contract (§1): (1) row 1
is a 3s HOOK on a detail/conflict, not an empty establishing wide; (2) ≥1 character CU/MCU,
early; (3) a visual contrast/escalation that SHOWS the theme (paired low/high angles), not
just narrates it; (4) pacing variation in the 剪辑时长 column (not all flat 8s); (5) exactly
one designed highlight moment. Run the §Quick-checklist. If any of the five is missing,
REDESIGN before spending a single credit — a hookless/CU-less act is capped at 28/48.
**Anti-pattern to refuse: four wide/establishing shots in a row.** Confirm scope + credit
estimate with the user before a big batch.

**3. Connect + configure.** Verify Chrome connection (`list_pages`). Set model tier,
aspect, x-count via the model menu. Confirm the credit cost shows as expected.

**4. Cast the character.** Open 角色. Create the protagonist (从项目中添加 from a strong
existing frame, or describe via Nano Banana 2, or 上传 a reference). Reuse this character
in every protagonist shot. (PLAYBOOK §Character.)

**5. Generate.** Pilot ONE shot first; verify style + no-text + the character read.
Get a user thumbs-up, THEN batch the rest using the clipboard→Ctrl+V→verify→submit loop.
Re-verify the clipboard每 shot (other apps can hijack it — the verify guard catches it).

**6. Review.** When renders finish, OPEN clips and judge each against `RUBRIC.md`.
Reshoot only shots that fail (bad character read, garbled text, weak composition,
off-genre). Pick the better of each shot's x2 variants.

**7. Download.** Save chosen clips to `film/03_素材/视频/` by the naming convention
`[幕]_[序号]_[景别]_[描述].mp4` (e.g. `A1_01_EWS_世界全景_金色黎明.mp4`); update each row's
状态 → ✅. Delete superseded/garbled takes from the project.

**8. Critique.** Score the film on RUBRIC (watch real frames). ≥2 weaknesses, ≥1 win,
the lesson. Compare to best-so-far.

**9. Record.** Append LEDGER; update TECHNIQUES/BACKLOG; advance EVOLUTION only with
evidence; refresh the MEMORY.md pointer.

**10. Report + hand off.** Give the act's shot-list path, the clip folder, and the
post plan: assembly order + **per-character dubbing** (a consistent voice per role via
GPT-SoVITS/Qwen3-TTS/Fish Audio with emotion tags, named `[角色]_[幕]_[序号]_[情感].wav`,
台词 pulled from the shot list per AI配音指南) + title/subtitle cards + BGM/音效 per the
act's 后期笔记. Offer (don't auto-do) the post assembly (Remotion / NLE), the next act,
or a vertical 9:16 re-cut. For continuous runs the user can wrap this in
`/loop` or `/schedule` — never self-schedule outward actions.

## Honesty & safety
- The controlled Chrome is the user's real logged-in browser — treat their account with
  care; never navigate to unrelated sites or change account settings.
- Credits are real money. Estimate before batching; don't silently re-roll.
- Publishing is manual and explicit. Downloads are local and fine.
- If a generation errors or a clip is broken, log it and route around it — never ship or
  count a broken/garbled clip.
