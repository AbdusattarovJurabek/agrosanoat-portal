import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PAGES = (
    "index.html",
    "about.html",
    "contact.html",
    "documents.html",
    "leadership.html",
    "news.html",
    "news-detail.html",
    "regions.html",
)
MENU_KEYS = {
    "nav_home",
    "nav_about",
    "nav_news",
    "nav_contact",
    "nav_general",
    "nav_leadership",
    "nav_regions",
    "nav_official_news",
    "nav_documents",
}


class TranslationMarkupParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.keys = set()
        self.languages = set()

    def handle_starttag(self, _tag, attrs):
        values = dict(attrs)
        if values.get("data-i18n"):
            self.keys.add(values["data-i18n"])
        if values.get("data-lang"):
            self.languages.add(values["data-lang"])


class NavigationTranslationTests(unittest.TestCase):
    def test_every_public_page_has_three_languages_and_translated_menu(self):
        for filename in PUBLIC_PAGES:
            with self.subTest(page=filename):
                parser = TranslationMarkupParser()
                parser.feed((ROOT / filename).read_text(encoding="utf-8"))
                self.assertEqual(parser.languages, {"uz", "ru", "en"})
                self.assertTrue(MENU_KEYS.issubset(parser.keys), MENU_KEYS - parser.keys)

    def test_menu_dictionary_contains_every_language(self):
        script = (ROOT / "js" / "app.js").read_text(encoding="utf-8")
        for key in MENU_KEYS | {"nav_services", "top_open_data", "top_virtual_reception"}:
            with self.subTest(key=key):
                self.assertEqual(len(re.findall(rf"\b{re.escape(key)}\s*:", script)), 3)


if __name__ == "__main__":
    unittest.main()
