# Design System — "Cinnabar Dossier"

The signature look of this skill's output. The aesthetic is the product; reproduce it faithfully. The canonical implementation lives in `assets/report-template.html` — this file explains the *intent* so you fill the template well and know what is safe to change.

## Concept

An **editorial intelligence dossier** on warm paper: the feel of a printed strategy brief or a field report, not a SaaS landing page or a generic dashboard. It should read as considered, evidence-forward, and a little austere. Restraint is the point — one strong accent, generous structure, real typographic hierarchy. The reader should trust it.

This is a refined-minimal direction, not a maximalist one: elegance comes from precise spacing, confident type, and a single decisive color — not from effects piled on.

## Color

Warm-paper background, near-black ink, one cinnabar (vermilion) accent. Defined as CSS variables in the template — do not introduce new hues.

| Token | Value | Use |
|---|---|---|
| `--paper` | `#F4EFE6` | page background |
| `--paper-deep` | `#EBE3D5` | section/card fills, table stripes |
| `--ink` | `#1C1A17` | primary text, dark inversion blocks |
| `--ink-soft` | `#4A453D` | body text |
| `--ink-faint` | `#8A8275` | labels, captions |
| `--cinnabar` | `#B5462E` | the one accent — kickers, rules, signals, numerals |
| `--cinnabar-deep` | `#963823` | accent text needing more contrast |
| `--gold` | `#9C7A3C` | sparse secondary detail only |

A faint SVG noise overlay (`multiply`) gives the paper its tooth — keep it. Dark inversion blocks (ink background, paper text, cinnabar highlights) are reserved for the **verdict snapshot** and the **closing verdict** so they bookend the document; do not overuse them.

## Type

Loaded from Google Fonts in the template. Pairing:

- **Display / headings (CN):** `Noto Serif SC` — weighty serif for section titles and big statements.
- **Display / accents (Latin):** `Fraunces` (italic for flourish) — large numerals, stage names, English glosses.
- **Body (CN + Latin):** `Noto Sans SC` at weight 300–400 — long-form readability; keep it light.
- **Labels / kickers / data:** `Space Mono`, uppercase, letter-spaced — the "spec-sheet" voice for section numbers, meta keys, and signal pills.

Hierarchy is carried by **size + weight + family contrast**, not by color. Big serif headings, a mono kicker above them, light sans body beneath.

## Layout primitives

- **Hairline rules** between sections (`1–2px` ink at low opacity) instead of cards-everywhere. The grid does the work.
- **Numbered sections** with an oversized cinnabar Fraunces numeral beside a serif title.
- **The five-stage maturity timeline** — equal columns with a top rule and a dot per stage; the active stage marked in cinnabar, the rest muted.
- **Dimension blocks** — a labelled left rail (mono kicker + serif label) beside a content column of a summary line, evidence-bearing bullets, and a signal pill. Diamond/square bullet markers, not discs.
- **Signal pills** — small mono uppercase tags colored by strength (strong/mixed/weak). Each pill earns its color from the findings beside it.
- **Comparison matrix** — bordered table, ink header row, paper-deep hover; first column is the bolded option name with an italic descriptor.
- **Bookend inversion blocks** — verdict snapshot near the top, full verdict at the bottom, both on ink.

## Motion

One orchestrated entrance, nothing fussy:
- A staggered hero rise on load (CSS `animation-delay`).
- Scroll-reveal (`IntersectionObserver` adding an `in` class) for sections as they enter the viewport.
- Subtle hover lifts on cards/rows.

Keep it CSS-driven and restrained. No autoplay carousels, parallax, or attention-grabbing loops — this is a document.

## Rules when filling the template

1. **Edit content, not the `<style>` block.** The design tokens, fonts, and layout are fixed. You may add a content block that *reuses* existing classes; you may not restyle.
2. **Numbers over adjectives.** The aesthetic is evidence-forward; "last release 14 months ago" belongs in the design as much as in the prose.
3. **Collapse what's empty.** Delete repeatable blocks you don't need (a 2-alternative comparison gets 2 rows). Stretched-thin sections break the austere feel.
4. **One accent.** Resist adding a second color to "brighten" it. The discipline is the design.
5. **Keep prose terse.** Short declarative sentences. White space is part of the composition; do not fill it with filler copy.
