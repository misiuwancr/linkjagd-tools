#!/usr/bin/env python3
"""Zweiundzwanzigste Liste: E-Mail, Fernwartung und Kasse."""

from __future__ import annotations

import json
import sqlite3
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def slugify(value: str) -> str:
    text = value.strip().lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    out, prev = [], False
    for ch in text:
        if ch.isalnum():
            out.append(ch)
            prev = False
        elif not prev:
            out.append("-")
            prev = True
    return "".join(out).strip("-")[:80]


def tool(name, url, domain, price, license_type, cats, short, long, features, uses, beginner=False):
    return {
        "name": name, "originalUrl": url, "domain": domain, "pricingModel": price,
        "licenseType": license_type, "categorySlugs": cats, "shortDescriptionDe": short,
        "longDescriptionDe": long, "featuresDe": features, "useCasesDe": uses,
        "partnerStatus": "none_found", "programPresence": "unknown", "programInfoUrl": "",
        "network": "manual", "verified": True, "beginnerFriendly": beginner,
        "discoverySource": "offizielle-website", "oss": None,
    }


E = []


def add(*a, **k):
    E.append(tool(*a, **k))


add("StartMail", "https://www.startmail.com/", "startmail.com", "paid", "proprietary", ["produktivitaet"],
    "StartMail ist ein E-Mail-Dienst mit Verschlüsselung und eigenem Postfach.",
    "StartMail legt ein Postfach an und kann Nachrichten verschlüsseln. Die Nutzung ist kostenpflichtig.",
    ["Eigenes Postfach", "Verschlüsselung", "Kostenpflichtige Nutzung"],
    ["Mail über einen eigenen Anbieter zu lesen", "Eine Nachricht verschlüsselt zu senden"], False)
add("ConnectWise", "https://www.connectwise.com/", "connectwise.com", "paid", "proprietary", ["kundenservice"],
    "ConnectWise steuert Fernwartung, Tickets und Abläufe für IT-Teams.",
    "ConnectWise bündelt Sitzungen auf fremden Rechnern und die zugehörigen Tickets. Die Nutzung ist kostenpflichtig.",
    ["Fernwartung", "Tickets", "Kostenpflichtige Nutzung"],
    ["Einen Rechner im Support zu öffnen", "Ein Ticket zur Sitzung zu führen"], False)
add("finAPI", "https://www.finapi.io/", "finapi.io", "freemium", "proprietary", ["finanzen", "programmierung"],
    "finAPI verbindet Anwendungen mit Bankkonten über eine Schnittstelle.",
    "finAPI holt Umsätze und Kontostände für eine eigene App. Es gibt einen Einstieg und bezahlte Nutzung.",
    ["Bankdaten per Schnittstelle", "Umsätze", "Einstieg und bezahlte Nutzung"],
    ["Umsätze in eine eigene App zu holen", "Ein Konto anzubinden"], False)
add("Square", "https://www.square.com/", "square.com", "freemium", "proprietary", ["e-commerce"],
    "Square nimmt Zahlungen an der Kasse und im Onlineshop entgegen.",
    "Square verbindet Kartenleser, Kasse und eine Rechnung. Es gibt einen Einstieg und Gebühren je Zahlung.",
    ["Kasse und Onlineshop", "Kartenzahlung", "Einstieg und Gebühren je Zahlung"],
    ["Eine Zahlung vor Ort anzunehmen", "Einen Beleg aus der Kasse zu erstellen"], True)
add("Zettle", "https://www.zettle.com/", "zettle.com", "freemium", "proprietary", ["e-commerce"],
    "Zettle nimmt Zahlungen an der Kasse entgegen und führt den Umsatz.",
    "Zettle verbindet ein Lesegerät mit einer Kassen-App. Es gibt einen Einstieg und Gebühren je Zahlung.",
    ["Kassen-App", "Kartenzahlung", "Gebühren je Zahlung"],
    ["An einem Stand Karte zu akzeptieren", "Den Umsatz des Tages zu sehen"], True)


def validate(entries):
    db = sqlite3.connect(ROOT / "data" / "linkjagd.db")
    domains = {row[0] for row in db.execute("select domain from tools")}
    slugs = {row[0] for row in db.execute("select slug from tools")}
    seen_d, seen_s, errors = set(), set(), []
    for entry in entries:
        slug = slugify(entry["name"])
        if entry["domain"] in domains:
            errors.append(f"db-domain {entry['domain']} {entry['name']}")
        if slug in slugs:
            errors.append(f"db-slug {slug} {entry['name']}")
        if entry["domain"] in seen_d:
            errors.append(f"dup {entry['domain']}")
        if slug in seen_s:
            errors.append(f"dup-slug {slug}")
        seen_d.add(entry["domain"])
        seen_s.add(slug)
        if not (10 <= len(entry["shortDescriptionDe"]) <= 280):
            errors.append(f"kurz {entry['name']} {len(entry['shortDescriptionDe'])}")
    if errors:
        raise SystemExit("\n".join(errors))
    return entries


if __name__ == "__main__":
    rows = validate(E)
    out = ROOT / "data" / "verified-tools-batch22.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows))
