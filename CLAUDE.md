# dariocannizzaro.com — project map

Personal site for Dario Cannizzaro: writer, screenwriter, director. Serves two audiences at
once — **readers** (of *Dead Men Naked* and the short fiction) and **work partners**
(agents, producers, development execs).

## The governing principle

**Conventional structure, dangerous prose.** The two audiences only conflict on tone. The
resolution is sequence, not compromise: a skeleton so legible that a producer can navigate it
in eight seconds, wrapped around sentences that could only be Dario's. Never the reverse — a
wild layout with safe copy dies with both audiences at once.

Corollary, and it matters: **no "For Readers / For Industry" split.** Nobody has ever clicked
"I am an agent." One site, ordered by reading *speed*: the fast reader gets everything they
need above the fold on `/`, the slow reader keeps going.

## Billing rule

Dario co-founded True Story Studios, but **his title in copy is "Head of Story."**
Never write "co-founder" anywhere a third party reads. Applies site-wide.

## Tech stack

- **Eleventy 3** (ESM config, `eleventy.config.js`), Nunjucks templates, Markdown for essays.
- **No CSS framework.** One hand-written stylesheet, `src/assets/css/style.css`.
- **No client-side JS.** Deliberate — this site's job is to be readable and indexable.
  Deviates from the True Story site (React + in-browser Babel), because here the prose has to
  be crawlable and fast, and there is no interactive slate to drive.
- **Fonts:** Fraunces (display + long-form reading) and DM Mono (everything else), from Google
  Fonts. Inter is gone.
- Deployed by `.github/workflows/deploy.yml` to GitHub Pages on push to `main`.

## File map

```
eleventy.config.js        Build config, date filters, the `writing` collection
src/
  _data/site.json         Identity, the promise line, email, credentials band, portrait, social
  _data/work.json         The slate, three shelves: `available` (first), `produced`,
                          `published`. `hidden: true` pulls an entry without deleting it;
                          `links: [{label, url}]` on produced and published
  _data/press.json        Interviews & reviews. `quotes` (loud, few) and `clippings` (the wall)
  _includes/layouts/
    base.njk              Shell: head/meta/OG, masthead, colophon
    page.njk              Generic inner page
    essay.njk             A single piece of writing
  index.njk               Home: promise, standing credits, two doors, top-3 strip
  work.njk                Three shelves, each entry a `.row`. Available has its own loop
                          (logline, genre); Produced and Published share one, driven by the
                          `shelves` list at the top of the file
  press.njk               Pull-quotes, then the clippings wall. Self-hiding from the nav
                          while press.json is empty — see base.njk
  writing.njk             Index of essays and stories. Self-hides the same way while the
                          `writing` collection is empty
  about.njk               Job-list lede first, then the credits
  contact.njk             Email large; Formspree form only if `formspreeId` is set
  writing/writing.json    Directory data: applies the essay layout + `writing` tag
  404.njk, robots.txt, sitemap.njk
  assets/css/style.css    All styling
  assets/img/             Book covers (480px JPEGs, slugged filenames). Still missing
                          share.jpg and favicon.png
WRITING-TEMPLATE.md       Copy into src/writing/ to start a piece
```

## Design system — "the ledger"

**A screenwriter's site should look like something catalogued** — a slate, an index, a set of
spines. Elegance here is made of three things and nothing else. If a change doesn't serve one of
them, it doesn't go in:

1. **Violent scale contrast.** Two sizes, far apart: enormous titles against 0.66rem metadata.
   Everything in the middle is deleted, because the middle is what "boring" is made of.
2. **Air.** Sections breathe in `--beat` (`clamp(4.5rem, 11vh, 9rem)`), not in units.
3. **Asymmetry. Nothing is centred, ever.** A left rail carries the index numbers, the body sits
   off it, the metadata sits far right. The eye has somewhere to go besides down.

### Tokens

| Token | Value | Role |
|---|---|---|
| `--ink` | `#0d100e` | Ground, under a barely-there radial lift from `--ink-lift` at the top. |
| `--bone` | `#ece8dd` | Body text. Paper that has been somewhere. |
| `--bone-dim` | `#98937f` | Meta, captions, secondary nav. |
| `--moss` | `#7fa67f` | The single accent: section titles, nav underline, hover index numbers. |
| `--ghost` | 17% bone | The index numbers at rest. |
| `--shell` | `84rem` | Page width. Wide on purpose — a 64rem centred column reads as a blog. |
| `--measure` | `min(56ch, 100%)` | Mono text. The `min()` is load-bearing on narrow screens. |
| `--beat` | `clamp(4.5rem, 11vh, 9rem)` | The vertical unit. `.section + .section` gets 0.55 of one. |

### The one repeating object

`.row` inside `.ledger` — a three-column grid, `4.5rem | 1fr | 11rem`: index number, body,
far-right metadata. Work entries, press clippings and essays are all the same object. It collapses
to two columns at 62rem and one at 34rem. Hover lifts the background, shifts the title 0.45rem
right, and turns the index number moss.

**The grain matters.** `body::after` lays an SVG turbulence at 3.5% opacity over everything. It is
the difference between a flat dark theme and an expensive one; don't delete it.

### Motion

CSS only — the no-JS rule is about crawlability, not about the page being inert. Scroll reveals use
`animation-timeline: view()` behind `@supports`, so elements are fully visible where it isn't
supported. Everything is off under `prefers-reduced-motion`.

### The typographic idiom: screenplay grammar, never screenplay furniture

**In** — fixed-width setting, uppercase letterspaced titles, marginalia in a right rail where a
scene number would sit, numbered entries.
**Out** — FADE IN / CUT TO, page numbers, brads, title-page pastiche, `INT.`/`EXT.` prefixes on
things that aren't places, dialogue blocks used as a joke. If a device needs the reader to be in
on it, it's out.

Fraunces appears in exactly three places — the homepage promise, page `<h1>`s, and press
pull-quotes — and it appears at clamp-to-9.5rem sizes. Three appearances at that scale is why they
land. Everything structural is DM Mono, and the fix for the first version of this site was making
that mono *big*, not making it different.

**DM Mono has no bold — 500 is the ceiling.** Nothing in the stylesheet may exceed
`--weight-strong`; a heavier value gets synthesised into a fake bold and looks wrong. Hierarchy
comes from **case, letter-spacing and colour**, never weight. Body sits at 400 — 300 is for
already-dim metadata only, because light weights smear on a dark ground.

**The essays are the one exception.** Monospace past ~800 words is measurably slower to read, and
`/writing/` is where someone is meant to sink in, so `.prose p` uses `--longform` (Fraunces at its
text optical size). Flipping that one token to `var(--mono)` makes the site all-mono; it is
deliberately a single value, not a redesign.

## Conventions

- **Content lives in data or Markdown, never in markup.** Adding a script means editing
  `work.json`; adding an essay means dropping a file in `src/writing/`. If a change to the
  slate requires touching a `.njk` file, something has gone wrong.
- **Loglines: drafted by Claire on 2026-09-08 at Dario's explicit request**, from scripts and
  books she has read in full. Dario edits them freely. Empty `logline` fields still render as
  nothing; the four entries still empty are ones Claire hasn't read, not ones she declined.
- **Three shelves, and the names are load-bearing.** *Available* is the only word on the site
  that tells an agent the script can be in their inbox today — never trade it for a format
  label like "Screenplays" (two entries aren't screenplays), and never for "In progress",
  which reads *unfinished* when the point is finished-but-unsold. *Produced* carries the
  directing credits, which is why it can't be folded into *Published*. *Published* is the
  books alone, on their own shelf because that is what a reader arrived for.
- **Covers are optional data, not a layout.** An entry on any shelf may carry `cover` +
  `coverAlt`; the row grows a `.row-cover` slot and is otherwise the same `.row` as every
  other row on the page. Rows without the field render byte-for-byte as before — that is the
  point, and it is why this doesn't violate the one-repeating-object rule. Source covers from
  Dario's own EPUBs (`WRITING/published/<title>/*.epub` → `images/`), never from a retailer's
  CDN. The 1px `--rule` border on `.row-cover img` is load-bearing: the *Of Life, Death,
  Aliens and Zombies* cover is near-black and dissolves into `--ink` without it.
- **A section that self-hides from the nav also leaves the sitemap.** Otherwise the one page
  nobody can click is the one Google is invited to index. The conditions live in two places —
  `base.njk` (nav) and `sitemap.njk` — and must move together.
- The outstanding pre-launch list lives in `README.md`, not here.

## Gotchas

- **Testing `PATH_PREFIX` from Git Bash on Windows** mangles the value: MSYS rewrites
  `/dariocannizzaro/` into `C:/Program Files/Git/dariocannizzaro/` and every internal href comes
  out wrong. It is a shell artifact, not a site bug — the Linux runner in the Action is fine. To
  reproduce the real thing locally:
  `MSYS_NO_PATHCONV=1 PATH_PREFIX=//dariocannizzaro// npx @11ty/eleventy --output=_site_pp`
- **`git push` has hung twice from Dario's Windows machine.** Use `timeout 100 git push origin main`.
