#!/usr/bin/env python3
"""Fünfte geprüfte Liste. Seiten haben in diesem Lauf mit HTTP 200 geantwortet."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tool(name, url, domain, price, license_type, cats, short, long, features, uses, beginner=False):
    return {
        "name": name,
        "originalUrl": url,
        "domain": domain,
        "pricingModel": price,
        "licenseType": license_type,
        "categorySlugs": cats,
        "shortDescriptionDe": short,
        "longDescriptionDe": long,
        "featuresDe": features,
        "useCasesDe": uses,
        "partnerStatus": "none_found",
        "programPresence": "unknown",
        "programInfoUrl": "",
        "network": "manual",
        "verified": True,
        "beginnerFriendly": beginner,
        "discoverySource": "offizielle-website",
        "oss": None,
    }


E = []


def add(*a, **k):
    E.append(tool(*a, **k))


add("sevdesk", "https://www.sevdesk.de/", "sevdesk.de", "freemium", "proprietary", ["finanzen"],
    "sevdesk schreibt Rechnungen und führt eine Buchhaltung für Selbstständige.",
    "sevdesk legt Angebote, Rechnungen und Belege an und bereitet die Zahlen für die Steuer vor. Der Dienst kommt aus Deutschland. Es gibt einen Test und kostenpflichtige Tarife.",
    ["Rechnungen und Belege", "Vorbereitung für die Steuer", "Test und kostenpflichtige Tarife"],
    ["Eine Rechnung an einen Kunden zu schreiben", "Einnahmen und Ausgaben zu überblicken"], True)
add("weclapp", "https://www.weclapp.com/", "weclapp.com", "paid", "proprietary", ["e-commerce", "produktivitaet"],
    "weclapp verbindet Warenwirtschaft, Shop und Buchhaltung in einer Cloud.",
    "weclapp führt Artikel, Aufträge und Rechnungen in einem System. Der Anbieter sitzt in Marburg. Die Nutzung ist kostenpflichtig.",
    ["Warenwirtschaft und Aufträge", "Rechnungen im selben System", "Kostenpflichtige Nutzung"],
    ["Aufträge und Bestände zusammenzuführen", "Eine Rechnung aus einem Auftrag zu erzeugen"], False)
add("Xentral", "https://www.xentral.com/", "xentral.com", "paid", "proprietary", ["e-commerce"],
    "Xentral steuert Artikel, Bestellungen und Versand für wachsende Händler.",
    "Xentral bündelt Warenwirtschaft, Einkauf und Fulfillment. Der Anbieter kommt aus Augsburg. Die Nutzung ist kostenpflichtig.",
    ["Warenwirtschaft und Fulfillment", "Einkauf und Bestellungen", "Kostenpflichtige Nutzung"],
    ["Bestellungen aus mehreren Kanälen zu steuern", "Bestände und Versand zu verbinden"], False)
add("smartsteuer", "https://www.smartsteuer.de/", "smartsteuer.de", "paid", "proprietary", ["finanzen"],
    "smartsteuer führt durch die Steuererklärung im Browser.",
    "smartsteuer stellt Fragen und füllt daraus die Formulare für das Finanzamt. Der Dienst richtet sich an Deutschland. Die Abgabe ist kostenpflichtig.",
    ["Fragen zur Steuererklärung", "Formulare für das Finanzamt", "Kostenpflichtige Abgabe"],
    ["Eine Erklärung ohne Desktop-Programm zu beginnen", "Angaben vor dem Versand zu prüfen"], True)
add("Steuerbot", "https://www.steuerbot.com/", "steuerbot.com", "paid", "proprietary", ["finanzen"],
    "Steuerbot führt als Chat durch die deutsche Steuererklärung.",
    "Steuerbot stellt die Fragen im Gespräch und erzeugt daraus die Erklärung. Der Dienst kommt aus Deutschland. Die Abgabe ist kostenpflichtig.",
    ["Steuerfragen im Chat", "Erklärung aus den Antworten", "Kostenpflichtige Abgabe"],
    ["Eine Erklärung im Dialog zu starten", "Belege anhand von Fragen zuzuordnen"], True)
add("WISO Steuer", "https://www.wiso-steuer.de/", "wiso-steuer.de", "paid", "proprietary", ["finanzen"],
    "WISO Steuer führt durch die Einkommensteuererklärung für Deutschland.",
    "WISO Steuer prüft Eingaben und gibt Hinweise zu Pauschalen und Belegen. Die Software kommt von Buhl. Die Nutzung ist kostenpflichtig.",
    ["Einkommensteuererklärung", "Hinweise zu Pauschalen", "Kostenpflichtige Software"],
    ["Eine Erklärung mit Prüfinweisen auszufüllen", "Belege einer Steuererklärung zuzuordnen"], True)
add("Stiftung Warentest", "https://www.stiftung-warentest.de/", "stiftung-warentest.de", "freemium", "proprietary", ["recherche"],
    "Stiftung Warentest veröffentlicht unabhängige Tests von Produkten und Diensten.",
    "Die Stiftung prüft Waren und Finanzprodukte und veröffentlicht die Ergebnisse. Ein Teil der Meldungen ist frei lesbar, ausführliche Tests sind kostenpflichtig.",
    ["Unabhängige Produkttests", "Tests zu Finanzen und Waren", "Freie Meldungen und kostenpflichtige Tests"],
    ["Einen Test vor einem Kauf zu lesen", "Produkte einer Kategorie zu vergleichen"], True)
add("Öko-Test", "https://www.oekotest.de/", "oekotest.de", "freemium", "proprietary", ["recherche", "gesundheit"],
    "Öko-Test untersucht Produkte auf Schadstoffe und Nutzen.",
    "Öko-Test veröffentlicht Untersuchungen zu Lebensmitteln, Kosmetik und Alltagsgegenständen. Kurzmeldungen sind frei, ausführliche Tests sind kostenpflichtig.",
    ["Untersuchungen zu Alltagprodukten", "Schwerpunkt Schadstoffe", "Freie Meldungen und kostenpflichtige Tests"],
    ["Einen Test zu einem Lebensmittel zu lesen", "Produkte einer Warengruppe zu vergleichen"], True)
add("Yazio", "https://www.yazio.com/de", "yazio.com", "freemium", "proprietary", ["gesundheit"],
    "Yazio führt ein Ernährungs- und Fastentagebuch.",
    "Yazio trägt Mahlzeiten ein und begleitet Intervallfasten. Der Dienst kommt aus Deutschland. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Ernährungstagebuch", "Intervallfasten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Mahlzeiten eines Tages zu erfassen", "Ein Fastenfenster zu planen"], True)
add("Yuka", "https://yuka.io/de", "yuka.io", "freemium", "proprietary", ["gesundheit"],
    "Yuka bewertet Lebensmittel und Kosmetik anhand des Strichcodes.",
    "Yuka liest einen Barcode und zeigt eine Einordnung der Zutaten. Die App kommt aus Frankreich und hat eine deutsche Fassung. Ein Teil ist ohne Abo nutzbar, weitere Funktionen sind bezahlt.",
    ["Barcode von Lebensmitteln und Kosmetik", "Einordnung der Zutaten", "Kostenloser Anteil und bezahlte Funktionen"],
    ["Ein Produkt im Laden zu scannen", "Zwei Produkte anhand der Bewertung zu vergleichen"], True)
add("Freeletics", "https://www.freeletics.com/de/", "freeletics.com", "freemium", "proprietary", ["gesundheit"],
    "Freeletics stellt Trainingspläne für Kraft und Ausdauer ohne Gerätepflicht bereit.",
    "Freeletics gibt Einheiten vor und passt sie an Rückmeldungen an. Der Dienst kommt aus München. Es gibt einen Einstieg und ein bezahltes Abo.",
    ["Trainingspläne für Kraft und Ausdauer", "Anpassung nach Rückmeldung", "Einstieg und bezahltes Abo"],
    ["Ein Training ohne Studio zu starten", "Einen mehrwöchigen Plan zu folgen"], True)
add("Urban Sports Club", "https://www.urbansportsclub.com/", "urbansportsclub.com", "paid", "proprietary", ["gesundheit"],
    "Urban Sports Club öffnet mit einer Mitgliedschaft viele Sportangebote in der Stadt.",
    "Die Mitgliedschaft gilt für Studios, Kurse und Schwimmbäder der Partner. Der Dienst ist in mehreren europäischen Städten verfügbar. Die Mitgliedschaft ist kostenpflichtig.",
    ["Eine Mitgliedschaft für viele Studios", "Kurse und Schwimmbäder", "Kostenpflichtige Mitgliedschaft"],
    ["Verschiedene Sportorte mit einem Zugang zu nutzen", "Einen Kurs in der Nähe zu finden"], True)
add("Superchat", "https://www.superchat.de/", "superchat.de", "freemium", "proprietary", ["kundenservice"],
    "Superchat bündelt WhatsApp, Mail und weitere Kanäle für den Kundenkontakt.",
    "Superchat legt Nachrichten aus mehreren Kanälen in einem Posteingang ab. Der Anbieter sitzt in Berlin. Es gibt einen Einstieg und bezahlte Stufen.",
    ["WhatsApp, Mail und weitere Kanäle", "Gemeinsamer Posteingang", "Einstieg und bezahlte Stufen"],
    ["Kundenchat über WhatsApp im Team zu führen", "Mehrere Kanäle in einem Posteingang zu lesen"], False)
add("Trusted Shops", "https://www.trustedshops.de/", "trustedshops.de", "paid", "proprietary", ["e-commerce", "recht"],
    "Trusted Shops prüft Online-Shops und bietet ein Gütesiegel mit Käuferschutz.",
    "Trusted Shops zertifiziert Shops nach eigenen Kriterien und kann einen Käuferschutz an die Bestellung hängen. Der Dienst kommt aus Köln. Die Mitgliedschaft für Händler ist kostenpflichtig.",
    ["Gütesiegel für Online-Shops", "Käuferschutz", "Kostenpflichtige Mitgliedschaft"],
    ["Einen Shop zertifizieren zu lassen", "Den Käuferschutz einer Bestellung zu prüfen"], False)
add("eRecht24", "https://www.e-recht24.de/", "e-recht24.de", "freemium", "proprietary", ["recht"],
    "eRecht24 stellt Muster und Generatoren für Rechtstexte deutscher Websites bereit.",
    "eRecht24 bietet Texte zu Datenschutz, Impressum und Widerruf und einen Generator für die Datenschutzerklärung. Ein Teil der Muster ist frei, der Generator und Updates sind kostenpflichtig.",
    ["Muster für Datenschutz und Impressum", "Generator für die Datenschutzerklärung", "Freie Muster und kostenpflichtige Updates"],
    ["Eine Datenschutzerklärung zu erzeugen", "Ein Muster für den Widerruf zu prüfen"], True)
add("Duden", "https://www.duden.de/", "duden.de", "freemium", "proprietary", ["bildung"],
    "Duden erklärt Rechtschreibung, Bedeutung und Grammatik deutscher Wörter.",
    "Duden zeigt Schreibweise, Aussprache und Beispiele. Die Suche im Wörterbuch ist ohne Abo möglich, weitere Nachschlagewerke sind bezahlt.",
    ["Rechtschreibung und Bedeutung", "Aussprache und Beispiele", "Freie Suche und bezahlte Nachschlagewerke"],
    ["Die Schreibweise eines Wortes zu prüfen", "Ein Beispiel zu einer Bedeutung zu lesen"], True)
add("DWDS", "https://www.dwds.de/", "dwds.de", "free", "unknown", ["bildung", "recherche"],
    "Das DWDS zeigt Wörterbücher und Belege aus Korpora des Deutschen.",
    "Das Digitale Wörterbuch der deutschen Sprache verbindet Bedeutung, Etymologie und echte Belegsätze. Die Abfrage ist ohne Abo möglich. Eine OSI-Lizenz der Website ist hier nicht hinterlegt.",
    ["Wörterbuch und Korpusbelege", "Etymologie", "Abfrage ohne Abo"],
    ["Die Verwendung eines Wortes in Sätzen zu sehen", "Herkunft und Bedeutung nachzuschlagen"], True)
add("OpenThesaurus", "https://www.openthesaurus.de/", "openthesaurus.de", "free", "unknown", ["bildung", "textgenerierung"],
    "OpenThesaurus sammelt Synonyme und Gegenwörter des Deutschen.",
    "OpenThesaurus zeigt bedeutungsähnliche Wörter und lässt Ergänzungen durch die Gemeinschaft zu. Die Suche ist ohne Abo möglich. Eine einzelne OSI-Kennung wird hier nicht eingetragen.",
    ["Synonyme und Gegenwörter", "Gemeinschaftliche Ergänzungen", "Suche ohne Abo"],
    ["Ein treffenderes Wort zu suchen", "Gegenwörter zu einem Begriff zu finden"], True)
add("CHECK24", "https://www.check24.de/", "check24.de", "free", "proprietary", ["recherche", "finanzen"],
    "CHECK24 vergleicht Tarife für Versicherung, Energie, Reisen und Finanzen.",
    "CHECK24 stellt Angebote mehrerer Anbieter nebeneinander. Der Vergleich ist ohne Abo möglich. Der Abschluss liegt beim jeweiligen Anbieter oder über die Plattform.",
    ["Vergleich vieler Tarife", "Versicherung, Energie und Reisen", "Vergleich ohne Abo"],
    ["Einen Stromtarif zu vergleichen", "Angebote einer Versicherung gegenüberzustellen"], True)
add("Verivox", "https://www.verivox.de/", "verivox.de", "free", "proprietary", ["recherche", "finanzen"],
    "Verivox vergleicht Tarife für Energie, Telekommunikation und Versicherungen.",
    "Verivox listet Angebote nach Preis und Konditionen. Die Suche ist ohne Abo möglich. Der Wechsel läuft über den jeweiligen Anbieter.",
    ["Tarifvergleich", "Energie, Telekommunikation und Versicherung", "Suche ohne Abo"],
    ["Einen Gastarif zu vergleichen", "Konditionen eines DSL-Angebots zu lesen"], True)
add("Softgarden", "https://www.softgarden.de/", "softgarden.de", "paid", "proprietary", ["personal"],
    "Softgarden veröffentlicht Stellen und sammelt Bewerbungen.",
    "Softgarden baut eine Karriereseite und legt eingehende Bewerbungen in einen Prozess. Der Anbieter sitzt in Berlin. Die Nutzung ist kostenpflichtig.",
    ["Karriereseite und Stellen", "Bewerbungsprozess", "Kostenpflichtige Nutzung"],
    ["Offene Stellen auf einer Karriereseite zu zeigen", "Bewerbungen in Stufen zu sortieren"], False)
add("StepStone", "https://www.stepstone.de/", "stepstone.de", "freemium", "proprietary", ["personal"],
    "StepStone listet Stellenangebote und Lebensläufe in Deutschland.",
    "StepStone zeigt Jobs und lässt Profile anlegen. Das Schalten einer Stelle ist kostenpflichtig, die Suche für Bewerbende ist ohne Abo möglich.",
    ["Stellenangebote und Profile", "Suche für Bewerbende ohne Abo", "Kostenpflichtige Stellenanzeigen"],
    ["Eine Stelle zu suchen", "Ein Profil für Arbeitgeber sichtbar zu machen"], True)
add("XING", "https://www.xing.com/", "xing.com", "freemium", "proprietary", ["personal", "social-media"],
    "XING vernetzt Berufstätige und zeigt Stellen im deutschsprachigen Raum.",
    "XING führt Profile, Nachrichten und Stellenanzeigen. Ein Basisprofil ist ohne Abo möglich, weitere Reichweite und Recruiter-Funktionen sind bezahlt.",
    ["Berufsprofile und Nachrichten", "Stellenanzeigen", "Basisprofil ohne Abo und bezahlte Funktionen"],
    ["Ein berufliches Profil zu pflegen", "Eine Stelle im Netzwerk zu finden"], True)
add("Dealfront", "https://www.dealfront.com/de/", "dealfront.com", "paid", "proprietary", ["marketing"],
    "Dealfront erkennt Unternehmen, die eine Website besuchen, und liefert Firmendaten.",
    "Dealfront, hervorgegangen aus Echobot und Leadfeeder, zeigt Firmeneinträge zu Besuchern und Kontakten. Der Dienst kommt aus Europa. Die Nutzung ist kostenpflichtig.",
    ["Firmendaten zu Website-Besuchen", "Kontaktdaten", "Kostenpflichtige Nutzung"],
    ["Zu sehen, welche Firmen die eigene Seite besucht haben", "Kontaktdaten zu einem Unternehmen zu suchen"], False)
add("Spendesk", "https://www.spendesk.com/", "spendesk.com", "paid", "proprietary", ["finanzen"],
    "Spendesk gibt Firmenkarten aus und sammelt Freigaben und Belege.",
    "Spendesk verbindet Karten, Rechnungen und Freigaben in einem Ausgabenprozess. Der Dienst kommt aus Frankreich. Die Nutzung ist kostenpflichtig.",
    ["Firmenkarten und Belege", "Freigaben", "Kostenpflichtige Nutzung"],
    ["Ausgaben eines Teams mit Belegen zu steuern", "Eine Rechnung zur Freigabe zu schicken"], False)
add("Billomat", "https://www.billomat.com/", "billomat.com", "freemium", "proprietary", ["finanzen"],
    "Billomat schreibt Angebote, Rechnungen und Mahnungen.",
    "Billomat speichert Kunden und erzeugt Belege, auch wiederkehrend. Der Dienst kommt aus Deutschland. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Angebote, Rechnungen und Mahnungen", "Wiederkehrende Belege", "Einstieg und bezahlte Stufen"],
    ["Eine wiederkehrende Rechnung anzulegen", "Eine Mahnung aus einer offenen Rechnung zu erzeugen"], True)
add("timr", "https://www.timr.com/", "timr.com", "freemium", "proprietary", ["personal", "produktivitaet"],
    "timr erfasst Arbeitszeit und Projekte, auch per App.",
    "timr stempelt Zeiten und ordnet sie Projekten und Tätigkeiten zu. Der Anbieter sitzt in Österreich. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Zeiterfassung per App", "Zuordnung zu Projekten", "Einstieg und bezahlte Stufen"],
    ["Arbeitsbeginn und Ende zu stempeln", "Stunden einem Projekt zuzuordnen"], True)
add("Shore", "https://www.shore.com/de", "shore.com", "freemium", "proprietary", ["produktivitaet"],
    "Shore vergibt Termine für Salons, Praxen und lokale Dienste.",
    "Shore zeigt freie Zeiten online und erinnert an den Termin. Der Anbieter kommt aus München. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Online-Terminbuchung", "Erinnerungen", "Einstieg und bezahlte Stufen"],
    ["Einen Terminlink für eine Praxis zu schalten", "Freie Zeiten ohne Telefon abzustimmen"], True)
add("AirHelp", "https://www.airhelp.com/de/", "airhelp.com", "freemium", "proprietary", ["reisen", "recht"],
    "AirHelp prüft Ansprüche bei Flugverspätung und Annulierung.",
    "AirHelp nimmt Flugdaten entgegen und schätzt, ob eine Ausgleichszahlung nach EU-Recht in Frage kommt. Die Prüfung des Anspruchs ist ohne Vorkasse beschrieben, eine erfolgreiche Durchsetzung ist erfolgsabhängig bezahlt.",
    ["Prüfung von Flugunregelmäßigkeiten", "Bezug auf EU-Ausgleich", "Erfolgsabhängige Vergütung"],
    ["Einen verspäteten Flug auf einen Anspruch zu prüfen", "Die Flugdaten für eine Forderung zu erfassen"], True)
add("Devin", "https://devin.ai/", "devin.ai", "paid", "proprietary", ["programmierung"],
    "Devin bearbeitet Softwareaufgaben als Agent in einer eigenen Umgebung.",
    "Devin nimmt einen Auftrag entgegen und arbeitet in einer Entwicklungsumgebung mit Terminal und Browser. Die Nutzung ist kostenpflichtig.",
    ["Agent für Softwareaufgaben", "Eigene Entwicklungsumgebung", "Kostenpflichtige Nutzung"],
    ["Einen Änderungsauftrag an einen Agenten zu geben", "Einen Lauf im Terminal nachzuvollziehen"], False)
add("Tabnine", "https://www.tabnine.com/", "tabnine.com", "freemium", "proprietary", ["programmierung"],
    "Tabnine schlägt Code in der Entwicklungsumgebung vor.",
    "Tabnine ergänzt Zeilen anhand des umgebenden Codes und kann auf das eigene Repository eingegrenzt werden. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Codevorschläge in der IDE", "Optional auf das eigene Repository begrenzt", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Funktion beim Tippen zu ergänzen", "Vorschläge auf den eigenen Code zu begrenzen"], False)
add("Kagi", "https://kagi.com/", "kagi.com", "paid", "proprietary", ["recherche"],
    "Kagi ist eine Suchmaschine ohne Werbung, die nach einem Abo sucht.",
    "Kagi liefert Suchergebnisse ohne Anzeigen und bietet Zusammenfassungen zu einer Seite. Die Nutzung ist kostenpflichtig.",
    ["Suche ohne Anzeigen", "Zusammenfassungen von Seiten", "Kostenpflichtige Nutzung"],
    ["Eine Suche ohne Werbeergebnisse zu starten", "Eine Seite kurz zusammenfassen zu lassen"], False)
add("You.com", "https://you.com/", "you.com", "freemium", "proprietary", ["recherche", "ki-chatbots"],
    "You.com beantwortet Fragen und zeigt dazu Quellen aus der Suche.",
    "You.com verbindet eine Suche mit einem Chat, der Angaben mit Links belegt. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Suche mit Chat", "Antworten mit Links", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Frage mit Quellen zu stellen", "Suchtreffer und eine Zusammenfassung zu vergleichen"], True)
add("Consensus", "https://consensus.app/", "consensus.app", "freemium", "proprietary", ["recherche"],
    "Consensus sucht Antworten in wissenschaftlichen Arbeiten.",
    "Consensus stellt eine Frage und zeigt, was Studien dazu berichten, mit Verweis auf die Paper. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Fragen an Studien", "Verweise auf Paper", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Den Stand der Forschung zu einer Frage zu sichten", "Eine Studie aus der Antwort zu öffnen"], False)
add("scite", "https://scite.ai/", "scite.ai", "freemium", "proprietary", ["recherche"],
    "scite zeigt, ob spätere Arbeiten eine Studie stützen oder widersprechen.",
    "scite ordnet Zitate als stützend, widersprechend oder erwähnend ein. Die detaillierte Ansicht ist teilweise bezahlt. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Einordnung von Zitaten", "Stützend oder widersprechend", "Einstieg und bezahlte Stufen"],
    ["Zu prüfen, wie eine Studie später zitiert wurde", "Widersprechende Arbeiten zu finden"], False)
add("arXiv", "https://arxiv.org/", "arxiv.org", "free", "unknown", ["recherche"],
    "arXiv veröffentlicht wissenschaftliche Preprints, vor allem aus Physik, Informatik und Mathematik.",
    "arXiv stellt Manuskripte als PDF bereit, oft vor der Zeitschrift. Die Texte sind ohne Abo lesbar. Eine OSI-Lizenz der Plattform ist hier nicht hinterlegt.",
    ["Preprints als PDF", "Schwerpunkt Physik, Informatik und Mathematik", "Lesen ohne Abo"],
    ["Ein Paper vor der Zeitschrift zu lesen", "Neue Arbeiten zu einem Stichwort zu finden"], True)
add("CORE", "https://core.ac.uk/", "core.ac.uk", "free", "unknown", ["recherche"],
    "CORE durchsucht frei zugängliche wissenschaftliche Texte aus Repositorien.",
    "CORE sammelt Open-Access-Arbeiten und macht sie über eine Suche findbar. Die Abfrage ist ohne Abo möglich. Eine OSI-Lizenz der Plattform ist hier nicht hinterlegt.",
    ["Suche über Open-Access-Texte", "Quellen aus Repositorien", "Abfrage ohne Abo"],
    ["Eine frei lesbare Fassung einer Arbeit zu finden", "Literatur zu einem Stichwort zu sichten"], True)
add("OSF", "https://osf.io/", "osf.io", "free", "unknown", ["recherche"],
    "Die Open Science Framework legt Projekte, Daten und Preprints offen ab.",
    "OSF speichert Materialien eines Forschungsprojekts und vergibt dafür eine bleibende Adresse. Das Anlegen ist ohne Abo möglich. Eine OSI-Lizenz der Plattform ist hier nicht hinterlegt.",
    ["Projekte, Daten und Preprints", "Bleibende Adressen", "Anlegen ohne Abo"],
    ["Daten zu einer Studie abzulegen", "Ein offenes Projekt zu zitieren"], False)
add("Unpaywall", "https://unpaywall.org/", "unpaywall.org", "free", "unknown", ["recherche"],
    "Unpaywall findet frei lesbare Fassungen hinter einer Bezahlschranke.",
    "Unpaywall prüft zu einem Aufsatz, ob ein Repositorium eine legale freie Fassung hält. Die Erweiterung und die Daten sind ohne Abo nutzbar. Eine OSI-Lizenz wird hier nicht eingetragen.",
    ["Suche nach freien Fassungen", "Abgleich mit Repositorien", "Nutzung ohne Abo"],
    ["Eine freie PDF-Fassung zu einem Paper zu finden", "Vor dem Kauf eine offene Kopie zu prüfen"], True)
add("Colossyan", "https://www.colossyan.com/", "colossyan.com", "freemium", "proprietary", ["videogenerierung"],
    "Colossyan erzeugt Erklärvideos mit Avatar und Skript.",
    "Colossyan lässt einen Avatar ein Skript sprechen und legt Folien darunter. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Avatar spricht ein Skript", "Folien im Video", "Einstieg und bezahlte Stufen"],
    ["Ein Schulungsvideo ohne Dreh zu erstellen", "Dasselbe Skript mit einem anderen Avatar zu sprechen"], False)
add("D-ID", "https://www.d-id.com/", "d-id.com", "freemium", "proprietary", ["videogenerierung"],
    "D-ID animiert ein Standbild und lässt es einen Text sprechen.",
    "D-ID nimmt ein Foto und ein Skript und erzeugt daraus ein sprechendes Video. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Sprechendes Foto", "Skript als Tonspur", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Portrait einen Text sprechen zu lassen", "Eine kurze Ansage aus einem Standbild zu machen"], False)
add("Powtoon", "https://www.powtoon.com/", "powtoon.com", "freemium", "proprietary", ["praesentationen", "videoschnitt"],
    "Powtoon baut animierte Erklärvideos und Folien aus Vorlagen.",
    "Powtoon setzt Figuren und Texte auf eine Zeitleiste und exportiert ein Video. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Animierte Erklärvideos", "Vorlagen und Zeitleiste", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein kurzes Erklärvideo zu animieren", "Eine Folie in eine Animation zu überführen"], True)
add("Visme", "https://www.visme.co/", "visme.co", "freemium", "proprietary", ["praesentationen", "design"],
    "Visme baut Präsentationen, Infografiken und kurze Formulare im Browser.",
    "Visme stellt Vorlagen für Folien und Grafiken bereit und exportiert sie als Bild oder PDF. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Folien und Infografiken", "Export als Bild oder PDF", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Infografik aus einer Vorlage zu bauen", "Eine Präsentation im Browser zu gestalten"], True)
add("Wooclap", "https://www.wooclap.com/", "wooclap.com", "freemium", "proprietary", ["praesentationen", "bildung"],
    "Wooclap sammelt Live-Antworten in Vorlesung und Workshop.",
    "Wooclap stellt Fragen, die das Publikum auf dem Handy beantwortet, und zeigt die Ergebnisse sofort. Der Dienst kommt aus Belgien. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Live-Fragen an ein Publikum", "Ergebnisse sofort sichtbar", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Verständnisfrage in der Vorlesung zu stellen", "Wortmeldungen in einem Workshop zu sammeln"], True)
add("Vectary", "https://www.vectary.com/", "vectary.com", "freemium", "proprietary", ["dreid", "design"],
    "Vectary modelliert 3D-Szenen im Browser und bettet sie in eine Seite ein.",
    "Vectary baut Objekte und Materialien ohne lokale Installation und kann die Szene auf einer Website zeigen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["3D im Browser", "Materialien und Einbettung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Produkt als 3D-Modell zu zeigen", "Eine Szene ohne Desktop-Software zu bauen"], True)
add("PlayCanvas", "https://playcanvas.com/", "playcanvas.com", "freemium", "proprietary", ["gaming", "dreid"],
    "PlayCanvas entwickelt 3D-Anwendungen im Browser.",
    "PlayCanvas bearbeitet Szenen, Materialien und Skripte gemeinsam im Browser und veröffentlicht sie als Webanwendung. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["3D-Szenen im Browser", "Skripte und Veröffentlichung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine 3D-Szene für das Web zu bauen", "Ein Projekt mit anderen im Browser zu bearbeiten"], False)
add("three.js", "https://threejs.org/", "threejs.org", "free", "unknown", ["dreid", "programmierung"],
    "three.js zeichnet 3D-Szenen im Browser mit WebGL.",
    "three.js ist eine Bibliothek, mit der eine Website Kameras, Lichter und Modelle darstellt. Die Beispiele auf threejs.org sind ohne Konto lesbar. Eine OSI-Kennung wird in diesem Eintrag nicht gesetzt, weil die Lizenzdatei hier nicht erneut gelesen wurde.",
    ["3D im Browser", "Kameras, Lichter und Modelle", "Beispiele ohne Konto"],
    ["Eine 3D-Szene in eine Website einzubauen", "Ein Beispiel als Ausgangspunkt zu nehmen"], False)
add("Piskel", "https://www.piskelapp.com/", "piskelapp.com", "free", "unknown", ["gaming", "design"],
    "Piskel zeichnet Pixelgrafik und kleine Animationen im Browser.",
    "Piskel arbeitet mit Ebenen und Einzelbildern und exportiert das Sprite. Die Nutzung im Browser ist ohne Abo möglich. Eine OSI-Lizenz wird hier nicht eingetragen.",
    ["Pixelgrafik im Browser", "Einzelbilder und Export", "Nutzung ohne Abo"],
    ["Ein Sprite für ein Spiel zu zeichnen", "Eine kurze Pixelanimation zu exportieren"], True)
add("Coverr", "https://coverr.co/", "coverr.co", "freemium", "proprietary", ["videoschnitt"],
    "Coverr stellt kurze Stock-Videos zum Herunterladen bereit.",
    "Coverr zeigt Clips, die sich in eigene Videos schneiden lassen. Ein Teil ist ohne Abo ladbar, weitere Lizenzen sind bezahlt.",
    ["Kurze Stock-Videos", "Download für den Schnitt", "Kostenloser Anteil und bezahlte Lizenzen"],
    ["Einen Hintergrundclip für ein Video zu finden", "Einen Schnitt mit frei ladbarem Material zu füllen"], True)
add("Mixkit", "https://mixkit.co/", "mixkit.co", "free", "proprietary", ["videoschnitt", "musik"],
    "Mixkit bietet Stock-Videos, Musik und Soundeffekte zum Download.",
    "Mixkit stellt Clips und Tracks bereit, die sich in eigenen Projekten verwenden lassen. Der Download ist ohne Abo möglich. Die Nutzungsregeln stehen auf der Website.",
    ["Videos, Musik und Effekte", "Download ohne Abo", "Nutzungsregeln auf der Website"],
    ["Einen Clip für einen Schnitt zu laden", "Einen Soundeffekt zu einem Video zu suchen"], True)
add("Epidemic Sound", "https://www.epidemicsound.com/", "epidemicsound.com", "paid", "proprietary", ["musik", "videoschnitt"],
    "Epidemic Sound lizenziert Musik und Soundeffekte für Videos.",
    "Epidemic Sound durchsucht Tracks nach Stimmung und Länge und gibt sie für die eigenen Produktionen frei, solange das Abo läuft. Die Nutzung ist kostenpflichtig.",
    ["Musik und Soundeffekte", "Suche nach Stimmung und Länge", "Kostenpflichtiges Abo"],
    ["Musik für ein Video zu lizenzieren", "Einen Track nach Länge zu filtern"], False)
add("ProWritingAid", "https://prowritingaid.com/", "prowritingaid.com", "freemium", "proprietary", ["textgenerierung"],
    "ProWritingAid markiert Stil, Wiederholungen und Grammatik in längeren Texten.",
    "ProWritingAid prüft einen Entwurf auf Satzlänge, Wortwiederholung und Grammatik. Der Schwerpunkt ist Englisch. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Stil und Grammatik", "Hinweise zu Wiederholungen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen längeren englischen Text zu prüfen", "Wortwiederholungen zu finden"], False)
add("Sudowrite", "https://www.sudowrite.com/", "sudowrite.com", "paid", "proprietary", ["textgenerierung"],
    "Sudowrite schreibt an Romanen und Szenen mit und schlägt Fortsetzungen vor.",
    "Sudowrite nimmt eine Szene und bietet Beschreibungen, Dialog und den nächsten Absatz. Die Nutzung ist kostenpflichtig.",
    ["Fortsetzungen von Szenen", "Beschreibungen und Dialog", "Kostenpflichtige Nutzung"],
    ["Eine Szene weiterschreiben zu lassen", "Mehrere Formulierungen für einen Absatz zu vergleichen"], False)
add("iA Writer", "https://ia.net/writer", "ia.net", "paid", "proprietary", ["textgenerierung", "produktivitaet"],
    "iA Writer ist ein reduzierter Editor für längere Texte.",
    "iA Writer blendet Formatierung aus und hebt den aktuellen Satz hervor. Der Hersteller sitzt in der Schweiz. Die App ist kostenpflichtig.",
    ["Reduzierter Schreibeditor", "Hervorhebung des aktuellen Satzes", "Kostenpflichtige App"],
    ["Einen langen Text ohne Ablenkung zu schreiben", "Den aktuellen Satz isoliert zu sehen"], True)
add("Bear", "https://bear.app/", "bear.app", "freemium", "proprietary", ["produktivitaet"],
    "Bear speichert Notizen in Markdown mit Schlagwörtern.",
    "Bear legt Notizen lokal auf Apple-Geräten ab und verknüpft sie über Tags. Die Grundfunktion ist ohne Abo nutzbar, Synchronisation über die eigenen Server ist bezahlt.",
    ["Notizen in Markdown", "Schlagwörter statt Ordner", "Grundfunktion ohne Abo, Sync bezahlt"],
    ["Eine Notiz mit Tags zu ordnen", "Einen Text in Markdown zu schreiben"], True)
add("Loom", "https://www.loom.com/", "loom.com", "freemium", "proprietary", ["videoschnitt", "produktivitaet"],
    "Loom nimmt den Bildschirm mit Kamera und Ton auf und teilt den Link.",
    "Loom zeichnet eine Erklärung am Bildschirm auf und legt den Clip unter eine Adresse. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Bildschirmaufnahme mit Kamera", "Teilen per Link", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine kurze Erklärung am Bildschirm aufzunehmen", "Einen Clip statt einer langen Mail zu schicken"], True)
add("Tella", "https://www.tella.tv/", "tella.tv", "freemium", "proprietary", ["videoschnitt"],
    "Tella nimmt Bildschirm und Kamera auf und schneidet die Szenen im Browser.",
    "Tella legt Aufnahmen als Szenen an und exportiert ein fertiges Video. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Bildschirm und Kamera", "Schnitt im Browser", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein kurzes Produktvideo aufzunehmen", "Szenen ohne ein Desktop-Schnittprogramm zu ordnen"], True)
add("StreamYard", "https://streamyard.com/", "streamyard.com", "freemium", "proprietary", ["videoschnitt", "social-media"],
    "StreamYard sendet Interviews und Präsentationen live in mehrere Kanäle.",
    "StreamYard holt Gäste per Link ins Bild und gibt den Stream an angebundene Plattformen weiter. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Live-Interviews im Browser", "Ausgabe an mehrere Kanäle", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Gespräch live zu senden", "Gäste ohne extra Software dazuzuschalten"], True)
add("Webflow", "https://webflow.com/", "webflow.com", "freemium", "proprietary", ["design"],
    "Webflow gestaltet Websites visuell und veröffentlicht sie mit CMS.",
    "Webflow verbindet Layout, Inhalte und Hosting. Die Seite lässt sich ohne eigenen Server ausliefern. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Visuelles Layout", "CMS und Hosting", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Website ohne eigenen Server zu veröffentlichen", "Inhalte in einem CMS zu pflegen"], False)
add("VSCodium", "https://vscodium.com/", "vscodium.com", "free", "unknown", ["programmierung"],
    "VSCodium ist ein Build des Code-OSS-Repositories ohne die Marken-Ergänzungen von Visual Studio Code.",
    "VSCodium liefert den Editor aus dem offenen Repository und lässt Erweiterungen aus einem eigenen Katalog zu. Eine OSI-Kennung wird hier nicht getrennt vom Upstream eingetragen. Die Builds sind ohne Abo erhältlich.",
    ["Editor aus dem offenen Repository", "Eigener Erweiterungskatalog", "Builds ohne Abo"],
    ["Einen Editor ohne die Microsoft-Marke zu installieren", "Ein Projekt lokal zu öffnen"], False)
add("Together AI", "https://www.together.ai/", "together.ai", "freemium", "proprietary", ["programmierung", "ki-chatbots"],
    "Together AI stellt offene Sprachmodelle über eine Schnittstelle bereit.",
    "Together hostet Modelle und rechnet Aufrufe ab. Die Konsole dient zum Testen. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Gehostete offene Modelle", "Konsole und API", "Einstieg und bezahlte Kontingente"],
    ["Ein offenes Modell ohne eigene GPU aufzurufen", "Mehrere Modelle über eine API zu vergleichen"], False)
add("Algolia", "https://www.algolia.com/", "algolia.com", "freemium", "proprietary", ["daten", "programmierung"],
    "Algolia liefert eine gehostete Suche für Websites und Apps.",
    "Algolia indexiert Datensätze und beantwortet Suchanfragen mit Tippfehler-Toleranz. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Gehostete Suche", "Tippfehler-Toleranz", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Produktsuche in einen Shop einzubauen", "Suchergebnisse ohne eigenen Index-Server zu liefern"], False)
add("Chroma", "https://www.trychroma.com/", "trychroma.com", "free", "unknown", ["daten", "programmierung"],
    "Chroma speichert Embeddings für die Suche in eigenen Anwendungen.",
    "Chroma legt Vektoren ab und beantwortet Ähnlichkeitsanfragen. Die Bibliothek lässt sich lokal starten. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Speicher für Embeddings", "Ähnlichkeitssuche", "Lokaler Start"],
    ["Eine Vektorsuche im eigenen Projekt zu starten", "Dokumente für einen Assistenten abzulegen"], False)
add("CVAT", "https://www.cvat.ai/", "cvat.ai", "freemium", "unknown", ["daten"],
    "CVAT beschriftet Bilder und Videos für das Training von Erkennungsmodellen.",
    "CVAT legt Aufgaben für Bounding-Boxes, Polygone und Tracks an. Es gibt eine Cloud und eine selbst betreibbare Ausgabe. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Markierung von Bild und Video", "Cloud und Selbstbetrieb", "Lizenz nicht eingetragen"],
    ["Objekte in einem Video zu markieren", "Eine Beschriftungsaufgabe im Team zu verteilen"], False)
add("TeamViewer", "https://www.teamviewer.com/de/", "teamviewer.com", "freemium", "proprietary", ["produktivitaet"],
    "TeamViewer öffnet einen Fernzugriff auf einen anderen Rechner.",
    "TeamViewer zeigt den Bildschirm eines entfernten Geräts und erlaubt Steuerung und Dateitausch. Der Anbieter sitzt in Göppingen. Private Nutzung hat einen kostenlosen Einstieg, gewerbliche Nutzung ist kostenpflichtig.",
    ["Fernsteuerung und Dateitausch", "Anbieter aus Göppingen", "Privater Einstieg und kostenpflichtige gewerbliche Nutzung"],
    ["Einem Rechner aus der Ferne zu helfen", "Eine Datei auf ein entferntes Gerät zu kopieren"], True)
add("Thunderbird", "https://www.thunderbird.net/de/", "thunderbird.net", "free", "unknown", ["produktivitaet"],
    "Thunderbird liest E-Mail, Kalender und Feeds auf dem eigenen Rechner.",
    "Thunderbird verbindet mehrere Postfächer und zeigt Kalender und Adressbuch lokal. Die Anwendung ist ohne Abo erhältlich. Eine OSI-Kennung wird in diesem Eintrag nicht gesetzt, weil die Lizenzdatei hier nicht erneut gelesen wurde.",
    ["Mehrere Postfächer", "Kalender und Adressbuch", "Nutzung ohne Abo"],
    ["Mehrere Mailkonten in einem Programm zu lesen", "Einen Kalender neben dem Posteingang zu führen"], True)
add("Signal", "https://signal.org/", "signal.org", "free", "proprietary", ["social-media"],
    "Signal verschickt Nachrichten und Anrufe mit Verschlüsselung.",
    "Signal führt Chats, Gruppen und Anrufe. Die App ist ohne Abo nutzbar. Der Dienst ist ein proprietäres Angebot der Signal-Stiftung, auch wenn Teile des Codes öffentlich sind. Eine OSI-Kennung für die ganze App wird hier nicht eingetragen.",
    ["Chats, Gruppen und Anrufe", "Verschlüsselung", "Nutzung ohne Abo"],
    ["Eine Nachricht verschlüsselt zu senden", "Einen Gruppenchat zu führen"], True)
add("Wire", "https://www.wire.com/de", "wire.com", "freemium", "proprietary", ["social-media"],
    "Wire führt verschlüsselte Chats und Anrufe für Teams.",
    "Wire bietet Nachrichten, Anrufe und Dateien. Es gibt eine persönliche Fassung und bezahlte Team-Pläne. Der Dienst hat Wurzeln in der Schweiz.",
    ["Chats und Anrufe", "Persönliche Fassung und Team-Pläne", "Einstieg und bezahlte Pläne"],
    ["Einen Team-Chat verschlüsselt zu führen", "Eine Datei in einem Gespräch zu teilen"], False)
add("Discord", "https://discord.com/", "discord.com", "freemium", "proprietary", ["social-media", "gaming"],
    "Discord führt Sprach- und Textkanäle für Gruppen und Communities.",
    "Discord legt Server mit Kanälen, Rollen und Sprachräumen an. Die Grundfunktion ist ohne Abo nutzbar, Nitro ist bezahlt.",
    ["Text- und Sprachkanäle", "Rollen auf einem Server", "Grundfunktion ohne Abo und bezahltes Nitro"],
    ["Einen Sprachraum für eine Gruppe zu öffnen", "Eine Community in Kanälen zu ordnen"], True)
add("Zoom", "https://zoom.us/", "zoom.us", "freemium", "proprietary", ["produktivitaet"],
    "Zoom startet Videokonferenzen mit Bildschirmfreigabe und Aufzeichnung.",
    "Zoom öffnet einen Raum über einen Link. Die kostenlose Fassung begrenzt die Dauer von Gruppengesprächen, längere Meetings und Zusatzfunktionen sind bezahlt.",
    ["Videoraum über einen Link", "Bildschirmfreigabe", "Begrenzte kostenlose Fassung und bezahlte Pläne"],
    ["Ein Meeting per Link zu starten", "Den Bildschirm in einem Gespräch zu teilen"], True)
add("LibreWolf", "https://librewolf.net/", "librewolf.net", "free", "unknown", ["recherche"],
    "LibreWolf ist ein Firefox-Build mit strengeren Datenschutz-Voreinstellungen.",
    "LibreWolf startet ohne Telemetrie und mit härteren Cookie-Regeln als Ausgang. Eine OSI-Kennung wird hier nicht getrennt eingetragen. Der Browser ist ohne Abo erhältlich.",
    ["Firefox-Build mit strengeren Voreinstellungen", "Ohne Telemetrie im Auslieferungszustand", "Nutzung ohne Abo"],
    ["Einen Browser mit weniger Voreinstellungs-Tracking zu nutzen", "Cookies strenger zu behandeln"], False)
add("Vivaldi", "https://vivaldi.com/", "vivaldi.com", "free", "proprietary", ["recherche"],
    "Vivaldi ist ein Browser mit vielen einstellbaren Leisten und Tab-Gruppen.",
    "Vivaldi lässt Tabs stapeln, die Oberfläche verschieben und Notizen neben der Seite halten. Der Browser ist ohne Abo nutzbar.",
    ["Stapelbare Tabs", "Anpassbare Oberfläche", "Nutzung ohne Abo"],
    ["Viele Tabs in Gruppen zu ordnen", "Eine Notiz neben der geöffneten Seite zu schreiben"], True)
add("Brave", "https://brave.com/", "brave.com", "free", "proprietary", ["recherche"],
    "Brave ist ein Browser, der Werbung und Tracker in der Voreinstellung blockiert.",
    "Brave lädt Seiten und filtert bekannte Tracker. Ein optionales Werbenetz des Herstellers lässt sich getrennt einschalten. Der Browser ist ohne Abo nutzbar.",
    ["Blockieren von Werbung und Trackern", "Optional getrenntes Werbenetz", "Nutzung ohne Abo"],
    ["Seiten mit weniger Trackern zu öffnen", "Werbung in der Voreinstellung zu filtern"], True)
add("qutebrowser", "https://qutebrowser.org/", "qutebrowser.org", "free", "unknown", ["recherche", "programmierung"],
    "qutebrowser steuert den Browser überwiegend über die Tastatur.",
    "qutebrowser öffnet Seiten und folgt Links mit Tasten statt mit der Maus. Eine OSI-Kennung wird hier nicht eingetragen. Der Browser ist ohne Abo erhältlich.",
    ["Steuerung über die Tastatur", "Links per Taste", "Nutzung ohne Abo"],
    ["Eine Seite ohne Maus zu bedienen", "Zwischen Tabs mit Tasten zu wechseln"], False)
add("Checkmk", "https://checkmk.com/", "checkmk.com", "freemium", "proprietary", ["programmierung"],
    "Checkmk überwacht Server, Dienste und Netzgeräte.",
    "Checkmk prüft Erreichbarkeit und Kennzahlen und alarmiert bei Ausfällen. Es gibt eine kostenlose Raw-Ausgabe und bezahlte Editionen. Der Anbieter sitzt in München.",
    ["Überwachung von Servern und Diensten", "Alarme bei Ausfällen", "Kostenlose Raw-Ausgabe und bezahlte Editionen"],
    ["Einen Dienst auf Erreichbarkeit zu prüfen", "Einen Alarm bei vollem Speicher zu setzen"], False)
add("Icinga", "https://icinga.com/", "icinga.com", "freemium", "unknown", ["programmierung"],
    "Icinga überwacht Hosts und Dienste und zeigt den Zustand in einer Oberfläche.",
    "Icinga prüft Erreichbarkeit und Schwellen und verschickt Meldungen. Es gibt eine selbst betreibbare Ausgabe und bezahlte Angebote. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Prüfungen von Hosts und Diensten", "Meldungen bei Schwellen", "Selbstbetrieb und bezahlte Angebote"],
    ["Einen Server auf Ausfälle zu überwachen", "Eine Meldung bei einem vollen Datenträger zu schicken"], False)
add("Netdata", "https://www.netdata.cloud/", "netdata.cloud", "freemium", "unknown", ["programmierung"],
    "Netdata zeigt Kennzahlen eines Servers in Echtzeit.",
    "Netdata sammelt CPU, Speicher, Platten und Dienste und zeichnet sie sofort. Es gibt einen Agenten zum Selbstbetrieb und eine Cloud. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Echtzeit-Kennzahlen", "Agent und Cloud", "Lizenz nicht eingetragen"],
    ["Die Last eines Servers live zu sehen", "Eine Platte zu beobachten, die vollläuft"], False)
add("Zabbix", "https://www.zabbix.com/", "zabbix.com", "free", "unknown", ["programmierung"],
    "Zabbix überwacht Infrastruktur und alarmiert bei Schwellen.",
    "Zabbix sammelt Werte von Servern und Netzwerkgeräten und löst Aktionen aus. Die Software ist ohne Pflichtabo erhältlich. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Überwachung von Servern und Netzwerk", "Aktionen bei Schwellen", "Nutzung ohne Pflichtabo"],
    ["Viele Hosts in einer Übersicht zu sehen", "Einen Alarm an eine Schwelle zu binden"], False)
add("etracker", "https://www.etracker.com/", "etracker.com", "paid", "proprietary", ["seo", "marketing"],
    "etracker zählt Besuche einer Website und kommt aus Deutschland.",
    "etracker zeigt Aufrufe, Kampagnen und Ziele. Der Anbieter sitzt in Hamburg. Die Nutzung ist kostenpflichtig.",
    ["Aufrufe, Kampagnen und Ziele", "Anbieter aus Hamburg", "Kostenpflichtige Nutzung"],
    ["Besuche einer deutschen Website zu zählen", "Eine Kampagne an den Aufrufen zu messen"], False)
add("Simple Analytics", "https://www.simpleanalytics.com/", "simpleanalytics.com", "paid", "proprietary", ["seo"],
    "Simple Analytics zählt Seitenaufrufe ohne Cookies und ohne Profile.",
    "Simple Analytics zeigt Aufrufe, Quellen und Seiten in einem kurzen Bericht. Die Nutzung ist kostenpflichtig.",
    ["Aufrufe ohne Cookies", "Quellen und Seiten", "Kostenpflichtige Nutzung"],
    ["Den Traffic ohne Cookie-Einwilligung zu zählen", "Die wichtigsten Seiten einer Website zu sehen"], False)
add("Fathom", "https://usefathom.com/", "usefathom.com", "paid", "proprietary", ["seo"],
    "Fathom zählt Besuche ohne Cookie-Banner und ohne Personenprofile.",
    "Fathom zeigt Aufrufe und Quellen in einer schmalen Ansicht. Die gehostete Fassung ist kostenpflichtig.",
    ["Aufrufe und Quellen", "Ohne Cookie-Banner", "Kostenpflichtige gehostete Fassung"],
    ["Besuche einer Website schlank zu zählen", "Quellen eines Monats zu vergleichen"], False)
add("Piwik PRO", "https://piwik.pro/", "piwik.pro", "freemium", "proprietary", ["seo", "marketing"],
    "Piwik PRO analysiert Besuche und kann die Daten in der EU halten.",
    "Piwik PRO zeigt Aufrufe, Kampagnen und Einwilligungen. Es gibt eine begrenzte kostenlose Core-Fassung und bezahlte Pläne.",
    ["Aufrufe und Kampagnen", "Einwilligungsverwaltung", "Begrenzte Core-Fassung und bezahlte Pläne"],
    ["Besuche mit Einwilligung zu zählen", "Eine Kampagne auszuwerten"], False)
add("SonarQube", "https://www.sonarsource.com/products/sonarqube/", "sonarsource.com", "freemium", "proprietary", ["programmierung"],
    "SonarQube prüft Quelltext auf Fehler, Gerüche und Sicherheitsmuster.",
    "SonarQube analysiert ein Repository und zeigt Befunde nach Schwere. Es gibt eine Community-Ausgabe und bezahlte Editionen. Die gehostete Plattform ist proprietär.",
    ["Befunde zu Fehlern und Sicherheit", "Community-Ausgabe und bezahlte Editionen", "Analyse eines Repository"],
    ["Ein Projekt auf wiederkehrende Fehler zu prüfen", "Sicherheitsmuster im Code zu sehen"], False)
add("Codacy", "https://www.codacy.com/", "codacy.com", "freemium", "proprietary", ["programmierung"],
    "Codacy prüft Pull-Requests auf Stil, Fehler und Abdeckung.",
    "Codacy kommentiert Änderungen in einem Repository und fasst die Qualität zusammen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Prüfung von Pull-Requests", "Stil, Fehler und Abdeckung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Änderung vor dem Merge prüfen zu lassen", "Die Testabdeckung eines Repository zu sehen"], False)
add("Sourcegraph Cody", "https://sourcegraph.com/docs/cody", "sourcegraph.com", "freemium", "proprietary", ["programmierung"],
    "Cody beantwortet Fragen zum eigenen Code und schlägt Änderungen vor.",
    "Cody nutzt den Index von Sourcegraph und ein Sprachmodell, um Stellen im Repository zu erklären. Es gibt einen kostenlosen Einstieg und bezahlte Stufen. Die Plattform ist proprietär.",
    ["Fragen zum eigenen Repository", "Änderungsvorschläge", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Funktion im eigenen Code erklären zu lassen", "Eine Stelle über mehrere Repositories zu finden"], False)
add("GitHub Copilot", "https://github.com/features/copilot", "github.com", "freemium", "proprietary", ["programmierung"],
    "GitHub Copilot schlägt Code in der Entwicklungsumgebung vor.",
    "Copilot ergänzt Zeilen und Chat-Antworten anhand des offenen Projekts. Es gibt einen begrenzten kostenlosen Einstieg und bezahlte Pläne. Das Angebot ist proprietär.",
    ["Codevorschläge in der IDE", "Chat zum offenen Projekt", "Begrenzter Einstieg und bezahlte Pläne"],
    ["Eine Funktion beim Tippen ergänzen zu lassen", "Eine Datei im Chat zu erklären"], False)
add("CapRover", "https://caprover.com/", "caprover.com", "free", "unknown", ["programmierung"],
    "CapRover spielt Anwendungen per Git oder Image auf den eigenen Server aus.",
    "CapRover verbindet einen Server mit einer Oberfläche für Apps, Datenbanken und HTTPS. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Deploy auf den eigenen Server", "Apps, Datenbanken und HTTPS", "Nutzung ohne Pflichtabo"],
    ["Eine Anwendung ohne große Cloud-Konsole zu starten", "HTTPS für eine App auf dem eigenen Server zu schalten"], False)
add("Dokku", "https://dokku.com/", "dokku.com", "free", "unknown", ["programmierung"],
    "Dokku startet Anwendungen auf einem eigenen Server nach einem Git-Push.",
    "Dokku baut aus einem Push einen Container und hängt Domains und Datenbanken an. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Deploy per Git-Push", "Domains und Datenbanken", "Nutzung ohne Pflichtabo"],
    ["Eine App mit einem Push zu veröffentlichen", "Eine Datenbank neben die App zu hängen"], False)
add("YunoHost", "https://yunohost.org/", "yunohost.org", "free", "unknown", ["programmierung"],
    "YunoHost installiert Webanwendungen auf einem eigenen Server über eine Oberfläche.",
    "YunoHost richtet Nutzer, Domains und fertige Apps ein. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Apps, Nutzer und Domains", "Oberfläche für den eigenen Server", "Nutzung ohne Pflichtabo"],
    ["Mehrere Webapps auf einem kleinen Server zu installieren", "Nutzer und Domains an einem Ort zu verwalten"], False)
add("HestiaCP", "https://hestiacp.com/", "hestiacp.com", "free", "unknown", ["programmierung"],
    "HestiaCP verwaltet Websites, Mail und DNS auf einem eigenen Server.",
    "HestiaCP legt Seiten, Postfächer und Zertifikate in einer Oberfläche an. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Websites, Mail und DNS", "Zertifikate in der Oberfläche", "Nutzung ohne Pflichtabo"],
    ["Mehrere Websites auf einem Server zu betreiben", "Ein Postfach zur Domain anzulegen"], False)
add("Froxlor", "https://www.froxlor.org/", "froxlor.org", "free", "unknown", ["programmierung"],
    "Froxlor verwaltet Webspace, Kunden und DNS für Hoster auf dem eigenen Server.",
    "Froxlor legt Kunden, Domains und Datenbanken an. Der Ursprung liegt in Deutschland. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Kunden, Domains und Datenbanken", "Verwaltung für Hoster", "Nutzung ohne Pflichtabo"],
    ["Webspace für mehrere Kunden zu vergeben", "Eine Domain mit Datenbank anzulegen"], False)
add("Apache Guacamole", "https://guacamole.apache.org/", "guacamole.apache.org", "free", "unknown", ["programmierung"],
    "Apache Guacamole öffnet Fernzugriff auf Rechner im Browser.",
    "Guacamole vermittelt RDP, VNC und SSH über eine Webseite, ohne dass auf dem Client eine extra App nötig ist. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Fernzugriff im Browser", "RDP, VNC und SSH", "Nutzung ohne Pflichtabo"],
    ["Einen Rechner ohne Client-Installation zu erreichen", "Mehrere Sitzungen über eine Webseite zu bündeln"], False)
add("Remmina", "https://remmina.org/", "remmina.org", "free", "unknown", ["programmierung"],
    "Remmina verbindet sich per RDP, VNC und SSH mit anderen Rechnern.",
    "Remmina speichert Verbindungsprofile und öffnet den entfernten Bildschirm auf dem eigenen Desktop. Eine OSI-Kennung wird hier nicht eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["RDP, VNC und SSH", "Gespeicherte Profile", "Nutzung ohne Pflichtabo"],
    ["Einen Windows-Rechner per RDP zu öffnen", "Mehrere Verbindungen als Profile zu halten"], False)
add("LibreSprite", "https://libresprite.github.io/", "libresprite.github.io", "free", "unknown", ["gaming", "design"],
    "LibreSprite zeichnet Pixelgrafik und Animationen.",
    "LibreSprite arbeitet mit Ebenen, Paletten und Einzelbildern. Eine OSI-Kennung wird hier nicht eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Pixelgrafik und Animation", "Ebenen und Paletten", "Nutzung ohne Pflichtabo"],
    ["Ein Sprite zu zeichnen", "Eine kurze Pixelanimation zu exportieren"], False)
add("Flowblade", "https://jliljebl.github.io/flowblade/", "jliljebl.github.io", "free", "unknown", ["videoschnitt"],
    "Flowblade schneidet Videos auf einer Timeline unter Linux.",
    "Flowblade setzt Clips auf Spuren und exportiert das Ergebnis. Eine OSI-Kennung wird hier nicht eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Timeline unter Linux", "Export des Schnitts", "Nutzung ohne Pflichtabo"],
    ["Einen Schnitt auf einem Linux-Rechner zu machen", "Clips auf Spuren zu legen"], False)
add("dynalist", "https://dynalist.io/", "dynalist.io", "freemium", "proprietary", ["produktivitaet"],
    "Dynalist sammelt Notizen als verschachtelte Listen mit Gliederung.",
    "Dynalist legt Punkte ineinander und kann sie filtern. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Verschachtelte Listen", "Filter über die Punkte", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Thema in eine Gliederung zu zerlegen", "Eine lange Liste zu filtern"], True)
add("Things", "https://culturedcode.com/things/", "culturedcode.com", "paid", "proprietary", ["produktivitaet"],
    "Things sammelt Aufgaben nach Bereichen, Projekten und dem heutigen Tag.",
    "Things legt To-dos in Projekte und zeigt, was heute ansteht. Die Apps sind kostenpflichtig. Der Hersteller sitzt in Stuttgart.",
    ["Aufgaben nach Projekt und Tag", "Ansicht für heute", "Kostenpflichtige Apps"],
    ["Den Tag als kurze Liste zu planen", "Ein Projekt in nächste Schritte zu teilen"], True)


def validate(entries):
    domains = {row[0] for row in sqlite3.connect(ROOT / "data" / "linkjagd.db").execute("select domain from tools")}
    # github.com is shared; allow only if path not used
    paths = set()
    for domain, url in sqlite3.connect(ROOT / "data" / "linkjagd.db").execute("select domain, original_url from tools"):
        if domain == "github.com":
            try:
                paths.add(urlparse_path(url))
            except Exception:
                pass
    seen = set()
    errors = []
    for entry in entries:
        if entry["domain"] in domains and entry["domain"] != "github.com":
            errors.append(f"db {entry['domain']} {entry['name']}")
        if entry["domain"] == "github.com":
            p = urlparse_path(entry["originalUrl"])
            if p in paths:
                errors.append(f"github {p}")
        if entry["domain"] in seen:
            errors.append(f"dup {entry['domain']}")
        seen.add(entry["domain"])
        if not (10 <= len(entry["shortDescriptionDe"]) <= 280):
            errors.append(f"kurz {entry['name']} {len(entry['shortDescriptionDe'])}")
        blob = entry["shortDescriptionDe"] + entry["longDescriptionDe"]
        if "zzgl" in blob.lower():
            errors.append(f"ust {entry['name']}")
    if errors:
        raise SystemExit("\n".join(errors[:40]))
    return entries


def urlparse_path(url):
    from urllib.parse import urlparse
    return urlparse(url).path.rstrip("/") or "/"


if __name__ == "__main__":
    rows = validate(E)
    out = ROOT / "data" / "verified-tools-batch5.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows), "->", out)
