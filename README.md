# AlphaWink

AlphaWink publishes research notes, project descriptions, and an engineering
profile. English pages live at the site root and Simplified Chinese pages under
`/zh/`.

Add notes to `opportunities.json`. Each entry has a stable `id` for links, a
`date` (YYYY-MM-DD), a `category` (`markets`, `data`, or `tools`), an HTTPS
`source`, and `en` and `zh` objects with `title`, `summary`, and `risk`.
Notes appear newest first. Include a primary source and what would weaken the
finding.

Page copy lives in `scripts/build.py`. After updating the copy or notes, run
`python3 scripts/build.py` and commit the generated HTML alongside its source.
The notes are readable without JavaScript. JavaScript enables the category
filters. GitHub Pages serves the static files from `master`.
