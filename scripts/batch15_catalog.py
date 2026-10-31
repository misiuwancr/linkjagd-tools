#!/usr/bin/env python3
"""Fünfzehnte Liste: weitere bekannte KI-Tools, die HTTP 200 geliefert haben."""

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


add("Sonix", "https://www.sonix.ai/", "sonix.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "Sonix schreibt Audio und Video mit und übersetzt das Transkript.",
    "Sonix lädt eine Datei hoch und liefert einen durchsuchbaren Text. Es gibt einen Einstieg und bezahlte Minuten.",
    ["Transkript aus Audio und Video", "Übersetzung", "Einstieg und bezahlte Minuten"],
    ["Eine Aufnahme abzutippen", "Ein Transkript zu übersetzen"], True)
add("Trint", "https://www.trint.com/", "trint.com", "freemium", "proprietary", ["audio-und-sprache"],
    "Trint wandelt Interviews in bearbeitbaren Text.",
    "Trint spielt die Aufnahme neben dem Transkript ab. Es gibt einen Einstieg und bezahlte Stunden.",
    ["Transkript neben der Aufnahme", "Bearbeitbarer Text", "Einstieg und bezahlte Stunden"],
    ["Ein Interview zu verschriftlichen", "Eine Stelle im Ton über den Text zu finden"], False)
add("Rev", "https://www.rev.com/", "rev.com", "freemium", "proprietary", ["audio-und-sprache"],
    "Rev schreibt Sprache mit, maschinell oder durch Menschen.",
    "Rev nimmt Audio entgegen und liefert ein Transkript oder Untertitel. Die maschinelle Fassung hat einen Einstieg, menschliche Abschrift ist kostenpflichtig.",
    ["Maschinelle und menschliche Abschrift", "Untertitel", "Einstieg und kostenpflichtige Abschrift"],
    ["Eine Datei abtippen zu lassen", "Untertitel für ein Video zu bestellen"], True)
add("Temi", "https://www.temi.com/", "temi.com", "paid", "proprietary", ["audio-und-sprache"],
    "Temi schreibt Aufnahmen automatisch mit und rechnet pro Minute.",
    "Temi lädt Audio hoch und liefert den Text in kurzer Zeit. Die Abschrift ist kostenpflichtig.",
    ["Automatische Abschrift", "Abrechnung pro Minute", "Kostenpflichtige Nutzung"],
    ["Eine Besprechung schnell abzutippen", "Den Text einer Aufnahme zu laden"], True)
add("Grain", "https://www.grain.com/", "grain.com", "freemium", "proprietary", ["audio-und-sprache"],
    "Grain schneidet Meetings in Clips und schreibt die Stellen mit.",
    "Grain nimmt das Gespräch auf und lässt Highlights teilen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Meeting-Clips", "Highlights", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Stelle aus einem Gespräch zu teilen", "Highlights statt des ganzen Meetings zu schicken"], False)
add("Listnr", "https://www.listnr.tech/", "listnr.tech", "freemium", "proprietary", ["audio-und-sprache"],
    "Listnr liest Texte mit vielen Stimmen vor.",
    "Listnr nimmt ein Skript und liefert eine Sprachdatei. Es gibt einen kostenlosen Einstieg und bezahlte Zeichen.",
    ["Vorlesen von Skripten", "Viele Stimmen", "Kostenloser Einstieg und bezahlte Zeichen"],
    ["Einen Artikel als Audio zu erzeugen", "Mehrere Stimmen zu vergleichen"], True)
add("VoiceMaker", "https://voicemaker.in/", "voicemaker.in", "freemium", "proprietary", ["audio-und-sprache"],
    "VoiceMaker erzeugt Sprache aus Text mit einstellbarer Betonung.",
    "VoiceMaker lässt Stimme und Tempo wählen. Es gibt einen kostenlosen Einstieg und bezahlte Zeichen.",
    ["Text zu Sprache", "Tempo und Betonung", "Kostenloser Einstieg und bezahlte Zeichen"],
    ["Eine Ansage aus einem Text zu machen", "Das Tempo einer Stimme zu ändern"], True)
add("Zubtitle", "https://www.zubtitle.com/", "zubtitle.com", "freemium", "proprietary", ["videoschnitt"],
    "Zubtitle setzt Untertitel auf Videos und spricht sie mit.",
    "Zubtitle nimmt einen Clip und legt den erkannten Text darüber. Es gibt einen Einstieg und bezahlte Videos.",
    ["Automatische Untertitel", "Text auf dem Video", "Einstieg und bezahlte Videos"],
    ["Untertitel auf ein Video zu legen", "Den erkannten Text zu korrigieren"], True)
add("DeepBrain", "https://www.deepbrain.io/", "deepbrain.io", "freemium", "proprietary", ["videogenerierung"],
    "DeepBrain lässt einen Avatar einen Text in einem Video sprechen.",
    "DeepBrain nimmt ein Skript und erzeugt eine sprechende Figur. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Avatar mit Skript", "Video ohne Dreh", "Einstieg und bezahlte Kontingente"],
    ["Ein Schulungsvideo ohne Kamera zu machen", "Einen Text von einer Figur sprechen zu lassen"], False)
add("Creatify", "https://www.creatify.ai/", "creatify.ai", "freemium", "proprietary", ["videogenerierung", "marketing"],
    "Creatify macht aus einem Produktlink ein Werbevideo.",
    "Creatify liest eine Produktseite und setzt Clips und Text dazu. Es gibt einen Einstieg und bezahlte Videos.",
    ["Werbevideo aus einem Produktlink", "Clips und Text", "Einstieg und bezahlte Videos"],
    ["Ein Anzeigenvideo aus einer Shopseite zu holen", "Mehrere Fassungen eines Produkts zu sehen"], False)
add("Munch", "https://www.getmunch.com/", "getmunch.com", "freemium", "proprietary", ["videoschnitt"],
    "Munch schneidet aus langen Videos kurze Clips für soziale Netze.",
    "Munch sucht Stellen und liefert Kurzvideos. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Kurzclips aus langen Videos", "Formate für soziale Netze", "Einstieg und bezahlte Stufen"],
    ["Ein Webinar in mehrere Clips zu teilen", "Einen Clip für ein soziales Netz zu exportieren"], True)
add("Splitter", "https://www.splitter.ai/", "splitter.ai", "freemium", "proprietary", ["audio-und-sprache", "musik"],
    "Splitter trennt Gesang und Instrumente in einer Aufnahme.",
    "Splitter nimmt einen Song und liefert getrennte Spuren. Es gibt einen kostenlosen Einstieg und bezahlte Dateien.",
    ["Getrennte Spuren", "Gesang und Instrumente", "Kostenloser Einstieg und bezahlte Dateien"],
    ["Eine Gesangsspur aus einem Song zu ziehen", "Eine Instrumental-Fassung zu erzeugen"], True)
add("Splash", "https://www.splashmusic.com/", "splashmusic.com", "freemium", "proprietary", ["musik"],
    "Splash erzeugt Songs aus einer Beschreibung oder einem Text.",
    "Splash liefert einen Track zu Stil und Inhalt. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Songs aus einer Beschreibung", "Stil und Text", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen kurzen Song zu einem Thema zu erzeugen", "Mehrere Stile zu hören"], True)
add("AIPRM", "https://www.aiprm.com/", "aiprm.com", "freemium", "proprietary", ["ki-chatbots"],
    "AIPRM sammelt Prompt-Vorlagen für Chat-Werkzeuge.",
    "AIPRM zeigt fertige Anweisungen nach Aufgabe und Ton. Es gibt einen kostenlosen Einstieg und bezahlte Vorlagen.",
    ["Prompt-Vorlagen", "Aufgaben und Töne", "Kostenloser Einstieg und bezahlte Vorlagen"],
    ["Eine Vorlage für einen Blogtext zu nehmen", "Prompts nach Aufgabe zu filtern"], True)
add("PromptHero", "https://prompthero.com/", "prompthero.com", "freemium", "proprietary", ["bildgenerierung"],
    "PromptHero zeigt Bild-Prompts und die dazugehörigen Ergebnisse.",
    "PromptHero durchsucht Beispiele nach Stil und Modell. Ein Teil ist ohne Abo sichtbar, weitere Funktionen sind bezahlt.",
    ["Beispiele von Bild-Prompts", "Suche nach Stil", "Freier Anteil und bezahlte Funktionen"],
    ["Einen Prompt zu einem Stil zu finden", "Zu sehen, welches Modell ein Bild erzeugt hat"], True)
add("Snack Prompt", "https://snackprompt.com/", "snackprompt.com", "free", "proprietary", ["ki-chatbots"],
    "Snack Prompt sammelt kurze Prompt-Bausteine zum Kopieren.",
    "Snack Prompt zeigt Anweisungen, die sich in einen Chat übernehmen lassen. Die Suche ist ohne Abo möglich.",
    ["Kurze Prompt-Bausteine", "Kopieren in den Chat", "Suche ohne Abo"],
    ["Einen Baustein für eine Aufgabe zu kopieren", "Prompts zu einem Thema zu durchsuchen"], True)
add("CopyMatic", "https://www.copymatic.ai/", "copymatic.ai", "freemium", "proprietary", ["textgenerierung", "marketing"],
    "CopyMatic schreibt Anzeigen, Produkttexte und Blogentwürfe.",
    "CopyMatic nimmt ein Thema und liefert mehrere Textarten. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Anzeigen und Produkttexte", "Blogentwürfe", "Einstieg und bezahlte Kontingente"],
    ["Einen Anzeigentext zu entwerfen", "Mehrere Überschriften zu vergleichen"], True)
add("ClosersCopy", "https://www.closerscopy.com/", "closerscopy.com", "paid", "proprietary", ["textgenerierung", "marketing"],
    "ClosersCopy schreibt Verkaufstexte für Seiten und Mails.",
    "ClosersCopy erzeugt Longform und kurze Werbetexte aus Stichpunkten. Die Nutzung ist kostenpflichtig.",
    ["Verkaufstexte", "Seiten und Mails", "Kostenpflichtige Nutzung"],
    ["Eine Verkaufsseite zu entwerfen", "Eine Mail-Sequenz zu skizzieren"], False)
add("HoppyCopy", "https://www.hoppycopy.co/", "hoppycopy.co", "paid", "proprietary", ["textgenerierung", "marketing"],
    "HoppyCopy schreibt E-Mail-Sequenzen und Betreffzeilen.",
    "HoppyCopy nimmt ein Angebot und liefert mehrere Mail-Fassungen. Die Nutzung ist kostenpflichtig.",
    ["E-Mail-Sequenzen", "Betreffzeilen", "Kostenpflichtige Nutzung"],
    ["Eine Folge von Mails zu entwerfen", "Mehrere Betreffzeilen zu vergleichen"], False)
add("Peppertype", "https://www.peppertype.ai/", "peppertype.ai", "freemium", "proprietary", ["textgenerierung"],
    "Peppertype schreibt kurze Texte für Social Media und Blogs.",
    "Peppertype nimmt ein Thema und einen Ton. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Kurze Texte", "Ton und Thema", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Einen Social-Media-Text zu entwerfen", "Mehrere Töne zu vergleichen"], True)
add("MarketMuse", "https://www.marketmuse.com/", "marketmuse.com", "freemium", "proprietary", ["seo", "textgenerierung"],
    "MarketMuse zeigt, welche Themen ein Text noch abdecken sollte.",
    "MarketMuse vergleicht einen Entwurf mit Seiten aus der Suche. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Themenlücken im Text", "Vergleich mit der Suche", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Artikel auf fehlende Themen zu prüfen", "Eine Gliederung aus der Suche zu holen"], False)
add("Dashword", "https://www.dashword.com/", "dashword.com", "freemium", "proprietary", ["seo", "textgenerierung"],
    "Dashword richtet einen Text an den Begriffen aus, die zu einem Thema ranken.",
    "Dashword zeigt Zielbegriffe neben dem Entwurf. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Zielbegriffe neben dem Entwurf", "Ausrichtung auf ein Thema", "Einstieg und bezahlte Stufen"],
    ["Einen Text an ein Keyword anzupassen", "Fehlende Begriffe zu sehen"], False)
add("Eraser", "https://www.eraser.io/", "eraser.io", "freemium", "proprietary", ["design", "programmierung"],
    "Eraser zeichnet Diagramme und kann sie aus einer Beschreibung erzeugen.",
    "Eraser legt Abläufe und Architektur auf eine Fläche. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Diagramme aus einer Beschreibung", "Architektur und Abläufe", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Ablauf zu skizzieren", "Ein Diagramm aus einem Satz zu holen"], True)
add("Banani", "https://www.banani.co/", "banani.co", "freemium", "proprietary", ["design"],
    "Banani erzeugt Oberflächenentwürfe aus einer Beschreibung.",
    "Banani setzt Screens, die sich weiter anpassen lassen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Screens aus einer Beschreibung", "Weiter anpassen", "Einstieg und bezahlte Stufen"],
    ["Einen UI-Entwurf zu starten", "Mehrere Screens zu vergleichen"], False)
add("iAsk", "https://iask.ai/", "iask.ai", "freemium", "proprietary", ["recherche", "ki-chatbots"],
    "iAsk beantwortet Fragen und zeigt Quellen aus der Suche.",
    "iAsk verbindet eine Antwort mit Links. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Antworten mit Quellen", "Suche im Chat", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Frage mit Belegen zu stellen", "Die verlinkte Quelle zu öffnen"], True)
add("Komo", "https://komo.ai/", "komo.ai", "freemium", "proprietary", ["recherche", "ki-chatbots"],
    "Komo sucht und fasst die Treffer in einer Antwort zusammen.",
    "Komo zeigt eine Suche mit einer kurzen Zusammenfassung. Es gibt einen kostenlosen Einstieg.",
    ["Suche mit Zusammenfassung", "Treffer und Antwort", "Kostenloser Einstieg"],
    ["Ein Thema suchen und zusammenfassen zu lassen", "Treffer neben der Antwort zu lesen"], True)
add("Andi", "https://andisearch.com/", "andisearch.com", "free", "proprietary", ["recherche"],
    "Andi antwortet auf Suchanfragen in ganzen Sätzen statt nur mit einer Linkliste.",
    "Andi zeigt eine Antwort und die zugehörigen Seiten. Die Suche ist ohne Konto möglich.",
    ["Antwort statt nur Linkliste", "Zugehörige Seiten", "Suche ohne Konto"],
    ["Eine Frage als Suche zu stellen", "Die Quelle unter der Antwort zu öffnen"], True)
add("Modal", "https://modal.com/", "modal.com", "freemium", "proprietary", ["programmierung"],
    "Modal startet Python-Jobs und Modelle in der Cloud, ohne einen Server einzurichten.",
    "Modal führt Funktionen auf gemieteter Rechenzeit aus. Es gibt einen kostenlosen Einstieg und bezahlte Nutzung.",
    ["Python-Jobs in der Cloud", "Modelle ohne eigenen Server", "Kostenloser Einstieg und bezahlte Nutzung"],
    ["Eine Funktion in der Cloud laufen zu lassen", "Ein Modell ohne eigene GPU aufzurufen"], False)
add("RunPod", "https://www.runpod.io/", "runpod.io", "freemium", "proprietary", ["programmierung"],
    "RunPod vermietet Grafikchips für Training und Inferenz.",
    "RunPod startet eine Umgebung mit GPU und rechnet die Zeit ab. Es gibt einen Einstieg und bezahlte Nutzung.",
    ["Grafikchips auf Zeit", "Umgebungen für Modelle", "Einstieg und bezahlte Nutzung"],
    ["Ein Modell auf einer gemieteten GPU zu starten", "Eine Umgebung nur für die Laufzeit zu bezahlen"], False)
add("Vast.ai", "https://vast.ai/", "vast.ai", "freemium", "proprietary", ["programmierung"],
    "Vast.ai vermittelt Grafikchip-Rechner von Anbietern zu einem Stundenpreis.",
    "Vast listet Maschinen und startet darauf eine Umgebung. Die Nutzung ist nach Zeit kostenpflichtig, ein Guthaben lässt sich vorher laden.",
    ["Grafikchip-Rechner auf Zeit", "Stundenpreis", "Nutzung nach Zeit"],
    ["Eine günstige GPU für einen Lauf zu mieten", "Maschinen nach Preis zu vergleichen"], False)
add("Cerebras", "https://www.cerebras.ai/", "cerebras.ai", "freemium", "proprietary", ["programmierung", "ki-chatbots"],
    "Cerebras stellt schnelle Inferenz für Sprachmodelle über eine Schnittstelle bereit.",
    "Cerebras betreibt eigene Chips und bietet Modelle per API. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Inferenz auf eigenen Chips", "Modelle per API", "Einstieg und bezahlte Kontingente"],
    ["Ein Sprachmodell über eine schnelle API aufzurufen", "Antwortzeiten zu vergleichen"], False)
add("SambaNova", "https://www.sambanova.ai/", "sambanova.ai", "freemium", "proprietary", ["programmierung"],
    "SambaNova betreibt Modelle auf eigener Hardware und bietet sie als Dienst.",
    "SambaNova stellt Sprachmodelle über eine Plattform bereit. Es gibt einen Einstieg und bezahlte Nutzung.",
    ["Modelle als Dienst", "Eigene Hardware", "Einstieg und bezahlte Nutzung"],
    ["Ein Modell ohne eigene Rechner anzubinden", "Eine Plattform für Inferenz zu testen"], False)
add("Lambda", "https://lambdalabs.com/", "lambdalabs.com", "freemium", "proprietary", ["programmierung"],
    "Lambda vermietet Rechner mit Grafikchips und bietet eine Cloud für Modelle.",
    "Lambda startet Instanzen für Training und Inferenz. Die Miete ist kostenpflichtig.",
    ["Rechner mit Grafikchips", "Cloud für Modelle", "Kostenpflichtige Miete"],
    ["Eine GPU-Instanz zu starten", "Ein Modell in der Cloud zu trainieren"], False)
add("Factory", "https://www.factory.ai/", "factory.ai", "paid", "proprietary", ["programmierung"],
    "Factory lässt Software-Agenten Aufgaben in einem Repository bearbeiten.",
    "Factory nimmt einen Auftrag und arbeitet im Code. Die Nutzung ist kostenpflichtig.",
    ["Agenten im Repository", "Aufträge an den Code", "Kostenpflichtige Nutzung"],
    ["Eine Änderung an ein Agenten-Team zu geben", "Den Verlauf im Repository zu sehen"], False)
add("Magic", "https://www.magic.dev/", "magic.dev", "freemium", "proprietary", ["programmierung"],
    "Magic arbeitet als Coding-Agent an längeren Softwareaufgaben.",
    "Magic nimmt eine Aufgabe und schlägt Änderungen im Projekt vor. Es gibt einen Einstieg und bezahlte Nutzung.",
    ["Coding-Agent", "Änderungen im Projekt", "Einstieg und bezahlte Nutzung"],
    ["Eine größere Code-Aufgabe abzugeben", "Den Vorschlag des Agenten zu prüfen"], False)
add("Poolside", "https://www.poolside.ai/", "poolside.ai", "freemium", "proprietary", ["programmierung"],
    "Poolside bietet ein Modell und einen Assistenten für Softwareentwicklung.",
    "Poolside sitzt in der Entwicklung und schlägt Code vor. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Assistent für Software", "Codevorschläge", "Einstieg und bezahlte Stufen"],
    ["Code im Editor vorschlagen zu lassen", "Ein Modell für Entwicklung zu testen"], False)
add("01.AI", "https://www.01.ai/", "01.ai", "freemium", "proprietary", ["ki-chatbots"],
    "01.AI entwickelt die Yi-Modelle und stellt sie zum Ausprobieren bereit.",
    "Die Seite zeigt die Modelle und den Zugang. Es gibt einen Einstieg und weitere, kostenpflichtige Nutzung.",
    ["Yi-Modelle", "Zugang zum Ausprobieren", "Einstieg und weitere Nutzung"],
    ["Ein Yi-Modell zu testen", "Den Zugang zur API zu finden"], False)
add("Baichuan", "https://www.baichuan-ai.com/", "baichuan-ai.com", "freemium", "proprietary", ["ki-chatbots"],
    "Baichuan bietet Sprachmodelle und einen Chat auf Chinesisch und weiteren Sprachen.",
    "Baichuan stellt Modelle über eine Plattform bereit. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Sprachmodelle und Chat", "Plattform", "Einstieg und bezahlte Kontingente"],
    ["Ein Modell auszuprobieren", "Einen Chat der Plattform zu öffnen"], False)
add("StepFun", "https://www.stepfun.com/", "stepfun.com", "freemium", "proprietary", ["ki-chatbots"],
    "StepFun bietet Sprachmodelle und einen Chat im Browser.",
    "StepFun lässt ein Gespräch starten und Modelle vergleichen. Es gibt einen kostenlosen Einstieg.",
    ["Chat im Browser", "Mehrere Modelle", "Kostenloser Einstieg"],
    ["Eine Frage im Chat zu stellen", "Modelle nebeneinander zu sehen"], True)
add("Zhipu", "https://www.zhipuai.cn/", "zhipuai.cn", "freemium", "proprietary", ["ki-chatbots", "programmierung"],
    "Zhipu stellt die GLM-Modelle und eine Plattform dafür bereit.",
    "Zhipu bietet Chat und eine Schnittstelle. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["GLM-Modelle", "Chat und Schnittstelle", "Einstieg und bezahlte Kontingente"],
    ["Ein GLM-Modell aufzurufen", "Den Chat der Plattform zu testen"], False)
add("Falcon", "https://falconllm.tii.ae/", "falconllm.tii.ae", "free", "unknown", ["ki-chatbots"],
    "Falcon stellt die offenen Falcon-Sprachmodelle und ihre Modellkarten vor.",
    "Die Seite des Technology Innovation Institute beschreibt die Falcon-Reihe und verweist auf die Gewichte. Eine einzelne OSI-Lizenz aller Modelle wird hier nicht eingetragen. Die Modellkarten sind ohne Konto lesbar.",
    ["Modellkarten der Falcon-Reihe", "Verweis auf die Gewichte", "Lesen ohne Konto"],
    ["Ein Falcon-Modell einzuordnen", "Die Modellkarte zu lesen"], False)
add("Layer", "https://www.layer.ai/", "layer.ai", "freemium", "proprietary", ["bildgenerierung", "design"],
    "Layer erzeugt Grafiken für Spiele und Marken in einem festen Stil.",
    "Layer trainiert auf vorhandene Bilder und liefert neue Assets. Es gibt einen Einstieg und bezahlte Kontingente.",
    ["Grafiken in einem festen Stil", "Eigene Vorlagen", "Einstieg und bezahlte Kontingente"],
    ["Ein Icon-Set im Markenstil zu erzeugen", "Neue Assets zu vorhandenen Bildern zu holen"], False)
add("Weights", "https://www.weights.gg/", "weights.gg", "freemium", "proprietary", ["audio-und-sprache", "musik"],
    "Weights wandelt eine Stimme in ein anderes Stimmmodell um.",
    "Weights nimmt Audio und setzt ein Modell darüber. Es gibt einen kostenlosen Einstieg und bezahlte Credits.",
    ["Stimmmodelle auf Audio", "Upload einer Aufnahme", "Kostenloser Einstieg und bezahlte Credits"],
    ["Eine Aufnahme in eine andere Stimme zu legen", "Mehrere Modelle zu vergleichen"], False)
add("Glasp", "https://www.glasp.co/", "glasp.co", "freemium", "proprietary", ["recherche", "produktivitaet"],
    "Glasp hebt Stellen auf Webseiten hervor und sammelt sie.",
    "Glasp speichert Markierungen und kann sie mit anderen teilen. Es gibt einen kostenlosen Einstieg und bezahlte Funktionen.",
    ["Markierungen auf Webseiten", "Sammlung der Stellen", "Kostenloser Einstieg und bezahlte Funktionen"],
    ["Eine Stelle auf einer Seite festzuhalten", "Markierungen später wiederzufinden"], True)
add("PromptPerfect", "https://www.promptperfect.xyz/", "promptperfect.xyz", "freemium", "proprietary", ["ki-chatbots"],
    "PromptPerfect formuliert einen knappen Prompt ausführlicher um.",
    "PromptPerfect nimmt eine kurze Anweisung und liefert eine ausgearbeitete Fassung. Es gibt einen kostenlosen Einstieg und bezahlte Läufe.",
    ["Prompts umformulieren", "Ausgearbeitete Fassung", "Kostenloser Einstieg und bezahlte Läufe"],
    ["Einen kurzen Prompt zu erweitern", "Mehrere Fassungen zu vergleichen"], True)
add("CopyMatic bleibt", "https://www.copymatic.ai/", "copymatic.ai", "freemium", "proprietary", ["textgenerierung"],
    "Platzhalter.", "Platzhalter.", ["x"], ["x"])


def validate(entries):
    entries[:] = [e for e in entries if "bleibt" not in e["name"] and e["name"] != "Glasp"]
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
        n = len(entry["shortDescriptionDe"])
        if not (10 <= n <= 280):
            errors.append(f"kurz {entry['name']} {n}")
    if errors:
        raise SystemExit("\n".join(errors[:20]))
    return entries


if __name__ == "__main__":
    rows = validate(E)
    out = ROOT / "data" / "verified-tools-batch15.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows))
