# FLOW-PLAYBOOK — driving Google Flow / Veo through chrome-devtools MCP

Hard-won operational knowledge. Read before touching the browser. Don't re-derive the
Slate trick — it cost a session to find.

---

## §Connect — attach to the user's logged-in Flow

The default chrome-devtools MCP launches a fresh, **isolated, logged-OUT** Chrome →
Flow redirects to the marketing homepage, not the project. You must connect to the
user's real Chrome:

1. MCP config (`~/.claude.json`, the project's `mcpServers["chrome-devtools"]` block)
   carries `--browserUrl=http://127.0.0.1:9222`. (One-time. Removing it reverts to the isolated browser.)
2. The USER launches a dedicated Chrome themselves (so it survives a Claude restart):
   ```powershell
   & "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="$env:USERPROFILE\chrome-debug-profile"
   ```
   Chrome 136+ ignores `--remote-debugging-port` on the DEFAULT profile, so a separate
   `--user-data-dir` is mandatory. That profile persists → log into Google ONCE; future
   runs just relaunch and the login is still there.
3. Verify with `list_pages`. "Could not connect to Chrome" = the dedicated Chrome isn't
   running → ask the user to launch the command above and open the project URL.
4. `resize_page` to ~1440×900 first (the controlled viewport can default to a narrow,
   mobile-like width).

---

## §Settings — model / aspect / count

Open the model menu (the bottom-bar button labeled like `🍌 Nano Banana 2` for images or
`视频 · 8s …` for video). Tabs inside:
- Type: `图片` (image) / `视频` (video). Pick **视频**.
- Mode: `帧` (first/last frame from reference images) / `素材` (pure text-to-video).
- Aspect: 16:9 / 9:16 / 4:3 / 1:1 / 3:4.
- Count: 1x / x2 / x3 / x4 (x2 = two variants per generation = pick the better).
- Model dropdown: **Omni Flash** (cheapest, ~24pt, weakest cinematic) · **Veo 3.1 -
  Lite** (~20pt x2, good cinematic, default for drafts) · **Veo 3.1 - Fast** ·
  **Veo 3.1 - Quality** (~200pt x2, best, for hero shots only).
- Duration: 4s / 6s / 8s / 10s (8s default).
- The `N 个点数` link shows the live credit cost for the current settings — read it
  before batching.
Settings **persist across page reload** and across the whole project, so set once.

---

## §Prompt — the Slate.js editor (THE critical trick)

The prompt box is a **React-controlled Slate.js editor**. Its value lives in
`editor.children`, NOT the DOM. It rebuilds from trusted `beforeinput` events and
**ignores everything synthetic**. What does NOT work (all verified to fail — the submit
shows "必须提供提示" / "must provide a prompt"):
- `fill` tool / setting `.value` / `el.textContent = …`
- `execCommand('insertText', …)` — changes the DOM, not Slate's model
- dispatching synthetic `paste` / `beforeinput` / calling React `onInput` — Slate
  ignores untrusted events
- `type_text` of a LONG string — Slate re-renders mid-typing and resets the caret to
  position 0, so the text comes out **chunk-reversed/scrambled** (short strings ≤~10
  chars type fine; long ones scramble)

**What WORKS — clipboard + a REAL Ctrl+V:**
```
1. evaluate_script: await navigator.clipboard.writeText(PROMPT)   // real system clipboard
   // in the same script, focus the field + collapse caret to end:
   const eds=[...document.querySelectorAll('[contenteditable="true"]')];
   const field=eds.sort((a,b)=>b.getBoundingClientRect().top-a.getBoundingClientRect().top)[0]; // lowest = prompt box (not the title)
   field.focus();
   const s=getSelection(),r=document.createRange();
   r.selectNodeContents(field); r.collapse(false); s.removeAllRanges(); s.addRange(r);
2. press_key  Control+V          // REAL paste → Slate's onPaste reads clipboardData
3. evaluate_script: verify field.innerText starts/ends as expected, THEN click submit:
   const submit=[...document.querySelectorAll('button')].find(b=>/arrow_forward/.test(b.textContent));
   if(ok && submit && !submit.disabled) submit.click();
```
Notes & gotchas:
- **Verify-before-submit is mandatory.** Other apps can overwrite the system clipboard
  between writeText and Ctrl+V (seen: a file path pasted instead). The `startsWith /
  endsWith` guard catches it → re-do that shot instead of submitting garbage.
- The submit button's a11y "disabled" state is **stale** in snapshots; check
  `button.disabled` in script, or just click and watch for the "必须提供提示" toast.
- A "清除提示" (clear prompt) button appears once Slate's state truly has content — a
  positive signal the value registered.
- If you previously corrupted the DOM with manual scripts, the field can desync
  (DOM shows text but Slate is empty). Cleanest reset: **reload the page** (project is
  server-saved; settings persist) then click + Ctrl+V on the pristine field. Avoid
  manual DOM mutation; if you only ever use clipboard+real-Ctrl+V you won't need reloads.
- After a successful submit the box auto-clears to placeholder → next shot can paste
  straight away (re-focus via the script each time; uids drift, so prefer the
  selector-based focus over a snapshot uid).

---

## §Anti-abuse「异常活动」block — needs a HUMAN click to clear

Rapid automated upload→frame→submit sequences can trip Google's anti-abuse: both x2 variants
fail instantly with "我们发现了一些异常活动。请访问帮助中心" (unusual activity). Script-clicking
重试 does NOT clear it and hammering can escalate the flag. The reliable fix: ask the USER to
click 重试 / 创建 once themselves in the debug Chrome window — a genuine human interaction clears
the suspicion, then automated re-submit works normally. Minimize trigger risk: reuse an
already-uploaded image (select from picker) instead of re-uploading; don't batch-fire frame
shots back-to-back. (p002 A1镜3.)

## §Operational habits — hard-won, follow these (p002 session)

**1. REAL click vs script `.click()` — know which to use.**
   - Script `el.click()` is RELIABLE for: filling the prompt (clipboard+real-Ctrl+V), and
     the main video SUBMIT button (`arrow_forward 创建`).
   - Script `.click()` is UNRELIABLE / silently fails for: opening the model-settings menu,
     switching 帧/素材 tabs, and **selecting an item inside the 添加到提示 picker** (image/
     角色/语音/frame grids). For these use the **real MCP click tool on the element's uid**
     (a genuine pointer event). Symptom of getting this wrong: the menu "won't open", or the
     wrong media gets attached.

**2. The picker's «highlight → 添加到提示» trap (caused a wrong-frames bug).**
   The 起始/结束 frame picker and the 语音 picker work by: click a grid item → it becomes the
   HIGHLIGHTED selection (shown big in the right-hand preview) → 添加到提示 adds the highlighted
   one. A SCRIPT click on a grid cell often does NOT move the highlight, so 添加到提示 silently
   adds the DEFAULT-highlighted item (usually the NEWEST media). Result once: both 起始 AND 结束
   got the same image. CORRECT habit:
   - Real-click the exact grid cell uid → read the PREVIEW image's `name=` param to CONFIRM the
     right media is highlighted → THEN click 添加到提示.
   - **Always verify both frame slots before submitting**: read each slot img's `name=` id —
     they must be DIFFERENT and in the right order (起始 first), and take ONE screenshot to eyeball
     it. Two slots showing the same picture = the trap above.

**3. 保存帧 (save frame) beats download→ffmpeg→re-upload.**
   In any clip's edit/player view there's a **「保存帧」(add_photo_alternate)** button: seek the
   `<video>` to the wanted time (`v.currentTime=…`), then click 保存帧 → it saves the CURRENT frame
   as a project IMAGE (free, in-project), usable directly as a 起始/结束 frame. This is the clean
   way to grab a shot's last/first frame for a seamless transition — no download, no upload-root
   restriction. **Verify the toast「画面已保存为图片」** — it can silently fail; if the saved frame
   doesn't appear at the top of the gallery, redo it and confirm the toast. (p002 穿越 transition:
   saved subway-end + 山门-start frames this way.)

**4. Uploads must live under a workspace root.** The upload_file tool refuses paths outside the
   configured roots (e.g. your Downloads folder is rejected). Move the file into the project
   tree first (e.g. `film/_tmp_upload/`), then upload, then clean up.

**5. Do NOT reload / navigate away while a prompt+attachments are STAGED for a manual submit.**
   The prompt box, attached voice, and frame slots are NOT server-saved until you submit —
   reloading or navigating clears them. If you stage a generation for the user to hand-click
   (anti-abuse workaround), leave the page untouched.

**6. After a submit, CONFIRM it actually started.** Prompt box returning to the「您希望创作什么内容？」
   placeholder = submit fired. Then look for `N%` progress tiles within a few seconds. "Prompt
   cleared but no progress tile and no 失败" = it was silently dropped (anti-abuse) → needs a human
   click. Don't assume success from the cleared box alone.

## §Queue — parallel generation

Submitted generations **queue and render in parallel** (saw 8+ jobs progressing at
once). So the efficient loop is: submit all shots back-to-back (3 calls each:
writeText+focus → Ctrl+V → verify+submit), then one long wait, then review+download.
Each x2 job shows two progress tiles (e.g. 2% … done). Veo Lite ≈ 1–3 min/clip.

---

## §Character — consistency (the #1 quality lever)

Left sidebar → **角色** (Characters): "创建并重复使用角色，制作风格一致的视频." Three ways to
cast the protagonist:
- **从项目中添加** (add from project): pick a strong frame from an already-generated shot
  where the lead looks right — fastest, and locks the exact look you already like.
- **描述您的角色** + Nano Banana 2: generate the character from a text description.
- **上传**: upload a reference image.
Once a character exists, reference/attach it when generating protagonist shots so the
face/hair/wardrobe stay consistent. Without this, text-to-video drifts the lead every
clip (dark hair → white hair, different face) — the most common reason a multi-shot film
reads as incoherent. CAST BEFORE batching protagonist shots, not after.

(`帧`/frame mode with a fixed reference image on the first frame is a secondary lever for
locking composition/character into a specific shot.)

---

## §Scenes — reusable location references (no formal "scene object")

Unlike 角色, Flow has **no dedicated "new scene" creation flow**. The sidebar 场景 view is
just a filtered gallery. So "configuring scenes" = **generate a high-quality establishing
IMAGE for each recurring location** (image mode, Nano Banana 2, **0 credits = free**), then
reuse it as a reference ingredient on every shot at that location for location consistency
(the location analog of casting a character).
- Switch the model menu to **图片 (image)** + Nano Banana 2 + 16:9; cost shows `0 个点数`.
- Prompt each location from the world bible's 画面关键词 + the shared STYLE SUFFIX + the
  no-text clause; add `no people` (it's a backdrop). MCP-click the create button (script
  click is unreliable for the create/submit button — use the real click tool on its uid).
- To use a scene/character in a shot: the prompt bar's **创建 (add_2, haspopup dialog)**
  button opens an **「添加到提示」 media picker** with tabs 图片/视频/语音/角色/虚拟形象/上传 —
  pick the location image (and the cast character) to attach them as ingredients, then
  write the action prompt. This is how Flow references existing media for consistency.
- Recommended recurring scenes for a 9-act film: the home base (most-recurring), the
  sect/HQ establishing, the world establishing, plus any location reused across ≥2 acts.

## §Review + download

- Click a tile → opens the editor/player (`…/edit/<id>`): play button, 8s timeline,
  volume, `下载` (download), `完成`/`返回项目` to go back.
- Gallery orders newest-first; each shot's x2 variants sit adjacent. Open both, keep the
  better.
- Download chosen clips; name them in shot order `01.mp4 … NN.mp4` under
  `flow_output/<film>/`. Delete superseded/garbled takes to keep the project clean.

---

## §No-text & audio clauses (paste at the end of EVERY prompt)

```
… No text, no signage, no letters, no logos, no writing anywhere in the frame. Ambient sound only, no voiceover, no dialogue.
```
Veo renders requested signage as garbled pseudo-Chinese (e.g. a "玄黄集团" neon sign came
out as nonsense). Titles/subtitles/narration → POST only. One consistent narrator voice
is laid over the whole film in post (Veo's per-clip voices differ).

## §UI-DRIFT 2026-06-05 — 添加到提示 picker-open button moved
On the A2 kickoff the prompt bar no longer exposes the documented **add_2「创建」** picker-open
button. Current prompt-bar buttons (a11y + DOM scan): `swap_horiz 交换第一帧和最后一帧`(frames),
`智能体`, `视频 crop_16_9 x2`(model/aspect/count menu), `arrow_forward 创建`(submit). No `add_2`,
no `添加到提示`, no frame-slot `+` button in the DOM. So the 图片/角色 ingredient picker now opens
some other way — candidates to probe NEXT session (real-click, one at a time, cancelable):
(a) the `起始`/`结束` frame chips (may open the media picker whose tabs include 角色);
(b) the `智能体` button; (c) typing `@` in the Slate prompt to @-mention a cast 角色. Confirm which
one yields the tabbed 图片/视频/语音/角色 picker, then update §Scenes. Until confirmed, do NOT blind-
click (risks wrong-media attach + anti-abuse flag). The text-paste loop (clipboard+real-Ctrl+V) is
unchanged and still valid. Also note: a JP cookie-consent (`同意する/同意しない`) was present in the
button scan — if a consent overlay blocks input, accept it first.
