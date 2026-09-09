# dariocannizzaro.com

The personal site of Dario Cannizzaro — writer, screenwriter, director.

Static site, built with [Eleventy](https://www.11ty.dev/), published by GitHub Pages
from a GitHub Action on every push to `main`.

---

## Running it locally

```bash
npm install     # once
npm start       # http://localhost:8080, live-reloads as you save
npm run build   # one-off build into _site/
```

Node 20 or newer.

---

## Adding a piece of writing

1. Copy `WRITING-TEMPLATE.md` into `src/writing/`.
2. Rename it. **The filename becomes the URL** — `the-door-in-the-tree.md` publishes to
   `/read/the-door-in-the-tree/`.
3. Fill in `title`, `date`, `description`, write the piece in Markdown, delete `draft: true`.
4. Commit and push. The Action builds and deploys; it takes about a minute.

The index at `/read/` (READ SOMETHING) builds itself from whatever is in that folder, newest
first. There is nothing else to update.

**While that folder is empty, `/read/` still opens** — it shows the two books under READ
SOMETHING LONGER and a one-line "nothing short here yet". READ SOMETHING is one of the four
doors on the front page and never hides. `/press/` (WHAT OTHERS SAY) is the one that
self-hides: it is About's child and its button disappears while `press.json` is empty.

It does not have to be a blog. The short fiction is the better use of the section: it is
finished, it is already vetted, and it is the only page where someone can read the prose
instead of reading about it.

## Changing the work slate

`src/_data/work.json`. Three shelves, rendered in this order:

- **`available`** — finished scripts, unsold, askable today. What a producer is here for, so
  it goes first. The homepage strip shows the top three.
- **`produced`** — screen and audio that exists in the world. This is the shelf carrying the
  directing credits.
- **`published`** — the books, on their own shelf so a reader doesn't have to scan past five
  audio dramas to find them.

Add or reorder entries and both pages follow. A fourth shelf is one line in the `shelves`
list at the top of `src/work.njk` — no new markup.

## Changing the greeting

`src/_data/site.json → greeting`: one array entry per paragraph, rendered in uppercase over
the right half of the hero. The current text is Claire's placeholder — rewrite it in your
own words. Keep it short; the hero is 340px tall and the signature sits under it.

## Putting your own pictures in

Every image slot already holds a placeholder that names itself and its size. Overwrite the
file with your picture, **same filename**, and nothing else changes:

| File | Size | Notes |
|---|---|---|
| `src/assets/img/home-hero.jpg` | 640 × 340 | Black and white. Subject on the LEFT; the right half must fade to black — the greeting sits on it. |
| `src/assets/img/portrait.jpg` | 200 × 260 | About page. |
| `src/assets/img/strip/01.jpg` … `06.jpg` | 640 × 40 | Kept as they are — the dithered static is the design. One shows at random per visit; add files and list them in `site.json → strips`. |
| `src/assets/img/signature.png` | 240 × 60 | Transparent PNG, white ink. Delete the `signature` field in `site.json` to drop it. |

`python3 tools/placeholders.py` regenerates the placeholders if you ever want them back.

## The visitor counter

Real, via [Abacus](https://abacus.jasoncameron.dev) — keyless, no account. `site.json →
counter`: `start` is what the first visitor sees (100723 — 10 July 2023, the day Dario quit
Apple to write); change `key` to begin again from `start`. If the service ever goes away
the counter shows `------` and nothing else on the page is affected.

---

## Before this goes live — the outstanding list

- [ ] **Loglines.** Drafted by Claire 2026-09-08 at Dario's request for everything she has
      read; Dario to approve or rewrite. Still empty: Wild Fires, The Venetian, Party's Over,
      The Secret Seas of Puglia. While a logline is empty the Work page shows
      `[logline pending]` **in dev only** — gated on the `isDev` global, cannot reach a
      production build. Verify with `npm run build && grep -r "logline pending" _site/`.
- [ ] **Pictures.** Every slot is a placeholder until Dario drops his own in — see "Putting
      your own pictures in" above. The hero is the one that matters.
- [ ] **The greeting.** Placeholder copy; Dario's words go in `site.json → greeting`.
- [ ] **Social card.** `share.jpg` still carries the old design (Fraunces on ink). Re-render
      it in the box style once the hero image is real.
- [ ] **David's credits.** `about.njk` has a TODO where his two best-known titles should go.
- [ ] **Confirm three links.** The two IMDb title links in `work.json` were carried over from
      the old site and mapped by position: check that Strati is `tt38907629` and Trigger
      Warning is `tt11953332`. Also confirm the Strati *Listen* link — Apple Podcasts
      `id1862584688`, verified via audiodrama.directory as the English full-cast series. The
      Spreaker original is in the `_comment_unconfirmed` note if you'd rather point there.
- [ ] **Writing.** `src/writing/` is empty, so the section is unlinked and out of the
      sitemap. One story or essay turns it on.
- [ ] **Press.** `src/_data/press.json` ships empty, with the two shapes documented as
      `_example_*` keys. Fill `quotes` (two or three, set large) and `clippings` (the wall).
      **While both arrays are empty the `/press/` page builds but is not linked from the
      masthead** — an empty press page is worse than none. Add one real entry and the nav
      link appears on its own.
- [ ] **True Story titles.** Six Dimes, Darkness is my Candle and Running the Amazon are not
      listed. Check with David whether they belong on a personal site before adding them.
- [ ] **The Last Supper** is off the slate at Dario's request (2026-09-03), not deleted. Its
      entry in `work.json` carries `"hidden": true`. Remove that one line to put it back.
- [ ] **Contact form (optional).** Set `formspreeId` in `site.json` to a
      [Formspree](https://formspree.io) form ID and the form appears. Leave it empty and the
      page shows the email address alone, which is the better default.

### Promoting an essay

Add `featured: true` to a piece's front matter and it surfaces in the **Start here** cluster
above the full index, marked with a ★. Resonance before recency — the newest thing you wrote
is rarely the one a stranger should read first.

---

## Going live on the real domain

The site publishes to `dariokan82.github.io/dariocannizzaro/` first, so you can look at it
without touching the live domain. When you are happy with it:

1. Create `src/CNAME` containing one line: `dariocannizzaro.com`
2. Uncomment the `addPassthroughCopy("src/CNAME")` line in `eleventy.config.js`.
3. Delete the `env:` block (and its `PATH_PREFIX` line) under the build step in
   `.github/workflows/deploy.yml`. On a project URL the site lives at
   `/dariocannizzaro/`; on the apex domain it lives at `/`, and that env var is the
   only thing that knows the difference.
4. In **Settings → Pages**, set the custom domain to `dariocannizzaro.com` and tick
   *Enforce HTTPS*.
5. At the registrar, point the apex `A` records at GitHub's four IPs
   (`185.199.108.153`, `.109.153`, `.110.153`, `.111.153`) and `www` at a `CNAME` to
   `dariokan82.github.io`.

Until step 5 the old site keeps serving. Nothing breaks while you decide.

---

## Repo settings that need doing once

**Settings → Pages → Source: GitHub Actions.** Not "Deploy from a branch" — this repo
builds, so it needs the Actions source or nothing will publish.
