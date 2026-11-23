# AlphaWink

AlphaWink publishes research reports, short notes, project descriptions, and an engineering
profile. English pages live at the site root and Simplified Chinese pages under
`/zh/`.

Add notes to `opportunities.json`. Each entry has a stable `id` for links, a
`date` (YYYY-MM-DD), a `category` (`markets`, `data`, or `tools`), an HTTPS
`source`, and `en` and `zh` objects with `title`, `summary`, and `risk`.
Notes appear newest first. Include a primary source and what would weaken the
finding. Market mechanics and research methods appear on Alpha. Notes tagged
`data` appear under Engineering notes on About.

Page copy lives in `scripts/build.py`. After updating the copy or notes, run
`python3 scripts/build.py` and commit the generated HTML alongside its source.
Long-form reports use metadata in `content/research/index.json` and HTML
fragments in `content/research/<id>/en.html` and `zh.html`. Give each report
a stable ID and optionally an `updated` date for a substantive revision.
The homepage features the newest report and previews three more. The research
archive lists every report. When it absorbs an older report, set `redirect.from` to the old ID
and `redirect.section` to its new heading ID. The build uses article headings of
the form `<h2 id="section-id">Heading</h2>` for the table of contents.
Put report figures in `assets/research/`, with alt text and a source or method
in the caption.
The committed charts can be regenerated with Matplotlib and
`python3 scripts/plot_research.py --cjk-font /path/to/chinese-font.ttf`.

Reports and notes are readable without JavaScript. JavaScript enables the note
filters. GitHub Pages serves the static files from `master`.
