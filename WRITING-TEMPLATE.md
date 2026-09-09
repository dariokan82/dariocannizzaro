---
title: The title goes here
kind: story
standfirst: One sentence under the title. Optional, but it is what makes someone click.
date: 2026-09-01
description: The line Google and link previews will show. Keep it under about 155 characters.
first: Where it first appeared, if anywhere. Optional. Renders in grey under the piece.
firstUrl: https://link-to-the-original.example
draft: true
---

Write the piece here, in plain Markdown. Everything above the second `---` is metadata;
everything below it is the piece.

## Notes on using this file

- Copy it into `src/writing/`, rename it. **The filename becomes the URL** —
  `the-door-in-the-tree.md` publishes to `/read/the-door-in-the-tree/`. Lowercase,
  hyphens, no spaces.
- `kind` is `story` or `essay` — it decides which shelf of READ SOMETHING the piece sits on.
- Delete `draft: true` when it is ready. Files that keep it still build, so strip it
  or the piece goes live with a draft flag sitting in its front matter.
- `date` controls the ordering on each shelf. Newest first. The index shows the year only.
- `first` and `firstUrl` are optional: "First published on Medium, 9 February 2023." and
  the link. Delete both lines if there is nothing to say.
- A section break in the stories is a line containing only `<p class="sep">#</p>`, with
  a blank line either side — the lone # from the book.
- This template lives at the repo root, NOT in `src/writing/`, so it never gets published.

> Block quotes look like this, with a white rule down the left.

Italics with `*asterisks*`, bold with `**double asterisks**`, a rule with `---` on its own line.
