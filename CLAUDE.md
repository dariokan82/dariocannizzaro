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
- **Fonts:** Fraunces (display) and Inter (body), from Google Fonts.
- Deployed by `.github/workflows/deploy.yml` to GitHub Pages on push to `main`.

## File map

```
eleventy.config.js        Build config, date filters, the `writing` collection
src/
  _data/site.json         Identity, the promise line, email, social links
  _data/work.json         The slate. `available` (first) and `produced`
  _includes/layouts/
    base.njk              Shell: head/meta/OG, masthead, colophon
    page.njk              Generic inner page
    essay.njk             A single piece of writing
  index.njk               Home: promise, standing credits, two doors, top-3 strip
  work.njk                Two shelves
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
| `--measure` | `34rem` | Reading measure. Prose never exceeds it. |

Type: Fraunces for anything that behaves like a headline, Inter for everything else.
Uppercase letter-spaced 0.78rem for eyebrows and metadata. Body prose is 1.125rem / 1.75 —
larger and looser than a marketing site, because people are meant to actually read here.

## Conventions

- **Content lives in data or Markdown, never in markup.** Adding a script means editing
  `work.json`; adding an essay means dropping a file in `src/writing/`. If a change to the
  slate requires touching a `.njk` file, something has gone wrong.
- **Loglines are Dario's to write.** Empty `logline` fields render as nothing, on purpose.
  Do not fill them in on his behalf.
- The outstanding pre-launch list lives in `README.md`, not here.
