#!/usr/bin/env python3
"""Achte geprüfte Liste."""

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


add("KfW", "https://www.kfw.de/", "kfw.de", "free", "proprietary", ["finanzen", "recherche"],
    "Die KfW vergibt Förderkredite für Gründung, Wohnen und Unternehmen.",
    "Die Kreditanstalt für Wiederaufbau beschreibt Programme und den Weg über die Hausbank. Die Informationen sind ohne Konto lesbar. Der Kredit selbst ist kostenpflichtig und läuft über ein Finanzierungsinstitut.",
    ["Förderkredite", "Programme für Gründung und Wohnen", "Informationen ohne Konto"],
    ["Ein Förderprogramm zu finden", "Den Weg über die Hausbank nachzulesen"], True)
add("IHK", "https://www.ihk.de/", "ihk.de", "free", "proprietary", ["recherche", "recht"],
    "Die IHK informiert Unternehmen zu Ausbildung, Recht und Standort.",
    "Das Portal der Industrie- und Handelskammern verweist auf die örtliche Kammer und deren Angebote. Die Übersichtsseiten sind ohne Konto lesbar.",
    ["Ausbildung, Recht und Standort", "Verweis auf die örtliche Kammer", "Lesen ohne Konto"],
    ["Die zuständige Kammer zu finden", "Ein Angebot zur Ausbildung nachzulesen"], True)
add("DIHK", "https://www.dihk.de/", "dihk.de", "free", "proprietary", ["recherche"],
    "Der DIHK vertritt die Industrie- und Handelskammern und veröffentlicht Positionen.",
    "Die Seite des Deutschen Industrie- und Handelskammertags erklärt Aufgaben und Publikationen. Die Texte sind ohne Konto lesbar.",
    ["Positionen und Publikationen", "Aufgaben der Kammern", "Lesen ohne Konto"],
    ["Eine Position der Kammern zu lesen", "Eine Publikation zu finden"], True)
add("ADAC", "https://www.adac.de/", "adac.de", "freemium", "proprietary", ["reisen"],
    "Der ADAC informiert zu Verkehr, Pannenhilfe und Reisen.",
    "Der Allgemeine Deutsche Automobil-Club beschreibt Mitgliedschaft, Pannenhilfe und Ratgeber. Ein Teil der Texte ist ohne Mitgliedschaft lesbar, die Hilfeleistung ist an die Mitgliedschaft gebunden.",
    ["Verkehr und Pannenhilfe", "Reiseratgeber", "Texte frei, Hilfe über die Mitgliedschaft"],
    ["Einen Ratgeber zu einer Reise zu lesen", "Die Pannenhilfe einzuordnen"], True)
add("HRS", "https://www.hrs.de/", "hrs.de", "free", "proprietary", ["reisen"],
    "HRS zeigt Hotels mit Preis und Lage, mit Schwerpunkt auf Geschäftsreisen.",
    "HRS filtert Unterkünfte nach Ort und Zeitraum. Die Suche ist ohne Konto möglich, die Buchung ist kostenpflichtig. Der Dienst kommt aus Deutschland.",
    ["Hotelsuche", "Fokus auf Geschäftsreisen", "Suche ohne Konto"],
    ["Ein Hotel für einen Zeitraum zu suchen", "Preise in einer Stadt zu vergleichen"], True)
add("Techniker Krankenkasse", "https://www.tk.de/", "tk.de", "free", "proprietary", ["gesundheit"],
    "Die Techniker Krankenkasse informiert zu Leistungen der gesetzlichen Krankenversicherung.",
    "Die TK beschreibt Leistungen, Bonus und den Weg in die Mitgliedschaft. Die Informationsseiten sind ohne Login lesbar. Die Versicherung selbst setzt eine Mitgliedschaft voraus.",
    ["Leistungen der gesetzlichen Krankenversicherung", "Bonus und Mitgliedschaft", "Informationen ohne Login"],
    ["Eine Leistung nachzulesen", "Den Weg in die Mitgliedschaft zu finden"], True)
add("AOK", "https://www.aok.de/", "aok.de", "free", "proprietary", ["gesundheit"],
    "Die AOK informiert zu Leistungen der gesetzlichen Krankenversicherung.",
    "Das Portal verweist auf die regionalen AOKs und beschreibt Leistungen. Die Übersichten sind ohne Login lesbar.",
    ["Leistungen und regionale Kassen", "Übersichten ohne Login", "Gesetzliche Krankenversicherung"],
    ["Die regionale AOK zu finden", "Eine Leistung nachzulesen"], True)
add("Barmer", "https://www.barmer.de/", "barmer.de", "free", "proprietary", ["gesundheit"],
    "Die Barmer informiert zu Leistungen der gesetzlichen Krankenversicherung.",
    "Die Barmer beschreibt Leistungen, Bonusprogramme und Anträge. Die Informationsseiten sind ohne Login lesbar.",
    ["Leistungen und Bonus", "Anträge", "Informationen ohne Login"],
    ["Eine Leistung nachzulesen", "Einen Antragsweg zu finden"], True)
add("DAK", "https://www.dak.de/", "dak.de", "free", "proprietary", ["gesundheit"],
    "Die DAK-Gesundheit informiert zu Leistungen der gesetzlichen Krankenversicherung.",
    "Die DAK beschreibt Leistungen und Services. Die Informationsseiten sind ohne Login lesbar.",
    ["Leistungen und Services", "Gesetzliche Krankenversicherung", "Informationen ohne Login"],
    ["Eine Leistung nachzulesen", "Einen Service der Kasse zu finden"], True)
add("jameda", "https://www.jameda.de/", "jameda.de", "free", "proprietary", ["gesundheit"],
    "jameda findet Ärztinnen und Ärzte und zeigt Termine und Bewertungen.",
    "jameda filtert nach Fachrichtung und Ort. Die Suche ist ohne Konto möglich. Ein Termin kann über die Praxis laufen.",
    ["Arztsuche nach Fach und Ort", "Bewertungen und Termine", "Suche ohne Konto"],
    ["Eine Praxis in der Nähe zu finden", "Einen Termin zu sehen"], True)
add("FHEM", "https://fhem.de/", "fhem.de", "free", "unknown", ["automatisierung"],
    "FHEM steuert Geräte im Haus auf dem eigenen Server.",
    "FHEM bindet Sensoren und Aktoren an und legt Abläufe fest. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Steuerung im eigenen Haus", "Abläufe auf dem eigenen Server", "Nutzung ohne Pflichtabo"],
    ["Eine Lampe oder Heizung selbst zu schalten", "Einen Ablauf ohne Cloud zu bauen"], False)
add("tado", "https://www.tado.com/de", "tado.com", "freemium", "proprietary", ["automatisierung"],
    "tado steuert Heizung und Klima über eine App.",
    "tado hängt Thermostate an die bestehende Heizung und regelt sie nach Zeit und Abwesenheit. Der Dienst kommt aus München. Geräte sind kostenpflichtig, die App hat einen Einstieg und bezahlte Funktionen.",
    ["Thermostate für Heizung und Klima", "Regelung nach Zeit und Abwesenheit", "Geräte kostenpflichtig"],
    ["Eine Heizung per App zu regeln", "Die Temperatur bei Abwesenheit zu senken"], True)
add("TUXEDO", "https://www.tuxedo.de/", "tuxedo.de", "paid", "proprietary", ["programmierung"],
    "TUXEDO verkauft Laptops und PCs, die mit Linux ausgeliefert werden.",
    "TUXEDO stellt Geräte mit eigener Linux-Distribution und Support bereit. Der Sitz ist in Augsburg. Die Rechner sind kostenpflichtig.",
    ["Rechner mit Linux", "Eigener Support", "Kostenpflichtige Geräte"],
    ["Einen Laptop mit Linux zu kaufen", "Support für die vorinstallierte Distribution zu nutzen"], False)
add("DENIC", "https://www.denic.de/", "denic.de", "free", "proprietary", ["recherche"],
    "Die DENIC verwaltet die Domain-Endung .de und bietet eine Whois-Abfrage.",
    "Über die DENIC lässt sich prüfen, ob eine .de-Domain vergeben ist. Die Abfrage ist ohne Konto möglich. Die Registrierung selbst läuft über einen Provider.",
    ["Whois für .de", "Verwaltung der Endung", "Abfrage ohne Konto"],
    ["Zu prüfen, ob eine .de-Domain frei ist", "Den Zuständigen für .de nachzulesen"], True)
add("MetaGer", "https://metager.de/", "metager.de", "free", "unknown", ["recherche"],
    "MetaGer ist eine Metasuchmaschine, die aus Deutschland betrieben wird.",
    "MetaGer fragt mehrere Suchmaschinen ab und zeigt die Treffer gebündelt. Der Dienst wird von SUMA-EV getragen. Die Suche ist ohne Konto möglich. Eine OSI-Kennung der Plattform wird hier nicht eingetragen.",
    ["Metasuche über mehrere Quellen", "Betrieb aus Deutschland", "Suche ohne Konto"],
    ["Eine Suche ohne eigenes Profil zu starten", "Treffer mehrerer Quellen zu vergleichen"], True)
add("1NCE", "https://www.1nce.com/de", "1nce.com", "paid", "proprietary", ["programmierung"],
    "1NCE verkauft Konnektivität für Geräte im Internet der Dinge.",
    "1NCE stellt SIM-Karten mit einem Datenvolumen über eine lange Laufzeit bereit. Der Anbieter sitzt in Köln. Die Karten sind kostenpflichtig.",
    ["Konnektivität für Geräte", "SIM mit langem Zeitraum", "Kostenpflichtige Karten"],
    ["Ein Gerät über Mobilfunk anzubinden", "Eine SIM für viele Jahre zu planen"], False)
add("HHV", "https://www.hhv.de/", "hhv.de", "free", "proprietary", ["musik"],
    "HHV verkauft Schallplatten und Musikbücher, mit Schwerpunkt auf unabhängigen Labels.",
    "HHV zeigt Titel mit Preis und Verfügbarkeit. Die Suche ist ohne Konto möglich, der Kauf ist kostenpflichtig. Der Shop sitzt in Deutschland.",
    ["Schallplatten und Bücher", "Unabhängige Labels", "Suche ohne Konto"],
    ["Eine Platte zu suchen", "Die Verfügbarkeit eines Titels zu prüfen"], True)
add("jpc", "https://www.jpc.de/", "jpc.de", "free", "proprietary", ["musik", "bildung"],
    "jpc verkauft CDs, Schallplatten, Bücher und Filme.",
    "jpc zeigt Titel mit Preis. Die Suche ist ohne Konto möglich, der Kauf ist kostenpflichtig. Der Händler sitzt in Deutschland.",
    ["Tonträger, Bücher und Filme", "Preise und Verfügbarkeit", "Suche ohne Konto"],
    ["Eine CD oder ein Buch zu suchen", "Einen Titel zu bestellen"], True)
add("Alternate", "https://www.alternate.de/", "alternate.de", "free", "proprietary", ["e-commerce"],
    "Alternate verkauft Computer, Bauteile und Unterhaltungselektronik.",
    "Alternate zeigt Geräte mit Preis und Verfügbarkeit. Die Suche ist ohne Konto möglich, der Kauf ist kostenpflichtig. Der Händler sitzt in Deutschland.",
    ["Computer und Bauteile", "Preis und Verfügbarkeit", "Suche ohne Konto"],
    ["Ein Bauteil zu suchen", "Den Preis eines Rechners zu vergleichen"], True)
add("reichelt", "https://www.reichelt.de/", "reichelt.de", "free", "proprietary", ["e-commerce"],
    "reichelt verkauft Elektronikbauteile und Werkstattbedarf.",
    "reichelt listet Bauteile mit Datenblatt und Preis. Die Suche ist ohne Konto möglich, der Kauf ist kostenpflichtig. Der Händler sitzt in Deutschland.",
    ["Elektronikbauteile", "Datenblatt und Preis", "Suche ohne Konto"],
    ["Ein Bauteil mit Datenblatt zu finden", "Werkstattbedarf zu bestellen"], True)
add("Mindfactory", "https://www.mindfactory.de/", "mindfactory.de", "free", "proprietary", ["e-commerce"],
    "Mindfactory verkauft PC-Komponenten und fertige Rechner.",
    "Mindfactory zeigt Prozessoren, Grafikkarten und Komplettsysteme mit Preis. Die Suche ist ohne Konto möglich, der Kauf ist kostenpflichtig.",
    ["PC-Komponenten", "Komplettsysteme", "Suche ohne Konto"],
    ["Eine Grafikkarte zu suchen", "Einen Komplettrechner zu vergleichen"], True)
add("Storytel", "https://www.storytel.com/de", "storytel.com", "paid", "proprietary", ["bildung"],
    "Storytel verleiht Hörbücher und E-Books über ein Abo.",
    "Storytel spielt Titel in der App. Der Zugang ist kostenpflichtig. Es gibt eine deutsche Ausgabe.",
    ["Hörbücher und E-Books", "Deutsche Ausgabe", "Kostenpflichtiges Abo"],
    ["Ein Hörbuch im Abo zu hören", "Einen Roman in der App zu lesen"], True)
add("Jellyfin", "https://jellyfin.org/", "jellyfin.org", "free", "unknown", ["videoschnitt"],
    "Jellyfin spielt die eigene Filmsammlung im Netz des Haushalts ab.",
    "Jellyfin läuft auf dem eigenen Server und streamt Filme und Serien an Geräte im Haus. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Eigene Filmsammlung", "Stream im eigenen Netz", "Nutzung ohne Pflichtabo"],
    ["Einen Film vom eigenen Server abzuspielen", "Eine Sammlung ohne Abo zu verwalten"], False)
add("VLC", "https://www.videolan.org/vlc/", "videolan.org", "free", "unknown", ["videoschnitt", "audio-und-sprache"],
    "VLC spielt Video- und Audiodateien in sehr vielen Formaten.",
    "VLC öffnet lokale Dateien und Streams und setzt Untertitel. Eine OSI-Kennung wird hier nicht erneut eingetragen. Der Player ist ohne Pflichtabo erhältlich.",
    ["Viele Formate", "Untertitel und Streams", "Nutzung ohne Pflichtabo"],
    ["Eine Datei abzuspielen, die ein anderer Player ablehnt", "Einen Stream mit Untertitel zu sehen"], True)
add("Proxmox", "https://www.proxmox.com/de", "proxmox.com", "freemium", "unknown", ["programmierung"],
    "Proxmox betreibt virtuelle Maschinen und Container auf dem eigenen Server.",
    "Proxmox Virtual Environment richtet VMs und Container über eine Weboberfläche ein. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich, Support-Abos sind bezahlt.",
    ["Virtuelle Maschinen und Container", "Weboberfläche", "Software ohne Pflichtabo, Support bezahlt"],
    ["Einen Server in mehrere Maschinen zu teilen", "Einen Container neben einer VM zu betreiben"], False)
add("Debian", "https://www.debian.org/", "debian.org", "free", "unknown", ["programmierung"],
    "Debian ist ein Betriebssystem, das aus frei weitergebbaren Paketen besteht.",
    "Debian installiert ein System und bezieht Programme aus eigenen Archiven. Eine einzelne OSI-Kennung für die ganze Distribution wird hier nicht eingetragen. Das System ist ohne Pflichtabo erhältlich.",
    ["Betriebssystem aus Paketen", "Eigene Archive", "Nutzung ohne Pflichtabo"],
    ["Einen Server mit Debian zu installieren", "Ein Paket aus dem Archiv zu beziehen"], False)
add("Python", "https://www.python.org/", "python.org", "free", "unknown", ["programmierung"],
    "Python ist eine Programmiersprache mit Interpreter und Standardbibliothek.",
    "python.org stellt den Interpreter und die Dokumentation bereit. Eine einzelne OSI-Kennung wird hier nicht erneut eingetragen. Der Interpreter ist ohne Pflichtabo erhältlich.",
    ["Interpreter und Standardbibliothek", "Dokumentation", "Nutzung ohne Pflichtabo"],
    ["Ein Skript auszuführen", "Die Dokumentation einer Funktion zu lesen"], True)
add("Rust", "https://www.rust-lang.org/", "rust-lang.org", "free", "unknown", ["programmierung"],
    "Rust ist eine Programmiersprache mit Fokus auf Speicher und Nebenläufigkeit.",
    "rust-lang.org stellt Compiler, Werkzeuge und das Buch zur Sprache bereit. Eine einzelne OSI-Kennung wird hier nicht erneut eingetragen. Die Werkzeuge sind ohne Pflichtabo erhältlich.",
    ["Compiler und Werkzeuge", "Buch zur Sprache", "Nutzung ohne Pflichtabo"],
    ["Ein Programm in Rust zu bauen", "Das Buch zur Sprache zu lesen"], False)
add("KiCad", "https://www.kicad.org/", "kicad.org", "free", "unknown", ["design", "programmierung"],
    "KiCad zeichnet Schaltpläne und Leiterplatten.",
    "KiCad setzt Symbole, Netze und das Layout einer Platine. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Schaltplan und Layout", "Eigene Bauteilbibliotheken", "Nutzung ohne Pflichtabo"],
    ["Einen Schaltplan zu zeichnen", "Eine Leiterplatte zu layouten"], False)
add("Seafile", "https://www.seafile.com/", "seafile.com", "freemium", "unknown", ["produktivitaet"],
    "Seafile synchronisiert Dateien und lässt sich selbst betreiben.",
    "Seafile hält Bibliotheken auf dem eigenen Server oder in einer Cloud und gleicht sie mit den Geräten ab. Der Ursprung liegt in Peking und es gibt Anbieter in Deutschland. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Dateibibliotheken", "Selbstbetrieb und Cloud", "Lizenz nicht eingetragen"],
    ["Dateien eines Teams selbst zu hosten", "Einen Ordner zwischen Geräten abzugleichen"], False)
add("Filen", "https://www.filen.io/", "filen.io", "freemium", "proprietary", ["produktivitaet"],
    "Filen speichert Dateien verschlüsselt in einer Cloud aus Deutschland.",
    "Filen legt Dateien ab und gleicht sie mit den Geräten ab. Der Anbieter sitzt in Deutschland. Es gibt einen kostenlosen Speicher und bezahlte Stufen.",
    ["Verschlüsselte Cloud", "Abgleich mit Geräten", "Kostenloser Speicher und bezahlte Stufen"],
    ["Dateien verschlüsselt abzulegen", "Einen Ordner zwischen Rechnern abzugleichen"], True)
add("Tresorit", "https://www.tresorit.com/", "tresorit.com", "paid", "proprietary", ["produktivitaet"],
    "Tresorit speichert und teilt Dateien Ende-zu-Ende-verschlüsselt.",
    "Tresorit legt Ordner ab und gibt sie gezielt frei. Der Dienst kommt aus der Schweiz und Ungarn. Die Nutzung ist kostenpflichtig.",
    ["Ende-zu-Ende-Verschlüsselung", "Gezieltes Freigeben", "Kostenpflichtige Nutzung"],
    ["Einen Ordner verschlüsselt zu teilen", "Dateien eines Teams abzulegen"], False)
add("pCloud", "https://www.pcloud.com/", "pcloud.com", "freemium", "proprietary", ["produktivitaet"],
    "pCloud speichert Dateien und kann sie clientseitig verschlüsseln.",
    "pCloud gleicht Ordner ab und bietet einen verschlüsselten Bereich als Zusatz. Der Dienst kommt aus der Schweiz. Es gibt einen kostenlosen Speicher und bezahlte Stufen.",
    ["Dateiabgleich", "Optionaler verschlüsselter Bereich", "Kostenloser Speicher und bezahlte Stufen"],
    ["Dateien in einer Cloud zu halten", "Einen Ordner zusätzlich zu verschlüsseln"], True)
add("UrBackup", "https://www.urbackup.org/", "urbackup.org", "free", "unknown", ["programmierung"],
    "UrBackup sichert Rechner auf einen eigenen Server.",
    "UrBackup legt Abbilder und Dateisicherungen an und spielt sie zurück. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Abbilder und Dateisicherungen", "Eigener Server", "Nutzung ohne Pflichtabo"],
    ["Einen Rechner auf den eigenen Server zu sichern", "Eine Datei zurückzuspielen"], False)
add("IPFire", "https://www.ipfire.org/", "ipfire.org", "free", "unknown", ["programmierung"],
    "IPFire ist eine Firewall-Distribution für den eigenen Router.",
    "IPFire filtert den Verkehr und kann als Gateway im Netz stehen. Das Projekt kommt aus Deutschland. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Firewall für das eigene Netz", "Projekt aus Deutschland", "Nutzung ohne Pflichtabo"],
    ["Den Internetzugang eines Netzes zu filtern", "Einen eigenen Router zu betreiben"], False)
add("OPNsense", "https://opnsense.org/", "opnsense.org", "free", "unknown", ["programmierung"],
    "OPNsense ist eine Firewall mit Weboberfläche für das eigene Netz.",
    "OPNsense filtert Verkehr, baut VPN und zeigt Zustände. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Firewall und VPN", "Weboberfläche", "Nutzung ohne Pflichtabo"],
    ["Einen Router mit Weboberfläche zu betreiben", "Ein VPN für das eigene Netz einzurichten"], False)
add("DuckDuckGo", "https://duckduckgo.com/", "duckduckgo.com", "free", "proprietary", ["recherche"],
    "DuckDuckGo liefert Suchergebnisse, ohne ein Profil der suchenden Person zu bauen.",
    "DuckDuckGo zeigt Treffer und eine kurze Zusammenfassung. Die Suche ist ohne Konto möglich. Das Angebot ist proprietär.",
    ["Suche ohne Profil", "Kurze Zusammenfassung", "Suche ohne Konto"],
    ["Eine Frage zu suchen, ohne ein Konto", "Treffer ohne personalisiertes Profil zu sehen"], True)
add("Startpage", "https://www.startpage.com/", "startpage.com", "free", "proprietary", ["recherche"],
    "Startpage zeigt Suchergebnisse, ohne die Abfrage direkt an die suchende Person zu knüpfen.",
    "Startpage reicht eine Suche weiter und liefert die Treffer zurück. Die Nutzung ist ohne Konto möglich.",
    ["Weitergereichte Suche", "Treffer ohne eigenes Profil", "Nutzung ohne Konto"],
    ["Eine Suche ohne eigenes Konto zu starten", "Treffer einer großen Suche zu sehen"], True)
add("Qwant", "https://www.qwant.com/", "qwant.com", "free", "proprietary", ["recherche"],
    "Qwant ist eine Suchmaschine aus Europa ohne Werbeprofil der Person.",
    "Qwant zeigt Webtreffer und Nachrichten. Die Suche ist ohne Konto möglich. Der Dienst kommt aus Frankreich.",
    ["Websuche und Nachrichten", "Anbieter aus Frankreich", "Suche ohne Konto"],
    ["Eine Suche ohne Profil zu starten", "Nachrichten zu einem Thema zu sehen"], True)
add("Proton VPN", "https://protonvpn.com/", "protonvpn.com", "freemium", "proprietary", ["programmierung"],
    "Proton VPN leitet den Verkehr über einen verschlüsselten Tunnel.",
    "Proton VPN bietet einen kostenlosen Zugang mit Einschränkungen und bezahlte Server. Der Dienst kommt aus der Schweiz.",
    ["Verschlüsselter Tunnel", "Kostenloser Zugang und bezahlte Server", "Anbieter aus der Schweiz"],
    ["Den Verkehr über einen Tunnel zu schicken", "Einen Server in einem anderen Land zu wählen"], True)
add("Mullvad VPN", "https://mullvad.net/en/vpn", "mullvad.net", "paid", "proprietary", ["programmierung"],
    "Mullvad VPN leitet den Verkehr durch einen Tunnel und verlangt keine E-Mail.",
    "Mullvad nummeriert Konten statt Namen zu speichern. Der Dienst kommt aus Schweden. Die Nutzung ist kostenpflichtig.",
    ["Tunnel ohne E-Mail-Konto", "Nummerierte Konten", "Kostenpflichtige Nutzung"],
    ["Den Verkehr über einen schwedischen Dienst zu leiten", "Ein Konto ohne Namen anzulegen"], False)
add("deepset", "https://www.deepset.ai/", "deepset.ai", "freemium", "proprietary", ["ki-chatbots", "programmierung"],
    "deepset baut Anwendungen, die Fragen an eigene Dokumente stellen.",
    "deepset, der Macher von Haystack, stellt eine Plattform bereit, die Texte durchsucht und antwortet. Der Sitz ist in Berlin. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Fragen an eigene Dokumente", "Plattform aus Berlin", "Einstieg und bezahlte Stufen"],
    ["Eine Suche über eigene Texte zu bauen", "Eine Antwort mit Quellen aus Dokumenten zu holen"], False)
add("Plex", "https://www.plex.tv/de/", "plex.tv", "freemium", "proprietary", ["videoschnitt"],
    "Plex spielt die eigene Filmsammlung und zusätzliche Kanäle ab.",
    "Plex streamt Dateien vom eigenen Server an Fernseher und Handy. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo für weitere Funktionen.",
    ["Eigene Filme und zusätzliche Kanäle", "Stream auf mehrere Geräte", "Kostenloser Einstieg und bezahltes Abo"],
    ["Einen Film vom eigenen Server zu sehen", "Dieselbe Bibliothek auf dem Fernseher zu öffnen"], True)
add("Spotify", "https://www.spotify.com/", "spotify.com", "freemium", "proprietary", ["musik"],
    "Spotify spielt Musik, Podcasts und Hörbücher.",
    "Spotify streamt einen Katalog und legt Playlists an. Es gibt einen werbefinanzierten Einstieg und ein bezahltes Abo.",
    ["Musik, Podcasts und Hörbücher", "Playlists", "Werbefinanzierter Einstieg und bezahltes Abo"],
    ["Ein Album zu hören", "Eine Playlist für eine Strecke zu bauen"], True)
add("Deezer", "https://www.deezer.com/", "deezer.com", "freemium", "proprietary", ["musik"],
    "Deezer streamt Musik und Podcasts.",
    "Deezer spielt einen Katalog und empfiehlt Titel. Es gibt einen Einstieg und ein bezahltes Abo. Der Dienst kommt aus Frankreich.",
    ["Musik und Podcasts", "Empfehlungen", "Einstieg und bezahltes Abo"],
    ["Ein Album zu hören", "Einen Sender nach Stimmung zu starten"], True)
add("Qobuz", "https://www.qobuz.com/de-de", "qobuz.com", "freemium", "proprietary", ["musik"],
    "Qobuz streamt Musik in hoher Auflösung und verkauft Downloads.",
    "Qobuz spielt Alben in höheren Bitraten als ein normaler Stream und bietet den Kauf einzelner Titel. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Stream in hoher Auflösung", "Download einzelner Titel", "Einstieg und bezahlte Stufen"],
    ["Ein Album in hoher Qualität zu hören", "Einen Titel zu kaufen"], False)
add("SoundCloud", "https://soundcloud.com/", "soundcloud.com", "freemium", "proprietary", ["musik"],
    "SoundCloud spielt Tracks von unabhängigen Künstlerinnen und Künstlern.",
    "SoundCloud streamt einzelne Stücke und Mixe und lässt eigene Tracks hochladen. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Tracks und Mixe", "Eigener Upload", "Kostenloser Einstieg und bezahltes Abo"],
    ["Einen Mix zu hören", "Einen eigenen Track hochzuladen"], True)
add("Wikipedia", "https://de.wikipedia.org/", "de.wikipedia.org", "free", "unknown", ["bildung", "recherche"],
    "Die deutschsprachige Wikipedia erklärt Begriffe, die eine Gemeinschaft fortschreibt.",
    "Artikel nennen Quellen und lassen sich ohne Konto lesen. Eine einzelne OSI-Kennung für die Plattform wird hier nicht eingetragen. Das Lesen ist ohne Abo möglich.",
    ["Artikel mit Quellen", "Gemeinschaftlich fortgeschrieben", "Lesen ohne Abo"],
    ["Einen Begriff nachzuschlagen", "Die Quellen eines Artikels zu prüfen"], True)
add("Project Gutenberg", "https://www.gutenberg.org/", "gutenberg.org", "free", "unknown", ["bildung"],
    "Project Gutenberg stellt gemeinfreie Bücher als Datei bereit.",
    "Die Bibliothek bietet vor allem englischsprachige Werke, deren Schutz abgelaufen ist, zum Download. Das Lesen ist ohne Konto möglich. Eine OSI-Kennung der Plattform wird hier nicht eingetragen.",
    ["Gemeinfreie Bücher", "Download als Datei", "Lesen ohne Konto"],
    ["Einen gemeinfreien Roman zu laden", "Ein Werk nach Autor zu suchen"], True)
add("Zenodo", "https://zenodo.org/", "zenodo.org", "free", "unknown", ["recherche", "daten"],
    "Zenodo speichert Forschungsdaten und Texte und vergibt eine DOI.",
    "Zenodo nimmt Dateien eines Projekts entgegen und macht sie zitierfähig. Der Dienst wird von CERN betrieben. Das Ablegen ist ohne Abo möglich. Eine OSI-Kennung der Plattform wird hier nicht eingetragen.",
    ["Forschungsdaten mit DOI", "Betrieb durch CERN", "Ablegen ohne Abo"],
    ["Einen Datensatz zitierfähig abzulegen", "Eine veröffentlichte Datei zu finden"], False)
add("ORCID", "https://orcid.org/", "orcid.org", "free", "proprietary", ["recherche"],
    "ORCID vergibt eine dauerhafte Kennung für Forschende.",
    "ORCID verbindet eine Person mit ihren Publikationen, unabhängig vom Arbeitgeber. Die Kennung ist ohne Abo erhältlich.",
    ["Dauerhafte Kennung", "Verknüpfung mit Publikationen", "Nutzung ohne Abo"],
    ["Eine Forschenden-Kennung anzulegen", "Publikationen einer Person zuzuordnen"], True)
add("Mendeley", "https://www.mendeley.com/", "mendeley.com", "freemium", "proprietary", ["recherche", "bildung"],
    "Mendeley sammelt Literatur und setzt Zitate in ein Dokument.",
    "Mendeley speichert Papers und formatiert das Literaturverzeichnis. Es gibt einen kostenlosen Einstieg und bezahlten Speicher.",
    ["Literatursammlung", "Zitate im Dokument", "Kostenloser Einstieg und bezahlter Speicher"],
    ["Papers zu einem Thema zu sammeln", "Ein Literaturverzeichnis zu erzeugen"], True)
add("Onshape", "https://www.onshape.com/", "onshape.com", "freemium", "proprietary", ["dreid"],
    "Onshape konstruiert CAD-Modelle im Browser, auch zu mehreren.",
    "Onshape zeichnet Bauteile und Baugruppen und speichert die Versionen. Es gibt einen kostenlosen Einstieg für öffentliche Projekte und bezahlte Pläne.",
    ["CAD im Browser", "Baugruppen und Versionen", "Öffentliche Projekte frei, Pläne bezahlt"],
    ["Ein Bauteil mit anderen zu konstruieren", "Eine Version eines Modells festzuhalten"], False)
add("Poly Haven", "https://polyhaven.com/", "polyhaven.com", "free", "unknown", ["design", "dreid"],
    "Poly Haven stellt Texturen, Modelle und HDRIs zum Herunterladen bereit.",
    "Poly Haven veröffentlicht Materialien, die sich in 3D-Programmen verwenden lassen. Der Download ist ohne Konto möglich. Eine einzelne OSI-Kennung für alle Inhalte wird hier nicht eingetragen.",
    ["Texturen, Modelle und HDRIs", "Download", "Nutzung ohne Konto"],
    ["Eine Textur für eine Szene zu laden", "Ein HDRI für die Beleuchtung zu nehmen"], True)
add("Sketchfab", "https://sketchfab.com/", "sketchfab.com", "freemium", "proprietary", ["dreid"],
    "Sketchfab zeigt 3D-Modelle im Browser und nimmt eigene Uploads an.",
    "Sketchfab dreht ein Modell im Fenster und kann es in eine Seite einbetten. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["3D-Modelle im Browser", "Einbettung und Upload", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Modell im Browser zu drehen", "Ein eigenes Modell zu veröffentlichen"], True)
add("LibreCAD", "https://www.librecad.org/", "librecad.org", "free", "unknown", ["dreid", "design"],
    "LibreCAD zeichnet zweidimensionale CAD-Pläne.",
    "LibreCAD setzt Linien, Bögen und Bemaßung in einer technischen Zeichnung. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["2D-Zeichnungen", "Bemaßung", "Nutzung ohne Pflichtabo"],
    ["Einen Grundriss zu zeichnen", "Eine technische Zeichnung zu bemaßen"], False)
add("SolveSpace", "https://www.solvespace.com/", "solvespace.com", "free", "unknown", ["dreid"],
    "SolveSpace konstruiert kleine Bauteile mit Zwangsbedingungen.",
    "SolveSpace setzt Linien und Flächen und löst die gesetzten Maße. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Konstruktion mit Zwangsbedingungen", "Kleine Bauteile", "Nutzung ohne Pflichtabo"],
    ["Ein einfaches Bauteil zu konstruieren", "Ein Maß zu ändern und die Zeichnung neu zu lösen"], False)
add("TrueNAS", "https://www.truenas.com/", "truenas.com", "freemium", "unknown", ["daten"],
    "TrueNAS speichert Dateien auf dem eigenen Server mit Prüfsummen.",
    "TrueNAS richtet Freigaben und Sicherungen ein. Eine OSI-Kennung wird hier nicht erneut eingetragen. Es gibt eine Ausgabe ohne Pflichtabo und bezahlte Appliances.",
    ["Dateispeicher mit Prüfsummen", "Freigaben und Sicherungen", "Ausgabe ohne Pflichtabo und bezahlte Geräte"],
    ["Einen Dateiserver selbst zu betreiben", "Eine Freigabe für ein Team einzurichten"], False)
add("Synology", "https://www.synology.com/", "synology.com", "paid", "proprietary", ["daten"],
    "Synology verkauft Netzwerkspeicher und das System DSM dafür.",
    "Synology-Geräte halten Dateien, Sicherungen und Freigaben im eigenen Netz. Die Geräte sind kostenpflichtig.",
    ["Netzwerkspeicher", "Sicherungen und Freigaben", "Kostenpflichtige Geräte"],
    ["Dateien im eigenen Netz zu halten", "Eine Sicherung mehrerer Rechner abzulegen"], False)
add("QNAP", "https://www.qnap.com/", "qnap.com", "paid", "proprietary", ["daten"],
    "QNAP verkauft Netzwerkspeicher für Dateien und Sicherungen.",
    "QNAP-Geräte stellen Freigaben im eigenen Netz bereit. Die Geräte sind kostenpflichtig.",
    ["Netzwerkspeicher", "Freigaben im eigenen Netz", "Kostenpflichtige Geräte"],
    ["Einen gemeinsamen Ordner im Netz zu betreiben", "Sicherungen auf das eigene Gerät zu legen"], False)
add("VirtualBox", "https://www.virtualbox.org/", "virtualbox.org", "free", "unknown", ["programmierung"],
    "VirtualBox startet ein zweites Betriebssystem in einem Fenster.",
    "VirtualBox richtet eine virtuelle Maschine ein und startet sie auf dem vorhandenen Rechner. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Zweites System im Fenster", "Virtuelle Maschinen", "Nutzung ohne Pflichtabo"],
    ["Ein anderes System zum Testen zu starten", "Eine Anwendung isoliert auszuprobieren"], False)
add("mpv", "https://mpv.io/", "mpv.io", "free", "unknown", ["videoschnitt"],
    "mpv spielt Video- und Audiodateien mit wenig Oberfläche.",
    "mpv öffnet Dateien und Streams über die Tastatur. Eine OSI-Kennung wird hier nicht erneut eingetragen. Der Player ist ohne Pflichtabo erhältlich.",
    ["Wiedergabe mit wenig Oberfläche", "Dateien und Streams", "Nutzung ohne Pflichtabo"],
    ["Eine Datei ohne große Oberfläche abzuspielen", "Einen Stream zu öffnen"], False)
add("Navidrome", "https://www.navidrome.org/", "navidrome.org", "free", "unknown", ["musik"],
    "Navidrome streamt die eigene Musiksammlung im Netz.",
    "Navidrome liest einen Ordner mit Musik und stellt sie Apps bereit. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Eigene Musiksammlung", "Stream an Apps", "Nutzung ohne Pflichtabo"],
    ["Die eigene Musik auf dem Handy zu hören", "Einen Musikordner selbst zu hosten"], False)
add("MusicBrainz", "https://musicbrainz.org/", "musicbrainz.org", "free", "unknown", ["musik", "daten"],
    "MusicBrainz sammelt Metadaten zu Aufnahmen, Alben und Künstlerinnen.",
    "MusicBrainz hält eine offene Datenbank, die andere Programme abfragen. Das Lesen ist ohne Konto möglich. Eine einzelne OSI-Kennung wird hier nicht eingetragen.",
    ["Metadaten zu Aufnahmen", "Abfrage durch andere Programme", "Lesen ohne Konto"],
    ["Ein Album eindeutig zuzuordnen", "Metadaten für eine Sammlung zu beziehen"], True)
add("Last.fm", "https://www.last.fm/de", "last.fm", "freemium", "proprietary", ["musik"],
    "Last.fm protokolliert gehörte Musik und empfiehlt Ähnliches.",
    "Last.fm schreibt mit, was gespielt wurde, und zeigt Statistiken. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Protokoll gehörter Musik", "Statistiken und Empfehlungen", "Kostenloser Einstieg und bezahltes Abo"],
    ["Zu sehen, was man im Jahr gehört hat", "Ähnliche Künstler zu finden"], True)
add("setlist.fm", "https://www.setlist.fm/", "setlist.fm", "free", "proprietary", ["musik", "recherche"],
    "setlist.fm sammelt Setlists von Konzerten.",
    "setlist.fm zeigt, welche Stücke bei einem Auftritt gespielt wurden. Die Suche ist ohne Konto möglich.",
    ["Setlists von Konzerten", "Suche nach Künstlerin und Stadt", "Suche ohne Konto"],
    ["Die Setlist eines Konzerts nachzuschlagen", "Zu sehen, welche Stücke eine Tour spielt"], True)
add("Songkick", "https://www.songkick.com/", "songkick.com", "free", "proprietary", ["musik", "reisen"],
    "Songkick zeigt Konzerte in einer Stadt und zu einer Künstlerin.",
    "Songkick listet Termine und Spielorte. Die Suche ist ohne Konto möglich, die Karte liegt beim Veranstalter.",
    ["Konzerttermine", "Spielorte", "Suche ohne Konto"],
    ["Konzerte in einer Stadt zu finden", "Die nächste Tour einer Künstlerin zu sehen"], True)
add("Garmin", "https://www.garmin.com/", "garmin.com", "freemium", "proprietary", ["gesundheit", "reisen"],
    "Garmin verkauft Uhren und Navis und zeigt die Aktivitäten in einer App.",
    "Garmin Connect nimmt Läufe, Fahrten und Routen auf. Die Geräte sind kostenpflichtig, die Anzeige der eigenen Aktivitäten ist ohne separates Abo beschrieben.",
    ["Uhren und Navis", "Aktivitäten und Routen", "Geräte kostenpflichtig"],
    ["Einen Lauf aufzuzeichnen", "Eine Route auf das Gerät zu laden"], True)
add("Zwift", "https://www.zwift.com/", "zwift.com", "paid", "proprietary", ["gesundheit"],
    "Zwift setzt Radfahren und Laufen in eine virtuelle Strecke.",
    "Zwift nimmt die Leistung eines Trainers oder Laufbands und bewegt eine Figur auf einer Strecke. Die Nutzung ist kostenpflichtig.",
    ["Virtuelle Strecken", "Anbindung an Trainer und Laufband", "Kostenpflichtige Nutzung"],
    ["Eine Einheit auf der Rolle zu fahren", "Mit anderen auf einer virtuellen Strecke zu sein"], False)
add("Airtable", "https://www.airtable.com/", "airtable.com", "freemium", "proprietary", ["daten", "produktivitaet"],
    "Airtable legt Tabellen an, die sich wie eine kleine Datenbank verhalten.",
    "Airtable mischt Zeilen, Ansichten und Formulare. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Tabellen mit Ansichten", "Formulare", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Liste mit mehreren Ansichten zu führen", "Ein Formular an eine Tabelle zu hängen"], True)
add("monday.com", "https://www.monday.com/", "monday.com", "freemium", "proprietary", ["produktivitaet"],
    "monday.com führt Arbeit als Tabelle mit Status und Datum.",
    "monday legt Boards an und zeigt, wer woran arbeitet. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Boards mit Status", "Zuständigkeiten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Projekt als Tabelle zu führen", "Den Status einer Aufgabe zu sehen"], True)
add("Anytype", "https://www.anytype.io/", "anytype.io", "freemium", "unknown", ["produktivitaet"],
    "Anytype speichert Notizen als verknüpfte Objekte, auch lokal.",
    "Anytype legt Seiten an und kann sie auf dem Gerät halten. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt einen Einstieg und weitere Angebote.",
    ["Verknüpfte Notizen", "Lokal auf dem Gerät", "Lizenz nicht eingetragen"],
    ["Ein Wissensnetz auf dem eigenen Gerät zu bauen", "Seiten miteinander zu verknüpfen"], False)
add("AFFiNE", "https://www.affine.pro/", "affine.pro", "freemium", "unknown", ["produktivitaet"],
    "AFFiNE mischt Dokument, Tafel und Datenbank in einem Arbeitsbereich.",
    "AFFiNE schreibt Seiten und schaltet dieselbe Fläche in eine Tafel um. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Dokument und Tafel", "Ein Arbeitsbereich", "Einstieg und bezahlte Stufen"],
    ["Eine Notiz in eine Tafel umzuschalten", "Ein Projekt an einem Ort zu halten"], False)
add("Capacities", "https://www.capacities.io/", "capacities.io", "freemium", "proprietary", ["produktivitaet"],
    "Capacities legt Notizen als Objekte mit Typ an.",
    "Capacities unterscheidet Personen, Bücher und eigene Typen und verknüpft sie. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Objekte mit Typ", "Verknüpfungen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Lese-Notiz an ein Buch zu hängen", "Ein Thema über Objekte zu ordnen"], True)
add("Ulysses", "https://ulysses.app/", "ulysses.app", "paid", "proprietary", ["textgenerierung", "produktivitaet"],
    "Ulysses schreibt längere Texte in einer Bibliothek aus Blättern.",
    "Ulysses sammelt Kapitel als einzelne Blätter und führt sie zu einem Export zusammen. Die App ist kostenpflichtig.",
    ["Texte als Blätter", "Export aus der Bibliothek", "Kostenpflichtige App"],
    ["Ein langes Dokument in Kapitel zu teilen", "Einen Text für die Veröffentlichung zu exportieren"], False)
add("Novelcrafter", "https://www.novelcrafter.com/", "novelcrafter.com", "freemium", "proprietary", ["textgenerierung"],
    "Novelcrafter hält Figuren, Orte und Szenen eines Romans und kann einen Entwurf fortsetzen.",
    "Novelcrafter legt die Bibel einer Geschichte an und schickt Szenen an ein Sprachmodell. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Figuren, Orte und Szenen", "Anbindung eines Sprachmodells", "Einstieg und bezahlte Stufen"],
    ["Die Figuren eines Romans festzuhalten", "Eine Szene fortschreiben zu lassen"], False)
add("Kanka", "https://kanka.io/", "kanka.io", "freemium", "unknown", ["gaming"],
    "Kanka sammelt Orte, Figuren und Chroniken einer Spielwelt.",
    "Kanka legt Einträge einer Kampagne an und verknüpft sie. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Orte, Figuren und Chronik", "Verknüpfte Einträge", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Spielwelt für eine Runde zu bauen", "Einen Ort mit den Figuren zu verknüpfen"], False)
add("Whereby", "https://whereby.com/", "whereby.com", "freemium", "proprietary", ["produktivitaet"],
    "Whereby öffnet einen Videoraum im Browser, ohne eine App zu installieren.",
    "Whereby vergibt einen Raumnamen und lässt Gäste per Link eintreten. Es gibt einen kostenlosen Einstieg und bezahlte Räume.",
    ["Videoraum im Browser", "Eintritt per Link", "Kostenloser Einstieg und bezahlte Räume"],
    ["Ein Gespräch ohne Installation zu starten", "Einen festen Raumlink zu verschicken"], True)
add("Parsec", "https://www.parsec.app/", "parsec.app", "freemium", "proprietary", ["gaming", "programmierung"],
    "Parsec überträgt einen Desktop mit geringer Verzögerung, auch zum Spielen.",
    "Parsec zeigt den Bildschirm eines anderen Rechners und gibt Eingaben zurück. Es gibt einen kostenlosen Einstieg und bezahlte Team-Funktionen.",
    ["Desktop mit geringer Verzögerung", "Eingaben aus der Ferne", "Kostenloser Einstieg und bezahlte Team-Funktionen"],
    ["Einen starken Rechner aus der Ferne zu nutzen", "Einen Bildschirm zum gemeinsamen Sehen freizugeben"], False)
add("Typesense", "https://typesense.org/", "typesense.org", "freemium", "unknown", ["daten", "programmierung"],
    "Typesense liefert eine Suche, die sich selbst betreiben lässt.",
    "Typesense indexiert Datensätze und beantwortet Suchanfragen mit Tippfehler-Toleranz. Eine OSI-Kennung wird hier nicht erneut eingetragen. Es gibt den Selbstbetrieb und eine Cloud.",
    ["Suche mit Tippfehler-Toleranz", "Selbstbetrieb und Cloud", "Lizenz nicht eingetragen"],
    ["Eine Produktsuche selbst zu hosten", "Tippfehler in der Suche abzufangen"], False)
add("Turso", "https://turso.tech/", "turso.tech", "freemium", "proprietary", ["daten", "programmierung"],
    "Turso stellt SQLite-Datenbanken am Rand des Netzes bereit.",
    "Turso startet eine LibSQL-Datenbank und kann sie nah an die Anwendung legen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["SQLite am Rand des Netzes", "LibSQL", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine kleine Datenbank ohne eigenen Server zu starten", "Lesezugriffe nah an die Nutzer zu legen"], False)
add("Twenty", "https://twenty.com/", "twenty.com", "freemium", "unknown", ["marketing"],
    "Twenty ist ein CRM, das sich selbst betreiben lässt.",
    "Twenty legt Personen, Firmen und Chancen an. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine Cloud und den Selbstbetrieb.",
    ["Personen, Firmen und Chancen", "Cloud und Selbstbetrieb", "Lizenz nicht eingetragen"],
    ["Ein CRM selbst zu hosten", "Eine Verkaufschance zu führen"], False)
add("Aptabase", "https://aptabase.com/", "aptabase.com", "freemium", "unknown", ["programmierung"],
    "Aptabase zählt Ereignisse in einer App, ohne ein Profil der Person zu bauen.",
    "Aptabase nimmt wenige Ereignisse entgegen und zeigt Häufigkeiten. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Ereignisse ohne Personenprofil", "Häufigkeiten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Zu sehen, welche Funktion genutzt wird", "Eine App ohne großes Tracking zu messen"], False)
add("Axiom", "https://axiom.co/", "axiom.co", "freemium", "proprietary", ["programmierung"],
    "Axiom durchsucht Logs und Ereignisse einer Anwendung.",
    "Axiom nimmt Logs entgegen und lässt sie abfragen. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Logs und Ereignisse", "Abfragen", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Einen Fehler in den Logs zu suchen", "Ereignisse eines Dienstes zu filtern"], False)
add("Arc", "https://arc.net/", "arc.net", "free", "proprietary", ["recherche"],
    "Arc ist ein Browser, der Tabs in Seitenleisten und Räume sortiert.",
    "Arc legt Tabs beiseite und trennt Bereiche wie Arbeit und Privat. Der Browser ist ohne Abo nutzbar.",
    ["Tabs in der Seitenleiste", "Getrennte Räume", "Nutzung ohne Abo"],
    ["Viele Tabs in Räume zu sortieren", "Arbeit und Privat zu trennen"], True)
add("Coder", "https://coder.com/", "coder.com", "freemium", "proprietary", ["programmierung"],
    "Coder stellt Entwicklungsumgebungen im Browser bereit.",
    "Coder startet eine Umgebung pro Person oder Aufgabe, auf der eigenen Infrastruktur oder gehostet. Es gibt eine Ausgabe zum Selbstbetrieb und bezahlte Angebote. Die gehostete Plattform ist proprietär.",
    ["Entwicklungsumgebung im Browser", "Selbstbetrieb und Hosting", "Bezahlte Angebote neben dem Selbstbetrieb"],
    ["Eine Umgebung für ein Team bereitzustellen", "Einen Workspace pro Aufgabe zu starten"], False)
add("Ferdium", "https://ferdium.org/", "ferdium.org", "free", "unknown", ["produktivitaet"],
    "Ferdium bündelt mehrere Webdienste in einem Fenster.",
    "Ferdium zeigt Chat, Mail und weitere Dienste nebeneinander. Eine OSI-Kennung wird hier nicht eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Mehrere Dienste in einem Fenster", "Chat und Mail", "Nutzung ohne Pflichtabo"],
    ["Mehrere Chats in einer App zu halten", "Zwischen Diensten zu wechseln, ohne den Browser zu füllen"], True)
add("Floorp", "https://floorp.app/", "floorp.app", "free", "unknown", ["recherche"],
    "Floorp ist ein Browser auf Firefox-Basis mit stark verstellbarer Oberfläche.",
    "Floorp lässt Leisten verschieben und setzt eigene Startseiten. Eine OSI-Kennung wird hier nicht getrennt eingetragen. Der Browser ist ohne Abo erhältlich.",
    ["Firefox-Basis", "Verstellbare Oberfläche", "Nutzung ohne Abo"],
    ["Einen Browser mit eigener Leistenanordnung zu nutzen", "Eine Startseite selbst zu setzen"], False)
add("Haystack", "https://haystack.deepset.ai/", "haystack.deepset.ai", "free", "unknown", ["programmierung", "ki-chatbots"],
    "Haystack baut Pipelines, die Dokumente durchsuchen und antworten.",
    "Haystack von deepset verbindet Abruf und ein Sprachmodell in Python. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Bibliothek ist ohne Pflichtabo erhältlich.",
    ["Pipelines für Suche und Antwort", "Python", "Nutzung ohne Pflichtabo"],
    ["Eine Frage-Antwort-Pipeline zu bauen", "Dokumente an ein Modell anzubinden"], False)
add("LangChain", "https://www.langchain.com/", "langchain.com", "freemium", "unknown", ["programmierung", "ki-chatbots"],
    "LangChain verknüpft Sprachmodelle mit Werkzeugen und Daten.",
    "LangChain stellt Bausteine für Ketten, Abruf und Agenten bereit. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Bibliothek ist ohne Pflichtabo erhältlich, LangSmith ist ein bezahltes Zusatzangebot.",
    ["Bausteine für Modelle und Daten", "Abruf und Agenten", "Bibliothek ohne Pflichtabo"],
    ["Ein Modell an eigene Dokumente zu hängen", "Einen Ablauf aus mehreren Schritten zu bauen"], False)
add("LlamaIndex", "https://www.llamaindex.ai/", "llamaindex.ai", "freemium", "unknown", ["programmierung", "daten"],
    "LlamaIndex indexiert Dokumente für Fragen an ein Sprachmodell.",
    "LlamaIndex liest Dateien ein und beantwortet Fragen darüber. Eine OSI-Kennung wird hier nicht eingetragen. Die Bibliothek ist ohne Pflichtabo erhältlich, gehostete Angebote sind bezahlt.",
    ["Index über Dokumente", "Fragen an die Dateien", "Bibliothek ohne Pflichtabo"],
    ["Einen Ordner für ein Modell zu indexieren", "Eine Frage an eigene Dateien zu stellen"], False)
add("Baserow", "https://baserow.io/", "baserow.io", "freemium", "unknown", ["daten"],
    "Baserow legt Tabellen im Browser an und lässt sich selbst betreiben.",
    "Baserow mischt Zeilen, Ansichten und eine API. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine Cloud und den Selbstbetrieb.",
    ["Tabellen im Browser", "API", "Cloud und Selbstbetrieb"],
    ["Eine Tabelle selbst zu hosten", "Eine Ansicht für ein Team zu bauen"], False)
add("Appsmith", "https://www.appsmith.com/", "appsmith.com", "freemium", "unknown", ["programmierung"],
    "Appsmith baut interne Werkzeuge aus Datenquellen im Browser.",
    "Appsmith setzt Formulare und Tabellen auf eine API oder Datenbank. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine Cloud und den Selbstbetrieb.",
    ["Formulare und Tabellen", "Anbindung an Datenquellen", "Cloud und Selbstbetrieb"],
    ["Ein internes Formular auf eine Datenbank zu setzen", "Ein Werkzeug selbst zu hosten"], False)
add("Retool", "https://www.retool.com/", "retool.com", "freemium", "proprietary", ["programmierung"],
    "Retool baut interne Oberflächen auf Datenbanken und APIs.",
    "Retool setzt Tabellen, Formulare und Knöpfe auf bestehende Systeme. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Interne Oberflächen", "Anbindung an Datenbanken und APIs", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Admin-Werkzeug ohne eigenes Frontend zu bauen", "Eine Tabelle auf eine API zu legen"], False)
add("Budibase", "https://www.budibase.com/", "budibase.com", "freemium", "unknown", ["programmierung"],
    "Budibase baut interne Anwendungen aus Daten und Formularen.",
    "Budibase legt Tabellen und Oberflächen an und kann sie selbst betreiben. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine Cloud und den Selbstbetrieb.",
    ["Tabellen und Formulare", "Cloud und Selbstbetrieb", "Lizenz nicht eingetragen"],
    ["Eine interne App selbst zu hosten", "Ein Formular auf eine Tabelle zu setzen"], False)
add("IFTTT", "https://ifttt.com/", "ifttt.com", "freemium", "proprietary", ["automatisierung"],
    "IFTTT verbindet Dienste nach dem Muster Wenn-dies-dann-das.",
    "IFTTT legt kleine Abläufe an, die einen Auslöser mit einer Aktion verbinden. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Auslöser und Aktion", "Verbindungen zwischen Diensten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Benachrichtigung aus einem anderen Dienst auszulösen", "Zwei Konten mit einer Regel zu verbinden"], True)
add("Prefect", "https://www.prefect.io/", "prefect.io", "freemium", "unknown", ["automatisierung", "daten"],
    "Prefect plant und überwacht Datenläufe in Python.",
    "Prefect hängt Aufgaben zu einem Ablauf und zeigt, welcher Lauf fehlgeschlagen ist. Eine OSI-Kennung wird hier nicht erneut eingetragen. Es gibt den Selbstbetrieb und eine Cloud.",
    ["Abläufe in Python", "Übersicht fehlgeschlagener Läufe", "Selbstbetrieb und Cloud"],
    ["Einen täglichen Datenlauf zu planen", "Einen fehlgeschlagenen Schritt zu sehen"], False)
add("Dagster", "https://dagster.io/", "dagster.io", "freemium", "unknown", ["automatisierung", "daten"],
    "Dagster beschreibt Datenpipelines als Assets und führt sie aus.",
    "Dagster zeigt, welches Asset von welchem abhängt, und startet die Läufe. Eine OSI-Kennung wird hier nicht erneut eingetragen. Es gibt den Selbstbetrieb und eine Cloud.",
    ["Pipelines als Assets", "Abhängigkeiten", "Selbstbetrieb und Cloud"],
    ["Eine Pipeline mit Abhängigkeiten zu bauen", "Einen Lauf nachzuvollziehen"], False)
add("Kestra", "https://kestra.io/", "kestra.io", "freemium", "unknown", ["automatisierung"],
    "Kestra plant Abläufe, die in einer Beschreibung statt nur in Code stehen.",
    "Kestra führt Aufgaben nach einem Zeitplan oder einem Ereignis aus. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt den Selbstbetrieb und eine Cloud.",
    ["Abläufe als Beschreibung", "Zeitplan und Ereignisse", "Selbstbetrieb und Cloud"],
    ["Einen Ablauf ohne großen Orchestrierer zu starten", "Eine Aufgabe zeitlich zu planen"], False)
add("Firecrawl", "https://www.firecrawl.dev/", "firecrawl.dev", "freemium", "proprietary", ["programmierung", "daten"],
    "Firecrawl liest Webseiten und liefert den Inhalt für eigene Anwendungen.",
    "Firecrawl holt Seiten und gibt sie als Text oder Markdown zurück. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Seiten als Text oder Markdown", "Schnittstelle", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Den Inhalt einer Seite für ein Modell zu holen", "Mehrere Unterseiten einzusammeln"], False)
add("Apify", "https://www.apify.com/", "apify.com", "freemium", "proprietary", ["automatisierung", "daten"],
    "Apify lässt fertige Web-Scraper laufen und eigene bauen.",
    "Apify startet Actors, die Seiten auslesen und das Ergebnis ablegen. Es gibt einen kostenlosen Einstieg und bezahlte Nutzung.",
    ["Fertige und eigene Scraper", "Ergebnisse ablegen", "Kostenloser Einstieg und bezahlte Nutzung"],
    ["Daten von einer öffentlichen Seite zu holen", "Einen wiederkehrenden Lauf zu planen"], False)
add("Unstructured", "https://www.unstructured.io/", "unstructured.io", "freemium", "unknown", ["daten", "programmierung"],
    "Unstructured zerlegt Dokumente in Stücke für eine Suche oder ein Modell.",
    "Unstructured liest PDF und andere Formate und gibt Abschnitte zurück. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine Bibliothek und eine bezahlte API.",
    ["Zerlegen von PDF und anderen Formaten", "Abschnitte für eine Suche", "Bibliothek und bezahlte API"],
    ["Ein PDF für einen Index vorzubereiten", "Abschnitte statt der ganzen Datei zu übergeben"], False)
add("Inngest", "https://www.inngest.com/", "inngest.com", "freemium", "proprietary", ["programmierung", "automatisierung"],
    "Inngest führt Hintergrundschritte einer Anwendung zuverlässig aus.",
    "Inngest hängt Funktionen an Ereignisse und wiederholt sie bei Fehlern. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Schritte an Ereignisse", "Wiederholung bei Fehlern", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Hintergrundjob an ein Ereignis zu hängen", "Einen fehlgeschlagenen Schritt erneut laufen zu lassen"], False)
add("Trigger.dev", "https://trigger.dev/", "trigger.dev", "freemium", "unknown", ["programmierung", "automatisierung"],
    "Trigger.dev startet längere Aufgaben aus einer Anwendung heraus.",
    "Trigger.dev führt Jobs außerhalb der Anfrage aus und zeigt den Verlauf. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Jobs außerhalb der Anfrage", "Verlauf", "Einstieg und bezahlte Stufen"],
    ["Eine lange Aufgabe aus einer App auszulagern", "Den Verlauf eines Jobs zu sehen"], False)
add("Hightouch", "https://www.hightouch.com/", "hightouch.com", "freemium", "proprietary", ["daten", "marketing"],
    "Hightouch kopiert Daten aus einem Warehouse in andere Werkzeuge.",
    "Hightouch liest eine Tabelle und schreibt sie in ein CRM oder ein Werbenetz. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Daten aus dem Warehouse", "Ziele wie CRM", "Einstieg und bezahlte Stufen"],
    ["Eine Zielgruppe in ein CRM zu schieben", "Eine Tabelle regelmäßig zu synchronisieren"], False)
add("RudderStack", "https://www.rudderstack.com/", "rudderstack.com", "freemium", "unknown", ["daten", "programmierung"],
    "RudderStack sammelt Ereignisse und leitet sie an andere Werkzeuge weiter.",
    "RudderStack nimmt Ereignisse aus einer App und schickt sie an mehrere Ziele. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine Cloud und den Selbstbetrieb.",
    ["Ereignisse aus der App", "Weiterleitung an Ziele", "Cloud und Selbstbetrieb"],
    ["Ereignisse selbst zu hosten", "Dieselben Ereignisse an mehrere Ziele zu geben"], False)
add("Segment", "https://segment.com/", "segment.com", "freemium", "proprietary", ["daten", "marketing"],
    "Segment sammelt Ereignisse und verteilt sie an Analysewerkzeuge.",
    "Segment nimmt eine Ereignisquelle und schickt sie an mehrere Ziele, ohne den Code jedes Mal zu ändern. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Eine Quelle, mehrere Ziele", "Ereignisse aus der App", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Ereignis an mehrere Werkzeuge zu geben", "Eine Quelle zu wechseln, ohne jedes Ziel neu zu bauen"], False)
add("Backblaze", "https://www.backblaze.com/", "backblaze.com", "paid", "proprietary", ["daten"],
    "Backblaze sichert einen Rechner und bietet Objektspeicher.",
    "Backblaze B2 speichert Dateien über eine Schnittstelle, die persönliche Sicherung legt ein Abbild des Rechners ab. Die Nutzung ist kostenpflichtig.",
    ["Objektspeicher und Rechnersicherung", "Schnittstelle", "Kostenpflichtige Nutzung"],
    ["Ein Backup eines Rechners abzulegen", "Dateien wie in einem Objektspeicher zu halten"], False)
add("MEGA", "https://mega.nz/", "mega.nz", "freemium", "proprietary", ["produktivitaet"],
    "MEGA speichert Dateien verschlüsselt und teilt sie per Link.",
    "MEGA legt Dateien in einem Konto ab und erzeugt Freigabelinks. Es gibt einen kostenlosen Speicher und bezahlte Stufen.",
    ["Verschlüsselte Dateien", "Freigabelinks", "Kostenloser Speicher und bezahlte Stufen"],
    ["Eine große Datei zu verschicken", "Einen Ordner in der Cloud zu halten"], True)
add("Sync.com", "https://www.sync.com/", "sync.com", "freemium", "proprietary", ["produktivitaet"],
    "Sync speichert Dateien mit Ende-zu-Ende-Verschlüsselung.",
    "Sync gleicht Ordner ab und teilt sie mit einem Link oder einem Konto. Es gibt einen kostenlosen Speicher und bezahlte Stufen.",
    ["Ende-zu-Ende-Verschlüsselung", "Abgleich und Freigabe", "Kostenloser Speicher und bezahlte Stufen"],
    ["Einen Ordner verschlüsselt abzulegen", "Eine Datei per Link zu teilen"], True)
add("Box", "https://www.box.com/", "box.com", "freemium", "proprietary", ["produktivitaet"],
    "Box speichert Dateien für Teams und setzt Freigaben und Aufbewahrung.",
    "Box legt Ordner an, regelt, wer sie sieht, und kann Versionen halten. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Team-Ordner und Freigaben", "Versionen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Dateien eines Teams mit Rechten zu teilen", "Eine alte Version einer Datei zu öffnen"], False)
add("Dropbox", "https://www.dropbox.com/", "dropbox.com", "freemium", "proprietary", ["produktivitaet"],
    "Dropbox gleicht einen Ordner zwischen Geräten ab.",
    "Dropbox hält Dateien in der Cloud und auf der Festplatte und teilt Links. Es gibt einen kostenlosen Speicher und bezahlte Stufen.",
    ["Ordnerabgleich", "Freigabelinks", "Kostenloser Speicher und bezahlte Stufen"],
    ["Eine Datei auf mehreren Geräten zu halten", "Einen Link auf einen Ordner zu schicken"], True)
add("WeeChat", "https://weechat.org/", "weechat.org", "free", "unknown", ["social-media"],
    "WeeChat ist ein Chat-Client für IRC im Terminal.",
    "WeeChat verbindet sich mit IRC-Netzen und legt Fenster und Skripte an. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["IRC im Terminal", "Fenster und Skripte", "Nutzung ohne Pflichtabo"],
    ["Einen IRC-Kanal im Terminal zu öffnen", "Mehrere Netze in einem Client zu halten"], False)
add("Libera Chat", "https://libera.chat/", "libera.chat", "free", "unknown", ["social-media"],
    "Libera Chat betreibt ein IRC-Netz für freie Software.",
    "Libera Chat stellt Kanäle bereit, in denen Projekte sich treffen. Der Zutritt mit einem Client ist ohne Abo möglich.",
    ["IRC-Netz für freie Software", "Kanäle je Projekt", "Zutritt ohne Abo"],
    ["Einen Projektkanal zu betreten", "Hilfe zu einem freien Programm zu fragen"], False)
add("Kiwi IRC", "https://kiwiirc.com/", "kiwiirc.com", "free", "proprietary", ["social-media"],
    "Kiwi IRC öffnet IRC-Kanäle im Browser.",
    "Kiwi IRC verbindet sich mit einem Netz, ohne einen eigenen Client zu installieren. Die Nutzung im Browser ist ohne Abo möglich.",
    ["IRC im Browser", "Ohne eigenen Client", "Nutzung ohne Abo"],
    ["Einen Kanal ohne Installation zu öffnen", "Kurz in einem Netz mitzulesen"], True)
add("Bluesky", "https://bsky.app/", "bsky.app", "free", "unknown", ["social-media"],
    "Bluesky zeigt kurze Beiträge in einem Netz, das mehrere Server zulässt.",
    "Bluesky führt ein Profil und eine Zeitleiste. Das Lesen ist ohne Abo möglich. Eine OSI-Kennung der App wird hier nicht eingetragen.",
    ["Kurze Beiträge", "Zeitleiste", "Nutzung ohne Abo"],
    ["Einer Person zu folgen", "Einen kurzen Beitrag zu schreiben"], True)
add("JLCPCB", "https://jlcpcb.com/", "jlcpcb.com", "paid", "proprietary", ["design"],
    "JLCPCB fertigt Leiterplatten nach hochgeladenen Daten.",
    "JLCPCB nimmt Gerber-Dateien entgegen und liefert die Platinen. Die Fertigung ist kostenpflichtig.",
    ["Fertigung nach Gerber-Dateien", "Lieferung der Platinen", "Kostenpflichtige Fertigung"],
    ["Eine Platine fertigen zu lassen", "Eine Stückzahl für einen Prototyp zu bestellen"], False)
add("EasyEDA", "https://easyeda.com/", "easyeda.com", "freemium", "proprietary", ["design"],
    "EasyEDA zeichnet Schaltpläne und Leiterplatten im Browser.",
    "EasyEDA setzt Schaltplan und Layout und kann die Daten an eine Fertigung geben. Es gibt einen kostenlosen Einstieg und bezahlte Funktionen.",
    ["Schaltplan und Layout im Browser", "Übergabe an die Fertigung", "Kostenloser Einstieg und bezahlte Funktionen"],
    ["Eine Platine im Browser zu zeichnen", "Die Daten zur Fertigung zu geben"], False)
add("GrabCAD", "https://grabcad.com/", "grabcad.com", "freemium", "proprietary", ["dreid"],
    "GrabCAD stellt CAD-Modelle von Bauteilen zum Herunterladen bereit.",
    "GrabCAD zeigt Modelle, die andere hochgeladen haben, und Werkzeuge der Firma. Ein Teil ist ohne Abo ladbar.",
    ["CAD-Modelle zum Download", "Community und Werkzeuge", "Teil ohne Abo"],
    ["Ein Normteil als Modell zu finden", "Ein hochgeladenes Bauteil zu laden"], False)
add("Shapr3D", "https://www.shapr3d.com/", "shapr3d.com", "freemium", "proprietary", ["dreid"],
    "Shapr3D konstruiert CAD-Modelle auf dem Tablet und am Rechner.",
    "Shapr3D zeichnet Körper mit dem Stift oder der Maus und exportiert sie. Es gibt einen Einstieg und bezahlte Stufen.",
    ["CAD auf Tablet und Rechner", "Export", "Einstieg und bezahlte Stufen"],
    ["Ein Bauteil auf dem Tablet zu skizzieren", "Einen Körper zu exportieren"], False)
add("Rhino", "https://www.rhino3d.com/", "rhino3d.com", "paid", "proprietary", ["dreid"],
    "Rhino modelliert freie Formen für Design und Fertigung.",
    "Rhino zeichnet Kurven und Flächen und gibt sie an andere Programme weiter. Die Lizenz ist kostenpflichtig.",
    ["Freiform-Modellierung", "Kurven und Flächen", "Kostenpflichtige Lizenz"],
    ["Eine freie Form zu modellieren", "Ein Modell für die Fertigung zu exportieren"], False)
add("MeshLab", "https://www.meshlab.net/", "meshlab.net", "free", "unknown", ["dreid"],
    "MeshLab bearbeitet und repariert Dreiecksnetze.",
    "MeshLab öffnet Scandaten und Netze, vereinfacht sie und schließt Löcher. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Bearbeitung von Netzen", "Vereinfachen und Löcher schließen", "Nutzung ohne Pflichtabo"],
    ["Einen Scan zu bereinigen", "Ein Netz zu vereinfachen"], False)
add("Arduino", "https://www.arduino.cc/", "arduino.cc", "freemium", "proprietary", ["programmierung"],
    "Arduino liefert Platinen und eine Umgebung für kleine Steuerungen.",
    "Arduino-Boards lesen Sensoren und schalten Ausgänge, die IDE schreibt das Programm. Die Platinen sind kostenpflichtig, die Software zum Entwickeln ist ohne Abo erhältlich. Die Marke und die gehosteten Dienste sind proprietär.",
    ["Platinen und Entwicklungsumgebung", "Sensoren und Ausgänge", "Platinen kostenpflichtig"],
    ["Eine kleine Steuerung zu programmieren", "Einen Sensor an einen Ausgang zu hängen"], True)
add("Espressif", "https://www.espressif.com/", "espressif.com", "freemium", "proprietary", ["programmierung"],
    "Espressif stellt Chips der ESP-Reihe für WLAN und Steuerung her.",
    "Espressif dokumentiert Module, die sich mit eigener Firmware betreiben lassen. Die Chips sind kostenpflichtig, ein Teil der Werkzeuge ist ohne Abo erhältlich.",
    ["Chips mit WLAN", "Dokumentation und Werkzeuge", "Chips kostenpflichtig"],
    ["Ein Gerät mit WLAN zu bauen", "Die Dokumentation eines Moduls zu lesen"], False)
add("Adafruit", "https://www.adafruit.com/", "adafruit.com", "free", "proprietary", ["programmierung", "bildung"],
    "Adafruit verkauft Platinen und schreibt Anleitungen dazu.",
    "Adafruit zeigt Bauteile und Lerntexte für kleine Elektronikprojekte. Die Anleitungen sind ohne Konto lesbar, die Bauteile sind kostenpflichtig.",
    ["Platinen und Anleitungen", "Lerntexte", "Anleitungen ohne Konto"],
    ["Eine Anleitung zu einem Sensor zu lesen", "Ein Bauteil für ein Projekt zu finden"], True)
add("SparkFun", "https://www.sparkfun.com/", "sparkfun.com", "free", "proprietary", ["programmierung", "bildung"],
    "SparkFun verkauft Elektronikmodule und dokumentiert sie.",
    "SparkFun zeigt Breakouts und Anleitungen. Die Texte sind ohne Konto lesbar, die Module sind kostenpflichtig.",
    ["Module und Anleitungen", "Breakouts", "Texte ohne Konto"],
    ["Ein Modul mit Anleitung zu finden", "Ein Breakout für einen Sensor zu suchen"], True)
add("balena", "https://www.balena.io/", "balena.io", "freemium", "proprietary", ["programmierung"],
    "balena spielt Container auf eine Flotte kleiner Geräte aus.",
    "balenaOS und balenaCloud verteilen eine Anwendung auf viele Geräte und aktualisieren sie. Es gibt einen kostenlosen Einstieg und bezahlte Gerätezahlen.",
    ["Container auf Geräten", "Aktualisierung einer Flotte", "Kostenloser Einstieg und bezahlte Gerätezahlen"],
    ["Eine Anwendung auf viele Geräte zu verteilen", "Ein Update aus der Ferne zu spielen"], False)
add("Framework", "https://frame.work/", "frame.work", "paid", "proprietary", ["programmierung"],
    "Framework verkauft Laptops, die sich mit Modulen reparieren und erweitern lassen.",
    "Framework liefert Rechner mit tauschbaren Anschlüssen und Ersatzteilen. Die Geräte sind kostenpflichtig.",
    ["Reparierbare Laptops", "Tauschbare Anschlüsse", "Kostenpflichtige Geräte"],
    ["Einen Laptop mit ersetzbaren Teilen zu kaufen", "Einen Anschluss zu wechseln"], False)
add("System76", "https://www.system76.com/", "system76.com", "paid", "proprietary", ["programmierung"],
    "System76 verkauft Rechner mit dem Linux-System Pop!_OS.",
    "System76 liefert Laptops und Desktops, die mit der eigenen Distribution starten. Die Geräte sind kostenpflichtig.",
    ["Rechner mit Pop!_OS", "Laptops und Desktops", "Kostenpflichtige Geräte"],
    ["Einen Rechner mit vorinstalliertem Linux zu kaufen", "Pop!_OS auf der eigenen Seite nachzulesen"], False)
add("MikroTik", "https://www.mikrotik.com/", "mikrotik.com", "paid", "proprietary", ["programmierung"],
    "MikroTik stellt Router und das System RouterOS her.",
    "MikroTik-Geräte routen Netze und lassen sich über eine eigene Oberfläche konfigurieren. Die Hardware ist kostenpflichtig.",
    ["Router und RouterOS", "Eigene Oberfläche", "Kostenpflichtige Hardware"],
    ["Ein Netz mit einem Router zu betreiben", "Eine Route zu konfigurieren"], False)
add("Ubiquiti", "https://www.ui.com/", "ui.com", "paid", "proprietary", ["programmierung"],
    "Ubiquiti verkauft Netzgeräte für WLAN, Routing und Kameras.",
    "Ubiquiti steuert Access Points und Gateways über eine zentrale Oberfläche. Die Geräte sind kostenpflichtig.",
    ["WLAN, Routing und Kameras", "Zentrale Oberfläche", "Kostenpflichtige Geräte"],
    ["Ein WLAN für ein Gebäude zu planen", "Access Points zentral zu sehen"], False)
add("Mosquitto", "https://mosquitto.org/", "mosquitto.org", "free", "unknown", ["programmierung", "automatisierung"],
    "Mosquitto ist ein Nachrichtenbroker für das Protokoll MQTT.",
    "Mosquitto nimmt Nachrichten von Geräten entgegen und verteilt sie an Abonnenten. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["MQTT-Broker", "Nachrichten an Abonnenten", "Nutzung ohne Pflichtabo"],
    ["Sensordaten im eigenen Netz zu verteilen", "Einen Broker selbst zu betreiben"], False)
add("ESPHome", "https://esphome.io/", "esphome.io", "free", "unknown", ["automatisierung", "programmierung"],
    "ESPHome beschreibt die Firmware eines ESP-Chips in einer Konfiguration.",
    "ESPHome erzeugt aus einer Textdatei die Software für Sensoren und Schalter. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Firmware aus einer Konfiguration", "Sensoren und Schalter", "Nutzung ohne Pflichtabo"],
    ["Einen Sensor ohne eigenes C-Programm anzubinden", "Eine Konfiguration auf einen Chip zu spielen"], False)
add("Last.fm deutsch", "https://www.last.fm/de", "last.fm", "freemium", "proprietary", ["musik"],
    "Platzhalter.",
    "Platzhalter.",
    ["x"], ["x"])


def validate(entries):
    skip_tail = {e["name"] for e in entries if e["name"].endswith(" deutsch")}
    entries[:] = [e for e in entries if e["name"] not in skip_tail and e["name"] not in {"IFTTT", "1NCE", "Framework"}]
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
            errors.append(f"dup-domain {entry['domain']}")
        if slug in seen_s:
            errors.append(f"dup-slug {slug}")
        seen_d.add(entry["domain"])
        seen_s.add(slug)
        if not (10 <= len(entry["shortDescriptionDe"]) <= 280):
            errors.append(f"kurz {entry['name']} {len(entry['shortDescriptionDe'])}")
    if errors:
        raise SystemExit("\n".join(errors[:30]))
    return entries


if __name__ == "__main__":
    rows = validate(E)
    out = ROOT / "data" / "verified-tools-batch8.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows), "->", out)
