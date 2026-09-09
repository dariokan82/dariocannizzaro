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
- **No client-side JS the page depends on.** One 40-line progressive script on the front
  page for the visitor counter and the rotating strip; everything else is HTML and CSS.
  Deviates from the True Story site (React + in-browser Babel), because here the prose has to
  be crawlable and fast.
- **Fonts:** none loaded. Helvetica Neue / Helvetica / Arial from the system. Fraunces and
  DM Mono are gone (2026-09-09).
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
  index.njk               The welcome page: hero + greeting + signature, the strip, the
                          four doors, the derelict band
  work.njk                THE WORK. Three shelves, each entry an `.entry`. Available has its
                          own loop (logline, genre); Produced and Published share one
  writing.njk             READ SOMETHING, published at /read/. Essays, then the books —
                          always present, so the door is never locked
  about.njk               ABOUT. Job list, portrait, bio, then ○ WHAT OTHERS SAY (→ /press/,
                          hidden while press.json is empty) and ○ GET IN TOUCH
  press.njk               WHAT OTHERS SAY. About's child — never in the main nav.
                          Pull-quotes, then the clippings
  contact.njk             CONTACTS. Email as the one loud button; social in the grid;
                          Formspree form only if `formspreeId` is set
  404.njk                 The NOTICE! gate
  writing/writing.json    Directory data: essay layout, `writing` tag, /read/{slug}/ permalink
  robots.txt, sitemap.njk
  assets/css/style.css    All styling
  assets/js/derelict.js   The one script (front page only)
  assets/img/             Covers, the placeholder slots (see Images), share.jpg, favicons
tools/placeholders.py     Regenerates the placeholder images
WRITING-TEMPLATE.md       Copy into src/writing/ to start a piece
```

## Design system — "the box" (2026-09-09, replaces "the ledger")

Modelled on davidlynch.com as it stood in June 2004 (Wayback `20040622084358`, studied from
the actual HTML and GIFs, not from memory). One idea, and everything obeys it:

1. **The box.** `#000` page. A 640px box (`min(640px, 100%)`), 1px `#fff` border, centred,
   near the top. Every page lives inside it. Inner pages grow downward; the front page is
   ~440px tall like the original.
2. **One typeface, uppercase for structure.** Helvetica Neue / Helvetica / Arial, system
   stack, no webfonts. Wordmark, nav, headings, greeting, metadata: UPPERCASE, 10–13px,
   `letter-spacing: .04em`. Long prose (bio, essays, loglines): sentence case, 13px/1.5,
   `#ddd`, measure 58ch. The site drops its voice to sentence case only where someone is
   meant to *read*.
3. **The button: `○ LABEL`.** A 9px hollow circle and an uppercase label. Hover: the circle
   fills red (`#d10000`) inside its white ring — the 2004 swap-image "on" state.
   `aria-current="page"` lights it permanently. It is the only link style on the site: nav,
   Listen/Read/IMDb, back-links, social, press outlets. Prose links get an underline instead.
4. **Hairlines and the grid.** 1px white rules divide *bands* (`.band + .band`); 1px `#333`
   rules divide *entries* inside a band. The nav is Lynch's two-column grid (`.grid2`,
   `215px | 1fr`), the rules drawn by cell borders; the contact page's social links borrow it.
5. **Nothing eases, ever.** No `transition`, no `animation`, no smooth scroll, no grain, no
   radial lift. Rollovers swap instantly. Of everything from 2004 this is the one that reads
   as taste today, because every other site has a transition on it.
6. **Weird arrives sideways.** Three derelict touches, all on the front page's bottom band:
   a real odometer visitor counter, a LAST UPDATED stamp (the build time, so every deploy is
   honest), and a strip image picked at random per visit. Nothing else winks. The NOTICE! gate
   from the original lives on the 404 page and nowhere else.

### Tokens

| Token | Value | Role |
|---|---|---|
| `--black` / `--white` | `#000` / `#fff` | Ground and structure. True black, not near-black. |
| `--soft` | `#ddd` | Prose. |
| `--grey` | `#999` | Metadata, eyebrows, copyright. |
| `--rule-soft` | `#333` | Hairline between entries. White rules are for bands only. |
| `--red` | `#d10000` | The lit circle. Appears nowhere else. |
| `--box` | `640px` | The box. Not a variable to tune — it *is* the design. |

### The one repeating object

`.entry` — a two-column grid, body left and uppercase metadata right (`1fr | auto`), a
`#333` rule beneath. Work entries, press clippings, essays and books are all the same object.
`.has-cover` adds a 72px thumbnail column with a 1px white border. Collapses to one column
under 600px, where metadata joins into a single ` · `-separated line.

### The front page

`index.njk`. A 640×340 hero image (`site.hero`), the greeting (`site.greeting`, an array of
paragraphs, rendered uppercase) absolutely positioned over its right half, a signature beneath
it. Then the strip, the four doors, the derelict band. Under 600px the text drops below the
image. **The hero's right half must be dark** — that is where the words sit.

### Images: placeholders you overwrite

`tools/placeholders.py` generates dithered stand-ins that name their own slot and size.
Dario overwrites each with his own picture, **same filename**, and nothing else changes:
`home-hero.jpg` 640×340 · `portrait.jpg` 200×260 · `strip/01.jpg…` 640×40 (list them in
`site.json → strips`) · `signature.png` 240×60 transparent, white ink.

### The one script

`src/assets/js/derelict.js`, front page only, `defer`, progressive. Picks the strip and fills
the counter from Abacus (`abacus.jasoncameron.dev/hit/{namespace}/{key}`, keyless, CORS).
Without it the page is complete: strip 01 shows and the counter reads `------`. This is the
whole exception to the no-JS rule; nothing the page *needs* runs in JS.

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
- **/press/ self-hides while press.json is empty** — from the About page's button and from
  the sitemap. Otherwise the one page nobody can click is the one Google is invited to index.
  The two conditions live in `about.njk` and `sitemap.njk` and must move together. The four
  doors in the nav never hide: /read/ with no essays still shows the books.
- The outstanding pre-launch list lives in `README.md`, not here.

## Gotchas

- **Testing `PATH_PREFIX` from Git Bash on Windows** mangles the value: MSYS rewrites
  `/dariocannizzaro/` into `C:/Program Files/Git/dariocannizzaro/` and every internal href comes
  out wrong. It is a shell artifact, not a site bug — the Linux runner in the Action is fine. To
  reproduce the real thing locally:
  `MSYS_NO_PATHCONV=1 PATH_PREFIX=//dariocannizzaro// npx @11ty/eleventy --output=_site_pp`
- **`git push` has hung twice from Dario's Windows machine.** Use `timeout 100 git push origin main`.
- **Screenshots must be served over http**, not opened as files: the `| url` filter emits
  root-relative paths, so `file://` loses every stylesheet and image. `python3 -m http.server`
  in `_site/` is enough. Headless Chrome writes the PNG and then may hang on exit — wrap it in
  a timeout and don't trust the exit code.
