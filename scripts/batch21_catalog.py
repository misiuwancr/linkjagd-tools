#!/usr/bin/env python3
"""Einundzwanzigste Liste: Buchhaltung, Notizen und Fernwartung."""

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


add("Bexio", "https://www.bexio.com/", "bexio.com", "paid", "proprietary", ["finanzen"],
    "Bexio schreibt Rechnungen und führt die Buchhaltung im Browser.",
    "Bexio legt Angebote, Rechnungen und Belege an. Die Nutzung ist kostenpflichtig.",
    ["Rechnungen", "Belege", "Kostenpflichtige Nutzung"],
    ["Eine Rechnung zu schreiben", "Belege in der Buchhaltung abzulegen"], False)
add("Accountable", "https://www.accountable.de/", "accountable.de", "freemium", "proprietary", ["finanzen"],
    "Accountable erfasst Einnahmen und Ausgaben für Selbstständige.",
    "Accountable sortiert Belege und bereitet die Steuer vor. Es gibt einen Einstieg und ein bezahltes Abo.",
    ["Einnahmen und Ausgaben", "Belege", "Einstieg und bezahltes Abo"],
    ["Einen Beleg abzufotografieren", "Einnahmen für die Steuer zu sammeln"], True)
add("Amazing Marvin", "https://www.amazingmarvin.com/", "amazingmarvin.com", "paid", "proprietary", ["produktivitaet"],
    "Amazing Marvin plant Aufgaben und lässt die Methode selbst wählen.",
    "Amazing Marvin kombiniert Listen, Kalender und Strategien. Die Nutzung ist kostenpflichtig.",
    ["Aufgaben", "Wählbare Methoden", "Kostenpflichtige Nutzung"],
    ["Den Tag aus einer Aufgabenliste zu bauen", "Eine Methode wie Zeitblöcke einzuschalten"], False)
add("Any.do", "https://www.any.do/", "any.do", "freemium", "proprietary", ["produktivitaet"],
    "Any.do hält Aufgaben, Listen und Termine an einem Ort.",
    "Any.do legt Erinnerungen und geteilte Listen an. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Aufgaben und Listen", "Erinnerungen", "Kostenloser Einstieg und bezahltes Abo"],
    ["Eine Einkaufsliste zu teilen", "Eine Aufgabe mit Erinnerung anzulegen"], True)
add("Banana Buchhaltung", "https://www.banana.ch/", "banana.ch", "freemium", "proprietary", ["finanzen"],
    "Banana Buchhaltung führt Konten in einer Tabelle auf dem eigenen Rechner.",
    "Banana rechnet Soll und Haben in einer Datei. Es gibt einen Einstieg und eine kostenpflichtige Lizenz.",
    ["Buchhaltung in einer Tabelle", "Datei auf dem eigenen Rechner", "Einstieg und kostenpflichtige Lizenz"],
    ["Eine einfache Buchhaltung zu führen", "Einen Abschluss aus der Datei zu rechnen"], False)
add("Candis", "https://www.candis.io/", "candis.io", "paid", "proprietary", ["finanzen"],
    "Candis liest Eingangsrechnungen und schlägt die Buchung vor.",
    "Candis nimmt einen Beleg und übergibt ihn an die Buchhaltung. Die Nutzung ist kostenpflichtig.",
    ["Eingangsrechnungen", "Buchungsvorschlag", "Kostenpflichtige Nutzung"],
    ["Eine Rechnung automatisch auszulesen", "Einen Beleg freizugeben"], False)
add("CashCtrl", "https://www.cashctrl.com/", "cashctrl.com", "paid", "proprietary", ["finanzen"],
    "CashCtrl führt Buchhaltung, Rechnungen und Belege im Browser.",
    "CashCtrl legt Geschäftsfälle an und erstellt Auswertungen. Die Nutzung ist kostenpflichtig.",
    ["Buchhaltung im Browser", "Rechnungen", "Kostenpflichtige Nutzung"],
    ["Eine Rechnung zu stellen", "Einen Monatsabschluss zu sehen"], False)
add("Debitoor", "https://www.debitoor.com/", "debitoor.com", "freemium", "proprietary", ["finanzen"],
    "Debitoor schreibt Rechnungen und erfasst Belege für kleine Firmen.",
    "Debitoor legt Kunden und Rechnungen an. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Rechnungen", "Belege", "Einstieg und bezahlte Stufen"],
    ["Eine Rechnung an einen Kunden zu schicken", "Belege zu sammeln"], True)
add("HRworks", "https://www.hrworks.de/", "hrworks.de", "paid", "proprietary", ["personal"],
    "HRworks verwaltet Abwesenheiten, Arbeitszeiten und Personalakten.",
    "HRworks nimmt Urlaubsanträge entgegen und führt Zeiten. Die Nutzung ist kostenpflichtig.",
    ["Abwesenheiten", "Arbeitszeiten", "Kostenpflichtige Nutzung"],
    ["Einen Urlaubsantrag zu stellen", "Zeiten im Monat zu sehen"], False)
add("Lexware", "https://www.lexware.de/", "lexware.de", "paid", "proprietary", ["finanzen"],
    "Lexware führt Buchhaltung, Lohn und Warenwirtschaft für kleine Firmen.",
    "Lexware bietet einzelne Programme für Rechnung, Lohn und Buchhaltung. Die Nutzung ist kostenpflichtig.",
    ["Buchhaltung und Lohn", "Rechnungen", "Kostenpflichtige Nutzung"],
    ["Eine Lohnabrechnung zu erstellen", "Eine Rechnung aus dem Programm zu schreiben"], False)
add("Missive", "https://www.missiveapp.com/", "missiveapp.com", "freemium", "proprietary", ["produktivitaet"],
    "Missive führt E-Mail und Chat eines Teams in einem Posteingang.",
    "Missive teilt Unterhaltungen und interne Kommentare. Es gibt einen kostenlosen Einstieg und bezahlte Plätze.",
    ["Gemeinsamer Posteingang", "Interne Kommentare", "Kostenloser Einstieg und bezahlte Plätze"],
    ["Eine Mail im Team zu beantworten", "Einen Kommentar neben der Mail zu lassen"], False)
add("NoMachine", "https://www.nomachine.com/", "nomachine.com", "freemium", "proprietary", ["programmierung"],
    "NoMachine zeigt den Bildschirm eines anderen Rechners und steuert ihn.",
    "NoMachine verbindet sich mit einem Rechner im Netz. Es gibt eine kostenlose Fassung und bezahlte Funktionen.",
    ["Fernsteuerung", "Bildschirm", "Kostenlose Fassung und bezahlte Funktionen"],
    ["Einen Rechner aus der Ferne zu bedienen", "Eine Datei über die Verbindung zu nutzen"], False)
add("Notesnook", "https://www.notesnook.com/", "notesnook.com", "freemium", "unknown", ["produktivitaet"],
    "Notesnook speichert Notizen verschlüsselt und gleicht sie zwischen Geräten ab.",
    "Notesnook legt Notizbücher an. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Verschlüsselte Notizen", "Abgleich zwischen Geräten", "Kostenloser Einstieg und bezahltes Abo"],
    ["Eine Notiz nur für sich abzulegen", "Dieselbe Notiz auf dem Handy zu öffnen"], True)
add("Shortwave", "https://www.shortwave.com/", "shortwave.com", "freemium", "proprietary", ["produktivitaet"],
    "Shortwave sortiert E-Mails und fasst Threads zusammen.",
    "Shortwave bündelt den Posteingang und schlägt Antworten vor. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Sortierter Posteingang", "Zusammengefasste Threads", "Kostenloser Einstieg und bezahltes Abo"],
    ["Einen langen Thread auf den Punkt zu bringen", "Den Posteingang nach Themen zu bündeln"], True)
add("Simplenote", "https://simplenote.com/", "simplenote.com", "free", "proprietary", ["produktivitaet"],
    "Simplenote hält schlichte Notizen und gleicht sie zwischen Geräten ab.",
    "Simplenote speichert Text und eine Verlaufsliste. Die Nutzung ist ohne Abo möglich.",
    ["Schlichte Notizen", "Verlauf", "Nutzung ohne Abo"],
    ["Eine Notiz schnell festzuhalten", "Dieselbe Notiz auf einem zweiten Gerät zu öffnen"], True)
add("SkedPal", "https://www.skedpal.com/", "skedpal.com", "paid", "proprietary", ["produktivitaet"],
    "SkedPal legt Aufgaben automatisch in freie Zeiten des Kalenders.",
    "SkedPal nimmt Fristen und Prioritäten und plant den Tag. Die Nutzung ist kostenpflichtig.",
    ["Aufgaben im Kalender", "Fristen", "Kostenpflichtige Nutzung"],
    ["Den Tag aus einer Aufgabenliste planen zu lassen", "Eine Aufgabe um einen Termin herum zu legen"], False)
add("Splashtop", "https://www.splashtop.com/", "splashtop.com", "paid", "proprietary", ["programmierung"],
    "Splashtop steuert einen anderen Rechner über das Netz.",
    "Splashtop zeigt den entfernten Bildschirm und nimmt Eingaben entgegen. Die Nutzung ist kostenpflichtig.",
    ["Fernsteuerung", "Entfernter Bildschirm", "Kostenpflichtige Nutzung"],
    ["Einen Bürorechner von unterwegs zu bedienen", "Jemandem am Bildschirm zu helfen"], False)
add("Taxdoo", "https://www.taxdoo.com/", "taxdoo.com", "paid", "proprietary", ["finanzen", "e-commerce"],
    "Taxdoo rechnet Umsatzsteuer für Verkäufe über mehrere Länder.",
    "Taxdoo liest Shop-Daten und bereitet Meldungen vor. Die Nutzung ist kostenpflichtig.",
    ["Umsatzsteuer über Länder", "Shop-Daten", "Kostenpflichtige Nutzung"],
    ["Verkäufe aus einem Shop für die Steuer zu sammeln", "Eine Meldung vorzubereiten"], False)
add("Things 3", "https://www.things.app/", "things.app", "paid", "proprietary", ["produktivitaet"],
    "Things sortiert Aufgaben nach Bereichen, Projekten und dem heutigen Tag.",
    "Things hält eine Heute-Liste und Fristen. Die Apps sind kostenpflichtig.",
    ["Heute-Liste", "Projekte", "Kostenpflichtige Apps"],
    ["Nur das für heute auszuwählen", "Ein Projekt in nächste Schritte zu teilen"], True)
add("DWService", "https://www.dwservice.net/", "dwservice.net", "free", "unknown", ["programmierung"],
    "DWService gibt einen Rechner für eine Sitzung zur Fernsteuerung frei.",
    "DWService erzeugt einen Zugangscode und öffnet den Bildschirm. Eine OSI-Kennung wird hier nicht eingetragen. Die Nutzung ist ohne Abo beschrieben.",
    ["Fernsteuerung per Code", "Sitzung", "Nutzung ohne Abo"],
    ["Jemandem kurz den eigenen Rechner zu zeigen", "Einen Rechner ohne Installation beim Gegenüber zu erreichen"], True)
add("Exact", "https://www.exact.com/", "exact.com", "paid", "proprietary", ["finanzen"],
    "Exact führt Buchhaltung, Projekte und Warenwirtschaft für Firmen.",
    "Exact bündelt Belege, Rechnungen und Auswertungen. Die Nutzung ist kostenpflichtig.",
    ["Buchhaltung", "Projekte", "Kostenpflichtige Nutzung"],
    ["Eine Rechnung in der Buchhaltung zu sehen", "Ein Projekt mit Kosten zu führen"], False)
add("Klippa", "https://www.klippa.com/", "klippa.com", "freemium", "proprietary", ["finanzen"],
    "Klippa liest Belege und zieht die Felder in eine strukturierte Form.",
    "Klippa nimmt ein Foto oder eine PDF und liefert Betrag und Datum. Es gibt einen Einstieg und bezahlte Mengen.",
    ["Belege auslesen", "Felder wie Betrag und Datum", "Einstieg und bezahlte Mengen"],
    ["Eine Rechnung automatisch zu erfassen", "Felder in die Buchhaltung zu geben"], False)
add("PlentyONE", "https://www.plentyone.com/", "plentyone.com", "paid", "proprietary", ["e-commerce"],
    "PlentyONE steuert Bestellungen und Artikel über mehrere Verkaufskanäle.",
    "PlentyONE bündelt Lager und Marktplatz-Bestellungen. Die Nutzung ist kostenpflichtig.",
    ["Bestellungen", "Mehrere Kanäle", "Kostenpflichtige Nutzung"],
    ["Artikel an mehrere Kanäle zu geben", "Bestellungen an einem Ort zu sehen"], False)
add("ScreenConnect", "https://www.screenconnect.com/", "screenconnect.com", "paid", "proprietary", ["kundenservice"],
    "ScreenConnect öffnet eine Fernwartungssitzung auf einem anderen Rechner.",
    "ScreenConnect verbindet Support und Bildschirm. Die Nutzung ist kostenpflichtig.",
    ["Fernwartung", "Support-Sitzung", "Kostenpflichtige Nutzung"],
    ["Einen Bildschirm im Support zu sehen", "Eine Sitzung mit einem Kunden zu starten"], False)
add("OpenTalk", "https://www.opentalk.eu/", "opentalk.eu", "freemium", "unknown", ["produktivitaet"],
    "OpenTalk führt Videokonferenzen, auch auf eigener Infrastruktur.",
    "OpenTalk stellt Räume für Gespräche bereit. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt betriebene Angebote und eine selbst zu betreibende Fassung.",
    ["Videokonferenzen", "Eigene Infrastruktur", "Betriebene und selbst betriebene Fassung"],
    ["Ein Gespräch ohne einen US-Dienst zu führen", "Einen Raum für ein Team zu öffnen"], False)
add("Canary Mail", "https://www.canarymail.io/", "canarymail.io", "freemium", "proprietary", ["produktivitaet"],
    "Canary Mail verschlüsselt E-Mails und fasst den Posteingang zusammen.",
    "Canary Mail liest bei den großen Anbietern mit und bietet Verschlüsselung. Es gibt einen Einstieg und ein bezahltes Abo.",
    ["Verschlüsselte Mails", "Zusammengefasster Posteingang", "Einstieg und bezahltes Abo"],
    ["Eine Mail verschlüsselt zu senden", "Den Posteingang kürzer zu sehen"], False)
add("Skype", "https://www.skype.com/", "skype.com", "freemium", "proprietary", ["produktivitaet"],
    "Skype führt Videoanrufe und Chats zwischen Kontakten.",
    "Skype startet einen Anruf oder eine Nachricht. Es gibt einen kostenlosen Einstieg und bezahlte Guthaben für einige Nummern.",
    ["Videoanrufe", "Chat", "Kostenloser Einstieg"],
    ["Jemanden per Video anzurufen", "Eine Nachricht zu schicken"], True)
add("TightVNC", "https://www.tightvnc.com/", "tightvnc.com", "free", "open_source", ["programmierung"],
    "TightVNC zeigt einen Windows-Bildschirm im Netz und steht unter der GPL.",
    "TightVNC besteht aus Server und Betrachter. Die Software ist quelloffen unter der GPL und ohne Lizenzgebühr nutzbar.",
    ["Fernsteuerung unter Windows", "Server und Betrachter", "GPL, ohne Lizenzgebühr"],
    ["Einen Windows-Rechner im eigenen Netz zu sehen", "Eine Sitzung ohne Abo zu öffnen"], False)
add("SteuerGo", "https://www.steuergo.de/", "steuergo.de", "freemium", "proprietary", ["finanzen"],
    "SteuerGo führt durch die Einkommensteuererklärung im Browser.",
    "SteuerGo stellt Fragen und füllt die Felder. Es gibt einen Einstieg und eine kostenpflichtige Abgabe.",
    ["Einkommensteuer im Browser", "Geführte Fragen", "Einstieg und kostenpflichtige Abgabe"],
    ["Eine Steuererklärung Schritt für Schritt auszufüllen", "Die Daten vor der Abgabe zu prüfen"], True)


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
    out = ROOT / "data" / "verified-tools-batch21.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows))
