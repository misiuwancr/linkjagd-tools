#!/usr/bin/env python3
"""Neunzehnte Liste: Automatisierung, Lernen und Seitenbau."""

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


add("Voiceflow", "https://www.voiceflow.com/", "voiceflow.com", "freemium", "proprietary", ["automatisierung", "ki-chatbots"],
    "Voiceflow baut Gesprächsabläufe für Chat und Sprache.",
    "Voiceflow setzt Schritte visuell und bindet ein Modell an. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Gesprächsabläufe", "Chat und Sprache", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Support-Chat zu bauen", "Einen Ablauf ohne Code zu setzen"], False)
add("Botpress", "https://www.botpress.com/", "botpress.com", "freemium", "proprietary", ["ki-chatbots", "automatisierung"],
    "Botpress baut Chatbots und stellt sie auf eine Website.",
    "Botpress legt Wissen und Abläufe an. Es gibt einen kostenlosen Einstieg und bezahlte Nachrichten.",
    ["Chatbots", "Wissen und Abläufe", "Kostenloser Einstieg und bezahlte Nachrichten"],
    ["Einen Bot auf die eigene Seite zu setzen", "Antworten aus eigenen Texten zu holen"], False)
add("Landbot", "https://www.landbot.io/", "landbot.io", "freemium", "proprietary", ["ki-chatbots", "marketing"],
    "Landbot macht aus einem Flussdiagramm einen Chat auf der Website.",
    "Landbot verbindet Fragen und leitet zu einer Person. Es gibt einen kostenlosen Einstieg und bezahlte Chats.",
    ["Chat aus einem Diagramm", "Weiterleitung", "Kostenloser Einstieg und bezahlte Chats"],
    ["Eine Anmeldung als Chat zu bauen", "Besucher an das Team zu geben"], True)
add("Chatfuel", "https://www.chatfuel.com/", "chatfuel.com", "freemium", "proprietary", ["ki-chatbots", "marketing"],
    "Chatfuel baut Chats für WhatsApp und andere Messenger.",
    "Chatfuel legt Antworten und Sequenzen an. Es gibt einen kostenlosen Einstieg und bezahlte Kontakte.",
    ["Chats für Messenger", "Sequenzen", "Kostenloser Einstieg und bezahlte Kontakte"],
    ["Einen WhatsApp-Ablauf zu starten", "Eine Sequenz an Kontakte zu schicken"], False)
add("Relay.app", "https://www.relay.app/", "relay.app", "freemium", "proprietary", ["automatisierung"],
    "Relay verbindet Dienste und lässt einen Assistenten Schritte prüfen.",
    "Relay startet einen Ablauf nach einem Ereignis. Es gibt einen kostenlosen Einstieg und bezahlte Schritte.",
    ["Abläufe zwischen Diensten", "Prüfung durch einen Menschen", "Kostenloser Einstieg und bezahlte Schritte"],
    ["Eine Mail in eine Aufgabe zu verwandeln", "Einen Schritt vor dem Senden zu prüfen"], False)
add("Axiom.ai", "https://www.axiom.ai/", "axiom.ai", "freemium", "proprietary", ["automatisierung"],
    "Axiom klickt Webseiten nach einem aufgenommenen Ablauf ab.",
    "Axiom zeichnet Klicks auf und wiederholt sie. Es gibt einen kostenlosen Einstieg und bezahlte Läufe.",
    ["Aufgezeichnete Klicks", "Wiederholung", "Kostenloser Einstieg und bezahlte Läufe"],
    ["Eine wiederkehrende Klickfolge aufzunehmen", "Einen Ablauf ohne API zu wiederholen"], False)
add("Browse AI", "https://www.browse.ai/", "browse.ai", "freemium", "proprietary", ["automatisierung"],
    "Browse AI liest Daten von Webseiten nach einem einmal gezeigten Muster.",
    "Browse AI überwacht eine Seite und liefert Zeilen. Es gibt einen kostenlosen Einstieg und bezahlte Läufe.",
    ["Daten von Seiten", "Überwachung", "Kostenloser Einstieg und bezahlte Läufe"],
    ["Eine Liste von einer Seite zu ziehen", "Eine Änderung auf einer Seite zu bemerken"], False)
add("PhantomBuster", "https://www.phantombuster.com/", "phantombuster.com", "freemium", "proprietary", ["automatisierung", "marketing"],
    "PhantomBuster zieht Daten aus dem Web und startet kleine Abläufe.",
    "PhantomBuster führt fertige Bausteine auf Seiten aus. Es gibt einen Einstieg und bezahlte Stunden.",
    ["Daten aus dem Web", "Fertige Bausteine", "Einstieg und bezahlte Stunden"],
    ["Eine Liste aus einer Seite zu exportieren", "Einen kleinen Ablauf täglich laufen zu lassen"], False)
add("Workato", "https://www.workato.com/", "workato.com", "paid", "proprietary", ["automatisierung"],
    "Workato verbindet Unternehmenssoftware über fertige Abläufe.",
    "Workato startet Schritte zwischen Systemen. Die Nutzung ist kostenpflichtig.",
    ["Abläufe zwischen Systemen", "Fertige Verbindungen", "Kostenpflichtige Nutzung"],
    ["Zwei Systeme ohne eigenen Code zu verbinden", "Einen Ablauf im Team zu betreiben"], False)
add("Tray.io", "https://tray.io/", "tray.io", "paid", "proprietary", ["automatisierung"],
    "Tray verbindet Dienste in grafischen Abläufen.",
    "Tray setzt Schritte zwischen APIs. Die Nutzung ist kostenpflichtig.",
    ["Grafische Abläufe", "Schritte zwischen APIs", "Kostenpflichtige Nutzung"],
    ["Einen Ablauf zwischen zwei Diensten zu bauen", "Einen Fehler im Schritt zu sehen"], False)
add("Systeme.io", "https://www.systeme.io/", "systeme.io", "freemium", "proprietary", ["marketing"],
    "Systeme.io bündelt Seiten, E-Mails und einen einfachen Shop.",
    "Systeme.io legt eine Strecke aus Seite und Mail an. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Seiten und E-Mails", "Einfacher Shop", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Anmeldeseite mit Mailfolge zu bauen", "Ein digitales Produkt anzubieten"], True)
add("Kajabi", "https://www.kajabi.com/", "kajabi.com", "paid", "proprietary", ["bildung", "marketing"],
    "Kajabi verkauft Kurse, Mitgliedschaften und E-Mails an einem Ort.",
    "Kajabi legt Lektionen und eine Kasse an. Die Nutzung ist kostenpflichtig.",
    ["Kurse und Mitgliedschaften", "E-Mails", "Kostenpflichtige Nutzung"],
    ["Einen Kurs online zu verkaufen", "Eine Mail an die Teilnehmenden zu schicken"], False)
add("Teachable", "https://www.teachable.com/", "teachable.com", "freemium", "proprietary", ["bildung"],
    "Teachable veröffentlicht Kurse und nimmt die Zahlung dafür an.",
    "Teachable legt Lektionen und eine Verkaufsseite an. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Kurse", "Zahlung", "Einstieg und bezahlte Stufen"],
    ["Einen Kurs mit Videos zu veröffentlichen", "Eine Lektion freizuschalten"], True)
add("Podia", "https://www.podia.com/", "podia.com", "freemium", "proprietary", ["bildung", "e-commerce"],
    "Podia verkauft Kurse, Downloads und Newsletter.",
    "Podia legt ein Produkt an und verschickt es an Käufer. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Kurse und Downloads", "Newsletter", "Einstieg und bezahlte Stufen"],
    ["Ein digitales Produkt zu verkaufen", "Einen Newsletter an Käufer zu schicken"], True)
add("ClickFunnels", "https://www.clickfunnels.com/", "clickfunnels.com", "paid", "proprietary", ["marketing"],
    "ClickFunnels baut Verkaufsstrecken aus Seiten, die aufeinander folgen.",
    "ClickFunnels setzt eine Seite nach der anderen bis zur Kasse. Die Nutzung ist kostenpflichtig.",
    ["Verkaufsstrecken", "Seitenfolge", "Kostenpflichtige Nutzung"],
    ["Eine Anmeldeseite mit der nächsten Seite zu verbinden", "Eine Kasse an die Strecke zu hängen"], False)
add("Unbounce", "https://www.unbounce.com/", "unbounce.com", "paid", "proprietary", ["marketing", "design"],
    "Unbounce baut Landingpages und testet zwei Fassungen gegeneinander.",
    "Unbounce veröffentlicht eine Seite und verteilt den Traffic. Die Nutzung ist kostenpflichtig.",
    ["Landingpages", "Zwei Fassungen", "Kostenpflichtige Nutzung"],
    ["Eine Seite für eine Anzeige zu bauen", "Zwei Überschriften zu vergleichen"], False)
add("Leadpages", "https://www.leadpages.com/", "leadpages.com", "paid", "proprietary", ["marketing", "design"],
    "Leadpages setzt Anmeldeseiten und hängt sie an eine Liste.",
    "Leadpages veröffentlicht eine Seite und sammelt Adressen. Die Nutzung ist kostenpflichtig.",
    ["Anmeldeseiten", "Liste", "Kostenpflichtige Nutzung"],
    ["Eine Seite für eine Anmeldung zu bauen", "Adressen an eine Liste zu geben"], False)
add("Instapage", "https://www.instapage.com/", "instapage.com", "paid", "proprietary", ["marketing", "design"],
    "Instapage baut Landingpages und zeigt, welche Fassung besser ankommt.",
    "Instapage setzt Seiten für Anzeigen und vergleicht sie. Die Nutzung ist kostenpflichtig.",
    ["Landingpages", "Vergleich von Fassungen", "Kostenpflichtige Nutzung"],
    ["Eine Seite zu einer Kampagne zu bauen", "Zwei Varianten zu messen"], False)
add("VWO", "https://www.vwo.com/", "vwo.com", "freemium", "proprietary", ["marketing"],
    "VWO testet zwei Fassungen einer Seite und zeichnet Sitzungen auf.",
    "VWO verteilt Besucher auf Varianten. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Tests von Seitenvarianten", "Sitzungen", "Einstieg und bezahlte Stufen"],
    ["Eine Überschrift gegen eine andere zu testen", "Zu sehen, wo Leute abspringen"], False)
add("Optimizely", "https://www.optimizely.com/", "optimizely.com", "paid", "proprietary", ["marketing"],
    "Optimizely testet Inhalte und Funktionen auf einer Website.",
    "Optimizely schaltet Varianten für einen Teil der Besucher frei. Die Nutzung ist kostenpflichtig.",
    ["Tests von Inhalten", "Varianten", "Kostenpflichtige Nutzung"],
    ["Eine Funktion nur für einen Teil zu zeigen", "Zwei Fassungen zu vergleichen"], False)
add("Kameleoon", "https://www.kameleoon.com/", "kameleoon.com", "paid", "proprietary", ["marketing"],
    "Kameleoon testet Seitenvarianten und personalisiert Inhalte.",
    "Kameleoon zeigt verschiedenen Gruppen verschiedene Fassungen. Die Nutzung ist kostenpflichtig.",
    ["Seitenvarianten", "Personalisierung", "Kostenpflichtige Nutzung"],
    ["Eine Variante nur einer Gruppe zu zeigen", "Einen Test auszuwerten"], False)
add("Crazy Egg", "https://www.crazyegg.com/", "crazyegg.com", "paid", "proprietary", ["marketing"],
    "Crazy Egg zeigt, wo auf einer Seite geklickt wird.",
    "Crazy Egg legt eine Heatmap über die Seite. Die Nutzung ist kostenpflichtig.",
    ["Heatmap", "Klicks", "Kostenpflichtige Nutzung"],
    ["Zu sehen, welche Stelle niemand klickt", "Eine Seite nach den Klicks zu ändern"], False)
add("Smartlook", "https://www.smartlook.com/", "smartlook.com", "freemium", "proprietary", ["marketing"],
    "Smartlook zeichnet Sitzungen auf und zeigt Heatmaps.",
    "Smartlook spielt einen Besuch nach. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Sitzungsaufzeichnung", "Heatmaps", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Besuch nachzusehen", "Zu sehen, wo eine Seite hakt"], False)
add("Lucky Orange", "https://www.luckyorange.com/", "luckyorange.com", "freemium", "proprietary", ["marketing"],
    "Lucky Orange zeichnet Besuche auf und bietet einen Chat dazu.",
    "Lucky Orange zeigt Heatmaps und einzelne Sitzungen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Sitzungen und Heatmaps", "Chat", "Einstieg und bezahlte Stufen"],
    ["Einen Besuch mit Abbruch nachzusehen", "Eine Frage im Chat zu beantworten"], False)
add("Maze UX", "https://www.maze.co/", "maze.co", "freemium", "proprietary", ["design"],
    "Maze lässt Menschen einen Prototyp durchklicken und sammelt die Wege.",
    "Maze misst, wo jemand hängen bleibt. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Tests von Prototypen", "Wege der Tester", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Prototyp testen zu lassen", "Zu sehen, welche Aufgabe scheitert"], False)
add("Useberry", "https://www.useberry.com/", "useberry.com", "freemium", "proprietary", ["design"],
    "Useberry testet Prototypen und zeigt, wohin geklickt wurde.",
    "Useberry sammelt Aufgaben und Klickpfade. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Prototyp-Tests", "Klickpfade", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Entwurf vor dem Bau zu testen", "Klickpfade zu vergleichen"], False)
add("Optimal Workshop", "https://www.optimalworkshop.com/", "optimalworkshop.com", "freemium", "proprietary", ["design"],
    "Optimal Workshop testet, wie Leute Informationen sortieren und suchen.",
    "Optimal Workshop legt Kartensortierungen und Baumtests an. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Kartensortierung", "Baumtests", "Einstieg und bezahlte Stufen"],
    ["Eine Navigation testen zu lassen", "Zu sehen, wie Begriffe sortiert werden"], False)
add("UserTesting", "https://www.usertesting.com/", "usertesting.com", "paid", "proprietary", ["design"],
    "UserTesting zeichnet auf, wie Menschen eine Website laut bedienen.",
    "UserTesting liefert Videos von echten Aufgaben. Die Nutzung ist kostenpflichtig.",
    ["Videos von Tests", "Aufgaben", "Kostenpflichtige Nutzung"],
    ["Zu hören, wo jemand auf einer Seite stockt", "Eine Aufgabe an Testpersonen zu geben"], False)
add("Zeplin", "https://www.zeplin.io/", "zeplin.io", "freemium", "proprietary", ["design"],
    "Zeplin übergibt Designs mit Maßen und Farben an die Entwicklung.",
    "Zeplin zeigt Abstände und Farben aus der Datei. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Maße und Farben", "Übergabe an die Entwicklung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Abstand aus dem Design abzulesen", "Eine Farbe an die Entwicklung zu geben"], False)
add("ProtoPie", "https://www.protopie.io/", "protopie.io", "freemium", "proprietary", ["design"],
    "ProtoPie macht aus Designs einen klickbaren Prototyp mit Sensoren.",
    "ProtoPie verbindet Screens und Reaktionen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Klickbare Prototypen", "Sensoren", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Ablauf zum Durchklicken zu bauen", "Eine Interaktion ohne Code zu zeigen"], False)
add("InVision", "https://www.invisionapp.com/", "invisionapp.com", "freemium", "proprietary", ["design"],
    "InVision macht aus Bildschirmen einen klickbaren Prototyp.",
    "InVision verbindet Screens und sammelt Kommentare. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Klickbare Prototypen", "Kommentare", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Ablauf zu zeigen", "Kommentare auf einem Screen zu sammeln"], True)
add("Principle", "https://principleformac.com/", "principleformac.com", "paid", "proprietary", ["design"],
    "Principle animiert Übergänge zwischen App-Screens auf dem Mac.",
    "Principle verbindet Zeichenflächen mit Bewegungen. Die App ist kostenpflichtig.",
    ["Animierte Übergänge", "Screens", "Kostenpflichtige App"],
    ["Einen Übergang zwischen zwei Screens zu zeigen", "Eine Bewegung zeitlich zu setzen"], False)
add("Copper", "https://www.copper.com/", "copper.com", "paid", "proprietary", ["marketing"],
    "Copper führt Kontakte und Deals direkt in Google Workspace.",
    "Copper hängt das CRM an Gmail und den Kalender. Die Nutzung ist kostenpflichtig.",
    ["CRM in Google Workspace", "Deals", "Kostenpflichtige Nutzung"],
    ["Einen Deal neben der Mail zu sehen", "Kontakte aus Gmail zu übernehmen"], False)
add("Streak", "https://www.streak.com/", "streak.com", "freemium", "proprietary", ["marketing"],
    "Streak legt eine Pipeline in den Gmail-Posteingang.",
    "Streak macht aus Mails Phasen eines Vorgangs. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Pipeline in Gmail", "Phasen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Bewerbungen im Posteingang zu führen", "Eine Mail einer Phase zuzuordnen"], True)
add("Affinity CRM", "https://www.affinity.co/", "affinity.co", "paid", "proprietary", ["marketing"],
    "Affinity führt Beziehungen und zeigt, wer wen im Netzwerk kennt.",
    "Affinity liest Mailkontakte und baut daraus ein Beziehungsnetz. Die Nutzung ist kostenpflichtig.",
    ["Beziehungsnetz", "Mailkontakte", "Kostenpflichtige Nutzung"],
    ["Zu sehen, wer einen Kontakt kennt", "Eine Beziehung über die Zeit zu führen"], False)
add("Zoho", "https://www.zoho.com/", "zoho.com", "freemium", "proprietary", ["produktivitaet"],
    "Zoho bündelt CRM, Mail, Projekte und weitere Büro-Apps.",
    "Zoho bietet einzelne Apps mit eigenem Einstieg. Viele haben einen kostenlosen Einstieg und bezahlte Stufen.",
    ["CRM, Mail, Projekte", "Einzelne Apps", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein CRM ohne ein zweites System zu starten", "Mail und Kontakte zu verbinden"], False)
add("Busuu", "https://www.busuu.com/", "busuu.com", "freemium", "proprietary", ["bildung"],
    "Busuu übt Sprachen mit Lektionen und Rückmeldung von anderen Lernenden.",
    "Busuu legt kurze Einheiten und Wiederholungen an. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Sprachlektionen", "Rückmeldung", "Kostenloser Einstieg und bezahltes Abo"],
    ["Täglich eine kurze Lektion zu machen", "Einen Text korrigieren zu lassen"], True)
add("Memrise", "https://www.memrise.com/", "memrise.com", "freemium", "proprietary", ["bildung"],
    "Memrise übt Vokabeln mit kurzen Wiederholungen und Videos.",
    "Memrise zeigt Karten und merkt sich, was noch unsicher ist. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Vokabeln", "Wiederholung", "Kostenloser Einstieg und bezahltes Abo"],
    ["Wörter über Tage zu wiederholen", "Eine kurze Einheit unterwegs zu machen"], True)
add("Cambly", "https://www.cambly.com/", "cambly.com", "paid", "proprietary", ["bildung"],
    "Cambly verbindet mit Lehrkräften für Gespräche auf Englisch per Video.",
    "Cambly bucht eine Unterrichtsstunde im Video. Die Stunden sind kostenpflichtig.",
    ["Video-Unterricht", "Englisch", "Kostenpflichtige Stunden"],
    ["Ein Gespräch auf Englisch zu üben", "Eine Stunde zu buchen"], True)
add("Weebly", "https://www.weebly.com/", "weebly.com", "freemium", "proprietary", ["design"],
    "Weebly baut Websites und einen kleinen Shop im Browser.",
    "Weebly setzt Seiten per Drag-and-drop. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Websites", "Kleiner Shop", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine einfache Seite zu veröffentlichen", "Einen kleinen Shop dazuzusetzen"], True)
add("Sellfy", "https://www.sellfy.com/", "sellfy.com", "freemium", "proprietary", ["e-commerce"],
    "Sellfy verkauft Downloads und Abos und liefert die Datei nach der Zahlung.",
    "Sellfy legt ein digitales Produkt an und schickt den Link. Es gibt einen Einstieg und Gebühren je Verkauf.",
    ["Downloads und Abos", "Lieferung nach Zahlung", "Einstieg und Gebühren je Verkauf"],
    ["Eine Datei direkt zu verkaufen", "Ein Abo für Inhalte anzubieten"], True)
add("Google Übersetzer", "https://translate.google.com/", "translate.google.com", "free", "proprietary", ["textgenerierung"],
    "Google Übersetzer überträgt Texte und kurze Gespräche zwischen Sprachen.",
    "Der Übersetzer nimmt Text, Sprache oder ein Bild. Die Nutzung im Browser ist ohne Abo möglich.",
    ["Text- und Bildübersetzung", "Mehrere Sprachen", "Nutzung ohne Abo"],
    ["Einen Absatz zu übersetzen", "Ein Gespräch live übertragen zu lassen"], True)
add("Cursor", "https://www.cursor.com/", "cursor.com", "freemium", "proprietary", ["programmierung"],
    "Cursor ist ein Editor, der Code vorschlägt und Aufgaben im Projekt übernimmt.",
    "Cursor schreibt beim Tippen mit und kann Änderungen über Dateien vorschlagen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Editor mit Vorschlägen", "Aufgaben im Projekt", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Funktion beim Tippen ergänzen zu lassen", "Eine Änderung über mehrere Dateien vorzuschlagen"], False)


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
    out = ROOT / "data" / "verified-tools-batch19.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows))
