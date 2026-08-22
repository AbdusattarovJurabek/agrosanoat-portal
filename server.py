#!/usr/bin/env python3
"""Agrosanoat portalining dependency-siz HTTP serveri va JSON API-si."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import mimetypes
import os
import re
import secrets
import tempfile
import threading
import time
from datetime import date, datetime, timedelta, timezone
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
CONTENT_FILE = DATA_DIR / "content.json"
CONTACTS_FILE = DATA_DIR / "contacts.json"
MAX_JSON_BODY = 3 * 1024 * 1024
SESSION_TTL = 8 * 60 * 60
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "0") == "1"
SESSION_COOKIE = "agro_admin_session"

_sessions: dict[str, float] = {}
_login_attempts: dict[str, list[float]] = {}
_contact_attempts: dict[str, list[float]] = {}
_state_lock = threading.RLock()
_file_lock = threading.RLock()


class ValidationError(ValueError):
    pass


def _text(value, field: str, *, minimum: int = 0, maximum: int = 500) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{field} matn bo‘lishi kerak")
    value = value.strip()
    if len(value) < minimum:
        raise ValidationError(f"{field} kamida {minimum} ta belgidan iborat bo‘lishi kerak")
    if len(value) > maximum:
        raise ValidationError(f"{field} {maximum} ta belgidan oshmasligi kerak")
    if any(ord(character) < 32 and character not in "\n\r\t" for character in value):
        raise ValidationError(f"{field} tarkibida ruxsat etilmagan boshqaruv belgisi bor")
    if "<" in value or ">" in value:
        raise ValidationError(f"{field} tarkibida HTML teglaridan foydalanish mumkin emas")
    return value


TRANSLATED_LANGUAGES = ("ru", "en")
EMAIL_RE = re.compile(r"^[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?(?:\.[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?)+$", re.IGNORECASE)


def _email(value, field: str = "Email", *, required: bool = False) -> str:
    value = _text(value or "", field, minimum=3 if required else 0, maximum=160)
    if value and not EMAIL_RE.fullmatch(value):
        raise ValidationError(f"{field} formati noto‘g‘ri. Masalan: name@example.uz")
    return value


def _phone(value, field: str = "Telefon", *, required: bool = False) -> str:
    value = _text(value or "", field, minimum=9 if required else 0, maximum=40)
    if not value:
        return value
    digits = re.sub(r"\D", "", value)
    if len(digits) != 12 or not digits.startswith("998"):
        raise ValidationError(f"{field} +998 XX XXX-XX-XX formatida bo‘lishi kerak")
    if re.search(r"[^0-9+()\-\s]", value):
        raise ValidationError(f"{field} tarkibida noto‘g‘ri belgi bor")
    return value


def _person_name(value, field: str) -> str:
    value = _text(value, field, minimum=2, maximum=160)
    allowed_punctuation = {" ", "-", ".", "'", "‘", "’", "ʻ", "ʼ", "`"}
    if any(not character.isalpha() and character not in allowed_punctuation for character in value):
        raise ValidationError(f"{field} faqat harflar, bo‘sh joy, apostrof, nuqta va chiziqchadan iborat bo‘lishi kerak")
    if sum(character.isalpha() for character in value) < 2:
        raise ValidationError(f"{field} to‘liq kiritilishi kerak")
    return value


def _iso_date(value, field: str = "Sana") -> str:
    value = _text(value, field, minimum=10, maximum=10)
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(f"{field} YYYY-MM-DD formatidagi haqiqiy sana bo‘lishi kerak") from exc
    if parsed < date(2000, 1, 1) or parsed > date.today() + timedelta(days=366):
        raise ValidationError(f"{field} ruxsat etilgan davrdan tashqarida")
    return value


def _contact_channel(value) -> str:
    value = _text(value, "Telefon yoki email", minimum=5, maximum=180)
    if "@" in value:
        return _email(value, "Telefon yoki email", required=True)
    return _phone(value, "Telefon yoki email", required=True)


def _translations(item: dict, fields: dict[str, tuple[int, int]]) -> dict[str, dict[str, str]]:
    raw = item.get("translations", {})
    if raw is None:
        raw = {}
    if not isinstance(raw, dict):
        raise ValidationError("Tarjimalar formati noto‘g‘ri")
    result = {}
    for language in TRANSLATED_LANGUAGES:
        values = raw.get(language, {})
        if values is None:
            values = {}
        if not isinstance(values, dict):
            raise ValidationError(f"{language.upper()} tarjima formati noto‘g‘ri")
        has_translation = any(str(values.get(field, "")).strip() for field in fields)
        translated = {}
        for field, (minimum, maximum) in fields.items():
            value = values.get(field, "")
            translated[field] = _text(
                value,
                f"{language.upper()} {field}",
                minimum=minimum if has_translation and minimum else 0,
                maximum=maximum,
            )
        result[language] = translated
    return result


def validate_leadership(payload) -> list[dict]:
    if not isinstance(payload, list) or not 1 <= len(payload) <= 50:
        raise ValidationError("Rahbariyat ro‘yxati 1–50 ta yozuvdan iborat bo‘lishi kerak")
    result = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValidationError(f"Rahbariyat #{index + 1} noto‘g‘ri")
        photo = item.get("photo", "")
        result.append({
            "name": _person_name(item.get("name"), "F.I.SH."),
            "role": _text(item.get("role"), "Lavozim", minimum=2, maximum=180),
            "hours": _text(item.get("hours", ""), "Qabul vaqti", maximum=120),
            "email": _email(item.get("email", "")),
            "desc": _text(item.get("desc", ""), "Vakolatlar", maximum=1200),
            "photo": _image(photo) if photo else "",
            "translations": _translations(item, {
                "name": (2, 160),
                "role": (2, 180),
                "hours": (0, 120),
                "desc": (0, 1200),
            }),
        })
    return result


REGION_ID_RE = re.compile(r"^[a-z0-9_\-]{2,50}$")


def validate_regions(payload) -> dict[str, dict]:
    if not isinstance(payload, dict) or not 1 <= len(payload) <= 50:
        raise ValidationError("Hududlar ro‘yxati 1–50 ta yozuvdan iborat bo‘lishi kerak")
    result = {}
    for key, item in payload.items():
        if not isinstance(key, str) or not REGION_ID_RE.fullmatch(key):
            raise ValidationError("Hudud ID-si faqat kichik lotin harflari, raqam, _ yoki - dan iborat bo‘lishi kerak")
        if not isinstance(item, dict):
            raise ValidationError(f"{key} hududi noto‘g‘ri")
        result[key] = {
            "name": _text(item.get("name"), "Boshqarma nomi", minimum=2, maximum=180),
            "head": _text(item.get("head", ""), "Rahbar", maximum=160),
            "phone": _phone(item.get("phone", "")),
            "address": _text(item.get("address", ""), "Manzil", maximum=300),
            "projects": _text(item.get("projects", ""), "Loyihalar", maximum=1200),
            "translations": _translations(item, {
                "name": (2, 180),
                "head": (0, 160),
                "address": (0, 300),
                "projects": (0, 1200),
            }),
        }
    return result


DATA_IMAGE_RE = re.compile(r"^data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/=]+)$")
LOCAL_IMAGE_RE = re.compile(r"^assets/(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_-]+\.(?:png|jpe?g|webp|svg)$", re.IGNORECASE)


def _image(value) -> str:
    value = _text(value or "assets/hero_agri.jpg", "Rasm", maximum=2_800_000)
    if LOCAL_IMAGE_RE.fullmatch(value):
        target = (ROOT / value).resolve()
        assets_root = (ROOT / "assets").resolve()
        if not str(target).startswith(str(assets_root) + os.sep) or not target.is_file():
            raise ValidationError("Ko‘rsatilgan lokal rasm topilmadi")
        return value
    match = DATA_IMAGE_RE.fullmatch(value)
    if not match:
        raise ValidationError("Rasm lokal assets yo‘li yoki PNG/JPEG/WEBP data URL bo‘lishi kerak")
    try:
        raw = base64.b64decode(match.group(2), validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise ValidationError("Rasm ma’lumoti buzilgan") from exc
    if len(raw) > 2 * 1024 * 1024:
        raise ValidationError("Rasm hajmi 2 MB dan oshmasligi kerak")
    return value


def validate_news(item, *, existing_id=None) -> dict:
    if not isinstance(item, dict):
        raise ValidationError("Yangilik ma’lumoti noto‘g‘ri")
    news_id = existing_id if existing_id is not None else item.get("id")
    if news_id is None:
        news_id = int(time.time() * 1000)
    try:
        news_id = int(news_id)
    except (TypeError, ValueError) as exc:
        raise ValidationError("Yangilik ID-si noto‘g‘ri") from exc
    return {
        "id": news_id,
        "title": _text(item.get("title"), "Sarlavha", minimum=4, maximum=240),
        "date": _iso_date(item.get("date") or datetime.now(timezone.utc).date().isoformat()),
        "category": _text(item.get("category", "Xabar"), "Kategoriya", minimum=2, maximum=80),
        "author": _text(item.get("author", "Agentlik Matbuot Xizmati"), "Muallif", maximum=160),
        "image": _image(item.get("image")),
        "excerpt": _text(item.get("excerpt"), "Qisqacha mazmun", minimum=10, maximum=1200),
        "content": _text(item.get("content"), "Batafsil matn", minimum=20, maximum=20_000),
        "translations": _translations(item, {
            "title": (4, 240),
            "category": (2, 80),
            "author": (0, 160),
            "excerpt": (10, 1200),
            "content": (20, 20_000),
        }),
    }


def validate_contact(item) -> dict:
    if not isinstance(item, dict):
        raise ValidationError("Murojaat ma’lumoti noto‘g‘ri")
    if item.get("website"):
        raise ValidationError("So‘rov qabul qilinmadi")
    return {
        "id": secrets.token_hex(12),
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "name": _text(item.get("name"), "Ism", minimum=2, maximum=160),
        "contact": _contact_channel(item.get("contact")),
        "message": _text(item.get("message"), "Murojaat", minimum=10, maximum=5000),
        "status": "new",
    }


def read_json(path: Path, default):
    with _file_lock:
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError:
            return default


def write_json_atomic(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _file_lock:
        fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(data, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, path)
        except Exception:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:
                pass
            raise


def _prune_sessions() -> None:
    now = time.time()
    with _state_lock:
        expired = [token for token, expiry in _sessions.items() if expiry <= now]
        for token in expired:
            _sessions.pop(token, None)


def _rate_allowed(bucket: dict[str, list[float]], key: str, *, limit: int, window: int) -> bool:
    now = time.time()
    with _state_lock:
        recent = [stamp for stamp in bucket.get(key, []) if stamp > now - window]
        if len(recent) >= limit:
            bucket[key] = recent
            return False
        recent.append(now)
        bucket[key] = recent
        return True


class PortalHandler(BaseHTTPRequestHandler):
    server_version = "AgroPortal/1.0"

    def _security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' "
            "https://fonts.googleapis.com https://cdnjs.cloudflare.com; font-src 'self' "
            "https://fonts.gstatic.com https://cdnjs.cloudflare.com; img-src 'self' data:; "
            "connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'",
        )

    def _json(self, status: int, payload, *, cookie: str | None = None) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._security_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValidationError("Content-Length noto‘g‘ri") from exc
        if length <= 0 or length > MAX_JSON_BODY:
            raise ValidationError("So‘rov hajmi noto‘g‘ri yoki juda katta")
        if "application/json" not in self.headers.get("Content-Type", ""):
            raise ValidationError("Content-Type application/json bo‘lishi kerak")
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValidationError("JSON ma’lumoti noto‘g‘ri") from exc

    def _client_ip(self) -> str:
        return self.client_address[0]

    def _same_origin(self) -> bool:
        origin = self.headers.get("Origin")
        if not origin:
            return True
        parsed = urlparse(origin)
        return parsed.netloc == self.headers.get("Host") and parsed.scheme in {"http", "https"}

    def _session_token(self) -> str | None:
        cookie = SimpleCookie()
        try:
            cookie.load(self.headers.get("Cookie", ""))
        except Exception:
            return None
        morsel = cookie.get(SESSION_COOKIE)
        return morsel.value if morsel else None

    def _authenticated(self) -> bool:
        _prune_sessions()
        token = self._session_token()
        if not token:
            return False
        with _state_lock:
            expiry = _sessions.get(token, 0)
            if expiry <= time.time():
                _sessions.pop(token, None)
                return False
            _sessions[token] = time.time() + SESSION_TTL
            return True

    def _require_auth(self) -> bool:
        if self._authenticated():
            return True
        self._json(HTTPStatus.UNAUTHORIZED, {"ok": False, "error": "Avtorizatsiya talab qilinadi"})
        return False

    def _require_mutation_guard(self) -> bool:
        if self._same_origin():
            return True
        self._json(HTTPStatus.FORBIDDEN, {"ok": False, "error": "Cross-origin so‘rov rad etildi"})
        return False

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health":
            self._json(HTTPStatus.OK, {"ok": True, "service": "agro-portal"})
            return
        if path == "/api/content":
            self._json(HTTPStatus.OK, read_json(CONTENT_FILE, {}))
            return
        if path == "/api/admin/session":
            self._json(HTTPStatus.OK, {"authenticated": self._authenticated(), "configured": bool(ADMIN_PASSWORD)})
            return
        if path == "/api/admin/contacts":
            if self._require_auth():
                self._json(HTTPStatus.OK, {"contacts": read_json(CONTACTS_FILE, [])})
            return
        if path.startswith("/api/"):
            self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "API manzili topilmadi"})
            return
        self._serve_static(path)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if not self._require_mutation_guard():
            return
        try:
            payload = self._read_body()
            if path == "/api/admin/login":
                self._login(payload)
            elif path == "/api/admin/logout":
                self._logout()
            elif path == "/api/contact":
                self._contact(payload)
            elif path == "/api/admin/news":
                if self._require_auth():
                    self._create_news(payload)
            else:
                self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "API manzili topilmadi"})
        except ValidationError as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
        except Exception:
            self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"ok": False, "error": "Server xatosi"})

    def do_PUT(self) -> None:
        path = urlparse(self.path).path
        if not self._require_mutation_guard() or not self._require_auth():
            return
        try:
            payload = self._read_body()
            content = read_json(CONTENT_FILE, {})
            if path == "/api/admin/leadership":
                content["leadership"] = validate_leadership(payload)
            elif path == "/api/admin/regions":
                content["regions"] = validate_regions(payload)
            elif path.startswith("/api/admin/news/"):
                news_id = int(path.rsplit("/", 1)[-1])
                updated = validate_news(payload, existing_id=news_id)
                news = content.get("news", [])
                index = next((i for i, item in enumerate(news) if int(item.get("id", -1)) == news_id), None)
                if index is None:
                    self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Yangilik topilmadi"})
                    return
                news[index] = updated
                content["news"] = news
            else:
                self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "API manzili topilmadi"})
                return
            write_json_atomic(CONTENT_FILE, content)
            self._json(HTTPStatus.OK, {"ok": True})
        except (ValueError, ValidationError) as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
        except Exception:
            self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"ok": False, "error": "Server xatosi"})

    def do_DELETE(self) -> None:
        path = urlparse(self.path).path
        if not self._require_mutation_guard() or not self._require_auth():
            return
        try:
            if not path.startswith("/api/admin/news/"):
                self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "API manzili topilmadi"})
                return
            news_id = int(path.rsplit("/", 1)[-1])
            content = read_json(CONTENT_FILE, {})
            original = content.get("news", [])
            filtered = [item for item in original if int(item.get("id", -1)) != news_id]
            if len(filtered) == len(original):
                self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Yangilik topilmadi"})
                return
            content["news"] = filtered
            write_json_atomic(CONTENT_FILE, content)
            self._json(HTTPStatus.OK, {"ok": True})
        except ValueError:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "Yangilik ID-si noto‘g‘ri"})
        except Exception:
            self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"ok": False, "error": "Server xatosi"})

    def _login(self, payload) -> None:
        if not ADMIN_PASSWORD:
            self._json(HTTPStatus.SERVICE_UNAVAILABLE, {"ok": False, "error": "Serverda ADMIN_PASSWORD sozlanmagan"})
            return
        ip = self._client_ip()
        if not _rate_allowed(_login_attempts, ip, limit=5, window=15 * 60):
            self._json(HTTPStatus.TOO_MANY_REQUESTS, {"ok": False, "error": "Juda ko‘p urinish. 15 daqiqadan keyin qayta urinib ko‘ring"})
            return
        username = str(payload.get("username", "")) if isinstance(payload, dict) else ""
        password = str(payload.get("password", "")) if isinstance(payload, dict) else ""
        valid = hmac.compare_digest(username.encode(), ADMIN_USERNAME.encode()) and hmac.compare_digest(password.encode(), ADMIN_PASSWORD.encode())
        if not valid:
            self._json(HTTPStatus.UNAUTHORIZED, {"ok": False, "error": "Login yoki parol noto‘g‘ri"})
            return
        token = secrets.token_urlsafe(32)
        with _state_lock:
            _sessions[token] = time.time() + SESSION_TTL
            _login_attempts.pop(ip, None)
        secure = "; Secure" if COOKIE_SECURE else ""
        cookie = f"{SESSION_COOKIE}={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age={SESSION_TTL}{secure}"
        self._json(HTTPStatus.OK, {"ok": True}, cookie=cookie)

    def _logout(self) -> None:
        token = self._session_token()
        if token:
            with _state_lock:
                _sessions.pop(token, None)
        cookie = f"{SESSION_COOKIE}=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0"
        self._json(HTTPStatus.OK, {"ok": True}, cookie=cookie)

    def _contact(self, payload) -> None:
        ip = self._client_ip()
        if not _rate_allowed(_contact_attempts, ip, limit=5, window=60 * 60):
            self._json(HTTPStatus.TOO_MANY_REQUESTS, {"ok": False, "error": "Bir soatda 5 tadan ortiq murojaat yuborib bo‘lmaydi"})
            return
        contact = validate_contact(payload)
        contacts = read_json(CONTACTS_FILE, [])
        contacts.insert(0, contact)
        write_json_atomic(CONTACTS_FILE, contacts[:5000])
        self._json(HTTPStatus.CREATED, {"ok": True, "reference": contact["id"]})

    def _create_news(self, payload) -> None:
        article = validate_news(payload)
        content = read_json(CONTENT_FILE, {})
        news = content.get("news", [])
        news.insert(0, article)
        content["news"] = news[:500]
        write_json_atomic(CONTENT_FILE, content)
        self._json(HTTPStatus.CREATED, {"ok": True, "article": article})

    def _serve_static(self, path: str) -> None:
        raw = unquote(path)
        if raw == "/":
            raw = "/index.html"
        parts = Path(raw.lstrip("/")).parts
        if not parts or any(part.startswith(".") for part in parts) or parts[0] in {"data", "tests"}:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        target = (ROOT / Path(*parts)).resolve()
        if not str(target).startswith(str(ROOT) + os.sep) or not target.is_file() or target.name in {"server.py"}:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            body = target.read_bytes()
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        mime = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        if target.suffix in {".html", ".js", ".css", ".svg"}:
            mime += "; charset=utf-8"
        self.send_response(HTTPStatus.OK)
        self._security_headers()
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store" if target.name == "admin.html" else "public, max-age=300")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.address_string()} - {fmt % args}")


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    DATA_DIR.mkdir(exist_ok=True)
    if not CONTACTS_FILE.exists():
        write_json_atomic(CONTACTS_FILE, [])
    if not CONTENT_FILE.exists():
        raise SystemExit("data/content.json topilmadi")
    if not ADMIN_PASSWORD:
        print("DIQQAT: ADMIN_PASSWORD belgilanmagan — admin login o‘chirilgan.")
    server = ThreadingHTTPServer((host, port), PortalHandler)
    print(f"Agrosanoat portali: http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer to‘xtatildi.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
