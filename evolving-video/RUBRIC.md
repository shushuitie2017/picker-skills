# EVALUATION — adversarial, verifiable, externally-grounded

## Why this was rewritten (2026-06-04)
The old /35 rubric FAILED: I authored the work, judged it against my own rubric, and
inflated the scores (called generic AnimateDiff montages "premium, 27/35"). Self-grading
with no ground truth is theater. New rules:

## Rule 0 — the only real score is the audience's
A self-score is NOT progress. It is, at best, a prediction. The fitness signal is REAL
engagement (views / saves / watch-time the user pastes into METRICS.md). Until a piece
has real numbers, its status is **UNVALIDATED — author's guess**, and the ledger must say so.
Never again claim a piece is good/"best" on a self-score alone.

## Rule 1 — judge as a hostile stranger, default to FAIL
Critique as someone who did NOT make it, is scrolling fast, owes it nothing, and assumes
it's AI slop until proven otherwise. The burden of proof is on the video. If you can't
PROVE a "pass" with a concrete on-screen reason, it fails.

## Rule 2 — a BLIND external reviewer is mandatory
Before recording any score, spawn a subagent (Agent tool) given ONLY the rendered
frames/clip + the goal (short-form retention), with NO hint that you made it and NO
rubric to please. Ask it to be brutal, name flaws, and answer the gate questions below.
Its verdict OUTWEIGHS yours. Log it verbatim in the ledger.

## Rule 3 — binary gate questions, not vibes (every one must be a defensible YES)
Answer each YES/NO with a concrete reason; any unproven YES = NO:
1. **Stop-scroll <1s?** Would a stranger stop in the first second? Why exactly?
2. **Distinct?** Name what's distinctive vs the 10,000 other AI-nature-clip-with-text videos. If you can't, it's generic → fail.
3. **Not AI-default?** Is it free of the tells (soft AI footage, centered text + fade, ambient pad, "satisfying" filler)? Be specific.
4. **One reason to send it to a friend?** State it in one sentence a real person would use. Vague = fail.
5. **Craft holds at 100%?** Watch real encoded frames — artifacts, warble, mushy upscales, readable on mute?
6. **Earns its length?** Every second pulls weight, or is it padding to hit a duration?
A piece that can't get ≥5/6 defensible YES is not shippable as "good" — log it as weak and say why.

## Rule 4 — compare to a real exemplar, not to my last piece
Name an actual high-performing video in the same lane (or describe its qualities) and
state, concretely, where this falls short of it. "Better than my last piece" is not a standard.

## Rule 5 — investigate before iterating
Each cycle: what specifically did real feedback (or the blind reviewer) say last time?
What did I change in response, and did it move the needle? If I can't point to a concrete
cause→change→effect, I'm not evolving, I'm shuffling. Write it down.

## Recording
Ledger entry must include: the blind reviewer's verdict (verbatim), the 6 gate answers
with reasons, the honest weak points, and `STATUS: UNVALIDATED` until real metrics exist.
No composite number unless it's tied to the gate answers — and it caps at "weak" until
the audience says otherwise.
