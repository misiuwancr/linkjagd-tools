#!/usr/bin/env python3
"""Vierte geprüfte Liste. Nur Seiten, die in diesem Lauf mit HTTP 200 geantwortet haben."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

INSTALL = "Die Schritte zum Installieren stehen in der Projektdokumentation."
ROOT = Path(__file__).resolve().parents[1]


def oss(repo, license_name, project):
    return {"projectUrl": project, "repoUrl": repo, "license": license_name, "systems": [], "install": INSTALL}


def tool(name, url, domain, price, license_type, cats, short, long, features, uses, beginner=False, oss_block=None):
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
        "oss": oss_block,
    }


E = []


def add(*a, **k):
    E.append(tool(*a, **k))


add("Aleph Alpha", "https://aleph-alpha.com/", "aleph-alpha.com", "paid", "proprietary", ["ki-chatbots", "textgenerierung"],
    "Aleph Alpha bietet Sprachmodelle und eine Plattform aus Deutschland für Unternehmen.",
    "Aleph Alpha stellt eigene Sprachmodelle bereit, die sich über eine Plattform und Schnittstelle in Unternehmenssoftware einbinden lassen. Der Sitz ist in Heidelberg. Die angebotenen Zugänge sind kostenpflichtig.",
    ["Sprachmodelle aus Deutschland", "Plattform und Schnittstelle", "Kostenpflichtige Zugänge"],
    ["Ein Sprachmodell in eine interne Anwendung einzubinden", "Texte in einer europäischen Umgebung zu verarbeiten"], False)
add("Langdock", "https://langdock.com/", "langdock.com", "freemium", "proprietary", ["ki-chatbots"],
    "Langdock stellt einem Team mehrere Sprachmodelle in einem gemeinsamen Arbeitsbereich bereit.",
    "Langdock bündelt Chats, Assistenten und angebundenes Wissen für ein Unternehmen. Der Dienst kommt aus Berlin. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Gemeinsamer Chat für ein Team", "Mehrere Modelle", "Einstieg und bezahlte Stufen"],
    ["Ein Team auf ein gemeinsames Sprachmodell zu setzen", "Internes Wissen an einen Assistenten zu hängen"], True)
add("neuroflash", "https://neuroflash.com/", "neuroflash.com", "freemium", "proprietary", ["textgenerierung", "marketing"],
    "neuroflash schreibt Marketingtexte auf Deutsch und in weiteren Sprachen.",
    "neuroflash erzeugt Entwürfe für Anzeigen, Seiten und Produkttexte und prüft sie auf Markenregeln. Der Anbieter sitzt in Hamburg. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Marketingtexte auf Deutsch", "Markenregeln im Entwurf", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen deutschen Werbetext zu entwerfen", "Mehrere Formulierungen für eine Seite zu vergleichen"], True)
add("Parloa", "https://www.parloa.com/", "parloa.com", "paid", "proprietary", ["kundenservice"],
    "Parloa baut telefonische und chatbasierte Assistenten für den Kundenservice.",
    "Parloa richtet Dialoge ein, die Anrufe und Chats annehmen und an bestehende Systeme anbinden. Das Unternehmen kommt aus Berlin. Die Nutzung ist kostenpflichtig.",
    ["Dialoge für Telefon und Chat", "Anbindung an bestehende Systeme", "Kostenpflichtige Nutzung"],
    ["Einen Service-Anruf automatisch anzunehmen", "Einen Chat-Assistenten an ein Ticketsystem zu hängen"], False)
add("Black Forest Labs", "https://bfl.ai/", "bfl.ai", "freemium", "proprietary", ["bildgenerierung"],
    "Black Forest Labs entwickelt die Flux-Bildmodelle und bietet sie über eine Plattform an.",
    "Über bfl.ai lassen sich Bilder aus Text erzeugen. Das Labor sitzt in Freiburg. Es gibt einen Einstieg und bezahlte Kontingente für die Schnittstelle.",
    ["Bildmodelle der Flux-Reihe", "Erzeugung aus Text", "Einstieg und bezahlte Kontingente"],
    ["Ein Bild aus einer Beschreibung zu erzeugen", "Ein Modell über die Schnittstelle anzubinden"], False)
add("Qonto", "https://qonto.com/", "qonto.com", "freemium", "proprietary", ["finanzen"],
    "Qonto führt ein Geschäftskonto mit Rechnungen, Karten und Belegen.",
    "Qonto bündelt Kontoumsätze, Team-Karten und Belege für kleine Unternehmen. Der Dienst ist in mehreren europäischen Ländern verfügbar. Die Konten sind kostenpflichtig, der Vergleich der Tarife steht auf der Website.",
    ["Geschäftskonto und Karten", "Belege und Rechnungen", "Kostenpflichtige Konten"],
    ["Ein Geschäftskonto für ein kleines Team zu führen", "Belege zu Umsätzen abzulegen"], True)
add("Stackfield", "https://www.stackfield.com/", "stackfield.com", "paid", "proprietary", ["produktivitaet"],
    "Stackfield bündelt Aufgaben, Dateien und Chat mit Ende-zu-Ende-Verschlüsselung.",
    "Stackfield legt Projekte mit Aufgaben, Dateien und Nachrichten an. Der Anbieter sitzt in München und wirbt mit Verschlüsselung der Inhalte. Die Nutzung ist kostenpflichtig.",
    ["Aufgaben, Dateien und Chat", "Verschlüsselte Projekträume", "Kostenpflichtige Nutzung"],
    ["Ein Projekt mit Aufgaben und Dateien zu führen", "Nachrichten im Team verschlüsselt zu lassen"], False)
add("Taxfix", "https://taxfix.de/", "taxfix.de", "freemium", "proprietary", ["finanzen"],
    "Taxfix führt durch die deutsche Steuererklärung in einer App.",
    "Taxfix stellt Fragen zur Steuer und überträgt die Angaben in eine Erklärung. Der Dienst richtet sich an Arbeitnehmerinnen und Arbeitnehmer in Deutschland. Die Abgabe ist kostenpflichtig, der Einstieg in die Fragen ist ohne sofortige Zahlung möglich.",
    ["Fragen zur Steuererklärung", "Ausrichtung auf Deutschland", "Kostenpflichtige Abgabe"],
    ["Eine Steuererklärung in der App zu beginnen", "Angaben Schritt für Schritt zu prüfen"], True)
add("mailbox.org", "https://mailbox.org/", "mailbox.org", "paid", "proprietary", ["produktivitaet"],
    "mailbox.org bietet E-Mail, Kalender und Kontakte aus Deutschland.",
    "mailbox.org stellt Postfächer mit Kalender und Cloud-Funktionen bereit. Der Betrieb liegt in Deutschland. Die Postfächer sind kostenpflichtig.",
    ["E-Mail, Kalender und Kontakte", "Betrieb in Deutschland", "Kostenpflichtige Postfächer"],
    ["Ein Postfach mit Kalender zu nutzen", "Mail außerhalb der großen US-Anbieter zu führen"], True)
add("Posteo", "https://posteo.de/", "posteo.de", "paid", "proprietary", ["produktivitaet"],
    "Posteo ist ein kostenpflichtiges E-Mail-Postfach aus Berlin ohne Werbung.",
    "Posteo stellt Postfächer mit Kalender und ohne Werbeeinblendung bereit. Ein Konto lässt sich ohne Klarnamen eröffnen. Der Preis ist ein fester Monatsbetrag, den die Website nennt.",
    ["E-Mail ohne Werbung", "Kalender im Postfach", "Kostenpflichtiges Konto"],
    ["Ein werbefreies Postfach zu nutzen", "Kalender und Mail an einem Ort zu halten"], True)
add("Lexware Office", "https://www.lexoffice.de/", "lexoffice.de", "freemium", "proprietary", ["finanzen"],
    "Lexware Office schreibt Rechnungen und führt Belege für Selbstständige in Deutschland.",
    "Lexware Office, früher lexoffice, legt Angebote, Rechnungen und Belege an und bereitet Daten für die Steuer vor. Der Dienst richtet sich an den deutschen Markt. Es gibt einen Test und kostenpflichtige Tarife.",
    ["Angebote, Rechnungen und Belege", "Ausrichtung auf Deutschland", "Test und kostenpflichtige Tarife"],
    ["Eine Rechnung an einen Kunden zu schreiben", "Belege für die Steuer zu sammeln"], True)
add("easybill", "https://www.easybill.de/", "easybill.de", "freemium", "proprietary", ["finanzen"],
    "easybill schreibt Rechnungen, Angebote und Mahnungen.",
    "easybill speichert Kunden und erzeugt daraus Belege. Der Dienst kommt aus Deutschland. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Rechnungen und Angebote", "Kundenstammdaten", "Einstieg und bezahlte Stufen"],
    ["Wiederkehrende Rechnungen zu schreiben", "Eine Mahnung aus einer offenen Rechnung zu erzeugen"], True)
add("BuchhaltungsButler", "https://www.buchhaltungsbutler.de/", "buchhaltungsbutler.de", "freemium", "proprietary", ["finanzen"],
    "BuchhaltungsButler liest Belege ein und bereitet Buchungen vor.",
    "BuchhaltungsButler holt Belege aus Postfach und Portalen und schlägt Buchungen vor. Die Daten lassen sich an eine Steuerkanzlei geben. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Belege aus Postfach und Portalen", "Buchungsvorschläge", "Einstieg und bezahlte Stufen"],
    ["Belege zu sammeln, ohne sie abzutippen", "Eine vorbereitete Buchhaltung an die Kanzlei zu geben"], False)
add("Papierkram", "https://www.papierkram.de/", "papierkram.de", "freemium", "proprietary", ["finanzen"],
    "Papierkram führt Angebote, Rechnungen und eine einfache Buchhaltung.",
    "Papierkram legt Belege an und zeigt Einnahmen und Ausgaben. Der Dienst richtet sich an Freiberufler in Deutschland. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Angebote und Rechnungen", "Einnahmen und Ausgaben", "Einstieg und bezahlte Stufen"],
    ["Eine Rechnung für ein Projekt zu schreiben", "Einnahmen eines Jahres zu überblicken"], True)
add("FastBill", "https://www.fastbill.com/", "fastbill.com", "freemium", "proprietary", ["finanzen"],
    "FastBill automatisiert Rechnungen und Zahlungsabgleich.",
    "FastBill erzeugt Rechnungen und gleicht Zahlungseingänge ab. Der Dienst kommt aus Deutschland. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Rechnungen und Zahlungsabgleich", "Automatisierte Belege", "Einstieg und bezahlte Stufen"],
    ["Rechnungen aus Aufträgen zu erzeugen", "Offene Posten gegen Eingänge zu prüfen"], False)
add("GetMyInvoices", "https://www.getmyinvoices.com/", "getmyinvoices.com", "freemium", "proprietary", ["finanzen"],
    "GetMyInvoices sammelt Eingangsrechnungen aus Portalen und dem Postfach.",
    "GetMyInvoices lädt Belege von Lieferanten herunter und legt sie an einem Ort ab. Von dort gehen sie an die Buchhaltung. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Eingangsrechnungen sammeln", "Weitergabe an die Buchhaltung", "Einstieg und bezahlte Stufen"],
    ["Lieferantenrechnungen automatisch zu holen", "Belege an ein Buchhaltungssystem zu geben"], False)
add("Billbee", "https://www.billbee.io/", "billbee.io", "freemium", "proprietary", ["e-commerce"],
    "Billbee bündelt Bestellungen aus mehreren Shops und Marktplätzen.",
    "Billbee holt Bestellungen aus angebundenen Shops und gibt sie an Versand und Rechnung weiter. Der Dienst richtet sich an Händler in Deutschland. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Bestellungen aus mehreren Shops", "Weitergabe an Versand und Rechnung", "Einstieg und bezahlte Stufen"],
    ["Mehrere Verkaufskanäle in einer Liste zu sehen", "Bestellungen an den Versand zu übergeben"], False)
add("JTL-Software", "https://www.jtl-software.com/", "jtl-software.com", "freemium", "proprietary", ["e-commerce"],
    "JTL führt Warenwirtschaft, Shop und Versand für Online-Händler.",
    "JTL verbindet Artikel, Bestellungen und Versand in einer Warenwirtschaft. Der Anbieter sitzt in Deutschland. Es gibt eine kostenlose Warenwirtschaft und bezahlte Module.",
    ["Warenwirtschaft und Versand", "Anbindung an Shops", "Kostenlose Warenwirtschaft und bezahlte Module"],
    ["Artikel und Bestände zu führen", "Bestellungen an den Versand zu übergeben"], False)
add("Gambio", "https://www.gambio.de/", "gambio.de", "freemium", "proprietary", ["e-commerce"],
    "Gambio ist eine Shop-Software aus Deutschland für Katalog und Kasse.",
    "Gambio stellt einen Onlineshop mit Artikeln, Kasse und Rechtstext-Anbindung bereit. Der Betrieb kann auf dem eigenen Webspace liegen. Es gibt kostenpflichtige Pakete, die Website nennt die aktuellen Tarife.",
    ["Shop mit Katalog und Kasse", "Ausrichtung auf den deutschen Handel", "Kostenpflichtige Pakete"],
    ["Einen Shop auf eigenem Webspace zu betreiben", "Artikel und Bestellungen in einer Oberfläche zu pflegen"], False)
add("DATEV", "https://www.datev.de/", "datev.de", "paid", "proprietary", ["finanzen", "recht"],
    "DATEV stellt Software für Buchhaltung, Lohn und den Austausch mit der Steuerkanzlei bereit.",
    "DATEV verbindet Unternehmen und Steuerberatung bei Buchführung, Lohn und Jahresabschluss. Die Programme richten sich an den deutschen Markt. Die Nutzung ist kostenpflichtig.",
    ["Buchhaltung und Lohn", "Austausch mit der Kanzlei", "Kostenpflichtige Programme"],
    ["Buchungen an die Steuerkanzlei zu geben", "Lohnabrechnungen vorzubereiten"], False)
add("ELSTER", "https://www.elster.de/", "elster.de", "free", "proprietary", ["finanzen"],
    "ELSTER ist das Portal der Finanzverwaltung für Steuererklärungen in Deutschland.",
    "Über ELSTER lassen sich Steuererklärungen elektronisch an das Finanzamt übermitteln. Der Zugang ist an ein Konto der Finanzverwaltung gebunden. Die Übermittlung selbst ist ohne zusätzliches Abo möglich.",
    ["Elektronische Steuererklärung", "Übermittlung an das Finanzamt", "Nutzung ohne zusätzliches Abo"],
    ["Eine Steuererklärung elektronisch abzugeben", "Bescheide im Portal nachzusehen"], True)
add("Finom", "https://www.finom.co/", "finom.co", "freemium", "proprietary", ["finanzen"],
    "Finom kombiniert ein Geschäftskonto mit Rechnungen und Belegen.",
    "Finom zeigt Umsätze, Karten und Rechnungen in einem Konto für Selbstständige und kleine Teams. Der Dienst ist in Europa verfügbar. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Geschäftskonto und Karten", "Rechnungen im selben Konto", "Einstieg und bezahlte Stufen"],
    ["Umsätze und Rechnungen an einem Ort zu sehen", "Eine Karte für ein Team auszugeben"], True)
add("Moss", "https://www.getmoss.com/", "getmoss.com", "paid", "proprietary", ["finanzen"],
    "Moss gibt Firmenkarten aus und sammelt dazu die Belege.",
    "Moss verbindet Kartenausgaben mit Belegfotos und Freigaben. Der Dienst kommt aus Berlin. Die Nutzung ist kostenpflichtig.",
    ["Firmenkarten und Belege", "Freigaben für Ausgaben", "Kostenpflichtige Nutzung"],
    ["Ausgaben eines Teams mit Belegen zu sammeln", "Eine Karte mit Freigabeprozess auszugeben"], False)
add("Pleo", "https://www.pleo.io/", "pleo.io", "freemium", "proprietary", ["finanzen"],
    "Pleo gibt Mitarbeiterkarten aus und ordnet jeder Zahlung einen Beleg zu.",
    "Pleo verbindet Karten mit Belegfotos und Ausgabenregeln. Das Unternehmen kommt aus Kopenhagen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Mitarbeiterkarten", "Beleg zu jeder Zahlung", "Einstieg und bezahlte Stufen"],
    ["Spesen mit einem Foto des Belegs zu erfassen", "Ausgabenregeln für ein Team zu setzen"], False)
add("Factorial", "https://factorialhr.com/", "factorialhr.com", "freemium", "proprietary", ["personal"],
    "Factorial führt Personalakten, Urlaub und Arbeitszeiten.",
    "Factorial speichert Mitarbeitende, Abwesenheiten und Dokumente. Der Dienst kommt aus Barcelona. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Personalakten und Urlaub", "Arbeitszeiten und Dokumente", "Einstieg und bezahlte Stufen"],
    ["Urlaubsanträge in einem Team zu sammeln", "Personalunterlagen digital abzulegen"], False)
add("Kenjo", "https://www.kenjo.io/", "kenjo.io", "freemium", "proprietary", ["personal"],
    "Kenjo plant Schichten, Urlaub und Personalakten.",
    "Kenjo legt Dienstpläne und Abwesenheiten an und speichert Stammdaten. Der Anbieter sitzt in Berlin. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Dienstpläne und Urlaub", "Personalakten", "Einstieg und bezahlte Stufen"],
    ["Einen Schichtplan für ein Team zu bauen", "Urlaub neben den Schichten zu sehen"], False)
add("Deel", "https://www.deel.com/", "deel.com", "paid", "proprietary", ["personal"],
    "Deel stellt Verträge und Lohn für Beschäftigte in anderen Ländern bereit.",
    "Deel führt Verträge, Lohn und Nachweise für internationale Teams. Die Nutzung richtet sich an Arbeitgeber mit Beschäftigten im Ausland. Sie ist kostenpflichtig.",
    ["Verträge und Lohn international", "Nachweise je Land", "Kostenpflichtige Nutzung"],
    ["Eine Person im Ausland anzustellen", "Lohnabrechnungen über Länder hinweg zu sammeln"], False)
add("Remote", "https://www.remote.com/", "remote.com", "paid", "proprietary", ["personal"],
    "Remote übernimmt Beschäftigung und Lohn für Teams in mehreren Ländern.",
    "Remote stellt lokale Verträge und Gehaltszahlung bereit, ohne dass das Unternehmen in jedem Land eine Gesellschaft braucht. Die Nutzung ist kostenpflichtig.",
    ["Lokale Verträge", "Gehaltszahlung in mehreren Ländern", "Kostenpflichtige Nutzung"],
    ["Eine Person im Ausland zu beschäftigen", "Lohn ohne eigene Landesgesellschaft zu zahlen"], False)
add("HiBob", "https://www.hibob.com/", "hibob.com", "paid", "proprietary", ["personal"],
    "HiBob führt Personalakten, Urlaub und Organigramme.",
    "HiBob speichert Stammdaten, Abwesenheiten und Organisationsstrukturen. Die Oberfläche richtet sich an Personalteams. Die Nutzung ist kostenpflichtig.",
    ["Personalakten und Organigramm", "Urlaub und Stammdaten", "Kostenpflichtige Nutzung"],
    ["Eine Personalakte für ein wachsendes Team zu führen", "Ein Organigramm aktuell zu halten"], False)
add("Groq", "https://groq.com/", "groq.com", "freemium", "proprietary", ["ki-chatbots", "programmierung"],
    "Groq stellt Sprachmodelle über eine schnelle Schnittstelle bereit.",
    "Groq betreibt eigene Rechner für Inferenz und bietet darüber Modelle per API und in einer Konsole an. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Schnittstelle für Sprachmodelle", "Konsole und API", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Ein Modell mit kurzer Antwortzeit anzubinden", "Antworten in einer Konsole zu testen"], False)
add("Cohere", "https://cohere.com/", "cohere.com", "freemium", "proprietary", ["ki-chatbots", "programmierung"],
    "Cohere bietet Sprachmodelle für Text, Suche und Unternehmensanwendungen.",
    "Cohere stellt Modelle über eine Schnittstelle bereit, unter anderem für Texte und Embeddings. Es gibt einen kostenlosen Einstieg und bezahlte Nutzung.",
    ["Sprachmodelle und Embeddings", "Schnittstelle für Anwendungen", "Kostenloser Einstieg und bezahlte Nutzung"],
    ["Texte über eine API zu erzeugen", "Dokumente für eine Suche zu vektorisieren"], False)
add("Stability AI", "https://stability.ai/", "stability.ai", "freemium", "proprietary", ["bildgenerierung"],
    "Stability AI entwickelt Bildmodelle und bietet sie über eine Plattform an.",
    "Stability AI stellt Modelle der Stable-Reihe für Bilder bereit. Die Erzeugung läuft über die Plattform und eine Schnittstelle. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Bildmodelle der Stable-Reihe", "Plattform und Schnittstelle", "Einstieg und bezahlte Kontingente"],
    ["Ein Bild aus Text zu erzeugen", "Ein Modell in eine eigene Anwendung einzubinden"], False)
add("fal", "https://fal.ai/", "fal.ai", "freemium", "proprietary", ["bildgenerierung", "programmierung"],
    "fal führt Bild- und Videomodelle über eine Schnittstelle aus.",
    "fal bietet gehostete Modelle, die man per API aufruft, ohne sie selbst zu betreiben. Die Abrechnung folgt der Nutzung. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Gehostete Bild- und Videomodelle", "Aufruf per API", "Einstieg und bezahlte Kontingente"],
    ["Ein Bildmodell ohne eigenen Server aufzurufen", "Mehrere Modelle über dieselbe Schnittstelle zu testen"], False)
add("Replicate", "https://replicate.com/", "replicate.com", "freemium", "proprietary", ["programmierung", "bildgenerierung"],
    "Replicate führt veröffentlichte Modelle in der Cloud aus.",
    "Replicate startet Modelle für Bild, Ton und Text per API, ohne dass man die Gewichte selbst hostet. Die Abrechnung folgt der Laufzeit. Es gibt einen Einstieg und bezahlte Nutzung.",
    ["Modelle per API", "Bild, Ton und Text", "Einstieg und bezahlte Nutzung"],
    ["Ein veröffentlichtes Modell auszuprobieren", "Eine Bildfunktion ohne eigene GPU anzubinden"], False)
add("Fireworks AI", "https://fireworks.ai/", "fireworks.ai", "freemium", "proprietary", ["programmierung", "ki-chatbots"],
    "Fireworks AI stellt Sprach- und Bildmodelle über eine schnelle API bereit.",
    "Fireworks hostet Modelle und rechnet Aufrufe ab. Die Konsole dient zum Testen. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Gehostete Sprach- und Bildmodelle", "Konsole zum Testen", "Einstieg und bezahlte Kontingente"],
    ["Ein Modell in eine Anwendung einzubinden", "Antwortzeiten verschiedener Modelle zu vergleichen"], False)
add("Krea", "https://www.krea.ai/", "krea.ai", "freemium", "proprietary", ["bildgenerierung", "design"],
    "Krea erzeugt und bearbeitet Bilder in Echtzeit aus Skizzen und Text.",
    "Krea zeigt eine Fläche, auf der aus einer Skizze oder einem Prompt ein Bild entsteht und sich weiterziehen lässt. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Bilder aus Skizze und Text", "Bearbeitung in Echtzeit", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Idee als Bild zu skizzieren", "Ein Motiv schrittweise zu verändern"], True)
add("Recraft", "https://www.recraft.ai/", "recraft.ai", "freemium", "proprietary", ["design", "bildgenerierung"],
    "Recraft erzeugt Vektoren, Icons und Illustrationen aus Text.",
    "Recraft liefert Grafiken, die sich als Vektor weiterbearbeiten lassen, und hält Stilvorgaben über mehrere Bilder. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Vektoren und Icons aus Text", "Stil über mehrere Bilder", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Icon-Set in einem Stil zu erzeugen", "Eine Illustration als Vektor zu starten"], True)
add("Photoroom", "https://www.photoroom.com/", "photoroom.com", "freemium", "proprietary", ["bildgenerierung", "e-commerce"],
    "Photoroom entfernt Hintergründe und setzt Produktfotos in Szene.",
    "Photoroom freistellt Gegenstände und legt sie auf Hintergründe oder in Vorlagen für den Verkauf. Die Arbeit läuft in der App und im Browser. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Freistellen von Produktfotos", "Vorlagen für den Verkauf", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Produktfoto für einen Shop vorzubereiten", "Den Hintergrund eines Gegenstands zu tauschen"], True)
add("Pixelcut", "https://www.pixelcut.ai/", "pixelcut.ai", "freemium", "proprietary", ["bildgenerierung"],
    "Pixelcut entfernt Hintergründe und erzeugt Produktbilder aus einem Foto.",
    "Pixelcut freistellt Objekte und bietet Vorlagen für Anzeigen und Shops. Die Bearbeitung läuft in der App. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Freistellen und Vorlagen", "Produktbilder aus einem Foto", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Foto für eine Anzeige freizustellen", "Einen Gegenstand auf einen neuen Hintergrund zu setzen"], True)
add("Grok", "https://grok.com/", "grok.com", "freemium", "proprietary", ["ki-chatbots"],
    "Grok beantwortet Fragen im Chat von xAI.",
    "Grok führt ein Gespräch im Browser und kann bei angebundenen Konten auf aktuelle Beiträge zugreifen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Chat für Fragen", "Zugang über grok.com", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Frage im Chat zu stellen", "Einen Textentwurf gegenzulesen"], True)
add("Google AI Studio", "https://aistudio.google.com/", "aistudio.google.com", "free", "proprietary", ["programmierung", "ki-chatbots"],
    "Google AI Studio testet Gemini-Modelle und baut daraus einen Prompt.",
    "In AI Studio lässt sich ein Prompt gegen Gemini-Modelle ausprobieren und als Schlüssel für eine Anwendung übernehmen. Die Testoberfläche ist ohne separates Abo nutzbar. Die spätere API-Nutzung kann Kosten verursachen.",
    ["Prompts gegen Gemini testen", "Schlüssel für die API", "Testoberfläche ohne separates Abo"],
    ["Einen Prompt zu erproben, bevor er in eine App wandert", "Zwei Gemini-Modelle an derselben Aufgabe zu vergleichen"], False)
add("NotebookLM", "https://notebooklm.google.com/", "notebooklm.google.com", "free", "proprietary", ["recherche", "ki-chatbots"],
    "NotebookLM beantwortet Fragen anhand hochgeladener Quellen.",
    "NotebookLM nimmt Dokumente entgegen und antwortet nur auf dieser Grundlage, mit Verweisen auf die Stellen. Die Nutzung ist ohne separates Abo möglich.",
    ["Fragen an eigene Dokumente", "Verweise auf Stellen", "Nutzung ohne separates Abo"],
    ["Ein langes Dokument gezielt zu befragen", "Mehrere Quellen gegenüberzustellen"], True)
add("Adobe Express", "https://express.adobe.com/", "express.adobe.com", "freemium", "proprietary", ["design"],
    "Adobe Express baut Social-Media-Grafiken, Flyer und kurze Videos im Browser.",
    "Adobe Express stellt Vorlagen für Beiträge, Flyer und Clips bereit und füllt sie mit Text und Bild. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Vorlagen für Beiträge und Flyer", "Kurze Videos", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Beitrag für ein soziales Netzwerk zu gestalten", "Einen Flyer aus einer Vorlage zu füllen"], True)
add("Lightroom", "https://lightroom.adobe.com/", "lightroom.adobe.com", "freemium", "proprietary", ["design"],
    "Lightroom entwickelt Fotos und gleicht sie über die Adobe-Cloud ab.",
    "Lightroom sortiert Aufnahmen und setzt Belichtung, Farbe und Ausschnitt, ohne die Originaldatei zu überschreiben. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Entwicklung von Farbe und Belichtung", "Abgleich über die Cloud", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Fotoserie farblich anzugleichen", "Bilder auf mehreren Geräten zu bearbeiten"], True)
add("Bolt", "https://bolt.new/", "bolt.new", "freemium", "proprietary", ["programmierung"],
    "Bolt erzeugt aus einer Beschreibung eine lauffähige Webanwendung im Browser.",
    "Bolt schreibt ein Projekt aus einem Prompt und zeigt die Vorschau direkt. Änderungen lassen sich im Chat nachreichen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Anwendung aus einem Prompt", "Vorschau im Browser", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Prototyp ohne lokale Einrichtung zu starten", "Eine Oberfläche im Chat nachzuziehen"], True)
add("v0", "https://v0.app/", "v0.app", "freemium", "proprietary", ["programmierung", "design"],
    "v0 erzeugt Oberflächen aus einer Beschreibung und liefert den zugehörigen Code.",
    "v0 baut Komponenten und Seiten aus einem Prompt und zeigt sie in der Vorschau. Der Code lässt sich übernehmen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Oberflächen aus einem Prompt", "Code zur Vorschau", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Seite als Entwurf zu generieren", "Eine Komponente in ein Projekt zu übernehmen"], False)
add("dejure.org", "https://dejure.org/", "dejure.org", "free", "unknown", ["recht"],
    "dejure.org verlinkt deutsche Gesetze und Entscheidungen im Volltext.",
    "dejure.org zeigt Paragraphen und verknüpft sie mit Fundstellen und Entscheidungen. Die Seiten sind ohne Konto lesbar. Eine OSI-Lizenz der Website ist hier nicht hinterlegt.",
    ["Gesetze und Entscheidungen", "Verknüpfte Fundstellen", "Lesen ohne Konto"],
    ["Einen Paragraphen nachzuschlagen", "Entscheidungen zu einer Norm zu finden"], True)
add("openJur", "https://openjur.de/", "openjur.de", "free", "unknown", ["recht"],
    "openJur veröffentlicht Entscheidungen deutscher Gerichte im Volltext.",
    "openJur durchsucht Urteile und Beschlüsse und zeigt den Text ohne Bezahlschranke. Die Suche ist ohne Konto möglich. Eine OSI-Lizenz der Plattform ist hier nicht hinterlegt.",
    ["Volltexte von Entscheidungen", "Suche ohne Bezahlschranke", "Nutzung ohne Konto"],
    ["Ein Urteil im Volltext zu lesen", "Entscheidungen zu einem Stichwort zu finden"], True)
add("EUR-Lex", "https://eur-lex.europa.eu/", "eur-lex.europa.eu", "free", "proprietary", ["recht"],
    "EUR-Lex ist die Amtssammlung für Recht der Europäischen Union.",
    "EUR-Lex veröffentlicht Verordnungen, Richtlinien und Urteile der EU in den Amtssprachen. Die Dokumente sind ohne Konto lesbar. Der Dienst ist ein Angebot der EU-Organe.",
    ["Verordnungen und Richtlinien", "Urteile der EU-Gerichte", "Lesen ohne Konto"],
    ["Eine EU-Verordnung im Wortlaut zu lesen", "Eine Richtlinie in der deutschen Fassung zu finden"], True)
add("DSGVO-Gesetz", "https://dsgvo-gesetz.de/", "dsgvo-gesetz.de", "free", "unknown", ["recht"],
    "DSGVO-Gesetz zeigt den Text der Datenschutz-Grundverordnung mit Erläuterungen.",
    "Die Seite stellt die Artikel der DSGVO dar und verknüpft sie mit kurzen Hinweisen. Das Lesen ist ohne Konto möglich. Eine OSI-Lizenz der Website ist hier nicht hinterlegt.",
    ["Wortlaut der DSGVO", "Artikel mit Hinweisen", "Lesen ohne Konto"],
    ["Einen Artikel der DSGVO nachzuschlagen", "Den Aufbau der Verordnung zu überblicken"], True)
add("dict.cc", "https://www.dict.cc/", "dict.cc", "free", "proprietary", ["bildung"],
    "dict.cc übersetzt Wörter zwischen Deutsch und vielen anderen Sprachen.",
    "dict.cc zeigt Wortpaare mit Beispielsätzen und Aussprache. Die Suche ist ohne Konto möglich. Die Wörterbücher sind ein proprietäres Angebot.",
    ["Wortpaare und Beispielsätze", "Mehrere Sprachen neben Deutsch", "Suche ohne Konto"],
    ["Ein Wort ins Englische zu übersetzen", "Beispielsätze zu einer Vokabel zu lesen"], True)
add("PONS", "https://de.pons.com/", "de.pons.com", "freemium", "proprietary", ["bildung"],
    "PONS übersetzt Wörter und kurze Wendungen, mit Schwerpunkt auf dem Schulunterricht.",
    "PONS zeigt Übersetzungen, Beispiele und Beugungen. Ein Teil der Suche ist ohne Abo nutzbar, Übungen und weitere Inhalte liegen in bezahlten Stufen.",
    ["Übersetzungen und Beispiele", "Beugungen", "Kostenloser Anteil und bezahlte Stufen"],
    ["Eine Vokabel mit Beispiel nachzuschlagen", "Eine Wendung in eine andere Sprache zu übertragen"], True)
add("RYTE", "https://www.ryte.com/", "ryte.com", "freemium", "proprietary", ["seo"],
    "RYTE prüft Websites auf technische Fehler und Inhalte für die Suche.",
    "RYTE crawlt eine Website und zeigt Fehler bei Indexierung, Links und Inhalten. Der Anbieter kommt aus München. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Crawl auf technische Fehler", "Hinweise zu Inhalten", "Einstieg und bezahlte Stufen"],
    ["Fehlerhafte Seiten einer Website zu finden", "Eine Domain vor einem Relaunch zu prüfen"], False)
add("Prezi", "https://prezi.com/", "prezi.com", "freemium", "proprietary", ["praesentationen"],
    "Prezi baut Präsentationen auf einer großen Fläche statt nur als Folienstapel.",
    "Prezi zoomt zwischen Übersicht und Detail. Die Datei liegt im Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Präsentation als Fläche", "Zoom zwischen Übersicht und Detail", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Vortrag mit einer Übersichtskarte zu bauen", "Zwischen Themen zu zoomen statt zu blättern"], True)
add("Mentimeter", "https://www.mentimeter.com/", "mentimeter.com", "freemium", "proprietary", ["praesentationen", "bildung"],
    "Mentimeter sammelt Live-Abstimmung und Wortwolken in einer Präsentation.",
    "Mentimeter legt Folien mit Fragen an, die das Publikum mit dem Handy beantwortet. Die Ergebnisse erscheinen sofort. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Live-Abstimmung", "Wortwolken und Quiz", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Abstimmung in einem Vortrag zu starten", "Rückmeldungen eines Kurses zu sammeln"], True)
add("Kahoot", "https://kahoot.com/", "kahoot.com", "freemium", "proprietary", ["bildung"],
    "Kahoot macht aus Fragen ein Live-Quiz für Gruppen.",
    "Kahoot zeigt Fragen auf einem gemeinsamen Bildschirm, die Teilnehmenden antworten auf dem eigenen Gerät. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Live-Quiz für Gruppen", "Antworten auf dem eigenen Gerät", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Quiz in einem Kurs zu spielen", "Wissen in einer Runde abzufragen"], True)
add("Nomad Sculpt", "https://nomadsculpt.com/", "nomadsculpt.com", "paid", "proprietary", ["dreid"],
    "Nomad Sculpt formt digitale Skulpturen auf dem Tablet.",
    "Nomad Sculpt arbeitet mit virtuellem Ton, Farben und Export für den Druck oder für andere 3D-Programme. Die App ist kostenpflichtig.",
    ["Digitale Skulptur auf dem Tablet", "Export für Druck und andere Programme", "Kostenpflichtige App"],
    ["Eine Figur auf dem Tablet zu modellieren", "Ein Modell für den Druck zu exportieren"], False)
add("RawTherapee", "https://www.rawtherapee.com/", "rawtherapee.com", "free", "open_source", ["design"],
    "RawTherapee entwickelt Raw-Dateien mit feinen Reglern auf dem eigenen Rechner.",
    "RawTherapee öffnet Kameradateien und stellt Belichtung, Farbe, Rauschen und Schärfe ein. Die Bearbeitung bleibt lokal. Die SPDX-Kennung des Repositories ist GPL-3.0. Die Anwendung ist ohne Pflichtabo nutzbar.",
    ["Raw-Entwicklung", "Lokale Bearbeitung", "Lizenz GPL-3.0"],
    ["Eine Raw-Datei genau zu entwickeln", "Rauschen und Schärfe lokal zu steuern"], False,
    oss("https://github.com/RawTherapee/RawTherapee", "GPL-3.0", "https://www.rawtherapee.com/"))
add("LosslessCut", "https://losslesscut.app/", "losslesscut.app", "free", "open_source", ["videoschnitt"],
    "LosslessCut schneidet Video- und Audiodateien ohne erneutes Encodieren.",
    "LosslessCut setzt Schnittmarken und schreibt die Abschnitte neu, ohne die Bildqualität neu zu rechnen. Die SPDX-Kennung des Repositories ist GPL-2.0. Die Anwendung ist ohne Pflichtabo nutzbar.",
    ["Schnitt ohne neues Encodieren", "Video und Audio", "Lizenz GPL-2.0"],
    ["Einen Clip verlustarm zu kürzen", "Eine lange Aufnahme in Abschnitte zu teilen"], True,
    oss("https://github.com/mifi/lossless-cut", "GPL-2.0", "https://losslesscut.app/"))
add("Pitivi", "https://pitivi.org/", "pitivi.org", "free", "unknown", ["videoschnitt"],
    "Pitivi schneidet Videos auf dem eigenen Rechner.",
    "Pitivi legt Clips auf eine Timeline und exportiert das Ergebnis. Die Anwendung richtet sich an den Desktop. Eine OSI-Kennung wurde in diesem Durchgang nicht bestätigt. Sie ist ohne Pflichtabo erhältlich.",
    ["Timeline und Export", "Desktop-Anwendung", "Betrieb ohne Pflichtabo"],
    ["Ein Video ohne Abo zu schneiden", "Einen Clip mit Tonspur zu kürzen"], False)
add("Natron", "https://natron.fr/", "natron.fr", "free", "open_source", ["videoschnitt"],
    "Natron setzt visuelle Effekte als Knotengraph auf Videomaterial.",
    "Natron verbindet Knoten für Keying, Farbe und Compositing. Die Projekte bleiben lokal. Die SPDX-Kennung des Repositories ist GPL-2.0. Die Anwendung ist ohne Pflichtabo nutzbar.",
    ["Compositing als Knotengraph", "Keying und Farbe", "Lizenz GPL-2.0"],
    ["Eine Szene mit Effekten zu kombinieren", "Einen Greenscreen lokal freizustellen"], False,
    oss("https://github.com/NatronGitHub/Natron", "GPL-2.0", "https://natron.fr/"))
add("Olive", "https://www.olivevideoeditor.org/", "olivevideoeditor.org", "free", "open_source", ["videoschnitt"],
    "Olive schneidet Videos mit einer Timeline auf dem eigenen Rechner.",
    "Olive setzt Clips, Überblendungen und Effekte auf Spuren und exportiert eine Datei. Die SPDX-Kennung des Repositories ist GPL-3.0. Die Anwendung ist ohne Pflichtabo nutzbar.",
    ["Timeline mit Effekten", "Export als Datei", "Lizenz GPL-3.0"],
    ["Einen Schnitt ohne Abo zu beginnen", "Eine Überblendung lokal zu setzen"], False,
    oss("https://github.com/olive-editor/olive", "GPL-3.0", "https://www.olivevideoeditor.org/"))
add("Chatwoot", "https://www.chatwoot.com/", "chatwoot.com", "freemium", "unknown", ["kundenservice"],
    "Chatwoot sammelt Website-Chat, Mail und soziale Kanäle in einem Posteingang.",
    "Chatwoot legt Gespräche in einem gemeinsamen Posteingang ab und lässt sich selbst betreiben. Die Lizenzdatei des Repositories ist nicht durchgängig eine OSI-Lizenz, der Lizenztyp bleibt Unbekannt. Daneben gibt es eine Cloud mit Einstieg und bezahlten Stufen.",
    ["Gemeinsamer Posteingang", "Chat, Mail und weitere Kanäle", "Cloud und Selbstbetrieb"],
    ["Einen Website-Chat selbst zu hosten", "Mehrere Kanäle in einem Posteingang zu lesen"], False)
add("Front", "https://front.com/", "front.com", "paid", "proprietary", ["kundenservice"],
    "Front legt Team-Postfächer und gemeinsame Antworten an einem Ort ab.",
    "Front sammelt E-Mail und weitere Kanäle in einem gemeinsamen Posteingang mit Zuweisung und internen Kommentaren. Die Nutzung ist kostenpflichtig.",
    ["Gemeinsame Postfächer", "Zuweisung und Kommentare", "Kostenpflichtige Nutzung"],
    ["Support-Mail im Team zu beantworten", "Eine Anfrage einer Person zuzuweisen"], False)
add("Gorgias", "https://www.gorgias.com/", "gorgias.com", "paid", "proprietary", ["kundenservice", "e-commerce"],
    "Gorgias beantwortet Kundenanfragen von Shops aus Mail, Chat und sozialen Kanälen.",
    "Gorgias zeigt die Bestellung neben der Nachricht und legt Antworten als Tickets ab. Der Dienst richtet sich an Online-Händler. Die Nutzung ist kostenpflichtig.",
    ["Tickets neben der Bestellung", "Mail, Chat und soziale Kanäle", "Kostenpflichtige Nutzung"],
    ["Eine Shop-Anfrage mit der Bestellung zu beantworten", "Support für einen Onlineshop zu bündeln"], False)
add("GameMaker", "https://gamemaker.io/", "gamemaker.io", "freemium", "proprietary", ["gaming"],
    "GameMaker baut 2D-Spiele mit einer eigenen Skriptsprache und einem Editor.",
    "GameMaker setzt Räume, Objekte und Ereignisse zusammen und exportiert das Spiel. Es gibt einen kostenlosen Einstieg und bezahlte Lizenzen für den Export auf weitere Plattformen.",
    ["2D-Editor mit Objekten und Ereignissen", "Export des Spiels", "Kostenloser Einstieg und bezahlte Lizenzen"],
    ["Ein 2D-Spiel zu prototypen", "Ein Spiel auf eine weitere Plattform zu bringen"], False)
add("Defold", "https://defold.com/", "defold.com", "free", "unknown", ["gaming"],
    "Defold ist eine Engine für 2D-Spiele, die sich ohne Lizenzgebühr nutzen lässt.",
    "Defold bringt Editor, Szenen und Skripte in Lua mit und exportiert auf mehrere Plattformen. Eine OSI-Kennung wurde hier nicht bestätigt. Eine Engine-Gebühr nennt die Website nicht.",
    ["2D-Engine mit Lua", "Export auf mehrere Plattformen", "Nutzung ohne Engine-Gebühr"],
    ["Ein 2D-Spiel ohne Lizenzgebühr zu bauen", "Einen Prototyp auf ein Handy zu exportieren"], False)
add("TIC-80", "https://tic80.com/", "tic80.com", "freemium", "proprietary", ["gaming"],
    "TIC-80 ist eine Fantasy-Konsole für kleine Spiele mit begrenzter Auflösung.",
    "TIC-80 stellt Code, Sprites, Karten und Ton in einem Fenster bereit. Die kostenlose Fassung lässt sich ausprobieren, der Export und weitere Funktionen sind bezahlt.",
    ["Code, Sprites und Ton in einem Fenster", "Begrenzte Auflösung", "Kostenlose Fassung und bezahlte Funktionen"],
    ["Ein kleines Spiel in einem begrenzten Rahmen zu schreiben", "Sprites und Code nebeneinander zu bearbeiten"], False)
add("bitsy", "https://bitsy.org/", "bitsy.org", "free", "open_source", ["gaming"],
    "bitsy baut kleine Spiele im Browser aus Räumen, Sprites und Dialog.",
    "bitsy setzt Räume und Figuren in einem begrenzten Raster und schreibt kurze Texte dazu. Die SPDX-Kennung des Repositories ist MIT. Die Nutzung im Browser ist ohne Abo möglich.",
    ["Räume und Sprites im Browser", "Kurze Dialoge", "Lizenz MIT"],
    ["Ein kurzes Spiel ohne Installation zu bauen", "Eine kleine Geschichte mit einer Figur zu erzählen"], True,
    oss("https://github.com/le-doux/bitsy", "MIT", "https://bitsy.org/"))
add("Qdrant", "https://qdrant.tech/", "qdrant.tech", "freemium", "open_source", ["daten", "programmierung"],
    "Qdrant speichert Vektoren für die Ähnlichkeitssuche und lässt sich selbst betreiben.",
    "Qdrant legt Embeddings ab und beantwortet Ähnlichkeitsanfragen. Die SPDX-Kennung ist Apache-2.0. Daneben gibt es eine Cloud mit Einstieg und bezahlten Stufen.",
    ["Vektorensuche", "Selbstbetrieb unter Apache-2.0", "Cloud mit Einstieg und bezahlten Stufen"],
    ["Eine Ähnlichkeitssuche selbst zu hosten", "Embeddings einer Anwendung abzulegen"], False,
    oss("https://github.com/qdrant/qdrant", "Apache-2.0", "https://qdrant.tech/"))
add("Valkey", "https://valkey.io/", "valkey.io", "free", "open_source", ["daten", "programmierung"],
    "Valkey ist ein Schlüssel-Wert-Speicher im Speicher, hervorgegangen aus Redis.",
    "Valkey hält Daten im Arbeitsspeicher und spricht ein zu Redis kompatibles Protokoll. Die SPDX-Kennung ist BSD-3-Clause. Die Software ist ohne Pflichtabo nutzbar.",
    ["Schlüssel-Wert-Speicher im Speicher", "Protokoll nahe an Redis", "Lizenz BSD-3-Clause"],
    ["Einen Cache auf dem eigenen Server zu betreiben", "Sitzungsdaten schnell abzulegen"], False,
    oss("https://github.com/valkey-io/valkey", "BSD-3-Clause", "https://valkey.io/"))
add("MariaDB", "https://mariadb.org/", "mariadb.org", "free", "open_source", ["daten", "programmierung"],
    "MariaDB ist ein relationaler Datenbankserver, verwandt mit MySQL.",
    "MariaDB speichert Tabellen und beantwortet SQL. Die SPDX-Kennung des Server-Repositories ist GPL-2.0. Der Server ist ohne Pflichtabo nutzbar.",
    ["Relationale Tabellen und SQL", "Betrieb auf dem eigenen Server", "Lizenz GPL-2.0"],
    ["Eine Anwendungsdatenbank selbst zu betreiben", "SQL auf dem eigenen Server auszuführen"], False,
    oss("https://github.com/MariaDB/server", "GPL-2.0", "https://mariadb.org/"))
add("MLflow", "https://mlflow.org/", "mlflow.org", "free", "open_source", ["daten", "programmierung"],
    "MLflow protokolliert Experimente, Modelle und Läufe beim Training.",
    "MLflow speichert Parameter, Metriken und Modelldateien eines Trainingslaufs. Die SPDX-Kennung ist Apache-2.0. Der Dienst lässt sich selbst betreiben.",
    ["Protokoll von Experimenten", "Modelle und Metriken", "Lizenz Apache-2.0"],
    ["Trainingsläufe vergleichbar abzulegen", "Ein Modell mit seinen Parametern zu sichern"], False,
    oss("https://github.com/mlflow/mlflow", "Apache-2.0", "https://mlflow.org/"))
add("Label Studio", "https://labelstud.io/", "labelstud.io", "freemium", "open_source", ["daten"],
    "Label Studio beschriftet Daten für das Training und lässt sich selbst betreiben.",
    "Label Studio legt Aufgaben für Text, Bild und Ton an und sammelt die Markierungen. Die SPDX-Kennung ist Apache-2.0. Daneben gibt es eine Cloud mit bezahlten Stufen.",
    ["Markierung von Text, Bild und Ton", "Selbstbetrieb unter Apache-2.0", "Cloud mit bezahlten Stufen"],
    ["Trainingsdaten im Team zu beschriften", "Eine Beschriftung selbst zu hosten"], False,
    oss("https://github.com/HumanSignal/label-studio", "Apache-2.0", "https://labelstud.io/"))
add("Jupyter", "https://jupyter.org/", "jupyter.org", "free", "open_source", ["programmierung", "daten"],
    "Jupyter mischt Code, Text und Grafiken in Notizbüchern.",
    "Jupyter führt Code in Zellen aus und zeigt das Ergebnis darunter. Die SPDX-Kennung des genannten Repositories ist BSD-3-Clause. Der Betrieb ist ohne Pflichtabo möglich.",
    ["Notizbücher mit Code und Text", "Ausgabe direkt unter der Zelle", "Lizenz BSD-3-Clause"],
    ["Eine Datenauswertung Schritt für Schritt zu notieren", "Code und Erklärung in einer Datei zu halten"], True,
    oss("https://github.com/jupyter/jupyter", "BSD-3-Clause", "https://jupyter.org/"))
add("Podman", "https://podman.io/", "podman.io", "free", "open_source", ["programmierung"],
    "Podman startet Container auf dem eigenen Rechner ohne einen zentralen Daemon.",
    "Podman baut und startet Container aus Images, ähnlich wie Docker, und kann Pods gruppieren. Die SPDX-Kennung ist Apache-2.0. Die Software ist ohne Pflichtabo nutzbar.",
    ["Container ohne zentralen Daemon", "Images und Pods", "Lizenz Apache-2.0"],
    ["Einen Container lokal zu starten", "Ein Image ohne Docker-Daemon zu bauen"], False,
    oss("https://github.com/containers/podman", "Apache-2.0", "https://podman.io/"))
add("RustDesk", "https://rustdesk.com/", "rustdesk.com", "freemium", "open_source", ["programmierung"],
    "RustDesk öffnet einen Fernzugriff auf einen Rechner und lässt den Server selbst betreiben.",
    "RustDesk zeigt den Bildschirm eines anderen Rechners und kann Dateien übertragen. Die SPDX-Kennung ist AGPL-3.0. Den Vermittlungsserver kann man selbst hosten. Daneben gibt es bezahlte Angebote.",
    ["Fernzugriff auf den Bildschirm", "Eigener Vermittlungsserver", "Lizenz AGPL-3.0"],
    ["Einen Rechner aus der Ferne zu bedienen", "Den Vermittlungsserver selbst zu betreiben"], False,
    oss("https://github.com/rustdesk/rustdesk", "AGPL-3.0", "https://rustdesk.com/"))
add("Clockodo", "https://www.clockodo.com/", "clockodo.com", "freemium", "proprietary", ["personal", "produktivitaet"],
    "Clockodo erfasst Arbeitszeiten und macht daraus Auswertungen für Teams in Deutschland.",
    "Clockodo startet und stoppt Zeiten, ordnet sie Projekten zu und bereitet Berichte vor. Der Anbieter sitzt in Deutschland. Es gibt einen Test und kostenpflichtige Tarife.",
    ["Zeiterfassung nach Projekt", "Berichte für Teams", "Test und kostenpflichtige Tarife"],
    ["Stunden für eine Rechnung festzuhalten", "Die Auslastung eines Teams zu sehen"], True)
add("Toggl Track", "https://toggl.com/", "toggl.com", "freemium", "proprietary", ["produktivitaet"],
    "Toggl Track misst Arbeitszeit mit einem Timer und Berichten.",
    "Toggl startet einen Timer je Aufgabe und zeigt die Summe nach Projekt und Person. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Timer je Aufgabe", "Berichte nach Projekt", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Die Zeit an einer Aufgabe zu messen", "Wochenstunden nach Projekt zu sehen"], True)
add("Clockify", "https://clockify.me/", "clockify.me", "freemium", "proprietary", ["produktivitaet"],
    "Clockify erfasst Zeiten und erstellt daraus Berichte für Teams.",
    "Clockify bietet Timer und manuelle Einträge und gruppiert sie nach Projekt. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Timer und manuelle Einträge", "Berichte nach Projekt", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Arbeitszeit eines Teams zu erfassen", "Stunden für eine Abrechnung zu summieren"], True)
add("Todoist", "https://todoist.com/", "todoist.com", "freemium", "proprietary", ["produktivitaet"],
    "Todoist sammelt Aufgaben mit Fälligkeit, Projekten und Priorität.",
    "Todoist legt Aufgaben in Projekte und zeigt, was heute fällig ist. Geteilte Projekte gibt es für Teams. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Aufgaben mit Fälligkeit", "Projekte und Priorität", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Tagesliste zu führen", "Aufgaben in einem gemeinsamen Projekt zu verteilen"], True)
add("Calendly", "https://calendly.com/", "calendly.com", "freemium", "proprietary", ["produktivitaet"],
    "Calendly vergibt Termine über einen Link in die freien Lücken des Kalenders.",
    "Calendly zeigt freie Zeiten und schreibt den Termin in den verbundenen Kalender. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Terminseiten mit freien Zeiten", "Eintrag im Kalender", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Terminlink zu verschicken", "Doppelte Buchungen zu vermeiden"], True)
add("Pipedrive", "https://www.pipedrive.com/", "pipedrive.com", "paid", "proprietary", ["marketing"],
    "Pipedrive führt Verkaufschancen in einer Pipeline von der Anfrage bis zum Abschluss.",
    "Pipedrive legt Deals in Phasen an und erinnert an den nächsten Schritt. Der Dienst kommt aus Estland und ist in Deutschland verbreitet. Die Nutzung ist kostenpflichtig.",
    ["Pipeline für Verkaufschancen", "Erinnerung an den nächsten Schritt", "Kostenpflichtige Nutzung"],
    ["Offene Angebote nach Phase zu sehen", "Einen Deal bis zum Abschluss zu führen"], False)
add("HubSpot", "https://www.hubspot.com/", "hubspot.com", "freemium", "proprietary", ["marketing", "kundenservice"],
    "HubSpot bündelt Kontakte, E-Mail, Formulare und einen Service-Posteingang.",
    "HubSpot speichert Kontakte und zeigt, welche Seiten und Mails sie gesehen haben. CRM, Marketing und Service lassen sich kombinieren. Es gibt kostenlose Werkzeuge und bezahlte Stufen.",
    ["Kontakte und Formulare", "E-Mail und Service-Posteingang", "Kostenlose Werkzeuge und bezahlte Stufen"],
    ["Anfragen aus einem Formular im CRM zu sehen", "Eine E-Mail an eine Kontaktliste zu schicken"], False)
add("Attio", "https://attio.com/", "attio.com", "freemium", "proprietary", ["marketing"],
    "Attio ist ein CRM, das Kontakte und Unternehmen flexibel als Datenmodell ablegt.",
    "Attio speichert Personen, Firmen und eigene Objekte und zeigt sie als Liste oder Pipeline. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Kontakte und Unternehmen", "Eigene Objekte und Pipelines", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein leichtes CRM für ein kleines Team zu führen", "Verkaufschancen als Pipeline zu sehen"], False)
add("Odoo", "https://www.odoo.com/", "odoo.com", "freemium", "unknown", ["e-commerce", "personal"],
    "Odoo bündelt Shop, Rechnungen, Lager und Personal in einer Suite.",
    "Odoo schaltet Module für Verkauf, Lager, Buchhaltung und Personal zu. Eine Community-Ausgabe lässt sich selbst betreiben, die Enterprise-Ausgabe ist bezahlt. Eine einzelne OSI-Kennung für die ganze Suite wird hier nicht eingetragen.",
    ["Module für Shop, Lager und Personal", "Community-Ausgabe und Enterprise", "Lizenz der Suite nicht als eine OSI-Kennung geführt"],
    ["Einen kleinen Betrieb in einer Suite zu führen", "Shop und Lager zu verbinden"], False)
add("7Mind", "https://www.7mind.de/", "7mind.de", "freemium", "proprietary", ["gesundheit"],
    "7Mind führt durch Meditationen und Kurse auf Deutsch.",
    "7Mind spielt angeleitete Sitzungen und Kurse zu Schlaf, Fokus und Alltag. Der Dienst kommt aus Deutschland. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Meditationen auf Deutsch", "Kurse zu Schlaf und Fokus", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine kurze Meditation auf Deutsch zu starten", "Einen Kurs über mehrere Tage zu hören"], True)
add("flowkey", "https://www.flowkey.com/de", "flowkey.com", "freemium", "proprietary", ["bildung", "musik"],
    "flowkey übt Klavierstücke mit Noten, die dem Spiel folgen.",
    "flowkey zeigt Noten und hört über das Mikrofon mit, welche Tasten getroffen wurden. Der Dienst kommt aus Berlin. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Noten, die dem Spiel folgen", "Rückmeldung über das Mikrofon", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Klavierstück mit Rückmeldung zu üben", "Notenlesen neben dem Spielen zu lernen"], True)
add("Lifesum", "https://lifesum.com/", "lifesum.com", "freemium", "proprietary", ["gesundheit"],
    "Lifesum führt ein Ernährungs- und Wassertagebuch mit Tageszielen.",
    "Lifesum trägt Mahlzeiten ein und zeigt, wie sie zu einem gesetzten Ziel passen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Ernährungstagebuch", "Tagesziele", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Mahlzeiten eines Tages zu erfassen", "Ein Ernährungsziel zu verfolgen"], True)
add("Finanztip", "https://www.finanztip.de/", "finanztip.de", "free", "proprietary", ["finanzen", "recherche"],
    "Finanztip erklärt Geldthemen für Verbraucherinnen und Verbraucher in Deutschland.",
    "Finanztip veröffentlicht Ratgeber zu Konto, Versicherung, Steuer und Verträgen. Die Artikel sind ohne Abo lesbar. Der Verein finanziert sich nicht über den Verkauf der einzelnen Texte.",
    ["Ratgeber zu Geldthemen", "Ausrichtung auf Deutschland", "Lesen ohne Abo"],
    ["Einen Vertrag oder ein Konto einzuordnen", "Einen Ratgeber zur Steuer zu lesen"], True)
add("Codecheck", "https://www.codecheck.info/", "codecheck.info", "freemium", "proprietary", ["gesundheit"],
    "Codecheck bewertet Lebensmittel und Kosmetik anhand des Strichcodes.",
    "Codecheck liest einen Barcode und zeigt Inhaltsstoffe und eine Einordnung. Ein Teil der Angaben ist ohne Abo sichtbar, weitere Filter liegen in bezahlten Stufen.",
    ["Barcode von Lebensmitteln und Kosmetik", "Inhaltsstoffe und Einordnung", "Kostenloser Anteil und bezahlte Stufen"],
    ["Ein Produkt im Laden anhand des Codes zu prüfen", "Inhaltsstoffe zu vergleichen"], True)
add("Open Food Facts", "https://de.openfoodfacts.org/", "de.openfoodfacts.org", "free", "unknown", ["gesundheit"],
    "Open Food Facts sammelt Inhaltsstoffe und Nährwerte von Lebensmitteln als offene Datenbank.",
    "Die deutschsprachige Seite zeigt Produkte, Nährwerte und Zutaten, die Freiwillige erfassen. Die Abfrage ist ohne Abo möglich. Eine einzelne OSI-Kennung für die ganze Plattform wird hier nicht eingetragen.",
    ["Offene Produktdaten", "Nährwerte und Zutaten", "Abfrage ohne Abo"],
    ["Zutaten eines Produkts nachzuschlagen", "Produkte anhand der Nährwerte zu vergleichen"], True)
add("Procreate", "https://procreate.com/", "procreate.com", "paid", "proprietary", ["design"],
    "Procreate zeichnet und malt auf dem iPad.",
    "Procreate arbeitet mit Ebenen, Pinseln und Animation auf dem Tablet. Die App ist einmalig kostenpflichtig, ein Abo nennt die Website nicht als Voraussetzung.",
    ["Zeichnen mit Ebenen und Pinseln", "Animation auf dem iPad", "Einmalig kostenpflichtige App"],
    ["Eine Illustration auf dem Tablet zu malen", "Eine kurze Animation zu zeichnen"], True)
add("Capture One", "https://www.captureone.com/", "captureone.com", "freemium", "proprietary", ["design"],
    "Capture One entwickelt Raw-Fotos mit Farbe, Schärfe und Tether-Aufnahme.",
    "Capture One importiert Kameradateien und setzt Look, Ausschnitt und lokale Korrekturen. Es gibt einen Einstieg und kostenpflichtige Lizenzen.",
    ["Raw-Entwicklung", "Lokale Korrekturen", "Einstieg und kostenpflichtige Lizenzen"],
    ["Eine Studioaufnahme zu entwickeln", "Einen Look über eine Serie zu legen"], False)
add("Soundful", "https://soundful.com/", "soundful.com", "freemium", "proprietary", ["musik"],
    "Soundful erzeugt Hintergrundmusik aus Stil und Stimmung.",
    "Soundful liefert Tracks, die sich in Länge und Genre anpassen lassen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Musik nach Stil und Stimmung", "Anpassbare Länge", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Musikbett für ein Video zu erzeugen", "Mehrere Genres zu einem Thema zu hören"], True)
add("Loudly", "https://www.loudly.com/", "loudly.com", "freemium", "proprietary", ["musik"],
    "Loudly erzeugt Musikstücke und bietet eine Bibliothek fertiger Tracks.",
    "Loudly kombiniert generierte Musik mit einer durchsuchbaren Bibliothek. Der Dienst kommt aus Berlin. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Generierte Musik und Bibliothek", "Anbieter aus Berlin", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Track für ein Video zu suchen", "Ein Stück in einem Genre erzeugen zu lassen"], True)
add("Beatoven", "https://www.beatoven.ai/", "beatoven.ai", "freemium", "proprietary", ["musik"],
    "Beatoven setzt Hintergrundmusik nach Stimmung und Länge zusammen.",
    "Beatoven erzeugt einen Track zu einer beschriebenen Stimmung und erlaubt den Austausch einzelner Abschnitte. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Musik nach Stimmung und Länge", "Austausch einzelner Abschnitte", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Musik unter ein Video zu legen", "Einen Abschnitt eines Tracks zu ersetzen"], False)
add("Splice", "https://splice.com/", "splice.com", "freemium", "proprietary", ["musik"],
    "Splice verleiht Samples, Presets und Loops für die Musikproduktion.",
    "Splice durchsucht eine Bibliothek und lädt Sounds in die eigene Session. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo für Credits.",
    ["Samples, Presets und Loops", "Suche in der Bibliothek", "Kostenloser Einstieg und bezahltes Abo"],
    ["Einen Drum-Loop für einen Beat zu finden", "Ein Preset in die eigene Produktion zu laden"], False)
add("Ableton Live", "https://www.ableton.com/", "ableton.com", "paid", "proprietary", ["musik"],
    "Ableton Live ist eine Software zum Produzieren und Live-Spielen von Musik.",
    "Ableton Live arrangiert Spuren in einer Session- und einer Arrangement-Ansicht. Der Hersteller sitzt in Berlin. Die Lizenzen sind kostenpflichtig.",
    ["Session- und Arrangement-Ansicht", "Produktion und Live-Spiel", "Kostenpflichtige Lizenzen"],
    ["Einen Track zu arrangieren", "Eine Liveshow mit Clips zu spielen"], False)
add("Bitwig Studio", "https://www.bitwig.com/", "bitwig.com", "paid", "proprietary", ["musik"],
    "Bitwig Studio produziert Musik mit einem modularen Aufbau der Geräte.",
    "Bitwig Studio mischt Spuren und lässt Klangerzeuger ineinander verschachteln. Der Hersteller sitzt in Berlin. Die Lizenz ist kostenpflichtig.",
    ["Mehrspur mit modularen Geräten", "Hersteller aus Berlin", "Kostenpflichtige Lizenz"],
    ["Einen elektronischen Track zu produzieren", "Einen Klangerzeuger modular zu verschalten"], False)
add("REAPER", "https://www.reaper.fm/", "reaper.fm", "paid", "proprietary", ["musik", "audio-und-sprache"],
    "REAPER nimmt und mischt Mehrspur-Audio auf dem eigenen Rechner.",
    "REAPER bietet Aufnahme, Schnitt und Mischung mit einem kleinen Installationspaket. Die Lizenz ist kostenpflichtig, eine Testphase nennt die Website.",
    ["Aufnahme, Schnitt und Mischung", "Kleines Installationspaket", "Kostenpflichtige Lizenz mit Testphase"],
    ["Einen Podcast mehrspurig aufzunehmen", "Einen Mix auf dem eigenen Rechner zu bauen"], False)
add("Flat", "https://flat.io/", "flat.io", "freemium", "proprietary", ["musik", "bildung"],
    "Flat schreibt Noten im Browser und lässt mehrere Personen gleichzeitig daran arbeiten.",
    "Flat zeigt eine Partitur im Browser und spielt sie ab. Kommentare bleiben am Dokument. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Notensatz im Browser", "Gleichzeitiges Arbeiten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Partitur mit einer Klasse zu schreiben", "Ein Stück im Browser anzuhören"], True)
add("NovelAI", "https://novelai.net/", "novelai.net", "freemium", "proprietary", ["textgenerierung"],
    "NovelAI schreibt Geschichten und erzeugt Bilder aus einem fortlaufenden Text.",
    "NovelAI setzt eine Erzählung fort und kann Szenen als Bild ausgeben. Die Modelle laufen im Konto. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Fortsetzen von Geschichten", "Bilder zu Szenen", "Einstieg und bezahlte Stufen"],
    ["Eine Geschichte weiterschreiben zu lassen", "Eine Szene als Bild zu sehen"], False)
add("Workflowy", "https://workflowy.com/", "workflowy.com", "freemium", "proprietary", ["produktivitaet"],
    "Workflowy sammelt Notizen als unendlich verschachtelte Liste.",
    "Workflowy legt Stichpunkte ineinander und zoomt in einen Punkt hinein, bis er die ganze Ansicht füllt. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Verschachtelte Listen", "Zoom in einen Stichpunkt", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Thema in Unterpunkte zu zerlegen", "Eine lange Liste auf einen Zweig zu zoomen"], True)
add("TickTick", "https://ticktick.com/", "ticktick.com", "freemium", "proprietary", ["produktivitaet"],
    "TickTick verbindet Aufgaben, Kalender und einen Fokus-Timer.",
    "TickTick legt Aufgaben mit Datum an und zeigt sie neben dem Kalender. Ein Timer begleitet eine einzelne Aufgabe. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Aufgaben und Kalender", "Fokus-Timer", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Den Tag als Aufgabenliste zu planen", "Eine Aufgabe mit Timer abzuarbeiten"], True)
add("Hunter", "https://hunter.io/", "hunter.io", "freemium", "proprietary", ["marketing"],
    "Hunter findet E-Mail-Adressen zu einer Domain und prüft sie.",
    "Hunter sucht öffentliche Adressen zu einem Unternehmen und schätzt, ob sie erreichbar sind. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Adressen zu einer Domain", "Prüfung der Erreichbarkeit", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Eine geschäftliche Adresse zu einer Website zu finden", "Eine Liste vor dem Versand zu prüfen"], False)
add("lemlist", "https://www.lemlist.com/", "lemlist.com", "paid", "proprietary", ["marketing"],
    "lemlist verschickt personalisierte Akquise-Mails in Sequenzen.",
    "lemlist legt Folgen von E-Mails an und füllt Platzhalter aus einer Liste. Der Dienst kommt aus Frankreich. Die Nutzung ist kostenpflichtig.",
    ["E-Mail-Sequenzen", "Platzhalter aus einer Liste", "Kostenpflichtige Nutzung"],
    ["Eine Folge von Akquise-Mails zu planen", "Dieselbe Sequenz an eine Liste zu senden"], False)
add("Pirsch Analytics", "https://pirsch.io/", "pirsch.io", "freemium", "proprietary", ["seo", "marketing"],
    "Pirsch zählt Seitenaufrufe ohne Cookies und kommt aus Deutschland.",
    "Pirsch zeigt Aufrufe, Quellen und Seiten einer Website in einem schmalen Bericht. Der Anbieter sitzt in Deutschland. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Aufrufe ohne Cookies", "Quellen und Seiten", "Anbieter aus Deutschland"],
    ["Den Traffic einer Website ohne Cookie-Banner-Zählung zu sehen", "Kampagnenlinks an den Aufrufen zu erkennen"], False)
add("GoatCounter", "https://www.goatcounter.com/", "goatcounter.com", "freemium", "unknown", ["seo"],
    "GoatCounter zählt Seitenaufrufe schlank und lässt sich selbst betreiben.",
    "GoatCounter erfasst Aufrufe ohne eine große Tracking-Suite. Es gibt eine gehostete Fassung und den Selbstbetrieb. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Schlanke Aufrufzählung", "Hosting und Selbstbetrieb", "Lizenz nicht als OSI eingetragen"],
    ["Aufrufe einer kleinen Website zu zählen", "Die Zählung selbst zu hosten"], False)
add("Microsoft Clarity", "https://clarity.microsoft.com/", "clarity.microsoft.com", "free", "proprietary", ["seo", "marketing"],
    "Clarity zeigt, wie sich Personen auf einer Website bewegen, inklusive Sitzungsaufnahmen.",
    "Clarity zeichnet Klicks und Sitzungen auf und zeigt Wärmebilder. Die Nutzung für die eigene Website ist ohne Abo möglich.",
    ["Sitzungsaufnahmen und Wärmebilder", "Klicks auf der eigenen Website", "Nutzung ohne Abo"],
    ["Zu sehen, wo Besucher auf einer Seite stocken", "Eine Sitzung nachzuvollziehen"], False)
add("Semgrep", "https://semgrep.dev/", "semgrep.dev", "freemium", "proprietary", ["programmierung"],
    "Semgrep sucht Muster und Sicherheitslücken im Quelltext.",
    "Semgrep prüft Repositories mit Regeln und zeigt Treffer in der Konsole oder in der Cloud. Es gibt einen kostenlosen Einstieg und bezahlte Stufen für Teams. Die gehostete Plattform ist proprietär.",
    ["Regeln über den Quelltext", "Treffer in Konsole und Cloud", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Repository auf bekannte Muster zu prüfen", "Eine eigene Regel für unsicheren Code zu schreiben"], False)
add("Snyk", "https://snyk.io/", "snyk.io", "freemium", "proprietary", ["programmierung"],
    "Snyk sucht bekannte Schwachstellen in Abhängigkeiten und Containern.",
    "Snyk liest Manifeste und Images und meldet Lücken mit einer empfohlenen Version. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Schwachstellen in Abhängigkeiten", "Hinweise auf neuere Versionen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Projekt auf bekannte Lücken zu prüfen", "Ein Container-Image vor dem Deploy zu scannen"], False)
add("Sentry", "https://sentry.io/", "sentry.io", "freemium", "unknown", ["programmierung"],
    "Sentry sammelt Fehler aus Anwendungen und gruppiert sie nach Ursache.",
    "Sentry zeigt Stacktraces, betroffene Versionen und wie oft ein Fehler auftritt. Die Cloud hat einen kostenlosen Einstieg und bezahlte Stufen. Die Lizenz des Servers ist keine durchgängige OSI-Lizenz, der Lizenztyp bleibt Unbekannt.",
    ["Gruppierte Fehler mit Stacktrace", "Cloud mit kostenlosem Einstieg", "Lizenz nicht als OSI geführt"],
    ["Abstürze einer Anwendung zu sehen", "Einen Fehler einer Version zuzuordnen"], False)
add("ClickHouse", "https://clickhouse.com/", "clickhouse.com", "freemium", "unknown", ["daten"],
    "ClickHouse ist eine spaltenorientierte Datenbank für große Auswertungen.",
    "ClickHouse beantwortet analytische SQL-Abfragen über viele Zeilen. Es gibt eine selbst betreibbare Ausgabe und eine Cloud. Eine einzelne OSI-Kennung wird hier nicht eingetragen.",
    ["Analytisches SQL", "Selbstbetrieb und Cloud", "Lizenz nicht als eine OSI-Kennung eingetragen"],
    ["Viele Ereignisse schnell auszuwerten", "Eine Auswertungsdatenbank selbst zu betreiben"], False)
add("MotherDuck", "https://motherduck.com/", "motherduck.com", "freemium", "proprietary", ["daten"],
    "MotherDuck betreibt DuckDB in der Cloud und verbindet sie mit lokalen Dateien.",
    "MotherDuck führt SQL über Cloud-Daten und kann lokale DuckDB-Dateien einbeziehen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["DuckDB in der Cloud", "SQL über Cloud und lokale Dateien", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Analyse zu teilen, ohne einen eigenen Server zu betreiben", "SQL auf größeren Daten zu fahren"], False)
add("Neon", "https://neon.tech/", "neon.tech", "freemium", "proprietary", ["daten", "programmierung"],
    "Neon stellt Postgres in der Cloud bereit und verzweigt Datenbanken wie Code.",
    "Neon startet eine Postgres-Datenbank und kann davon eine Kopie für einen Test erzeugen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Postgres in der Cloud", "Zweige einer Datenbank", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Postgres-Datenbank ohne eigenen Server zu starten", "Einen Testzweig neben den echten Daten anzulegen"], False)
add("Redis", "https://redis.io/", "redis.io", "freemium", "unknown", ["daten", "programmierung"],
    "Redis hält Datenstrukturen im Speicher für Cache, Warteschlangen und Sitzungen.",
    "Redis speichert Schlüssel, Listen und weitere Strukturen im Arbeitsspeicher und bietet dazu eine Cloud. Die Lizenz der aktuellen Ausgabe ist keine durchgängig bestätigte OSI-Lizenz, der Lizenztyp bleibt Unbekannt.",
    ["Datenstrukturen im Speicher", "Cache und Warteschlangen", "Software und Cloud"],
    ["Einen Cache vor eine Datenbank zu setzen", "Eine Warteschlange für Jobs zu betreiben"], False)
add("Weaviate", "https://weaviate.io/", "weaviate.io", "freemium", "unknown", ["daten", "programmierung"],
    "Weaviate speichert Objekte und Vektoren für die Suche und lässt sich selbst betreiben.",
    "Weaviate legt Daten mit Embeddings ab und beantwortet Suche und Filter. Es gibt eine Cloud und den Selbstbetrieb. Eine OSI-Kennung wurde in diesem Durchgang nicht bestätigt.",
    ["Objekte mit Vektoren", "Suche und Filter", "Cloud und Selbstbetrieb"],
    ["Eine Vektorsuche selbst zu hosten", "Objekte mit Filtern und Ähnlichkeit zu suchen"], False)
add("Jina AI", "https://jina.ai/", "jina.ai", "freemium", "proprietary", ["daten", "programmierung"],
    "Jina AI stellt Modelle für Embeddings und Suche über eine Schnittstelle bereit.",
    "Jina bietet Embeddings und eine Suche, die sich in eigene Anwendungen einbinden lässt. Der Anbieter sitzt in Berlin. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Embeddings und Suche", "Schnittstelle für Anwendungen", "Anbieter aus Berlin"],
    ["Texte in Vektoren zu überführen", "Eine Suche über eigene Dokumente anzubinden"], False)
add("Pinecone", "https://www.pinecone.io/", "pinecone.io", "freemium", "proprietary", ["daten"],
    "Pinecone speichert Vektoren in einer verwalteten Datenbank.",
    "Pinecone nimmt Embeddings entgegen und beantwortet Ähnlichkeitsanfragen, ohne dass man den Index selbst betreibt. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Verwaltete Vektordatenbank", "Ähnlichkeitssuche", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Vektorindex ohne eigenen Server zu betreiben", "Ähnliche Dokumente zu einer Anfrage zu finden"], False)
add("Roboflow", "https://roboflow.com/", "roboflow.com", "freemium", "proprietary", ["daten", "bildgenerierung"],
    "Roboflow beschriftet Bilder und trainiert daraus Erkennungsmodelle.",
    "Roboflow sammelt Bilddatensätze, markiert Objekte und trainiert ein Modell, das sich per API abrufen lässt. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Bilddatensätze und Markierungen", "Training und API", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Objekte auf Fotos zu markieren", "Ein Erkennungsmodell über eine API aufzurufen"], False)
add("Airbyte", "https://airbyte.com/", "airbyte.com", "freemium", "unknown", ["daten", "automatisierung"],
    "Airbyte kopiert Daten aus Quellen in ein Warehouse und lässt sich selbst betreiben.",
    "Airbyte verbindet Quellen und Ziele über fertige Konnektoren und führt die Läufe nach Plan aus. Es gibt eine Cloud und den Selbstbetrieb. Eine OSI-Kennung der aktuellen Ausgabe wird hier nicht eingetragen.",
    ["Konnektoren von Quelle zu Ziel", "Läufe nach Plan", "Cloud und Selbstbetrieb"],
    ["Daten aus einem Dienst in ein Warehouse zu kopieren", "Einen Konnektor selbst zu hosten"], False)
add("KNIME", "https://www.knime.com/", "knime.com", "freemium", "unknown", ["daten"],
    "KNIME baut Datenanalysen als Knotengraph ohne dass jede Zeile Code sein muss.",
    "KNIME Analytics Platform verbindet Knoten für Lesen, Filtern und Modelle auf dem eigenen Rechner. Die Desktop-Plattform ist ohne Abo nutzbar, Server und Hub sind bezahlt. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Analysen als Knotengraph", "Desktop ohne Abo", "Server und Hub bezahlt"],
    ["Eine Auswertung ohne eigenes Skript zu bauen", "Tabellen zu filtern und zu verbinden"], False)
add("Orange Data Mining", "https://orangedatamining.com/", "orangedatamining.com", "free", "unknown", ["daten", "bildung"],
    "Orange baut Datenanalysen aus Widgets auf einer Fläche.",
    "Orange verbindet Tabellen, Diagramme und Modelle per Drag-and-drop. Die Anwendung ist ohne Abo erhältlich. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Widgets für Tabellen und Modelle", "Diagramme auf der Fläche", "Nutzung ohne Abo"],
    ["Einen Datensatz im Unterricht zu untersuchen", "Ein Modell ohne eigenes Skript zu versuchen"], True)
add("Google Colab", "https://colab.research.google.com/", "colab.research.google.com", "freemium", "proprietary", ["programmierung", "daten"],
    "Google Colab führt Jupyter-Notizbücher im Browser aus, auch mit Grafikchip.",
    "Colab öffnet ein Notizbuch in der Google-Cloud und führt Python-Zellen aus. Ein kostenloses Kontingent gibt es, mehr Rechenzeit ist bezahlt.",
    ["Notizbücher im Browser", "Option auf einen Grafikchip", "Kostenloses Kontingent und bezahlte Rechenzeit"],
    ["Ein Python-Notebook ohne lokale Installation zu starten", "Ein Modell auf einem Grafikchip zu testen"], True)
add("Kaggle", "https://www.kaggle.com/", "kaggle.com", "free", "proprietary", ["daten", "programmierung"],
    "Kaggle stellt Datensätze, Notizbücher und Wettbewerbe für maschinelles Lernen bereit.",
    "Kaggle hostet Datensätze und Jupyter-Notizbücher und zeigt öffentliche Wettbewerbe. Die Nutzung der Notizbücher ist ohne Abo möglich.",
    ["Datensätze und Notizbücher", "Öffentliche Wettbewerbe", "Nutzung ohne Abo"],
    ["Einen öffentlichen Datensatz zu untersuchen", "Ein Notebook ohne eigenen Rechner zu starten"], True)
add("Phrase", "https://phrase.com/", "phrase.com", "freemium", "proprietary", ["textgenerierung"],
    "Phrase verwaltet Übersetzungen von Software-Texten für mehrere Sprachen.",
    "Phrase speichert Strings, übergibt sie an Übersetzende und spielt sie zurück in den Code. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Strings in mehreren Sprachen", "Übergabe an Übersetzende", "Einstieg und bezahlte Stufen"],
    ["Oberflächentexte einer App übersetzen zu lassen", "Übersetzungen zurück in den Code zu spielen"], False)
add("Crowdin", "https://crowdin.com/", "crowdin.com", "freemium", "proprietary", ["textgenerierung"],
    "Crowdin sammelt Übersetzungen für Software und Dokumente.",
    "Crowdin lädt Ausgangstexte hoch und verteilt sie an Übersetzende. Fortschritt und Prüfungen bleiben im Projekt. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Übersetzungsprojekte", "Prüfung und Fortschritt", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine App in mehrere Sprachen zu bringen", "Den Fortschritt einer Übersetzung zu sehen"], False)
add("Lokalise", "https://lokalise.com/", "lokalise.com", "freemium", "proprietary", ["textgenerierung"],
    "Lokalise verwaltet Übersetzungen und spielt sie in Apps und Websites zurück.",
    "Lokalise hält Schlüssel und Übersetzungen und liefert sie über eine Schnittstelle oder Dateien aus. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Schlüssel und Übersetzungen", "Auslieferung per Datei oder API", "Einstieg und bezahlte Stufen"],
    ["Texte einer App an Übersetzende zu geben", "Übersetzungen automatisch auszuliefern"], False)
add("Proton Mail", "https://proton.me/mail", "proton.me", "freemium", "proprietary", ["produktivitaet"],
    "Proton Mail verschlüsselt E-Mails und kommt aus der Schweiz.",
    "Proton Mail speichert Postfächer verschlüsselt und bietet Kalender und weitere Dienste im selben Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Verschlüsselte E-Mail", "Anbieter aus der Schweiz", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein verschlüsseltes Postfach zu nutzen", "Mail und Kalender im selben Konto zu halten"], True)
add("Tuta", "https://tuta.com/", "tuta.com", "freemium", "proprietary", ["produktivitaet"],
    "Tuta verschlüsselt E-Mail und Kalender und kommt aus Deutschland.",
    "Tuta, früher Tutanota, speichert Postfach und Kalender verschlüsselt. Der Anbieter sitzt in Hannover. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Verschlüsselte Mail und Kalender", "Anbieter aus Hannover", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein verschlüsseltes Postfach aus Deutschland zu nutzen", "Termine im selben Konto abzulegen"], True)
add("Threema", "https://threema.ch/de", "threema.ch", "paid", "proprietary", ["social-media"],
    "Threema ist ein kostenpflichtiger Messenger aus der Schweiz.",
    "Threema verschickt Nachrichten und Anrufe ohne eine Telefonnummer als Pflicht und ohne Werbung im Chat. Die App ist einmalig kostenpflichtig. Der Anbieter sitzt in der Schweiz.",
    ["Nachrichten und Anrufe", "Kein Pflichtabo nach dem Kauf", "Einmalig kostenpflichtige App"],
    ["Einen Chat ohne Werbenetzwerk zu führen", "Eine Nachricht ohne Telefonnummer als Kennung zu senden"], True)
add("Telegram", "https://telegram.org/", "telegram.org", "free", "proprietary", ["social-media"],
    "Telegram verschickt Nachrichten, Kanäle und Dateien über eine Cloud.",
    "Telegram führt Einzelchats, Gruppen und Kanäle und synchronisiert sie über Geräte. Die App ist ohne Abo nutzbar. Der Server ist ein proprietärer Dienst.",
    ["Chats, Gruppen und Kanäle", "Abgleich über Geräte", "Nutzung ohne Abo"],
    ["Eine Gruppe zu führen", "Dateien in einem Chat zu verschicken"], True)
add("Delta Chat", "https://delta.chat/de/", "delta.chat", "free", "unknown", ["social-media"],
    "Delta Chat verschickt Nachrichten über gewöhnliche E-Mail-Konten.",
    "Delta Chat nutzt ein vorhandenes Postfach als Transport und zeigt die Unterhaltung wie einen Messenger. Eine OSI-Kennung wird hier nicht eingetragen. Die App ist ohne Abo erhältlich.",
    ["Nachrichten über E-Mail", "Darstellung als Messenger", "Nutzung ohne Abo"],
    ["Mit einem bestehenden Postfach zu chatten", "Ohne einen zusätzlichen Messenger-Server zu schreiben"], False)
add("SimpleX Chat", "https://simplex.chat/", "simplex.chat", "free", "unknown", ["social-media"],
    "SimpleX Chat verschickt Nachrichten ohne eine feste Nutzerkennung.",
    "SimpleX verbindet zwei Personen über einen Einladungslink und speichert keine Telefonnummer als Kennung. Eine OSI-Kennung wird hier nicht eingetragen. Die App ist ohne Abo erhältlich.",
    ["Chat ohne feste Nutzerkennung", "Verbindung über einen Einladungslink", "Nutzung ohne Abo"],
    ["Einen Chat ohne Telefonnummer zu starten", "Eine Einladung als Link zu verschicken"], False)
add("7Mind Kurse", "https://www.7mind.de/", "7mind.de", "freemium", "proprietary", ["gesundheit"],
    "Platzhalter wird nicht benutzt.",
    "Platzhalter.",
    ["x"], ["x"])


def validate(entries):
    domains = {row[0] for row in sqlite3.connect(ROOT / "data" / "linkjagd.db").execute("select domain from tools")}
    seen = set()
    errors = []
    # drop the accidental placeholder if present
    entries[:] = [e for e in entries if e["name"] != "7Mind Kurse"]
    for entry in entries:
        if entry["domain"] in domains:
            errors.append(f"db {entry['domain']} {entry['name']}")
        if entry["domain"] in seen:
            errors.append(f"dup {entry['domain']}")
        seen.add(entry["domain"])
        if not (10 <= len(entry["shortDescriptionDe"]) <= 280):
            errors.append(f"kurz {entry['name']} {len(entry['shortDescriptionDe'])}")
        if "zzgl" in (entry["shortDescriptionDe"] + entry["longDescriptionDe"]).lower():
            errors.append(f"ust {entry['name']}")
        if entry["licenseType"] == "open_source" and not (entry["oss"] and entry["oss"]["license"]):
            errors.append(f"oss {entry['name']}")
        if entry["licenseType"] != "open_source" and entry["oss"] is not None:
            errors.append(f"ossblock {entry['name']}")
    if errors:
        raise SystemExit("\n".join(errors))
    return entries


if __name__ == "__main__":
    rows = validate(E)
    out = ROOT / "data" / "verified-tools-batch4.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows), "->", out)
