#!/usr/bin/env python3
"""Siebte geprüfte Liste. Kurznamen werden gegen den Bestand geprüft."""

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
    out = []
    prev = False
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


add("Linguee", "https://www.linguee.de/", "linguee.de", "free", "proprietary", ["bildung"],
    "Linguee zeigt Übersetzungen zusammen mit echten Beispielsätzen.",
    "Linguee durchsucht zweisprachige Texte und stellt das Wort im Zusammenhang dar. Die Suche ist ohne Konto möglich.",
    ["Übersetzungen mit Beispielsätzen", "Mehrere Sprachen neben Deutsch", "Suche ohne Konto"],
    ["Ein Wort im Satzzusammenhang zu sehen", "Eine Wendung statt nur ein Einzelwort zu prüfen"], True)
add("Bab.la", "https://de.bab.la/", "de.bab.la", "free", "proprietary", ["bildung"],
    "Bab.la übersetzt Wörter und zeigt Konjugationen.",
    "Bab.la listet Bedeutungen, Beispiele und Beugungen. Die Suche ist ohne Konto möglich.",
    ["Wörter und Konjugationen", "Beispielsätze", "Suche ohne Konto"],
    ["Ein Verb zu beugen", "Eine Übersetzung mit Beispiel zu lesen"], True)
add("Cambridge Dictionary", "https://dictionary.cambridge.org/", "dictionary.cambridge.org", "free", "proprietary", ["bildung"],
    "Das Cambridge Dictionary erklärt englische Wörter mit Aussprache und Niveau.",
    "Der Eintrag zeigt Bedeutung, Aussprache und Beispielsätze, oft mit Angabe des Sprachniveaus. Die Suche ist ohne Konto möglich.",
    ["Bedeutung und Aussprache", "Beispielsätze", "Suche ohne Konto"],
    ["Ein englisches Wort nachzuschlagen", "Die Aussprache anzuhören"], True)
add("WordReference", "https://www.wordreference.com/", "wordreference.com", "free", "proprietary", ["bildung"],
    "WordReference übersetzt Wörter und führt dazu ein Forum mit Zweifelsfällen.",
    "Die Wörterbücher zeigen Bedeutungen und Wendungen, das Forum sammelt Rückfragen. Die Suche ist ohne Konto möglich.",
    ["Wörterbücher", "Forum zu Zweifelsfällen", "Suche ohne Konto"],
    ["Eine Wendung nachzuschlagen", "Einen Zweifelsfall im Forum zu lesen"], True)
add("Greenhouse", "https://www.greenhouse.io/", "greenhouse.io", "paid", "proprietary", ["personal"],
    "Greenhouse führt Bewerbungen von der Anzeige bis zur Zusage.",
    "Greenhouse legt Stellen an, sammelt Unterlagen und führt Bewerbende durch Stufen. Die Nutzung ist kostenpflichtig.",
    ["Stellen und Bewerbungsstufen", "Gemeinsame Bewertung", "Kostenpflichtige Nutzung"],
    ["Bewerbungen einer Stelle zu sammeln", "Eine Entscheidung im Team festzuhalten"], False)
add("Teamtailor", "https://www.teamtailor.com/", "teamtailor.com", "paid", "proprietary", ["personal"],
    "Teamtailor baut eine Karriereseite und sammelt Bewerbungen.",
    "Teamtailor zeigt offene Stellen auf einer eigenen Seite und legt eingehende Bewerbungen ab. Die Nutzung ist kostenpflichtig.",
    ["Karriereseite", "Bewerbungen an einem Ort", "Kostenpflichtige Nutzung"],
    ["Offene Stellen auf einer Karriereseite zu zeigen", "Bewerbungen nach Stufe zu sortieren"], False)
add("Lattice", "https://www.lattice.com/", "lattice.com", "paid", "proprietary", ["personal"],
    "Lattice führt Ziele, Feedback und Mitarbeitergespräche.",
    "Lattice legt Ziele an und sammelt Rückmeldungen und Gesprächsnotizen. Die Nutzung ist kostenpflichtig.",
    ["Ziele und Feedback", "Gesprächsnotizen", "Kostenpflichtige Nutzung"],
    ["Ein Ziel für ein Quartal festzuhalten", "Ein Mitarbeitergespräch vorzubereiten"], False)
add("Culture Amp", "https://www.cultureamp.com/", "cultureamp.com", "paid", "proprietary", ["personal"],
    "Culture Amp befragt Belegschaften und wertet die Antworten aus.",
    "Culture Amp verschickt Umfragen zu Stimmung und Führung und zeigt die Ergebnisse nach Team. Die Nutzung ist kostenpflichtig.",
    ["Mitarbeiterumfragen", "Auswertung nach Team", "Kostenpflichtige Nutzung"],
    ["Eine Stimmungsumfrage zu starten", "Ergebnisse zweier Teams zu vergleichen"], False)
add("BambooHR", "https://www.bamboohr.com/", "bamboohr.com", "paid", "proprietary", ["personal"],
    "BambooHR führt Personalakten, Urlaub und Bewerbungen.",
    "BambooHR speichert Stammdaten, Abwesenheiten und den Eingang von Bewerbungen. Die Nutzung ist kostenpflichtig.",
    ["Personalakten und Urlaub", "Bewerbungseingang", "Kostenpflichtige Nutzung"],
    ["Eine Personalakte zu führen", "Urlaubsanträge zu sammeln"], False)
add("Workday", "https://www.workday.com/", "workday.com", "paid", "proprietary", ["personal", "finanzen"],
    "Workday führt Personal, Lohn und Finanzen großer Organisationen.",
    "Workday bündelt Stammdaten, Abrechnung und Berichte. Die Einführung ist ein kostenpflichtiges Unternehmensprojekt.",
    ["Personal und Lohn", "Finanzberichte", "Kostenpflichtige Einführung"],
    ["Personaldaten einer großen Organisation zu führen", "Lohn und Stammdaten zu verbinden"], False)
add("Rippling", "https://www.rippling.com/", "rippling.com", "paid", "proprietary", ["personal"],
    "Rippling legt Beschäftigte an und hängt Geräte, Lohn und Zugänge daran.",
    "Rippling startet mit der Person und schaltet davon Konten und Geräte. Die Nutzung ist kostenpflichtig.",
    ["Personal, Geräte und Zugänge", "Lohn", "Kostenpflichtige Nutzung"],
    ["Einen neuen Zugang zusammen mit der Personalakte anzulegen", "Geräte einer Person zuzuordnen"], False)
add("Kayak", "https://www.kayak.de/", "kayak.de", "free", "proprietary", ["reisen"],
    "Kayak vergleicht Flüge, Hotels und Mietwagen.",
    "Kayak stellt Angebote mehrerer Anbieter nebeneinander. Die Suche ist ohne Konto möglich, die Buchung liegt beim Anbieter.",
    ["Vergleich von Flügen und Hotels", "Mietwagen", "Suche ohne Konto"],
    ["Einen Flugpreis über Tage zu vergleichen", "Hotel und Flug nebeneinander zu sehen"], True)
add("Momondo", "https://www.momondo.de/", "momondo.de", "free", "proprietary", ["reisen"],
    "Momondo vergleicht Flugpreise über mehrere Anbieter.",
    "Momondo zeigt Preise nach Route und Datum. Die Suche ist ohne Konto möglich, das Ticket liegt beim jeweiligen Anbieter.",
    ["Flugvergleich", "Preise nach Datum", "Suche ohne Konto"],
    ["Eine Route über mehrere Tage zu prüfen", "Anbieterpreise gegenüberzustellen"], True)
add("Booking.com", "https://www.booking.com/", "booking.com", "free", "proprietary", ["reisen"],
    "Booking.com zeigt Unterkünfte mit Preis, Lage und Bewertungen.",
    "Die Suche filtert nach Zeitraum und Ort. Ein Konto ist für die Suche nicht nötig, die Buchung ist kostenpflichtig.",
    ["Unterkünfte mit Preis und Lage", "Bewertungen", "Suche ohne Konto"],
    ["Ein Hotel für einen Zeitraum zu suchen", "Preise in einer Stadt zu vergleichen"], True)
add("Geizhals", "https://www.geizhals.de/", "geizhals.de", "free", "proprietary", ["recherche", "e-commerce"],
    "Geizhals vergleicht Preise von Elektronik und anderen Waren im deutschsprachigen Handel.",
    "Geizhals listet Angebote mehrerer Shops zu einem Produkt und zeigt die Preisentwicklung. Die Suche ist ohne Konto möglich.",
    ["Preisvergleich über Shops", "Preisentwicklung", "Suche ohne Konto"],
    ["Den günstigsten Shop zu einem Gerät zu finden", "Die Preisentwicklung eines Produkts zu sehen"], True)
add("billiger.de", "https://www.billiger.de/", "billiger.de", "free", "proprietary", ["recherche", "e-commerce"],
    "billiger.de vergleicht Preise über viele Online-Shops.",
    "Die Seite stellt Angebote zu einem Suchbegriff nebeneinander. Die Suche ist ohne Konto möglich, der Kauf liegt im jeweiligen Shop.",
    ["Preisvergleich", "Angebote mehrerer Shops", "Suche ohne Konto"],
    ["Einen Preis vor dem Kauf zu vergleichen", "Shops zu einem Produkt zu sehen"], True)
add("CHIP", "https://www.chip.de/", "chip.de", "free", "proprietary", ["recherche"],
    "CHIP testet Technik und veröffentlicht Ratgeber und Downloads.",
    "CHIP berichtet über Geräte und Software und stellt einen Teil der Tests frei lesbar bereit. Einzelne Downloads und Tests können weitere Bedingungen haben, die die Seite nennt.",
    ["Techniktests und Ratgeber", "Downloads", "Texte ohne Abo"],
    ["Einen Test zu einem Gerät zu lesen", "Einen Ratgeber zu Software zu suchen"], True)
add("heise", "https://www.heise.de/", "heise.de", "freemium", "proprietary", ["recherche"],
    "heise berichtet über IT, Sicherheit und Technik aus Deutschland.",
    "heise online veröffentlicht Meldungen, ein Teil davon frei und ein Teil hinter einem kostenpflichtigen Zugang. Der Verlag sitzt in Hannover.",
    ["Meldungen zu IT und Sicherheit", "Verlag aus Hannover", "Freie Meldungen und kostenpflichtiger Zugang"],
    ["Eine Meldung zur IT-Sicherheit zu lesen", "Einen Hintergrundartikel zu suchen"], True)
add("Golem", "https://www.golem.de/", "golem.de", "freemium", "proprietary", ["recherche"],
    "Golem berichtet über IT, Wissenschaft und Technik.",
    "Golem veröffentlicht Meldungen und Tests. Ein Teil ist frei lesbar, Golem Pur ist kostenpflichtig.",
    ["Meldungen und Tests", "Schwerpunkt IT", "Freie Texte und kostenpflichtiges Pur"],
    ["Eine Meldung zu einem IT-Thema zu lesen", "Einen Test zu suchen"], True)
add("t3n", "https://www.t3n.de/", "t3n.de", "freemium", "proprietary", ["recherche"],
    "t3n schreibt über digitale Wirtschaft, Gründung und Werkzeuge.",
    "t3n veröffentlicht Meldungen und längere Stücke. Ein Teil ist frei, das Magazin und weitere Texte sind kostenpflichtig.",
    ["Digitale Wirtschaft und Gründung", "Meldungen und längere Texte", "Freier Anteil und kostenpflichtiges Magazin"],
    ["Einen Text zu einem Werkzeug zu lesen", "Meldungen zur digitalen Wirtschaft zu verfolgen"], True)
add("Utopia", "https://www.utopia.de/", "utopia.de", "free", "proprietary", ["recherche", "gesundheit"],
    "Utopia erklärt nachhaltigen Konsum, von Lebensmitteln bis zu Verträgen.",
    "Utopia veröffentlicht Ratgeber, die ohne Abo lesbar sind. Der Schwerpunkt liegt auf Alltagsentscheidungen.",
    ["Ratgeber zu nachhaltigem Konsum", "Alltagsthemen", "Lesen ohne Abo"],
    ["Einen Ratgeber zu einem Produkt zu lesen", "Alternativen im Alltag nachzuschlagen"], True)
add("test.de", "https://www.test.de/", "test.de", "freemium", "proprietary", ["recherche"],
    "test.de veröffentlicht die Tests der Stiftung Warentest.",
    "Die Seite zeigt Untersuchungsergebnisse zu Waren und Diensten. Kurzmeldungen sind oft frei, ausführliche Tests sind kostenpflichtig.",
    ["Tests der Stiftung Warentest", "Waren und Dienste", "Freie Meldungen und kostenpflichtige Tests"],
    ["Einen Test vor dem Kauf zu lesen", "Produkte einer Kategorie zu vergleichen"], True)
add("Computerbild", "https://www.computerbild.de/", "computerbild.de", "free", "proprietary", ["recherche"],
    "Computerbild testet Technik und schreibt Ratgeber für den Alltag.",
    "Die Seite veröffentlicht Tests, Meldungen und Anleitungen. Die Artikel sind ohne Abo lesbar.",
    ["Techniktests", "Anleitungen", "Lesen ohne Abo"],
    ["Einen Test zu einem Gerät zu lesen", "Eine Anleitung zu einem Programm zu suchen"], True)
add("mobile.de", "https://www.mobile.de/", "mobile.de", "free", "proprietary", ["recherche"],
    "mobile.de listet Gebraucht- und Neuwagen mit Preis und Daten.",
    "Die Suche filtert nach Modell, Preis und Ort. Ein Konto ist für die Suche nicht nötig, der Kauf liegt beim Anbieter.",
    ["Fahrzeuginserate", "Filter nach Preis und Ort", "Suche ohne Konto"],
    ["Ein Modell in einer Preisspanne zu suchen", "Angebote in der Nähe zu vergleichen"], True)
add("AutoScout24", "https://www.autoscout24.de/", "autoscout24.de", "free", "proprietary", ["recherche"],
    "AutoScout24 zeigt Fahrzeuge von Händlern und Privatleuten.",
    "Die Suche filtert Modell, Preis und Standort. Sie ist ohne Konto möglich, der Kauf liegt beim Inserenten.",
    ["Fahrzeugsuche", "Händler und Privat", "Suche ohne Konto"],
    ["Ein Gebrauchtwagenangebot zu finden", "Preise eines Modells zu vergleichen"], True)
add("Vinted", "https://www.vinted.de/", "vinted.de", "free", "proprietary", ["e-commerce"],
    "Vinted vermittelt gebrauchte Kleidung zwischen Privatleuten.",
    "Vinted zeigt Inserate und einen Chat zur Übergabe. Das Einstellen ist ohne Verkaufsprovision beschrieben, die die Seite so ausweist. Der Kaufpreis liegt beim Angebot.",
    ["Gebrauchte Kleidung", "Chat zur Übergabe", "Preis laut Inserat"],
    ["Ein Kleidungsstück gebraucht zu suchen", "Ein Teil selbst einzustellen"], True)
add("Thalia", "https://www.thalia.de/", "thalia.de", "free", "proprietary", ["bildung"],
    "Thalia verkauft Bücher, E-Books und Hörbücher.",
    "Thalia zeigt Titel mit Preis und Verfügbarkeit, auch zum Abholen in einer Filiale. Die Suche ist ohne Konto möglich, der Kauf ist kostenpflichtig.",
    ["Bücher, E-Books und Hörbücher", "Verfügbarkeit in Filialen", "Suche ohne Konto"],
    ["Einen Titel zu suchen", "Ein E-Book oder Hörbuch zu kaufen"], True)
add("Nextory", "https://www.nextory.de/", "nextory.de", "paid", "proprietary", ["bildung"],
    "Nextory verleiht E-Books und Hörbücher über ein Abo.",
    "Nextory stellt einen Katalog zum Lesen und Hören in der App bereit. Der Zugang ist kostenpflichtig.",
    ["E-Books und Hörbücher", "Katalog in der App", "Kostenpflichtiges Abo"],
    ["Ein Hörbuch im Abo zu hören", "Einen Roman in der App zu lesen"], True)
add("onvista", "https://www.onvista.de/", "onvista.de", "freemium", "proprietary", ["finanzen", "recherche"],
    "onvista zeigt Kurse, Nachrichten und Kennzahlen zu Wertpapieren.",
    "onvista stellt Aktien, Fonds und Indizes mit Kurs und Meldungen dar. Ein Teil ist ohne Abo lesbar, weitere Funktionen sind bezahlt.",
    ["Kurse und Kennzahlen", "Nachrichten zu Wertpapieren", "Freier Anteil und bezahlte Funktionen"],
    ["Einen Aktienkurs nachzuschlagen", "Kennzahlen eines Fonds zu lesen"], True)
add("Börse Frankfurt", "https://www.boerse-frankfurt.de/", "boerse-frankfurt.de", "free", "proprietary", ["finanzen", "recherche"],
    "Die Börse Frankfurt veröffentlicht Kurse und Indizes des Handelsplatzes.",
    "Die Seite zeigt Kurse, Indizes und Handelsdaten. Die Abfrage ist ohne Konto möglich.",
    ["Kurse und Indizes", "Handelsdaten", "Abfrage ohne Konto"],
    ["Einen Kurs an der Frankfurter Börse nachzuschlagen", "Einen Index zu verfolgen"], True)
add("Morningstar", "https://www.morningstar.de/", "morningstar.de", "freemium", "proprietary", ["finanzen", "recherche"],
    "Morningstar bewertet Fonds und zeigt Kennzahlen.",
    "Morningstar stellt Factsheets, Kosten und eine eigene Bewertung dar. Ein Teil ist ohne Abo lesbar, weitere Daten sind bezahlt.",
    ["Fondsdaten und Factsheets", "Eigene Bewertung", "Freier Anteil und bezahlte Daten"],
    ["Die Kosten eines Fonds nachzuschlagen", "Zwei Fonds gegenüberzustellen"], True)
add("Consorsbank", "https://www.consorsbank.de/", "consorsbank.de", "freemium", "proprietary", ["finanzen"],
    "Die Consorsbank führt Girokonto und Depot.",
    "Die Bank bietet Zahlungsverkehr und Wertpapierhandel. Konto und Depot haben Konditionen, die die Website nennt. Der Sitz ist in Deutschland.",
    ["Girokonto und Depot", "Wertpapierhandel", "Konditionen auf der Website"],
    ["Ein Depot bei einer deutschen Bank zu führen", "Eine Order zu setzen"], False)
add("flatex", "https://www.flatex.de/", "flatex.de", "freemium", "proprietary", ["finanzen"],
    "flatex führt ein Depot für Aktien, ETFs und andere Wertpapiere.",
    "flatex nimmt Orders entgegen und zeigt das Depot. Die Konditionen stehen auf der Website. Der Broker sitzt in Deutschland.",
    ["Depot und Orders", "Aktien und ETFs", "Konditionen auf der Website"],
    ["Ein Depot zu eröffnen", "Eine Order zu erfassen"], False)
add("DEGIRO", "https://www.degiro.de/", "degiro.de", "freemium", "proprietary", ["finanzen"],
    "DEGIRO führt ein Depot mit Handel in Aktien und ETFs.",
    "DEGIRO zeigt Kurse und nimmt Orders entgegen. Gebühren stehen auf der Website. Der Broker ist in Europa verfügbar.",
    ["Depot für Aktien und ETFs", "Orders", "Gebühren auf der Website"],
    ["Eine Aktie zu kaufen", "Die Gebühr einer Order nachzulesen"], False)
add("Smartbroker", "https://www.smartbroker.de/", "smartbroker.de", "freemium", "proprietary", ["finanzen"],
    "Smartbroker führt ein Depot für den Handel mit Wertpapieren.",
    "Smartbroker nimmt Orders entgegen und zeigt Bestände. Die Konditionen stehen auf der Website. Der Anbieter sitzt in Deutschland.",
    ["Depot und Orders", "Konditionen auf der Website", "Anbieter aus Deutschland"],
    ["Ein Depot in Deutschland zu führen", "Eine Order zu prüfen"], False)
add("quirion", "https://www.quirion.de/", "quirion.de", "paid", "proprietary", ["finanzen"],
    "quirion legt ein ETF-Depot an und verwaltet es nach einem Risikoprofil.",
    "quirion verteilt das Geld auf ETFs und passt die Mischung an. Der Dienst kommt aus Deutschland. Die Verwaltung ist kostenpflichtig.",
    ["ETF-Depot nach Risikoprofil", "Anpassung der Mischung", "Kostenpflichtige Verwaltung"],
    ["Ein verwaltetes ETF-Depot zu starten", "Ein Risikoprofil festzulegen"], True)
add("Oskar", "https://www.oskar.de/", "oskar.de", "paid", "proprietary", ["finanzen"],
    "Oskar bespart ein ETF-Portfolio in einer App.",
    "Oskar legt eine Mischung aus ETFs an und zieht eine Sparrate ein. Der Dienst kommt aus Deutschland. Die Nutzung ist kostenpflichtig.",
    ["ETF-Portfolio in der App", "Sparrate", "Kostenpflichtige Nutzung"],
    ["Einen Sparplan auf ein Portfolio zu starten", "Die Mischung in der App zu sehen"], True)
add("Whitebox", "https://www.whitebox.de/", "whitebox.de", "paid", "proprietary", ["finanzen"],
    "Whitebox verwaltet ein ETF-Portfolio nach Risikoneigung.",
    "Whitebox verteilt Einzahlungen auf ETFs und passt die Anteile an. Der Dienst kommt aus Deutschland. Die Verwaltung ist kostenpflichtig.",
    ["Verwaltetes ETF-Portfolio", "Anpassung der Anteile", "Kostenpflichtige Verwaltung"],
    ["Geld in ein verwaltetes Portfolio zu geben", "Die Zusammensetzung zu sehen"], True)
add("Ginmon", "https://www.ginmon.de/", "ginmon.de", "paid", "proprietary", ["finanzen"],
    "Ginmon legt ein ETF-Portfolio an und führt es.",
    "Ginmon verteilt das Vermögen auf ETFs und zeigt die Entwicklung. Der Dienst kommt aus Deutschland. Die Nutzung ist kostenpflichtig.",
    ["ETF-Portfolio", "Entwicklung in der App", "Kostenpflichtige Nutzung"],
    ["Ein Portfolio starten zu lassen", "Die Wertentwicklung zu verfolgen"], True)
add("Lynx", "https://www.lynxbroker.de/", "lynxbroker.de", "freemium", "proprietary", ["finanzen"],
    "Lynx vermittelt den Handel über Interactive Brokers.",
    "Lynx stellt die Oberfläche und den Support für ein Depot bei Interactive Brokers bereit. Konditionen stehen auf der Website. Der Anbieter sitzt in Deutschland.",
    ["Handel über Interactive Brokers", "Support auf Deutsch", "Konditionen auf der Website"],
    ["Ein Depot mit deutscher Betreuung zu führen", "Eine Order über die Plattform zu setzen"], False)
add("CapTrader", "https://www.captrader.com/", "captrader.com", "freemium", "proprietary", ["finanzen"],
    "CapTrader vermittelt den Handel über Interactive Brokers.",
    "CapTrader legt ein Depot an und nennt eigene Konditionen für den Handel. Der Anbieter sitzt in Düsseldorf.",
    ["Depot über Interactive Brokers", "Konditionen des Vermittlers", "Anbieter aus Düsseldorf"],
    ["Ein Depot mit Sitz in Deutschland zu eröffnen", "Die Konditionen vor einer Order zu lesen"], False)
add("Deutsche Rentenversicherung", "https://www.deutsche-rentenversicherung.de/", "deutsche-rentenversicherung.de", "free", "proprietary", ["finanzen", "recht"],
    "Die Deutsche Rentenversicherung erklärt Renten, Reha und Beiträge.",
    "Die Website beschreibt Leistungen und Anträge und verweist auf die Online-Dienste. Die Informationen sind ohne Konto lesbar. Ein Antrag kann ein Konto verlangen.",
    ["Renten, Reha und Beiträge", "Hinweise zu Anträgen", "Informationen ohne Konto"],
    ["Eine Rentenart nachzulesen", "Den Weg zu einem Antrag zu finden"], True)
add("Existenzgründungsportal", "https://www.existenzgruender.de/", "existenzgruender.de", "free", "proprietary", ["finanzen", "recherche"],
    "Das Existenzgründungsportal des BMWE erklärt Schritte in die Selbstständigkeit.",
    "Die Seite führt durch Planung, Finanzierung und Anmeldung. Die Texte sind ohne Konto lesbar.",
    ["Schritte in die Selbstständigkeit", "Finanzierung und Anmeldung", "Lesen ohne Konto"],
    ["Eine Gründung vorzubereiten", "Einen Hinweis zur Anmeldung zu lesen"], True)
add("Für-Gründer", "https://www.fuer-gruender.de/", "fuer-gruender.de", "free", "proprietary", ["finanzen", "recherche"],
    "Für-Gründer erklärt Businessplan, Rechtsform und Finanzierung.",
    "Die Seite veröffentlicht Ratgeber für Menschen, die ein Unternehmen starten. Die Texte sind ohne Abo lesbar.",
    ["Businessplan und Rechtsform", "Finanzierung", "Lesen ohne Abo"],
    ["Eine Rechtsform einzuordnen", "Einen Punkt für den Businessplan nachzulesen"], True)
add("Jimdo", "https://www.jimdo.com/", "jimdo.com", "freemium", "proprietary", ["design"],
    "Jimdo baut eine Website im Browser, auch für kleine Betriebe in Deutschland.",
    "Jimdo stellt Seiten aus Vorlagen zusammen und kann eine Domain mitliefern. Der Anbieter kommt aus Hamburg. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Website aus Vorlagen", "Domain optional", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine einfache Firmenwebsite zu starten", "Texte und Bilder ohne eigenen Server zu pflegen"], True)
add("goneo", "https://www.goneo.de/", "goneo.de", "paid", "proprietary", ["design"],
    "goneo vermietet Webspace, Domains und Mail.",
    "goneo legt Seiten und Postfächer an. Der Anbieter sitzt in Deutschland. Die Pakete sind kostenpflichtig.",
    ["Webspace, Domains und Mail", "Anbieter aus Deutschland", "Kostenpflichtige Pakete"],
    ["Eine kleine Website zu hosten", "Mail zur Domain einzurichten"], True)
add("webgo", "https://www.webgo.de/", "webgo.de", "paid", "proprietary", ["design"],
    "webgo vermietet Hosting, Domains und Server.",
    "webgo stellt Webspace und Mail bereit. Der Anbieter sitzt in Deutschland. Die Tarife sind kostenpflichtig.",
    ["Hosting und Domains", "Mail", "Kostenpflichtige Tarife"],
    ["Eine Website auf deutschem Webspace zu betreiben", "Einen Tarif nach Speicher zu wählen"], False)
add("DomainFactory", "https://www.df.eu/", "df.eu", "paid", "proprietary", ["design"],
    "DomainFactory vermietet Domains, Webspace und Mail.",
    "DomainFactory legt Domains und dazugehörige Postfächer an. Der Anbieter sitzt in Deutschland. Die Pakete sind kostenpflichtig.",
    ["Domains, Webspace und Mail", "Anbieter aus Deutschland", "Kostenpflichtige Pakete"],
    ["Eine Domain zu registrieren", "Webspace und Mail dazu zu buchen"], False)
add("plusserver", "https://www.plusserver.com/", "plusserver.com", "paid", "proprietary", ["programmierung"],
    "plusserver betreibt Cloud und Server in deutschen Rechenzentren.",
    "plusserver stellt virtuelle Maschinen und Managed Services bereit. Der Anbieter sitzt in Köln. Die Nutzung ist kostenpflichtig.",
    ["Cloud in deutschen Rechenzentren", "Managed Services", "Kostenpflichtige Nutzung"],
    ["Einen Server in Deutschland zu mieten", "Einen betriebenen Dienst statt einer eigenen Instanz zu nehmen"], False)
add("DigitalOcean", "https://www.digitalocean.com/", "digitalocean.com", "paid", "proprietary", ["programmierung"],
    "DigitalOcean vermietet virtuelle Server und Datenbanken.",
    "DigitalOcean startet eine Instanz oder eine verwaltete Datenbank und rechnet sie nach Tarif ab. Die Nutzung ist kostenpflichtig.",
    ["Virtuelle Server", "Verwaltete Datenbanken", "Abrechnung nach Tarif"],
    ["Einen kleinen Server zu starten", "Eine Datenbank ohne eigene Pflege zu mieten"], False)
add("Netlify", "https://www.netlify.com/", "netlify.com", "freemium", "proprietary", ["programmierung", "design"],
    "Netlify veröffentlicht Websites aus einem Repository.",
    "Netlify baut eine statische oder gerenderte Seite und hängt eine Domain daran. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Veröffentlichung aus einem Repository", "Eigene Domain", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Website bei jedem Push zu veröffentlichen", "Eine Vorschau einer Änderung zu sehen"], False)
add("Render", "https://www.render.com/", "render.com", "freemium", "proprietary", ["programmierung"],
    "Render startet Webdienste, Datenbanken und Hintergrundjobs.",
    "Render deployed aus einem Repository und hält die laufende Fassung. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Webdienste und Datenbanken", "Deploy aus einem Repository", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Webdienst ohne eigenen Server zu starten", "Eine Datenbank daneben zu legen"], False)
add("Vercel", "https://vercel.com/", "vercel.com", "freemium", "proprietary", ["programmierung"],
    "Vercel veröffentlicht Webanwendungen aus einem Repository.",
    "Vercel baut bei jedem Push eine Fassung und vergibt eine Vorschau-Adresse. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Deploy bei jedem Push", "Vorschau-Adressen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Webanwendung zu veröffentlichen", "Eine Änderung vor dem Merge anzusehen"], False)
add("Heroku", "https://www.heroku.com/", "heroku.com", "freemium", "proprietary", ["programmierung"],
    "Heroku startet Anwendungen und Add-ons, ohne einen eigenen Server zu verwalten.",
    "Heroku nimmt einen Deploy entgegen und betreibt den Prozess. Es gibt einen Einstieg und bezahlte Dynos.",
    ["Betrieb ohne eigenen Server", "Add-ons", "Einstieg und bezahlte Dynos"],
    ["Eine Anwendung zu deployen", "Eine Datenbank als Add-on anzuhängen"], False)
add("MongoDB", "https://www.mongodb.com/", "mongodb.com", "freemium", "unknown", ["daten", "programmierung"],
    "MongoDB speichert Dokumente und bietet dazu eine gehostete Fassung namens Atlas.",
    "MongoDB legt Daten als Dokumente ab. Die Server-Software lässt sich selbst betreiben, Atlas ist die Cloud. Eine einzelne OSI-Kennung wird hier nicht eingetragen, weil die Lizenz der Ausgabe nicht erneut gelesen wurde.",
    ["Dokumentenspeicher", "Selbstbetrieb und Atlas", "Lizenz nicht eingetragen"],
    ["Dokumente statt Tabellen zu speichern", "Eine Datenbank ohne eigenen Server zu starten"], False)
add("Datadog", "https://www.datadoghq.com/", "datadoghq.com", "freemium", "proprietary", ["programmierung"],
    "Datadog sammelt Kennzahlen, Logs und Traces einer Anwendung.",
    "Datadog zeigt Last, Fehler und Infrastruktur in einer Oberfläche. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Kennzahlen, Logs und Traces", "Eine Oberfläche", "Einstieg und bezahlte Kontingente"],
    ["Die Last eines Dienstes zu sehen", "Einen Fehler mit einem Trace zu verbinden"], False)
add("New Relic", "https://www.newrelic.com/", "newrelic.com", "freemium", "proprietary", ["programmierung"],
    "New Relic zeigt Leistung und Fehler einer Anwendung.",
    "New Relic sammelt Antwortzeiten, Fehler und Infrastrukturdaten. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Antwortzeiten und Fehler", "Infrastrukturdaten", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Eine langsame Stelle in einer Anwendung zu finden", "Fehler einer Version zu sehen"], False)
add("Dynatrace", "https://www.dynatrace.com/", "dynatrace.com", "paid", "proprietary", ["programmierung"],
    "Dynatrace überwacht Anwendungen und Infrastruktur und kommt aus Österreich.",
    "Dynatrace zeichnet Anfragen durch die Dienste und zeigt, wo Zeit verloren geht. Die Nutzung ist kostenpflichtig.",
    ["Überwachung von Anwendung und Infrastruktur", "Anbieter aus Österreich", "Kostenpflichtige Nutzung"],
    ["Einen langsamen Request zu verfolgen", "Die Abhängigkeiten eines Dienstes zu sehen"], False)
add("Amplitude", "https://www.amplitude.com/", "amplitude.com", "freemium", "proprietary", ["marketing", "programmierung"],
    "Amplitude zeigt, welche Schritte Menschen in einem Produkt gehen.",
    "Amplitude zählt Ereignisse und baut daraus Trichter und Verläufe. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Ereignisse und Trichter", "Verläufe im Produkt", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Zu sehen, wo ein Ablauf abbricht", "Zwei Versionen eines Trichters zu vergleichen"], False)
add("Mixpanel", "https://www.mixpanel.com/", "mixpanel.com", "freemium", "proprietary", ["marketing", "programmierung"],
    "Mixpanel wertet Ereignisse in einem Produkt aus.",
    "Mixpanel zeigt, welche Aktionen wie oft passieren und wo ein Trichter abreißt. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Ereignisse und Trichter", "Häufigkeiten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Funktion nach Nutzung zu messen", "Einen Trichter zu untersuchen"], False)
add("Twilio", "https://www.twilio.com/", "twilio.com", "paid", "proprietary", ["programmierung", "kundenservice"],
    "Twilio verschickt SMS, Anrufe und Nachrichten über eine Schnittstelle.",
    "Twilio stellt Nummern und APIs für SMS, Sprache und Chat bereit. Die Abrechnung folgt der Nutzung.",
    ["SMS, Anrufe und Chat", "Schnittstelle", "Abrechnung nach Nutzung"],
    ["Eine SMS aus einer Anwendung zu senden", "Einen Anruf über eine API auszulösen"], False)
add("Crisp", "https://crisp.chat/", "crisp.chat", "freemium", "proprietary", ["kundenservice"],
    "Crisp legt einen Chat auf die eigene Website und sammelt die Gespräche.",
    "Crisp zeigt ein Chatfenster und einen gemeinsamen Posteingang. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Chat auf der Website", "Gemeinsamer Posteingang", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Website-Chat einzubauen", "Gespräche im Team zu beantworten"], True)
add("Tawk", "https://www.tawk.to/", "tawk.to", "freemium", "proprietary", ["kundenservice"],
    "Tawk stellt einen Website-Chat bereit, die Grundfunktion ohne Monatspreis.",
    "Tawk blendet ein Chatfenster ein und sammelt die Gespräche. Die Basis ist ohne Monatsabo beschrieben, Zusatzangebote sind bezahlt.",
    ["Chatfenster", "Gemeinsamer Eingang", "Basis ohne Monatsabo und bezahlte Zusätze"],
    ["Einen Chat auf eine Seite zu setzen", "Anfragen live zu beantworten"], True)
add("Smartsupp", "https://www.smartsupp.com/", "smartsupp.com", "freemium", "proprietary", ["kundenservice"],
    "Smartsupp zeigt einen Chat und optional, was Besucher auf der Seite tun.",
    "Smartsupp legt ein Chatfenster auf die Website und kann Sitzungen aufzeichnen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Website-Chat", "Optionale Sitzungsaufzeichnung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Chat in einen Shop einzubauen", "Eine Anfrage live zu beantworten"], True)
add("Asterisk", "https://www.asterisk.org/", "asterisk.org", "free", "unknown", ["kundenservice", "programmierung"],
    "Asterisk ist eine Telefonanlage, die man auf dem eigenen Server betreibt.",
    "Asterisk schaltet Anrufe, Warteschleifen und Voicemail. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Anrufe und Warteschleifen", "Betrieb auf dem eigenen Server", "Nutzung ohne Pflichtabo"],
    ["Eine Telefonanlage selbst zu betreiben", "Eine Warteschleife einzurichten"], False)
add("FFmpeg", "https://ffmpeg.org/", "ffmpeg.org", "free", "unknown", ["videoschnitt", "audio-und-sprache"],
    "FFmpeg wandelt, schneidet und liest Video- und Audiodateien auf der Kommandozeile.",
    "FFmpeg liest sehr viele Formate und schreibt sie in andere um. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Umwandeln von Video und Audio", "Schnitt auf der Kommandozeile", "Nutzung ohne Pflichtabo"],
    ["Eine Datei in ein anderes Format zu wandeln", "Einen Abschnitt ohne große Oberfläche zu schneiden"], False)
add("Kling AI", "https://klingai.com/", "klingai.com", "freemium", "proprietary", ["videogenerierung"],
    "Kling erzeugt kurze Videos aus Text oder einem Bild.",
    "Kling nimmt eine Beschreibung oder ein Standbild und liefert einen Clip. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Video aus Text oder Bild", "Kurze Clips", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Einen kurzen Clip aus einer Beschreibung zu erzeugen", "Ein Standbild in Bewegung zu setzen"], False)
add("Luma AI", "https://www.luma.ai/", "luma.ai", "freemium", "proprietary", ["videogenerierung", "dreid"],
    "Luma erzeugt Videos aus Text und baut 3D-Szenen aus Aufnahmen.",
    "Luma Dream Machine macht Clips aus einer Beschreibung, weitere Werkzeuge setzen Fotos zu einer Szene zusammen. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Video aus Text", "3D aus Aufnahmen", "Einstieg und bezahlte Kontingente"],
    ["Einen kurzen Clip zu erzeugen", "Eine Szene aus Fotos zu setzen"], False)
add("Twitch", "https://www.twitch.tv/", "twitch.tv", "freemium", "proprietary", ["gaming", "social-media"],
    "Twitch überträgt Livestreams, vor allem von Spielen.",
    "Twitch zeigt Kanäle live und speichert Zuschnitte. Das Zuschauen ist ohne Abo möglich, ein Kanal kann frei senden, Zusatzangebote sind bezahlt.",
    ["Livestreams", "Kanäle und Zuschnitte", "Zuschauen ohne Abo"],
    ["Einen Stream zu sehen", "Einen eigenen Kanal zu starten"], True)
add("Vimeo", "https://vimeo.com/", "vimeo.com", "freemium", "proprietary", ["videoschnitt"],
    "Vimeo hostet Videos und spielt sie auf der eigenen Website ab.",
    "Vimeo nimmt Dateien entgegen, setzt Privatsphäre und liefert einen Player. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Video-Hosting und Player", "Privatsphäre je Video", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Video auf der eigenen Seite einzubetten", "Einen Film nur für eine Gruppe freizugeben"], True)
add("Riverside", "https://riverside.fm/", "riverside.fm", "freemium", "proprietary", ["audio-und-sprache", "videoschnitt"],
    "Riverside nimmt Gespräche in hoher Qualität auf, getrennt je Person.",
    "Riverside zeichnet Ton und Bild lokal bei jedem Gast auf und setzt sie danach zusammen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Getrennte Spuren je Gast", "Ton und Bild", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Gespräch für einen Podcast aufzunehmen", "Spuren getrennt zu behalten"], True)
add("Affinity", "https://affinity.serif.com/", "affinity.serif.com", "paid", "proprietary", ["design"],
    "Affinity bündelt Layout, Bildbearbeitung und Vektorgrafik.",
    "Affinity Publisher, Photo und Designer arbeiten mit Dokumenten, Fotos und Vektoren. Die Lizenzen sind kostenpflichtig, ein Abo nennt die Produktseite nicht als einzige Form.",
    ["Layout, Foto und Vektor", "Drei Anwendungen", "Kostenpflichtige Lizenzen"],
    ["Ein Layout zu setzen", "Ein Foto oder eine Vektorgrafik zu bearbeiten"], False)
add("Cubase", "https://www.steinberg.net/de/cubase/", "steinberg.net", "paid", "proprietary", ["musik"],
    "Cubase nimmt und mischt Musik auf mehreren Spuren.",
    "Cubase von Steinberg arrangiert Audio und MIDI. Der Hersteller sitzt in Hamburg. Die Lizenzen sind kostenpflichtig.",
    ["Mehrspur für Audio und MIDI", "Hersteller aus Hamburg", "Kostenpflichtige Lizenzen"],
    ["Einen Song auf mehreren Spuren aufzunehmen", "MIDI und Audio zu mischen"], False)
add("Native Instruments", "https://www.native-instruments.com/", "native-instruments.com", "freemium", "proprietary", ["musik"],
    "Native Instruments verkauft Instrumente, Effekte und die Plattform Komplete.",
    "Native Instruments stellt Klangerzeuger und Effekte bereit, die in einer DAW laufen. Ein Teil ist kostenlos, die Sammlungen sind kostenpflichtig. Der Sitz ist in Berlin.",
    ["Instrumente und Effekte", "Plattform Komplete", "Kostenlose Werkzeuge und kostenpflichtige Sammlungen"],
    ["Einen Klangerzeuger in eine Produktion zu laden", "Eine Sammlung von Instrumenten zu durchsuchen"], False)
add("digiKam", "https://www.digikam.org/", "digikam.org", "free", "unknown", ["design"],
    "digiKam sortiert Fotos auf dem eigenen Rechner und bearbeitet Metadaten.",
    "digiKam verschlagwortet Aufnahmen, zeigt sie auf einer Karte und kann sie entwickeln. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Verschlagwortung und Karte", "Entwicklung", "Nutzung ohne Pflichtabo"],
    ["Ein Fotoarchiv lokal zu ordnen", "Schlagwörter über viele Aufnahmen zu setzen"], False)
add("Ocenaudio", "https://www.ocenaudio.com/", "ocenaudio.com", "free", "proprietary", ["audio-und-sprache"],
    "Ocenaudio schneidet und zeigt Audiodateien.",
    "Ocenaudio öffnet Aufnahmen, setzt Schnittmarken und wendet einfache Effekte an. Die Anwendung ist ohne Abo erhältlich.",
    ["Schnitt und Effekte", "Wellenform", "Nutzung ohne Abo"],
    ["Eine Aufnahme zu kürzen", "Eine Stelle in der Wellenform zu finden"], True)
add("Yousician", "https://www.yousician.com/", "yousician.com", "freemium", "proprietary", ["bildung", "musik"],
    "Yousician übt Gitarre, Klavier, Bass und Gesang mit Rückmeldung.",
    "Yousician hört über das Mikrofon mit und zeigt, ob der Ton getroffen wurde. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Übungen für mehrere Instrumente", "Rückmeldung über das Mikrofon", "Kostenloser Einstieg und bezahltes Abo"],
    ["Ein Instrument mit sofortiger Rückmeldung zu üben", "Eine Lektion über Tage zu folgen"], True)
add("Simply Piano", "https://www.simplypiano.com/", "simplypiano.com", "freemium", "proprietary", ["bildung", "musik"],
    "Simply Piano übt Klavier mit Stücken, die dem Spiel folgen.",
    "Simply Piano zeigt Noten und hört mit, welche Tasten getroffen wurden. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Noten, die dem Spiel folgen", "Rückmeldung zu den Tasten", "Kostenloser Einstieg und bezahltes Abo"],
    ["Ein Klavierstück mit Rückmeldung zu üben", "Notenlesen neben dem Spielen zu lernen"], True)
add("Babylon.js", "https://www.babylonjs.com/", "babylonjs.com", "free", "unknown", ["dreid", "programmierung"],
    "Babylon.js zeichnet 3D-Szenen im Browser.",
    "Babylon.js stellt Kameras, Licht und Modelle in einer Website dar. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Bibliothek ist ohne Pflichtabo erhältlich.",
    ["3D im Browser", "Kameras, Licht und Modelle", "Nutzung ohne Pflichtabo"],
    ["Eine 3D-Szene in eine Website einzubauen", "Ein Beispiel im Playground zu ändern"], False)
add("PixiJS", "https://www.pixijs.com/", "pixijs.com", "free", "unknown", ["gaming", "programmierung"],
    "PixiJS zeichnet 2D-Grafik im Browser über WebGL.",
    "PixiJS setzt Bilder, Text und Filter in eine Bühne. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Bibliothek ist ohne Pflichtabo erhältlich.",
    ["2D im Browser", "Bilder, Text und Filter", "Nutzung ohne Pflichtabo"],
    ["Ein 2D-Spiel im Browser zu zeichnen", "Eine Bühne mit Filtern aufzubauen"], False)
add("RPG Maker", "https://www.rpgmakerweb.com/", "rpgmakerweb.com", "paid", "proprietary", ["gaming"],
    "RPG Maker baut Rollenspiele aus Karten, Ereignissen und Dialogen.",
    "RPG Maker setzt Karten und Ereignisse zusammen und exportiert das Spiel. Die Software ist kostenpflichtig.",
    ["Karten, Ereignisse und Dialoge", "Export des Spiels", "Kostenpflichtige Software"],
    ["Ein Rollenspiel ohne eigene Engine zu bauen", "Einen Dialog auf einer Karte zu setzen"], False)
add("Adventure Game Studio", "https://www.adventuregamestudio.co.uk/", "adventuregamestudio.co.uk", "free", "unknown", ["gaming"],
    "Adventure Game Studio baut Point-and-Click-Spiele.",
    "Die Umgebung setzt Räume, Figuren und Dialoge zusammen. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Räume, Figuren und Dialoge", "Point-and-Click", "Nutzung ohne Pflichtabo"],
    ["Ein Adventure zu prototypen", "Einen Dialog in einem Raum zu schreiben"], False)
add("PeerTube", "https://joinpeertube.org/", "joinpeertube.org", "free", "unknown", ["social-media", "videoschnitt"],
    "PeerTube hostet Videos im Verbund vieler Server statt auf einer zentralen Plattform.",
    "PeerTube spielt Videos und lässt einen eigenen Server an den Verbund hängen. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Video im Verbund vieler Server", "Eigener Server möglich", "Nutzung ohne Pflichtabo"],
    ["Ein Video auf einem eigenen Server zu veröffentlichen", "Einen Kanal im Verbund zu abonnieren"], False)
add("Owncast", "https://owncast.online/", "owncast.online", "free", "unknown", ["social-media"],
    "Owncast sendet einen Livestream vom eigenen Server.",
    "Owncast nimmt einen Stream entgegen und zeigt ihn auf einer eigenen Seite mit Chat. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Livestream auf dem eigenen Server", "Chat auf der Seite", "Nutzung ohne Pflichtabo"],
    ["Einen Stream selbst zu hosten", "Den Chat neben dem Bild zu führen"], False)
add("LiveKit", "https://livekit.io/", "livekit.io", "freemium", "unknown", ["programmierung"],
    "LiveKit baut Audio- und Videoräume, die sich in eine eigene Anwendung setzen lassen.",
    "LiveKit stellt Räume über eine Schnittstelle bereit und lässt sich selbst betreiben. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine Cloud mit Einstieg und bezahlten Stufen.",
    ["Audio- und Videoräume", "Schnittstelle und Selbstbetrieb", "Cloud mit Einstieg und bezahlten Stufen"],
    ["Einen Videoraum in eine Anwendung einzubauen", "Den Server selbst zu betreiben"], False)
add("Mux", "https://mux.com/", "mux.com", "paid", "proprietary", ["videoschnitt", "programmierung"],
    "Mux speichert Videos und liefert den Player über eine Schnittstelle.",
    "Mux nimmt Dateien oder Streams entgegen, kodiert sie und spielt sie aus. Die Abrechnung folgt der Nutzung.",
    ["Upload, Kodierung und Player", "Schnittstelle", "Abrechnung nach Nutzung"],
    ["Ein Video in eine Anwendung einzubinden", "Einen Livestream auszuliefern"], False)
add("Wings 3D", "https://www.wings3d.com/", "wings3d.com", "free", "unknown", ["dreid"],
    "Wings 3D modelliert Polygonnetze auf dem eigenen Rechner.",
    "Wings 3D zieht Kanten und Flächen zu einem Modell und exportiert es. Eine OSI-Kennung wird hier nicht eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Polygonmodellierung", "Export", "Nutzung ohne Pflichtabo"],
    ["Ein einfaches 3D-Modell zu bauen", "Ein Netz für ein anderes Programm zu exportieren"], False)
add("BlocksCAD", "https://www.blockscad3d.com/", "blockscad3d.com", "freemium", "proprietary", ["dreid", "bildung"],
    "BlocksCAD baut 3D-Modelle aus Blöcken, ähnlich wie eine visuelle Programmiersprache.",
    "BlocksCAD setzt Formen zusammen und kann den Körper für den Druck exportieren. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["3D aus Blöcken", "Export für den Druck", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Modell ohne Freiform-Modellierung zu bauen", "Einen Körper für den Druck vorzubereiten"], True)
add("Topaz Labs", "https://www.topazlabs.com/", "topazlabs.com", "paid", "proprietary", ["design", "videoschnitt"],
    "Topaz Labs schärft, entrauscht und vergrößert Foto und Video.",
    "Topaz bietet getrennte Werkzeuge für Standbilder und für Videomaterial. Die Lizenzen sind kostenpflichtig.",
    ["Schärfen, Entrauschen und Vergrößern", "Foto und Video", "Kostenpflichtige Lizenzen"],
    ["Ein Foto zu vergrößern", "Rauschen aus einer Aufnahme zu nehmen"], False)
add("Zencastr", "https://www.zencastr.com/", "zencastr.com", "freemium", "proprietary", ["audio-und-sprache"],
    "Zencastr nimmt Podcast-Gespräche in getrennten Spuren auf.",
    "Zencastr zeichnet jeden Gast einzeln auf, damit der Schnitt die Stimmen getrennt hält. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Getrennte Spuren je Gast", "Aufnahme im Browser", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Gespräch mit getrennten Spuren aufzunehmen", "Gäste ohne gemeinsames Studio zu verbinden"], True)
add("SquadCast", "https://www.squadcast.fm/", "squadcast.fm", "freemium", "proprietary", ["audio-und-sprache"],
    "SquadCast nimmt Interviews in hoher Qualität und getrennten Spuren auf.",
    "SquadCast verbindet Gäste im Browser und speichert die Spuren getrennt. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Getrennte Spuren", "Aufnahme im Browser", "Einstieg und bezahlte Stufen"],
    ["Ein Interview ohne Studio aufzunehmen", "Stimmen getrennt in den Schnitt zu geben"], False)
add("Cleanfeed", "https://cleanfeed.net/", "cleanfeed.net", "freemium", "proprietary", ["audio-und-sprache"],
    "Cleanfeed überträgt Studio-Audio zwischen zwei Browsern.",
    "Cleanfeed schickt Ton in hoher Qualität an eine Gegenstelle, ohne eine extra App. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Audio zwischen Browsern", "Hohe Qualität", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Gast in hoher Tonqualität dazuzuschalten", "Eine Aufnahmeleitung ohne extra Software zu öffnen"], False)
add("Wistia", "https://www.wistia.com/", "wistia.com", "freemium", "proprietary", ["videoschnitt", "marketing"],
    "Wistia hostet Videos für Unternehmen und zeigt, wer sie sieht.",
    "Wistia spielt Videos auf der eigenen Seite und zählt Aufrufe und Stellen, an denen Menschen aussteigen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Video-Hosting", "Aufrufe und Absprünge", "Einstieg und bezahlte Stufen"],
    ["Ein Erklärvideo auf der eigenen Seite zu hosten", "Zu sehen, an welcher Stelle Zuschauende aussteigen"], False)
add("Dailymotion", "https://www.dailymotion.com/", "dailymotion.com", "freemium", "proprietary", ["social-media", "videoschnitt"],
    "Dailymotion spielt Videos und lässt eigene Kanäle anlegen.",
    "Dailymotion zeigt Filme und Kanäle im Browser. Das Ansehen ist ohne Abo möglich, ein Kanal kann frei bespielt werden.",
    ["Videokanäle", "Wiedergabe im Browser", "Ansehen ohne Abo"],
    ["Ein Video zu veröffentlichen", "Einen Kanal zu abonnieren"], True)
add("Kick", "https://kick.com/", "kick.com", "freemium", "proprietary", ["gaming", "social-media"],
    "Kick überträgt Livestreams, vor allem von Spielen.",
    "Kick zeigt Kanäle live. Das Zuschauen ist ohne Abo möglich. Wer sendet, nutzt die Konditionen, die die Seite nennt.",
    ["Livestreams", "Kanäle", "Zuschauen ohne Abo"],
    ["Einen Stream zu sehen", "Einen Kanal zu öffnen"], True)
add("Restream", "https://www.restream.io/", "restream.io", "freemium", "proprietary", ["social-media"],
    "Restream sendet einen Livestream gleichzeitig an mehrere Plattformen.",
    "Restream nimmt ein Signal entgegen und verteilt es. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Ein Signal, mehrere Plattformen", "Verteilung eines Streams", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Denselben Stream an zwei Plattformen zu senden", "Einen Gast-Stream weiterzuleiten"], False)
add("GOG", "https://www.gog.com/", "gog.com", "free", "proprietary", ["gaming"],
    "GOG verkauft Spiele ohne Kopierschutz und pflegt ältere Titel.",
    "GOG listet Spiele mit Preis und einer Fassung, die sich ohne zusätzliche Plattform-Pflicht starten lässt. Die Suche ist ohne Konto möglich, der Kauf ist kostenpflichtig.",
    ["Spiele ohne Kopierschutz", "Ältere Titel", "Suche ohne Konto"],
    ["Ein Spiel ohne zusätzlichen Launcher zu kaufen", "Einen älteren Titel zu finden"], True)
add("Minecraft", "https://www.minecraft.net/", "minecraft.net", "paid", "proprietary", ["gaming"],
    "Minecraft setzt Welten aus Blöcken, die man abbaut und neu setzt.",
    "Minecraft gibt es als Java- und als Bedrock-Fassung. Die Welten sind kostenpflichtig, die Website nennt die aktuelle Edition.",
    ["Welten aus Blöcken", "Java- und Bedrock-Fassung", "Kostenpflichtige Edition"],
    ["Eine Welt zu bauen", "Mit anderen auf einem Server zu spielen"], True)
add("Roblox", "https://www.roblox.com/", "roblox.com", "freemium", "proprietary", ["gaming"],
    "Roblox spielt und veröffentlicht Spiele, die andere auf der Plattform gebaut haben.",
    "Roblox startet einzelne Erlebnisse im Client und stellt mit Roblox Studio einen Editor bereit. Das Spielen ist ohne Kauf möglich, Gegenstände und der Editor haben eigene Bedingungen.",
    ["Spiele anderer auf einer Plattform", "Editor Roblox Studio", "Spielen ohne Kauf"],
    ["Ein Spiel auf der Plattform zu starten", "Ein eigenes Erlebnis im Studio zu bauen"], True)


def validate(entries):
    skip = {
        "Greenhouse", "BambooHR", "Kayak", "Booking.com", "Crisp", "PeerTube",
        "Bab.la", "WordReference", "Geizhals", "mobile.de", "Vinted", "Thalia", "Asterisk",
    }
    entries[:] = [e for e in entries if e["name"] not in skip]
    db = sqlite3.connect(ROOT / "data" / "linkjagd.db")
    domains = {row[0] for row in db.execute("select domain from tools")}
    slugs = {row[0] for row in db.execute("select slug from tools")}
    seen_d, seen_s = set(), set()
    errors = []
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
        if "zzgl" in (entry["shortDescriptionDe"] + entry["longDescriptionDe"]).lower():
            errors.append(f"ust {entry['name']}")
    if errors:
        raise SystemExit("\n".join(errors[:40]))
    return entries


if __name__ == "__main__":
    rows = validate(E)
    out = ROOT / "data" / "verified-tools-batch7.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows), "->", out)
