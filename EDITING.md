# Editing the site yourself

Everything you'll touch regularly lives in three places. Templates and CSS you shouldn't
need to open.

## Run it

```
cd ~/coding/dariocannizzaro
npm start          # http://localhost:8080 — reloads as you save
```

## Words

**The greeting on the front page** — `src/_data/site.json`, the `greeting` field. One entry
per paragraph. It renders in uppercase automatically, so write it in normal case. Keep it
short: it has to fit in the right half of the hero next to the signature.

**The bio** — `src/about.njk`. It's plain HTML paragraphs between `<p>` tags; write and
delete freely. The job list at the top is one line of `<span>`s. The comment about David's
credits is a note to you, invisible on the site.

**The slate** — `src/_data/work.json`. Three lists: `available`, `produced`, `published`.
Each entry is a title, a format, a logline, an optional note and links. Reorder entries to
reorder the page. `"hidden": true` pulls an entry without deleting it.

**Press** — `src/_data/press.json`. `quotes` are the big ones (few), `clippings` the list.
Empty both and WHAT OTHERS SAY disappears from the About page on its own.

**Contact** — `src/_data/site.json`: `email`, `location`, `social`. Add a `formspreeId` and
a contact form appears under the email.

## Pictures

Every image slot already holds a placeholder that says its own name and size. Drop your
picture over it, **same filename**, and you're done:

| File | Size | Notes |
|---|---|---|
| `src/assets/img/home-hero.jpg` | 640 × 340 | Black and white. You on the LEFT. Right half fades to black — the greeting sits on it. |
| `src/assets/img/portrait.jpg` | 200 × 260 | About page. |
| `src/assets/img/strip/01.jpg` … `06.jpg` | 640 × 40 | Not placeholders — the dithered static stays. One shows at random per visit. To add one, drop a 640×40 file in and list it under `strips` in `site.json`. |
| `src/assets/img/signature.png` | 240 × 60 | Transparent PNG, white ink. Delete the `signature` line in `site.json` to drop it. |

Book covers: `cover` field on an entry in `work.json`, file in `src/assets/img/`.

## The visitor counter

`src/_data/site.json → counter`. `start` is what the first visitor sees (100723, the day you
quit Apple); every visit after that adds one. Change `key` to any new word and it begins
again from `start`.

## Writing

Copy `WRITING-TEMPLATE.md` into `src/writing/`, rename it (the filename is the URL:
`the-door.md` → `/read/the-door/`), fill in title and date, write in Markdown, delete
`draft: true`. It appears under READ SOMETHING on its own. `featured: true` puts it in
START HERE.

## Ship it

```
git add -A && git commit -m "what you changed" && git push
```

Pushes to `main` go live in about a minute. Right now the new design is on the `lynch`
branch; merge it when you're happy:

```
git checkout main && git merge lynch && git push
```

## If `npm start` says permission denied

Syncthing brought `node_modules` over from Windows without execute bits. The scripts now call
node directly so it shouldn't recur; if it does, `chmod +x node_modules/.bin/*` or just
`rm -rf node_modules && npm install`.
