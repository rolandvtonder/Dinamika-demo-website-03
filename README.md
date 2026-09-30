# Hoërskool Dinamika — webwerf / website

Static bilingual website (Afrikaans default, English toggle). No database or server code, so it can be hosted anywhere (cPanel, Netlify, GitHub Pages, etc.).

## Upload these to the web host
```
index.html  ons-skool.html  akademie.html  sport-kultuur.html
aansoeke.html  personeel.html  nuus.html  kontak.html
assets/
```
`_src/`, `medias/`, `.claude/` and this README don't need to be uploaded.

## Everyday updates (no rebuild needed)
| What | File |
|---|---|
| News articles | `assets/js/news-data.js` — add a new entry at the top |
| Calendar events | `assets/js/events-data.js` — past events hide automatically |
| Staff list | `assets/js/staff-data.js` — photos go in `assets/img/staff/` |
| Photos | `assets/img/` |

## Sport pages
Each sport has its own page (`sport-rugby.html`, `sport-hokkie.html`, …). All their content lives in **`_src/sports.py`**, one entry per sport: description, season, highlights, kit, photos and an optional coach line. Edit an entry, or copy one to add a new sport, then run the build. The sport cards on the Sport & Culture page and the "Other sports" links update automatically. News articles whose category matches a sport (e.g. `Hockey`) appear on that sport's page.

## Page text, menu, header or footer
The `.html` pages are **generated**. Don't edit them by hand. Edit:
- page content: `_src/pages/<page>.html`
- menu, header, footer, contact details: `_src/build.py`

Then rebuild (needs Python 3, no extra packages):
```
python _src/build.py
```

Shorthand inside the page files:
- `[[Afrikaans||English]]` is a bilingual phrase.
- For longer text, use two blocks: `<p lang="af">…</p><p lang="en">…</p>`.
- `{{i:phone}}` inserts an icon (the full list is in `ICONS` in `build.py`).

## Contact form
By default the form opens the visitor's e-mail app, addressed to ontvangs@namies.co.za. To receive messages directly, create a free form at https://formspree.io and paste its URL into `FORM_ENDPOINT` at the top of `assets/js/main.js`.

## To check before launch
- **News** (`news-data.js`) is starter content written from recent photos. Replace it with real stories and dates.
- **Calendar**: entries marked `SAMPLE` in `events-data.js` have placeholder dates.
- **Fees**: the amounts come from the old site's 2023 fee page. Confirm the current year's figures.
- **Staff**: 4 people had no photo on the old site and show a placeholder: Shanté Bekker, Karen Bezuidenhoudt, Martin Els and Sharné Potgieter.

## Preview locally
```
python -m http.server 8080
```
Then open http://localhost:8080
