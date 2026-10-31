#!/usr/bin/env python3
"""Zehnte geprüfte Liste."""

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


add("Hochschulkompass", "https://www.hochschulkompass.de/", "hochschulkompass.de", "free", "proprietary", ["bildung", "recherche"],
    "Der Hochschulkompass listet Studiengänge und Hochschulen in Deutschland.",
    "Die Seite der Hochschulrektorenkonferenz filtert Studiengänge nach Ort und Abschluss. Die Suche ist ohne Konto möglich.",
    ["Studiengänge und Hochschulen", "Filter nach Ort und Abschluss", "Suche ohne Konto"],
    ["Einen Studiengang zu suchen", "Hochschulen eines Fachs zu vergleichen"], True)
add("DFG", "https://www.dfg.de/", "dfg.de", "free", "proprietary", ["recherche", "bildung"],
    "Die DFG fördert Forschung und veröffentlicht Programme und Entscheidungen.",
    "Die Deutsche Forschungsgemeinschaft beschreibt Förderlinien und Verfahren. Die Informationsseiten sind ohne Konto lesbar. Eine Förderung selbst setzt einen Antrag voraus.",
    ["Förderlinien", "Verfahren", "Informationen ohne Konto"],
    ["Ein Förderprogramm zu finden", "Ein Verfahren nachzulesen"], True)
add("BMBF", "https://www.bmbf.de/", "bmbf.de", "free", "proprietary", ["bildung", "recherche"],
    "Das BMBF informiert zu Bildung, Forschung und Förderung.",
    "Das Bundesministerium für Bildung und Forschung veröffentlicht Programme und Meldungen. Die Seiten sind ohne Konto lesbar.",
    ["Programme zu Bildung und Forschung", "Meldungen", "Lesen ohne Konto"],
    ["Ein Förderprogramm nachzulesen", "Eine Meldung des Ministeriums zu lesen"], True)
add("MAXQDA", "https://www.maxqda.com/", "maxqda.com", "paid", "proprietary", ["recherche", "bildung"],
    "MAXQDA wertet Interviews und Texte qualitativ aus.",
    "MAXQDA kodiert Textstellen und zeigt, wie oft ein Kode vorkommt. Der Hersteller sitzt in Berlin. Die Lizenz ist kostenpflichtig.",
    ["Kodieren von Texten", "Auswertung der Kodes", "Kostenpflichtige Lizenz"],
    ["Ein Interview zu kodieren", "Häufigkeiten von Themen zu sehen"], False)
add("Amberscript", "https://www.amberscript.com/", "amberscript.com", "freemium", "proprietary", ["audio-und-sprache"],
    "Amberscript schreibt Sprache aus Audio und Video mit, auch auf Deutsch.",
    "Amberscript erzeugt ein Transkript und lässt es korrigieren. Es gibt einen Einstieg und bezahlte Minuten.",
    ["Transkript aus Audio und Video", "Korrektur im Text", "Einstieg und bezahlte Minuten"],
    ["Ein Interview verschriftlichen zu lassen", "Untertitel aus einer Aufnahme zu erzeugen"], True)
add("Spektrum", "https://www.spektrum.de/", "spektrum.de", "freemium", "proprietary", ["recherche", "bildung"],
    "Spektrum der Wissenschaft erklärt Forschung für ein breites Publikum.",
    "Spektrum veröffentlicht Meldungen und längere Texte zu Naturwissenschaft. Ein Teil ist frei, das Abo ist kostenpflichtig.",
    ["Wissenschaft für ein breites Publikum", "Meldungen und längere Texte", "Freier Anteil und kostenpflichtiges Abo"],
    ["Einen Forschungsstand nachzulesen", "Eine Meldung zu einem Fach zu lesen"], True)
add("GEO", "https://www.geo.de/", "geo.de", "freemium", "proprietary", ["recherche"],
    "GEO berichtet über Natur, Wissen und Reisen.",
    "GEO veröffentlicht Reportagen und Meldungen. Ein Teil ist frei lesbar, das Magazin ist kostenpflichtig.",
    ["Natur, Wissen und Reisen", "Reportagen", "Freier Anteil und kostenpflichtiges Magazin"],
    ["Eine Reportage zu einem Ort zu lesen", "Ein Wissensthema nachzuschlagen"], True)
add("Babbel", "https://www.babbel.com/", "babbel.com", "paid", "proprietary", ["bildung"],
    "Babbel übt Sprachen in kurzen Lektionen, mit Deutsch als Ausgang.",
    "Babbel gibt Dialoge und Wiederholungen vor. Der Dienst kommt aus Berlin. Die Nutzung ist kostenpflichtig.",
    ["Kurze Sprachlektionen", "Dialoge und Wiederholung", "Kostenpflichtige Nutzung"],
    ["Eine Sprache in kurzen Einheiten zu üben", "Einen Dialog zu wiederholen"], True)
add("Duolingo", "https://de.duolingo.com/", "de.duolingo.com", "freemium", "proprietary", ["bildung"],
    "Duolingo übt Sprachen in kurzen Aufgaben mit sofortiger Rückmeldung.",
    "Duolingo führt durch Lektionen und merkt sich Fehler. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Kurze Aufgaben", "Sofortige Rückmeldung", "Kostenloser Einstieg und bezahltes Abo"],
    ["Täglich ein paar Minuten Sprache zu üben", "Eine Lektion zu wiederholen"], True)
add("Khan Academy", "https://de.khanacademy.org/", "de.khanacademy.org", "free", "proprietary", ["bildung"],
    "Die Khan Academy erklärt Schulstoff mit Videos und Aufgaben, auch auf Deutsch.",
    "Die deutschsprachige Seite führt durch Mathematik und weitere Fächer. Die Nutzung ist ohne Abo möglich.",
    ["Videos und Aufgaben", "Deutschsprachige Fächer", "Nutzung ohne Abo"],
    ["Einen Schulstoff mit Aufgaben zu üben", "Ein Erklärvideo anzusehen"], True)
add("Lingoda", "https://www.lingoda.com/", "lingoda.com", "paid", "proprietary", ["bildung"],
    "Lingoda gibt Sprachunterricht in kleinen Gruppen per Video.",
    "Lingoda legt Kurse mit festen Lektionen und Live-Stunden an. Der Dienst kommt aus Berlin. Die Kurse sind kostenpflichtig.",
    ["Live-Unterricht in Gruppen", "Feste Lektionen", "Kostenpflichtige Kurse"],
    ["Eine Sprache mit einer Lehrkraft zu üben", "Einen Kursplan zu folgen"], False)
add("Preply", "https://www.preply.com/", "preply.com", "freemium", "proprietary", ["bildung"],
    "Preply vermittelt Einzelnachhilfe in Sprachen per Video.",
    "Preply zeigt Lehrkräfte mit Preis und lässt Stunden buchen. Die Suche ist ohne sofortige Zahlung möglich, die Stunde ist kostenpflichtig.",
    ["Einzelnachhilfe per Video", "Preis je Lehrkraft", "Suche ohne sofortige Zahlung"],
    ["Eine Lehrkraft für eine Sprache zu finden", "Eine einzelne Stunde zu buchen"], True)
add("italki", "https://www.italki.com/", "italki.com", "freemium", "proprietary", ["bildung"],
    "italki vermittelt Sprachlehrkräfte für Einzelstunden.",
    "italki listet Lehrkräfte und Community-Beiträge. Die Suche ist ohne Abo möglich, die Stunde ist kostenpflichtig.",
    ["Einzelstunden", "Profile von Lehrkräften", "Suche ohne Abo"],
    ["Eine Lehrkraft nach Sprache zu suchen", "Eine Probestunde zu buchen"], True)
add("StudyCheck", "https://www.studycheck.de/", "studycheck.de", "free", "proprietary", ["bildung"],
    "StudyCheck sammelt Erfahrungsberichte zu Studiengängen.",
    "StudyCheck zeigt Bewertungen und Eckdaten eines Studiums. Die Berichte sind ohne Konto lesbar.",
    ["Erfahrungsberichte", "Eckdaten zum Studium", "Lesen ohne Konto"],
    ["Einen Studiengang anhand von Berichten einzuordnen", "Hochschulen eines Fachs zu vergleichen"], True)
add("myStipendium", "https://www.mystipendium.de/", "mystipendium.de", "free", "proprietary", ["bildung", "finanzen"],
    "myStipendium listet Stipendien und rechnet aus, welche passen könnten.",
    "Die Suche filtert Stipendien nach Fach und Person. Ein Teil ist ohne Konto nutzbar.",
    ["Stipendiensuche", "Filter nach Fach", "Ein Teil ohne Konto"],
    ["Ein passendes Stipendium zu suchen", "Voraussetzungen einer Förderung zu lesen"], True)
add("uni-assist", "https://www.uni-assist.de/", "uni-assist.de", "paid", "proprietary", ["bildung"],
    "uni-assist prüft Bewerbungen internationaler Studieninteressierter für deutsche Hochschulen.",
    "uni-assist nimmt Unterlagen entgegen und leitet sie an angeschlossene Hochschulen weiter. Die Bearbeitung ist kostenpflichtig.",
    ["Prüfung internationaler Bewerbungen", "Weiterleitung an Hochschulen", "Kostenpflichtige Bearbeitung"],
    ["Eine Bewerbung für ein Studium in Deutschland vorzubereiten", "Den Weg über uni-assist nachzulesen"], False)
add("KMK", "https://www.kmk.org/", "kmk.org", "free", "proprietary", ["bildung", "recht"],
    "Die Kultusministerkonferenz veröffentlicht Beschlüsse der Länder zu Schule und Hochschule.",
    "Die KMK stellt Vereinbarungen und Listen bereit. Die Dokumente sind ohne Konto lesbar.",
    ["Beschlüsse der Länder", "Schule und Hochschule", "Lesen ohne Konto"],
    ["Eine Vereinbarung der Länder nachzulesen", "Einen Abschluss einzuordnen"], True)
add("Prusa", "https://www.prusa3d.com/de/", "prusa3d.com", "freemium", "proprietary", ["dreid"],
    "Prusa baut 3D-Drucker und stellt PrusaSlicer bereit.",
    "Prusa Research aus Prag verkauft Drucker und dokumentiert den Slicer. Die Drucker sind kostenpflichtig, PrusaSlicer ist ohne Pflichtabo erhältlich.",
    ["3D-Drucker", "PrusaSlicer", "Drucker kostenpflichtig"],
    ["Einen Drucker auszuwählen", "Ein Modell für den Druck vorzubereiten"], False)
add("Bambu Lab", "https://www.bambu-lab.com/", "bambu-lab.com", "paid", "proprietary", ["dreid"],
    "Bambu Lab verkauft 3D-Drucker mit automatischem Materialwechsel.",
    "Bambu Lab liefert Drucker, die mehrere Farben in einem Druck wechseln können. Die Geräte sind kostenpflichtig.",
    ["3D-Drucker", "Materialwechsel", "Kostenpflichtige Geräte"],
    ["Einen Mehrfarbdruck zu planen", "Einen Drucker der Reihe einzuordnen"], False)
add("Creality", "https://www.creality.com/", "creality.com", "paid", "proprietary", ["dreid"],
    "Creality verkauft 3D-Drucker für Einsteiger und Werkstätten.",
    "Creality zeigt Geräte mit Bauraum und Preis. Die Drucker sind kostenpflichtig.",
    ["3D-Drucker", "Unterschiedliche Bauräume", "Kostenpflichtige Geräte"],
    ["Einen Einsteigerdrucker zu vergleichen", "Den Bauraum eines Modells nachzulesen"], True)
add("Shelly", "https://www.shelly.com/", "shelly.com", "paid", "proprietary", ["automatisierung"],
    "Shelly schaltet Stromkreise und misst Verbrauch über WLAN.",
    "Shelly-Module sitzen hinter dem Schalter oder in der Dose und lassen sich lokal oder per App ansprechen. Die Geräte sind kostenpflichtig.",
    ["Schalten und Messen über WLAN", "Einbau hinter dem Schalter", "Kostenpflichtige Geräte"],
    ["Eine Lampe per WLAN zu schalten", "Den Verbrauch eines Kreises zu messen"], False)
add("Philips Hue", "https://www.philips-hue.com/", "philips-hue.com", "paid", "proprietary", ["automatisierung"],
    "Philips Hue steuert Lampen über eine Bridge und eine App.",
    "Hue setzt Farben und Zeitpläne für angebundene Leuchten. Die Lampen und die Bridge sind kostenpflichtig.",
    ["Lampen mit Farbe und Zeitplan", "Bridge und App", "Kostenpflichtige Geräte"],
    ["Eine Lampe zeitgesteuert zu schalten", "Eine Farbe für einen Raum zu setzen"], True)
add("Netatmo", "https://www.netatmo.com/", "netatmo.com", "paid", "proprietary", ["automatisierung"],
    "Netatmo misst Wetter, Luft und Heizung im Haus.",
    "Netatmo stellt Stationen und Thermostate bereit und zeigt die Werte in einer App. Die Geräte sind kostenpflichtig. Der Hersteller sitzt in Frankreich.",
    ["Wetter, Luft und Heizung", "Werte in der App", "Kostenpflichtige Geräte"],
    ["Die Luft in einem Raum zu messen", "Eine Heizung nach Zeit zu regeln"], False)
add("Zigbee2MQTT", "https://www.zigbee2mqtt.io/", "zigbee2mqtt.io", "free", "unknown", ["automatisierung"],
    "Zigbee2MQTT bindet Zigbee-Geräte an einen MQTT-Broker.",
    "Die Software spricht Leuchten und Sensoren an, ohne die Cloud des Herstellers. Eine OSI-Kennung wird hier nicht erneut eingetragen. Sie ist ohne Pflichtabo erhältlich.",
    ["Zigbee ohne Hersteller-Cloud", "Anbindung an MQTT", "Nutzung ohne Pflichtabo"],
    ["Eine Lampe lokal anzubinden", "Sensoren an den eigenen Broker zu hängen"], False)
add("openHAB", "https://www.openhab.org/", "openhab.org", "free", "unknown", ["automatisierung"],
    "openHAB steuert Geräte im Haus auf dem eigenen Server.",
    "openHAB verbindet unterschiedliche Systeme und legt Regeln an. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Steuerung auf dem eigenen Server", "Regeln über mehrere Systeme", "Nutzung ohne Pflichtabo"],
    ["Lampen und Sensoren selbst zu verbinden", "Eine Regel ohne Cloud zu bauen"], False)
add("Wiki.js", "https://js.wiki/", "js.wiki", "free", "unknown", ["produktivitaet"],
    "Wiki.js betreibt ein Wiki auf dem eigenen Server.",
    "Wiki.js speichert Seiten und lässt sie im Team bearbeiten. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Wiki auf dem eigenen Server", "Bearbeitung im Team", "Nutzung ohne Pflichtabo"],
    ["Ein internes Wiki selbst zu hosten", "Eine Seite im Team fortzuschreiben"], False)
add("MediaWiki", "https://www.mediawiki.org/", "mediawiki.org", "free", "unknown", ["produktivitaet", "bildung"],
    "MediaWiki ist die Software hinter Wikipedia und lässt sich selbst betreiben.",
    "MediaWiki legt Seiten mit Versionen an. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Seiten mit Versionen", "Selbstbetrieb", "Nutzung ohne Pflichtabo"],
    ["Ein Wiki selbst zu betreiben", "Die Geschichte einer Seite zu sehen"], False)
add("GitBook", "https://www.gitbook.com/", "gitbook.com", "freemium", "proprietary", ["produktivitaet"],
    "GitBook schreibt Dokumentation und interne Handbücher.",
    "GitBook legt Seiten in einer Hierarchie an und kann sie veröffentlichen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Dokumentation in Hierarchien", "Veröffentlichen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Handbuch zu schreiben", "Eine Dokumentation zu veröffentlichen"], True)
add("R Project", "https://www.r-project.org/", "r-project.org", "free", "unknown", ["daten", "programmierung"],
    "R ist eine Sprache für Statistik und Grafiken.",
    "Das R Project stellt die Sprache und Pakete für Auswertungen bereit. Eine einzelne OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Statistik und Grafiken", "Pakete", "Nutzung ohne Pflichtabo"],
    ["Eine Auswertung zu rechnen", "Eine Grafik aus einer Tabelle zu zeichnen"], False)
add("Kotlin", "https://kotlinlang.org/", "kotlinlang.org", "free", "unknown", ["programmierung"],
    "Kotlin ist eine Programmiersprache für Anwendungen, auch auf Android.",
    "kotlinlang.org stellt Compiler, Dokumentation und den Einstieg bereit. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Werkzeuge sind ohne Pflichtabo erhältlich.",
    ["Sprache für Anwendungen", "Dokumentation", "Nutzung ohne Pflichtabo"],
    ["Eine Anwendung in Kotlin zu schreiben", "Den Einstieg in der Dokumentation zu lesen"], False)
add("PHP", "https://www.php.net/", "php.net", "free", "unknown", ["programmierung"],
    "PHP ist eine Sprache, mit der viele Websites auf dem Server laufen.",
    "php.net stellt die Sprache und die Funktionsreferenz bereit. Eine OSI-Kennung wird hier nicht erneut eingetragen. Der Interpreter ist ohne Pflichtabo erhältlich.",
    ["Sprache für Websites", "Funktionsreferenz", "Nutzung ohne Pflichtabo"],
    ["Eine Seite auf dem Server zu erzeugen", "Eine Funktion in der Referenz nachzuschlagen"], True)
add("PyPI", "https://pypi.org/", "pypi.org", "free", "unknown", ["programmierung"],
    "PyPI verteilt Pakete für die Sprache Python.",
    "Der Python Package Index zeigt Beschreibungen und Versionen und liefert die Dateien an pip. Die Suche ist ohne Konto möglich. Eine OSI-Kennung des Index wird hier nicht eingetragen.",
    ["Pakete für Python", "Versionen und Dateien", "Suche ohne Konto"],
    ["Ein Paket zu finden", "Die aktuelle Version nachzusehen"], True)
add("Flathub", "https://flathub.org/", "flathub.org", "free", "unknown", ["programmierung"],
    "Flathub verteilt Anwendungen als Flatpak für den Linux-Desktop.",
    "Flathub listet Programme und installiert sie in einer eigenen Umgebung. Die Suche ist ohne Konto möglich. Eine OSI-Kennung des Katalogs wird hier nicht eingetragen.",
    ["Anwendungen als Flatpak", "Eigene Umgebung je App", "Suche ohne Konto"],
    ["Eine Desktop-Anwendung zu installieren", "Ein Programm unabhängig von der Distribution zu beziehen"], True)
add("NixOS", "https://nixos.org/", "nixos.org", "free", "unknown", ["programmierung"],
    "NixOS ist ein Linux-System, dessen Aufbau in einer Konfiguration steht.",
    "NixOS beschreibt Pakete und Dienste deklarativ und kann einen Stand zurücksetzen. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das System ist ohne Pflichtabo erhältlich.",
    ["Deklarative Konfiguration", "Zurücksetzen eines Stands", "Nutzung ohne Pflichtabo"],
    ["Einen Server aus einer Konfigurationsdatei zu bauen", "Einen Stand zurückzusetzen"], False)
add("Ansible", "https://www.ansible.com/", "ansible.com", "freemium", "unknown", ["programmierung", "automatisierung"],
    "Ansible richtet Server nach einer Beschreibung ein, ohne einen Agenten.",
    "Ansible spielt Playbooks über SSH auf Maschinen. Eine OSI-Kennung der aktuellen Ausgabe wird hier nicht eingetragen. Die Engine ist ohne Pflichtabo erhältlich, Automation Controller ist bezahlt.",
    ["Einrichtung über SSH", "Playbooks", "Engine ohne Pflichtabo"],
    ["Mehrere Server gleich einzurichten", "Einen Ablauf zu wiederholen"], False)
add("Terraform", "https://www.terraform.io/", "terraform.io", "freemium", "unknown", ["programmierung"],
    "Terraform beschreibt Infrastruktur als Datei und legt sie an.",
    "Terraform plant Änderungen an Servern und Netzen und führt sie aus. Die Lizenz der aktuellen Ausgabe ist keine durchgängig bestätigte OSI-Lizenz, der Lizenztyp bleibt Unbekannt. Es gibt die Engine und bezahlte Team-Funktionen.",
    ["Infrastruktur als Datei", "Plan und Ausführung", "Lizenz nicht als OSI geführt"],
    ["Einen Server aus einer Datei anzulegen", "Eine Änderung vor dem Anwenden zu sehen"], False)
add("OpenTofu", "https://opentofu.org/", "opentofu.org", "free", "unknown", ["programmierung"],
    "OpenTofu beschreibt Infrastruktur als Datei, hervorgegangen aus Terraform.",
    "OpenTofu liest Konfigurationen und legt Ressourcen an. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Infrastruktur als Datei", "Anlegen von Ressourcen", "Nutzung ohne Pflichtabo"],
    ["Eine Infrastruktur ohne die Terraform-Lizenz zu bauen", "Einen Plan vor dem Anwenden zu lesen"], False)
add("Helm", "https://helm.sh/", "helm.sh", "free", "unknown", ["programmierung"],
    "Helm packt Anwendungen für Kubernetes in Charts.",
    "Helm installiert und aktualisiert eine Anwendung anhand eines Charts. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Charts für Kubernetes", "Installation und Update", "Nutzung ohne Pflichtabo"],
    ["Eine Anwendung in ein Cluster zu spielen", "Ein Chart zu aktualisieren"], False)
add("Jenkins", "https://www.jenkins.io/", "jenkins.io", "free", "unknown", ["programmierung", "automatisierung"],
    "Jenkins baut und prüft Software, sobald sich der Code ändert.",
    "Jenkins führt Jobs auf dem eigenen Server aus. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Builds bei Codeänderung", "Eigener Server", "Nutzung ohne Pflichtabo"],
    ["Einen Build nach jedem Push zu starten", "Einen Job auf dem eigenen Server zu betreiben"], False)
add("Git", "https://git-scm.com/", "git-scm.com", "free", "unknown", ["programmierung"],
    "Git merkt sich Versionen eines Projekts und Zweige davon.",
    "Git speichert Änderungen lokal und kann sie mit einem Server abgleichen. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Versionen und Zweige", "Abgleich mit einem Server", "Nutzung ohne Pflichtabo"],
    ["Den Verlauf eines Projekts zu sichern", "Einen Zweig für eine Änderung anzulegen"], True)
add("Node.js", "https://nodejs.org/", "nodejs.org", "free", "unknown", ["programmierung"],
    "Node.js führt JavaScript außerhalb des Browsers aus.",
    "Node.js stellt die Laufzeit und einen Paketmanager bereit. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Laufzeit ist ohne Pflichtabo erhältlich.",
    ["JavaScript auf dem Server", "Paketmanager", "Nutzung ohne Pflichtabo"],
    ["Ein Skript außerhalb des Browsers zu starten", "Eine kleine Webanwendung zu betreiben"], True)
add("Vite", "https://vitejs.dev/", "vitejs.dev", "free", "unknown", ["programmierung"],
    "Vite startet eine Entwicklungsumgebung für Weboberflächen und baut sie für die Auslieferung.",
    "Vite lädt Module beim Entwickeln schnell nach und erzeugt ein Bundle. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Entwicklungsserver", "Bundle für die Auslieferung", "Nutzung ohne Pflichtabo"],
    ["Eine Oberfläche lokal zu starten", "Ein Projekt für die Veröffentlichung zu bauen"], False)
add("Astro", "https://astro.build/", "astro.build", "freemium", "unknown", ["programmierung", "design"],
    "Astro baut inhaltslastige Websites und schickt wenig JavaScript an den Browser.",
    "Astro mischt Seiten und Komponenten und kann sie statisch ausliefern. Eine OSI-Kennung wird hier nicht eingetragen. Das Framework ist ohne Pflichtabo erhältlich, die Plattform hat bezahlte Stufen.",
    ["Inhaltslastige Websites", "Wenig JavaScript im Browser", "Framework ohne Pflichtabo"],
    ["Eine Dokumentationsseite zu bauen", "Eine Website statisch auszuliefern"], False)
add("Svelte", "https://svelte.dev/", "svelte.dev", "free", "unknown", ["programmierung"],
    "Svelte beschreibt Oberflächen, die der Compiler in schlankes JavaScript übersetzt.",
    "Svelte schreibt Komponenten und erzeugt daraus den Code für den Browser. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Framework ist ohne Pflichtabo erhältlich.",
    ["Komponenten", "Compiler statt Laufzeitbibliothek", "Nutzung ohne Pflichtabo"],
    ["Eine Oberfläche mit wenig Laufzeit zu bauen", "Eine Komponente zu schreiben"], False)
add("Vue", "https://vuejs.org/", "vuejs.org", "free", "unknown", ["programmierung"],
    "Vue baut Oberflächen aus Komponenten im Browser.",
    "Vue verbindet Vorlage und Daten einer Komponente. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Framework ist ohne Pflichtabo erhältlich.",
    ["Komponenten", "Vorlage und Daten", "Nutzung ohne Pflichtabo"],
    ["Eine Oberfläche in Komponenten zu teilen", "Daten an eine Vorlage zu binden"], True)
add("React", "https://react.dev/", "react.dev", "free", "unknown", ["programmierung"],
    "React beschreibt Oberflächen als Funktionen, die bei Datenänderung neu zeichnen.",
    "Die Dokumentation auf react.dev erklärt Komponenten und den Abgleich mit dem Browser. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Bibliothek ist ohne Pflichtabo erhältlich.",
    ["Komponenten als Funktionen", "Abgleich mit dem Browser", "Nutzung ohne Pflichtabo"],
    ["Eine Oberfläche in Komponenten zu zerlegen", "Die Dokumentation zu einem Hook zu lesen"], False)
add("htmx", "https://htmx.org/", "htmx.org", "free", "unknown", ["programmierung"],
    "htmx lässt HTML selbst Anfragen auslösen und Teile der Seite ersetzen.",
    "htmx hängt Attribute an Elemente, die einen Ausschnitt vom Server nachladen. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Bibliothek ist ohne Pflichtabo erhältlich.",
    ["Anfragen aus HTML", "Ersetzen von Ausschnitten", "Nutzung ohne Pflichtabo"],
    ["Ein Formular ohne eigenes JavaScript nachzuladen", "Einen Ausschnitt der Seite zu ersetzen"], False)
add("Tailwind CSS", "https://tailwindcss.com/", "tailwindcss.com", "freemium", "unknown", ["design", "programmierung"],
    "Tailwind setzt das Aussehen über viele kleine Klassen im HTML.",
    "Tailwind erzeugt aus den genutzten Klassen eine CSS-Datei. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Framework ist ohne Pflichtabo erhältlich, UI-Baukasten und Plus sind bezahlt.",
    ["Kleine Klassen im HTML", "Erzeugte CSS-Datei", "Framework ohne Pflichtabo"],
    ["Eine Seite ohne eigene CSS-Datei zu gestalten", "Abstände und Farben über Klassen zu setzen"], False)
add("Firefox", "https://www.mozilla.org/de/firefox/", "mozilla.org", "free", "unknown", ["recherche"],
    "Firefox ist ein Browser der Mozilla Foundation mit Tracking-Schutz.",
    "Firefox öffnet Seiten und blockiert in der Voreinstellung bekannte Tracker. Eine OSI-Kennung wird hier nicht erneut eingetragen. Der Browser ist ohne Abo erhältlich.",
    ["Browser mit Tracking-Schutz", "Deutsche Seite von Mozilla", "Nutzung ohne Abo"],
    ["Seiten mit weniger Trackern zu öffnen", "Einen Browser ohne Abo zu nutzen"], True)
add("Tor Browser", "https://www.torproject.org/", "torproject.org", "free", "unknown", ["recherche"],
    "Der Tor Browser leitet Seitenaufrufe über das Tor-Netz.",
    "Das Tor Project stellt den Browser bereit, der Anfragen über mehrere Stationen schickt. Eine OSI-Kennung wird hier nicht erneut eingetragen. Der Browser ist ohne Abo erhältlich.",
    ["Aufrufe über das Tor-Netz", "Browser des Tor Project", "Nutzung ohne Abo"],
    ["Eine Seite über das Tor-Netz zu öffnen", "Die Dokumentation des Projekts zu lesen"], False)
add("tagesschau", "https://www.tagesschau.de/", "tagesschau.de", "free", "proprietary", ["recherche"],
    "Die tagesschau veröffentlicht Nachrichten des öffentlich-rechtlichen Rundfunks.",
    "tagesschau.de zeigt Meldungen, die ohne Abo lesbar sind. Das Angebot kommt von der ARD.",
    ["Nachrichten der ARD", "Meldungen ohne Abo", "Öffentlich-rechtliches Angebot"],
    ["Eine Meldung des Tages zu lesen", "Ein Thema in der Übersicht zu sehen"], True)
add("Handelsblatt", "https://www.handelsblatt.com/", "handelsblatt.com", "freemium", "proprietary", ["recherche", "finanzen"],
    "Das Handelsblatt berichtet über Wirtschaft und Unternehmen.",
    "Ein Teil der Meldungen ist frei, längere Analysen liegen hinter einem kostenpflichtigen Zugang. Der Verlag sitzt in Düsseldorf.",
    ["Wirtschaftsnachrichten", "Freie Meldungen und kostenpflichtige Analysen", "Verlag aus Düsseldorf"],
    ["Eine Meldung zu einem Unternehmen zu lesen", "Eine Analyse einzuordnen"], True)
add("FRITZ!Box", "https://www.fritz.com/", "fritz.com", "paid", "proprietary", ["programmierung"],
    "AVM verkauft FRITZ!Box-Router und das System FRITZ!OS.",
    "Die FRITZ!Box stellt WLAN, Telefonie und ein Heimnetz bereit. Der Hersteller sitzt in Berlin. Die Geräte sind kostenpflichtig.",
    ["WLAN, Telefonie und Heimnetz", "Hersteller aus Berlin", "Kostenpflichtige Geräte"],
    ["Einen Router für zu Hause auszuwählen", "Das Heimnetz einzurichten"], True)
add("IONOS", "https://www.ionos.de/", "ionos.de", "paid", "proprietary", ["design"],
    "IONOS vermietet Domains, Hosting und Server.",
    "IONOS legt Seiten, Mail und Domains an. Der Anbieter sitzt in Deutschland. Die Pakete sind kostenpflichtig.",
    ["Domains, Hosting und Server", "Mail", "Kostenpflichtige Pakete"],
    ["Eine Domain mit Webspace zu mieten", "Mail zur Domain einzurichten"], True)
add("Cloudflare", "https://www.cloudflare.com/", "cloudflare.com", "freemium", "proprietary", ["programmierung"],
    "Cloudflare stellt DNS, Schutz und Auslieferung für Websites bereit.",
    "Cloudflare schaltet eine Domain davor und kann Inhalte zwischenspeichern. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["DNS und Auslieferung", "Schutz davor", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Website über Cloudflare zu schalten", "DNS einer Domain zu verwalten"], False)
add("Docker", "https://www.docker.com/", "docker.com", "freemium", "proprietary", ["programmierung"],
    "Docker packt Anwendungen in Container und startet sie gleich auf jedem Rechner.",
    "Docker baut Images und startet sie lokal oder in einer Registry. Es gibt eine kostenlose Desktop-Nutzung für viele Fälle und bezahlte Team-Pläne. Die Marke und die gehosteten Dienste sind proprietär.",
    ["Container aus Images", "Lokaler Start und Registry", "Kostenlose Desktop-Nutzung und bezahlte Pläne"],
    ["Eine Anwendung in einem Container zu starten", "Ein Image zu bauen"], False)
add("audiotranskription", "https://www.audiotranskription.de/", "audiotranskription.de", "freemium", "proprietary", ["audio-und-sprache", "recherche"],
    "audiotranskription liefert f4 und f5 zum Abtippen von Interviews.",
    "Die Programme spielen Audio langsam ab und setzen Zeitmarken in den Text. Der Anbieter sitzt in Marburg. Es gibt Testversionen und kostenpflichtige Lizenzen.",
    ["Langsames Abspielen", "Zeitmarken im Text", "Testversion und kostenpflichtige Lizenzen"],
    ["Ein Interview abzutippen", "Eine Stelle im Ton wiederzufinden"], False)
add("Alexander von Humboldt-Stiftung", "https://www.humboldt-foundation.de/", "humboldt-foundation.de", "free", "proprietary", ["bildung", "recherche"],
    "Die Humboldt-Stiftung vergibt Stipendien für Forschende aus dem Ausland und aus Deutschland.",
    "Die Stiftung beschreibt Programme und Fristen. Die Informationsseiten sind ohne Konto lesbar. Ein Stipendium setzt einen Antrag voraus.",
    ["Stipendien für Forschende", "Programme und Fristen", "Informationen ohne Konto"],
    ["Ein Programm für einen Forschungsaufenthalt zu finden", "Eine Frist nachzulesen"], True)
add("BAföG-Rechner", "https://www.bafoeg-rechner.de/", "bafoeg-rechner.de", "free", "proprietary", ["bildung", "finanzen"],
    "Der BAföG-Rechner schätzt den möglichen Anspruch auf Ausbildungsförderung.",
    "Die Seite rechnet aus eingegebenen Angaben eine Orientierung. Die Nutzung des Rechners ist ohne Konto möglich. Der Antrag selbst läuft über das Amt.",
    ["Schätzung des BAföG", "Orientierung aus Angaben", "Nutzung ohne Konto"],
    ["Einen möglichen Anspruch grob zu schätzen", "Zu sehen, welche Angaben zählen"], True)
add("Formlabs", "https://www.formlabs.com/de/", "formlabs.com", "paid", "proprietary", ["dreid"],
    "Formlabs verkauft Kunstharz-Drucker für feine Teile.",
    "Formlabs liefert Drucker, die mit flüssigem Harz arbeiten, und die passenden Materialien. Die Geräte sind kostenpflichtig.",
    ["Kunstharz-Drucker", "Materialien", "Kostenpflichtige Geräte"],
    ["Einen Drucker für feine Teile einzuordnen", "Ein Material nachzulesen"], False)
add("Tagesschau Platzhalter", "https://www.tagesschau.de/", "tagesschau.de", "free", "proprietary", ["recherche"],
    "Platzhalter.", "Platzhalter.", ["x"], ["x"])


def validate(entries):
    entries[:] = [e for e in entries if "Platzhalter" not in e["name"] and e["name"] not in {"Duolingo", "Khan Academy", "BMBF"}]
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
        raise SystemExit("\n".join(errors[:25]))
    return entries


if __name__ == "__main__":
    rows = validate(E)
    out = ROOT / "data" / "verified-tools-batch10.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows), "->", out)
