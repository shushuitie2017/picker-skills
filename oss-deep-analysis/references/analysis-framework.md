# Analysis Framework

The dimensions to cover when analyzing an open-source project, what to look for in each, and how to turn raw facts into a defensible read. Work through these against the `repo_facts.json` you gathered plus your own reading of the repo.

## Contents
- [Reading signals: strong / mixed / weak](#reading-signals)
- [Dimension 0 — What it solves (the thesis)](#d0-thesis)
- [Dimension 1 — Architecture & how it works](#d1-architecture)
- [Dimension 2 — Maturity stage](#d2-maturity)
- [Dimension 3 — Code health](#d3-code-health)
- [Dimension 4 — Community & maintenance](#d4-community)
- [Dimension 5 — Adoption & ecosystem](#d5-adoption)
- [Dimension 6 — Competitive landscape](#d6-competition)
- [Dimension 7 — Defensibility (moat)](#d7-moat)
- [Dimension 8 — License & legal](#d8-license)
- [The verdict & the counter-argument](#verdict)

<a id="reading-signals"></a>
## Reading signals: strong / mixed / weak

Each dimension gets a one-word signal, tied to evidence. Use these consistently (English or 强/中/弱):

- **Strong / 强** — multiple positive indicators, no major red flag. Safe to rely on for this dimension.
- **Mixed / 中** — genuine positives offset by a real concern; usable with eyes open.
- **Weak / 弱** — a material problem a careful adopter would not ignore.
- **Insufficient evidence** — you genuinely could not determine it. This is an honest, allowed answer; do not bluff a signal.

The signal is a summary of evidence, not a vibe. If you write "weak", the findings under it must show *why*.

<a id="d0-thesis"></a>
## Dimension 0 — What it solves (the thesis)

Before anything technical, pin down what the project is *for*. Push past the marketing one-liner to a specific, falsifiable statement of the problem and the user.

- Weak: "a fast web framework." Strong: "an ASGI framework for Python teams who want type-hint-driven request validation and automatic OpenAPI docs without a separate schema layer."
- Identify the intended user precisely (which role, which stack, which scale), and the *one* thing this project does that made someone build it instead of using what existed.
- Note the scope boundary the project deliberately draws — what it explicitly does *not* try to be is often the most revealing line in a good README.

This becomes the report's "What it solves" section and anchors everything after it: every later judgment is relative to *this* purpose.

<a id="d1-architecture"></a>
## Dimension 1 — Architecture & how it works

The goal is a mental model a reader could hold in their head, not a file tour.

- The core abstraction(s): what are the 2–4 nouns the whole system is organized around? How do data and control flow between them?
- The tech stack and key dependencies — and whether those choices are conservative (boring, stable) or bleeding-edge (powerful, riskier).
- Notable design decisions and the tradeoffs behind them (e.g. "plugin architecture buys extensibility at the cost of a heavier core"; "zero-dependency by design, so it reimplements things you might expect to import").
- Extensibility surface: plugins, hooks, an API/SDK, config. The breadth here later feeds the moat (lock-in) analysis.
- Where the complexity concentrates — the module a new contributor would dread touching.

Read enough source to be honest. The entry point, the main module(s), and the public API are usually enough to form the model; you do not need to read everything.

<a id="d2-maturity"></a>
## Dimension 2 — Maturity stage

Place the project on a five-stage scale (the report timeline mirrors this). This is the single most useful framing for "can I rely on it".

1. **Prototype / 原型** — proof of concept, API churns freely, expect breakage. Fine to learn from, risky to depend on.
2. **Early / 早期** — usable, real users, but pre-1.0 energy: APIs still move, docs partial, sharp edges.
3. **Production-ready / 生产可用** — stable releases, semver discipline, real adoption, docs you can onboard from. The sweet spot for adoption.
4. **Mature / 成熟** — battle-tested, broad adoption, deep ecosystem, slow and deliberate change. Reliable; innovation may have moved elsewhere.
5. **Maintenance / Declining / 维护 · 衰退** — stable or stagnant; few new features; watch for slowing cadence, unanswered issues, maintainer burnout, or an explicit "looking for maintainers" notice. Depending on it is a bet on its longevity.

Read the stage from evidence, not self-description: release cadence and recency, version number and semver behavior, breaking-change history, docs completeness, and the issue/PR backlog shape. A repo can call itself 1.0 and behave like a prototype, or sit at 0.x and be rock solid — judge by behavior.

<a id="d3-code-health"></a>
## Dimension 3 — Code health

Whether the codebase is something a team could live inside.

- **Tests** — is there a test suite at all? Does CI run it? Rough coverage signal (a `tests/` dir and CI config is a baseline; coverage badges or config strengthen it). Absence is a real finding.
- **Documentation** — README depth, a docs site, inline docs/docstrings, a changelog, contributing guide. Can a newcomer get from zero to running?
- **Type safety / static analysis** — type hints/types, linters, formatters, type-checker config. Signals engineering rigor.
- **Structure & complexity** — coherent module boundaries vs a sprawl; size (LOC) relative to the problem; obvious hot spots.
- **CI/CD & release hygiene** — automated tests, releases, security scanning; lockfiles; reproducible builds.

Tie each to evidence from the facts (CI files found, test dir present, LOC, languages). "No tests directory and no CI configuration found" is a stronger, more useful line than "testing could be better".

<a id="d4-community"></a>
## Dimension 4 — Community & maintenance

Often the deciding dimension for a dependency, and the one a README cannot fake.

- **Cadence & recency** — commits in the last 90 days / year; date of last commit and last release. Recency matters more than lifetime totals.
- **Bus factor / contributor concentration** — how many people actually commit, and what share comes from the top one or two? A project that is 90% one person is a continuity risk no matter how good the code is.
- **Responsiveness** — are issues and PRs being triaged and answered, or piling up untouched? Ratio and age of open issues; stale-PR graveyard?
- **Governance & backing** — individual hobby project, company-backed, or foundation-governed (CNCF, Apache, etc.)? Backing changes the longevity calculus.
- **Trajectory** — accelerating, steady, or slowing? A clearly slowing curve on a project you'd depend on is a flag worth surfacing prominently.

<a id="d5-adoption"></a>
## Dimension 5 — Adoption & ecosystem

Evidence that others rely on it — treated as supporting, not decisive.

- Stars/forks/watchers as **popularity** signals (explicitly not health). Package-registry downloads and dependent-count are stronger "real usage" signals than stars.
- Notable production users, integrations, and a third-party ecosystem (plugins, extensions, tutorials, SO/Discord activity).
- Breadth of the ecosystem feeds back into the moat analysis (more integration surface → more lock-in).

Always caveat star-driven claims. A 40k-star repo last touched two years ago is a museum, not a dependency.

<a id="d6-competition"></a>
## Dimension 6 — Competitive landscape

No project exists alone. This becomes the comparison matrix.

- Name the real alternatives (direct competitors, the "boring" incumbent, and the build-it-yourself option).
- For each: the axis on which it differs from the subject (performance, ergonomics, ecosystem, license, maturity, scope).
- **When to pick which** — the genuinely useful output. "Pick X if you need A; pick the incumbent if you need B." Resist declaring a universal winner.
- Apply the counter-bias move here: make the most compelling case for why a *competitor* would be the better choice. If that case is strong, that is itself a finding about the subject.

<a id="d7-moat"></a>
## Dimension 7 — Defensibility (moat)

Why this project persists rather than being displaced — and, for an adopter, how hard it is to *leave* once embedded.

- Accumulated depth: domain-specific correctness, edge cases handled that a generalist alternative gets wrong, years of refinement.
- Network/ecosystem effects: integrations, plugins, and a community that compound over time.
- Switching cost / lock-in for adopters: how deeply it embeds into a user's workflow, data, and other tools — the deepest form being "others build on top of its API/SDK".
- For a *fork* decision, invert it: is the moat thin enough (and the maintenance gap real enough) that a fork is viable?

<a id="d8-license"></a>
## Dimension 8 — License & legal

Short, factual, and decision-relevant — never legal advice.

- Identify the license precisely (MIT, Apache-2.0, BSD, GPL/AGPL family, MPL, BSL/SSPL/source-available, dual-license, or none).
- Flag the practically important implications: permissive vs copyleft (and whether copyleft reaches across a network boundary, as AGPL does), patent grants (Apache-2.0), and source-available licenses (BSL/SSPL) that restrict commercial/hosted use — these are the ones that surprise teams.
- Note CLA/DCO requirements if contribution is on the table, and any unlicensed code (the riskiest case — "no license" means no permission by default).
- State that this is a factual summary, not legal advice, and the team should confirm against its own use case.

<a id="verdict"></a>
## The verdict & the counter-argument

Close with a single clear call, framed for a decision-maker.

**Recommendation tiers** (a tech-radar-style scale):
- **Adopt** — proven; default choice for the stated use case.
- **Trial** — promising; worth a real pilot on a non-critical path.
- **Assess** — interesting; worth understanding, not yet worth betting on.
- **Hold** — avoid for new work (immature, abandoned, risky license, or better options exist).

The verdict must specify **for whom and for what** — the right answer differs for "depend on it in production" vs "fork and learn from it" vs "contribute to it". State the use case the tier is conditioned on.

**The required counter-argument.** End with the strongest honest case *against* the recommendation — the reason a thoughtful skeptic would push back. This is not a disclaimer; it is the antidote to having quietly assembled a one-sided case. If you find you cannot articulate a real counter-argument, treat that as a signal you have not dug hard enough, and go back to the evidence.
