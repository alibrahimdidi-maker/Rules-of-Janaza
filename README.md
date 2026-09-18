# Rules of Janazah — Course Slides Site

Same setup as the Family and Imams Practice sites: a module-code gate first,
then all 13 topics as royal-styled accordion cards.

## Files

```
index.html       — the whole site (gate + all 13 topics)
fonts/Faruma.ttf — Dhivehi Faruma font, embedded via @font-face
```

Module code (password): **SHA0302**

## Deploying to GitHub Pages

Same steps as before:
1. Create a new repository (e.g. `rules-of-janazah-slides`).
2. Upload `index.html` and the `fonts/` folder (with `Faruma.ttf` inside),
   keeping the folder structure intact.
3. Settings → Pages → Source: "Deploy from a branch" → `main` → `/ (root)` → Save.
4. Your live link: `https://<username>.github.io/<repo-name>/`

## Hiding topics not yet taught

Search `index.html` for `LAST_VISIBLE_WEEK` and change the number — topics
beyond it stay in the file but are hidden from view.

## Note on topic 6-7

Topics 6 and 7 were provided as a single combined slide file, so they appear
together under one accordion card labelled [WEEK-6-7].
