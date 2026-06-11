---
name: oss-deep-analysis
description: Produce a rigorous, beautifully-rendered deep analysis of any open-source project (a GitHub or GitLab repo, a library, a framework, a CLI tool, an SDK) and output it as a single self-contained editorial HTML report. Use this whenever the user wants to evaluate, understand, review, 解析, 分析, 调研, or do a deep dive on an open-source project, library, or repository — whether they are deciding whether to adopt it, contribute to it, fork it, depend on it, or just learn from it — even if they only paste a repo URL or a project name. Covers value proposition, architecture and how-it-works, maturity staging, code health, community and maintenance signals, adoption and ecosystem, competitive landscape, defensibility (moat), license and legal risk, and a clear adopt/trial/assess/hold verdict with a deliberate counter-argument. Always gathers facts from the repo (README, docs, manifests, git history, host API) before judging, then renders the result in a distinctive cinnabar-on-paper editorial style.
license: For the user's own use. The bundled fonts are loaded from Google Fonts at render time and are not redistributed.
---

# Open-Source Deep Analysis

Turn any open-source project into a single, self-contained editorial HTML report that an experienced engineer would actually trust: evidence first, judgment second, and an honest counter-argument at the end.

The output is one `.html` file in the cinnabar-on-paper "dossier" style defined in `references/design-system.md`.

## The stance that makes this worth doing

Three principles run through every section. They are the whole point — keep them in mind the entire time.

1. **Gather before you judge.** A star count or a slick README is not evidence that a project is healthy, well-architected, or worth depending on. Pull the actual signals — commit cadence, contributor concentration, release history, test presence, license, open-issue shape — *before* forming an opinion. An assessment that leads with vibes is worse than no assessment.
2. **Show the evidence inline.** Every claim in the report should be traceable to something concrete: "last release 14 months ago", "87% of commits from one author", "no CI config found". The reader is making a real decision (adopt / depend / fork); give them the basis, not just the conclusion.
3. **Argue the other side on purpose.** The most common failure when evaluating a project you already like is confirmation bias with a research engine attached — it is easy to assemble a polished case for a bad choice. So the report must include a deliberate counter-argument: the strongest reason *not* to adopt it. If you cannot make that case convincingly, you have not finished the analysis.

(The maturity-staging and moat/counter-argument lenses below are adapted from the AI-native startup lifecycle framing — Idea → MVP → Launch → Scale, the "moat", and the "make the case you'll lose" exercise — and repurposed for evaluating a codebase rather than a company.)

## Workflow

### Step 1 — Establish the target and gather facts

Figure out what you are pointed at. Accept any of: a repo URL (GitHub/GitLab), `owner/repo`, a local path to a clone, or just a project name (resolve it to a repo with a quick search if needed, and confirm with the user if ambiguous).

Then gather a structured fact base. Use the bundled helper:

```bash
python scripts/gather_repo.py <github-url | owner/repo | local-path> --out repo_facts.json
# optional: GITHUB_TOKEN=... in the environment lifts API rate limits
```

It degrades gracefully — if a tool (`git`, `tokei`/`cloc`) or the network is missing, it records `null` for that field and keeps going, and prints a short summary of what it could and could not collect. Read `repo_facts.json`, and read whatever it could not fetch yourself (e.g. open the README, skim `pyproject.toml`/`package.json`/`Cargo.toml`/`go.mod`, look at the top-level directory layout, scan a few core source files to understand the architecture). For anything that materially affects the verdict and is still missing, fetch it directly rather than guessing.

Do not skip this step even for a project you think you already know well — current maintenance state, latest release, and contributor concentration all change, and they are exactly the things a stale impression gets wrong.

### Step 2 — Analyze across the dimensions

Read `references/analysis-framework.md`. It defines the dimensions to cover, what to look for in each, how to read a signal as strong / mixed / weak, the verdict tiers, and the required counter-argument. Work through them against the facts you gathered. It is fine for a dimension to be "insufficient evidence" — say so plainly rather than padding.

### Step 3 — Render the report

Read `references/design-system.md`, then build the HTML by **copying** `assets/report-template.html` and replacing its placeholder content.

- **Do not rewrite or regenerate the CSS.** The aesthetic is the skill's signature; the template's `<style>` block is the source of truth. Edit content, not design tokens. (You may add a new content block that reuses existing classes.)
- The template is a working example with HTML comments marking each region and the repeatable blocks (dimension cards, competitor rows, risk cards). Duplicate or delete those blocks to fit the project — a project with two real alternatives gets two rows, not five empty ones.
- Fill the maturity timeline by marking the project's current stage as active and leaving the rest inert.
- Keep prose tight and evidence-bearing. This is a dossier, not a blog post: short declarative sentences, concrete numbers, no filler.

The report must contain, in order:

```
1. Hero            — project name (and CN gloss if useful), one-line tagline, meta bar
                     (primary language · license · stars · activity · maturity stage)
2. Verdict snapshot — the adopt/trial/assess/hold call + one-sentence rationale, up top
3. What it solves   — the problem, stated as a specific testable claim; who it's for
4. Maturity         — the five-stage timeline with the current stage marked
5. Dimension cards  — architecture & how-it-works, code health, community & maintenance,
                     adoption & ecosystem (each: summary line, findings, evidence note, signal)
6. Competitive matrix — this project vs named alternatives; when to pick which
7. Risks & red flags  — including the deliberate counter-argument ("why NOT adopt")
8. The verdict        — recommendation tier, for-whom, the counter-case, repo/docs links
9. Footer             — provenance: that it's an analysis, the source repo, the date
```

### Step 4 — Present it

Save the file to `/mnt/user-data/outputs/<project>-analysis.html` and present it with `present_files`. Give a brief summary of the headline finding and the verdict in chat — do not narrate the section list back.

## Notes on doing this well

- **Honesty over flattery.** If the project is abandoned, single-maintainer, or risky to depend on, the report says that clearly and early. A reassuring report about a dying dependency is the harmful outcome here.
- **Signals, not scores you can't defend.** Use the strong/mixed/weak (or 强/中/弱) signal pills from the framework, each tied to evidence. Avoid inventing precise numeric scores (e.g. "8.4/10") that imply false precision.
- **Stars are popularity, not health.** Treat adoption metrics as one weak signal among many, and say so where it matters; weight maintenance and code-health signals higher for a "should I depend on this" question.
- **Non-code targets.** The same structure adapts to a dataset, a spec/standard, a protocol, or a design-system project — swap "architecture" for "structure/schema" and "code health" for "completeness & upkeep", keep everything else.
- **Right-size it.** A tiny single-file utility does not need the full nine sections stretched thin; collapse empty regions. A large framework warrants the full treatment. Match depth to the subject.
