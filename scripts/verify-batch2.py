#!/usr/bin/env python3
"""Prüft die zweite Liste einmalig: robots.txt, eine Antwort der offiziellen URL, Lizenzbeleg."""

from __future__ import annotations

import json
import sqlite3
import ssl
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "data" / "batch2-candidates.json"
OUT = ROOT / "data" / "verified-tools-batch2.json"
SKIPPED = ROOT / "data" / "batch2-skipped.json"
DB = ROOT / "data" / "linkjagd.db"
ARTIFACTS = Path("/opt/cursor/artifacts")

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
SHARED = {
    "github.com",
    "gitlab.com",
    "invent.kde.org",
    "huggingface.co",
    "apps.apple.com",
    "chromewebstore.google.com",
}
CTX = ssl.create_default_context()


def slugify(value: str) -> str:
    import unicodedata

    text = value.strip().lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    out = []
    for ch in text:
        out.append(ch if ch.isalnum() else "-")
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:80]


def domain_of(url: str) -> str:
    host = urlparse(url).hostname or ""
    return host.lower().removeprefix("www.")


def path_of(url: str) -> str:
    path = urlparse(url).path.rstrip("/") or "/"
    return path


def fetch(url: str, timeout: int = 20) -> tuple[int, str, bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8"})
    with urllib.request.urlopen(request, timeout=timeout, context=CTX) as response:
        body = response.read(200_000)
        return response.status, response.geturl(), body


def robots_allows(url: str) -> tuple[bool, str]:
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    status = 0
    body = b""
    last_error = "robots.txt nicht lesbar"
    for attempt in range(3):
        try:
            status, _, body = fetch(robots_url, timeout=12)
            last_error = ""
            break
        except urllib.error.HTTPError as error:
            if error.code in (404, 410):
                return True, "keine robots.txt"
            last_error = f"robots.txt HTTP {error.code}"
            if error.code != 429:
                return False, last_error
        except Exception as error:
            last_error = f"robots.txt nicht lesbar: {error.__class__.__name__}"
            return False, last_error
        import time
        time.sleep(2 * (attempt + 1))
    if last_error:
        return False, last_error
    if status >= 400:
        return False, f"robots.txt HTTP {status}"
    text = body.decode("utf-8", "replace")
    groups: list[tuple[bool, list[str], list[str]]] = []
    current_star = False
    disallow: list[str] = []
    allow: list[str] = []
    seen = False

    def flush() -> None:
        nonlocal disallow, allow, seen
        if seen:
            groups.append((True, disallow, allow))
        disallow, allow, seen_reset = [], [], False
        return seen_reset

    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if key == "user-agent":
            if seen:
                groups.append((current_star, disallow, allow))
            current_star = value == "*"
            disallow, allow = [], []
            seen = current_star
            continue
        if not seen:
            continue
        if key == "disallow" and value:
            disallow.append(value)
        elif key == "allow" and value:
            allow.append(value)
    if seen:
        groups.append((current_star, disallow, allow))
    path = parsed.path or "/"
    best_allow = -1
    best_disallow = -1
    for _star, dis, alw in groups:
        for rule in alw:
            prefix = rule.replace("$", "")
            if path.startswith(prefix) and len(prefix) > best_allow:
                best_allow = len(prefix)
        for rule in dis:
            prefix = rule.replace("$", "")
            if prefix and path.startswith(prefix) and len(prefix) > best_disallow:
                best_disallow = len(prefix)
    if best_disallow >= 0 and best_disallow > best_allow:
        return False, "robots.txt untersagt die Adresse"
    return True, "erlaubt"


def existing_keys() -> tuple[set[str], dict[str, set[str]], set[str]]:
    connection = sqlite3.connect(DB)
    rows = connection.execute("select name, domain, original_url from tools").fetchall()
    connection.close()
    domains = {row[1] for row in rows}
    paths: dict[str, set[str]] = {}
    slugs = {slugify(row[0]) for row in rows}
    for _name, domain, url in rows:
        paths.setdefault(domain, set()).add(path_of(url))
    return domains, paths, slugs


def check(entry: dict, domains: set[str], paths: dict[str, set[str]], slugs: set[str]) -> tuple[dict | None, dict | None]:
    name = entry["name"]
    url = entry["originalUrl"]
    domain = domain_of(url)
    if domain != entry["domain"]:
        return None, {"name": name, "url": url, "reason": f"Domain weicht ab: {domain} statt {entry['domain']}"}
    slug = slugify(name)
    if slug in slugs:
        return None, {"name": name, "url": url, "reason": f"Kurzname {slug} ist schon vergeben"}
    if domain in domains and domain not in SHARED:
        return None, {"name": name, "url": url, "reason": f"Domain {domain} ist schon im Verzeichnis"}
    if domain in SHARED and path_of(url) in paths.get(domain, set()):
        return None, {"name": name, "url": url, "reason": "Dieselbe Adresse auf einem gemeinsamen Host ist schon vergeben"}
    allowed, robots_reason = robots_allows(url)
    if not allowed:
        return None, {"name": name, "url": url, "reason": robots_reason}
    try:
        status, final, body = fetch(url)
    except urllib.error.HTTPError as error:
        return None, {"name": name, "url": url, "reason": f"HTTP {error.code}"}
    except Exception as error:
        return None, {"name": name, "url": url, "reason": f"nicht erreichbar: {error.__class__.__name__}"}
    if status < 200 or status >= 300:
        return None, {"name": name, "url": url, "reason": f"HTTP {status}"}
    sample = body[:4000].decode("utf-8", "replace").lower()
    if "just a moment" in sample or "attention required" in sample or "cf-browser-verification" in sample:
        return None, {"name": name, "url": url, "reason": "Antwort ist eine Zugriffsprüfung, nicht die Website"}
    if "domain is for sale" in sample or "hugedomains" in sample:
        return None, {"name": name, "url": url, "reason": "Antwort wirkt wie eine geparkte Domain"}
    evidence = entry.get("evidence")
    if evidence:
        try:
            estatus, _, ebody = fetch(evidence["url"])
        except Exception as error:
            return None, {"name": name, "url": url, "reason": f"Lizenzbeleg nicht lesbar: {error.__class__.__name__}"}
        if estatus < 200 or estatus >= 300:
            return None, {"name": name, "url": url, "reason": f"Lizenzbeleg HTTP {estatus}"}
        text = ebody.decode("utf-8", "replace")
        missing = [needle for needle in evidence["needles"] if needle not in text]
        if missing:
            return None, {"name": name, "url": url, "reason": "Lizenzbeleg enthält die erwartete Stelle nicht: " + ", ".join(missing)}
    clean = {key: value for key, value in entry.items() if key != "evidence"}
    clean["verified"] = True
    return clean, {"name": name, "url": url, "final": final, "note": robots_reason}


def main() -> None:
    entries = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    domains, paths, slugs = existing_keys()
    accepted: list[dict] = []
    skipped: list[dict] = []
    seen_slugs = set(slugs)
    seen_domain = set(domains)
    seen_paths = {key: set(value) for key, value in paths.items()}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(check, entry, domains, paths, slugs) for entry in entries]
        results = []
        for future in as_completed(futures):
            results.append(future.result())
    mapped: dict[str, tuple] = {}
    for clean, info in results:
        mapped[info["name"]] = (clean, info)
    for entry in entries:
        clean, info = mapped[entry["name"]]
        if clean is None:
            skipped.append({"name": info["name"], "url": info["url"], "reason": info["reason"]})
            continue
        slug = slugify(clean["name"])
        domain = clean["domain"]
        path = path_of(clean["originalUrl"])
        if slug in seen_slugs:
            skipped.append({"name": clean["name"], "url": clean["originalUrl"], "reason": f"Kurzname {slug} kollidiert in dieser Liste"})
            continue
        if domain not in SHARED and domain in seen_domain:
            skipped.append({"name": clean["name"], "url": clean["originalUrl"], "reason": f"Domain {domain} kollidiert in dieser Liste"})
            continue
        if domain in SHARED and path in seen_paths.get(domain, set()):
            skipped.append({"name": clean["name"], "url": clean["originalUrl"], "reason": "Adresse kollidiert in dieser Liste"})
            continue
        seen_slugs.add(slug)
        seen_domain.add(domain)
        seen_paths.setdefault(domain, set()).add(path)
        accepted.append(clean)
    OUT.write_text(json.dumps(accepted, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SKIPPED.write_text(json.dumps(skipped, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / "batch2-skipped.json").write_text(SKIPPED.read_text(encoding="utf-8"), encoding="utf-8")
    print(json.dumps({"accepted": len(accepted), "skipped": len(skipped)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
