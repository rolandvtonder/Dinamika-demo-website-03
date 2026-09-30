"""
Hoërskool Dinamika — static site builder (Python 3 standard library only).

Page content lives in _src/pages/*.html. The shared header, navigation and
footer live in this file, so a menu change only has to be made once.

    python _src/build.py

Writes the finished .html pages to the project root. Do not edit the root
.html files by hand — edit _src/pages/ and run the build again.

Shorthand available inside page files:
    [[Afrikaans||English]]   -> bilingual inline text
    {{i:name}}               -> inline SVG icon (see ICONS below)
    {{i:name extra-class}}   -> icon with an extra CSS class
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sports import SPORTS, SPORT_ICONS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGES = Path(__file__).resolve().parent / "pages"

SCHOOL = {
    "phone": "011 867 5986",
    "phone_href": "+27118675986",
    "email": "ontvangs@namies.co.za",
    "accounts_email": "accounts@namies.co.za",
    "accounts_phone": "011 867 0774",
    "address": "55 Roy Campbell St, Brackenhurst, Alberton, 1448",
    "facebook": "https://www.facebook.com/HsDinamika99",
    "instagram": "https://www.instagram.com/hs_dinamika/",
}

# Lucide icons (https://lucide.dev, ISC licence) — 24×24, stroke based.
ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "map-pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "instagram": '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>',
    "menu": '<line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "chevron-left": '<path d="m15 18-6-6 6-6"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-up": '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
    "pause": '<rect x="14" y="4" width="4" height="16" rx="1"/><rect x="6" y="4" width="4" height="16" rx="1"/>',
    "play": '<polygon points="6 3 20 12 6 21 6 3"/>',
    "calendar": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/>',
    "graduation-cap": '<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    "trophy": '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
    "music": '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "book-open": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "file-text": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "wallet": '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
    "shirt": '<path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/>',
    "send": '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "check-circle": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/>',
    "external-link": '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "school": '<path d="M14 22v-4a2 2 0 1 0-4 0v4"/><path d="m18 10 4 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-8l4-2"/><path d="M18 5v17"/><path d="m4 6 8-4 8 4"/><path d="M6 5v17"/><circle cx="12" cy="9" r="2"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "image": '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>',
    "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "quote": '<path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"/><path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/>',
    "history": '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "sparkles": '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>',
    "cpu": '<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>',
    "atom": '<circle cx="12" cy="12" r="1"/><path d="M20.2 20.2c2.04-2.03.02-7.36-4.5-11.9-4.54-4.52-9.87-6.54-11.9-4.5-2.04 2.03-.02 7.36 4.5 11.9 4.54 4.52 9.87 6.54 11.9 4.5Z"/><path d="M15.7 15.7c4.52-4.54 6.54-9.87 4.5-11.9-2.03-2.04-7.36-.02-11.9 4.5-4.52 4.54-6.54 9.87-4.5 11.9 2.03 2.04 7.36.02 11.9-4.5Z"/>',
    "sprout": '<path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/><path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/><path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"/>',
    "monitor": '<rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/>',
    "zap": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    "palette": '<circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/>',
    "handshake": '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/>',
    "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    "alert": '<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>',
}

ICONS.update(SPORT_ICONS)


def icon(name: str, cls: str = "") -> str:
    if name not in ICONS:
        raise KeyError(f"Unknown icon: {name}")
    klass = ("icon " + cls).strip()
    return f'<svg class="{klass}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'


def bi(af: str, en: str) -> str:
    return f'<span lang="af">{af}</span><span lang="en">{en}</span>'


def expand(text: str) -> str:
    text = re.sub(r"\[\[(.+?)\|\|(.+?)\]\]", lambda m: bi(m.group(1), m.group(2)), text, flags=re.S)
    text = re.sub(r"\{\{i:([a-z0-9-]+)(?: ([^}]+))?\}\}", lambda m: icon(m.group(1), m.group(2) or ""), text)
    return text


# --------------------------------------------------------------------------
# Navigation — (key, href, Afrikaans, English, [sub-items])
# Sub-item hrefs starting with "#" point to a section on the parent page.
# --------------------------------------------------------------------------
NAV_LEFT = [
    ("ons-skool", "ons-skool.html", "Ons Skool", "Our School", [
        ("#hoof", "Boodskap van die Hoof", "Principal's Message"),
        ("#visie", "Visie &amp; Missie", "Vision &amp; Mission"),
        ("#fondasie", "Ons Fondasie", "Our Foundation"),
        ("#waardes", "Waardes", "Values"),
        ("#geskiedenis", "Ons Geskiedenis", "Our History"),
        ("#dissipline", "Dissipline", "Discipline"),
        ("#skooldrag", "Skooldrag", "School Uniform"),
        ("#skoollied", "Skoollied", "School Anthem"),
        ("personeel.html", "Personeel", "Staff"),
    ]),
    ("akademie", "akademie.html", "Akademie", "Academics", [
        ("#oorsig", "Oorsig", "Overview"),
        ("#gr8-9", "Graad 8–9-vakke", "Grade 8–9 Subjects"),
        ("#gr10-12", "Graad 10–12-vakke", "Grade 10–12 Subjects"),
        ("#verryking", "Verryking &amp; Fasiliteite", "Enrichment &amp; Facilities"),
    ]),
    ("sport-kultuur", "sport-kultuur.html", "Sport &amp; Kultuur", "Sport &amp; Culture", [
        ("#sport", "Sport", "Sport"),
        ("#kultuur", "Kultuur", "Culture"),
        ("#sosiaal", "Sosiale Funksies", "Social Functions"),
        ("#galery", "Galery", "Gallery"),
    ]),
]
NAV_RIGHT = [
    ("aansoeke", "aansoeke.html", "Aansoeke", "Admissions", [
        ("#graad-8", "Graad 8-aansoeke", "Grade 8 Applications"),
        ("#graad-9-12", "Graad 9–12-aansoeke", "Grade 9–12 Applications"),
        ("#dokumente", "Vereiste Dokumente", "Required Documents"),
        ("#skoolfonds", "Skoolfonds", "School Fees"),
    ]),
    ("nuus", "nuus.html", "Nuus", "News", [
        ("#nuus", "Namies Nuus", "Namies News"),
        ("#kalender", "Skoolkalender", "School Calendar"),
    ]),
    ("kontak", "kontak.html", "Kontak", "Contact", []),
]


def sub_href(parent: str, href: str) -> str:
    return parent + href if href.startswith("#") else href


def nav_items(items, active: str) -> str:
    out = []
    for key, href, af, en, subs in items:
        is_active = key == active or (active == "personeel" and key == "ons-skool")
        cur = ' aria-current="page"' if key == active else ""
        cls = "nav-item" + (" has-sub" if subs else "") + (" is-active" if is_active else "")
        html = f'<li class="{cls}"><a class="nav-link" href="{href}"{cur}>{bi(af, en)}</a>'
        if subs:
            html += (f'<button class="sub-toggle" type="button" aria-expanded="false" '
                     f'aria-label="{af.replace("&amp;", "&")}: submenu" data-en-aria-label="{en.replace("&amp;", "&")}: submenu">'
                     f'{icon("chevron-down")}</button><ul class="subnav">')
            for shref, saf, sen in subs:
                html += f'<li><a href="{sub_href(href, shref)}">{bi(saf, sen)}</a></li>'
            html += "</ul>"
        out.append(html + "</li>")
    return "".join(out)


def drawer_nav() -> str:
    out = ['<a href="index.html">' + bi("Tuis", "Home") + "</a>"]
    for key, href, af, en, subs in NAV_LEFT + NAV_RIGHT:
        if not subs:
            out.append(f'<a href="{href}">{bi(af, en)}</a>')
            continue
        links = f'<li><a href="{href}">{bi("Oorsig: " + af, "Overview: " + en)}</a></li>'
        links += "".join(f'<li><a href="{sub_href(href, h)}">{bi(a, e)}</a></li>' for h, a, e in subs)
        out.append(f"<details><summary>{bi(af, en)}{icon('chevron-down')}</summary><ul>{links}</ul></details>")
    return "".join(out)


LANG_SWITCH = ('<div class="lang-switch" role="group" aria-label="Taal / Language">'
               '<button type="button" data-lang="af" aria-pressed="true" lang="af-ZA" title="Afrikaans">AF</button>'
               '<button type="button" data-lang="en" aria-pressed="false" lang="en-ZA" title="English">EN</button></div>')

SOCIAL = (f'<ul class="social">'
          f'<li><a href="{SCHOOL["facebook"]}" target="_blank" rel="noopener" aria-label="Facebook">{icon("facebook")}</a></li>'
          f'<li><a href="{SCHOOL["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram">{icon("instagram")}</a></li></ul>')


def head(meta: dict) -> str:
    return f"""<!doctype html>
<html lang="af">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-en="{meta['title_en']}">{meta['title_af']}</title>
<meta name="description" content="{meta['desc_af']}" data-en-content="{meta['desc_en']}">
<meta name="theme-color" content="#121750">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Hoërskool Dinamika">
<meta property="og:title" content="{meta['title_af']}">
<meta property="og:description" content="{meta['desc_af']}">
<meta property="og:image" content="assets/img/{meta.get('og_image', 'leaders.jpg')}">
<link rel="icon" href="assets/img/crest.webp" type="image/webp">
<link rel="apple-touch-icon" href="assets/img/crest.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;family=Barlow+Condensed:wght@600;700&amp;family=Crimson+Pro:ital,wght@0,500;1,400;1,500&amp;display=swap">
<link rel="stylesheet" href="assets/css/style.css">
<script>/* Apply the saved language before first paint (no flash of the wrong language) */
(function(){{try{{var q=new URLSearchParams(location.search).get("lang"),s=localStorage.getItem("dinamika-lang"),l=q||s;if(l==="en"||l==="af")document.documentElement.lang=l;}}catch(e){{}}}})();</script>
</head>"""


def header(active: str) -> str:
    return f"""
<a class="skip-link" href="#main">{bi("Slaan oor na die inhoud", "Skip to content")}</a>
<p id="lang-status" class="visually-hidden" aria-live="polite"></p>
<div class="topbar">
  <div class="container topbar__inner">
    <ul class="topbar__info">
      <li><a href="tel:{SCHOOL['phone_href']}">{icon('phone', 'icon--sm')}{SCHOOL['phone']}</a></li>
      <li class="topbar__email"><a href="mailto:{SCHOOL['email']}">{icon('mail', 'icon--sm')}{SCHOOL['email']}</a></li>
      <li class="hide-sm">{icon('clock', 'icon--sm')}{bi("Ma–Vr 07:40–14:00", "Mon–Fri 07:40–14:00")}</li>
    </ul>
    <div class="topbar__actions">
      <div class="hide-sm">{SOCIAL}</div>
      {LANG_SWITCH}
    </div>
  </div>
</div>
<header class="site-header">
  <div class="navbar">
    <div class="container navbar__inner">
      <nav class="primary-nav" aria-label="Hoofnavigasie" data-en-aria-label="Main navigation">
        <ul class="nav-group nav-group--left">{nav_items(NAV_LEFT, active)}</ul>
      </nav>
      <a class="brand" href="index.html" aria-label="Hoërskool Dinamika — Tuis" data-en-aria-label="Hoërskool Dinamika — Home">
        <span class="brand__crest"><img src="assets/img/crest.webp" alt="" width="400" height="415"></span>
        <span class="brand__text"><strong>Hoërskool Dinamika</strong><span>Reik na die Lig</span></span>
      </a>
      <nav class="primary-nav" aria-label="Hoofnavigasie (vervolg)" data-en-aria-label="Main navigation (continued)">
        <ul class="nav-group nav-group--right">{nav_items(NAV_RIGHT, active)}</ul>
      </nav>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="drawer">{icon('menu')}<span>{bi("Kieslys", "Menu")}</span></button>
    </div>
  </div>
</header>
<dialog class="drawer" id="drawer" aria-label="Kieslys" data-en-aria-label="Menu">
  <div class="drawer__head">
    <img src="assets/img/crest.webp" alt="" width="52" height="52">
    {LANG_SWITCH}
    <button class="drawer__close" type="button" aria-label="Maak toe" data-en-aria-label="Close">{icon('x')}</button>
  </div>
  <nav class="drawer__nav" aria-label="Hoofnavigasie" data-en-aria-label="Main navigation">{drawer_nav()}</nav>
  <div class="drawer__foot">
    <a href="tel:{SCHOOL['phone_href']}">{icon('phone')}{SCHOOL['phone']}</a>
    <a href="mailto:{SCHOOL['email']}">{icon('mail')}{SCHOOL['email']}</a>
    <a class="btn btn--mint" href="aansoeke.html">{bi("Doen aansoek", "Apply now")}{icon('arrow-right', 'icon--arrow')}</a>
  </div>
</dialog>
"""


def footer(scripts: list[str]) -> str:
    s = SCHOOL
    col = lambda items: "".join(f'<li><a href="{h}">{bi(a, e)}</a></li>' for h, a, e in items)
    about = [("ons-skool.html#visie", "Visie &amp; Missie", "Vision &amp; Mission"), ("ons-skool.html#geskiedenis", "Ons Geskiedenis", "Our History"),
             ("ons-skool.html#waardes", "Waardes", "Values"), ("ons-skool.html#skooldrag", "Skooldrag", "School Uniform"),
             ("ons-skool.html#skoollied", "Skoollied", "School Anthem"), ("personeel.html", "Personeel", "Staff")]
    info = [("akademie.html", "Akademie", "Academics"), ("sport-kultuur.html", "Sport &amp; Kultuur", "Sport &amp; Culture"),
            ("aansoeke.html", "Aansoeke", "Admissions"), ("aansoeke.html#skoolfonds", "Skoolfonds", "School Fees"),
            ("nuus.html", "Namies Nuus", "Namies News"), ("nuus.html#kalender", "Skoolkalender", "School Calendar")]
    tags = "\n".join(f'<script src="assets/js/{x}" defer></script>' for x in scripts + ["main.js"])
    return f"""
<footer class="site-footer on-dark">
  <div class="container footer-top">
    <div>
      <div class="footer-brand">
        <img src="assets/img/crest.webp" alt="Hoërskool Dinamika-skoolwapen" data-en-alt="Hoërskool Dinamika school crest" width="84" height="84" loading="lazy">
        <div><strong>Hoërskool Dinamika</strong><span>Reik na die Lig</span></div>
      </div>
      <p lang="af">'n Waardegebaseerde parallelmedium-hoërskool in Alberton wat sedert 1993 leerders bemagtig vir die toekoms.</p>
      <p lang="en">A values-based, parallel-medium high school in Alberton, empowering learners for the future since 1993.</p>
      {SOCIAL}
    </div>
    <div>
      <h2>{bi("Ons Skool", "Our School")}</h2>
      <ul class="footer-links">{col(about)}</ul>
    </div>
    <div>
      <h2>{bi("Inligting", "Information")}</h2>
      <ul class="footer-links">{col(info)}</ul>
    </div>
    <div>
      <h2>{bi("Kontak Ons", "Contact Us")}</h2>
      <ul class="footer-contact">
        <li>{icon('map-pin')}<span>{s['address']}</span></li>
        <li>{icon('phone')}<a href="tel:{s['phone_href']}">{s['phone']}</a></li>
        <li>{icon('mail')}<a href="mailto:{s['email']}">{s['email']}</a></li>
        <li>{icon('wallet')}<span>{bi("Rekeninge", "Accounts")}: <a href="mailto:{s['accounts_email']}">{s['accounts_email']}</a></span></li>
        <li>{icon('clock')}<span>{bi("Ma–Vr 07:40–14:00", "Mon–Fri 07:40–14:00")}</span></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>© <span data-year>2026</span> Hoërskool Dinamika. {bi("Alle regte voorbehou.", "All rights reserved.")}</p>
    <p>{bi("Parallelmedium · Afrikaans &amp; Engels", "Parallel medium · Afrikaans &amp; English")}</p>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Terug na bo" data-en-aria-label="Back to top">{icon('arrow-up')}</button>
{tags}
</body>
</html>
"""


# --------------------------------------------------------------------------
# Reusable blocks — use @@NAME@@ inside a page file
# --------------------------------------------------------------------------
PARTIALS = {
    "CONTACT_FORM": """
<form class="form" id="contact-form" action="#" method="post" novalidate>
  <div id="form-summary" class="form-summary" hidden></div>
  <p class="field__hint">[[Velde gemerk met <span class="req">*</span> is verpligtend.||Fields marked with <span class="req">*</span> are required.]]</p>
  <div class="form__row form__row--2">
    <div class="field">
      <label for="cf-name">[[Naam en van||Name and surname]] <span class="req" aria-hidden="true">*</span></label>
      <input id="cf-name" name="name" type="text" autocomplete="name" required data-validate="name" aria-describedby="cf-name-error">
      <p class="field__error" id="cf-name-error"></p>
    </div>
    <div class="field">
      <label for="cf-phone">[[Kontaknommer||Contact number]]</label>
      <input id="cf-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" data-validate="phone" aria-describedby="cf-phone-hint cf-phone-error">
      <p class="field__hint" id="cf-phone-hint">[[Bv. 082 123 4567||E.g. 082 123 4567]]</p>
      <p class="field__error" id="cf-phone-error"></p>
    </div>
  </div>
  <div class="form__row form__row--2">
    <div class="field">
      <label for="cf-email">[[E-posadres||E-mail address]] <span class="req" aria-hidden="true">*</span></label>
      <input id="cf-email" name="email" type="email" autocomplete="email" inputmode="email" required data-validate="email" aria-describedby="cf-email-error">
      <p class="field__error" id="cf-email-error"></p>
    </div>
    <div class="field">
      <label for="cf-subject">[[Onderwerp||Subject]]</label>
      <select id="cf-subject" name="subject">
        <option value="Algemene navraag" data-en="General enquiry">Algemene navraag</option>
        <option value="Aansoeke" data-en="Admissions">Aansoeke</option>
        <option value="Skoolfonds / Rekeninge" data-en="School fees / Accounts">Skoolfonds / Rekeninge</option>
        <option value="Sport en Kultuur" data-en="Sport and Culture">Sport en Kultuur</option>
        <option value="Ander" data-en="Other">Ander</option>
      </select>
    </div>
  </div>
  <div class="field">
    <label for="cf-message">[[Boodskap||Message]] <span class="req" aria-hidden="true">*</span></label>
    <textarea id="cf-message" name="message" required data-validate="message" aria-describedby="cf-message-error"></textarea>
    <p class="field__error" id="cf-message-error"></p>
  </div>
  <div class="field">
    <div class="check">
      <input id="cf-consent" name="consent" type="checkbox" value="ja" data-validate="consent" aria-describedby="cf-consent-error">
      <label for="cf-consent">[[Ek stem in dat Hoërskool Dinamika my mag kontak oor hierdie navraag.||I agree that Hoërskool Dinamika may contact me about this enquiry.]] <span class="req" aria-hidden="true">*</span></label>
    </div>
    <p class="field__error" id="cf-consent-error"></p>
  </div>
  <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" style="display:none" aria-hidden="true">
  <div><button class="btn" type="submit">[[Stuur boodskap||Send message]]{{i:send}}</button></div>
  <div id="form-status" class="form-status" role="status" hidden></div>
</form>""",
    "LIGHTBOX": """
<dialog class="lightbox" id="lightbox" aria-label="Foto" data-en-aria-label="Photo">
  <figure><img src="data:," alt=""><figcaption></figcaption></figure>
  <button class="lightbox__btn lightbox__close" type="button" aria-label="Maak toe" data-en-aria-label="Close">{{i:x}}</button>
  <button class="lightbox__btn lightbox__prev" type="button" aria-label="Vorige foto" data-en-aria-label="Previous photo">{{i:chevron-left}}</button>
  <button class="lightbox__btn lightbox__next" type="button" aria-label="Volgende foto" data-en-aria-label="Next photo">{{i:chevron-right}}</button>
</dialog>""",
    "NEWS_MODAL": """
<dialog class="modal" id="news-modal" aria-labelledby="news-modal-title">
  <button class="modal__close" type="button" aria-label="Maak toe" data-en-aria-label="Close">{{i:x}}</button>
  <div class="modal__content"></div>
</dialog>""",
}


# --------------------------------------------------------------------------
# Sport pages (content lives in _src/sports.py)
# --------------------------------------------------------------------------
def sport_grid(current: str = "") -> str:
    items = []
    for sp in SPORTS:
        cur = ' aria-current="page"' if sp["slug"] == current else ""
        items.append(
            f'<li><a class="sport-card" href="sport-{sp["slug"]}.html"{cur}>'
            f'<span class="sport-card__icon">{icon(sp["icon"])}</span>'
            f'<span class="sport-card__text"><span class="sport-card__name">{bi(*sp["name"])}</span>'
            f'<span class="sport-card__meta">{bi(*sp["season"])} · {bi(*sp["kind"])}</span></span>'
            f'{icon("arrow-right", "sport-card__arrow")}</a></li>')
    return '<ul class="sport-grid">' + "".join(items) + "</ul>"


def sport_page(sp: dict) -> tuple[dict, str]:
    af, en = sp["name"]
    af_l, en_l = af.lower(), en.lower()        # name inside a sentence
    photos = sp.get("photos", [])
    s = SCHOOL

    if photos:
        hero = f'<section class="page-hero"><img class="page-hero__img" src="assets/img/{photos[0][0]}" alt="" fetchpriority="high">'
    else:
        hero = f'<section class="page-hero page-hero--pattern"><span class="page-hero__icon" aria-hidden="true">{icon(sp["icon"])}</span>'

    intro_parts = []
    for i, (a, e) in enumerate(sp["intro"]):
        cls = ' class="lead"' if i == 0 else ""
        intro_parts.append(f'<p lang="af"{cls}>{a}</p><p lang="en"{cls}>{e}</p>')
    intro = "".join(intro_parts)

    if photos:
        f, alt_af, alt_en = photos[-1]
        media = (f'<div class="split__media reveal" style="--delay:100ms"><img src="assets/img/{f}" '
                 f'alt="{alt_af}" data-en-alt="{alt_en}" loading="lazy"></div>')
    else:
        media = (f'<div class="sport-emblem reveal" style="--delay:100ms" aria-hidden="true">'
                 f'<span class="sport-emblem__icon">{icon(sp["icon"])}</span>'
                 f'<span class="sport-emblem__name">{bi(af, en)}</span>'
                 f'<span class="sport-emblem__motto">Reik na die Lig</span></div>')

    highlights = "".join(
        f'<article class="card reveal" style="--delay:{i * 80}ms"><span class="card__icon">{icon("check-circle", "icon--lg")}</span>'
        f'<h3>{bi(ta, te)}</h3><p>{bi(xa, xe)}</p></article>'
        for i, (ta, te, xa, xe) in enumerate(sp["highlights"]))

    coach = sp.get("coach")
    coach_html = f'<li>{icon("users")}<span>{bi(*coach)}</span></li>' if coach else ""

    if sp["kit"]:
        kit_items = "".join(f'<li>{icon("check")}<span>{bi(a, e)}</span></li>' for a, e in sp["kit"])
        kit = (f'<div class="panel reveal"><h3 class="panel__title">{icon("shirt")}{bi("Sportdrag", "Sports kit")}</h3>'
               f'<ul class="checklist">{kit_items}</ul>'
               f'<p class="fine-print" style="margin:16px 0 0">'
               + bi('Volgens die skool se <a href="ons-skool.html#skooldrag">skooldragbeleid</a>. Verskaffers: Fays (Bracken City) en Simply Schools (New Market Mall).',
                    "According to the school's <a href=\"ons-skool.html#skooldrag\">uniform policy</a>. Stockists: Fays (Bracken City) and Simply Schools (New Market Mall).")
               + "</p></div>")
    else:
        kit = (f'<div class="panel reveal"><h3 class="panel__title">{icon("shirt")}{bi("Drag", "Dress")}</h3>'
               f'<p style="margin:0;color:var(--muted)">'
               + bi("Geen spesiale sportdrag word vereis nie — leerders dra hul gewone skooldrag.",
                    "No special sports kit is required — learners wear their normal school uniform.")
               + "</p></div>")

    gallery = ""
    if len(photos) > 1:
        tiles = "".join(
            f'<li class="gallery__item"><button class="gallery__btn" type="button"><img src="assets/img/{f}" '
            f'alt="{a}" data-en-alt="{e}" loading="lazy"></button></li>' for f, a, e in photos)
        gallery = (f'<section class="section section--paper" aria-labelledby="foto-title"><div class="container">'
                   f'<div class="section-head reveal"><p class="eyebrow">{bi("Galery", "Gallery")}</p>'
                   f'<h2 id="foto-title">{bi(af + " in aksie", en + " in action")}</h2></div>'
                   f'<ul class="gallery gallery--2">{tiles}</ul></div></section>@@LIGHTBOX@@')

    body = f"""
{hero}
  <div class="container page-hero__inner">
    <nav class="breadcrumb" aria-label="Broodkrummels" data-en-aria-label="Breadcrumb">
      <ol><li><a href="index.html">{bi("Tuis", "Home")}</a></li><li><a href="sport-kultuur.html#sport">{bi("Sport &amp; Kultuur", "Sport &amp; Culture")}</a></li><li aria-current="page">{bi(af, en)}</li></ol>
    </nav>
    <h1>{bi(af, en)}</h1>
    <ul class="sport-facts">
      <li>{icon("calendar")}<span>{bi("Seisoen", "Season")}: <strong>{bi(*sp["season"])}</strong></span></li>
      <li>{icon(sp["icon"])}<span>{bi("Tipe", "Type")}: <strong>{bi(*sp["kind"])}</strong></span></li>
      {coach_html}
    </ul>
  </div>
</section>

<section class="section" aria-labelledby="oor-title">
  <div class="container split">
    <div class="prose reveal">
      <p class="eyebrow">{bi("Oor " + af_l, "About " + en_l)}</p>
      <h2 id="oor-title">{bi(af + " by Dinamika", en + " at Dinamika")}</h2>
      {intro}
      <div class="btn-row" style="margin-top:24px">
        <a class="btn" href="#deelneem">{bi("Raak betrokke", "Get involved")}{icon("arrow-right", "icon--arrow")}</a>
        <a class="btn btn--ghost" href="{s['facebook']}" target="_blank" rel="noopener">{icon("facebook")}{bi("Uitslae op Facebook", "Results on Facebook")}</a>
      </div>
    </div>
    {media}
  </div>
</section>

<section class="section section--paper" aria-labelledby="verwag-title">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">{bi("Wat om te verwag", "What to expect")}</p>
      <h2 id="verwag-title">{bi("Hoogtepunte", "Highlights")}</h2>
    </div>
    <div class="card-grid card-grid--3">{highlights}</div>
  </div>
</section>

<section class="section" id="deelneem" aria-labelledby="inligting-title">
  <div class="container admit">
    <div>
      <div class="section-head reveal" style="margin-bottom:24px">
        <p class="eyebrow">{bi("Praktiese inligting", "Practical information")}</p>
        <h2 id="inligting-title">{bi("Wat jy nodig het", "What you need")}</h2>
      </div>
      {kit}
    </div>
    <aside class="panel panel--navy reveal" style="--delay:100ms;align-self:start">
      <h3>{bi("Wil jy deelneem?", "Want to take part?")}</h3>
      <p style="color:var(--on-dark-muted)">{bi("Kontak die skool vir oefentye en meer inligting oor " + af_l + " by Dinamika.", "Contact the school for practice times and more information about " + en_l + " at Dinamika.")}</p>
      <ul class="footer-contact">
        <li>{icon("phone")}<a href="tel:{s['phone_href']}">{s['phone']}</a></li>
        <li>{icon("mail")}<a href="mailto:{s['email']}?subject={en.replace(' ', '%20')}">{s['email']}</a></li>
      </ul>
      <a class="btn btn--mint" href="kontak.html">{bi("Stuur 'n navraag", "Send an enquiry")}{icon("arrow-right", "icon--arrow")}</a>
    </aside>
  </div>
</section>

{gallery}

<section class="section section--paper" data-news-section hidden aria-labelledby="nuus-title">
  <div class="container">
    <div class="section-head section-head--split">
      <div><p class="eyebrow">Namies Nuus</p><h2 id="nuus-title">{bi("Nuus oor " + af_l, en + " news")}</h2></div>
      <a class="btn btn--ghost" href="nuus.html">{bi("Alle nuus", "All news")}{icon("arrow-right", "icon--arrow")}</a>
    </div>
    <div class="news-grid news-grid--3" data-news-list data-category="{sp['news']}" data-limit="3"></div>
  </div>
</section>
@@NEWS_MODAL@@

<section class="section" aria-labelledby="ander-title">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">{bi("Ontdek meer", "Discover more")}</p>
      <h2 id="ander-title">{bi("Ander sportsoorte", "Other sports")}</h2>
    </div>
    {sport_grid(sp["slug"])}
  </div>
</section>
"""
    meta = {
        "active": "sport-kultuur",
        "title_af": f"{af} | Sport | Hoërskool Dinamika",
        "title_en": f"{en} | Sport | Hoërskool Dinamika",
        "desc_af": sp["intro"][0][0][:155].replace('"', "'"),
        "desc_en": sp["intro"][0][1][:155].replace('"', "'"),
        "og_image": photos[0][0] if photos else "leaders.jpg",
        "scripts": ["news-data.js"],
    }
    return meta, body


def render(meta: dict, body: str, out_name: str) -> None:
    for k, v in PARTIALS.items():
        body = body.replace(f"@@{k}@@", v)
    body = expand(body)
    page = (head(meta) + f'\n<body class="page-{meta["active"]}">' + header(meta["active"])
            + f'<main id="main" tabindex="-1">\n{body}\n</main>' + footer(meta.get("scripts", [])))
    (ROOT / out_name).write_text(page, encoding="utf-8")
    print(f"  built {out_name}")


def build() -> None:
    PARTIALS["SPORT_GRID"] = sport_grid()
    count = 0
    for src in sorted(PAGES.glob("*.html")):
        raw = src.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--META\s*(\{.*?\})\s*-->", raw, flags=re.S)
        if not m:
            raise SystemExit(f"{src.name}: missing <!--META {{...}} --> block")
        render(json.loads(m.group(1)), raw[m.end():], src.name)
        count += 1
    for sp in SPORTS:
        meta, body = sport_page(sp)
        render(meta, body, f"sport-{sp['slug']}.html")
        count += 1
    print(f"Done — {count} pages.")


if __name__ == "__main__":
    build()
