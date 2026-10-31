#!/usr/bin/env python3
"""Vierzehnte Liste: bekannte KI- und Alltags-Tools."""

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


add("DeepSeek Chat", "https://chat.deepseek.com/", "chat.deepseek.com", "freemium", "proprietary", ["ki-chatbots"],
    "DeepSeek beantwortet Fragen im Chat und schreibt Code.",
    "Der Chat von DeepSeek nimmt Anweisungen auf Deutsch und Englisch entgegen. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Chat für Fragen und Code", "Kostenloser Einstieg", "Bezahlte Kontingente"],
    ["Eine Frage im Chat zu stellen", "Einen Codeschnipsel erklären zu lassen"], True)
add("Kimi", "https://www.moonshot.cn/", "moonshot.cn", "freemium", "proprietary", ["ki-chatbots"],
    "Kimi ist der Chat von Moonshot und liest auch lange Dokumente.",
    "Über moonshot.cn startet der Assistent Kimi. Er beantwortet Fragen und kann längere Texte verarbeiten. Es gibt einen kostenlosen Einstieg.",
    ["Chat mit langen Dokumenten", "Kostenloser Einstieg", "Anbieter Moonshot"],
    ["Ein langes Dokument befragen zu lassen", "Eine Frage im Chat zu stellen"], True)
add("ChatGLM", "https://chatglm.cn/", "chatglm.cn", "freemium", "proprietary", ["ki-chatbots"],
    "ChatGLM ist der Chat von Zhipu und beantwortet Fragen im Browser.",
    "ChatGLM führt ein Gespräch und kann Texte zusammenfassen. Es gibt einen kostenlosen Einstieg und weitere Modelle in bezahlten Stufen.",
    ["Chat im Browser", "Zusammenfassen von Texten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Frage zu stellen", "Einen Text zusammenfassen zu lassen"], True)
add("MiniMax", "https://www.minimax.io/", "minimax.io", "freemium", "proprietary", ["ki-chatbots", "audio-und-sprache"],
    "MiniMax bietet Sprachmodelle für Chat, Sprache und Video.",
    "MiniMax stellt Modelle über eine Konsole und eine Schnittstelle bereit. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Chat, Sprache und Video", "Konsole und Schnittstelle", "Einstieg und bezahlte Kontingente"],
    ["Ein Modell auszuprobieren", "Sprache oder Video über die API zu erzeugen"], False)
add("Microsoft Designer", "https://designer.microsoft.com/", "designer.microsoft.com", "freemium", "proprietary", ["design", "bildgenerierung"],
    "Microsoft Designer baut Social-Media-Grafiken und Bilder aus einer Beschreibung.",
    "Designer setzt Vorlagen und erzeugt Bilder aus Text. Es gibt einen kostenlosen Einstieg und Funktionen, die an Microsoft 365 gebunden sind.",
    ["Grafiken aus einer Beschreibung", "Vorlagen", "Kostenloser Einstieg"],
    ["Einen Beitrag für ein soziales Netzwerk zu gestalten", "Ein Bild aus einem Satz zu erzeugen"], True)
add("Otter", "https://otter.ai/", "otter.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "Otter schreibt Gespräche mit und fasst sie zusammen.",
    "Otter nimmt ein Meeting oder eine Aufnahme auf und liefert ein Transkript mit Zusammenfassung. Es gibt einen kostenlosen Einstieg und bezahlte Minuten.",
    ["Transkript von Gesprächen", "Zusammenfassung", "Kostenloser Einstieg und bezahlte Minuten"],
    ["Ein Meeting mitzuschreiben", "Die Zusammenfassung eines Gesprächs zu lesen"], True)
add("Fireflies", "https://fireflies.ai/", "fireflies.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "Fireflies sitzt in Meetings und schreibt mit, was besprochen wurde.",
    "Fireflies nimmt an einem Videogespräch teil und liefert Transkript und Notizen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Mitschrieb im Meeting", "Notizen und Transkript", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Gespräch automatisch mitzuschreiben", "Aufgaben aus dem Meeting zu sehen"], False)
add("Fathom Video", "https://fathom.video/", "fathom.video", "freemium", "proprietary", ["audio-und-sprache"],
    "Fathom zeichnet Meetings auf und markiert die wichtigen Stellen.",
    "Fathom schreibt mit und lässt Highlights setzen. Es gibt einen kostenlosen Einstieg und bezahlte Team-Funktionen.",
    ["Meeting-Aufzeichnung", "Highlights", "Kostenloser Einstieg und bezahlte Team-Funktionen"],
    ["Ein Gespräch aufzuzeichnen", "Eine Stelle später wiederzufinden"], True)
add("tl;dv", "https://tldv.io/", "tldv.io", "freemium", "proprietary", ["audio-und-sprache"],
    "tl;dv schneidet Meetings in kurze Clips und schreibt mit.",
    "tl;dv nimmt das Gespräch auf und erzeugt ein Transkript mit Clips. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Meeting-Clips", "Transkript", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Stelle aus einem Meeting zu teilen", "Das Transkript zu durchsuchen"], True)
add("Notta", "https://www.notta.ai/", "notta.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "Notta wandelt Sprache in Text und übersetzt das Transkript.",
    "Notta nimmt Audio auf oder lädt eine Datei und liefert den Text. Es gibt einen kostenlosen Einstieg und bezahlte Minuten.",
    ["Sprache zu Text", "Übersetzung des Transkripts", "Kostenloser Einstieg und bezahlte Minuten"],
    ["Eine Aufnahme abzutippen", "Ein Transkript in eine andere Sprache zu holen"], True)
add("Rytr", "https://rytr.me/", "rytr.me", "freemium", "proprietary", ["textgenerierung", "marketing"],
    "Rytr schreibt kurze Texte für Mails, Anzeigen und Produktbeschreibungen.",
    "Rytr nimmt einen Anwendungsfall und einen Ton und liefert Entwürfe. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Kurze Marketingtexte", "Ton und Anwendungsfall", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Eine Produktbeschreibung zu entwerfen", "Mehrere Töne für eine Mail zu vergleichen"], True)
add("Simplified", "https://simplified.com/", "simplified.com", "freemium", "proprietary", ["design", "textgenerierung"],
    "Simplified schreibt Texte und baut dazu Grafiken und kurze Videos.",
    "Simplified bündelt Text, Design und Video in einem Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Text, Grafik und Video", "Ein Konto für mehrere Formate", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Beitrag mit Bild und Text zu bauen", "Einen kurzen Clip zu schneiden"], True)
add("Anyword", "https://www.anyword.com/", "anyword.com", "freemium", "proprietary", ["textgenerierung", "marketing"],
    "Anyword schreibt Werbetexte und schätzt, welche Fassung besser ankommt.",
    "Anyword erzeugt Varianten für Anzeigen und Seiten. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Werbetext-Varianten", "Einschätzung der Fassung", "Einstieg und bezahlte Stufen"],
    ["Mehrere Anzeigentexte zu vergleichen", "Eine Landingpage zu entwerfen"], False)
add("Hypotenuse", "https://www.hypotenuse.ai/", "hypotenuse.ai", "freemium", "proprietary", ["textgenerierung", "e-commerce"],
    "Hypotenuse schreibt Produkttexte und Blogentwürfe in größerer Menge.",
    "Hypotenuse nimmt Stichpunkte oder eine Tabelle und erzeugt Beschreibungen. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Produkttexte in Menge", "Blogentwürfe", "Einstieg und bezahlte Kontingente"],
    ["Viele Produktbeschreibungen zu erzeugen", "Einen Artikel aus Stichpunkten zu starten"], False)
add("Scalenut", "https://www.scalenut.com/", "scalenut.com", "freemium", "proprietary", ["seo", "textgenerierung"],
    "Scalenut plant Inhalte zu einem Keyword und schreibt den Entwurf.",
    "Scalenut zeigt Begriffe aus der Suche und einen Texteditor dazu. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Inhalte zu einem Keyword", "Begriffe aus der Suche", "Einstieg und bezahlte Stufen"],
    ["Einen Artikel an ein Keyword anzupassen", "Eine Gliederung aus der Suche zu holen"], False)
add("Jenni", "https://jenni.ai/", "jenni.ai", "freemium", "proprietary", ["textgenerierung", "bildung"],
    "Jenni schreibt an Aufsätzen mit und schlägt den nächsten Satz vor.",
    "Jenni sitzt im Text und ergänzt Formulierungen und Zitate. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Mitschreiben im Aufsatz", "Satzvorschläge", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Aufsatz weiterzuschreiben", "Eine Formulierung vorschlagen zu lassen"], True)
add("SciSpace", "https://scispace.com/", "scispace.com", "freemium", "proprietary", ["recherche", "bildung"],
    "SciSpace erklärt wissenschaftliche Paper und beantwortet Fragen dazu.",
    "SciSpace öffnet ein PDF und markiert Stellen zu einer Frage. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Fragen an ein Paper", "Markierte Stellen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Paper abschnittsweise zu verstehen", "Eine Methode im PDF zu finden"], False)
add("Connected Papers", "https://www.connectedpapers.com/", "connectedpapers.com", "freemium", "proprietary", ["recherche"],
    "Connected Papers zeigt, welche Arbeiten mit einem Paper verwandt sind.",
    "Aus einem Ausgangspaper entsteht ein Netz ähnlicher Arbeiten. Es gibt einen kostenlosen Einstieg und bezahlte Graphen.",
    ["Netz verwandter Paper", "Ein Ausgangspaper", "Kostenloser Einstieg und bezahlte Graphen"],
    ["Literatur rund um ein Paper zu finden", "Einen Überblick über ein Feld zu bekommen"], False)
add("ResearchRabbit", "https://www.researchrabbit.ai/", "researchrabbit.ai", "free", "proprietary", ["recherche"],
    "ResearchRabbit sammelt Paper und schlägt ähnliche Arbeiten vor.",
    "ResearchRabbit legt eine Sammlung an und zeigt neuere, verwandte Titel. Die Nutzung ist ohne Abo beschrieben.",
    ["Sammlungen von Papern", "Ähnliche Arbeiten", "Nutzung ohne Abo"],
    ["Eine Literaturliste wachsen zu lassen", "Neue Arbeiten zu einem Thema zu sehen"], True)
add("Litmaps", "https://www.litmaps.com/", "litmaps.com", "freemium", "proprietary", ["recherche"],
    "Litmaps zeichnet eine Literaturkarte aus zitierten Papern.",
    "Litmaps zeigt, welche Arbeiten sich zitieren, und lässt die Karte filtern. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Karte aus Zitaten", "Filter", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Den Weg von Zitat zu Zitat zu sehen", "Eine Literatursuche zu visualisieren"], False)
add("Paperpal", "https://www.paperpal.com/", "paperpal.com", "freemium", "proprietary", ["textgenerierung", "bildung"],
    "Paperpal prüft wissenschaftliches Englisch und schlägt Formulierungen vor.",
    "Paperpal sitzt im Manuskript und markiert Sprache und Aufbau. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Wissenschaftliches Englisch", "Formulierungsvorschläge", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Manuskript sprachlich zu prüfen", "Einen Satz für ein Paper umzuformulieren"], False)
add("Getimg", "https://getimg.ai/", "getimg.ai", "freemium", "proprietary", ["bildgenerierung"],
    "Getimg erzeugt und bearbeitet Bilder aus Text in einem Editor.",
    "Getimg bietet mehrere Bildmodelle, Freistellen und Variationen. Es gibt einen kostenlosen Einstieg und bezahlte Credits.",
    ["Bilder aus Text", "Mehrere Modelle", "Kostenloser Einstieg und bezahlte Credits"],
    ["Ein Bild aus einer Beschreibung zu erzeugen", "Eine Variation eines Motivs zu holen"], True)
add("OpenArt", "https://openart.ai/", "openart.ai", "freemium", "proprietary", ["bildgenerierung"],
    "OpenArt erzeugt Bilder und kurze Clips aus Text und bietet mehrere Modelle.",
    "OpenArt sammelt Werkzeuge zum Erzeugen und Nachbearbeiten. Es gibt einen kostenlosen Einstieg und bezahlte Credits.",
    ["Bilder und kurze Clips", "Mehrere Modelle", "Kostenloser Einstieg und bezahlte Credits"],
    ["Ein Motiv aus Text zu erzeugen", "Ein Bild weiterzubearbeiten"], True)
add("SeaArt", "https://seaart.ai/", "seaart.ai", "freemium", "proprietary", ["bildgenerierung"],
    "SeaArt erzeugt Bilder aus Text und stellt Modelle der Community bereit.",
    "SeaArt lässt ein Modell wählen und ein Bild erzeugen. Es gibt einen kostenlosen Einstieg und bezahlte Credits.",
    ["Bilder aus Text", "Modelle der Community", "Kostenloser Einstieg und bezahlte Credits"],
    ["Ein Bild mit einem Community-Modell zu erzeugen", "Mehrere Stile zu vergleichen"], True)
add("StarryAI", "https://starryai.com/", "starryai.com", "freemium", "proprietary", ["bildgenerierung"],
    "StarryAI macht Bilder aus einer Beschreibung, auch in der App.",
    "StarryAI nimmt einen Prompt und liefert Bilder. Es gibt einen kostenlosen Einstieg und bezahlte Credits.",
    ["Bilder aus einer Beschreibung", "App", "Kostenloser Einstieg und bezahlte Credits"],
    ["Ein Bild auf dem Handy zu erzeugen", "Einen Stil auszuprobieren"], True)
add("Playground", "https://playground.com/", "playground.com", "freemium", "proprietary", ["bildgenerierung", "design"],
    "Playground erzeugt Bilder und legt sie auf eine Arbeitsfläche.",
    "Playground mischt Erzeugung und Layout auf einer Fläche. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Bilder auf einer Fläche", "Erzeugung aus Text", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Mehrere Motive nebeneinander zu legen", "Ein Bild aus Text zu starten"], True)
add("Scenario", "https://www.scenario.gg/", "scenario.gg", "freemium", "proprietary", ["bildgenerierung", "gaming"],
    "Scenario trainiert Bildmodelle auf den Stil eines Spiels.",
    "Scenario erzeugt Assets, die zum vorhandenen Look passen. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Assets im Spielstil", "Eigene Modelle", "Einstieg und bezahlte Kontingente"],
    ["Icons in einem festen Stil zu erzeugen", "Ein Modell auf eigene Bilder zu trainieren"], False)
add("Mage", "https://www.mage.space/", "mage.space", "freemium", "proprietary", ["bildgenerierung"],
    "Mage erzeugt Bilder aus Text mit mehreren offenen Modellen.",
    "Mage lässt das Modell und die Einstellungen wählen. Es gibt einen kostenlosen Einstieg und bezahlte Credits.",
    ["Mehrere Bildmodelle", "Einstellungen im Formular", "Kostenloser Einstieg und bezahlte Credits"],
    ["Ein Modell gegen ein anderes zu testen", "Ein Bild aus einer Beschreibung zu holen"], True)
add("Erase.bg", "https://www.erase.bg/", "erase.bg", "freemium", "proprietary", ["bildgenerierung"],
    "Erase.bg entfernt den Hintergrund von Bildern.",
    "Erase.bg nimmt ein Foto und liefert das freigestellte Motiv. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Hintergrund entfernen", "Download des Motivs", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Ein Produktfoto freizustellen", "Ein Porträt vom Hintergrund zu lösen"], True)
add("WatermarkRemover", "https://www.watermarkremover.io/", "watermarkremover.io", "freemium", "proprietary", ["bildgenerierung"],
    "WatermarkRemover versucht, Wasserzeichen aus Bildern zu entfernen.",
    "Das Werkzeug lädt ein Bild und liefert eine Fassung ohne das erkannte Zeichen. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Wasserzeichen entfernen", "Download der Fassung", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Ein Wasserzeichen aus einem eigenen Foto zu nehmen", "Eine saubere Fassung zu laden"], True)
add("Relume", "https://www.relume.io/", "relume.io", "freemium", "proprietary", ["design"],
    "Relume erzeugt aus einer Beschreibung eine Sitemap und Wireframes.",
    "Relume baut die Struktur einer Website und exportiert sie nach Figma oder Webflow. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Sitemap und Wireframes", "Export nach Figma oder Webflow", "Einstieg und bezahlte Stufen"],
    ["Die Struktur einer Website zu skizzieren", "Wireframes in Figma zu übernehmen"], False)
add("Uizard", "https://uizard.io/", "uizard.io", "freemium", "proprietary", ["design"],
    "Uizard macht aus einer Beschreibung oder einer Skizze einen Oberflächenentwurf.",
    "Uizard setzt Screens für Apps und Websites. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Oberflächen aus Text oder Skizze", "Screens für Apps", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen App-Entwurf zu skizzieren", "Aus einem Satz einen Screen zu holen"], True)
add("Visily", "https://www.visily.ai/", "visily.ai", "freemium", "proprietary", ["design"],
    "Visily baut Wireframes und klickbare Prototypen aus Text.",
    "Visily erzeugt Screens und verbindet sie zu einem Ablauf. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Wireframes und Prototypen", "Abläufe zwischen Screens", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen klickbaren Entwurf zu bauen", "Einen Ablauf ohne Designprogramm zu zeigen"], True)
add("Galileo AI", "https://www.usegalileo.ai/", "usegalileo.ai", "freemium", "proprietary", ["design"],
    "Galileo AI erzeugt Oberflächenentwürfe aus einer Beschreibung.",
    "Galileo setzt Screens, die sich weiterbearbeiten lassen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Screens aus einer Beschreibung", "Weiterbearbeiten", "Einstieg und bezahlte Stufen"],
    ["Einen ersten UI-Entwurf zu erzeugen", "Mehrere Screens zu einem Ablauf zu holen"], False)
add("Magic Patterns", "https://www.magicpatterns.com/", "magicpatterns.com", "freemium", "proprietary", ["design", "programmierung"],
    "Magic Patterns erzeugt Oberflächen und den dazu passenden Code.",
    "Magic Patterns nimmt eine Beschreibung und liefert einen Entwurf mit Komponenten. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Oberfläche und Code", "Komponenten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Screen mit Code zu starten", "Eine Komponente aus einem Satz zu holen"], False)
add("Replit", "https://replit.com/", "replit.com", "freemium", "proprietary", ["programmierung"],
    "Replit schreibt und startet Programme im Browser, auch mit einem Assistenten.",
    "Replit hält den Code online und führt ihn aus. Es gibt einen kostenlosen Einstieg und bezahlte Rechenzeit.",
    ["Code im Browser", "Assistent", "Kostenloser Einstieg und bezahlte Rechenzeit"],
    ["Ein Programm ohne lokale Einrichtung zu starten", "Einen Assistenten am Code mitarbeiten zu lassen"], True)
add("StackBlitz", "https://www.stackblitz.com/", "stackblitz.com", "freemium", "proprietary", ["programmierung"],
    "StackBlitz startet Webprojekte im Browser, nah an einer lokalen Umgebung.",
    "StackBlitz öffnet ein Projekt und führt es ohne Installation aus. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Webprojekte im Browser", "Start ohne Installation", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Frontend sofort zu öffnen", "Eine Abhängigkeit im Browser zu testen"], False)
add("CodeSandbox", "https://codesandbox.io/", "codesandbox.io", "freemium", "proprietary", ["programmierung"],
    "CodeSandbox zeigt laufende Webprojekte und lässt sie im Browser ändern.",
    "CodeSandbox startet eine Vorschau und speichert das Projekt online. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Vorschau im Browser", "Projekte online", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Beispiel sofort auszuführen", "Eine Änderung in der Vorschau zu sehen"], True)
add("Glitch", "https://www.glitch.com/", "glitch.com", "freemium", "proprietary", ["programmierung"],
    "Glitch hostet kleine Webprojekte, die sich im Browser bearbeiten lassen.",
    "Glitch mischt Editor und laufende Seite. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Editor und laufende Seite", "Kleine Webprojekte", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine kleine Seite sofort zu veröffentlichen", "Code und Ergebnis nebeneinander zu sehen"], True)
add("Val Town", "https://www.val.town/", "val.town", "freemium", "proprietary", ["programmierung"],
    "Val Town führt kleine JavaScript-Funktionen im Web aus und gibt ihnen eine Adresse.",
    "Val Town speichert eine Funktion und ruft sie über HTTP auf. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["JavaScript-Funktionen im Web", "Aufruf über HTTP", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine kleine API ohne Server zu starten", "Eine Funktion per Link zu teilen"], False)
add("Windsurf", "https://www.windsurf.com/", "windsurf.com", "freemium", "proprietary", ["programmierung"],
    "Windsurf ist ein Editor, der Code vorschlägt und Aufgaben im Projekt übernimmt.",
    "Windsurf schreibt mit und kann Änderungen über mehrere Dateien vorschlagen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Editor mit Vorschlägen", "Änderungen über mehrere Dateien", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Funktion beim Tippen ergänzen zu lassen", "Eine Änderung im Projekt vorzuschlagen"], False)
add("Continue", "https://www.continue.dev/", "continue.dev", "freemium", "unknown", ["programmierung"],
    "Continue hängt einen Chat an den Editor und lässt das Modell wählen.",
    "Continue beantwortet Fragen zum offenen Code. Eine OSI-Kennung wird hier nicht erneut eingetragen. Es gibt eine kostenlose Erweiterung und bezahlte Modelle.",
    ["Chat im Editor", "Wahl des Modells", "Kostenlose Erweiterung"],
    ["Den offenen Code erklären zu lassen", "Ein eigenes Modell anzubinden"], False)
add("Cline", "https://www.cline.bot/", "cline.bot", "freemium", "unknown", ["programmierung"],
    "Cline arbeitet als Agent im Editor und ändert Dateien nach einer Aufgabe.",
    "Cline liest das Projekt und schlägt konkrete Änderungen vor. Eine OSI-Kennung wird hier nicht eingetragen. Die Erweiterung ist ohne Pflichtabo erhältlich, das Modell dahinter kann kosten.",
    ["Agent im Editor", "Änderungen an Dateien", "Erweiterung ohne Pflichtabo"],
    ["Eine Aufgabe an den Editor zu geben", "Die vorgeschlagenen Änderungen zu prüfen"], False)
add("Roo Code", "https://www.roocode.com/", "roocode.com", "free", "unknown", ["programmierung"],
    "Roo Code ist ein Coding-Agent im Editor, verwandt mit Cline.",
    "Roo Code übernimmt Aufgaben im Projekt und zeigt die Schritte. Eine OSI-Kennung wird hier nicht eingetragen. Die Erweiterung ist ohne Pflichtabo erhältlich.",
    ["Coding-Agent", "Schritte im Projekt", "Nutzung ohne Pflichtabo"],
    ["Eine Änderung über mehrere Dateien vorzuschlagen", "Die Schritte des Agenten zu lesen"], False)
add("Qodo", "https://www.qodo.ai/", "qodo.ai", "freemium", "proprietary", ["programmierung"],
    "Qodo prüft Code und schlägt Tests zu einer Änderung vor.",
    "Qodo sitzt in der Entwicklungsumgebung und kommentiert Qualität und Tests. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Prüfung von Änderungen", "Testvorschläge", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Test zu einer Funktion vorzuschlagen", "Eine Änderung vor dem Merge prüfen zu lassen"], False)
add("Taskade", "https://www.taskade.com/", "taskade.com", "freemium", "proprietary", ["produktivitaet"],
    "Taskade legt Aufgaben, Notizen und Assistenten in einem Arbeitsbereich an.",
    "Taskade mischt Listen und einen Chat, der beim Formulieren hilft. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Aufgaben und Notizen", "Assistent im Arbeitsbereich", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Projektliste mit einem Assistenten zu führen", "Notizen in Aufgaben zu verwandeln"], True)
add("Mem", "https://www.mem.ai/", "mem.ai", "freemium", "proprietary", ["produktivitaet"],
    "Mem speichert Notizen und findet sie über den Inhalt statt über Ordner.",
    "Mem legt Notizen ab und beantwortet Fragen dazu. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Notizen ohne Ordnerzwang", "Fragen an die Notizen", "Einstieg und bezahlte Stufen"],
    ["Eine Notiz später über den Inhalt zu finden", "Eine Frage an die eigenen Notizen zu stellen"], False)
add("Reflect", "https://reflect.app/", "reflect.app", "paid", "proprietary", ["produktivitaet"],
    "Reflect verknüpft Notizen und lässt sie durchsuchen.",
    "Reflect speichert tägliche Notizen und Verbindungen zwischen ihnen. Die Nutzung ist kostenpflichtig.",
    ["Verknüpfte Notizen", "Tägliche Seiten", "Kostenpflichtige Nutzung"],
    ["Ein Tagesprotokoll mit Verweisen zu führen", "Eine Notiz über Verbindungen zu finden"], False)
add("Tana", "https://www.tana.inc/", "tana.inc", "freemium", "proprietary", ["produktivitaet"],
    "Tana legt Notizen als strukturierte Objekte mit Feldern an.",
    "Tana mischt Freitext und Felder, die sich abfragen lassen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Notizen mit Feldern", "Abfragen", "Einstieg und bezahlte Stufen"],
    ["Eine Besprechung als Objekt mit Feldern abzulegen", "Notizen nach einem Feld zu filtern"], False)
add("Craft", "https://www.craft.do/", "craft.do", "freemium", "proprietary", ["produktivitaet"],
    "Craft schreibt Dokumente mit Blöcken und teilt sie als Seite.",
    "Craft legt Texte, Bilder und Aufgaben in einem Dokument ab. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Dokumente aus Blöcken", "Teilen als Seite", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein geteiltes Dokument zu schreiben", "Aufgaben neben dem Text zu halten"], True)
add("Limitless", "https://www.limitless.ai/", "limitless.ai", "freemium", "proprietary", ["produktivitaet", "audio-und-sprache"],
    "Limitless schreibt Gespräche mit und macht sie später durchsuchbar.",
    "Limitless nimmt über ein Gerät oder die App auf und liefert ein Transkript. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Durchsuchbare Gespräche", "Transkript", "Einstieg und bezahlte Stufen"],
    ["Ein Gespräch später nach einem Satz zu durchsuchen", "Eine Aufnahme als Text zu lesen"], False)
add("Reclaim", "https://www.reclaim.ai/", "reclaim.ai", "freemium", "proprietary", ["produktivitaet"],
    "Reclaim legt Aufgaben als Blöcke in den Kalender und schiebt sie bei Konflikten.",
    "Reclaim verbindet sich mit dem Kalender und reserviert Zeit für Gewohnheiten und Aufgaben. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Aufgaben im Kalender", "Verschieben bei Konflikten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Fokuszeit im Kalender zu blocken", "Eine Aufgabe automatisch zu verschieben"], False)
add("Motion", "https://www.usemotion.com/", "usemotion.com", "paid", "proprietary", ["produktivitaet"],
    "Motion plant Aufgaben automatisch in die freien Lücken des Kalenders.",
    "Motion nimmt Aufgaben mit Frist und legt sie um Termine herum. Die Nutzung ist kostenpflichtig.",
    ["Aufgaben in Kalenderlücken", "Fristen", "Kostenpflichtige Nutzung"],
    ["Den Tag automatisch zu planen", "Eine Aufgabe um einen Termin herum zu legen"], False)
add("Sunsama", "https://www.sunsama.com/", "sunsama.com", "paid", "proprietary", ["produktivitaet"],
    "Sunsama plant den Tag aus Aufgaben mehrerer Werkzeuge.",
    "Sunsama zieht Aufgaben heran und lässt den Tag bewusst zusammenstellen. Die Nutzung ist kostenpflichtig.",
    ["Tagesplan aus mehreren Quellen", "Bewusstes Auswählen", "Kostenpflichtige Nutzung"],
    ["Den Tag aus einer Aufgabenliste zu bauen", "Nur das zu planen, was heute realistisch ist"], False)
add("Akiflow", "https://www.akiflow.com/", "akiflow.com", "paid", "proprietary", ["produktivitaet"],
    "Akiflow sammelt Aufgaben aus mehreren Diensten und legt sie in den Kalender.",
    "Akiflow bündelt Eingänge und macht daraus Zeitblöcke. Die Nutzung ist kostenpflichtig.",
    ["Aufgaben aus mehreren Diensten", "Zeitblöcke", "Kostenpflichtige Nutzung"],
    ["Eingänge an einem Ort zu sehen", "Eine Aufgabe in den Kalender zu ziehen"], False)
add("Clockwise", "https://www.clockwise.com/", "clockwise.com", "freemium", "proprietary", ["produktivitaet"],
    "Clockwise schiebt Meetings, damit längere Fokusblöcke entstehen.",
    "Clockwise verbindet sich mit dem Kalender und sucht zusammenhängende freie Zeit. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Fokusblöcke im Kalender", "Verschieben von Meetings", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen langen freien Block zu schützen", "Meetings automatisch zu bündeln"], False)
add("Podcastle", "https://podcastle.ai/", "podcastle.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "Podcastle nimmt Podcasts auf und räumt die Tonspur auf.",
    "Podcastle bietet Aufnahme, Transkript und Bereinigung. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Aufnahme und Transkript", "Bereinigung der Tonspur", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Folge im Browser aufzunehmen", "Eine Tonspur von Störgeräuschen zu befreien"], True)
add("Submagic", "https://submagic.co/", "submagic.co", "freemium", "proprietary", ["videoschnitt"],
    "Submagic setzt automatische Untertitel auf kurze Videos.",
    "Submagic nimmt einen Clip und legt animierte Untertitel darüber. Es gibt einen Einstieg und bezahlte Credits.",
    ["Automatische Untertitel", "Animierte Stile", "Einstieg und bezahlte Credits"],
    ["Untertitel auf ein Kurzvideo zu legen", "Einen Stil für die Worte zu wählen"], True)
add("Vizard", "https://vizard.ai/", "vizard.ai", "freemium", "proprietary", ["videoschnitt"],
    "Vizard schneidet aus einem langen Video kurze Clips.",
    "Vizard sucht Stellen und liefert fertige Kurzvideos mit Untertiteln. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Kurze Clips aus einem langen Video", "Untertitel", "Einstieg und bezahlte Stufen"],
    ["Aus einem Webinar mehrere Clips zu holen", "Einen Clip mit Untertiteln zu exportieren"], False)
add("Klap", "https://klap.app/", "klap.app", "freemium", "proprietary", ["videoschnitt"],
    "Klap macht aus langen Videos kurze Clips für soziale Netze.",
    "Klap wählt Stellen aus und setzt sie ins Hochformat. Es gibt einen Einstieg und bezahlte Credits.",
    ["Clips im Hochformat", "Auswahl aus einem langen Video", "Einstieg und bezahlte Credits"],
    ["Ein langes Video in Kurzclips zu teilen", "Einen Clip für ein soziales Netz zu exportieren"], True)
add("Vidnoz", "https://www.vidnoz.com/", "vidnoz.com", "freemium", "proprietary", ["videogenerierung"],
    "Vidnoz lässt einen Avatar einen Text sprechen.",
    "Vidnoz nimmt ein Skript und erzeugt ein Video mit einer Figur. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Avatar spricht ein Skript", "Video ohne Dreh", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Ein Erklärvideo ohne Kamera zu machen", "Dasselbe Skript mit einer anderen Figur zu sprechen"], True)
add("FlexClip", "https://www.flexclip.com/", "flexclip.com", "freemium", "proprietary", ["videoschnitt"],
    "FlexClip schneidet Videos im Browser aus Vorlagen, Text und Clips.",
    "FlexClip legt Szenen auf eine Zeitleiste und exportiert die Datei. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Schnitt im Browser", "Vorlagen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein kurzes Video aus Vorlagen zu bauen", "Text und Clips auf eine Zeitleiste zu legen"], True)
add("Steve AI", "https://www.steve.ai/", "steve.ai", "freemium", "proprietary", ["videogenerierung"],
    "Steve AI macht aus einem Text ein animiertes Erklärvideo.",
    "Steve AI setzt Szenen und eine Stimme unter ein Skript. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Animierte Erklärvideos", "Stimme unter dem Skript", "Einstieg und bezahlte Stufen"],
    ["Ein Erklärvideo aus einem Text zu erzeugen", "Szenen automatisch setzen zu lassen"], False)
add("Riffusion", "https://riffusion.com/", "riffusion.com", "freemium", "proprietary", ["musik"],
    "Riffusion erzeugt Musikclips aus einer Beschreibung.",
    "Riffusion nimmt Stil und Text und liefert einen kurzen Track. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Musik aus einer Beschreibung", "Kurze Tracks", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Einen Jingle aus einem Satz zu holen", "Mehrere Stile zu vergleichen"], True)
add("FakeYou", "https://fakeyou.com/", "fakeyou.com", "freemium", "proprietary", ["audio-und-sprache"],
    "FakeYou spricht einen Text mit Stimmen aus einer Bibliothek.",
    "FakeYou lässt eine Stimme wählen und den Text vorlesen. Es gibt einen kostenlosen Einstieg und bezahlte Funktionen.",
    ["Text mit gewählter Stimme", "Bibliothek von Stimmen", "Kostenloser Einstieg und bezahlte Funktionen"],
    ["Einen Satz in einer bestimmten Stimme zu hören", "Mehrere Stimmen zu vergleichen"], True)
add("Voicemod", "https://www.voicemod.net/", "voicemod.net", "freemium", "proprietary", ["audio-und-sprache"],
    "Voicemod verändert die Stimme live in Calls und Aufnahmen.",
    "Voicemod sitzt zwischen Mikrofon und Programm und setzt Effekte oder andere Stimmen. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Live-Stimmveränderung", "Effekte und andere Stimmen", "Kostenloser Einstieg und bezahltes Abo"],
    ["Die Stimme in einem Call zu verändern", "Einen Effekt auf eine Aufnahme zu legen"], True)
add("WellSaid", "https://www.wellsaidlabs.com/", "wellsaidlabs.com", "paid", "proprietary", ["audio-und-sprache"],
    "WellSaid liest Skripte mit Studio-Stimmen vor.",
    "WellSaid erzeugt Voiceover für Videos und Kurse. Die Nutzung ist kostenpflichtig.",
    ["Studio-Stimmen", "Voiceover aus einem Skript", "Kostenpflichtige Nutzung"],
    ["Einen Sprechertext für ein Video zu erzeugen", "Mehrere Stimmen zu einem Skript zu hören"], False)
add("Resemble AI", "https://www.resemble.ai/", "resemble.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "Resemble AI klont eine Stimme und spricht damit neuen Text.",
    "Resemble nimmt eine Stimmprobe und erzeugt Sprache. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Stimmklon aus einer Probe", "Neuer Text in der Stimme", "Einstieg und bezahlte Kontingente"],
    ["Eine eigene Stimme für Ansagen zu nutzen", "Einen Text in der geklonten Stimme zu erzeugen"], False)
add("Kits AI", "https://www.kits.ai/", "kits.ai", "freemium", "proprietary", ["musik", "audio-und-sprache"],
    "Kits AI wandelt Gesang in eine andere Stimme um.",
    "Kits nimmt eine Gesangsspur und setzt ein Stimmmodell darüber. Es gibt einen kostenlosen Einstieg und bezahlte Credits.",
    ["Gesang in eine andere Stimme", "Stimmmodelle", "Kostenloser Einstieg und bezahlte Credits"],
    ["Eine Gesangsspur umzufärben", "Mehrere Stimmmodelle zu vergleichen"], False)
add("Uberduck", "https://www.uberduck.ai/", "uberduck.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "Uberduck spricht Text mit Stimmen und kann dazu Rap-Rhythmen setzen.",
    "Uberduck nimmt Text und eine Stimme und liefert Audio. Es gibt einen kostenlosen Einstieg und bezahlte Credits.",
    ["Text zu Sprache", "Stimmen und Rhythmus", "Kostenloser Einstieg und bezahlte Credits"],
    ["Einen Satz in einer bestimmten Stimme zu erzeugen", "Einen kurzen Rap aus Text zu holen"], True)
add("Podcastle Platzhalter", "https://podcastle.ai/", "podcastle.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "Platzhalter.", "Platzhalter.", ["x"], ["x"])


def validate(entries):
    entries[:] = [e for e in entries if "Platzhalter" not in e["name"]]
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
        if "zzgl" in (entry["shortDescriptionDe"] + entry["longDescriptionDe"]).lower():
            errors.append(f"ust {entry['name']}")
    if errors:
        raise SystemExit("\n".join(errors[:25]))
    return entries


if __name__ == "__main__":
    rows = validate(E)
    out = ROOT / "data" / "verified-tools-batch14.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows))
