#!/usr/bin/env python3
"""Sechste geprüfte Liste. Nur Seiten, die in diesem Lauf HTTP 200 geliefert haben."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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


add("Kontist", "https://kontist.com/", "kontist.com", "freemium", "proprietary", ["finanzen"],
    "Kontist führt ein Geschäftskonto und schätzt die Steuer auf Einnahmen.",
    "Kontist zeigt Umsätze eines Geschäftskontos und setzt davon einen Steueranteil beiseite. Der Dienst kommt aus Berlin. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Geschäftskonto", "Steuerschätzung auf Einnahmen", "Einstieg und bezahlte Stufen"],
    ["Einnahmen und einen Steueranteil zu trennen", "Ein Konto für Selbstständige zu führen"], True)
add("Trade Republic", "https://traderepublic.com/", "traderepublic.com", "freemium", "proprietary", ["finanzen"],
    "Trade Republic handelt Aktien, ETFs und Krypto in einer App.",
    "Trade Republic legt Sparpläne und Einzelorders an. Der Anbieter sitzt in Berlin. Das Depot selbst ist ohne monatliche Grundgebühr beschrieben, der Handel kann Kosten haben, die die App nennt.",
    ["Aktien, ETFs und Krypto", "Sparpläne", "Kosten stehen in der App"],
    ["Einen ETF-Sparplan anzulegen", "Eine einzelne Aktie zu kaufen"], True)
add("Scalable Capital", "https://de.scalable.capital/", "de.scalable.capital", "freemium", "proprietary", ["finanzen"],
    "Scalable Capital führt ein Depot mit Sparplänen auf ETFs und Aktien.",
    "Scalable Capital legt Sparpläne und Orders an und bietet ein Verrechnungskonto. Der Broker kommt aus München. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Depot und Sparpläne", "Verrechnungskonto", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Sparplan auf einen ETF zu starten", "Eine Order im Depot zu setzen"], True)
add("Parqet", "https://www.parqet.com/", "parqet.com", "freemium", "proprietary", ["finanzen"],
    "Parqet zeigt ein Depot über mehrere Broker hinweg.",
    "Parqet liest Bestände ein und zeigt Wert und Verteilung, ohne selbst zu handeln. Der Dienst kommt aus Deutschland. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Depot über mehrere Broker", "Wert und Verteilung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Mehrere Depots in einer Ansicht zu sehen", "Die Verteilung eines Portfolios zu prüfen"], True)
add("getquin", "https://www.getquin.com/", "getquin.com", "freemium", "proprietary", ["finanzen"],
    "getquin fasst Depots und Krypto in einer Übersicht zusammen.",
    "getquin zeigt Performance über angebundene Konten. Der Dienst kommt aus Berlin. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Depots und Krypto", "Performance über Konten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Die Entwicklung eines Depots zu sehen", "Mehrere Konten nebeneinander zu halten"], True)
add("extraETF", "https://www.extraetf.com/", "extraetf.com", "freemium", "proprietary", ["finanzen", "recherche"],
    "extraETF vergleicht ETFs nach Kosten, Index und Größe.",
    "extraETF filtert Fonds und zeigt Kennzahlen. Ein Teil der Suche ist ohne Abo lesbar, weitere Daten sind bezahlt.",
    ["Vergleich von ETFs", "Kosten, Index und Größe", "Freie Suche und bezahlte Daten"],
    ["Einen ETF nach Kosten zu filtern", "Zwei Fonds gegenüberzustellen"], True)
add("Finanzfluss", "https://www.finanzfluss.de/", "finanzfluss.de", "free", "proprietary", ["finanzen", "recherche"],
    "Finanzfluss erklärt Geldanlage und Steuern für Einsteiger in Deutschland.",
    "Finanzfluss veröffentlicht Erklärstücke zu ETF, Depot und Steuer. Die Artikel sind ohne Abo lesbar. Der Anbieter sitzt in Deutschland.",
    ["Erklärstücke zu ETF und Steuer", "Ausrichtung auf Deutschland", "Lesen ohne Abo"],
    ["Einen ETF-Sparplan einzuordnen", "Eine Frage zur Abgeltungsteuer nachzulesen"], True)
add("Mite", "https://www.mite.de/", "mite.de", "paid", "proprietary", ["produktivitaet"],
    "Mite erfasst Zeiten für Kunden und Projekte.",
    "Mite stoppt Zeiten und ordnet sie einem Kunden zu. Der Dienst kommt aus Deutschland. Die Nutzung ist kostenpflichtig.",
    ["Zeiterfassung nach Kunde", "Auswertungen", "Kostenpflichtige Nutzung"],
    ["Stunden für eine Rechnung festzuhalten", "Die Zeit an einem Projekt zu sehen"], True)
add("MOCO", "https://www.mocoapp.com/", "mocoapp.com", "paid", "proprietary", ["produktivitaet", "personal"],
    "MOCO führt Projekte, Zeiten und Rechnungen für Agenturen.",
    "MOCO verbindet Planung, Zeiterfassung und Abrechnung. Der Anbieter sitzt in der Schweiz. Die Nutzung ist kostenpflichtig.",
    ["Projekte, Zeiten und Rechnungen", "Ausrichtung auf Agenturen", "Kostenpflichtige Nutzung"],
    ["Stunden eines Projekts abzurechnen", "Die Auslastung eines Teams zu sehen"], False)
add("HQ", "https://www.hellohq.io/", "hellohq.io", "paid", "proprietary", ["produktivitaet"],
    "HQ plant Projekte und schreibt daraus Rechnungen.",
    "HQ, früher helloHQ, legt Aufgaben, Zeiten und Belege an einem Ort ab. Die Nutzung ist kostenpflichtig.",
    ["Projekte und Zeiten", "Rechnungen aus dem Projekt", "Kostenpflichtige Nutzung"],
    ["Ein Agenturprojekt bis zur Rechnung zu führen", "Zeiten einer Aufgabe zuzuordnen"], False)
add("zep", "https://www.zep.de/", "zep.de", "paid", "proprietary", ["produktivitaet", "personal"],
    "zep erfasst Projektzeiten und überführt sie in die Abrechnung.",
    "zep sammelt Stunden, Spesen und Abwesenheiten. Der Anbieter sitzt in Deutschland. Die Nutzung ist kostenpflichtig.",
    ["Projektzeiten und Spesen", "Abwesenheiten", "Kostenpflichtige Nutzung"],
    ["Stunden eines Projekts zu erfassen", "Spesen neben den Zeiten abzurechnen"], False)
add("TimeButler", "https://www.timebutler.de/", "timebutler.de", "freemium", "proprietary", ["personal"],
    "TimeButler führt Urlaub, Krankheit und Arbeitszeiten.",
    "TimeButler nimmt Anträge entgegen und zeigt den Resturlaub. Der Dienst kommt aus Deutschland. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Urlaub und Krankheit", "Resturlaub", "Einstieg und bezahlte Stufen"],
    ["Einen Urlaubsantrag zu stellen", "Den Resturlaub eines Teams zu sehen"], True)
add("Personizer", "https://www.personizer.de/", "personizer.de", "freemium", "proprietary", ["personal"],
    "Personizer verwaltet Personalakten, Urlaub und Zeiterfassung.",
    "Personizer legt Stammdaten und Abwesenheiten ab. Der Anbieter sitzt in Berlin. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Personalakten und Urlaub", "Zeiterfassung", "Einstieg und bezahlte Stufen"],
    ["Eine Personalakte digital zu führen", "Urlaub und Zeiten nebeneinander zu sehen"], False)
add("Leapsome", "https://www.leapsome.com/de", "leapsome.com", "paid", "proprietary", ["personal"],
    "Leapsome führt Ziele, Feedback und Mitarbeitergespräche.",
    "Leapsome legt Ziele und Befragungen an und sammelt Rückmeldungen im Team. Der Anbieter kommt aus Berlin. Die Nutzung ist kostenpflichtig.",
    ["Ziele und Feedback", "Mitarbeitergespräche", "Kostenpflichtige Nutzung"],
    ["Ein Ziel für ein Quartal festzuhalten", "Ein Gespräch mit Notizen vorzubereiten"], False)
add("JOIN", "https://join.com/", "join.com", "freemium", "proprietary", ["personal"],
    "JOIN schaltet eine Stelle auf mehreren Jobbörsen gleichzeitig.",
    "JOIN nimmt eine Anzeige entgegen und verteilt sie an angebundene Börsen. Der Dienst kommt aus Berlin. Es gibt einen Einstieg und bezahlte Schaltungen.",
    ["Eine Anzeige, mehrere Börsen", "Eingang der Bewerbungen", "Einstieg und bezahlte Schaltungen"],
    ["Eine Stelle breit zu streuen", "Bewerbungen an einem Ort zu sammeln"], False)
add("heyjobs", "https://www.heyjobs.de/", "heyjobs.de", "paid", "proprietary", ["personal"],
    "heyjobs schaltet Stellenanzeigen und spricht passende Profile an.",
    "heyjobs verteilt eine Anzeige und zeigt, welche Profile dazu passen. Der Dienst richtet sich an Arbeitgeber in Deutschland. Die Nutzung ist kostenpflichtig.",
    ["Stellenanzeigen", "Passende Profile", "Kostenpflichtige Nutzung"],
    ["Eine Stelle in Deutschland zu schalten", "Reichweite einer Anzeige zu sehen"], False)
add("rexx systems", "https://www.rexx-systems.com/", "rexx-systems.com", "paid", "proprietary", ["personal"],
    "rexx führt Bewerbungen, Personalakten und Zeiterfassung.",
    "rexx legt den Weg von der Bewerbung bis zur Akte in einem System ab. Der Anbieter sitzt in Deutschland. Die Nutzung ist kostenpflichtig.",
    ["Bewerbung bis Personalakte", "Zeiterfassung", "Kostenpflichtige Nutzung"],
    ["Bewerbungen in Stufen zu sortieren", "Stammdaten nach der Einstellung zu übernehmen"], False)
add("onlyfy", "https://www.onlyfy.com/", "onlyfy.com", "paid", "proprietary", ["personal"],
    "onlyfy schaltet Stellen und sucht Profile im Umfeld von XING.",
    "onlyfy veröffentlicht Anzeigen und durchsucht Profile. Das Angebot gehört zu New Work. Die Nutzung ist kostenpflichtig.",
    ["Stellenanzeigen", "Suche in Profilen", "Kostenpflichtige Nutzung"],
    ["Eine Stelle über XING zu schalten", "Profile zu einer Rolle zu sichten"], False)
add("sipgate", "https://www.sipgate.de/", "sipgate.de", "freemium", "proprietary", ["kundenservice"],
    "sipgate stellt Telefonie für Teams im Browser und in der App bereit.",
    "sipgate vergibt Nummern, Weiterleitungen und Anrufgruppen. Der Anbieter sitzt in Düsseldorf. Es gibt einen Einstieg und bezahlte Tarife.",
    ["Nummern und Weiterleitungen", "Anrufgruppen", "Einstieg und bezahlte Tarife"],
    ["Eine Team-Nummer einzurichten", "Anrufe an mehrere Personen zu verteilen"], False)
add("Placetel", "https://www.placetel.de/", "placetel.de", "paid", "proprietary", ["kundenservice"],
    "Placetel betreibt eine Cloud-Telefonanlage für Unternehmen.",
    "Placetel legt Nebenstellen, Warteschleifen und Ansagen an. Der Dienst kommt aus Deutschland. Die Nutzung ist kostenpflichtig.",
    ["Nebenstellen und Warteschleifen", "Ansagen", "Kostenpflichtige Nutzung"],
    ["Eine Telefonanlage ohne eigene Hardware zu betreiben", "Eine Warteschleife für den Support einzurichten"], False)
add("easybell", "https://www.easybell.de/", "easybell.de", "paid", "proprietary", ["kundenservice"],
    "easybell liefert SIP-Trunks und Rufnummern für Telefonanlagen.",
    "easybell schaltet Rufnummern und Leitungen, die eine eigene Anlage anbindet. Der Anbieter sitzt in Berlin. Die Tarife sind kostenpflichtig.",
    ["SIP-Trunks und Rufnummern", "Anbindung an eine Anlage", "Kostenpflichtige Tarife"],
    ["Eine bestehende Anlage an das Netz zu hängen", "Rufnummern zu übernehmen"], False)
add("3CX", "https://www.3cx.com/", "3cx.com", "freemium", "proprietary", ["kundenservice"],
    "3CX ist eine Telefonanlage, die sich selbst betreiben oder hosten lässt.",
    "3CX schaltet Nebenstellen, Warteschleifen und Apps für Anrufe. Es gibt eine kostenlose Ausgabe für kleine Teams und bezahlte Lizenzen.",
    ["Nebenstellen und Warteschleifen", "Selbstbetrieb oder Hosting", "Kostenlose Ausgabe und bezahlte Lizenzen"],
    ["Eine kleine Telefonanlage selbst zu betreiben", "Anrufe in einer App entgegenzunehmen"], False)
add("Auphonic", "https://auphonic.com/", "auphonic.com", "freemium", "proprietary", ["audio-und-sprache"],
    "Auphonic gleicht Lautstärke und Rauschen einer Aufnahme automatisch an.",
    "Auphonic nimmt eine Audiodatei und liefert eine ausgeglichene Fassung. Der Dienst kommt aus Österreich. Es gibt ein Freikontingent und bezahlte Stunden.",
    ["Lautstärke und Rauschen", "Automatische Nachbearbeitung", "Freikontingent und bezahlte Stunden"],
    ["Eine Podcast-Folge lautstärkemäßig anzugleichen", "Rauschen aus einer Aufnahme zu nehmen"], True)
add("Podigee", "https://www.podigee.com/", "podigee.com", "paid", "proprietary", ["audio-und-sprache"],
    "Podigee hostet Podcasts und liefert den Feed aus.",
    "Podigee nimmt Folgen entgegen, erzeugt den Feed und zeigt Statistiken. Der Anbieter sitzt in Berlin. Die Nutzung ist kostenpflichtig.",
    ["Hosting und Feed", "Statistiken", "Kostenpflichtige Nutzung"],
    ["Einen Podcast zu veröffentlichen", "Abrufe einer Folge zu sehen"], False)
add("letscast.fm", "https://www.letscast.fm/", "letscast.fm", "freemium", "proprietary", ["audio-und-sprache"],
    "letscast.fm hostet einen Podcast und erzeugt den Feed.",
    "letscast.fm lädt Folgen hoch und stellt sie Verzeichnissen bereit. Der Dienst kommt aus Deutschland. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Upload und Feed", "Auslieferung an Verzeichnisse", "Einstieg und bezahlte Stufen"],
    ["Eine Folge zu veröffentlichen", "Einen Feed ohne eigenen Server zu betreiben"], True)
add("fyyd", "https://fyyd.de/", "fyyd.de", "free", "proprietary", ["audio-und-sprache", "recherche"],
    "fyyd durchsucht Podcasts und Folgen.",
    "fyyd indexiert Feeds und macht Episoden suchbar. Die Suche ist ohne Abo möglich. Der Dienst kommt aus Deutschland.",
    ["Suche über Podcasts", "Index von Feeds", "Suche ohne Abo"],
    ["Eine Folge zu einem Stichwort zu finden", "Einen Podcast zu entdecken"], True)
add("podcast.de", "https://www.podcast.de/", "podcast.de", "free", "proprietary", ["audio-und-sprache", "recherche"],
    "podcast.de verzeichnet Podcasts und spielt Folgen im Browser.",
    "Das Verzeichnis listet Sendungen und zeigt einzelne Episoden. Die Suche ist ohne Abo möglich.",
    ["Verzeichnis von Podcasts", "Wiedergabe im Browser", "Suche ohne Abo"],
    ["Einen Podcast zu einem Thema zu finden", "Eine Folge direkt anzuhören"], True)
add("Buzzsprout", "https://www.buzzsprout.com/", "buzzsprout.com", "freemium", "proprietary", ["audio-und-sprache"],
    "Buzzsprout hostet Podcasts und liefert Statistiken zum Feed.",
    "Buzzsprout nimmt Folgen an und verteilt sie an Verzeichnisse. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Hosting und Statistiken", "Verteilung an Verzeichnisse", "Einstieg und bezahlte Stufen"],
    ["Einen Podcast ohne eigenen Server zu starten", "Abrufe einer Folge zu sehen"], True)
add("Transistor", "https://transistor.fm/", "transistor.fm", "paid", "proprietary", ["audio-und-sprache"],
    "Transistor hostet mehrere Podcasts unter einem Konto.",
    "Transistor erzeugt Feeds, Webseiten zur Folge und Statistiken. Die Nutzung ist kostenpflichtig.",
    ["Mehrere Podcasts", "Seiten zur Folge und Statistiken", "Kostenpflichtige Nutzung"],
    ["Mehrere Sendungen in einem Konto zu führen", "Eine Folge mit einer eigenen Seite zu veröffentlichen"], False)
add("Audible", "https://www.audible.de/", "audible.de", "freemium", "proprietary", ["bildung"],
    "Audible verleiht Hörbücher und Hörspiele über ein Abo.",
    "Audible spielt Titel in der App und tauscht sie im Rahmen des Abos. Es gibt Testangebote und bezahlte Stufen, die die Seite nennt.",
    ["Hörbücher und Hörspiele", "Wiedergabe in der App", "Testangebote und bezahlte Stufen"],
    ["Ein Hörbuch zu leihen", "Einen Titel unterwegs zu hören"], True)
add("Onleihe", "https://www.onleihe.de/", "onleihe.de", "free", "proprietary", ["bildung"],
    "Die Onleihe leiht E-Books und Hörbücher über die örtliche Bibliothek.",
    "Die Onleihe stellt Titel digital bereit, wenn die Bibliothek den Dienst anbietet. Die Ausleihe selbst hängt am Bibliotheksausweis und ist für dessen Inhaber ohne separates Abo.",
    ["E-Books und Hörbücher", "Ausleihe über die Bibliothek", "Nutzung mit Bibliotheksausweis"],
    ["Ein E-Book über die Stadtbibliothek zu leihen", "Einen Titel nach Verfügbarkeit zu suchen"], True)
add("Deutsche Digitale Bibliothek", "https://www.deutsche-digitale-bibliothek.de/", "deutsche-digitale-bibliothek.de", "free", "proprietary", ["recherche", "bildung"],
    "Die Deutsche Digitale Bibliothek durchsucht Bestände von Bibliotheken, Archiven und Museen.",
    "Die Plattform zeigt digitalisierte Werke und Nachweise aus deutschen Einrichtungen. Die Suche ist ohne Konto möglich.",
    ["Bestände aus Bibliotheken und Archiven", "Digitalisierte Werke", "Suche ohne Konto"],
    ["Ein digitalisiertes Dokument zu finden", "Bestände mehrerer Häuser zu durchsuchen"], True)
add("Deutsche Nationalbibliografie", "https://www.dnb.de/", "dnb.de", "free", "proprietary", ["recherche", "bildung"],
    "Die Deutsche Nationalbibliothek verzeichnet in Deutschland erschienene Medien.",
    "Der Katalog der DNB weist Bücher, Zeitschriften und weitere Medien nach. Die Suche ist ohne Konto möglich.",
    ["Nachweis erschienener Medien", "Katalogsuche", "Suche ohne Konto"],
    ["Ein Buch bibliografisch nachzuweisen", "Eine Zeitschrift im Katalog zu finden"], True)
add("Projekt Gutenberg-DE", "https://www.projekt-gutenberg.org/", "projekt-gutenberg.org", "free", "proprietary", ["bildung"],
    "Projekt Gutenberg-DE stellt gemeinfreie deutsche Texte zum Lesen bereit.",
    "Die Seite zeigt Romane und Erzählungen, deren Schutz abgelaufen ist. Das Lesen im Browser ist ohne Konto möglich. Das Angebot ist nicht dasselbe wie das US-Projekt Gutenberg.",
    ["Gemeinfreie deutsche Texte", "Lesen im Browser", "Nutzung ohne Konto"],
    ["Einen gemeinfreien Roman zu lesen", "Ein Werk nach Autor zu finden"], True)
add("Zeno.org", "https://www.zeno.org/", "zeno.org", "free", "proprietary", ["bildung", "recherche"],
    "Zeno.org veröffentlicht gemeinfreie Nachschlagewerke und Literatur.",
    "Zeno.org zeigt Lexika, Quellentexte und literarische Werke. Das Lesen ist ohne Konto möglich.",
    ["Lexika und Quellentexte", "Gemeinfreie Literatur", "Lesen ohne Konto"],
    ["Einen Lexikonartikel nachzuschlagen", "Einen historischen Text zu lesen"], True)
add("Internet Archive", "https://archive.org/", "archive.org", "free", "unknown", ["recherche", "bildung"],
    "Das Internet Archive speichert Webseiten, Bücher, Filme und Software.",
    "Archive.org hält Momentaufnahmen von Seiten und digitalisierte Medien. Ein Teil ist ohne Konto lesbar. Eine OSI-Lizenz der Plattform ist hier nicht hinterlegt.",
    ["Momentaufnahmen von Webseiten", "Bücher, Filme und Software", "Lesen ohne Konto"],
    ["Eine frühere Fassung einer Seite zu öffnen", "Ein digitalisiertes Buch zu suchen"], True)
add("Wikidata", "https://www.wikidata.org/", "wikidata.org", "free", "unknown", ["daten", "recherche"],
    "Wikidata sammelt strukturierte Fakten, die Wikipedia und andere frei nutzen.",
    "Wikidata speichert Aussagen zu Einträgen mit Quellen und macht sie abfragbar. Das Bearbeiten ist ohne Abo möglich. Eine einzelne OSI-Kennung wird hier nicht eingetragen.",
    ["Strukturierte Fakten mit Quellen", "Abfrage der Daten", "Bearbeiten ohne Abo"],
    ["Ein Datum zu einem Eintrag nachzuschlagen", "Fakten für eine eigene Abfrage zu nutzen"], True)
add("Wiktionary", "https://de.wiktionary.org/", "de.wiktionary.org", "free", "unknown", ["bildung"],
    "Das deutsche Wiktionary erklärt Wörter, Beugungen und Herkunft.",
    "Der Eintrag zeigt Bedeutung, Formen und Beispiele. Das Lesen ist ohne Konto möglich. Eine einzelne OSI-Kennung wird hier nicht eingetragen.",
    ["Bedeutung und Beugung", "Herkunft und Beispiele", "Lesen ohne Konto"],
    ["Die Formen eines Verbs nachzuschlagen", "Die Herkunft eines Wortes zu lesen"], True)
add("Langenscheidt", "https://www.langenscheidt.de/", "langenscheidt.de", "freemium", "proprietary", ["bildung"],
    "Langenscheidt übersetzt Wörter und bietet Übungen für Sprachen.",
    "Langenscheidt zeigt Übersetzungen und Aussprache. Ein Teil der Suche ist ohne Abo nutzbar, Wörterbücher und Kurse sind bezahlt.",
    ["Übersetzungen und Aussprache", "Übungen", "Freie Suche und bezahlte Wörterbücher"],
    ["Ein Wort nachzuschlagen", "Eine Vokabel mit Aussprache zu hören"], True)
add("Korrekturen.de", "https://www.korrekturen.de/", "korrekturen.de", "free", "proprietary", ["bildung", "textgenerierung"],
    "Korrekturen.de erklärt Zweifelsfälle der deutschen Rechtschreibung.",
    "Die Seite zeigt, welche Schreibung empfohlen ist, und sammelt typische Fehler. Das Lesen ist ohne Konto möglich.",
    ["Zweifelsfälle der Rechtschreibung", "Typische Fehler", "Lesen ohne Konto"],
    ["Eine Schreibung zu prüfen", "Einen häufigen Fehler nachzulesen"], True)
add("Wortschatz Leipzig", "https://corpora.uni-leipzig.de/", "corpora.uni-leipzig.de", "free", "unknown", ["bildung", "recherche"],
    "Der Wortschatz der Universität Leipzig zeigt, wie Wörter in Korpora vorkommen.",
    "Die Suche liefert Beispielsätze, Nachbarn und Häufigkeiten. Die Abfrage ist ohne Konto möglich. Eine OSI-Lizenz der Website ist hier nicht hinterlegt.",
    ["Beispielsätze und Häufigkeit", "Wortnachbarn", "Abfrage ohne Konto"],
    ["Zu sehen, wie ein Wort in Sätzen steht", "Häufige Nachbarn eines Begriffs zu finden"], True)
add("synonyme.de", "https://www.synonyme.de/", "synonyme.de", "free", "proprietary", ["bildung", "textgenerierung"],
    "synonyme.de listet bedeutungsähnliche Wörter.",
    "Die Seite zeigt Synonyme zu einem Suchwort. Die Abfrage ist ohne Konto möglich.",
    ["Synonyme zu einem Wort", "Suche ohne Konto", "Kurze Trefferlisten"],
    ["Ein anderes Wort für einen Begriff zu finden", "Formulierungen zu variieren"], True)
add("buzer", "https://www.buzer.de/", "buzer.de", "free", "proprietary", ["recht"],
    "buzer zeigt deutsche Gesetze und markiert Änderungen am Wortlaut.",
    "buzer stellt Paragraphen dar und hebt, was sich geändert hat. Das Lesen ist ohne Konto möglich.",
    ["Gesetzestext mit Änderungen", "Paragraphen", "Lesen ohne Konto"],
    ["Einen Paragraphen nachzuschlagen", "Zu sehen, was sich an einer Norm geändert hat"], True)
add("Verlag C.H.Beck", "https://www.beck.de/", "beck.de", "freemium", "proprietary", ["recht"],
    "C.H.Beck verlegt Kommentare, Zeitschriften und Datenbanken zum deutschen Recht.",
    "Die Verlagsseite führt Bücher und den Zugang zu beck-online. Einzelne Hinweise sind frei lesbar, die Datenbank ist kostenpflichtig.",
    ["Kommentare und Zeitschriften", "Zugang zu beck-online", "Freie Hinweise und kostenpflichtige Datenbank"],
    ["Einen Kommentar zu einem Gesetz zu finden", "Eine Zeitschrift des Verlags zu suchen"], False)
add("BfDI", "https://www.bfdi.bund.de/", "bfdi.bund.de", "free", "proprietary", ["recht"],
    "Der Bundesbeauftragte für den Datenschutz veröffentlicht Hinweise zur DSGVO.",
    "Die Website des BfDI erklärt Zuständigkeiten und informiert über Beschwerden. Die Seiten sind ohne Konto lesbar.",
    ["Hinweise zum Datenschutz", "Zuständigkeiten und Beschwerden", "Lesen ohne Konto"],
    ["Die zuständige Aufsicht zu finden", "Einen Hinweis des BfDI zu lesen"], True)
add("BSI", "https://www.bsi.bund.de/", "bsi.bund.de", "free", "proprietary", ["programmierung", "recht"],
    "Das BSI veröffentlicht Standards und Warnungen zur IT-Sicherheit.",
    "Das Bundesamt für Sicherheit in der Informationstechnik stellt den IT-Grundschutz und aktuelle Warnungen bereit. Die Dokumente sind ohne Konto lesbar.",
    ["IT-Grundschutz", "Warnungen", "Dokumente ohne Konto"],
    ["Eine Warnung zu einer Schwachstelle zu lesen", "Einen Baustein des Grundschutzes zu öffnen"], True)
add("Datenschutz-Generator", "https://www.datenschutz-generator.de/", "datenschutz-generator.de", "freemium", "proprietary", ["recht"],
    "Der Datenschutz-Generator von eRecht24 erzeugt eine Datenschutzerklärung.",
    "Der Generator stellt Fragen zur Website und setzt daraus einen Text. Ein Teil ist frei, die aktuelle Fassung mit Updates ist kostenpflichtig.",
    ["Fragen zur eigenen Website", "Text der Datenschutzerklärung", "Freier Anteil und kostenpflichtige Updates"],
    ["Eine Datenschutzerklärung zu erzeugen", "Zu prüfen, welche Dienste im Text stehen"], True)
add("ActiveMind", "https://www.activemind.de/", "activemind.de", "freemium", "proprietary", ["recht"],
    "ActiveMind erklärt Datenschutz und bietet Generatoren für Website-Texte.",
    "ActiveMind veröffentlicht Hinweise zur DSGVO und Generatoren für Erklärungen. Ein Teil der Texte ist frei, Generatoren und Beratung sind kostenpflichtig.",
    ["Hinweise zur DSGVO", "Generatoren für Website-Texte", "Freie Texte und kostenpflichtige Generatoren"],
    ["Einen Hinweis zur DSGVO zu lesen", "Einen Text für die Website zu erzeugen"], False)
add("Händlerbund", "https://www.haendlerbund.de/", "haendlerbund.de", "paid", "proprietary", ["recht", "e-commerce"],
    "Der Händlerbund liefert Rechtstexte und Beratung für Online-Shops.",
    "Mitglieder erhalten Muster zu AGB, Widerruf und Datenschutz, abgestimmt auf den Shop. Die Mitgliedschaft ist kostenpflichtig.",
    ["Muster für AGB und Widerruf", "Datenschutztexte", "Kostenpflichtige Mitgliedschaft"],
    ["Rechtstexte für einen Shop zu beziehen", "Eine Änderung im Widerruf nachzuziehen"], False)
add("Flightright", "https://www.flightright.de/", "flightright.de", "freemium", "proprietary", ["reisen", "recht"],
    "Flightright prüft Ausgleichsansprüche nach einer Flugunregelmäßigkeit.",
    "Flightright nimmt Flugdaten entgegen und schätzt einen Anspruch nach EU-Recht. Die Prüfung ist ohne Vorkasse beschrieben, eine Durchsetzung ist erfolgsabhängig bezahlt.",
    ["Prüfung von Flugdaten", "Bezug auf EU-Ausgleich", "Erfolgsabhängige Vergütung"],
    ["Einen verspäteten Flug prüfen zu lassen", "Die Daten für eine Forderung zu erfassen"], True)
add("Fairplane", "https://www.fairplane.de/", "fairplane.de", "freemium", "proprietary", ["reisen", "recht"],
    "Fairplane setzt Entschädigungen bei Verspätung und Annulierung durch.",
    "Fairplane prüft den Flug und übernimmt die Forderung auf Erfolgsbasis. Der Dienst kommt aus Österreich.",
    ["Prüfung von Verspätung und Annulierung", "Durchsetzung auf Erfolgsbasis", "Anbieter aus Österreich"],
    ["Einen annullierten Flug auf Entschädigung zu prüfen", "Eine Forderung abzugeben"], True)
add("advocado", "https://www.advocado.de/", "advocado.de", "freemium", "proprietary", ["recht"],
    "advocado vermittelt rechtliche Ersteinschätzungen und Anwältinnen.",
    "advocado nimmt einen Sachverhalt auf und verbindet ihn mit einer Kanzlei. Ein Teil der Orientierung ist ohne sofortige Zahlung möglich, die anwaltliche Leistung ist kostenpflichtig.",
    ["Ersteinschätzung", "Vermittlung an Kanzleien", "Anwaltliche Leistung kostenpflichtig"],
    ["Einen Sachverhalt einzuordnen", "Eine Kanzlei zu einem Thema zu finden"], True)
add("legalbird", "https://www.legalbird.de/", "legalbird.de", "freemium", "proprietary", ["recht"],
    "legalbird führt durch häufige Rechtsfragen und vermittelt Anwälte.",
    "legalbird stellt Fragen zu einem Fall und zeigt, welcher Weg offen ist. Die anwaltliche Vertretung ist kostenpflichtig.",
    ["Fragen zu häufigen Fällen", "Vermittlung", "Anwaltliche Vertretung kostenpflichtig"],
    ["Einen häufigen Fall einzuordnen", "Den nächsten Schritt zu sehen"], True)
add("frag-einen-anwalt.de", "https://www.frag-einen-anwalt.de/", "frag-einen-anwalt.de", "freemium", "proprietary", ["recht"],
    "frag-einen-anwalt.de lässt eine Frage von einer Kanzlei beantworten.",
    "Die Seite nimmt eine Rechtsfrage entgegen und veröffentlicht oder übermittelt eine Antwort. Die ausführliche Beratung ist kostenpflichtig.",
    ["Fragen an Kanzleien", "Antworten auf der Plattform", "Ausführliche Beratung kostenpflichtig"],
    ["Eine Rechtsfrage zu stellen", "Ähnliche beantwortete Fragen zu lesen"], True)
add("Verbraucherzentrale", "https://www.verbraucherzentrale.de/", "verbraucherzentrale.de", "free", "proprietary", ["recht", "recherche"],
    "Die Verbraucherzentrale erklärt Verträge, Abzocke und Rechte im Alltag.",
    "Der Bundesverband veröffentlicht Ratgeber, die ohne Abo lesbar sind. Beratung vor Ort kann je nach Stelle kosten.",
    ["Ratgeber zu Verträgen und Rechten", "Hinweise zu Abzocke", "Texte ohne Abo"],
    ["Einen Vertrag einzuordnen", "Einen Ratgeber zu einem Produkt zu lesen"], True)
add("RKI", "https://www.rki.de/", "rki.de", "free", "proprietary", ["gesundheit", "recherche"],
    "Das Robert Koch-Institut veröffentlicht Zahlen und Empfehlungen zur Gesundheit.",
    "Das RKI stellt Lageberichte, Empfehlungen und Daten bereit. Die Seiten sind ohne Konto lesbar.",
    ["Empfehlungen und Lageberichte", "Daten zur Gesundheit", "Lesen ohne Konto"],
    ["Eine Empfehlung des RKI zu lesen", "Zahlen zu einer Krankheit nachzuschlagen"], True)
add("BfArM", "https://www.bfarm.de/", "bfarm.de", "free", "proprietary", ["gesundheit", "recherche"],
    "Das BfArM informiert über Arzneimittel und Medizinprodukte.",
    "Das Bundesinstitut veröffentlicht Zulassungen, Warnungen und Verzeichnisse. Die Seiten sind ohne Konto lesbar.",
    ["Arzneimittel und Medizinprodukte", "Warnungen und Verzeichnisse", "Lesen ohne Konto"],
    ["Eine Warnung zu einem Produkt zu lesen", "Ein Arzneimittel im Verzeichnis zu suchen"], True)
add("gesund.bund", "https://www.gesund.bund.de/", "gesund.bund.de", "free", "proprietary", ["gesundheit"],
    "gesund.bund erklärt Krankheitsbilder in verständlicher Sprache.",
    "Das Portal des Gesundheitsministeriums beschreibt Symptome, Untersuchungen und Anlaufstellen. Die Texte sind ohne Konto lesbar.",
    ["Krankheitsbilder in verständlicher Sprache", "Untersuchungen und Anlaufstellen", "Lesen ohne Konto"],
    ["Ein Krankheitsbild nachzulesen", "Eine Anlaufstelle zu finden"], True)
add("Ärzteblatt", "https://www.aerzteblatt.de/", "aerzteblatt.de", "freemium", "proprietary", ["gesundheit", "recherche"],
    "Das Deutsche Ärzteblatt berichtet über Medizin und Gesundheitspolitik.",
    "Ein Teil der Meldungen ist frei lesbar, das Archiv und einige Fachtexte sind kostenpflichtig.",
    ["Meldungen zu Medizin und Politik", "Fachtexte", "Freie Meldungen und kostenpflichtiges Archiv"],
    ["Eine Meldung zur Gesundheitspolitik zu lesen", "Einen Fachtext zu suchen"], False)
add("NetDoktor", "https://www.netdoktor.de/", "netdoktor.de", "free", "proprietary", ["gesundheit"],
    "NetDoktor erklärt Symptome und Krankheiten für Laien.",
    "NetDoktor beschreibt Krankheitsbilder und Untersuchungen in Alltagssprache. Die Artikel sind ohne Abo lesbar.",
    ["Symptome und Krankheiten", "Alltagssprache", "Lesen ohne Abo"],
    ["Ein Symptom einzuordnen", "Den Ablauf einer Untersuchung nachzulesen"], True)
add("samedi", "https://www.samedi.de/", "samedi.de", "freemium", "proprietary", ["gesundheit"],
    "samedi vergibt Termine für Praxen und Kliniken online.",
    "samedi zeigt freie Zeiten und schreibt den Termin in den Kalender der Einrichtung. Es gibt Angebote für Praxen, die kostenpflichtig sind.",
    ["Online-Termine für Praxen", "Kalender der Einrichtung", "Kostenpflichtige Angebote für Praxen"],
    ["Einen Arzttermin online zu buchen", "Freie Zeiten einer Praxis zu sehen"], True)
add("tomedo", "https://www.tomedo.de/", "tomedo.de", "paid", "proprietary", ["gesundheit"],
    "tomedo führt die Akte und die Abrechnung in einer Arztpraxis.",
    "tomedo speichert Patientendaten, Termine und Abrechnung auf dem System der Praxis. Der Anbieter sitzt in Deutschland. Die Lizenz ist kostenpflichtig.",
    ["Patientenakte und Termine", "Abrechnung", "Kostenpflichtige Lizenz"],
    ["Eine Praxisakte zu führen", "Termine und Abrechnung zu verbinden"], False)
add("RED medical", "https://www.redmedical.de/", "redmedical.de", "paid", "proprietary", ["gesundheit"],
    "RED medical führt die Praxissoftware in der Cloud.",
    "RED speichert Akte, Termine und Abrechnung über den Browser. Der Anbieter sitzt in Deutschland. Die Nutzung ist kostenpflichtig.",
    ["Akte, Termine und Abrechnung", "Zugriff über den Browser", "Kostenpflichtige Nutzung"],
    ["Eine Praxis ohne lokalen Server zu führen", "Die Akte im Browser zu öffnen"], False)
add("CGM", "https://www.cgm.com/", "cgm.com", "paid", "proprietary", ["gesundheit"],
    "CompuGroup Medical liefert Praxis- und Kliniksoftware.",
    "CGM verbindet Akte, Abrechnung und Vernetzung zwischen Einrichtungen. Die Systeme sind kostenpflichtig.",
    ["Praxis- und Kliniksoftware", "Abrechnung und Vernetzung", "Kostenpflichtige Systeme"],
    ["Eine Praxissoftware auszuwählen", "Daten zwischen Einrichtungen zu verbinden"], False)
add("HelloBetter", "https://www.hellobetter.de/", "hellobetter.de", "freemium", "proprietary", ["gesundheit"],
    "HelloBetter führt durch Online-Kurse zu Schlaf, Stress und Stimmung.",
    "HelloBetter gibt Einheiten mit Texten und Übungen vor. Ein Teil ist frei, Kurse auf Rezept und weitere Programme sind bezahlt.",
    ["Kurse zu Schlaf, Stress und Stimmung", "Texte und Übungen", "Freier Anteil und bezahlte Kurse"],
    ["Einen Kurs zu Schlafproblemen zu beginnen", "Übungen über mehrere Einheiten zu machen"], True)
add("Selfapy", "https://www.selfapy.com/", "selfapy.com", "freemium", "proprietary", ["gesundheit"],
    "Selfapy bietet Online-Kurse bei psychischen Belastungen.",
    "Selfapy führt durch Einheiten mit Übungen, die sich ärztlich verordnen lassen. Der Dienst kommt aus Berlin. Die Kurse sind je nach Weg kostenpflichtig oder über die Krankenkasse.",
    ["Online-Kurse mit Übungen", "Verordnung möglich", "Kosten je nach Weg"],
    ["Einen Kurs zu Depression oder Angst zu beginnen", "Übungen über Wochen zu folgen"], True)
add("MindDoc", "https://www.minddoc.de/", "minddoc.de", "freemium", "proprietary", ["gesundheit"],
    "MindDoc begleitet Stimmung und Übungen in einer App.",
    "MindDoc fragt die Stimmung ab und schlägt kurze Übungen vor. Es gibt einen Einstieg und bezahlte Inhalte.",
    ["Stimmungsabfrage", "Kurze Übungen", "Einstieg und bezahlte Inhalte"],
    ["Die Stimmung über Tage festzuhalten", "Eine kurze Übung zu starten"], True)
add("novego", "https://www.novego.de/", "novego.de", "freemium", "proprietary", ["gesundheit"],
    "novego führt Online-Programme zu Stress, Depression und Angst.",
    "novego gibt Lektionen mit Übungen vor. Programme lassen sich je nach Krankenkasse nutzen. Ein Teil ist ohne sofortige Zahlung beschrieben.",
    ["Programme zu Stress und Stimmung", "Lektionen mit Übungen", "Nutzung je nach Krankenkasse"],
    ["Ein Programm gegen Stress zu beginnen", "Lektionen über mehrere Wochen zu folgen"], True)
add("komoot", "https://www.komoot.de/", "komoot.de", "freemium", "proprietary", ["reisen"],
    "komoot plant Wander- und Radrouten und spricht sie unterwegs an.",
    "komoot baut eine Tour aus Wegen und zeigt sie auf der Karte. Der Dienst kommt aus Deutschland. Es gibt einen kostenlosen Einstieg und bezahlte Regionen oder ein Abo.",
    ["Routen für Wandern und Rad", "Ansage unterwegs", "Kostenloser Einstieg und bezahlte Regionen"],
    ["Eine Wandertour zu planen", "Eine Route unterwegs abzufahren"], True)
add("AllTrails", "https://www.alltrails.com/", "alltrails.com", "freemium", "proprietary", ["reisen"],
    "AllTrails zeigt Wanderwege mit Länge, Anstieg und Berichten.",
    "AllTrails kartiert Touren und lässt eigene Aufzeichnungen hochladen. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo für Karten offline.",
    ["Wanderwege mit Länge und Anstieg", "Berichte und Aufzeichnungen", "Kostenloser Einstieg und bezahltes Abo"],
    ["Eine Tour in der Nähe zu finden", "Länge und Anstieg vor dem Start zu prüfen"], True)
add("bahn.de", "https://www.bahn.de/", "bahn.de", "free", "proprietary", ["reisen"],
    "bahn.de sucht Verbindungen und verkauft Tickets der Deutschen Bahn.",
    "Die Auskunft zeigt Züge, Umstiege und Preise. Die Suche ist ohne Konto möglich, ein Ticket ist kostenpflichtig.",
    ["Verbindungen und Preise", "Tickets", "Suche ohne Konto"],
    ["Eine Zugverbindung zu suchen", "Ein Ticket zu buchen"], True)
add("FlixBus", "https://www.flixbus.de/", "flixbus.de", "free", "proprietary", ["reisen"],
    "FlixBus sucht Fernbusverbindungen und verkauft die Fahrkarte.",
    "FlixBus zeigt Abfahrten, Preise und Haltestellen. Die Suche ist ohne Konto möglich, die Fahrt ist kostenpflichtig.",
    ["Fernbusverbindungen", "Preise und Haltestellen", "Suche ohne Konto"],
    ["Einen Fernbus zu suchen", "Eine Fahrkarte zu buchen"], True)
add("Omio", "https://www.omio.de/", "omio.de", "free", "proprietary", ["reisen"],
    "Omio vergleicht Zug, Bus und Flug für eine Strecke.",
    "Omio stellt Verbindungen mehrerer Anbieter nebeneinander. Die Suche ist ohne Konto möglich, das Ticket ist kostenpflichtig.",
    ["Vergleich von Zug, Bus und Flug", "Mehrere Anbieter", "Suche ohne Konto"],
    ["Eine Strecke über Verkehrsmittel zu vergleichen", "Eine Verbindung zu buchen"], True)
add("Skyscanner", "https://www.skyscanner.de/", "skyscanner.de", "free", "proprietary", ["reisen"],
    "Skyscanner vergleicht Flüge über mehrere Anbieter.",
    "Skyscanner zeigt Preise nach Datum und Route. Die Suche ist ohne Konto möglich, das Ticket liegt beim jeweiligen Anbieter.",
    ["Flugvergleich", "Preise nach Datum", "Suche ohne Konto"],
    ["Einen Flugpreis über Monate zu vergleichen", "Eine Route mit Zwischenstopps zu sehen"], True)
add("Airbnb", "https://www.airbnb.de/", "airbnb.de", "free", "proprietary", ["reisen"],
    "Airbnb vermittelt Unterkünfte von privaten Gastgebern.",
    "Airbnb zeigt Wohnungen und Zimmer mit Preis und Zeitraum. Die Suche ist ohne Konto möglich, die Buchung ist kostenpflichtig.",
    ["Wohnungen und Zimmer", "Preis und Zeitraum", "Suche ohne Konto"],
    ["Eine Unterkunft für einen Zeitraum zu suchen", "Preis und Lage zu vergleichen"], True)
add("Holidu", "https://www.holidu.de/", "holidu.de", "free", "proprietary", ["reisen"],
    "Holidu vergleicht Ferienwohnungen über mehrere Portale.",
    "Holidu sammelt Angebote und zeigt sie nebeneinander. Die Suche ist ohne Konto möglich, die Buchung liegt beim jeweiligen Anbieter.",
    ["Vergleich von Ferienwohnungen", "Mehrere Portale", "Suche ohne Konto"],
    ["Eine Ferienwohnung zu vergleichen", "Preise für denselben Zeitraum zu sehen"], True)
add("TUI", "https://www.tui.com/", "tui.com", "free", "proprietary", ["reisen"],
    "TUI bucht Pauschalreisen, Hotels und Flüge.",
    "TUI zeigt Reisen mit Flug und Hotel in einem Preis. Die Suche ist ohne Konto möglich, die Reise ist kostenpflichtig.",
    ["Pauschalreisen", "Hotels und Flüge", "Suche ohne Konto"],
    ["Eine Pauschalreise zu suchen", "Hotel und Flug in einem Angebot zu sehen"], True)
add("DERTOUR", "https://www.dertour.de/", "dertour.de", "free", "proprietary", ["reisen"],
    "DERTOUR vermittelt Pauschalreisen und Bausteine aus Flug und Hotel.",
    "DERTOUR zeigt Angebote mit Preis und Zeitraum. Die Suche ist ohne Konto möglich, die Buchung ist kostenpflichtig.",
    ["Pauschalreisen und Bausteine", "Preis und Zeitraum", "Suche ohne Konto"],
    ["Eine Reise mit Flug und Hotel zu suchen", "Angebote eines Reiseziels zu vergleichen"], True)
add("CLARK", "https://www.clark.de/", "clark.de", "free", "proprietary", ["finanzen"],
    "CLARK vergleicht Versicherungen und verwaltet bestehende Verträge.",
    "CLARK zeigt Policen an einem Ort und macht Vorschläge zum Wechsel. Der Dienst kommt aus Frankfurt. Die Nutzung der Übersicht ist ohne eigenes Abo beschrieben, der Vertrag selbst ist kostenpflichtig.",
    ["Übersicht bestehender Verträge", "Vergleich und Wechsel", "Vertrag beim Versicherer kostenpflichtig"],
    ["Eigene Versicherungen zu sammeln", "Einen Tarif zu vergleichen"], True)
add("TradingView", "https://www.tradingview.com/", "tradingview.com", "freemium", "proprietary", ["finanzen"],
    "TradingView zeigt Kurse und Charts für Aktien, Devisen und Krypto.",
    "TradingView zeichnet Indikatoren auf Kursverläufe und teilt Ideen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Charts und Indikatoren", "Aktien, Devisen und Krypto", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Kursverlauf zu zeichnen", "Zwei Werte in einem Chart zu vergleichen"], True)
add("YNAB", "https://www.ynab.com/", "ynab.com", "paid", "proprietary", ["finanzen"],
    "YNAB verteilt Einkommen auf Kategorien, bevor es ausgegeben wird.",
    "YNAB gibt jedem Euro eine Aufgabe und zeigt, was noch in einer Kategorie liegt. Die Nutzung ist kostenpflichtig.",
    ["Budget nach Kategorien", "Jeder Betrag bekommt eine Aufgabe", "Kostenpflichtige Nutzung"],
    ["Ein Monatsbudget zu planen", "Zu sehen, was in einer Kategorie übrig ist"], True)
add("Finanzguru", "https://www.finanzguru.de/", "finanzguru.de", "freemium", "proprietary", ["finanzen"],
    "Finanzguru liest Kontoumsätze ein und ordnet sie Kategorien zu.",
    "Finanzguru zeigt, wohin Geld geht, und erkennt Verträge. Der Dienst kommt aus Deutschland. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Umsätze nach Kategorie", "Erkennen von Verträgen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ausgaben eines Monats zu sehen", "Einen wiederkehrenden Vertrag zu finden"], True)
add("Outbank", "https://www.outbank.de/", "outbank.de", "freemium", "proprietary", ["finanzen"],
    "Outbank bündelt Konten mehrerer Banken in einer App.",
    "Outbank zeigt Salden und Umsätze nebeneinander. Der Dienst kommt aus Deutschland. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Konten mehrerer Banken", "Salden und Umsätze", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Mehrere Konten in einer App zu sehen", "Umsätze über Banken hinweg zu lesen"], True)
add("StarMoney", "https://www.starmoney.de/", "starmoney.de", "paid", "proprietary", ["finanzen"],
    "StarMoney führt Konten, Umsätze und eine einfache Buchhaltung.",
    "StarMoney holt Umsätze ab und ordnet sie Kategorien oder Buchungen zu. Die Software kommt von der Sparkassen-Finanzgruppe. Die Nutzung ist kostenpflichtig.",
    ["Konten und Umsätze", "Kategorien und Buchungen", "Kostenpflichtige Nutzung"],
    ["Mehrere Konten auf dem Rechner zu führen", "Umsätze einer Kategorie zuzuordnen"], False)
add("MoneyMoney", "https://moneymoney-app.com/", "moneymoney-app.com", "paid", "proprietary", ["finanzen"],
    "MoneyMoney liest Bankkonten auf dem Mac und ordnet Umsätze.",
    "MoneyMoney holt Salden ab und filtert Buchungen. Die App ist einmalig kostenpflichtig.",
    ["Konten auf dem Mac", "Filter über Buchungen", "Einmalig kostenpflichtige App"],
    ["Mehrere Konten auf dem Mac zu sehen", "Buchungen zu filtern"], True)
add("Akaunting", "https://akaunting.com/", "akaunting.com", "freemium", "unknown", ["finanzen"],
    "Akaunting führt Rechnungen und Ausgaben und lässt sich selbst betreiben.",
    "Akaunting legt Kunden, Belege und Berichte an. Es gibt eine selbst betreibbare Ausgabe und eine Cloud. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Rechnungen und Ausgaben", "Selbstbetrieb und Cloud", "Lizenz nicht eingetragen"],
    ["Eine einfache Buchhaltung selbst zu hosten", "Eine Rechnung zu schreiben"], False)
add("Invoice Ninja", "https://invoiceninja.com/", "invoiceninja.com", "freemium", "unknown", ["finanzen"],
    "Invoice Ninja schreibt Rechnungen und lässt sich selbst betreiben.",
    "Invoice Ninja legt Kunden, Angebote und Zahlungslinks an. Es gibt eine gehostete Fassung und den Selbstbetrieb. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Rechnungen und Angebote", "Zahlungslinks", "Hosting und Selbstbetrieb"],
    ["Eine Rechnung mit Zahlungslink zu schicken", "Die Anwendung selbst zu hosten"], False)
add("Afterbuy", "https://www.afterbuy.de/", "afterbuy.de", "freemium", "proprietary", ["e-commerce"],
    "Afterbuy steuert Bestellungen und Listings für Marktplätze.",
    "Afterbuy holt Verkäufe aus angebundenen Kanälen und gibt sie an Versand und Rechnung weiter. Der Dienst kommt aus Deutschland. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Bestellungen aus Marktplätzen", "Versand und Rechnung", "Einstieg und bezahlte Stufen"],
    ["Verkäufe mehrerer Marktplätze zu bündeln", "Bestellungen an den Versand zu geben"], False)
add("plentymarkets", "https://www.plentymarkets.eu/", "plentymarkets.eu", "paid", "proprietary", ["e-commerce"],
    "plentymarkets führt Shop, Marktplätze und Warenwirtschaft.",
    "plentymarkets verbindet Artikel, Bestellungen und Kanäle. Der Anbieter sitzt in Kassel. Die Nutzung ist kostenpflichtig.",
    ["Shop und Marktplätze", "Warenwirtschaft", "Kostenpflichtige Nutzung"],
    ["Mehrere Verkaufskanäle zu steuern", "Bestände zentral zu führen"], False)
add("STRATO", "https://www.strato.de/", "strato.de", "paid", "proprietary", ["design"],
    "STRATO vermietet Domains, Hosting und einen Baukasten.",
    "STRATO legt Seiten, Mail und Domains an. Der Anbieter sitzt in Berlin. Die Pakete sind kostenpflichtig.",
    ["Domains, Hosting und Baukasten", "Mail zur Domain", "Kostenpflichtige Pakete"],
    ["Eine Domain mit Webspace zu mieten", "Eine einfache Seite mit dem Baukasten zu starten"], True)
add("netcup", "https://www.netcup.de/", "netcup.de", "paid", "proprietary", ["programmierung"],
    "netcup vermietet Server, Webhosting und Domains.",
    "netcup stellt virtuelle Server und Webspace bereit. Der Anbieter sitzt in Deutschland. Die Tarife sind kostenpflichtig.",
    ["Server und Webhosting", "Domains", "Kostenpflichtige Tarife"],
    ["Einen kleinen Server zu mieten", "Eine Domain auf den Server zu legen"], False)
add("Contabo", "https://contabo.com/", "contabo.com", "paid", "proprietary", ["programmierung"],
    "Contabo vermietet virtuelle Server mit viel Speicher zum Festpreis.",
    "Contabo stellt VPS und dedizierte Maschinen bereit. Der Anbieter sitzt in München. Die Miete ist kostenpflichtig.",
    ["Virtuelle und dedizierte Server", "Festpreis-Miete", "Kostenpflichtige Tarife"],
    ["Einen günstigen Server für ein Projekt zu mieten", "Mehr Speicher ohne Aufpreisstaffel zu bekommen"], False)
add("ALL-INKL", "https://all-inkl.com/", "all-inkl.com", "paid", "proprietary", ["design"],
    "ALL-INKL vermietet Webspace, Domains und Mail.",
    "ALL-INKL legt Seiten und Postfächer auf deutschem Webspace an. Die Pakete sind kostenpflichtig.",
    ["Webspace, Domains und Mail", "Betrieb in Deutschland", "Kostenpflichtige Pakete"],
    ["Eine Website auf deutschem Webspace zu betreiben", "Postfächer zur Domain anzulegen"], True)
add("mittwald", "https://www.mittwald.de/", "mittwald.de", "paid", "proprietary", ["design"],
    "mittwald hostet Agenturprojekte und Shops.",
    "mittwald stellt Projekte, Datenbanken und Support für Agenturen bereit. Der Anbieter sitzt in Espelkamp. Die Tarife sind kostenpflichtig.",
    ["Hosting für Agenturen und Shops", "Projekte und Datenbanken", "Kostenpflichtige Tarife"],
    ["Einen Kundenshop zu hosten", "Ein Projekt mit Datenbank anzulegen"], False)
add("Hetzner", "https://www.hetzner.com/", "hetzner.com", "paid", "proprietary", ["programmierung"],
    "Hetzner vermietet Cloud-Server, Storage und dedizierte Maschinen.",
    "Hetzner stellt Instanzen in eigenen Rechenzentren bereit, unter anderem in Deutschland und Finnland. Die Abrechnung folgt dem Tarif. Die Nutzung ist kostenpflichtig.",
    ["Cloud und dedizierte Server", "Rechenzentren in Europa", "Kostenpflichtige Tarife"],
    ["Einen Server in Europa zu mieten", "Speicher und Instanz zu trennen"], False)
add("Stripe", "https://stripe.com/", "stripe.com", "paid", "proprietary", ["finanzen", "e-commerce"],
    "Stripe nimmt Kartenzahlungen in eine Website oder App auf.",
    "Stripe stellt Zahlungsformulare und eine Schnittstelle bereit und zahlt Auszahlungen aus. Die Gebühr hängt von der Transaktion ab.",
    ["Kartenzahlung per Formular und API", "Auszahlungen", "Gebühr je Transaktion"],
    ["Eine Karte im eigenen Shop zu akzeptieren", "Zahlungen in einer App auszulösen"], False)
add("Mollie", "https://www.mollie.com/de", "mollie.com", "paid", "proprietary", ["finanzen", "e-commerce"],
    "Mollie bindet Zahlarten wie Karte, Klarna und Lastschrift in einen Shop ein.",
    "Mollie stellt eine Kasse für europäische Zahlarten bereit. Der Dienst kommt aus den Niederlanden. Die Gebühr hängt von der Transaktion ab.",
    ["Karte, Klarna und Lastschrift", "Kasse für Shops", "Gebühr je Transaktion"],
    ["Mehrere Zahlarten in einen Shop zu hängen", "Auszahlungen an einem Ort zu sehen"], False)
add("SumUp", "https://www.sumup.de/", "sumup.de", "freemium", "proprietary", ["finanzen", "e-commerce"],
    "SumUp nimmt Kartenzahlungen mit einem Lesegerät oder per Link entgegen.",
    "SumUp berechnet eine Gebühr je Zahlung und zahlt auf ein Konto aus. Der Dienst ist in Deutschland verbreitet. Das Lesegerät ist kostenpflichtig, ein Zahlungslink kommt ohne eigenes Terminal aus.",
    ["Kartenleser und Zahlungslink", "Gebühr je Zahlung", "Lesegerät kostenpflichtig"],
    ["Eine Karte auf einem Markt entgegenzunehmen", "Einen Zahlungslink zu schicken"], True)
add("Adyen", "https://www.adyen.com/", "adyen.com", "paid", "proprietary", ["finanzen", "e-commerce"],
    "Adyen verarbeitet Zahlungen für größere Händler über eine Plattform.",
    "Adyen bündelt Karten und lokale Zahlarten und zahlt an den Händler aus. Der Dienst kommt aus den Niederlanden. Die Nutzung ist kostenpflichtig.",
    ["Karten und lokale Zahlarten", "Eine Plattform für Händler", "Kostenpflichtige Nutzung"],
    ["Zahlungen mehrerer Länder zu bündeln", "Auszahlungen eines Händlers zu sehen"], False)
add("Wise", "https://wise.com/", "wise.com", "freemium", "proprietary", ["finanzen"],
    "Wise überweist Geld in andere Währungen zum angezeigten Kurs.",
    "Wise zeigt den Kurs vor dem Absenden und hält Konten in mehreren Währungen. Es gibt ein Konto ohne Monatsgrundgebühr, Überweisungen kosten eine ausgewiesene Gebühr.",
    ["Überweisungen in andere Währungen", "Konten in mehreren Währungen", "Ausgewiesene Gebühr je Überweisung"],
    ["Geld in eine andere Währung zu senden", "Einen Kontostand in Fremdwährung zu halten"], True)
add("bunq", "https://www.bunq.com/", "bunq.com", "paid", "proprietary", ["finanzen"],
    "bunq führt ein App-Konto mit Unterkonten und mehreren Währungen.",
    "bunq legt Unterkonten an und sortiert Ausgaben. Der Dienst kommt aus den Niederlanden. Die Konten sind kostenpflichtig.",
    ["Unterkonten und mehrere Währungen", "Ausgaben sortieren", "Kostenpflichtige Konten"],
    ["Geld auf Unterkonten zu verteilen", "Ausgaben einer Kategorie zu sehen"], True)
add("N26", "https://www.n26.com/", "n26.com", "freemium", "proprietary", ["finanzen"],
    "N26 führt ein Girokonto in der App.",
    "N26 zeigt Umsätze, Karten und Benachrichtigungen. Der Sitz der Bank ist in Berlin. Es gibt ein kostenloses Konto und bezahlte Stufen.",
    ["Girokonto in der App", "Karte und Umsätze", "Kostenloses Konto und bezahlte Stufen"],
    ["Ein Konto ohne Filiale zu führen", "Umsätze in der App zu sehen"], True)
add("PayPal", "https://www.paypal.com/", "paypal.com", "freemium", "proprietary", ["finanzen", "e-commerce"],
    "PayPal sendet Geld und nimmt Zahlungen im Shop entgegen.",
    "PayPal hält ein Guthaben, zahlt an andere Konten und bietet einen Bezahlbutton. Das Privatkonto ist ohne Monatsgebühr beschrieben, der Empfang von Geschäftszahlungen kann Gebühren haben.",
    ["Geld senden und empfangen", "Bezahlbutton für Shops", "Geschäftszahlungen können Gebühren haben"],
    ["Geld an eine Person zu senden", "Eine Zahlung im Shop über PayPal anzubieten"], True)
add("Billie", "https://www.billie.io/", "billie.io", "paid", "proprietary", ["finanzen", "e-commerce"],
    "Billie bietet Firmenkäufern einen Kauf auf Rechnung.",
    "Billie prüft den Firmenkunden und zahlt den Händler aus. Der Dienst kommt aus Berlin. Die Nutzung ist kostenpflichtig.",
    ["Kauf auf Rechnung für Firmen", "Auszahlung an den Händler", "Kostenpflichtige Nutzung"],
    ["Firmenkunden Rechnungskauf anzubieten", "Die Prüfung des Käufers abzugeben"], False)
add("Mondu", "https://www.mondu.ai/", "mondu.ai", "paid", "proprietary", ["finanzen", "e-commerce"],
    "Mondu übernimmt den Rechnungskauf zwischen Händlern.",
    "Mondu prüft den Käufer und zahlt den Verkäufer aus. Der Dienst kommt aus Berlin. Die Nutzung ist kostenpflichtig.",
    ["Rechnungskauf zwischen Firmen", "Prüfung des Käufers", "Kostenpflichtige Nutzung"],
    ["Geschäftskunden später zahlen zu lassen", "Das Ausfallrisiko abzugeben"], False)
add("Förderdatenbank", "https://www.foerderdatenbank.de/", "foerderdatenbank.de", "free", "proprietary", ["finanzen", "recherche"],
    "Die Förderdatenbank des Bundes listet Programme für Unternehmen und Gründung.",
    "Die Suche filtert Zuschüsse und Kredite nach Thema und Ort. Die Datenbank ist ohne Konto nutzbar. Den Antrag stellt die jeweilige Stelle.",
    ["Zuschüsse und Kredite", "Filter nach Thema und Ort", "Suche ohne Konto"],
    ["Ein Förderprogramm zu finden", "Voraussetzungen einer Hilfe zu lesen"], True)
add("BAFA", "https://www.bafa.de/", "bafa.de", "free", "proprietary", ["finanzen", "recherche"],
    "Das BAFA veröffentlicht Förderprogramme, unter anderem für Energie und Beratung.",
    "Das Bundesamt für Wirtschaft und Ausfuhrkontrolle beschreibt Anträge und Merkblätter. Die Seiten sind ohne Konto lesbar. Eine Förderung selbst ist an den Antrag gebunden.",
    ["Programme für Energie und Beratung", "Merkblätter und Anträge", "Lesen ohne Konto"],
    ["Ein Förderprogramm des BAFA zu finden", "Ein Merkblatt vor dem Antrag zu lesen"], True)
add("Bundesagentur für Arbeit", "https://www.arbeitsagentur.de/", "arbeitsagentur.de", "free", "proprietary", ["personal", "recherche"],
    "Die Bundesagentur für Arbeit veröffentlicht Stellen und Leistungen für Arbeitgeber.",
    "Die Website zeigt die Jobsuche und Informationen zu Kurzarbeit, Förderung und Meldungen. Ein Teil ist ohne Konto lesbar.",
    ["Jobsuche", "Leistungen für Arbeitgeber", "Texte ohne Konto"],
    ["Eine Stelle zu suchen", "Eine Meldung als Arbeitgeber nachzulesen"], True)
add("BaFin", "https://www.bafin.de/", "bafin.de", "free", "proprietary", ["finanzen", "recht"],
    "Die BaFin beaufsichtigt Banken, Versicherer und den Wertpapierhandel.",
    "Die Website veröffentlicht Warnungen, Merkblätter und Unternehmensdatenbanken. Die Seiten sind ohne Konto lesbar.",
    ["Aufsicht über Banken und Versicherer", "Warnungen und Datenbanken", "Lesen ohne Konto"],
    ["Eine Warnung der BaFin zu lesen", "Ein Unternehmen in der Datenbank zu suchen"], True)
add("Bundesbank", "https://www.bundesbank.de/", "bundesbank.de", "free", "proprietary", ["finanzen", "recherche"],
    "Die Deutsche Bundesbank veröffentlicht Statistiken, Kurse und Regeln zum Zahlungsverkehr.",
    "Die Website stellt Zeitreihen, Wechselkurse und Erklärungen bereit. Die Daten sind ohne Konto abrufbar.",
    ["Statistiken und Wechselkurse", "Regeln zum Zahlungsverkehr", "Abruf ohne Konto"],
    ["Einen Wechselkurs nachzuschlagen", "Eine Statistik der Bundesbank zu lesen"], True)
add("Statistisches Bundesamt", "https://www.destatis.de/", "destatis.de", "free", "proprietary", ["daten", "recherche"],
    "Destatis veröffentlicht amtliche Zahlen zu Bevölkerung, Wirtschaft und Preisen.",
    "Das Statistische Bundesamt stellt Tabellen und Pressemitteilungen bereit. Die Seiten sind ohne Konto lesbar.",
    ["Amtliche Zahlen", "Tabellen und Meldungen", "Lesen ohne Konto"],
    ["Eine Preisstatistik nachzuschlagen", "Eine Bevölkerungszahl zu finden"], True)
add("Moodle", "https://moodle.org/", "moodle.org", "free", "unknown", ["bildung"],
    "Moodle betreibt Lernräume mit Aufgaben, Foren und Abgaben.",
    "Moodle lässt sich auf dem eigenen Server installieren und führt Kurse mit Material und Tests. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Kurse mit Aufgaben und Foren", "Betrieb auf dem eigenen Server", "Nutzung ohne Pflichtabo"],
    ["Einen Kurs mit Abgaben zu betreiben", "Material für eine Klasse bereitzustellen"], False)
add("ILIAS", "https://www.ilias.de/", "ilias.de", "free", "unknown", ["bildung"],
    "ILIAS ist eine Lernplattform aus Deutschland für Kurse und Material.",
    "ILIAS legt Kurse, Tests und Dateien an und lässt sich selbst betreiben. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Kurse, Tests und Dateien", "Selbstbetrieb", "Nutzung ohne Pflichtabo"],
    ["Einen Hochschulkurs zu betreiben", "Tests und Material an einem Ort zu halten"], False)
add("Stud.IP", "https://www.studip.de/", "studip.de", "free", "unknown", ["bildung"],
    "Stud.IP organisiert Lehrveranstaltungen, Dateien und Termine.",
    "Stud.IP führt Veranstaltungen einer Hochschule und lässt Materialien ablegen. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Lehrveranstaltungen und Dateien", "Termine", "Nutzung ohne Pflichtabo"],
    ["Eine Veranstaltung mit Materialien zu führen", "Termine eines Semesters zu sehen"], False)
add("OpenOlat", "https://www.openolat.org/", "openolat.org", "free", "unknown", ["bildung"],
    "OpenOlat betreibt Kurse, Tests und Abgaben.",
    "OpenOlat legt Lerninhalte an und lässt sich selbst hosten. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Kurse und Tests", "Selbsthosting", "Nutzung ohne Pflichtabo"],
    ["Einen Kurs selbst zu hosten", "Eine Abgabe einzusammeln"], False)
add("H5P", "https://h5p.org/", "h5p.org", "free", "unknown", ["bildung"],
    "H5P baut interaktive Übungen, die sich in eine Lernplattform einbetten lassen.",
    "H5P erstellt Lückentexte, Videos mit Fragen und weitere Bausteine. Eine OSI-Kennung wird hier nicht eingetragen. Die Erstellung ist ohne Pflichtabo möglich.",
    ["Interaktive Übungen", "Einbettung in eine Lernplattform", "Erstellung ohne Pflichtabo"],
    ["Einen Lückentext für einen Kurs zu bauen", "Ein Video mit Fragen zu versehen"], True)
add("Anki", "https://apps.ankiweb.net/", "ankiweb.net", "free", "unknown", ["bildung"],
    "Anki wiederholt Karteikarten in Abständen, die sich nach der Antwort richten.",
    "Anki zeigt eine Karte und legt den nächsten Termin nach der Bewertung fest. Die Desktop-Anwendung ist ohne Abo erhältlich. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Karteikarten mit Abstand", "Nächster Termin nach der Antwort", "Desktop ohne Abo"],
    ["Vokabeln über Wochen zu wiederholen", "Einen eigenen Kartenstapel zu lernen"], True)
add("Quizlet", "https://quizlet.com/", "quizlet.com", "freemium", "proprietary", ["bildung"],
    "Quizlet übt Begriffe mit Karten, Tests und Spielen.",
    "Quizlet legt ein Set an und fragt die Begriffe in mehreren Formen ab. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Karten, Tests und Spiele", "Geteilte Sets", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Vokabelset zu lernen", "Ein Set mit einer Klasse zu teilen"], True)
add("Miro", "https://miro.com/", "miro.com", "freemium", "proprietary", ["produktivitaet", "design"],
    "Miro legt eine große Fläche für Notizen, Diagramme und Workshops an.",
    "Miro lässt mehrere Personen gleichzeitig auf einer Tafel arbeiten. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Unendliche Tafel", "Gleichzeitiges Arbeiten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Workshop auf einer Tafel zu halten", "Ein Diagramm mit dem Team zu skizzieren"], True)
add("Excalidraw", "https://excalidraw.com/", "excalidraw.com", "free", "unknown", ["design", "produktivitaet"],
    "Excalidraw zeichnet Diagramme im Browser, die wie von Hand skizziert aussehen.",
    "Excalidraw setzt Formen und Pfeile und lässt eine Tafel teilen. Eine OSI-Kennung wird hier nicht eingetragen. Die Fläche im Browser ist ohne Abo nutzbar.",
    ["Diagramme im Browser", "Teilen einer Tafel", "Nutzung ohne Abo"],
    ["Einen Ablauf zu skizzieren", "Eine Skizze mit anderen zu teilen"], True)
add("tldraw", "https://www.tldraw.com/", "tldraw.com", "freemium", "unknown", ["design"],
    "tldraw ist eine Zeichenfläche im Browser für Skizzen und Abläufe.",
    "tldraw setzt Formen, Texte und Pfeile und kann die Fläche teilen. Es gibt eine kostenlose Fläche und weitere Angebote. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Skizzen und Abläufe", "Teilen im Browser", "Kostenlose Fläche"],
    ["Einen Ablauf zu zeichnen", "Eine Skizze weiterzugeben"], True)
add("diagrams.net", "https://www.diagrams.net/", "diagrams.net", "free", "unknown", ["design", "produktivitaet"],
    "diagrams.net zeichnet Flussdiagramme und speichert sie lokal oder in einer Cloud.",
    "Die Anwendung, auch als draw.io bekannt, setzt Formen für Abläufe und Netzwerke. Eine OSI-Kennung wird hier nicht eingetragen. Die Nutzung im Browser ist ohne Abo möglich.",
    ["Flussdiagramme", "Speichern lokal oder in der Cloud", "Nutzung ohne Abo"],
    ["Einen Ablauf zu zeichnen", "Ein Netzwerkdiagramm abzulegen"], True)
add("Whimsical", "https://www.whimsical.com/", "whimsical.com", "freemium", "proprietary", ["design", "produktivitaet"],
    "Whimsical baut Flussdiagramme, Mindmaps und Wireframes.",
    "Whimsical legt Diagramme auf einer geteilten Fläche an. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Flussdiagramme und Mindmaps", "Wireframes", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Ablauf mit dem Team zu zeichnen", "Ein Wireframe einer Seite zu skizzieren"], True)
add("Lucid", "https://www.lucid.co/", "lucid.co", "freemium", "proprietary", ["design", "produktivitaet"],
    "Lucid zeichnet Diagramme und arbeitet mit anderen auf derselben Fläche.",
    "Lucidchart und Lucidspark liegen unter lucid.co und setzen Abläufe, Organigramme und Tafeln. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Diagramme und Tafeln", "Gemeinsames Arbeiten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Organigramm zu zeichnen", "Einen Ablauf mit dem Team zu bearbeiten"], False)
add("Conceptboard", "https://www.conceptboard.com/de/", "conceptboard.com", "freemium", "proprietary", ["produktivitaet"],
    "Conceptboard hält Workshops auf einer Online-Tafel, der Anbieter sitzt in Stuttgart.",
    "Conceptboard lässt Notizen, Bilder und Kommentare auf einer Fläche zu. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Online-Tafel für Workshops", "Anbieter aus Stuttgart", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Workshop remote zu moderieren", "Ideen auf einer Fläche zu sammeln"], True)
add("Padlet", "https://padlet.com/", "padlet.com", "freemium", "proprietary", ["bildung", "produktivitaet"],
    "Padlet sammelt Notizen, Bilder und Links auf einer gemeinsamen Wand.",
    "Padlet legt eine Wand an, auf die mehrere Personen Beiträge setzen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Gemeinsame Wand", "Notizen, Bilder und Links", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ideen einer Klasse zu sammeln", "Links zu einem Thema zu bündeln"], True)
add("Milanote", "https://milanote.com/", "milanote.com", "freemium", "proprietary", ["produktivitaet", "design"],
    "Milanote legt Notizen, Bilder und Aufgaben auf einer Pinnwand ab.",
    "Milanote sammelt Material für ein Projekt auf einer Fläche. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Pinnwand für Notizen und Bilder", "Aufgaben auf der Fläche", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Recherche für ein Projekt zu sammeln", "Bilder und Notizen nebeneinander zu legen"], True)
add("Linear", "https://linear.app/", "linear.app", "paid", "proprietary", ["produktivitaet", "programmierung"],
    "Linear führt Aufgaben und Zyklen für Softwareteams.",
    "Linear legt Issues, Projekte und Zyklen an und zeigt, was als Nächstes ansteht. Die Nutzung ist kostenpflichtig.",
    ["Issues und Projekte", "Zyklen", "Kostenpflichtige Nutzung"],
    ["Einen Fehler als Issue zu führen", "Die Arbeit eines Zyklus zu sehen"], False)
add("Trello", "https://trello.com/", "trello.com", "freemium", "proprietary", ["produktivitaet"],
    "Trello ordnet Aufgaben als Karten auf Listen.",
    "Trello zieht Karten von einer Liste in die nächste und hängt Checklisten an. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Karten auf Listen", "Checklisten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Aufgabe durch Stufen zu ziehen", "Ein kleines Projekt als Board zu sehen"], True)
add("Basecamp", "https://basecamp.com/", "basecamp.com", "paid", "proprietary", ["produktivitaet"],
    "Basecamp bündelt Nachrichten, Aufgaben und Dateien eines Projekts.",
    "Basecamp legt pro Projekt eine Pinnwand, eine Aufgabenliste und einen Chat an. Die Nutzung ist kostenpflichtig.",
    ["Nachrichten, Aufgaben und Dateien", "Ein Raum je Projekt", "Kostenpflichtige Nutzung"],
    ["Ein Projekt mit dem Kunden zu führen", "Aufgaben neben dem Chat zu halten"], False)
add("ClickUp", "https://www.clickup.com/", "clickup.com", "freemium", "proprietary", ["produktivitaet"],
    "ClickUp führt Aufgaben als Liste, Board oder Zeitstrahl.",
    "ClickUp legt Aufgaben mit Status, Datum und Unterpunkten an. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Liste, Board und Zeitstrahl", "Status und Unterpunkte", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Aufgaben eines Teams in einer Ansicht zu sehen", "Dieselbe Arbeit als Board oder Liste zu schalten"], True)
add("Asana", "https://www.asana.com/", "asana.com", "freemium", "proprietary", ["produktivitaet"],
    "Asana verteilt Aufgaben in Projekte und zeigt, wer woran arbeitet.",
    "Asana legt Aufgaben mit Datum und Zuständigkeit an. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Aufgaben mit Zuständigkeit", "Projekte und Datum", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Arbeit in einem Team zu verteilen", "Zu sehen, was diese Woche fällig ist"], True)
add("Jira", "https://www.atlassian.com/software/jira", "atlassian.com", "freemium", "proprietary", ["produktivitaet", "programmierung"],
    "Jira führt Vorgänge, Boards und Releases für Softwareteams.",
    "Jira legt Issues an und zeigt sie auf einem Board. Es gibt einen kostenlosen Einstieg für kleine Teams und bezahlte Stufen.",
    ["Issues und Boards", "Releases", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Fehler bis zur Behebung zu führen", "Die Arbeit eines Sprints zu sehen"], False)
add("Slack", "https://www.slack.com/", "slack.com", "freemium", "proprietary", ["produktivitaet"],
    "Slack legt Kanäle und Direktnachrichten für ein Team an.",
    "Slack sortiert Gespräche nach Kanal und durchsucht den Verlauf. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Kanäle und Direktnachrichten", "Durchsuchbarer Verlauf", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Team nach Themen zu sortieren", "Eine Entscheidung im Verlauf nachzulesen"], True)
add("Mattermost", "https://www.mattermost.com/", "mattermost.com", "freemium", "unknown", ["produktivitaet"],
    "Mattermost legt Team-Chat in Kanälen an und lässt sich selbst betreiben.",
    "Mattermost führt Kanäle und Direktnachrichten auf dem eigenen Server oder in der Cloud. Eine OSI-Kennung der aktuellen Ausgabe wird hier nicht eingetragen.",
    ["Kanäle und Direktnachrichten", "Selbstbetrieb und Cloud", "Lizenz nicht eingetragen"],
    ["Einen Team-Chat selbst zu hosten", "Kanäle nach Thema zu trennen"], False)
add("Rocket.Chat", "https://www.rocket.chat/", "rocket.chat", "freemium", "unknown", ["produktivitaet", "kundenservice"],
    "Rocket.Chat führt Team-Nachrichten und lässt sich selbst betreiben.",
    "Rocket.Chat legt Kanäle an und kann Gespräche mit außen anbinden. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine Cloud und den Selbstbetrieb.",
    ["Kanäle und äußere Gespräche", "Cloud und Selbstbetrieb", "Lizenz nicht eingetragen"],
    ["Einen Chat selbst zu hosten", "Kundengespräche in einem Kanal zu lesen"], False)
add("Zulip", "https://www.zulip.com/", "zulip.com", "freemium", "unknown", ["produktivitaet"],
    "Zulip sortiert Team-Nachrichten nach Thema statt nur nach Kanal.",
    "Zulip legt Themen in einen Kanal, sodass ein Gespräch am Betreff hängen bleibt. Es gibt eine Cloud und den Selbstbetrieb. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Themen innerhalb eines Kanals", "Cloud und Selbstbetrieb", "Lizenz nicht eingetragen"],
    ["Ein Gespräch an einem Betreff zu halten", "Einen Chat selbst zu betreiben"], False)
add("Pumble", "https://pumble.com/", "pumble.com", "freemium", "proprietary", ["produktivitaet"],
    "Pumble legt Kanäle und Direktnachrichten für kleine Teams an.",
    "Pumble sortiert den Chat nach Kanal. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Kanäle und Direktnachrichten", "Verlauf", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Team-Chat ohne großes Abo zu starten", "Nachrichten nach Kanal zu trennen"], True)
add("Twist", "https://www.twist.com/", "twist.com", "freemium", "proprietary", ["produktivitaet"],
    "Twist legt Gespräche als Threads ab statt als endlosen Chat.",
    "Twist sortiert Nachrichten nach Thema und lässt sie asynchron liegen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Threads nach Thema", "Asynchrone Nachrichten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Entscheidung in einem Thread festzuhalten", "Nachrichten ohne Live-Druck zu lesen"], True)
add("Element", "https://element.io/", "element.io", "freemium", "unknown", ["social-media"],
    "Element ist ein Client für das Matrix-Netz und lässt Räume selbst betreiben.",
    "Element führt Chats und Räume über Matrix. Den Heimserver kann man selbst stellen oder den gehosteten Dienst nutzen. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Chats über Matrix", "Eigener oder gehosteter Server", "Lizenz nicht eingetragen"],
    ["Einen Raum auf einem eigenen Server zu führen", "Verschlüsselte Nachrichten zu senden"], False)
add("Session", "https://www.session.im/", "session.im", "free", "unknown", ["social-media"],
    "Session verschickt Nachrichten ohne Telefonnummer als Konto.",
    "Session nutzt eine Kennung statt einer Rufnummer. Eine OSI-Kennung wird hier nicht eingetragen. Die App ist ohne Abo erhältlich.",
    ["Nachrichten ohne Telefonnummer", "Kennung statt Rufnummer", "Nutzung ohne Abo"],
    ["Einen Chat ohne Telefonnummer zu starten", "Eine Nachricht über Session zu senden"], False)
add("Briar", "https://briarproject.org/", "briarproject.org", "free", "unknown", ["social-media"],
    "Briar tauscht Nachrichten direkt zwischen Geräten, auch über Bluetooth.",
    "Briar verbindet Kontakte ohne einen zentralen Server. Eine OSI-Kennung wird hier nicht eingetragen. Die App ist ohne Abo erhältlich.",
    ["Nachrichten ohne zentralen Server", "Auch über Bluetooth", "Nutzung ohne Abo"],
    ["Eine Nachricht ohne zentralen Dienst zu senden", "Kontakte direkt zu verbinden"], False)
add("XMPP", "https://xmpp.org/", "xmpp.org", "free", "unknown", ["social-media"],
    "XMPP ist ein offener Standard für Chat zwischen Servern.",
    "Die Website erklärt das Protokoll und verweist auf Clients und Server. Eine OSI-Kennung des Standards wird hier nicht als Produktlizenz eingetragen. Die Spezifikation ist ohne Abo lesbar.",
    ["Offener Chat-Standard", "Clients und Server", "Spezifikation ohne Abo"],
    ["Einen eigenen Chat-Server zu wählen", "Zu verstehen, wie Clients sich verbinden"], False)
add("Gajim", "https://gajim.org/", "gajim.org", "free", "unknown", ["social-media"],
    "Gajim ist ein Desktop-Client für XMPP.",
    "Gajim verbindet sich mit einem XMPP-Server und führt Chats und Gruppen. Eine OSI-Kennung wird hier nicht eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Desktop-Client für XMPP", "Chats und Gruppen", "Nutzung ohne Pflichtabo"],
    ["Einen XMPP-Account auf dem Desktop zu nutzen", "Eine Gruppe im Client zu öffnen"], False)
add("Dino", "https://dino.im/", "dino.im", "free", "unknown", ["social-media"],
    "Dino ist ein schlanker XMPP-Client für den Desktop.",
    "Dino zeigt Gespräche und unterstützt verschlüsselte Chats, wenn der Server es zulässt. Eine OSI-Kennung wird hier nicht eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Schlanker Desktop-Client", "Verschlüsselte Chats", "Nutzung ohne Pflichtabo"],
    ["Einen XMPP-Chat auf dem Desktop zu führen", "Eine Unterhaltung verschlüsselt zu halten"], False)
add("Conversations", "https://conversations.im/", "conversations.im", "paid", "unknown", ["social-media"],
    "Conversations ist ein XMPP-Client für Android.",
    "Conversations führt Chats und Gruppen über einen XMPP-Server. Die App im Play Store ist kostenpflichtig. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["XMPP auf Android", "Chats und Gruppen", "Kostenpflichtige App"],
    ["Einen XMPP-Chat auf dem Handy zu führen", "Eine Gruppe über den eigenen Server zu nutzen"], False)
add("Roundcube", "https://roundcube.net/", "roundcube.net", "free", "unknown", ["produktivitaet"],
    "Roundcube liest E-Mail im Browser auf dem eigenen Server.",
    "Roundcube zeigt Postfach, Kontakte und Ordner über IMAP. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Webmail über IMAP", "Kontakte und Ordner", "Nutzung ohne Pflichtabo"],
    ["Webmail auf dem eigenen Server zu betreiben", "Mehrere Ordner im Browser zu lesen"], False)
add("SnappyMail", "https://snappymail.eu/", "snappymail.eu", "free", "unknown", ["produktivitaet"],
    "SnappyMail ist eine schlanke Webmail für den eigenen Server.",
    "SnappyMail zeigt das Postfach im Browser und spricht IMAP. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Schlanke Webmail", "IMAP", "Nutzung ohne Pflichtabo"],
    ["Ein Postfach im Browser selbst zu hosten", "Mail ohne großen Webmail-Client zu lesen"], False)
add("Betterbird", "https://www.betterbird.eu/", "betterbird.eu", "free", "unknown", ["produktivitaet"],
    "Betterbird ist ein Thunderbird-Build mit zusätzlichen Korrekturen.",
    "Betterbird liest Mail und Kalender und übernimmt das Profil von Thunderbird. Eine OSI-Kennung wird hier nicht getrennt eingetragen. Die Anwendung ist ohne Abo erhältlich.",
    ["Mail und Kalender", "Profil von Thunderbird", "Nutzung ohne Abo"],
    ["Einen Mail-Client mit den Thunderbird-Daten zu nutzen", "Kalender neben dem Posteingang zu führen"], True)
add("Fastmail", "https://www.fastmail.com/", "fastmail.com", "paid", "proprietary", ["produktivitaet"],
    "Fastmail führt E-Mail, Kalender und Kontakte.",
    "Fastmail stellt Postfächer mit eigener Domain und Filterregeln bereit. Die Nutzung ist kostenpflichtig.",
    ["Mail, Kalender und Kontakte", "Eigene Domain und Filter", "Kostenpflichtige Nutzung"],
    ["Mail unter der eigenen Domain zu führen", "Filterregeln für den Posteingang zu setzen"], False)
add("HEY", "https://www.hey.com/", "hey.com", "paid", "proprietary", ["produktivitaet"],
    "HEY sortiert eingehende Mail in Imbox, Feed und Paper Trail.",
    "HEY verlangt, dass Absender einmal freigegeben werden, und legt den Rest beiseite. Die Nutzung ist kostenpflichtig.",
    ["Freigabe neuer Absender", "Getrennte Fächer", "Kostenpflichtige Nutzung"],
    ["Den Posteingang auf freigegebene Absender zu begrenzen", "Newsletter von echter Mail zu trennen"], False)
add("Superhuman", "https://www.superhuman.com/", "superhuman.com", "paid", "proprietary", ["produktivitaet"],
    "Superhuman beschleunigt das Abarbeiten des Posteingangs mit Tasten.",
    "Superhuman zeigt Mail in einer auf Geschwindigkeit ausgelegten Oberfläche. Die Nutzung ist kostenpflichtig.",
    ["Posteingang über Tasten", "Schnelle Oberfläche", "Kostenpflichtige Nutzung"],
    ["Einen vollen Posteingang zügig zu leeren", "Mail ohne Maus zu sortieren"], False)
add("Spark", "https://sparkmailapp.com/", "sparkmailapp.com", "freemium", "proprietary", ["produktivitaet"],
    "Spark bündelt mehrere Postfächer und schlägt kurze Antworten vor.",
    "Spark zeigt Konten nebeneinander und kann eine Antwort als Entwurf setzen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Mehrere Postfächer", "Kurze Antwortentwürfe", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Mehrere Konten in einer App zu lesen", "Eine kurze Antwort vorbereiten zu lassen"], True)
add("Mailspring", "https://www.getmailspring.com/", "getmailspring.com", "freemium", "unknown", ["produktivitaet"],
    "Mailspring liest mehrere IMAP-Konten auf dem Desktop.",
    "Mailspring zeigt Postfächer nebeneinander und setzt Signaturen und Vorlagen. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine kostenlose Fassung und bezahlte Funktionen.",
    ["Mehrere IMAP-Konten", "Signaturen und Vorlagen", "Kostenlose Fassung und bezahlte Funktionen"],
    ["Mehrere Konten auf dem Desktop zu lesen", "Eine Signatur an eine Mail zu hängen"], True)
add("grommunio", "https://www.grommunio.com/", "grommunio.com", "freemium", "unknown", ["produktivitaet"],
    "grommunio betreibt Groupware mit Mail und Kalender auf dem eigenen Server.",
    "grommunio stellt Postfach, Kontakte und Kalender bereit und spricht gängige Clients. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine Community-Ausgabe und bezahlte Angebote.",
    ["Mail und Kalender auf dem eigenen Server", "Clients", "Community-Ausgabe und bezahlte Angebote"],
    ["Groupware selbst zu betreiben", "Kalender und Mail für ein Team zu halten"], False)
add("Stalwart", "https://stalw.art/", "stalw.art", "free", "unknown", ["programmierung"],
    "Stalwart ist ein Mailserver für den eigenen Betrieb.",
    "Stalwart nimmt und sendet Mail und spricht moderne Protokolle. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Mailserver zum Selbstbetrieb", "Moderne Protokolle", "Nutzung ohne Pflichtabo"],
    ["Einen Mailserver selbst zu betreiben", "Postfächer auf der eigenen Domain zu halten"], False)
add("Disroot", "https://disroot.org/", "disroot.org", "free", "unknown", ["produktivitaet"],
    "Disroot stellt Mail, Cloud und weitere Dienste ohne Werbekonto bereit.",
    "Disroot bietet ein Postfach und angegliederte Werkzeuge, getragen von einer Gemeinschaft. Eine OSI-Kennung der Plattform wird hier nicht eingetragen. Die Nutzung ist ohne Abo beschrieben.",
    ["Mail und Cloud", "Gemeinschaft getragen", "Nutzung ohne Abo"],
    ["Ein Postfach ohne Werbenetz zu nutzen", "Dateien neben der Mail abzulegen"], True)
add("systemli", "https://systemli.org/", "systemli.org", "free", "unknown", ["produktivitaet"],
    "systemli betreibt Mail und Dienste für politisch Aktive.",
    "systemli stellt Postfächer und weitere Werkzeuge nach eigenen Aufnahmebedingungen bereit. Eine OSI-Kennung wird hier nicht eingetragen. Ein Preisabo nennt die Seite nicht.",
    ["Mail für politisch Aktive", "Weitere Werkzeuge", "Kein Preisabo auf der Seite"],
    ["Ein Postfach bei einem unabhängigen Anbieter zu nutzen", "Die Aufnahmebedingungen zu lesen"], False)
add("Riseup", "https://riseup.net/", "riseup.net", "free", "unknown", ["produktivitaet"],
    "Riseup stellt Mail und weitere Dienste für aktivistische Gruppen bereit.",
    "Riseup vergibt Postfächer nach eigenen Kriterien. Eine OSI-Kennung wird hier nicht eingetragen. Ein Preisabo nennt die Seite nicht.",
    ["Mail für Gruppen", "Vergabe nach eigenen Kriterien", "Kein Preisabo auf der Seite"],
    ["Ein Postfach bei einem aktivistischen Anbieter zu beantragen", "Die angebotenen Dienste zu lesen"], False)
add("GMX", "https://www.gmx.net/", "gmx.net", "freemium", "proprietary", ["produktivitaet"],
    "GMX stellt E-Mail und Cloud-Speicher bereit.",
    "GMX führt ein Postfach mit eigener Adresse und zusätzlichem Speicher in bezahlten Stufen. Der Dienst ist in Deutschland verbreitet. Es gibt einen kostenlosen Einstieg.",
    ["E-Mail und Cloud-Speicher", "Verbreitung in Deutschland", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein kostenloses Postfach zu nutzen", "Mehr Speicher dazuzubuchen"], True)
add("WEB.DE", "https://www.web.de/", "web.de", "freemium", "proprietary", ["produktivitaet"],
    "WEB.DE stellt E-Mail und Cloud-Speicher bereit.",
    "WEB.DE führt ein Postfach und bietet mehr Speicher in bezahlten Stufen. Der Dienst ist in Deutschland verbreitet. Es gibt einen kostenlosen Einstieg.",
    ["E-Mail und Cloud", "Verbreitung in Deutschland", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Postfach mit deutscher Adresse zu nutzen", "Mail im Browser zu lesen"], True)
add("T-Online", "https://www.t-online.de/", "t-online.de", "free", "proprietary", ["recherche"],
    "t-online veröffentlicht Nachrichten und bietet ein E-Mail-Postfach.",
    "Das Portal zeigt Meldungen aus Deutschland und verlinkt auf Mail. Die Nachrichten sind ohne Abo lesbar.",
    ["Nachrichten aus Deutschland", "Verweis auf Mail", "Lesen ohne Abo"],
    ["Eine Meldung des Tages zu lesen", "Zum Postfach zu wechseln"], True)
add("freenet", "https://www.freenet.de/", "freenet.de", "freemium", "proprietary", ["produktivitaet"],
    "freenet bietet Mail und Mobilfunk aus einer Hand.",
    "freenet führt ein Postfach und Mobilfunkverträge. Mail hat einen kostenlosen Einstieg, Mobilfunk ist kostenpflichtig.",
    ["Mail und Mobilfunk", "Kostenloser Mail-Einstieg", "Mobilfunk kostenpflichtig"],
    ["Ein Postfach bei freenet zu nutzen", "Einen Mobilfunkvertrag zu vergleichen"], True)
add("all-inkl.com bleibt", "https://all-inkl.com/", "all-inkl.com", "paid", "proprietary", ["design"],
    "Platzhalter.",
    "Platzhalter.",
    ["x"], ["x"])


def validate(entries):
    skip = {
        "ILIAS", "H5P", "Miro", "Excalidraw", "tldraw", "Whimsical", "Zulip", "Element",
        "Korrekturen.de", "Moodle", "Quizlet", "Lucid", "Padlet", "Zeno.org",
        "komoot", "YNAB", "Anki", "diagrams.net",
    }
    entries[:] = [e for e in entries if not e["name"].endswith("bleibt") and e["name"] not in skip]
    domains = {row[0] for row in sqlite3.connect(ROOT / "data" / "linkjagd.db").execute("select domain from tools")}
    seen = set()
    errors = []
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
    if errors:
        raise SystemExit("\n".join(errors[:50]))
    return entries


if __name__ == "__main__":
    rows = validate(E)
    out = ROOT / "data" / "verified-tools-batch6.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows), "->", out)
