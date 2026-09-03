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
  _data/work.json         The slate. `available` (first) and `produced`. `hidden: true` pulls
                          an entry without deleting it; `links: [{label, url}]` on produced
  _data/press.json        Interviews & reviews. `quotes` (loud, few) and `clippings` (the wall)
  _includes/layouts/
    base.njk              Shell: head/meta/OG, masthead, colophon
    page.njk              Generic inner page
    essay.njk             A single piece of writing
  index.njk               Home: promise, standing credits, two doors, top-3 strip
  work.njk                Two shelves, each entry a scene block
  press.njk               Pull-quotes, then the clippings wall. Self-hiding from the nav
                          while press.json is empty — see base.njk
  about.njk               Job-list lede first, then the credits
  contact.njk             Email large; Formspree form only if `formspreeId` is set
  writing.njk             Index of essays, newest first
  writing/writing.json    Directory data: applies the essay layout + `writing` tag
  404.njk, robots.txt, sitemap.njk
  assets/css/style.css    All styling
  assets/img/             share.jpg, favicon.png, portraits — currently EMPTY
WRITING-TEMPLATE.md       Copy into src/writing/ to start a piece
```

## Design system

Dark, wooded, editorial. Defined as CSS custom properties at the top of `style.css`.

| Token | Value | Role |
|---|---|---|
| `--ink` | `#0d100e` | Ground. Deep green-black. |
| `--bone` | `#e9e5da` | Body text. Paper that has been somewhere. |
| `--bone-dim` | `#a8a294` | Meta, captions, secondary nav. |
| `--moss` | `#7fa67f` | The single accent. Link underlines, section eyebrows, quote rules. |
| `--measure` | `61ch` | A screenplay action line is 61 characters. Mono text never exceeds it. |
| `--measure-prose` | `36rem` | The same job for the proportional essay body. |

### The typographic idiom: screenplay grammar, never screenplay furniture

**In** — fixed-width setting, uppercase letterspaced sluglines, the 61-character action measure,
marginalia in a right rail where a scene number would sit.
**Out** — FADE IN / CUT TO, page numbers, brads, title-page pastiche, `INT.`/`EXT.` prefixes on
things that aren't places, dialogue blocks used as a joke. If a device needs the reader to be in
on it, it's out.

Fraunces appears in exactly three places: the homepage promise, page `<h1>`s, and press
pull-quotes. Everything structural is DM Mono.

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
- **Loglines are Dario's to write.** Empty `logline` fields render as nothing, on purpose.
  Do not fill them in on his behalf.
- The outstanding pre-launch list lives in `README.md`, not here.

## Gotchas

- **Testing `PATH_PREFIX` from Git Bash on Windows** mangles the value: MSYS rewrites
  `/dariocannizzaro/` into `C:/Program Files/Git/dariocannizzaro/` and every internal href comes
  out wrong. It is a shell artifact, not a site bug — the Linux runner in the Action is fine. To
  reproduce the real thing locally:
  `MSYS_NO_PATHCONV=1 PATH_PREFIX=//dariocannizzaro// npx @11ty/eleventy --output=_site_pp`
- **`git push` has hung twice from Dario's Windows machine.** Use `timeout 100 git push origin main`.
