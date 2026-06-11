# oss-deep-analysis

A Claude **Skill** that turns any open-source project into a single, self-contained
editorial HTML report — evidence first, judgment second, with an honest counter-argument.

It's a generalization of a deep-analysis workflow: gather the real signals about a
repo (commit cadence, contributor concentration, releases, tests, license, adoption),
reason across a fixed set of dimensions, and render the result in a distinctive
"cinnabar-on-paper" dossier style.

## Install

- **claude.ai** → Settings → Skills (or Capabilities) → upload this `.zip`.
- **Claude Code / Cowork** → drop the unzipped `oss-deep-analysis/` folder into your
  skills directory (e.g. `~/.claude/skills/`), or upload via the Skills UI.

Then just ask, e.g.:
> 帮我深度解析一下 tiangolo/fastapi，我在考虑要不要在生产里依赖它
> do a deep dive on https://github.com/owner/repo — should I fork it?

## What's inside

```
oss-deep-analysis/
├── SKILL.md                       # the workflow Claude follows
├── references/
│   ├── analysis-framework.md      # the dimensions, signal-reading, verdict tiers, counter-argument
│   └── design-system.md           # the "Cinnabar Dossier" aesthetic spec
├── assets/
│   └── report-template.html       # the editorial HTML skeleton (copy + fill; don't restyle)
└── scripts/
    └── gather_repo.py             # stdlib-only fact gatherer (local clone OR GitHub API)
```

## Notes

- `gather_repo.py` needs only Python 3. For best results run it on a **local clone**
  (full git history + LOC + manifests). For GitHub-API metadata (stars, releases,
  contributors), set `GITHUB_TOKEN` in the environment to avoid the unauthenticated
  60-requests/hour rate limit. It degrades gracefully if a tool or the network is missing.
- The report loads its fonts from Google Fonts at view time; open the `.html` in any browser.
- The maturity-staging and "moat / make-the-case-against" lenses are adapted from the
  AI-native startup lifecycle framing and repurposed for evaluating a codebase.
