from pathlib import Path
from html.parser import HTMLParser
ROOT = Path(__file__).resolve().parents[1]
BASE = "https://ziontechgroup.com"
LOCALES = {"en": "en", "pt": "pt-BR", "es": "es", "fr": "fr", "de": "de"}
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.lang = None; self.links = []; self.alts = {}; self.canonical = None; self.items = 0; self.main = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = a.get("lang")
        if tag == "main": self.main = a.get("id") == "main"
        if tag == "li": self.items += 1
        if tag == "a": self.links.append(a.get("href"))
        if tag == "link" and a.get("rel") == "alternate": self.alts[a["hreflang"]] = a["href"]
        if tag == "link" and a.get("rel") == "canonical": self.canonical = a["href"]
for locale, lang in LOCALES.items():
    text = (ROOT / ("index.html" if locale == "en" else locale + "/index.html")).read_text()
    p = Page(); p.feed(text)
    url = BASE + "/site-survey-planner/" + ("" if locale == "en" else locale + "/")
    prefix = "" if locale == "en" else "/" + locale
    assert p.lang == lang and p.canonical == url and p.main and p.items == 6
    assert len(p.alts) == 6 and p.alts[lang] == url
    assert BASE + prefix + "/apps/app-experiment-planner.html" in p.links
    assert BASE + ("/discovery/" if locale == "en" else prefix + "/discovery/") in p.links
    assert "site-survey-translations-2026-10-08" in text
    assert "<script" not in text and "<form" not in text
    assert "commercial@ziontechgroup.com" in text and "assets/css/discovery.css" in text
print("PASS: five static locales, six-step checklist parity, canonical/hreflang, locale-preserving planner/Discovery links and no external submissions.")
