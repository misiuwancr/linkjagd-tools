#!/usr/bin/env python3
"""Zwölfte geprüfte Liste."""

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


add("Docusaurus", "https://docusaurus.io/", "docusaurus.io", "free", "unknown", ["programmierung"],
    "Docusaurus baut Dokumentationsseiten aus Markdown.",
    "Docusaurus erzeugt eine Website mit Navigation, Suche und Versionen. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Dokumentation aus Markdown", "Navigation und Versionen", "Nutzung ohne Pflichtabo"],
    ["Eine Dokumentation zu veröffentlichen", "Mehrere Versionen einer Anleitung zu halten"], False)
add("Quarto", "https://quarto.org/", "quarto.org", "free", "unknown", ["daten", "programmierung"],
    "Quarto setzt Texte, Code und Grafiken zu einem Bericht oder einer Website zusammen.",
    "Quarto rendert Markdown mit eingebettetem Code. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Berichte aus Text und Code", "Websites und PDFs", "Nutzung ohne Pflichtabo"],
    ["Einen Bericht mit Grafiken zu schreiben", "Eine Projektdokumentation zu erzeugen"], False)
add("OpenTopoMap", "https://opentopomap.org/", "opentopomap.org", "free", "unknown", ["reisen"],
    "OpenTopoMap zeigt eine topografische Karte aus offenen Daten.",
    "Die Karte stellt Höhenlinien und Wege dar. Das Ansehen ist ohne Konto möglich. Eine OSI-Kennung der Darstellung wird hier nicht eingetragen.",
    ["Höhenlinien und Wege", "Offene Kartendaten", "Ansehen ohne Konto"],
    ["Eine Wanderung im Gelände zu prüfen", "Höhenlinien einer Region zu sehen"], True)
add("Overpass Turbo", "https://overpass-turbo.eu/", "overpass-turbo.eu", "free", "unknown", ["daten", "reisen"],
    "Overpass Turbo fragt Daten aus OpenStreetMap mit einer Abfrage ab.",
    "Die Seite zeigt das Ergebnis einer Abfrage auf der Karte. Die Nutzung ist ohne Konto möglich. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Abfragen an OpenStreetMap", "Ergebnis auf der Karte", "Nutzung ohne Konto"],
    ["Alle Cafés in einem Ausschnitt zu finden", "Eine Abfrage zu testen"], False)
add("OpenStreetMap Deutschland", "https://www.openstreetmap.de/", "openstreetmap.de", "free", "unknown", ["reisen", "recherche"],
    "OpenStreetMap Deutschland informiert die deutschsprachige Gemeinschaft der Karte.",
    "Die Seite erklärt, wie man mitmacht, und verweist auf die Karte. Die Texte sind ohne Konto lesbar.",
    ["Deutschsprachige Gemeinschaft", "Hinweise zum Mitmachen", "Lesen ohne Konto"],
    ["Zu erfahren, wie die Karte entsteht", "Einen Einstieg in die Mitarbeit zu finden"], True)
add("Natural Earth", "https://www.naturalearthdata.com/", "naturalearthdata.com", "free", "unknown", ["daten"],
    "Natural Earth stellt Kartengrundlagen in mehreren Maßstäben bereit.",
    "Die Daten eignen sich für Übersichtskarten. Der Download ist ohne Konto möglich. Eine einzelne OSI-Kennung wird hier nicht eingetragen.",
    ["Kartengrundlagen", "Mehrere Maßstäbe", "Download ohne Konto"],
    ["Eine Weltkarte für eine Grafik zu laden", "Länderumrisse zu beziehen"], False)
add("geojson.io", "https://geojson.io/", "geojson.io", "free", "unknown", ["daten", "programmierung"],
    "geojson.io zeichnet Punkte und Flächen und zeigt das GeoJSON dazu.",
    "Die Seite lässt Formen auf einer Karte setzen und kopiert den Text. Die Nutzung ist ohne Konto möglich. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Zeichnen auf der Karte", "GeoJSON als Text", "Nutzung ohne Konto"],
    ["Einen Bereich als GeoJSON zu zeichnen", "Eine Fläche für eine Anwendung zu umreißen"], True)
add("Kepler.gl", "https://kepler.gl/", "kepler.gl", "free", "unknown", ["daten"],
    "Kepler.gl zeigt große Mengen von Punkten und Wegen auf einer Karte.",
    "Kepler.gl nimmt eine Tabelle und zeichnet sie. Die Nutzung im Browser ist ohne Konto möglich. Eine OSI-Kennung wird hier nicht erneut eingetragen.",
    ["Punkte und Wege auf der Karte", "Tabelle als Eingabe", "Nutzung ohne Konto"],
    ["Viele Standorte auf einmal zu sehen", "Eine Tabelle geografisch zu prüfen"], False)
add("Cesium", "https://cesium.com/", "cesium.com", "freemium", "unknown", ["dreid", "programmierung"],
    "Cesium zeichnet einen Globus im Browser, auch mit 3D-Gelände.",
    "Cesium stellt eine Bibliothek und gehostete Kacheln bereit. Eine OSI-Kennung wird hier nicht erneut eingetragen. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Globus im Browser", "3D-Gelände", "Einstieg und bezahlte Kontingente"],
    ["Eine 3D-Karte in eine Website einzubauen", "Gelände eines Orts zu zeigen"], False)
add("Felt", "https://felt.com/", "felt.com", "freemium", "proprietary", ["reisen", "daten"],
    "Felt zeichnet Karten im Browser, die ein Team gemeinsam bearbeitet.",
    "Felt legt Markierungen und Flächen auf eine Karte. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Gemeinsame Karten", "Markierungen und Flächen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Karte mit einem Team zu zeichnen", "Orte für ein Projekt zu markieren"], True)
add("intervals.icu", "https://www.intervals.icu/", "intervals.icu", "freemium", "proprietary", ["gesundheit"],
    "intervals.icu wertet Trainings aus, die von der Uhr oder vom Radcomputer kommen.",
    "Die Seite zeigt Belastung, Fitness und einzelne Einheiten. Es gibt einen kostenlosen Einstieg und eine bezahlte Stufe.",
    ["Belastung und Fitness", "Einheiten aus Uhr und Radcomputer", "Kostenloser Einstieg und bezahlte Stufe"],
    ["Eine Trainingswoche auszuwerten", "Die Belastung über Wochen zu sehen"], False)
add("TrainingPeaks", "https://www.trainingpeaks.com/", "trainingpeaks.com", "freemium", "proprietary", ["gesundheit"],
    "TrainingPeaks plant und auswertet Ausdauertraining.",
    "TrainingPeaks legt Pläne an und zeigt die Belastung der Einheiten. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Trainingspläne", "Belastung der Einheiten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Trainingsplan zu führen", "Eine Einheit auszuwerten"], False)
add("TrainerRoad", "https://www.trainerroad.com/", "trainerroad.com", "paid", "proprietary", ["gesundheit"],
    "TrainerRoad steuert Einheiten auf der Rolle fürs Rad.",
    "TrainerRoad gibt Intervalle vor und passt sie an. Die Nutzung ist kostenpflichtig.",
    ["Intervalle auf der Rolle", "Anpassung der Einheiten", "Kostenpflichtige Nutzung"],
    ["Eine Einheit auf der Rolle zu fahren", "Einen Plan für mehrere Wochen zu folgen"], False)
add("BuzzSumo", "https://buzzsumo.com/", "buzzsumo.com", "freemium", "proprietary", ["seo", "marketing"],
    "BuzzSumo zeigt, welche Inhalte zu einem Thema geteilt werden.",
    "BuzzSumo sucht Artikel und deren Verbreitung. Es gibt einen Einstieg und bezahlte Abfragen.",
    ["Geteilte Inhalte", "Suche nach Thema", "Einstieg und bezahlte Abfragen"],
    ["Zu sehen, welcher Text zu einem Thema läuft", "Themen für einen Artikel zu finden"], False)
add("Mention", "https://mention.com/", "mention.com", "freemium", "proprietary", ["marketing", "seo"],
    "Mention benachrichtigt, wenn ein Name im Web oder in sozialen Netzen auftaucht.",
    "Mention legt eine Beobachtung an und sammelt Treffer. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Beobachtung eines Namens", "Treffer aus Web und Netzen", "Einstieg und bezahlte Stufen"],
    ["Erwähnungen einer Marke zu sehen", "Einen Namen zu beobachten"], False)
add("Brand24", "https://www.brand24.com/", "brand24.com", "paid", "proprietary", ["marketing"],
    "Brand24 sammelt Erwähnungen einer Marke und zeigt die Stimmung.",
    "Brand24 durchsucht Quellen und fasst die Treffer. Die Nutzung ist kostenpflichtig.",
    ["Erwähnungen einer Marke", "Stimmung der Treffer", "Kostenpflichtige Nutzung"],
    ["Zu sehen, was über eine Marke geschrieben wird", "Eine Häufung von Erwähnungen zu erkennen"], False)
add("Basic Thinking", "https://www.basicthinking.de/", "basicthinking.de", "free", "proprietary", ["recherche", "marketing"],
    "Basic Thinking schreibt über digitales Marketing und Netzkultur.",
    "Das Magazin veröffentlicht Artikel, die ohne Abo lesbar sind. Die Redaktion sitzt in Deutschland.",
    ["Digitales Marketing", "Artikel ohne Abo", "Redaktion in Deutschland"],
    ["Einen Text zu einem Werkzeug zu lesen", "Ein Marketingthema nachzuvollziehen"], True)
add("etailment", "https://www.etailment.de/", "etailment.de", "freemium", "proprietary", ["e-commerce", "recherche"],
    "etailment berichtet über den Onlinehandel in Deutschland.",
    "Ein Teil der Meldungen ist frei, weitere Berichte sind kostenpflichtig.",
    ["Onlinehandel", "Freie Meldungen", "Weitere Berichte kostenpflichtig"],
    ["Eine Meldung zum Handel zu lesen", "Einen Trend im Onlinehandel einzuordnen"], False)
add("Onlinehändler-News", "https://www.onlinehaendler-news.de/", "onlinehaendler-news.de", "free", "proprietary", ["e-commerce", "recherche"],
    "Onlinehändler-News berichtet über Shop-Systeme, Marktplätze und Recht für Händler.",
    "Die Meldungen sind ohne Abo lesbar. Das Angebot richtet sich an den deutschen Handel.",
    ["Shop-Systeme und Marktplätze", "Recht für Händler", "Lesen ohne Abo"],
    ["Eine Änderung an einem Marktplatz nachzulesen", "Eine Meldung zum Handel zu finden"], True)
add("Shopbetreiber-Blog", "https://www.shopbetreiber-blog.de/", "shopbetreiber-blog.de", "free", "proprietary", ["e-commerce", "recht"],
    "Der Shopbetreiber-Blog schreibt über Recht und Alltag im Onlinehandel.",
    "Die Artikel sind ohne Abo lesbar und richten sich an Shopbetreiber in Deutschland.",
    ["Recht im Onlinehandel", "Artikel ohne Abo", "Zielgruppe Shopbetreiber"],
    ["Eine Rechtsfrage für einen Shop nachzulesen", "Eine Änderung bei Marktplätzen zu verfolgen"], True)
add("iBusiness", "https://www.ibusiness.de/", "ibusiness.de", "freemium", "proprietary", ["e-commerce", "recherche"],
    "iBusiness berichtet über digitalen Handel und Marketing.",
    "Ein Teil der Texte ist frei, das Abo ist kostenpflichtig.",
    ["Digitaler Handel", "Freier Anteil", "Kostenpflichtiges Abo"],
    ["Eine Analyse zum Handel zu lesen", "Ein Marketingthema einzuordnen"], False)
add("news aktuell", "https://www.newsaktuell.de/", "newsaktuell.de", "freemium", "proprietary", ["marketing", "recherche"],
    "news aktuell verbreitet Pressemitteilungen an Redaktionen.",
    "Unternehmen stellen Mitteilungen ein, Redaktionen lesen sie. Das Einstellen ist kostenpflichtig, ein Teil der öffentlichen Meldungen ist ohne Konto lesbar.",
    ["Verbreitung von Pressemitteilungen", "Öffentliche Meldungen", "Einstellen kostenpflichtig"],
    ["Eine Pressemitteilung zu verbreiten", "Eine öffentliche Meldung zu lesen"], False)
add("APA-OTS", "https://www.ots.at/", "ots.at", "free", "proprietary", ["recherche"],
    "APA-OTS veröffentlicht Pressemitteilungen aus Österreich.",
    "Die Originaltext-Service-Seite zeigt Mitteilungen, die ohne Konto lesbar sind.",
    ["Pressemitteilungen aus Österreich", "Originaltexte", "Lesen ohne Konto"],
    ["Eine Mitteilung aus Österreich zu finden", "Meldungen eines Absenders zu lesen"], True)
add("Der Standard", "https://www.derstandard.at/", "derstandard.at", "freemium", "proprietary", ["recherche"],
    "Der Standard berichtet über Politik, Wirtschaft und Kultur in Österreich.",
    "Ein Teil der Artikel ist frei, PUR ist kostenpflichtig. Die Redaktion sitzt in Wien.",
    ["Nachrichten aus Österreich", "Freier Anteil und kostenpflichtiges PUR", "Redaktion in Wien"],
    ["Eine Meldung aus Österreich zu lesen", "Einen Hintergrundartikel zu finden"], True)
add("Republik", "https://www.republik.ch/", "republik.ch", "freemium", "proprietary", ["recherche"],
    "Die Republik veröffentlicht Recherchen aus der Schweiz für Genossenschafterinnen.",
    "Ein Teil der Texte ist offen, das volle Angebot ist an die Mitgliedschaft gebunden. Die Redaktion sitzt in Zürich.",
    ["Recherchen aus der Schweiz", "Offener Anteil", "Mitgliedschaft für das volle Angebot"],
    ["Eine Recherche zu lesen", "Das Modell der Genossenschaft einzuordnen"], True)
add("Blätter", "https://www.blaetter.de/", "blaetter.de", "freemium", "proprietary", ["recherche"],
    "Die Blätter für deutsche und internationale Politik veröffentlichen Essays.",
    "Ein Teil der Texte ist frei, das Heft ist kostenpflichtig.",
    ["Politische Essays", "Freier Anteil", "Kostenpflichtiges Heft"],
    ["Einen Essay zu lesen", "Ein Heftthema zu finden"], True)
add("IPG-Journal", "https://www.ipg-journal.de/", "ipg-journal.de", "free", "proprietary", ["recherche"],
    "Das IPG-Journal veröffentlicht Texte zu internationaler Politik.",
    "Die Beiträge sind ohne Abo lesbar. Das Journal gehört zur Friedrich-Ebert-Stiftung.",
    ["Internationale Politik", "Beiträge ohne Abo", "Angebot der Friedrich-Ebert-Stiftung"],
    ["Einen Text zur internationalen Politik zu lesen", "Ein Land oder ein Thema zu suchen"], True)
add("Internationale Politik", "https://www.internationalepolitik.de/", "internationalepolitik.de", "freemium", "proprietary", ["recherche"],
    "Internationale Politik ist die Zeitschrift der Deutschen Gesellschaft für Auswärtige Politik.",
    "Ein Teil der Texte ist frei, das Abo ist kostenpflichtig.",
    ["Außenpolitik", "Freier Anteil", "Kostenpflichtiges Abo"],
    ["Einen Text zur Außenpolitik zu lesen", "Ein Thema der Zeitschrift zu finden"], False)
add("Perlentaucher", "https://www.perlentaucher.de/", "perlentaucher.de", "freemium", "proprietary", ["recherche", "bildung"],
    "Perlentaucher fasst Feuilleton und Buchkritik deutschsprachiger Zeitungen zusammen.",
    "Die Übersichten sind ohne Abo lesbar, ein Magazinanteil ist bezahlt.",
    ["Zusammenfassungen von Feuilleton", "Buchkritik", "Freie Übersichten und bezahlter Anteil"],
    ["Zu sehen, welche Bücher besprochen werden", "Eine Debatte über Zeitungen hinweg zu verfolgen"], True)
add("MapTiler", "https://www.maptiler.com/", "maptiler.com", "freemium", "proprietary", ["programmierung", "reisen"],
    "MapTiler stellt Kartenkacheln und Stile für eigene Anwendungen bereit.",
    "MapTiler liefert Karten über eine Schnittstelle. Es gibt einen kostenlosen Einstieg und bezahlte Abrufe.",
    ["Kartenkacheln und Stile", "Schnittstelle", "Kostenloser Einstieg und bezahlte Abrufe"],
    ["Eine Karte in eine Anwendung einzubauen", "Einen eigenen Kartenstil zu nutzen"], False)
add("Thunderforest", "https://www.thunderforest.com/", "thunderforest.com", "freemium", "proprietary", ["reisen", "programmierung"],
    "Thunderforest zeichnet Kartenstile auf Basis von OpenStreetMap.",
    "Thunderforest bietet Stile für Wandern, Rad und den Stadtplan. Es gibt einen kostenlosen Einstieg und bezahlte Abrufe.",
    ["Kartenstile", "Wandern, Rad und Stadt", "Kostenloser Einstieg und bezahlte Abrufe"],
    ["Eine Wanderkarte in eine App einzubauen", "Einen Stil fürs Rad zu wählen"], False)
add("GPSBabel", "https://www.gpsbabel.org/", "gpsbabel.org", "free", "unknown", ["reisen"],
    "GPSBabel wandelt Routen und Tracks zwischen Formaten.",
    "GPSBabel liest Dateien von Geräten und schreibt sie in ein anderes Format. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Umwandlung von Tracks und Routen", "Viele Formate", "Nutzung ohne Pflichtabo"],
    ["Eine Route für ein anderes Gerät zu wandeln", "Einen Track in ein gängiges Format zu bringen"], False)
add("Flix", "https://www.flix.com/", "flix.com", "free", "proprietary", ["reisen"],
    "Flix bündelt Fernbus und Zug unter einer Marke.",
    "Die Seite zeigt Verbindungen und Preise. Die Suche ist ohne Konto möglich, die Fahrt ist kostenpflichtig.",
    ["Fernbus und Zug", "Preise und Verbindungen", "Suche ohne Konto"],
    ["Eine Fernverbindung zu suchen", "Einen Preis zu vergleichen"], True)
add("CalTopo", "https://caltopo.com/", "caltopo.com", "freemium", "proprietary", ["reisen"],
    "CalTopo zeichnet Routen auf topografischen Karten.",
    "CalTopo legt Wege und Markierungen auf Geländekarten. Es gibt einen kostenlosen Einstieg und bezahlte Karten.",
    ["Routen auf Geländekarten", "Markierungen", "Kostenloser Einstieg und bezahlte Karten"],
    ["Eine Tour im Gelände zu planen", "Eine Karte für unterwegs vorzubereiten"], False)
add("TrainingPeaks bleibt", "https://www.trainingpeaks.com/", "trainingpeaks.com", "freemium", "proprietary", ["gesundheit"],
    "Platzhalter.", "Platzhalter.", ["x"], ["x"])


def validate(entries):
    entries[:] = [e for e in entries if "bleibt" not in e["name"]]
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
    out = ROOT / "data" / "verified-tools-batch12.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows), "->", out)
