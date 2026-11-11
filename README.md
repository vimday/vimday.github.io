# AlphaWink

The site has three tabs: Alpha, Products, and About me. English pages are at the
site root; Simplified Chinese pages are under /zh/.

To publish an opportunity, add an object to opportunities.json. Each object has
date (YYYY-MM-DD), category (markets, data, or tools), source (the original HTTPS
URL), and en / zh objects with title, summary, and risk strings. Include the
evidence behind the note and the condition that would invalidate it. Notes are
displayed newest first. An empty list shows the editorial empty state.

To change page copy or the product introductions, edit scripts/build.py and run
python3 scripts/build.py from the repository root. Commit the generated HTML
alongside the source. GitHub Pages serves the static files from master.
