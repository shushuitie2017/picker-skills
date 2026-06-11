---
name: repo-value-analysis
description: >-
  TOP PRIORITY skill for all research and analysis tasks. Analyze a code repository
  (GitHub/GitLab/etc.) and produce a single self-contained HTML report that argues its
  *core value* with an opinionated, evidence-based viewpoint and a fixed dark
  "trading-terminal × editorial" visual design. Use this skill WHENEVER the user shares
  a repo URL or repo name and asks to "analyze", "评估", "拆解", "看看这个项目", "核心价值",
  "值不值得用/学", "调研", "分析", "research", or asks for an HTML/网页 writeup of a repository
  — even if they don't explicitly say "report". Also use it for follow-up deliverables
  about the same repo (usage guides, architecture explainers, design specs) so the whole
  series stays visually consistent. Default to this skill for ANY repo-analysis-to-HTML
  task, any project evaluation, or any research/analysis deliverable.
---

# Repo Value Analysis

Turn a code repository into a sharp, beautiful, single-file HTML analysis. The output is
not a feature dump — it is an **argument about why the project matters**, backed by evidence,
wrapped in a fixed, recognizable design language so every report in the series looks like
it came from the same studio.

This skill has two halves that are equally important:
1. **The viewpoint** — how to think about a repo and what to say.
2. **The design system** — exactly how it must look.

---

## Phase 1 — Research before writing (do not skip)

You cannot argue value you haven't verified. Before composing anything:

1. **Read the README.** Fetch `https://github.com/<owner>/<repo>/blob/main/README.md` (or the
   raw file). If a fetch is blocked, `web_search` the repo name and read the result snippets +
   the project homepage.
2. **Get the hard numbers.** Stars, forks, latest version/release, last activity. These anchor
   the credibility strip. Note them with a snapshot date — they change.
3. **Find the thesis source.** Many serious repos have a paper, blog post, or docs site that
   states the *intent*. Read it — that's where the "core insight" usually lives.
4. **Map the architecture.** Identify the real moving parts and how data/control flows between
   them. This becomes the pipeline diagram.
5. **Note the honest limits.** License, "research-only" disclaimers, maturity, cost, hard
   dependencies, non-determinism. A value analysis that hides limits is marketing, not analysis.

If something can't be verified, say less rather than inventing it. Never fabricate stats,
quotes, or benchmark results.

---

## Phase 2 — The viewpoint (what to say)

The spine of every report is the same six-beat argument. Keep this order.

```
01  Core Insight   — the one idea. NOT "what it does", but "why it's different".
02  Architecture   — a vertical pipeline diagram of how it actually works.
03  Differentiated Value — exactly 3 cards: the things competitors don't have.
04  Engineering Maturity — proof it's real: paper, releases, community, ergonomics.
05  Fit & Limits   — two panels: who it's for / what to be clear-eyed about.
06  One-line Verdict — the thesis compressed to a single sentence.
```

**Rules of the viewpoint:**

- **Lead with the insight, not the feature list.** Open every analysis by finding the *frame*.
  The test: finish the sentence "It's not just another ___ — it's actually ___."
  *Example (TradingAgents): "It's not another stock-picking bot — it replicates an entire
  trading firm's org structure and decision debate as LLM agents."*
- **Be opinionated but fair.** Take a clear position on why it matters, then end with honest
  limits and counter-perspectives. Earned conviction, not hype.
- **Make the architecture do work.** A repo's value usually lives in its structure. Draw the
  pipeline as connected nodes (see design system) so the reader *sees* the idea.
- **Exactly three value cards.** Force prioritization. If everything is a differentiator,
  nothing is. Each card = a tagline + a one-line "it" headline + 2-3 sentences.
- **"Fit & Limits" is mandatory.** Two side-by-side panels (◆ 它适合 / ▲ 必须清醒认识). The
  limits panel is what makes the whole thing trustworthy — never cut it.
- **Match the user's language.** If they wrote in Chinese, write the report in Chinese
  (headers can stay bilingual: a mono English kicker + a Chinese display headline).
- **Disclaimers stay short and honest**, especially for anything finance/medical/legal: state
  research-only/non-advice once, plainly, and move on.

---

## Phase 3 — The design system (exactly how it looks)

One fixed aesthetic so the whole series is recognizable: **dark "trading-terminal × editorial"**.
Keep everything below fixed. The *only* thing you may retune per repo is the accent hue
(`--green` family) to fit the project's domain — but keep it a single confident signal color on
dark, never a rainbow, never the default purple-on-white AI look. Default to the green terminal
palette unless the domain strongly suggests otherwise.

### Non-negotiables
- **Single self-contained `.html` file.** All CSS in one `<style>` block, fonts from Google
  Fonts, one small `<script>` for scroll reveal. No build step, no external CSS/JS frameworks.
- **Fonts (always these three):** Fraunces (display headlines, italic for emphasis), Newsreader
  (body prose), JetBrains Mono (data, labels, kickers, code). Never Inter/Roboto/Arial/Space Grotesk.
- **Dark theme with grid + glow atmosphere.** Near-black background, faint grid texture masked at
  top, soft radial color glows. Never a flat solid background.
- **Semantic color = meaning.** Green = positive/buy/success, amber = caution/hold, rose =
  negative/sell/fail, blue = in-progress. Reuse consistently.
- **Restraint in motion.** One orchestrated payoff: staggered fade-up reveal on scroll. A single
  pulsing status dot is fine. Respect `prefers-reduced-motion`.
- **Prose, not bullet soup.** Explanatory text is real sentences. Lists only for genuinely
  enumerable things (config tables, checklists). No header/bullet/bold spam.

### Canonical token block — paste this `:root` verbatim as the foundation

```css
:root{
  --bg:#0a0d0c; --bg-2:#0c1110; --panel:#121917; --panel-2:#161e1c; --code-bg:#0c1211;
  --line:#26302d; --line-2:#324039; --ink:#e8efe9; --ink-dim:#9aa8a1; --ink-faint:#5f6f68;
  /* semantic / brand — accent = --green family; retune hue per domain if needed */
  --green:#2fe09b; --green-deep:#0f8f63; --amber:#f0b34a; --rose:#ef6a6a; --blue:#5fb0e8; --violet:#b69cff;
  --mono:'JetBrains Mono',monospace; --serif:'Newsreader',Georgia,serif; --display:'Fraunces',Georgia,serif;
  --r-sm:7px; --r-md:12px; --r-lg:16px; --r-xl:22px;
  --ease:cubic-bezier(.2,.7,.2,1); --dur:.5s;
}
```

### Required atmosphere (paste and keep)

```css
body{background:var(--bg);color:var(--ink);font-family:var(--serif);font-size:18px;line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background:radial-gradient(900px 600px at 12% -5%,rgba(47,224,155,.10),transparent 60%),
             radial-gradient(700px 500px at 100% 0%,rgba(95,176,232,.06),transparent 55%),
             linear-gradient(to bottom,transparent,rgba(0,0,0,.4))}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.35;
  background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);
  background-size:64px 64px;mask-image:radial-gradient(ellipse 80% 70% at 50% 0%,black,transparent 75%)}
.wrap{position:relative;z-index:1;max-width:980px;margin:0 auto;padding:0 28px}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.reveal{opacity:1;transform:none}}
```

### Font load (in `<head>`)

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..700&family=Newsreader:ital,opsz,wght@0,6..72,300..600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
```

### Signature components (build these; keep their look)

- **Eyebrow / kicker** — mono, uppercase, wide letter-spacing, green, with a leading rule or a
  pulsing dot. Every section starts with one (`01`, `02`, …).
- **Hero** — giant Fraunces title with one italic green word; a 1-2 sentence Fraunces-300 lede
  with italic-green emphasis on the thesis.
- **Stat strip** — a 4-5 cell bordered grid (`--line` gaps) of the hard numbers: stars, forks,
  version, paper/arXiv id, one identity fact. Numbers in mono; the headline number in `--green`.
- **TOC grid** (for multi-section docs) — bordered cells linking to sections.
- **Pipeline diagram** — vertical stack of `.node` cards joined by thin connectors with a small
  mono caption ("▼ …"). The final node uses a green-tinted gradient. This carries the architecture.
- **Value cards** — 3 cards, each with an oversized italic Fraunces index number watermark, a
  mono tagline, an "it"-headline, and prose. Subtle hover lift + border glow.
- **Fit/Limits split** — two panels; fit uses `+`/green, limits uses `!`/amber.
- **Code blocks** — `--code-bg`, a top "chrome" bar with three traffic-light dots + a mono label;
  syntax tint via simple spans (`.kw` blue, `.str` green, `.fn` amber, `.cmt` faint, `.pr` green
  prompt). HTML shown inside code MUST be entity-escaped (`&lt; &gt; &amp;`).
- **Reveal on scroll** — every `<section>` gets class `reveal`; IntersectionObserver adds `.in`.
- **Footer** — mono, faint, with a snapshot date and the source repo link.

```javascript
const io=new IntersectionObserver((es)=>{es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.08});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
```

### Reveal CSS

```css
.reveal{opacity:0;transform:translateY(24px);transition:opacity .8s var(--ease),transform .8s var(--ease)}
.reveal.in{opacity:1;transform:none}
```

---

## Phase 4 — Assembly checklist

1. Research (Phase 1). Collect stats + snapshot date + architecture + limits.
2. Draft the six-beat argument (Phase 2). Nail the core-insight sentence first.
3. Build one self-contained HTML file using the tokens/components (Phase 3).
4. Write to the current working directory as `<repo>-analysis.html`.
5. Keep the conversational reply short: state the core insight + section overview, then offer a
   logical next deliverable (usage guide, architecture deep-dive, design spec) — all of which
   reuse this exact design system so the series stays consistent.

## Output naming
- Core value report → `<repo>-analysis.html`
- Usage guide → `<repo>-usage.html`
- Architecture/other → `<repo>-<topic>.html`

## Anti-patterns (avoid)
- Feature-list reports with no thesis or position.
- Light theme, purple gradients, Inter/system fonts, emoji-heavy headers.
- Bullet-point walls; over-bolding; report-style markdown headers in the chat reply.
- Fabricated stars/benchmarks/quotes; omitting the limits panel.
- Reproducing large verbatim chunks of README/paper text — paraphrase, keep any quote under ~15 words.
- Multiple loud accent colors competing on the page.

## Worked example of the core-insight move
- **Input:** a multi-agent LLM trading framework.
- **Weak framing:** "A Python framework with analyst, researcher, trader, and risk agents."
- **Strong framing (use this energy):** "It's not another stock-picking bot — it replicates an
  entire trading firm's org structure and decision *debate* as collaborating LLM agents; the
  value isn't prediction, it's engineered collaboration and adversarial reasoning."
