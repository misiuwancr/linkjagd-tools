#!/usr/bin/env python3
"""Elfte geprüfte Liste, Schwerpunkt Präsentationen, SEO, Karten und deutsche Nachrichten."""

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


add("Slidesgo", "https://slidesgo.com/", "slidesgo.com", "freemium", "proprietary", ["praesentationen"],
    "Slidesgo stellt Vorlagen für Folien bereit, die sich in gängige Programme übernehmen lassen.",
    "Slidesgo zeigt Gestaltungen nach Thema. Ein Teil ist ohne Abo ladbar, weitere Vorlagen sind bezahlt.",
    ["Folienvorlagen nach Thema", "Übernahme in Präsentationsprogramme", "Kostenloser Anteil und bezahlte Vorlagen"],
    ["Eine Vorlage für einen Vortrag zu suchen", "Folien in ein Programm zu übernehmen"], True)
add("Slidebean", "https://slidebean.com/", "slidebean.com", "freemium", "proprietary", ["praesentationen"],
    "Slidebean baut aus Stichpunkten eine Folienfolge für Pitches.",
    "Slidebean setzt Inhalte in ein Layout und lässt das Design wechseln. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Folien aus Stichpunkten", "Wechselbares Layout", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Pitch aus Stichpunkten zu setzen", "Das Layout einer Folge zu wechseln"], True)
add("Genially", "https://genial.ly/", "genial.ly", "freemium", "proprietary", ["praesentationen", "bildung"],
    "Genially baut interaktive Folien, Bilder und kleine Lernspiele.",
    "Genially legt klickbare Elemente auf eine Fläche. Es gibt einen kostenlosen Einstieg und bezahlte Stufen. Der Dienst kommt aus Spanien.",
    ["Interaktive Folien", "Klickbare Elemente", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Folie mit Klicks zu bauen", "Ein Lernspiel aus einer Vorlage zu machen"], True)
add("Slido", "https://www.slido.com/", "slido.com", "freemium", "proprietary", ["praesentationen", "bildung"],
    "Slido sammelt Fragen und Abstimmungen während eines Vortrags.",
    "Slido zeigt eine Frage auf der Folie, das Publikum antwortet mit dem Handy. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Fragen und Abstimmungen", "Antworten per Handy", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Fragen aus dem Publikum zu sammeln", "Eine Abstimmung in einem Vortrag zu starten"], True)
add("SlidesAI", "https://www.slidesai.io/", "slidesai.io", "freemium", "proprietary", ["praesentationen"],
    "SlidesAI macht aus einem Text eine Folienfolge.",
    "SlidesAI nimmt einen Entwurf und setzt ihn auf Folien. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Folien aus einem Text", "Entwurf als Ausgang", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Aus einem Text eine erste Folge zu erzeugen", "Einen Entwurf auf Folien zu verteilen"], True)
add("Plus AI", "https://www.plusai.com/", "plusai.com", "freemium", "proprietary", ["praesentationen"],
    "Plus AI schreibt und überarbeitet Folien in einer Präsentation.",
    "Plus AI ergänzt Folien aus einer Anweisung und schreibt Texte um. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Neue Folien aus einer Anweisung", "Umschreiben vorhandener Folien", "Einstieg und bezahlte Stufen"],
    ["Eine Folie aus einem Satz zu erzeugen", "Einen Folientext umschreiben zu lassen"], False)
add("Presentations.AI", "https://www.presentations.ai/", "presentations.ai", "freemium", "proprietary", ["praesentationen"],
    "Presentations.AI erzeugt eine Folienfolge aus einem Thema.",
    "Die Seite nimmt ein Thema und setzt dazu Folien. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Folien aus einem Thema", "Fertige Folge", "Einstieg und bezahlte Stufen"],
    ["Zu einem Thema eine erste Folge zu bekommen", "Einen Vortrag zu skizzieren"], True)
add("Decktopus", "https://www.decktopus.com/", "decktopus.com", "freemium", "proprietary", ["praesentationen"],
    "Decktopus baut Präsentationen aus Fragen zu Ziel und Inhalt.",
    "Decktopus fragt nach dem Anlass und setzt daraus Folien. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Folien aus Fragen zum Anlass", "Vorgegebene Struktur", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Vortrag entlang von Fragen aufzubauen", "Eine Folge für ein Meeting zu starten"], True)
add("ChatSlide", "https://www.chatslide.ai/", "chatslide.ai", "freemium", "proprietary", ["praesentationen"],
    "ChatSlide macht aus einem Chat eine Folienfolge.",
    "ChatSlide nimmt eine Unterhaltung oder einen Text und setzt Folien. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Folien aus einem Chat", "Text als Ausgang", "Einstieg und bezahlte Stufen"],
    ["Aus einer Notiz eine Folge zu machen", "Einen Entwurf im Chat in Folien zu überführen"], False)
add("Mangools", "https://mangools.com/", "mangools.com", "freemium", "proprietary", ["seo"],
    "Mangools bündelt Keyword-Suche, Rankings und Linkdaten.",
    "Mangools zeigt Suchvolumen, Positionen und verweisende Seiten. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Keywords und Rankings", "Verweisende Seiten", "Einstieg und bezahlte Stufen"],
    ["Ein Keyword nach Volumen zu prüfen", "Die Position einer Seite zu sehen"], False)
add("SE Ranking", "https://seranking.com/", "seranking.com", "freemium", "proprietary", ["seo"],
    "SE Ranking verfolgt Positionen und prüft eine Website auf SEO-Fehler.",
    "SE Ranking misst Rankings über die Zeit und zeigt technische Hinweise. Es gibt einen Test und bezahlte Stufen.",
    ["Positionen über die Zeit", "Technische Hinweise", "Test und bezahlte Stufen"],
    ["Rankings einer Domain zu verfolgen", "Fehler einer Website zu sehen"], False)
add("AlsoAsked", "https://alsoasked.com/", "alsoasked.com", "freemium", "proprietary", ["seo", "recherche"],
    "AlsoAsked zeigt, welche Folgefragen Menschen zu einem Begriff stellen.",
    "AlsoAsked zeichnet einen Baum verwandter Fragen. Es gibt einen kostenlosen Einstieg und bezahlte Abfragen.",
    ["Folgefragen zu einem Begriff", "Baum verwandter Fragen", "Kostenloser Einstieg und bezahlte Abfragen"],
    ["Themen für einen Text zu sammeln", "Zu sehen, was neben einem Begriff gefragt wird"], True)
add("Majestic", "https://majestic.com/", "majestic.com", "freemium", "proprietary", ["seo"],
    "Majestic bewertet, welche Seiten auf eine Domain verweisen.",
    "Majestic zeigt Verweise und einen eigenen Index-Wert. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Verweisende Seiten", "Eigener Index-Wert", "Einstieg und bezahlte Stufen"],
    ["Die Verweise auf eine Domain zu sehen", "Zwei Domains nach Verweisen zu vergleichen"], False)
add("Similarweb", "https://www.similarweb.com/", "similarweb.com", "freemium", "proprietary", ["seo", "recherche"],
    "Similarweb schätzt Besuche und Quellen von Websites.",
    "Similarweb zeigt Reichweite, Herkunft und ähnliche Seiten. Ein Teil ist ohne Abo sichtbar, ausführliche Zahlen sind bezahlt.",
    ["Geschätzte Besuche und Quellen", "Ähnliche Seiten", "Freier Anteil und bezahlte Zahlen"],
    ["Die Reichweite einer Website einzuordnen", "Ähnliche Angebote zu finden"], False)
add("SparkToro", "https://sparktoro.com/", "sparktoro.com", "freemium", "proprietary", ["seo", "marketing"],
    "SparkToro zeigt, welche Quellen und Profile eine Zielgruppe nutzt.",
    "SparkToro sucht nach einer Beschreibung der Zielgruppe und listet Medien und Konten. Es gibt einen Einstieg und bezahlte Abfragen.",
    ["Quellen einer Zielgruppe", "Medien und Profile", "Einstieg und bezahlte Abfragen"],
    ["Zu sehen, wo eine Zielgruppe liest", "Profile für eine Ansprache zu finden"], False)
add("Frase", "https://www.frase.io/", "frase.io", "freemium", "proprietary", ["seo", "textgenerierung"],
    "Frase sammelt Fragen aus der Suche und hilft, einen Text daran auszurichten.",
    "Frase zeigt, welche Fragen zu einem Thema auftauchen, und vergleicht den eigenen Entwurf. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Fragen aus der Suche", "Vergleich des Entwurfs", "Einstieg und bezahlte Stufen"],
    ["Einen Text an Suchfragen auszurichten", "Lücken gegenüber anderen Seiten zu sehen"], False)
add("NeuronWriter", "https://www.neuronwriter.com/", "neuronwriter.com", "freemium", "proprietary", ["seo", "textgenerierung"],
    "NeuronWriter bewertet einen Text anhand von Seiten, die schon zu dem Thema ranken.",
    "NeuronWriter schlägt Begriffe vor und zeigt eine Punktzahl. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Vergleich mit rankenden Seiten", "Begriffsvorschläge", "Einstieg und bezahlte Stufen"],
    ["Einen Artikel an ein Thema anzupassen", "Fehlende Begriffe zu sehen"], False)
add("Clearscope", "https://www.clearscope.io/", "clearscope.io", "paid", "proprietary", ["seo", "textgenerierung"],
    "Clearscope prüft, ob ein Text die Begriffe eines Themas abdeckt.",
    "Clearscope vergleicht den Entwurf mit Seiten aus der Suche und markiert Lücken. Die Nutzung ist kostenpflichtig.",
    ["Abdeckung eines Themas", "Lücken im Entwurf", "Kostenpflichtige Nutzung"],
    ["Einen Text vor der Veröffentlichung zu prüfen", "Begriffe zu ergänzen, die im Thema fehlen"], False)
add("Sitebulb", "https://www.sitebulb.com/", "sitebulb.com", "paid", "proprietary", ["seo"],
    "Sitebulb crawlt eine Website und erklärt technische SEO-Befunde.",
    "Sitebulb läuft auf dem eigenen Rechner und zeigt Hinweise mit Begründung. Die Lizenz ist kostenpflichtig.",
    ["Crawl auf dem eigenen Rechner", "Befunde mit Begründung", "Kostenpflichtige Lizenz"],
    ["Eine Website vor einem Relaunch zu prüfen", "Einen technischen Fehler nachzuvollziehen"], False)
add("XOVI", "https://www.xovi.de/", "xovi.de", "freemium", "proprietary", ["seo"],
    "XOVI beobachtet Rankings, Keywords und Sichtbarkeit, mit Sitz in Deutschland.",
    "XOVI zeigt Positionen und Suchbegriffe einer Domain. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Rankings und Keywords", "Sichtbarkeit", "Anbieter aus Deutschland"],
    ["Die Sichtbarkeit einer Domain zu verfolgen", "Keywords eines Wettbewerbers zu sehen"], False)
add("Lumar", "https://www.lumar.io/", "lumar.io", "paid", "proprietary", ["seo"],
    "Lumar crawlt große Websites und zeigt technische SEO-Daten.",
    "Lumar, früher Deepcrawl, sammelt Indexierung, Links und Inhalte. Die Nutzung ist kostenpflichtig.",
    ["Crawl großer Websites", "Indexierung und Links", "Kostenpflichtige Nutzung"],
    ["Eine große Website technisch zu prüfen", "Indexierungsprobleme zu finden"], False)
add("Oncrawl", "https://www.oncrawl.com/", "oncrawl.com", "freemium", "proprietary", ["seo"],
    "Oncrawl verbindet Crawl-Daten mit der Suche und mit Logs.",
    "Oncrawl zeigt, welche Seiten der Crawler und die Suche sehen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Crawl und Suchdaten", "Logs", "Einstieg und bezahlte Stufen"],
    ["Zu sehen, welche Seiten nicht indexiert werden", "Crawl und Logs zu vergleichen"], False)
add("Botify", "https://www.botify.com/", "botify.com", "paid", "proprietary", ["seo"],
    "Botify analysiert Crawl, Logs und Suche für große Websites.",
    "Botify zeigt, wie Suchmaschinen eine Website durchlaufen. Die Nutzung ist kostenpflichtig.",
    ["Crawl, Logs und Suche", "Große Websites", "Kostenpflichtige Nutzung"],
    ["Den Weg einer Suchmaschine durch die Seite zu sehen", "Seiten mit wenig Abrufen zu finden"], False)
add("OpenStreetMap", "https://www.openstreetmap.org/", "openstreetmap.org", "free", "unknown", ["reisen", "daten"],
    "OpenStreetMap ist eine Karte, die eine Gemeinschaft fortschreibt.",
    "Die Karte zeigt Wege, Orte und Gebäude und lässt sich in eigene Programme einbinden. Das Ansehen ist ohne Konto möglich. Eine einzelne OSI-Kennung der Daten wird hier nicht eingetragen.",
    ["Karte der Gemeinschaft", "Wege, Orte und Gebäude", "Ansehen ohne Konto"],
    ["Einen Weg auf der Karte zu prüfen", "Kartendaten für ein eigenes Programm zu nutzen"], True)
add("QGIS", "https://qgis.org/", "qgis.org", "free", "unknown", ["daten", "reisen"],
    "QGIS zeigt und bearbeitet Geodaten auf dem eigenen Rechner.",
    "QGIS legt Karten aus Dateien und Diensten übereinander. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Geodaten auf dem eigenen Rechner", "Überlagerte Karten", "Nutzung ohne Pflichtabo"],
    ["Eine Karte aus eigenen Daten zu zeichnen", "Zwei Ebenen übereinanderzulegen"], False)
add("BRouter", "https://brouter.de/", "brouter.de", "free", "unknown", ["reisen"],
    "BRouter rechnet Rad- und Wanderrouten aus offenen Kartendaten.",
    "BRouter sucht einen Weg nach Profil, etwa fürs Rennrad oder den Alltag. Der Dienst kommt aus Deutschland. Die Berechnung ist ohne Abo möglich. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Routen für Rad und Wandern", "Profile je Fortbewegung", "Berechnung ohne Abo"],
    ["Eine Radroute abseits der Straße zu rechnen", "Ein Profil für den Alltag zu wählen"], True)
add("GraphHopper", "https://graphhopper.com/", "graphhopper.com", "freemium", "unknown", ["reisen", "programmierung"],
    "GraphHopper rechnet Routen und bietet dafür eine Schnittstelle.",
    "GraphHopper sucht Wege für Auto, Rad und Fuß und lässt sich in eigene Programme einbinden. Es gibt einen Einstieg und bezahlte Kontingente. Eine OSI-Kennung der gehosteten Fassung wird hier nicht eingetragen.",
    ["Routen für Auto, Rad und Fuß", "Schnittstelle", "Einstieg und bezahlte Kontingente"],
    ["Eine Route in eine eigene Anwendung einzubauen", "Einen Weg fürs Rad zu rechnen"], False)
add("Leaflet", "https://leafletjs.com/", "leafletjs.com", "free", "unknown", ["programmierung", "reisen"],
    "Leaflet zeichnet interaktive Karten im Browser.",
    "Leaflet legt Kartenkacheln und Markierungen auf eine Seite. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Bibliothek ist ohne Pflichtabo erhältlich.",
    ["Karten im Browser", "Markierungen", "Nutzung ohne Pflichtabo"],
    ["Eine Karte in eine Website einzubauen", "Einen Ort zu markieren"], False)
add("MapLibre", "https://maplibre.org/", "maplibre.org", "free", "unknown", ["programmierung", "reisen"],
    "MapLibre zeichnet Vektorkarten im Browser und auf dem Handy.",
    "MapLibre stellt Bibliotheken bereit, die Kacheln selbst darstellen. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Bibliotheken sind ohne Pflichtabo erhältlich.",
    ["Vektorkarten", "Browser und Handy", "Nutzung ohne Pflichtabo"],
    ["Eine Karte ohne einen bestimmten Kartenanbieter zu zeichnen", "Eine Bibliothek fürs Web zu wählen"], False)
add("Geofabrik", "https://www.geofabrik.de/", "geofabrik.de", "freemium", "proprietary", ["daten", "reisen"],
    "Geofabrik stellt Auszüge aus OpenStreetMap nach Regionen bereit.",
    "Geofabrik aus Karlsruhe bietet kostenlose Auszüge und feinere, bezahlte Zuschnitte. Der Download der Standardauszüge ist ohne Konto möglich.",
    ["Auszüge nach Region", "Kostenlose Standardauszüge", "Feinere Zuschnitte bezahlt"],
    ["Kartendaten eines Landes zu laden", "Einen Auszug für ein Routing zu nutzen"], False)
add("Ride with GPS", "https://ridewithgps.com/", "ridewithgps.com", "freemium", "proprietary", ["reisen"],
    "Ride with GPS plant Radrouten und zeichnet Fahrten auf.",
    "Die Seite legt eine Route auf die Karte und exportiert sie auf den Radcomputer. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Radrouten auf der Karte", "Export auf den Radcomputer", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Radtour zu planen", "Eine Route zu exportieren"], True)
add("TomTom", "https://www.tomtom.com/", "tomtom.com", "freemium", "proprietary", ["reisen"],
    "TomTom liefert Navigation und Kartendaten für Geräte und Autos.",
    "TomTom zeigt Karten, Verkehr und Geräte. Kartenupdates und Geräte sind je nach Angebot kostenpflichtig. Der Sitz ist in den Niederlanden.",
    ["Navigation und Karten", "Verkehr", "Geräte und Updates kostenpflichtig"],
    ["Ein Navigationsgerät einzuordnen", "Kartendaten für eine Anwendung zu prüfen"], False)
add("HERE", "https://www.here.com/", "here.com", "freemium", "proprietary", ["reisen", "programmierung"],
    "HERE stellt Karten und eine Schnittstelle für Navigation bereit.",
    "HERE zeigt Karten und bietet Entwicklern eine API. Es gibt einen Einstieg und bezahlte Kontingente. Der Dienst hat Wurzeln in Europa.",
    ["Karten und Navigation", "Schnittstelle", "Einstieg und bezahlte Kontingente"],
    ["Eine Karte in eine Anwendung einzubauen", "Verkehrsdaten einzubinden"], False)
add("Mapbox", "https://www.mapbox.com/", "mapbox.com", "freemium", "proprietary", ["programmierung", "reisen"],
    "Mapbox zeichnet anpassbare Karten und rechnet Routen über eine Schnittstelle.",
    "Mapbox liefert Kacheln und Stile für eigene Anwendungen. Es gibt einen kostenlosen Einstieg und bezahlte Abrufe.",
    ["Anpassbare Karten", "Routen über die Schnittstelle", "Kostenloser Einstieg und bezahlte Abrufe"],
    ["Eine Karte im eigenen Stil einzubauen", "Eine Route über die API zu rechnen"], False)
add("bpb", "https://www.bpb.de/", "bpb.de", "free", "proprietary", ["bildung", "recherche"],
    "Die Bundeszentrale für politische Bildung erklärt Politik und Gesellschaft.",
    "Die bpb veröffentlicht Texte, Hefte und Zahlen. Die Seiten sind ohne Abo lesbar.",
    ["Texte zu Politik und Gesellschaft", "Hefte und Zahlen", "Lesen ohne Abo"],
    ["Ein politisches Thema nachzulesen", "Eine Zahl aus einem Heft zu suchen"], True)
add("netzpolitik.org", "https://netzpolitik.org/", "netzpolitik.org", "free", "proprietary", ["recherche", "recht"],
    "netzpolitik.org berichtet über digitale Grundrechte und Netzpolitik.",
    "Die Redaktion in Berlin veröffentlicht Recherchen, die ohne Abo lesbar sind. Das Angebot finanziert sich nicht über einen Einzelverkauf der Texte.",
    ["Recherchen zu Grundrechten", "Redaktion in Berlin", "Lesen ohne Abo"],
    ["Eine Recherche zur Netzpolitik zu lesen", "Ein Gesetz aus digitaler Sicht einzuordnen"], True)
add("CORRECTIV", "https://correctiv.org/", "correctiv.org", "free", "proprietary", ["recherche"],
    "CORRECTIV veröffentlicht Recherchen und Faktenchecks.",
    "Das Recherchezentrum zeigt Untersuchungen, die ohne Abo lesbar sind. Der Sitz ist in Essen und Berlin.",
    ["Recherchen und Faktenchecks", "Sitz in Essen und Berlin", "Lesen ohne Abo"],
    ["Einen Faktencheck zu lesen", "Eine Recherche zu einem Thema zu finden"], True)
add("Deutscher Bundestag", "https://www.bundestag.de/", "bundestag.de", "free", "proprietary", ["recht", "recherche"],
    "Der Bundestag veröffentlicht Drucksachen, das Plenum und die Abgeordneten.",
    "Die Website zeigt Dokumente und Mediathek. Die Seiten sind ohne Konto lesbar.",
    ["Drucksachen und Plenum", "Abgeordnete", "Lesen ohne Konto"],
    ["Eine Drucksache zu suchen", "Eine Debatte in der Mediathek zu finden"], True)
add("Bundesregierung", "https://www.bundesregierung.de/", "bundesregierung.de", "free", "proprietary", ["recherche", "recht"],
    "Die Bundesregierung veröffentlicht Beschlüsse, Meldungen und Erklärstücke.",
    "Die Seite zeigt Politikfelder und Dokumente. Die Texte sind ohne Konto lesbar.",
    ["Beschlüsse und Meldungen", "Erklärstücke", "Lesen ohne Konto"],
    ["Einen Beschluss nachzulesen", "Ein Politikfeld zu überblicken"], True)
add("Bundesrat", "https://www.bundesrat.de/", "bundesrat.de", "free", "proprietary", ["recht", "recherche"],
    "Der Bundesrat dokumentiert die Mitwirkung der Länder an Bundesgesetzen.",
    "Die Website zeigt Sitzungen und Drucksachen. Die Dokumente sind ohne Konto lesbar.",
    ["Mitwirkung der Länder", "Sitzungen und Drucksachen", "Lesen ohne Konto"],
    ["Eine Bundesratsdrucksache zu suchen", "Eine Sitzung nachzuvollziehen"], True)
add("vzbv", "https://www.vzbv.de/", "vzbv.de", "free", "proprietary", ["recht", "recherche"],
    "Der Verbraucherzentrale Bundesverband vertritt Verbraucherinnen und Verbraucher politisch.",
    "Der vzbv veröffentlicht Positionen und Meldungen. Die Texte sind ohne Abo lesbar.",
    ["Positionen zu Verbraucherthemen", "Meldungen", "Lesen ohne Abo"],
    ["Eine Position zu einem Vertragsthema zu lesen", "Eine Meldung des Verbands zu finden"], True)
add("Deutsche Welle", "https://www.dw.com/de/", "dw.com", "free", "proprietary", ["recherche"],
    "Die Deutsche Welle sendet Nachrichten und Sprachangebote aus Deutschland in viele Sprachen.",
    "DW.com zeigt Artikel und Videos. Die deutschsprachigen Seiten sind ohne Abo lesbar.",
    ["Nachrichten aus Deutschland", "Mehrere Sprachen", "Lesen ohne Abo"],
    ["Eine Nachricht auf Deutsch zu lesen", "Ein Sprachangebot zu finden"], True)
add("presseportal", "https://www.presseportal.de/", "presseportal.de", "free", "proprietary", ["recherche", "marketing"],
    "presseportal veröffentlicht Pressemitteilungen von Unternehmen und Behörden.",
    "Die Suche findet Mitteilungen nach Thema und Absender. Das Lesen ist ohne Konto möglich.",
    ["Pressemitteilungen", "Suche nach Thema und Absender", "Lesen ohne Konto"],
    ["Eine Mitteilung eines Unternehmens zu finden", "Meldungen zu einem Thema zu verfolgen"], True)
add("BVG", "https://www.bvg.de/", "bvg.de", "free", "proprietary", ["reisen"],
    "Die BVG informiert zu Bussen und Bahnen in Berlin und verkauft Fahrscheine.",
    "Die Seite zeigt Linien und Verbindungen. Die Auskunft ist ohne Konto möglich, die Fahrt ist kostenpflichtig.",
    ["Bus und Bahn in Berlin", "Verbindungen", "Auskunft ohne Konto"],
    ["Eine Verbindung in Berlin zu suchen", "Einen Fahrschein einzuordnen"], True)
add("HVV", "https://www.hvv.de/", "hvv.de", "free", "proprietary", ["reisen"],
    "Der HVV informiert zum Nahverkehr in Hamburg.",
    "Der Hamburger Verkehrsverbund zeigt Linien, Tickets und Ausfälle. Die Auskunft ist ohne Konto möglich, die Fahrt ist kostenpflichtig.",
    ["Nahverkehr in Hamburg", "Tickets und Ausfälle", "Auskunft ohne Konto"],
    ["Eine Verbindung in Hamburg zu suchen", "Ein Ticket einzuordnen"], True)
add("MVG", "https://www.mvg.de/", "mvg.de", "free", "proprietary", ["reisen"],
    "Die MVG informiert zu U-Bahn, Bus und Tram in München.",
    "Die Münchner Verkehrsgesellschaft zeigt Linien und Störungen. Die Auskunft ist ohne Konto möglich, die Fahrt ist kostenpflichtig.",
    ["U-Bahn, Bus und Tram in München", "Störungen", "Auskunft ohne Konto"],
    ["Eine Linie in München nachzusehen", "Eine Störung zu prüfen"], True)
add("RMV", "https://www.rmv.de/", "rmv.de", "free", "proprietary", ["reisen"],
    "Der RMV informiert zum Nahverkehr in Rhein-Main.",
    "Der Rhein-Main-Verkehrsverbund zeigt Verbindungen und Tickets. Die Auskunft ist ohne Konto möglich, die Fahrt ist kostenpflichtig.",
    ["Nahverkehr in Rhein-Main", "Verbindungen und Tickets", "Auskunft ohne Konto"],
    ["Eine Verbindung im Verbund zu suchen", "Ein Ticket nachzulesen"], True)
add("VBB", "https://www.vbb.de/", "vbb.de", "free", "proprietary", ["reisen"],
    "Der VBB informiert zum Nahverkehr in Berlin und Brandenburg.",
    "Der Verkehrsverbund Berlin-Brandenburg zeigt Tarife und Verbindungen. Die Auskunft ist ohne Konto möglich, die Fahrt ist kostenpflichtig.",
    ["Nahverkehr in Berlin und Brandenburg", "Tarife", "Auskunft ohne Konto"],
    ["Einen Tarif des Verbunds nachzulesen", "Eine Verbindung über die Landesgrenze zu suchen"], True)
add("VCD", "https://www.vcd.org/", "vcd.org", "freemium", "proprietary", ["reisen", "recherche"],
    "Der VCD setzt sich für umweltverträglichen Verkehr ein und veröffentlicht Ratgeber.",
    "Der Verkehrsclub Deutschland erklärt Alternativen zum Auto und Mitgliedsleistungen. Ein Teil der Texte ist ohne Mitgliedschaft lesbar.",
    ["Ratgeber zum Verkehr", "Mitgliedschaft", "Texte ohne Mitgliedschaft lesbar"],
    ["Einen Ratgeber zu Bus und Bahn zu lesen", "Die Arbeit des Clubs einzuordnen"], True)
add("Ryanair", "https://www.ryanair.com/", "ryanair.com", "free", "proprietary", ["reisen"],
    "Ryanair verkauft Flüge in Europa und zeigt die Verbindungen auf der eigenen Seite.",
    "Die Suche listet Abflüge und Preise. Sie ist ohne Konto möglich, das Ticket ist kostenpflichtig.",
    ["Flüge in Europa", "Preise und Abflüge", "Suche ohne Konto"],
    ["Einen Flugpreis zu suchen", "Eine Verbindung zu buchen"], True)
add("Tagesspiegel", "https://www.tagesspiegel.de/", "tagesspiegel.de", "freemium", "proprietary", ["recherche"],
    "Der Tagesspiegel berichtet aus Berlin und über Politik.",
    "Ein Teil der Artikel ist frei, längere Stücke liegen hinter einem kostenpflichtigen Zugang.",
    ["Nachrichten aus Berlin", "Politik", "Freier Anteil und kostenpflichtiger Zugang"],
    ["Eine Meldung aus Berlin zu lesen", "Einen Hintergrundartikel zu suchen"], True)
add("Süddeutsche Zeitung", "https://www.sueddeutsche.de/", "sueddeutsche.de", "freemium", "proprietary", ["recherche"],
    "Die Süddeutsche Zeitung berichtet über Politik, Wirtschaft und Kultur.",
    "Ein Teil der Artikel ist frei, das digitale Abo ist kostenpflichtig. Der Verlag sitzt in München.",
    ["Politik, Wirtschaft und Kultur", "Verlag aus München", "Freier Anteil und kostenpflichtiges Abo"],
    ["Eine Meldung zu lesen", "Einen längeren Text einzuordnen"], True)
add("DER SPIEGEL", "https://www.spiegel.de/", "spiegel.de", "freemium", "proprietary", ["recherche"],
    "Der Spiegel veröffentlicht Nachrichten und Recherchen.",
    "Ein Teil der Texte ist frei, SPIEGEL+ ist kostenpflichtig. Die Redaktion sitzt in Hamburg.",
    ["Nachrichten und Recherchen", "Redaktion in Hamburg", "Freier Anteil und kostenpflichtiges SPIEGEL+"],
    ["Eine Recherche zu lesen", "Eine Meldung des Tages zu finden"], True)
add("WELT", "https://www.welt.de/", "welt.de", "freemium", "proprietary", ["recherche"],
    "WELT berichtet über Nachrichten, Wirtschaft und Meinung.",
    "Ein Teil der Artikel ist frei, WELT+ ist kostenpflichtig.",
    ["Nachrichten und Wirtschaft", "Meinung", "Freier Anteil und kostenpflichtiges WELT+"],
    ["Eine Wirtschaftsmeldung zu lesen", "Einen Kommentar zu finden"], True)
add("NZZ", "https://www.nzz.ch/", "nzz.ch", "freemium", "proprietary", ["recherche"],
    "Die Neue Zürcher Zeitung berichtet über Politik, Wirtschaft und Kultur.",
    "Ein Teil der Artikel ist frei, das Abo ist kostenpflichtig. Der Verlag sitzt in Zürich.",
    ["Politik, Wirtschaft und Kultur", "Verlag aus Zürich", "Freier Anteil und kostenpflichtiges Abo"],
    ["Eine Meldung aus der Schweiz zu lesen", "Einen Wirtschaftstext zu finden"], True)
add("taz", "https://www.taz.de/", "taz.de", "freemium", "proprietary", ["recherche"],
    "Die taz berichtet über Politik, Gesellschaft und Kultur.",
    "Viele Artikel sind frei lesbar, die Genossenschaft bietet eine bezahlte Mitgliedschaft. Die Redaktion sitzt in Berlin.",
    ["Politik und Gesellschaft", "Redaktion in Berlin", "Freie Artikel und bezahlte Mitgliedschaft"],
    ["Einen Artikel zu lesen", "Die Finanzierung der Zeitung einzuordnen"], True)
add("der Freitag", "https://www.freitag.de/", "freitag.de", "freemium", "proprietary", ["recherche"],
    "der Freitag veröffentlicht Debatten und Hintergründe.",
    "Ein Teil der Texte ist frei, das Abo ist kostenpflichtig.",
    ["Debatten und Hintergründe", "Freier Anteil", "Kostenpflichtiges Abo"],
    ["Einen Debattenbeitrag zu lesen", "Ein Thema in der Übersicht zu sehen"], True)
add("Cicero", "https://www.cicero.de/", "cicero.de", "freemium", "proprietary", ["recherche"],
    "Cicero veröffentlicht politische Essays und Hintergründe.",
    "Ein Teil der Texte ist frei, das Magazin ist kostenpflichtig.",
    ["Politische Essays", "Freier Anteil", "Kostenpflichtiges Magazin"],
    ["Einen Essay zu lesen", "Ein aktuelles Thema einzuordnen"], True)
add("HORIZONT", "https://www.horizont.net/", "horizont.net", "freemium", "proprietary", ["marketing", "recherche"],
    "HORIZONT berichtet über Werbung, Medien und Marken.",
    "Ein Teil der Meldungen ist frei, weitere Berichte sind kostenpflichtig. Das Fachblatt kommt aus Deutschland.",
    ["Werbung, Medien und Marken", "Freie Meldungen", "Weitere Berichte kostenpflichtig"],
    ["Eine Meldung zur Werbebranche zu lesen", "Eine Kampagne einzuordnen"], False)
add("euronews", "https://de.euronews.com/", "de.euronews.com", "free", "proprietary", ["recherche"],
    "euronews berichtet auf Deutsch über Europa und die Welt.",
    "Die deutschsprachige Ausgabe zeigt Nachrichten und Videos. Die Artikel sind ohne Abo lesbar.",
    ["Nachrichten auf Deutsch", "Europa und die Welt", "Lesen ohne Abo"],
    ["Eine europäische Nachricht zu lesen", "Ein Video zu einem Thema zu sehen"], True)
add("POLITICO Europe", "https://www.politico.eu/", "politico.eu", "freemium", "proprietary", ["recherche"],
    "POLITICO Europe berichtet über Politik in Brüssel und den Hauptstädten.",
    "Ein Teil der Texte ist frei, das Pro-Abo ist kostenpflichtig.",
    ["Politik in Europa", "Freier Anteil", "Kostenpflichtiges Pro-Abo"],
    ["Eine Meldung aus Brüssel zu lesen", "Ein Dossier zu einem Gesetz zu finden"], False)
add("Pulumi", "https://www.pulumi.com/", "pulumi.com", "freemium", "unknown", ["programmierung"],
    "Pulumi beschreibt Infrastruktur in einer Programmiersprache.",
    "Pulumi legt Ressourcen aus Code an. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Infrastruktur aus Code", "Mehrere Sprachen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Server aus einem Programm anzulegen", "Eine Änderung vor dem Anwenden zu sehen"], False)
add("Argo CD", "https://argoproj.io/", "argoproj.io", "free", "unknown", ["programmierung"],
    "Argo CD spielt Kubernetes-Anwendungen aus einem Git-Repository aus.",
    "Argo CD gleicht den Cluster mit dem Stand im Repository ab. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Ausrollen aus Git", "Abgleich mit dem Cluster", "Nutzung ohne Pflichtabo"],
    ["Eine Anwendung aus Git in ein Cluster zu spielen", "Abweichungen vom Repository zu sehen"], False)
add("Flux", "https://fluxcd.io/", "fluxcd.io", "free", "unknown", ["programmierung"],
    "Flux hält ein Kubernetes-Cluster am Stand eines Git-Repository.",
    "Flux zieht Änderungen aus Git und wendet sie an. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Cluster folgt Git", "Automatisches Anwenden", "Nutzung ohne Pflichtabo"],
    ["Ein Cluster an ein Repository zu binden", "Ein Update aus Git zu ziehen"], False)
add("pnpm", "https://pnpm.io/", "pnpm.io", "free", "unknown", ["programmierung"],
    "pnpm installiert JavaScript-Pakete und spart dabei Speicher.",
    "pnpm legt Abhängigkeiten in einem Speicher ab und verlinkt sie in Projekte. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Pakete für JavaScript", "Gemeinsamer Speicher", "Nutzung ohne Pflichtabo"],
    ["Abhängigkeiten eines Projekts zu installieren", "Dieselben Pakete über Projekte zu teilen"], False)
add("Bun", "https://bun.sh/", "bun.sh", "free", "unknown", ["programmierung"],
    "Bun führt JavaScript und TypeScript und installiert Pakete.",
    "Bun startet Skripte und kann als Paketmanager und Bundler dienen. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Laufzeit ist ohne Pflichtabo erhältlich.",
    ["Laufzeit für JavaScript", "Pakete und Bundler", "Nutzung ohne Pflichtabo"],
    ["Ein Skript mit Bun zu starten", "Abhängigkeiten zu installieren"], False)
add("Deno", "https://deno.com/", "deno.com", "freemium", "unknown", ["programmierung"],
    "Deno führt TypeScript und JavaScript mit Rechten, die man einzeln freigibt.",
    "Deno startet Skripte und kann sie veröffentlichen. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Laufzeit ist ohne Pflichtabo erhältlich, Deploy ist bezahlt.",
    ["TypeScript ohne eigenen Übersetzungs-Schritt", "Einzelne Rechte", "Laufzeit ohne Pflichtabo"],
    ["Ein Skript mit eingeschränkten Rechten zu starten", "TypeScript direkt auszuführen"], False)
add("Yarn", "https://www.yarnpkg.com/", "yarnpkg.com", "free", "unknown", ["programmierung"],
    "Yarn installiert JavaScript-Pakete und hält die Versionen fest.",
    "Yarn liest ein Manifest und schreibt einen Lockfile. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Installation von Paketen", "Festgeschriebene Versionen", "Nutzung ohne Pflichtabo"],
    ["Abhängigkeiten eines Projekts zu installieren", "Versionen für das Team festzuhalten"], False)
add("crates.io", "https://crates.io/", "crates.io", "free", "unknown", ["programmierung"],
    "crates.io verteilt Bibliotheken für die Sprache Rust.",
    "Die Seite zeigt Beschreibungen und Versionen und liefert die Crates an Cargo. Die Suche ist ohne Konto möglich. Eine OSI-Kennung des Index wird hier nicht eingetragen.",
    ["Bibliotheken für Rust", "Versionen", "Suche ohne Konto"],
    ["Eine Rust-Bibliothek zu finden", "Die aktuelle Version nachzusehen"], True)
add("Packagist", "https://packagist.org/", "packagist.org", "free", "unknown", ["programmierung"],
    "Packagist verteilt Pakete für PHP und Composer.",
    "Packagist zeigt Pakete und Versionen. Die Suche ist ohne Konto möglich. Eine OSI-Kennung des Index wird hier nicht eingetragen.",
    ["Pakete für PHP", "Versionen für Composer", "Suche ohne Konto"],
    ["Ein PHP-Paket zu finden", "Eine Version für Composer nachzusehen"], True)
add("RubyGems", "https://rubygems.org/", "rubygems.org", "free", "unknown", ["programmierung"],
    "RubyGems verteilt Bibliotheken für die Sprache Ruby.",
    "Die Seite zeigt Gems und Versionen. Die Suche ist ohne Konto möglich. Eine OSI-Kennung des Index wird hier nicht eingetragen.",
    ["Bibliotheken für Ruby", "Versionen", "Suche ohne Konto"],
    ["Ein Gem zu finden", "Die Abhängigkeiten eines Gems zu sehen"], True)
add("Homebrew", "https://brew.sh/", "brew.sh", "free", "unknown", ["programmierung"],
    "Homebrew installiert Programme auf dem Mac und auf Linux über die Kommandozeile.",
    "Homebrew lädt Formeln und legt die Programme ab. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Installation über die Kommandozeile", "Formeln", "Nutzung ohne Pflichtabo"],
    ["Ein Programm auf dem Mac zu installieren", "Eine Formel nachzusehen"], True)
add("Flatpak", "https://flatpak.org/", "flatpak.org", "free", "unknown", ["programmierung"],
    "Flatpak installiert Desktop-Anwendungen in einer eigenen Umgebung.",
    "Flatpak bezieht Anwendungen aus Repositories wie Flathub. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Desktop-Anwendungen", "Eigene Umgebung", "Nutzung ohne Pflichtabo"],
    ["Eine App unabhängig von der Distribution zu installieren", "Ein Repository einzubinden"], False)
add("Snapcraft", "https://snapcraft.io/", "snapcraft.io", "free", "proprietary", ["programmierung"],
    "Snapcraft verteilt Anwendungen als Snap-Pakete.",
    "Der Store listet Snaps und installiert sie auf Linux. Die Suche ist ohne Konto möglich. Der Store ist ein proprietäres Angebot.",
    ["Snap-Pakete", "Store für Linux", "Suche ohne Konto"],
    ["Eine Anwendung als Snap zu finden", "Ein Paket zu installieren"], True)
add("Sublime Text", "https://www.sublimetext.com/", "sublimetext.com", "freemium", "proprietary", ["programmierung"],
    "Sublime Text ist ein schneller Editor für Code.",
    "Sublime Text öffnet große Dateien und lässt sich mit Paketen erweitern. Es gibt eine Testphase, die Lizenz ist kostenpflichtig.",
    ["Editor für Code", "Pakete", "Testphase und kostenpflichtige Lizenz"],
    ["Eine große Datei zu bearbeiten", "Den Editor mit Paketen zu erweitern"], False)
add("Notepad++", "https://notepad-plus-plus.org/", "notepad-plus-plus.org", "free", "unknown", ["programmierung"],
    "Notepad++ bearbeitet Textdateien unter Windows mit Hervorhebung der Syntax.",
    "Notepad++ öffnet viele Dateien in Reitern und färbt Code ein. Eine OSI-Kennung wird hier nicht erneut eingetragen. Der Editor ist ohne Pflichtabo erhältlich.",
    ["Text unter Windows", "Syntax-Hervorhebung", "Nutzung ohne Pflichtabo"],
    ["Eine Konfigurationsdatei zu bearbeiten", "Mehrere Dateien in Reitern zu öffnen"], True)
add("Kate", "https://kate-editor.org/", "kate-editor.org", "free", "unknown", ["programmierung"],
    "Kate ist der Texteditor der KDE-Oberfläche.",
    "Kate öffnet Projekte, hebt Syntax hervor und kann ein Terminal daneben zeigen. Eine OSI-Kennung wird hier nicht erneut eingetragen. Der Editor ist ohne Pflichtabo erhältlich.",
    ["Editor mit Projekten", "Terminal daneben", "Nutzung ohne Pflichtabo"],
    ["Code in einem KDE-Editor zu schreiben", "Ein Projekt mit mehreren Dateien zu öffnen"], False)
add("dpa", "https://www.dpa.de/", "dpa.de", "free", "proprietary", ["recherche"],
    "Die dpa ist eine Nachrichtenagentur und zeigt ausgewählte Meldungen auf ihrer Seite.",
    "dpa.com und die deutsche Seite stellen die Agentur und Beispiele ihrer Meldungen vor. Der Bezug des Dienstes für Redaktionen ist kostenpflichtig, die Vorstellung ist ohne Konto lesbar.",
    ["Nachrichtenagentur", "Beispiele von Meldungen", "Bezug für Redaktionen kostenpflichtig"],
    ["Die Agentur einzuordnen", "Eine Beispielmeldung zu lesen"], False)
add("Bundeskanzler", "https://www.bundeskanzler.de/", "bundeskanzler.de", "free", "proprietary", ["recherche"],
    "Die Seite des Bundeskanzlers veröffentlicht Termine, Reden und Meldungen.",
    "bundeskanzler.de zeigt das Amt und aktuelle Beiträge. Die Seiten sind ohne Konto lesbar.",
    ["Termine und Reden", "Meldungen des Amts", "Lesen ohne Konto"],
    ["Einen Termin des Kanzlers nachzusehen", "Eine Rede zu finden"], True)
add("Alpenverein Österreich", "https://www.alpenverein.at/", "alpenverein.at", "freemium", "proprietary", ["reisen"],
    "Der Österreichische Alpenverein informiert zu Touren, Hütten und Mitgliedschaft.",
    "Die Seite beschreibt Wege und Hütten in Österreich. Ein Teil der Texte ist ohne Mitgliedschaft lesbar.",
    ["Touren und Hütten", "Mitgliedschaft", "Texte ohne Mitgliedschaft lesbar"],
    ["Eine Hütte in Österreich nachzuschlagen", "Die Mitgliedschaft einzuordnen"], True)
add("SAC", "https://www.sac-cas.ch/", "sac-cas.ch", "freemium", "proprietary", ["reisen"],
    "Der Schweizer Alpen-Club informiert zu Touren und Hütten.",
    "Die Seite zeigt Hütten und Touren der Sektionen. Ein Teil ist ohne Mitgliedschaft lesbar.",
    ["Hütten und Touren", "Sektionen", "Ein Teil ohne Mitgliedschaft"],
    ["Eine SAC-Hütte zu finden", "Eine Tour in der Schweiz nachzulesen"], True)
add("Hikr", "https://www.hikr.org/", "hikr.org", "free", "proprietary", ["reisen"],
    "Hikr sammelt Tourenberichte aus den Alpen.",
    "Hikr zeigt Berichte mit Route und Bildern. Das Lesen ist ohne Konto möglich.",
    ["Tourenberichte", "Routen und Bilder", "Lesen ohne Konto"],
    ["Einen Bericht zu einem Gipfel zu lesen", "Eine Route in den Alpen zu finden"], True)


def validate(entries):
    entries[:] = [e for e in entries if e["name"] != "Hikr"]
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
    out = ROOT / "data" / "verified-tools-batch11.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows), "->", out)
