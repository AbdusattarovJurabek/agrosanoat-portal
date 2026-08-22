import json
import tempfile
import unittest
from pathlib import Path

import server


class ValidationTests(unittest.TestCase):
    def test_leadership_rejects_oversized_payloads(self):
        valid = [{
            "name": "Ali Valiyev",
            "role": "Direktor",
            "hours": "",
            "email": "a@example.uz",
            "desc": "Vakolatlar",
            "photo": "assets/hero_agri.jpg",
            "translations": {
                "ru": {"name": "Али Валиев", "role": "Директор"},
                "en": {"name": "Ali Valiyev", "role": "Director"},
            },
        }]
        self.assertEqual(server.validate_leadership(valid)[0]["name"], "Ali Valiyev")
        self.assertEqual(server.validate_leadership(valid)[0]["photo"], "assets/hero_agri.jpg")
        self.assertEqual(server.validate_leadership(valid)[0]["translations"]["ru"]["role"], "Директор")
        valid[0]["name"] = "x" * 161
        with self.assertRaises(server.ValidationError):
            server.validate_leadership(valid)

    def test_leadership_rejects_unsafe_photo_path(self):
        with self.assertRaises(server.ValidationError):
            server.validate_leadership([{
                "name": "Ali Valiyev",
                "role": "Direktor",
                "hours": "",
                "email": "a@example.uz",
                "desc": "Vakolatlar",
                "photo": "javascript:alert(1)",
            }])

    def test_leadership_rejects_invalid_name_and_email(self):
        base = {
            "name": "Ali Valiyev",
            "role": "Direktor",
            "email": "ali@example.uz",
            "photo": "assets/hero_agri.jpg",
        }
        with self.assertRaises(server.ValidationError):
            server.validate_leadership([{**base, "name": "Ali123"}])
        with self.assertRaises(server.ValidationError):
            server.validate_leadership([{**base, "email": "ali-at-example"}])

    def test_region_id_is_restricted(self):
        with self.assertRaises(server.ValidationError):
            server.validate_regions({
                "../secret": {
                    "name": "Test",
                    "head": "",
                    "phone": "",
                    "address": "",
                    "projects": "",
                }
            })

    def test_region_phone_must_be_uzbekistan_format(self):
        with self.assertRaises(server.ValidationError):
            server.validate_regions({
                "toshkent": {
                    "name": "Toshkent boshqarmasi",
                    "head": "",
                    "phone": "12345",
                    "address": "",
                    "projects": "",
                }
            })

    def test_news_accepts_plain_text_and_local_image(self):
        article = server.validate_news({
            "title": "Yangi rasmiy xabar",
            "date": "2026-08-19",
            "category": "Rasmiy",
            "author": "Matbuot xizmati",
            "image": "assets/hero_agri.jpg",
            "excerpt": "Bu yetarlicha uzun qisqacha mazmun.",
            "content": "Bu yangilikning yetarlicha uzun batafsil matni hisoblanadi.",
            "translations": {
                "en": {
                    "title": "A new official announcement",
                    "category": "Official",
                    "author": "Press service",
                    "excerpt": "This is a sufficiently detailed announcement summary.",
                    "content": "This is sufficiently detailed content for the official announcement.",
                }
            },
        })
        self.assertIsInstance(article["id"], int)
        self.assertEqual(article["image"], "assets/hero_agri.jpg")
        self.assertEqual(article["translations"]["en"]["category"], "Official")

    def test_news_rejects_javascript_image(self):
        with self.assertRaises(server.ValidationError):
            server.validate_news({
                "title": "Yangi rasmiy xabar",
                "date": "2026-08-19",
                "category": "Rasmiy",
                "author": "Matbuot xizmati",
                "image": "javascript:alert(1)",
                "excerpt": "Bu yetarlicha uzun qisqacha mazmun.",
                "content": "Bu yangilikning yetarlicha uzun batafsil matni hisoblanadi.",
            })

    def test_news_rejects_invalid_date_and_incomplete_translation(self):
        base = {
            "title": "Yangi rasmiy xabar",
            "date": "2026-02-30",
            "category": "Rasmiy",
            "author": "Matbuot xizmati",
            "image": "assets/hero_agri.jpg",
            "excerpt": "Bu yetarlicha uzun qisqacha mazmun.",
            "content": "Bu yangilikning yetarlicha uzun batafsil matni hisoblanadi.",
        }
        with self.assertRaises(server.ValidationError):
            server.validate_news(base)
        with self.assertRaises(server.ValidationError):
            server.validate_news({
                **base,
                "date": "2026-08-19",
                "translations": {"en": {"title": "Translated title only"}},
            })

    def test_contact_honeypot(self):
        with self.assertRaises(server.ValidationError):
            server.validate_contact({
                "name": "Test User",
                "contact": "test@example.uz",
                "message": "Yetarlicha uzun murojaat matni.",
                "website": "spam.example",
            })

    def test_contact_requires_valid_email_or_uzbekistan_phone(self):
        valid = {
            "name": "Test User",
            "contact": "+998 95 450-59-50",
            "message": "Yetarlicha uzun murojaat matni.",
        }
        self.assertEqual(server.validate_contact(valid)["contact"], "+998 95 450-59-50")
        with self.assertRaises(server.ValidationError):
            server.validate_contact({**valid, "contact": "not-a-contact"})

    def test_atomic_json_write(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            server.write_json_atomic(path, {"ok": True, "text": "O‘zbekcha"})
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["text"], "O‘zbekcha")


if __name__ == "__main__":
    unittest.main()
