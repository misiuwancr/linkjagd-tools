#!/usr/bin/env python3
"""Achtzehnte Liste: weitere geprüfte Web-Apps."""

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


add("Gong", "https://www.gong.io/", "gong.io", "paid", "proprietary", ["audio-und-sprache", "marketing"],
    "Gong zeichnet Vertriebsgespräche auf und zeigt, was darin vorkam.",
    "Gong schreibt Calls mit und filtert nach Themen. Die Nutzung ist kostenpflichtig.",
    ["Aufzeichnung von Vertriebsgesprächen", "Themenfilter", "Kostenpflichtige Nutzung"],
    ["Ein Verkaufsgespräch später zu durchsuchen", "Zu sehen, welche Themen oft vorkommen"], False)
add("Avoma", "https://www.avoma.com/", "avoma.com", "freemium", "proprietary", ["audio-und-sprache"],
    "Avoma schreibt Meetings mit und zieht daraus Notizen und Coaching.",
    "Avoma liefert Transkript und Zusammenfassung. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Meeting-Notizen", "Transkript", "Einstieg und bezahlte Stufen"],
    ["Ein Gespräch zusammenzufassen", "Stellen im Transkript zu finden"], False)
add("Bluedot", "https://www.bluedot.org/", "bluedot.org", "freemium", "proprietary", ["audio-und-sprache"],
    "Bluedot schreibt Google-Meetings mit und legt die Notizen ab.",
    "Bluedot nimmt am Meet teil und liefert eine Zusammenfassung. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Notizen zu Google Meet", "Zusammenfassung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Meet automatisch mitzuschreiben", "Die Notizen zu teilen"], True)
add("Supernormal", "https://www.supernormal.com/", "supernormal.com", "freemium", "proprietary", ["audio-und-sprache"],
    "Supernormal schreibt Meetings mit und macht daraus Notizen.",
    "Supernormal liefert Transkript und eine kurze Fassung. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Meeting-Notizen", "Kurze Fassung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Meeting nachzulesen", "Die kurze Fassung zu verschicken"], True)
add("Demodesk", "https://www.demodesk.com/", "demodesk.com", "freemium", "proprietary", ["audio-und-sprache", "marketing"],
    "Demodesk führt Verkaufsdemos und schreibt das Gespräch mit.",
    "Demodesk kombiniert einen Demo-Raum mit Notizen. Es gibt einen Einstieg und bezahlte Plätze.",
    ["Demo-Raum", "Notizen zum Gespräch", "Einstieg und bezahlte Plätze"],
    ["Eine Produktdemo zu halten", "Das Gespräch danach nachzulesen"], False)
add("Chorus", "https://www.chorus.ai/", "chorus.ai", "paid", "proprietary", ["audio-und-sprache", "marketing"],
    "Chorus zeichnet Vertriebsgespräche auf und macht sie durchsuchbar.",
    "Chorus schreibt Calls mit und zeigt Themen. Die Nutzung ist kostenpflichtig.",
    ["Durchsuchbare Calls", "Themen", "Kostenpflichtige Nutzung"],
    ["Ein Gespräch nach einem Stichwort zu finden", "Themen über viele Calls zu sehen"], False)
add("Clari", "https://www.clari.com/", "clari.com", "paid", "proprietary", ["marketing"],
    "Clari bündelt die Vertriebs-Pipeline und prognostiziert Abschlüsse.",
    "Clari liest Aktivitäten aus dem CRM und zeigt eine Prognose. Die Nutzung ist kostenpflichtig.",
    ["Pipeline", "Prognose", "Kostenpflichtige Nutzung"],
    ["Den Stand der Abschlüsse zu sehen", "Eine Prognose aus dem CRM zu holen"], False)
add("Around", "https://www.around.co/", "around.co", "freemium", "proprietary", ["produktivitaet"],
    "Around führt kleine Videogespräche mit wenig Bildfläche.",
    "Around setzt die Kamera als kleinen Kreis über die Arbeit. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Kleine Videogespräche", "Kamera als Kreis", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Kurz über eine Datei zu sprechen", "Den Bildschirm dabei sichtbar zu lassen"], True)
add("mmhmm", "https://www.mmhmm.app/", "mmhmm.app", "freemium", "proprietary", ["videogenerierung"],
    "mmhmm legt Folien und die eigene Kamera in eine Präsentation.",
    "mmhmm mischt Person und Inhalt in einer Aufnahme. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Folien und Kamera", "Aufnahme", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Präsentation mit Gesicht aufzunehmen", "Folien hinter der Person zu legen"], True)
add("Iris.ai", "https://www.iris.ai/", "iris.ai", "freemium", "proprietary", ["recherche"],
    "Iris.ai sucht wissenschaftliche Texte zu einer beschriebenen Frage.",
    "Iris.ai nimmt eine Forschungsfrage und zeigt passende Arbeiten. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Suche nach Forschungsfragen", "Passende Arbeiten", "Einstieg und bezahlte Stufen"],
    ["Literatur zu einer Frage zu finden", "Einen Überblick über ein Feld zu holen"], False)
add("Qualtrics", "https://www.qualtrics.com/", "qualtrics.com", "paid", "proprietary", ["produktivitaet"],
    "Qualtrics baut Umfragen und wertet Erfahrungswerte aus.",
    "Qualtrics verteilt Fragebögen und zeigt die Auswertung. Die Nutzung ist kostenpflichtig.",
    ["Umfragen", "Auswertung", "Kostenpflichtige Nutzung"],
    ["Eine Kundenbefragung zu fahren", "Antworten in Berichten zu sehen"], False)
add("Foxit", "https://www.foxit.com/", "foxit.com", "freemium", "proprietary", ["produktivitaet"],
    "Foxit liest, kommentiert und signiert PDF-Dateien.",
    "Foxit öffnet PDFs und legt Anmerkungen darauf. Es gibt einen kostenlosen Reader und bezahlte Editor-Funktionen.",
    ["PDF lesen und kommentieren", "Signatur", "Kostenloser Reader und bezahlter Editor"],
    ["Eine PDF zu kommentieren", "Ein Dokument zu signieren"], True)
add("HelloSign", "https://www.hellosign.com/", "hellosign.com", "freemium", "proprietary", ["produktivitaet"],
    "HelloSign holt Unterschriften auf Dokumente, ohne sie auszudrucken.",
    "HelloSign schickt eine Datei zur Signatur und legt sie ab. Es gibt einen Einstieg und bezahlte Signaturen.",
    ["Elektronische Signatur", "Ablage", "Einstieg und bezahlte Signaturen"],
    ["Einen Vertrag unterschreiben zu lassen", "Die signierte Datei abzulegen"], True)
add("pdfFiller", "https://www.pdffiller.com/", "pdffiller.com", "freemium", "proprietary", ["produktivitaet"],
    "pdfFiller füllt PDF-Formulare im Browser aus.",
    "pdfFiller schreibt in Felder und speichert die Datei. Es gibt einen Einstieg und bezahlte Stufen.",
    ["PDF-Formulare ausfüllen", "Speichern im Browser", "Einstieg und bezahlte Stufen"],
    ["Ein Formular ohne Druck auszufüllen", "Die ausgefüllte Datei zu laden"], True)
add("Pigment", "https://www.pigment.com/", "pigment.com", "paid", "proprietary", ["produktivitaet"],
    "Pigment plant Zahlen in Modellen für Teams statt in einzelnen Tabellen.",
    "Pigment verbindet Datenquellen mit einem Planungsmodell. Die Nutzung ist kostenpflichtig.",
    ["Planungsmodelle", "Datenquellen", "Kostenpflichtige Nutzung"],
    ["Eine Planung über Teams zu rechnen", "Eine Quelle an ein Modell zu hängen"], False)
add("Kustomer", "https://www.kustomer.com/", "kustomer.com", "paid", "proprietary", ["kundenservice"],
    "Kustomer sammelt Kundenanfragen und die bisherige Historie an einem Ort.",
    "Kustomer zeigt Mails, Chats und Bestellungen zu einer Person. Die Nutzung ist kostenpflichtig.",
    ["Anfragen und Historie", "Mails und Chats", "Kostenpflichtige Nutzung"],
    ["Eine Anfrage mit der Bestellhistorie zu sehen", "Ein Gespräch im Team zu übergeben"], False)
add("Braze", "https://www.braze.com/", "braze.com", "paid", "proprietary", ["marketing"],
    "Braze sendet Nachrichten in App, Push und E-Mail nach dem Verhalten.",
    "Braze startet eine Nachricht nach einem Ereignis. Die Nutzung ist kostenpflichtig.",
    ["Nachrichten nach Verhalten", "App, Push, E-Mail", "Kostenpflichtige Nutzung"],
    ["Eine Push-Nachricht nach einem Ereignis zu senden", "Kanäle in einer Kampagne zu mischen"], False)
add("Pusher", "https://www.pusher.com/", "pusher.com", "freemium", "proprietary", ["programmierung"],
    "Pusher liefert Ereignisse in Echtzeit an Browser und Apps.",
    "Pusher schickt eine Nachricht an verbundene Clients. Es gibt einen kostenlosen Einstieg und bezahlte Mengen.",
    ["Ereignisse in Echtzeit", "Clients", "Kostenloser Einstieg und bezahlte Mengen"],
    ["Einen Live-Stand in eine Seite zu schicken", "Mehrere Browser gleichzeitig zu aktualisieren"], False)
add("MessageBird", "https://www.messagebird.com/", "messagebird.com", "freemium", "proprietary", ["kundenservice"],
    "MessageBird verschickt SMS, WhatsApp und Anrufe über eine Schnittstelle.",
    "MessageBird spricht Kanäle aus einer Plattform an. Es gibt einen Einstieg und bezahlte Nachrichten.",
    ["SMS, WhatsApp, Anrufe", "Eine Plattform", "Einstieg und bezahlte Nachrichten"],
    ["Eine SMS aus einer Anwendung zu senden", "Einen WhatsApp-Kanal anzubinden"], False)
add("Salesforce", "https://www.salesforce.com/", "salesforce.com", "paid", "proprietary", ["marketing"],
    "Salesforce führt Kunden, Leads und Vorgänge in einem CRM.",
    "Salesforce legt Datensätze an und zeigt Pipelines. Die Nutzung ist kostenpflichtig.",
    ["CRM", "Leads und Vorgänge", "Kostenpflichtige Nutzung"],
    ["Einen Lead mit seiner Historie zu sehen", "Eine Pipeline zu filtern"], False)
add("AuthoredUp", "https://www.authoredup.com/", "authoredup.com", "freemium", "proprietary", ["marketing"],
    "AuthoredUp schreibt und plant LinkedIn-Beiträge mit Vorschau.",
    "AuthoredUp zeigt, wie der Beitrag später aussieht, und legt den Zeitpunkt fest. Es gibt einen Einstieg und bezahlte Stufen.",
    ["LinkedIn-Vorschau", "Planung", "Einstieg und bezahlte Stufen"],
    ["Einen Beitrag vor dem Posten zu sehen", "Mehrere Posts zu planen"], False)
add("Awario", "https://www.awario.com/", "awario.com", "freemium", "proprietary", ["marketing"],
    "Awario sucht Erwähnungen einer Marke im Web und in sozialen Netzen.",
    "Awario legt eine Suche an und sammelt Treffer. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Erwähnungen einer Marke", "Suche", "Einstieg und bezahlte Stufen"],
    ["Zu sehen, wo eine Marke genannt wird", "Treffer über die Woche zu sammeln"], False)
add("Brandwatch", "https://www.brandwatch.com/", "brandwatch.com", "paid", "proprietary", ["marketing"],
    "Brandwatch wertet Erwähnungen und Stimmung in sozialen Netzen aus.",
    "Brandwatch sammelt Beiträge und zeigt Themen. Die Nutzung ist kostenpflichtig.",
    ["Erwähnungen", "Stimmung und Themen", "Kostenpflichtige Nutzung"],
    ["Die Stimmung zu einer Marke zu sehen", "Themen in Beiträgen zu finden"], False)
add("Meltwater", "https://www.meltwater.com/", "meltwater.com", "paid", "proprietary", ["marketing"],
    "Meltwater durchsucht Medien und soziale Netze nach Erwähnungen.",
    "Meltwater legt eine Beobachtung an und liefert Treffer. Die Nutzung ist kostenpflichtig.",
    ["Mediensuche", "Erwähnungen", "Kostenpflichtige Nutzung"],
    ["Artikel zu einem Thema zu finden", "Eine Marke in den Medien zu beobachten"], False)
add("Talkwalker", "https://www.talkwalker.com/", "talkwalker.com", "paid", "proprietary", ["marketing"],
    "Talkwalker beobachtet Marken in sozialen Netzen und im Web.",
    "Talkwalker sammelt Erwähnungen und zeigt Themen. Die Nutzung ist kostenpflichtig.",
    ["Markenbeobachtung", "Themen", "Kostenpflichtige Nutzung"],
    ["Erwähnungen einer Marke zu sammeln", "Ein Thema über die Zeit zu sehen"], False)
add("Sprout Social", "https://www.sproutsocial.com/", "sproutsocial.com", "paid", "proprietary", ["marketing"],
    "Sprout Social plant Beiträge und beantwortet Nachrichten mehrerer Netze.",
    "Sprout Social bündelt Posteingänge und einen Kalender. Die Nutzung ist kostenpflichtig.",
    ["Beitragskalender", "Gemeinsamer Posteingang", "Kostenpflichtige Nutzung"],
    ["Einen Beitrag für mehrere Netze zu planen", "Nachrichten an einem Ort zu beantworten"], False)
add("Planoly", "https://www.planoly.com/", "planoly.com", "freemium", "proprietary", ["marketing"],
    "Planoly plant das Raster von Instagram und Pinterest im Voraus.",
    "Planoly legt Bilder in eine Vorschau und postet sie später. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Raster-Vorschau", "Geplante Beiträge", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Instagram-Raster zu planen", "Einen Beitrag auf einen Tag zu legen"], True)
add("Hugo", "https://www.hugo.team/", "hugo.team", "freemium", "proprietary", ["produktivitaet"],
    "Hugo hält Meeting-Notizen an der Agenda und teilt sie danach.",
    "Hugo verbindet Kalender und Protokoll. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Notizen an der Agenda", "Teilen nach dem Meeting", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Während des Meetings mitzuschreiben", "Das Protokoll an die Runde zu schicken"], True)
add("Soda PDF", "https://www.sodapdf.com/", "sodapdf.com", "freemium", "proprietary", ["produktivitaet"],
    "Soda PDF bearbeitet, verbindet und signiert PDF-Dateien.",
    "Soda PDF öffnet eine Datei im Browser oder in der App. Es gibt einen Einstieg und bezahlte Stufen.",
    ["PDF bearbeiten", "Verbinden und signieren", "Einstieg und bezahlte Stufen"],
    ["Zwei PDFs zu verbinden", "Ein Formular auszufüllen"], True)
add("Vonage", "https://www.vonage.com/", "vonage.com", "paid", "proprietary", ["kundenservice"],
    "Vonage stellt Telefonie und Nachrichten über eine Schnittstelle bereit.",
    "Vonage verbindet Anrufe und SMS mit einer Anwendung. Die Nutzung ist kostenpflichtig.",
    ["Telefonie und SMS", "Schnittstelle", "Kostenpflichtige Nutzung"],
    ["Einen Anruf aus einer App zu starten", "Eine SMS zuzustellen"], False)


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
        raise SystemExit("\n".join(errors[:20]))
    return entries


if __name__ == "__main__":
    rows = validate(E)
    out = ROOT / "data" / "verified-tools-batch18.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows))
