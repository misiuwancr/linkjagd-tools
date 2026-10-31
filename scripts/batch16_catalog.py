#!/usr/bin/env python3
"""Sechzehnte Liste: bekannte KI-Tools, die noch gefehlt haben."""

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


add("Hailuo", "https://hailuoai.video/", "hailuoai.video", "freemium", "proprietary", ["videogenerierung"],
    "Hailuo erzeugt kurze Videos aus Text oder einem Bild.",
    "Hailuo, von MiniMax, nimmt eine Beschreibung und liefert einen Clip. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Video aus Text oder Bild", "Kurze Clips", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Einen kurzen Clip aus einer Beschreibung zu erzeugen", "Ein Standbild in Bewegung zu setzen"], True)
add("Haiper", "https://haiper.ai/", "haiper.ai", "freemium", "proprietary", ["videogenerierung"],
    "Haiper macht kurze Videos aus Text und Bildern.",
    "Haiper nimmt einen Prompt und erzeugt einen Clip. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Video aus Text", "Kurze Clips", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Einen Clip aus einem Satz zu holen", "Mehrere Varianten zu vergleichen"], True)
add("Manus", "https://manus.im/", "manus.im", "freemium", "proprietary", ["ki-chatbots", "programmierung"],
    "Manus übernimmt Aufgaben im Browser und arbeitet sie als Agent ab.",
    "Manus nimmt einen Auftrag und führt Schritte auf Webseiten und in Dateien aus. Es gibt einen Einstieg und bezahlte Nutzung.",
    ["Agent für Aufgaben", "Schritte im Browser", "Einstieg und bezahlte Nutzung"],
    ["Eine Recherche an einen Agenten zu geben", "Den Ablauf der Schritte zu sehen"], False)
add("Qwen", "https://qwen.ai/", "qwen.ai", "freemium", "proprietary", ["ki-chatbots"],
    "Qwen ist der Chat von Alibaba und beantwortet Fragen im Browser.",
    "Qwen führt ein Gespräch und kann Texte und Code bearbeiten. Es gibt einen kostenlosen Einstieg.",
    ["Chat im Browser", "Text und Code", "Kostenloser Einstieg"],
    ["Eine Frage im Chat zu stellen", "Einen Text umschreiben zu lassen"], True)
add("Z.ai", "https://z.ai/", "z.ai", "freemium", "proprietary", ["ki-chatbots"],
    "Z.ai führt einen Chat mit den GLM-Modellen von Zhipu.",
    "Z.ai nimmt Fragen entgegen und antwortet im Browser. Es gibt einen kostenlosen Einstieg.",
    ["Chat mit GLM-Modellen", "Browser", "Kostenloser Einstieg"],
    ["Eine Frage zu stellen", "Einen Entwurf gegenzulesen"], True)
add("Pi", "https://www.inflection.ai/", "inflection.ai", "freemium", "proprietary", ["ki-chatbots"],
    "Inflection stellt den Gesprächsassistenten Pi vor.",
    "Die Seite führt zu Pi, einem Chat für Alltagsfragen. Es gibt einen kostenlosen Einstieg.",
    ["Gesprächsassistent", "Alltagsfragen", "Kostenloser Einstieg"],
    ["Eine Frage im Gespräch zu stellen", "Einen Gedanken laut zu sortieren"], True)
add("Replika", "https://www.replika.com/", "replika.com", "freemium", "proprietary", ["ki-chatbots"],
    "Replika führt ein fortlaufendes Gespräch und merkt sich Themen.",
    "Replika chattet im Alltag und bietet Übungen zur Stimmung. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Fortlaufender Chat", "Übungen zur Stimmung", "Kostenloser Einstieg und bezahltes Abo"],
    ["Ein Gespräch über den Tag zu führen", "Eine Übung in der App zu starten"], True)
add("Roam Research", "https://www.roamresearch.com/", "roamresearch.com", "freemium", "proprietary", ["produktivitaet"],
    "Roam verknüpft Notizen über Seiten und Rückverweise.",
    "Roam legt tägliche Notizen an und zeigt, wo ein Begriff noch vorkommt. Es gibt einen Einstieg und ein bezahltes Abo.",
    ["Verknüpfte Notizen", "Rückverweise", "Einstieg und bezahltes Abo"],
    ["Ein Wissensnetz aus Notizen zu bauen", "Zu sehen, wo ein Begriff noch steht"], False)
add("RemNote", "https://www.remnote.com/", "remnote.com", "freemium", "proprietary", ["bildung", "produktivitaet"],
    "RemNote verbindet Notizen mit Karteikarten und Wiederholung.",
    "RemNote macht aus einer Notiz Karten und legt den nächsten Wiederholungstermin fest. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Notizen und Karteikarten", "Wiederholung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Aus einer Vorlesungsnotiz Karten zu machen", "Einen Stapel über Wochen zu wiederholen"], True)
add("Wordtune", "https://www.wordtune.com/", "wordtune.com", "freemium", "proprietary", ["textgenerierung"],
    "Wordtune formuliert Sätze um und schlägt einen anderen Ton vor.",
    "Wordtune sitzt im Text und bietet kürzere, längere oder formellere Fassungen. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Sätze umformulieren", "Anderer Ton", "Kostenloser Einstieg und bezahltes Abo"],
    ["Einen Satz klarer zu machen", "Mehrere Töne zu vergleichen"], True)
add("Turnitin", "https://www.turnitin.com/", "turnitin.com", "paid", "proprietary", ["bildung"],
    "Turnitin prüft Texte auf übereinstimmende Stellen und auf KI-Muster.",
    "Turnitin vergleicht eine Arbeit mit Quellen und markiert Treffer. Die Nutzung läuft über Schulen und Hochschulen und ist kostenpflichtig.",
    ["Ähnlichkeit mit Quellen", "Hinweise auf KI-Muster", "Kostenpflichtig über Bildungseinrichtungen"],
    ["Eine Arbeit vor der Abgabe prüfen zu lassen", "Übereinstimmende Stellen zu sehen"], False)
add("Cosine", "https://www.cosine.sh/", "cosine.sh", "freemium", "proprietary", ["programmierung"],
    "Cosine lässt einen Coding-Agenten Aufgaben in einem Repository bearbeiten.",
    "Cosine nimmt einen Auftrag und arbeitet im Code. Es gibt einen Einstieg und bezahlte Nutzung.",
    ["Coding-Agent", "Aufgaben im Repository", "Einstieg und bezahlte Nutzung"],
    ["Eine Änderung an einen Agenten zu geben", "Den Verlauf im Code zu sehen"], False)


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
    out = ROOT / "data" / "verified-tools-batch16.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows))
