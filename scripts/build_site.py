#!/usr/bin/env python3
"""Render the use-case guides (docs/USE_CASES*.md) into GitHub Pages HTML
and refresh docs/sitemap.xml.

    pip install markdown
    python3 scripts/build_site.py

Run after editing docs/USE_CASES.md or docs/USE_CASES.en.md.
"""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify_unicode

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = "https://roni5604.github.io/hebrew-words-db/"
REPO = "https://github.com/roni5604/hebrew-words-db/blob/main/"

PAGES = [
    {
        "src": DOCS / "USE_CASES.md",
        "out": DOCS / "use-cases.html",
        "lang": "he",
        "dir": "rtl",
        "title": "מה אפשר לבנות עם מאגר מילים בעברית — מדריך שימושים",
        "desc": "מדריך מלא לשימושים במאגר מילים בעברית: משחקי מילים, בדיקת איות, "
                "חיפוש באתרים, AI ומודלי שפה, OCR, חינוך, נגישות ואבטחה — עם קוד לדוגמה.",
        "nav": [("ראשי", "./"), ("מדריך שימושים", "use-cases.html"),
                ("English", "en/use-cases.html"), ("GitHub", "https://github.com/roni5604/hebrew-words-db")],
        "prefix": "",
    },
    {
        "src": DOCS / "USE_CASES.en.md",
        "out": DOCS / "en" / "use-cases.html",
        "lang": "en",
        "dir": "ltr",
        "title": "What you can build with a Hebrew word list — use-case guide",
        "desc": "Complete guide to using a free CC0 Hebrew word list: word games, "
                "spellcheck, site search, LLMs & NLP, OCR, education, accessibility "
                "and security — with runnable code.",
        "nav": [("Home", "../"), ("Use cases", "use-cases.html"),
                ("עברית", "../use-cases.html"), ("GitHub", "https://github.com/roni5604/hebrew-words-db")],
        "prefix": "../",
    },
]

TEMPLATE = """<!doctype html>
<html lang="{lang}" dir="{dir}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="he" href="{site}use-cases.html">
<link rel="alternate" hreflang="en" href="{site}en/use-cases.html">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}social-preview.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"TechArticle","headline":"{title}","description":"{desc}","inLanguage":"{lang}","url":"{url}","dateModified":"{date}","author":{{"@type":"Person","name":"Roni Michaeli","url":"https://ronimichaeli.com/"}},"about":{{"@type":"Dataset","name":"hebrew-words-db","url":"https://github.com/roni5604/hebrew-words-db","license":"https://creativecommons.org/publicdomain/zero/1.0/"}}}}
</script>
<style>
  :root {{ --bg:#f7f8fb; --card:#fff; --ink:#14182b; --muted:#5d6480; --line:#e2e5ee; --accent:#0038b8; --code:#eef1f8; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --bg:#0f1220; --card:#181c2e; --ink:#eef0f8; --muted:#a2a8c3; --line:#2a2f47; --accent:#7aa2ff; --code:#11152a; }} }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font:17px/1.75 system-ui, -apple-system, "Segoe UI", Arial, sans-serif; }}
  nav {{ position:sticky; top:0; background:var(--card); border-bottom:1px solid var(--line); z-index:1; }}
  nav div {{ max-width:860px; margin:0 auto; padding:10px 16px; display:flex; gap:18px; flex-wrap:wrap; font-size:15px; }}
  main {{ max-width:860px; margin:0 auto; padding:24px 16px 64px; }}
  h1 {{ font-size:clamp(26px,5vw,38px); line-height:1.25; }}
  h2 {{ margin-top:48px; padding-top:12px; border-top:1px solid var(--line); }}
  h3 {{ margin-top:28px; }}
  a {{ color:var(--accent); }}
  code {{ background:var(--code); padding:1px 5px; border-radius:5px; font-size:.88em; }}
  pre {{ direction:ltr; text-align:left; background:var(--code); border:1px solid var(--line); border-radius:10px; padding:12px; overflow-x:auto; }}
  pre code {{ background:none; padding:0; }}
  table {{ border-collapse:collapse; width:100%; display:block; overflow-x:auto; font-size:15px; }}
  th, td {{ border:1px solid var(--line); padding:8px 10px; text-align:start; vertical-align:top; }}
  th {{ background:var(--code); }}
  blockquote {{ margin:16px 0; padding:8px 16px; border-inline-start:4px solid var(--accent); background:var(--card); border-radius:6px; }}
  .cta {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px 20px; margin:32px 0; }}
  footer {{ color:var(--muted); font-size:14px; margin-top:40px; }}
</style>
</head>
<body>
<nav><div>{nav}</div></nav>
<main>
{body}
<div class="cta">{cta}</div>
<footer>Data: CC0 1.0 · Code: MIT · <a href="https://ronimichaeli.com/">Roni Michaeli · רוני מיכאלי</a> · {date}</footer>
</main>
</body>
</html>
"""

CTA = {
    "he": '⬇️ <b>להורדת המאגר:</b> <a href="https://raw.githubusercontent.com/roni5604/hebrew-words-db/main/data/words.txt">words.txt</a> · '
          '<a href="https://raw.githubusercontent.com/roni5604/hebrew-words-db/main/data/words.json">words.json</a> · '
          '<a href="https://raw.githubusercontent.com/roni5604/hebrew-words-db/main/data/words.csv">words.csv</a> — '
          'או <a href="{p}">נסו את בודק המילים</a> · <a href="https://github.com/roni5604/hebrew-words-db">⭐ GitHub</a>',
    "en": '⬇️ <b>Get the list:</b> <a href="https://raw.githubusercontent.com/roni5604/hebrew-words-db/main/data/words.txt">words.txt</a> · '
          '<a href="https://raw.githubusercontent.com/roni5604/hebrew-words-db/main/data/words.json">words.json</a> · '
          '<a href="https://raw.githubusercontent.com/roni5604/hebrew-words-db/main/data/words.csv">words.csv</a> — '
          'or <a href="{p}">try the word checker</a> · <a href="https://github.com/roni5604/hebrew-words-db">⭐ GitHub</a>',
}


def rewrite_links(html: str, prefix: str) -> str:
    def fix(m: re.Match) -> str:
        href = m.group(1)
        if href.startswith(("http", "#", "mailto:")):
            return m.group(0)
        if href in ("USE_CASES.en.md",):
            return 'href="en/use-cases.html"'
        if href in ("USE_CASES.md",):
            return 'href="../use-cases.html"'
        path = href[3:] if href.startswith("../") else "docs/" + href
        return f'href="{REPO}{path}"'

    return re.sub(r'href="([^"]+)"', fix, html)


def main() -> None:
    today = dt.date.today().isoformat()
    for page in PAGES:
        md = page["src"].read_text(encoding="utf-8")
        body = markdown.markdown(
            md,
            extensions=["tables", "fenced_code", "toc", "sane_lists"],
            extension_configs={"toc": {"slugify": slugify_unicode}},
        )
        body = rewrite_links(body, page["prefix"])
        url = SITE + page["out"].relative_to(DOCS).as_posix()
        nav = " ".join(f'<a href="{h}">{t}</a>' for t, h in page["nav"])
        html = TEMPLATE.format(
            lang=page["lang"], dir=page["dir"], title=page["title"], desc=page["desc"],
            url=url, site=SITE, date=today, nav=nav, body=body,
            cta=CTA[page["lang"]].format(p=page["prefix"] or "./"),
        )
        page["out"].parent.mkdir(parents=True, exist_ok=True)
        page["out"].write_text(html, encoding="utf-8")
        print("wrote", page["out"].relative_to(ROOT))

    urls = [SITE, SITE + "use-cases.html", SITE + "en/use-cases.html"]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls]
    sitemap.append("</urlset>")
    (DOCS / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    print("wrote docs/sitemap.xml")


if __name__ == "__main__":
    main()
