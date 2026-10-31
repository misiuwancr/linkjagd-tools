#!/usr/bin/env python3
"""Siebzehnte Liste: bekannte Web-Apps, die HTTP 200 geliefert haben."""

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


add("Read AI", "https://www.read.ai/", "read.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "Read AI schreibt Meetings mit und fasst sie zusammen.",
    "Read AI nimmt am Gespräch teil und liefert Notizen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Meeting-Notizen", "Zusammenfassung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Gespräch mitzuschreiben", "Die Zusammenfassung zu teilen"], True)
add("Tactiq", "https://www.tactiq.io/", "tactiq.io", "freemium", "proprietary", ["audio-und-sprache"],
    "Tactiq schreibt Videogespräche im Browser mit.",
    "Tactiq läuft als Erweiterung und liefert ein Transkript. Es gibt einen kostenlosen Einstieg und bezahlte Minuten.",
    ["Transkript im Browser", "Erweiterung", "Kostenloser Einstieg und bezahlte Minuten"],
    ["Ein Meeting live mitzuschreiben", "Das Transkript zu exportieren"], True)
add("MeetGeek", "https://www.meetgeek.ai/", "meetgeek.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "MeetGeek zeichnet Meetings auf und zieht Aufgaben daraus.",
    "MeetGeek liefert Transkript, Zusammenfassung und Aufgaben. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Transkript und Aufgaben", "Zusammenfassung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Aufgaben aus einem Meeting zu ziehen", "Die Aufnahme später zu durchsuchen"], False)
add("Circleback", "https://www.circleback.ai/", "circleback.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "Circleback schreibt Meetings mit und legt Notizen automatisch ab.",
    "Circleback nimmt das Gespräch auf und verteilt die Notizen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Automatische Meeting-Notizen", "Verteilen der Notizen", "Einstieg und bezahlte Stufen"],
    ["Notizen ohne manuelles Tippen zu bekommen", "Ein Gespräch später nachzulesen"], False)
add("Fellow", "https://www.fellow.app/", "fellow.app", "freemium", "proprietary", ["produktivitaet"],
    "Fellow plant Meetings und hält Agenda und Notizen an einem Ort.",
    "Fellow verbindet Kalender, Agenda und Protokoll. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Agenda und Notizen", "Kalender", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Agenda vor dem Meeting zu teilen", "Beschlüsse festzuhalten"], False)
add("Noota", "https://www.noota.io/", "noota.io", "freemium", "proprietary", ["audio-und-sprache"],
    "Noota schreibt Meetings und Telefonate mit.",
    "Noota liefert Transkript und Zusammenfassung. Es gibt einen kostenlosen Einstieg und bezahlte Minuten.",
    ["Transkript von Gesprächen", "Zusammenfassung", "Kostenloser Einstieg und bezahlte Minuten"],
    ["Ein Telefonat abzutippen", "Die Zusammenfassung zu lesen"], True)
add("Sembly", "https://www.sembly.ai/", "sembly.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "Sembly fasst Meetings zusammen und markiert Aufgaben.",
    "Sembly sitzt im Gespräch und liefert Notizen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Zusammenfassung", "Aufgaben", "Einstieg und bezahlte Stufen"],
    ["Ein langes Meeting auf den Punkt zu bringen", "Aufgaben an Personen zu sehen"], False)
add("Humata", "https://www.humata.ai/", "humata.ai", "freemium", "proprietary", ["recherche"],
    "Humata beantwortet Fragen zu hochgeladenen PDF-Dateien.",
    "Humata liest ein Dokument und zeigt die Stelle zur Antwort. Es gibt einen kostenlosen Einstieg und bezahlte Seiten.",
    ["Fragen an PDFs", "Fundstelle", "Kostenloser Einstieg und bezahlte Seiten"],
    ["Eine Klausel in einem Vertrag zu finden", "Ein langes PDF zu befragen"], True)
add("Explainpaper", "https://www.explainpaper.com/", "explainpaper.com", "freemium", "proprietary", ["recherche", "bildung"],
    "Explainpaper erklärt markierte Stellen in einem wissenschaftlichen PDF.",
    "Explainpaper öffnet ein Paper und beantwortet Fragen zu einer Passage. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Erklärungen zu einer Passage", "PDF eines Papers", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen schwierigen Absatz erklären zu lassen", "Ein Paper abschnittsweise zu lesen"], True)
add("ChatDoc", "https://www.chatdoc.com/", "chatdoc.com", "freemium", "proprietary", ["recherche"],
    "ChatDoc beantwortet Fragen zu Dokumenten und Tabellen.",
    "ChatDoc nimmt Dateien entgegen und verweist auf die Stelle. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Fragen an Dokumente", "Verweis auf die Stelle", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Eine Zahl in einem Bericht zu finden", "Mehrere Dateien zu befragen"], True)
add("PDF.ai", "https://pdf.ai/", "pdf.ai", "freemium", "proprietary", ["recherche"],
    "PDF.ai lässt Fragen an eine hochgeladene PDF-Datei stellen.",
    "PDF.ai liest die Datei und antwortet im Chat. Es gibt einen kostenlosen Einstieg und bezahlte Dokumente.",
    ["Chat mit einer PDF", "Upload", "Kostenloser Einstieg und bezahlte Dokumente"],
    ["Ein Handbuch zu durchsuchen", "Eine Antwort mit der Stelle zu prüfen"], True)
add("Tally", "https://tally.so/", "tally.so", "freemium", "proprietary", ["produktivitaet"],
    "Tally baut Formulare, die sich wie ein Dokument anfühlen.",
    "Tally setzt Fragen untereinander und sammelt die Antworten. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Formulare wie ein Dokument", "Gesammelte Antworten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Anmeldung zu bauen", "Antworten zu exportieren"], True)
add("Fillout", "https://www.fillout.com/", "fillout.com", "freemium", "proprietary", ["produktivitaet"],
    "Fillout baut Formulare und verbindet sie mit Tabellen.",
    "Fillout setzt Fragen und schreibt Antworten in angebundene Dienste. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Formulare", "Anbindung an Tabellen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Formular an eine Tabelle zu hängen", "Antworten an einem Ort zu sehen"], True)
add("Typeform", "https://www.typeform.com/", "typeform.com", "freemium", "proprietary", ["produktivitaet"],
    "Typeform zeigt Fragen nacheinander in einem Gesprächsformular.",
    "Typeform führt durch eine Frage nach der anderen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Eine Frage nach der anderen", "Gesprächsformular", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Umfrage zu gestalten", "Eine Anmeldung Schritt für Schritt abzufragen"], True)
add("Jotform", "https://www.jotform.com/", "jotform.com", "freemium", "proprietary", ["produktivitaet"],
    "Jotform baut Formulare mit vielen Feldtypen und sammelt die Einsendungen.",
    "Jotform setzt Felder per Drag-and-drop und speichert die Antworten. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Viele Feldtypen", "Gespeicherte Einsendungen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Bewerbungsformular zu bauen", "Einsendungen als Tabelle zu sehen"], True)
add("SurveyMonkey", "https://www.surveymonkey.com/", "surveymonkey.com", "freemium", "proprietary", ["produktivitaet"],
    "SurveyMonkey erstellt Umfragen und wertet die Antworten aus.",
    "SurveyMonkey verteilt einen Fragebogen und zeigt Diagramme. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Fragebögen", "Auswertung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Umfrage zu verschicken", "Antworten in Diagrammen zu sehen"], True)
add("Bubble", "https://bubble.io/", "bubble.io", "freemium", "proprietary", ["design", "programmierung"],
    "Bubble baut Web-Apps im Browser, ohne den Code selbst zu schreiben.",
    "Bubble setzt Seiten, Daten und Abläufe visuell. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Web-Apps ohne eigenen Code", "Daten und Abläufe", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine kleine App zu starten", "Einen Ablauf visuell zu setzen"], False)
add("FlutterFlow", "https://www.flutterflow.io/", "flutterflow.io", "freemium", "proprietary", ["programmierung"],
    "FlutterFlow gestaltet App-Oberflächen und erzeugt daraus ein Flutter-Projekt.",
    "FlutterFlow setzt Screens und exportiert den Code. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["App-Oberflächen", "Export als Flutter-Projekt", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen App-Screen zu gestalten", "Das Projekt weiter in Flutter zu öffnen"], False)
add("Softr", "https://www.softr.io/", "softr.io", "freemium", "proprietary", ["design"],
    "Softr macht aus einer Tabelle eine Website mit Anmeldung.",
    "Softr setzt Seiten auf Daten und veröffentlicht sie. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Website aus einer Tabelle", "Anmeldung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Verzeichnis aus einer Tabelle zu bauen", "Eine Seite mit Login zu veröffentlichen"], True)
add("Glide", "https://www.glideapps.com/", "glideapps.com", "freemium", "proprietary", ["programmierung"],
    "Glide macht aus einer Tabelle eine App fürs Handy und den Browser.",
    "Glide liest Zeilen als Einträge und setzt Listen und Formulare. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["App aus einer Tabelle", "Listen und Formulare", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine einfache App ohne Code zu starten", "Einträge aus einer Tabelle anzuzeigen"], True)
add("Adalo", "https://www.adalo.com/", "adalo.com", "freemium", "proprietary", ["programmierung"],
    "Adalo baut Apps aus Komponenten und veröffentlicht sie.",
    "Adalo setzt Screens und Daten visuell. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Apps aus Komponenten", "Visuelle Daten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine kleine App zu skizzieren", "Screens miteinander zu verbinden"], False)
add("Fibery", "https://fibery.io/", "fibery.io", "freemium", "proprietary", ["produktivitaet"],
    "Fibery legt Arbeit in eigenen Datenbanken, Dokumenten und Ansichten ab.",
    "Fibery verbindet Aufgaben, Texte und Felder. Es gibt einen kostenlosen Einstieg und bezahlte Plätze.",
    ["Eigene Datenbanken", "Dokumente und Ansichten", "Kostenloser Einstieg und bezahlte Plätze"],
    ["Ein Produktboard selbst zu modellieren", "Aufgaben und Notizen zu verknüpfen"], False)
add("Shortcut", "https://www.shortcut.com/", "shortcut.com", "freemium", "proprietary", ["produktivitaet"],
    "Shortcut plant Stories, Iterationen und Dokumente für Softwareteams.",
    "Shortcut hält Aufgaben auf einem Board und in Iterationen. Es gibt einen kostenlosen Einstieg und bezahlte Plätze.",
    ["Stories und Iterationen", "Board", "Kostenloser Einstieg und bezahlte Plätze"],
    ["Eine Iteration zu planen", "Stories einem Board zuzuordnen"], False)
add("Evernote", "https://evernote.com/", "evernote.com", "freemium", "proprietary", ["produktivitaet"],
    "Evernote sammelt Notizen, Scans und Aufgaben in Notizbüchern.",
    "Evernote durchsucht Notizen über Geräte hinweg. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Notizbücher", "Suche über Geräte", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Notiz mit Anhang abzulegen", "Ein Notizbuch zu durchsuchen"], True)
add("OmniFocus", "https://www.omnifocus.com/", "omnifocus.com", "paid", "proprietary", ["produktivitaet"],
    "OmniFocus sortiert Aufgaben nach Projekten, Kontexten und Fristen.",
    "OmniFocus ist eine Aufgaben-App mit Perspektiven auf das, was als Nächstes ansteht. Die Nutzung ist kostenpflichtig.",
    ["Projekte und Kontexte", "Perspektiven", "Kostenpflichtige Nutzung"],
    ["Aufgaben nach Kontext zu filtern", "Eine Wochenplanung zu bauen"], False)
add("Causal", "https://www.causal.app/", "causal.app", "freemium", "proprietary", ["produktivitaet"],
    "Causal rechnet Modelle und Szenarien statt einer klassischen Tabelle.",
    "Causal setzt Formeln als Modell und zeigt Szenarien. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Modelle und Szenarien", "Formeln", "Einstieg und bezahlte Stufen"],
    ["Ein Umsatzmodell mit Varianten zu rechnen", "Ein Szenario gegen ein anderes zu halten"], False)
add("Equals", "https://equals.com/", "equals.com", "freemium", "proprietary", ["produktivitaet"],
    "Equals verbindet eine Tabelle mit Live-Daten aus anderen Diensten.",
    "Equals zieht Zahlen in Zellen und rechnet damit. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Tabelle mit Live-Daten", "Berechnungen", "Einstieg und bezahlte Stufen"],
    ["Kennzahlen ohne manuellen Export zu sehen", "Eine Tabelle an eine Quelle zu hängen"], False)
add("Clay", "https://www.clay.com/", "clay.com", "freemium", "proprietary", ["marketing"],
    "Clay sammelt Firmendaten und reichert Listen mit weiteren Angaben an.",
    "Clay zieht Zeilen aus Quellen und ergänzt Felder. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Listen von Firmen", "Angereicherte Felder", "Einstieg und bezahlte Kontingente"],
    ["Eine Kontaktliste anzureichern", "Felder aus mehreren Quellen zu füllen"], False)
add("Apollo", "https://www.apollo.io/", "apollo.io", "freemium", "proprietary", ["marketing"],
    "Apollo sucht Kontakte und Firmen und startet E-Mail-Sequenzen.",
    "Apollo filtert eine Datenbank und schreibt Sequenzen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Kontaktsuche", "E-Mail-Sequenzen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Kontakte nach Branche zu filtern", "Eine Sequenz zu starten"], False)
add("Instantly", "https://www.instantly.ai/", "instantly.ai", "freemium", "proprietary", ["marketing"],
    "Instantly verschickt kalte E-Mail-Sequenzen über mehrere Postfächer.",
    "Instantly verteilt den Versand und zeigt Antworten. Es gibt einen Einstieg und bezahlte Stufen.",
    ["E-Mail-Sequenzen", "Mehrere Postfächer", "Einstieg und bezahlte Stufen"],
    ["Eine Sequenz an eine Liste zu schicken", "Antworten an einem Ort zu sehen"], False)
add("Smartlead", "https://www.smartlead.ai/", "smartlead.ai", "freemium", "proprietary", ["marketing"],
    "Smartlead verschickt E-Mail-Kampagnen und wärmt Postfächer an.",
    "Smartlead legt Sequenzen an und verteilt den Versand. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Kampagnen", "Angewärmte Postfächer", "Einstieg und bezahlte Stufen"],
    ["Eine Kampagne über mehrere Postfächer zu fahren", "Antworten zu sehen"], False)
add("beehiiv", "https://www.beehiiv.com/", "beehiiv.com", "freemium", "proprietary", ["marketing"],
    "beehiiv verschickt Newsletter und zeigt, welche Ausgaben gelesen werden.",
    "beehiiv schreibt, sendet und wertet eine Ausgabe aus. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Newsletter", "Auswertung der Ausgaben", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Newsletter zu verschicken", "Zu sehen, welche Links geklickt wurden"], True)
add("Buttondown", "https://buttondown.com/", "buttondown.com", "freemium", "proprietary", ["marketing"],
    "Buttondown verschickt einen Newsletter aus Markdown.",
    "Buttondown nimmt einen Text und sendet ihn an die Liste. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Newsletter aus Markdown", "Liste", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Ausgabe in Markdown zu schreiben", "Die Liste zu exportieren"], True)
add("Substack", "https://substack.com/", "substack.com", "freemium", "proprietary", ["marketing"],
    "Substack veröffentlicht einen Newsletter und optional kostenpflichtige Ausgaben.",
    "Substack schreibt, sendet und kann ein Abo für Leser anbieten. Der Einstieg für Autorinnen und Autoren ist ohne Pflichtgebühr möglich, bezahlte Funktionen kommen dazu.",
    ["Newsletter", "Optionale kostenpflichtige Ausgaben", "Einstieg ohne Pflichtgebühr"],
    ["Eine Ausgabe zu veröffentlichen", "Ein Abo für Leser anzubieten"], True)
add("Typefully", "https://www.typefully.com/", "typefully.com", "freemium", "proprietary", ["marketing"],
    "Typefully schreibt und plant Beiträge für X und LinkedIn.",
    "Typefully zeigt die Vorschau und legt einen Zeitpunkt fest. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Beiträge planen", "Vorschau", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Thread zu entwerfen", "Einen Beitrag auf eine Uhrzeit zu legen"], True)
add("Taplio", "https://www.taplio.com/", "taplio.com", "freemium", "proprietary", ["marketing"],
    "Taplio hilft beim Schreiben und Planen von LinkedIn-Beiträgen.",
    "Taplio schlägt Formulierungen vor und legt den Zeitpunkt fest. Es gibt einen Einstieg und bezahlte Stufen.",
    ["LinkedIn-Beiträge", "Formulierungsvorschläge", "Einstieg und bezahlte Stufen"],
    ["Einen Beitrag zu entwerfen", "Mehrere Posts in der Woche zu planen"], False)
add("Hypefury", "https://www.hypefury.com/", "hypefury.com", "paid", "proprietary", ["marketing"],
    "Hypefury plant Beiträge und verteilt sie über den Tag.",
    "Hypefury nimmt Entwürfe und postet sie nach einem Plan. Die Nutzung ist kostenpflichtig.",
    ["Geplante Beiträge", "Verteilung über den Tag", "Kostenpflichtige Nutzung"],
    ["Eine Woche an Beiträgen vorzuplanen", "Einen Entwurf automatisch zu posten"], False)
add("Tweet Hunter", "https://tweethunter.io/", "tweethunter.io", "freemium", "proprietary", ["marketing"],
    "Tweet Hunter sammelt Ideen und plant Beiträge für X.",
    "Tweet Hunter zeigt Vorlagen und einen Kalender. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Ideen und Vorlagen", "Kalender", "Einstieg und bezahlte Stufen"],
    ["Einen Beitrag aus einer Vorlage zu starten", "Posts für die Woche zu legen"], False)
add("Folk", "https://www.folk.app/", "folk.app", "freemium", "proprietary", ["marketing"],
    "Folk hält Kontakte in einem leichten CRM und an Pipelines.",
    "Folk legt Personen an und zeigt den Stand einer Beziehung. Es gibt einen Einstieg und bezahlte Plätze.",
    ["Leichtes CRM", "Pipelines", "Einstieg und bezahlte Plätze"],
    ["Kontakte ohne ein großes CRM zu führen", "Den Stand einer Anfrage zu sehen"], True)
add("Close", "https://www.close.com/", "close.com", "paid", "proprietary", ["marketing"],
    "Close führt Vertrieb mit Anrufen, Mails und einer Pipeline.",
    "Close legt Leads an und protokolliert Gespräche. Die Nutzung ist kostenpflichtig.",
    ["Pipeline", "Anrufe und Mails", "Kostenpflichtige Nutzung"],
    ["Einen Lead mit dem letzten Gespräch zu sehen", "Eine Mail aus dem CRM zu schicken"], False)
add("Resend", "https://resend.com/", "resend.com", "freemium", "proprietary", ["programmierung"],
    "Resend verschickt transaktionale E-Mails über eine Schnittstelle.",
    "Resend nimmt eine Vorlage und sendet sie an eine Adresse. Es gibt einen kostenlosen Einstieg und bezahlte Mengen.",
    ["Transaktionale E-Mails", "Vorlagen", "Kostenloser Einstieg und bezahlte Mengen"],
    ["Eine Bestätigungsmail zu senden", "Eine Vorlage im Code zu nutzen"], False)
add("Loops", "https://www.loops.so/", "loops.so", "freemium", "proprietary", ["marketing"],
    "Loops verschickt Produktmails und Sequenzen an Nutzerinnen und Nutzer.",
    "Loops legt eine Sequenz an und sendet sie nach einem Ereignis. Es gibt einen kostenlosen Einstieg und bezahlte Kontakte.",
    ["Produktmails", "Sequenzen nach Ereignis", "Kostenloser Einstieg und bezahlte Kontakte"],
    ["Eine Willkommensserie zu starten", "Eine Mail nach einer Anmeldung zu senden"], False)
add("OneSignal", "https://onesignal.com/", "onesignal.com", "freemium", "proprietary", ["marketing"],
    "OneSignal verschickt Push-Nachrichten und E-Mails an App-Nutzer.",
    "OneSignal spricht Geräte und Adressen an. Es gibt einen kostenlosen Einstieg und bezahlte Mengen.",
    ["Push und E-Mail", "Ansprache von Geräten", "Kostenloser Einstieg und bezahlte Mengen"],
    ["Eine Push-Nachricht an eine App zu senden", "Eine Zielgruppe zu wählen"], False)
add("Postmark", "https://postmarkapp.com/", "postmarkapp.com", "freemium", "proprietary", ["programmierung"],
    "Postmark stellt transaktionale E-Mails zu und trennt sie vom Newsletter.",
    "Postmark sendet über eine Schnittstelle und zeigt die Zustellung. Es gibt einen Einstieg und bezahlte Mengen.",
    ["Transaktionale E-Mails", "Zustellbericht", "Einstieg und bezahlte Mengen"],
    ["Eine Passwortmail zuzustellen", "Zu sehen, ob eine Mail angekommen ist"], False)
add("SendGrid", "https://www.sendgrid.com/", "sendgrid.com", "freemium", "proprietary", ["programmierung"],
    "SendGrid verschickt transaktionale Mails und Kampagnen über eine API.",
    "SendGrid nimmt Vorlagen und Adressen entgegen. Es gibt einen kostenlosen Einstieg und bezahlte Mengen.",
    ["API für E-Mails", "Vorlagen", "Kostenloser Einstieg und bezahlte Mengen"],
    ["Eine Mail aus einer Anwendung zu senden", "Eine Vorlage wiederzuverwenden"], False)
add("Hotjar", "https://www.hotjar.com/", "hotjar.com", "freemium", "proprietary", ["marketing"],
    "Hotjar zeigt, wo Leute auf einer Seite klicken, und sammelt Umfragen.",
    "Hotjar zeichnet Sitzungen auf und legt Heatmaps an. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Heatmaps", "Sitzungsaufzeichnungen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Zu sehen, wo eine Seite nicht geklickt wird", "Eine kurze Umfrage einzublenden"], False)
add("FullStory", "https://www.fullstory.com/", "fullstory.com", "freemium", "proprietary", ["marketing"],
    "FullStory zeichnet Sitzungen auf und macht Fehler in der Oberfläche suchbar.",
    "FullStory spielt eine Sitzung nach und filtert nach Ereignissen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Sitzungsaufzeichnung", "Suche nach Ereignissen", "Einstieg und bezahlte Stufen"],
    ["Einen Fehler im Ablauf nachzusehen", "Sitzungen mit einem bestimmten Klick zu finden"], False)
add("LogRocket", "https://logrocket.com/", "logrocket.com", "freemium", "proprietary", ["programmierung"],
    "LogRocket zeichnet Sitzungen auf und zeigt Fehler im Frontend.",
    "LogRocket verbindet eine Session mit der Konsole und dem Netzwerk. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Sitzung und Konsole", "Netzwerk zur Session", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Frontend-Fehler mit der Sitzung zu sehen", "Zu prüfen, welcher Request fehlschlug"], False)
add("Paddle", "https://www.paddle.com/", "paddle.com", "paid", "proprietary", ["e-commerce"],
    "Paddle verkauft Software-Abos und übernimmt die Zahlung und die Steuer.",
    "Paddle legt Preise an und checkt Käufer aus. Die Nutzung ist an Verkäufe gebunden und damit kostenpflichtig.",
    ["Abos für Software", "Zahlung und Steuer", "Nutzung an Verkäufe gebunden"],
    ["Ein Abo für eine Software zu verkaufen", "Die Steuer beim Checkout abzugeben"], False)
add("Lemon Squeezy", "https://www.lemonsqueezy.com/", "lemonsqueezy.com", "freemium", "proprietary", ["e-commerce"],
    "Lemon Squeezy verkauft digitale Produkte und Abos und erstellt die Rechnung.",
    "Lemon Squeezy legt ein Produkt an und übernimmt die Zahlung. Es gibt einen Einstieg und Gebühren je Verkauf.",
    ["Digitale Produkte und Abos", "Rechnung", "Gebühren je Verkauf"],
    ["Ein digitales Produkt zu verkaufen", "Ein Abo mit Rechnung anzubieten"], True)
add("SavvyCal", "https://savvycal.com/", "savvycal.com", "freemium", "proprietary", ["produktivitaet"],
    "SavvyCal legt Termine und zeigt dabei den eigenen Kalender überlagert.",
    "SavvyCal teilt einen Link und blendet belegte Zeiten ein. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Terminlink", "Überlagerter Kalender", "Einstieg und bezahlte Stufen"],
    ["Einen Termin zu vergeben, ohne hin und her zu schreiben", "Belegte Zeiten sichtbar zu machen"], False)
add("TidyCal", "https://tidycal.com/", "tidycal.com", "freemium", "proprietary", ["produktivitaet"],
    "TidyCal vergibt Termine über einen Link mit einer einmaligen Zahlung oder kostenlos.",
    "TidyCal zeigt freie Slots und schreibt den Termin in den Kalender. Es gibt einen kostenlosen Einstieg und eine bezahlte Stufe.",
    ["Terminlink", "Freie Slots", "Kostenloser Einstieg und eine bezahlte Stufe"],
    ["Einen Buchungslink zu teilen", "Termine in den Kalender schreiben zu lassen"], True)
add("Zcal", "https://zcal.co/", "zcal.co", "freemium", "proprietary", ["produktivitaet"],
    "Zcal teilt einen Buchungslink und schreibt den Termin in den Kalender.",
    "Zcal zeigt freie Zeiten und bestätigt die Buchung. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Buchungslink", "Bestätigung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Termin ohne Mailwechsel zu finden", "Eine Buchung bestätigen zu lassen"], True)
add("Dorik", "https://dorik.com/", "dorik.com", "freemium", "proprietary", ["design"],
    "Dorik baut Websites aus Blöcken im Browser.",
    "Dorik setzt Seiten und veröffentlicht sie. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Websites aus Blöcken", "Veröffentlichen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine einfache Seite zu bauen", "Einen Block zu verschieben"], True)
add("Super", "https://super.so/", "super.so", "paid", "proprietary", ["design"],
    "Super veröffentlicht eine Notion-Seite als eigene Website.",
    "Super nimmt eine Notion-Seite und legt eine Domain darüber. Die Nutzung ist kostenpflichtig.",
    ["Notion-Seite als Website", "Eigene Domain", "Kostenpflichtige Nutzung"],
    ["Eine Dokumentationsseite zu veröffentlichen", "Eine Domain auf Notion zu legen"], False)
add("Typedream", "https://typedream.com/", "typedream.com", "freemium", "proprietary", ["design"],
    "Typedream baut eine Website, indem man den Text direkt auf die Seite schreibt.",
    "Typedream mischt Schreiben und Layout. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Schreiben direkt auf der Seite", "Layout", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Landingpage im Textfluss zu bauen", "Eine Seite zu veröffentlichen"], True)
add("Unicorn Platform", "https://unicornplatform.com/", "unicornplatform.com", "freemium", "proprietary", ["design"],
    "Unicorn Platform setzt Landingpages aus fertigen Blöcken.",
    "Unicorn Platform veröffentlicht eine Seite ohne eigenes Frontend. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Landingpages aus Blöcken", "Veröffentlichen", "Einstieg und bezahlte Stufen"],
    ["Eine Produktseite schnell zu setzen", "Einen Block auszutauschen"], True)
add("Drift", "https://www.drift.com/", "drift.com", "freemium", "proprietary", ["kundenservice", "marketing"],
    "Drift legt einen Chat auf die Website und qualifiziert Anfragen.",
    "Drift spricht Besucher an und übergibt ein Gespräch. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Chat auf der Website", "Qualifizierte Anfragen", "Einstieg und bezahlte Stufen"],
    ["Besucher auf einer Seite anzusprechen", "Ein Gespräch an den Vertrieb zu geben"], False)
add("LiveChat", "https://www.livechat.com/", "livechat.com", "paid", "proprietary", ["kundenservice"],
    "LiveChat legt ein Chat-Fenster auf die Website und sammelt die Gespräche.",
    "LiveChat verbindet Besucher mit einem Menschen im Team. Die Nutzung ist kostenpflichtig.",
    ["Chat-Fenster", "Gespräche im Team", "Kostenpflichtige Nutzung"],
    ["Eine Frage auf der Website live zu beantworten", "Ein Gespräch später nachzulesen"], False)
add("Klaviyo", "https://www.klaviyo.com/", "klaviyo.com", "freemium", "proprietary", ["marketing", "e-commerce"],
    "Klaviyo verschickt E-Mails und SMS an Käufer eines Shops.",
    "Klaviyo segmentiert nach dem, was jemand gekauft hat. Es gibt einen kostenlosen Einstieg und bezahlte Kontakte.",
    ["E-Mail und SMS", "Segmente nach Käufen", "Kostenloser Einstieg und bezahlte Kontakte"],
    ["Eine Mail nach einem Kauf zu senden", "Ein Segment der Käufer zu bauen"], False)
add("Customer.io", "https://www.customer.io/", "customer.io", "freemium", "proprietary", ["marketing"],
    "Customer.io sendet Nachrichten, wenn jemand etwas in der App tut.",
    "Customer.io startet eine Mail oder Push nach einem Ereignis. Es gibt einen Einstieg und bezahlte Profile.",
    ["Nachrichten nach Ereignis", "Mail und Push", "Einstieg und bezahlte Profile"],
    ["Eine Mail nach einer Anmeldung zu senden", "Eine Nachricht an ein Segment zu schicken"], False)
add("ActiveCampaign", "https://www.activecampaign.com/", "activecampaign.com", "paid", "proprietary", ["marketing"],
    "ActiveCampaign verbindet E-Mail-Automation mit einem kleinen CRM.",
    "ActiveCampaign startet Strecken nach einem Verhalten. Die Nutzung ist kostenpflichtig.",
    ["E-Mail-Automation", "Kleines CRM", "Kostenpflichtige Nutzung"],
    ["Eine Strecke nach einem Klick zu starten", "Kontakte in einer Pipeline zu sehen"], False)
add("GetResponse", "https://www.getresponse.com/", "getresponse.com", "freemium", "proprietary", ["marketing"],
    "GetResponse verschickt Newsletter und baut dazu einfache Seiten.",
    "GetResponse legt eine Liste, eine Ausgabe und eine Landingpage an. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Newsletter", "Landingpages", "Einstieg und bezahlte Stufen"],
    ["Einen Newsletter zu starten", "Eine Anmeldeseite dazuzusetzen"], True)
add("Omnisend", "https://www.omnisend.com/", "omnisend.com", "freemium", "proprietary", ["marketing", "e-commerce"],
    "Omnisend sendet E-Mails und SMS an Shop-Kunden nach ihrem Verhalten.",
    "Omnisend startet Nachrichten nach einem Warenkorb oder einem Kauf. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["E-Mail und SMS", "Nachrichten nach Verhalten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Mail zu einem offenen Warenkorb zu senden", "Käufer nach einem Kauf anzuschreiben"], False)
add("Woodpecker", "https://www.woodpecker.co/", "woodpecker.co", "paid", "proprietary", ["marketing"],
    "Woodpecker verschickt kalte E-Mail-Sequenzen und stoppt bei einer Antwort.",
    "Woodpecker legt Schritte an und protokolliert Öffnungen. Die Nutzung ist kostenpflichtig.",
    ["Kalte Sequenzen", "Stopp bei Antwort", "Kostenpflichtige Nutzung"],
    ["Eine Folge von Mails zu planen", "Zu sehen, wer geantwortet hat"], False)
add("Productboard", "https://www.productboard.com/", "productboard.com", "freemium", "proprietary", ["produktivitaet"],
    "Productboard sammelt Kundenfeedback und ordnet es Ideen zu.",
    "Productboard zeigt, welche Anfrage zu welchem Feature gehört. Es gibt einen Einstieg und bezahlte Plätze.",
    ["Feedback zu Ideen", "Prioritäten", "Einstieg und bezahlte Plätze"],
    ["Kundenstimmen einem Feature zuzuordnen", "Eine Roadmap aus Feedback zu bauen"], False)
add("Aha", "https://www.aha.io/", "aha.io", "paid", "proprietary", ["produktivitaet"],
    "Aha plant eine Produkt-Roadmap mit Zielen und Features.",
    "Aha legt Ziele, Ideen und einen Zeitplan an. Die Nutzung ist kostenpflichtig.",
    ["Roadmap", "Ziele und Features", "Kostenpflichtige Nutzung"],
    ["Eine Roadmap zu zeichnen", "Ein Feature einem Ziel zuzuordnen"], False)
add("OneNote", "https://www.onenote.com/", "onenote.com", "freemium", "proprietary", ["produktivitaet"],
    "OneNote legt Notizen in Abschnitten und durchsucht sie.",
    "OneNote mischt Text, Bilder und Zeichnungen. Es gibt einen kostenlosen Einstieg über ein Microsoft-Konto und bezahlte Funktionen in Microsoft 365.",
    ["Notizen in Abschnitten", "Text, Bilder, Zeichnungen", "Kostenloser Einstieg und Funktionen in Microsoft 365"],
    ["Eine Vorlesung mitzuschreiben", "Ein Notizbuch zu durchsuchen"], True)


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
        raise SystemExit("\n".join(errors[:30]))
    return entries


if __name__ == "__main__":
    rows = validate(E)
    out = ROOT / "data" / "verified-tools-batch17.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows))
