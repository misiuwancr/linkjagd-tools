#!/usr/bin/env python3
"""Dritte geprüfte Liste. Open Source nur mit gelesener SPDX-Kennung."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

INSTALL = "Die Schritte zum Installieren stehen in der Projektdokumentation."
ROOT = Path(__file__).resolve().parents[1]


def oss(repo: str, license_name: str, project: str):
    return {
        "projectUrl": project,
        "repoUrl": repo,
        "license": license_name,
        "systems": [],
        "install": INSTALL,
    }


def tool(name, url, domain, price, license_type, cats, short, long, features, uses, beginner=False, oss_block=None, program=None):
    entry = {
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
        "partnerStatus": "found" if program else "none_found",
        "programPresence": "yes" if program else "unknown",
        "programInfoUrl": program[1] if program else "",
        "network": program[0] if program else "manual",
        "verified": True,
        "beginnerFriendly": beginner,
        "discoverySource": "offizielle-website",
        "oss": oss_block,
    }
    return entry


E: list[dict] = []


def add(*args, **kwargs):
    E.append(tool(*args, **kwargs))


add("Suno", "https://suno.com/", "suno.com", "freemium", "proprietary", ["musik", "audio-und-sprache"],
    "Suno erzeugt Musikstücke aus einer Textbeschreibung.",
    "Suno nimmt eine Stilangabe oder einen kurzen Text und liefert ein fertiges Stück mit Gesang oder Instrumenten. Die Erstellung läuft im Browser. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Musik aus einer Beschreibung", "Gesang oder Instrumental", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Songentwurf ohne Studio zu starten", "Eine Melodie zu einem Text zu hören"], True)
add("Udio", "https://www.udio.com/", "udio.com", "freemium", "proprietary", ["musik"],
    "Udio komponiert Songs aus Stil, Text und Referenzen im Browser.",
    "Udio erzeugt musikalische Entwürfe und lässt sie in weiteren Durchgängen anpassen. Die Dateien bleiben im Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Songs aus Stil und Text", "Weitere Durchgänge am Entwurf", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Songidee schnell hörbar zu machen", "Mehrere Varianten eines Stücks zu vergleichen"], True)
add("Stable Audio", "https://stableaudio.com/", "stableaudio.com", "freemium", "proprietary", ["musik", "audio-und-sprache"],
    "Stable Audio erzeugt Klänge und Musikclips aus einer Beschreibung.",
    "Stable Audio erstellt kurze Audioaufnahmen nach einer Texteingabe, von Geräuschen bis zu musikalischen Passagen. Die Nutzung läuft über die Website. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Audio aus Text", "Klänge und musikalische Passagen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Soundeffekt zu beschreiben", "Eine kurze Musikpassage zu erzeugen"], False)
add("AIVA", "https://www.aiva.ai/", "aiva.ai", "freemium", "proprietary", ["musik"],
    "AIVA komponiert instrumentale Musik für Filme, Spiele und Hintergründe.",
    "AIVA erzeugt instrumentale Stücke nach Stilvorgaben und erlaubt Anpassungen an Struktur und Instrumentation. Die Ergebnisse lädt man aus dem Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Instrumentale Kompositionen", "Stilvorgaben für Film und Spiel", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Hintergrund für ein Video zu komponieren", "Ein instrumentales Thema auszuprobieren"], False)
add("Boomy", "https://boomy.com/", "boomy.com", "freemium", "proprietary", ["musik"],
    "Boomy erstellt Songs und kann sie zur Veröffentlichung vorbereiten.",
    "Boomy erzeugt musikalische Entwürfe aus wenigen Angaben und bietet Wege, ein Stück weiter zu veröffentlichen. Die Arbeit bleibt im Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Songentwürfe aus wenigen Angaben", "Weg zur Veröffentlichung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen ersten Song ohne Instrumente zu bauen", "Einen Entwurf zur Veröffentlichung vorzubereiten"], True)
add("Soundraw", "https://soundraw.io/", "soundraw.io", "freemium", "proprietary", ["musik"],
    "Soundraw setzt Hintergrundmusik nach Länge, Stimmung und Tempo zusammen.",
    "Soundraw liefert nutzbare Musikbetten, deren Länge und Energie sich einstellen lassen. Gedacht ist der Einsatz unter Videos und Podcasts. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Musik nach Länge und Stimmung", "Einsatz unter Video und Podcast", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Musikbett für ein Video zu wählen", "Tempo und Stimmung eines Stücks anzupassen"], True)
add("Mubert", "https://mubert.com/", "mubert.com", "freemium", "proprietary", ["musik"],
    "Mubert streamt und erzeugt Hintergrundmusik für Inhalte und Apps.",
    "Mubert stellt generierte Musikstrecken bereit, die zu einer Stimmung passen. Neben dem Hören gibt es eine Anbindung für eigene Produkte. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Generierte Hintergrundmusik", "Stimmung als Vorgabe", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Musik unter einen Stream zu legen", "Eine Strecke für eine App zu erzeugen"], False)
add("Lalal.ai", "https://www.lalal.ai/", "lalal.ai", "freemium", "proprietary", ["audio-und-sprache", "musik"],
    "Lalal.ai trennt Gesang, Sprache und Instrumente in einer Audiodatei.",
    "Lalal.ai nimmt einen Mix und gibt einzelne Spuren zurück, etwa Stimme oder Begleitung. Die Verarbeitung läuft im Browser. Es gibt einen kostenlosen Einstieg und bezahlte Kontingente.",
    ["Stimmen und Instrumente trennen", "Verarbeitung im Browser", "Kostenloser Einstieg und bezahlte Kontingente"],
    ["Eine Gesangsspur aus einem Song zu ziehen", "Eine Sprachaufnahme von der Musik zu lösen"], True)
add("Murf", "https://murf.ai/", "murf.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "Murf spricht Texte mit wählbaren Stimmen für Vertonungen.",
    "Murf wandelt ein Skript in gesprochene Sprache um und erlaubt Pausen und Betonung im Editor. Die Datei lässt sich herunterladen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Text zu Sprache", "Pausen und Betonung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Erklärvideo zu vertonen", "Ein Skript mit einer festen Stimme zu sprechen"], True)
add("Speechify", "https://speechify.com/", "speechify.com", "freemium", "proprietary", ["audio-und-sprache", "bildung"],
    "Speechify liest Texte, Dokumente und Seiten vor.",
    "Speechify macht aus einem Text oder einer Datei eine Vorlesestimme und spielt sie im Browser oder in der App ab. Die Geschwindigkeit lässt sich ändern. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Vorlesen von Text und Dateien", "Einstellbare Geschwindigkeit", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Artikel anzuhören", "Ein Dokument vorlesen zu lassen"], True)
add("NaturalReader", "https://www.naturalreaders.com/", "naturalreaders.com", "freemium", "proprietary", ["audio-und-sprache", "bildung"],
    "NaturalReader liest Texte und Dokumente mit synthetischen Stimmen vor.",
    "NaturalReader spricht eingegebene Texte und hochgeladene Dokumente. Die Stimme und das Tempo lassen sich wählen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Vorlesen von Text und Dokumenten", "Wahl von Stimme und Tempo", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Text anzuhören statt zu lesen", "Ein Lernmaterial vorlesen zu lassen"], True)
add("Krisp", "https://krisp.ai/", "krisp.ai", "freemium", "proprietary", ["audio-und-sprache"],
    "Krisp filtert Störgeräusche aus Mikrofon und Gegenseite in Gesprächen.",
    "Krisp sitzt zwischen Mikrofon und Gesprächsanwendung und dämpft Hintergrundlärm. Die Stimme bleibt das Signal. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Geräuschfilter für Gespräche", "Einsatz vor der Gesprächs-App", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Gespräch in einem lauten Raum zu führen", "Das Mikrofon für eine Aufnahme zu beruhigen"], True)
add("Moises", "https://moises.ai/", "moises.ai", "freemium", "proprietary", ["musik", "audio-und-sprache"],
    "Moises trennt Spuren, setzt Tempo und übt Stücke zum Mitspielen.",
    "Moises zerlegt einen Song in Spuren und kann Tempo oder Tonart fürs Üben ändern. Die Arbeit läuft in der App und im Browser. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Spuren trennen", "Tempo und Tonart ändern", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Instrumentenspur zum Üben zu isolieren", "Ein Stück langsamer mitzuspielen"], True)
add("LANDR", "https://www.landr.com/", "landr.com", "freemium", "proprietary", ["musik"],
    "LANDR masstert Audiodateien und verteilt Musik an Plattformen.",
    "LANDR bearbeitet einen Mix zu einem lauteren, ausgewogeneren Master und bietet zusätzlich Veröffentlichung. Die Datei bleibt im Konto, bis man sie lädt. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Automatisches Mastering", "Veröffentlichung an Plattformen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Mix fertig zu machen", "Ein Stück zur Veröffentlichung vorzubereiten"], False)
add("BandLab", "https://www.bandlab.com/", "bandlab.com", "freemium", "proprietary", ["musik"],
    "BandLab ist ein Online-Studio für Aufnahmen, Beats und Zusammenarbeit.",
    "BandLab nimmt Spuren im Browser auf, mischt sie und lässt andere Personen am Projekt arbeiten. Fertige Stücke kann man teilen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Aufnahmen im Browser", "Mehrspur und Zusammenarbeit", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Song mit anderen im Browser aufzunehmen", "Einen Beat ohne lokale DAW zu bauen"], True)
add("LMMS", "https://lmms.io/", "lmms.io", "free", "open_source", ["musik"],
    "LMMS ist ein Mehrspur-Studio für Beats und elektronische Musik auf dem eigenen Rechner.",
    "LMMS bietet Sequenzer, Synthesizer und Mixer in einer lokalen Anwendung. Projekte bleiben als Dateien auf dem Rechner. Die Software ist ohne Pflichtabo nutzbar. Die SPDX-Kennung des Repositories ist GPL-2.0.",
    ["Sequenzer, Synthesizer und Mixer", "Projekte als lokale Dateien", "Lizenz GPL-2.0"],
    ["Einen Beat ohne Abo zu bauen", "Elektronische Musik lokal zu arrangieren"], False,
    oss("https://github.com/LMMS/lmms", "GPL-2.0", "https://lmms.io/"))
add("Ardour", "https://ardour.org/", "ardour.org", "free", "unknown", ["musik", "audio-und-sprache"],
    "Ardour nimmt und mischt Mehrspur-Audio auf dem eigenen Rechner.",
    "Ardour ist eine digitale Audio-Workstation für Aufnahme, Schnitt und Mischung. Die Sitzungen liegen lokal. Eine einzelne OSI-Kennung wurde hier nicht bestätigt, der Lizenztyp bleibt Unbekannt. Die Software ist ohne Pflichtabo erhältlich.",
    ["Aufnahme und Mischung", "Sitzungen auf dem eigenen Rechner", "Lizenztyp nicht als OSI bestätigt"],
    ["Eine Mehrspuraufnahme lokal zu mischen", "Einen Podcast oder ein Stück zu schneiden"], False)
add("MuseScore", "https://musescore.org/", "musescore.org", "freemium", "unknown", ["musik", "bildung"],
    "MuseScore setzt Noten und spielt Partituren ab.",
    "MuseScore Studio schreibt Noten auf dem eigenen Rechner und spielt sie zur Kontrolle ab. Die Website bietet zusätzlich ein Konto zum Teilen. Eine einzelne OSI-Kennung der aktuellen Ausgabe wurde hier nicht bestätigt.",
    ["Notensatz auf dem eigenen Rechner", "Wiedergabe der Partitur", "Teilen über ein Konto"],
    ["Eine Partitur zu schreiben", "Ein Stück aus den Noten anzuhören"], True)
add("CapCut", "https://www.capcut.com/", "capcut.com", "freemium", "proprietary", ["videoschnitt"],
    "CapCut schneidet Clips, Untertitel und Effekte auf dem Handy und im Browser.",
    "CapCut legt Videospuren, Texte und Musik auf eine Timeline und exportiert das Ergebnis. Vorlagen beschleunigen kurze Formate. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Timeline mit Text und Musik", "Vorlagen für kurze Formate", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein kurzes Video für ein soziales Netzwerk zu schneiden", "Untertitel auf einen Clip zu legen"], True)
add("DaVinci Resolve", "https://www.blackmagicdesign.com/products/davinciresolve", "blackmagicdesign.com", "freemium", "proprietary", ["videoschnitt"],
    "DaVinci Resolve schneidet, färbt und mischt Ton in einer Desktop-Anwendung.",
    "DaVinci Resolve bündelt Schnitt, Farbe und Audiomischung. Die kostenlose Ausgabe deckt den Schnitt ab, die Studio-Ausgabe ist bezahlt. Die Projekte liegen auf dem eigenen Rechner.",
    ["Schnitt, Farbe und Ton", "Kostenlose Ausgabe und bezahltes Studio", "Projekte auf dem eigenen Rechner"],
    ["Einen längeren Film lokal zu schneiden", "Farbe und Ton im selben Projekt zu bearbeiten"], False)
add("OpenShot", "https://www.openshot.org/", "openshot.org", "free", "unknown", ["videoschnitt"],
    "OpenShot schneidet Videos auf dem eigenen Rechner.",
    "OpenShot setzt Clips auf eine Timeline und exportiert eine Datei. Übergänge und Titel bleiben lokal. Eine OSI-Kennung wurde in diesem Durchgang nicht bestätigt, der Lizenztyp bleibt Unbekannt. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Timeline und Export", "Titel und Übergänge", "Betrieb ohne Pflichtabo"],
    ["Ein Video ohne Abo zu schneiden", "Einen Clip mit Titel lokal zu exportieren"], True)
add("Clipchamp", "https://clipchamp.com/", "clipchamp.com", "freemium", "proprietary", ["videoschnitt"],
    "Clipchamp schneidet Videos im Browser, auch mit Vorlagen und Untertiteln.",
    "Clipchamp öffnet eine Timeline im Browser und exportiert das fertige Video. Vorlagen und Text helfen bei kurzen Beiträgen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Schnitt im Browser", "Vorlagen und Untertitel", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Video ohne Installation zu schneiden", "Eine Vorlage für einen kurzen Beitrag zu nutzen"], True)
add("VEED", "https://www.veed.io/", "veed.io", "freemium", "proprietary", ["videoschnitt"],
    "VEED schneidet Videos im Browser und setzt Untertitel automatisch.",
    "VEED kombiniert Schnitt, Untertitel und einfache Bereinigung in einem Browser-Projekt. Die Datei wird online exportiert. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Schnitt und Untertitel im Browser", "Online-Export", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Untertitel unter einen Clip zu setzen", "Einen kurzen Beitrag im Browser zu schneiden"], True)
add("Kapwing", "https://www.kapwing.com/", "kapwing.com", "freemium", "proprietary", ["videoschnitt", "design"],
    "Kapwing bearbeitet Video, Bild und Untertitel gemeinsam im Browser.",
    "Kapwing legt Medien auf eine Arbeitsfläche und exportiert Video oder Bild. Untertitel und Zuschnitt sind Teil desselben Projekts. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Video und Bild im selben Projekt", "Untertitel und Zuschnitt", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Clip zu kürzen und zu untertiteln", "Ein Bild und ein Video in einem Entwurf zu mischen"], True)
add("InVideo", "https://invideo.io/", "invideo.io", "freemium", "proprietary", ["videoschnitt", "videogenerierung"],
    "InVideo baut Videos aus Vorlagen, Texten und eigenem Material.",
    "InVideo startet mit einer Vorlage oder einer Texteingabe und füllt Szenen mit Medien. Den Schnitt passt man in der Timeline an. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Vorlagen und Text zu Video", "Eigene Medien in der Timeline", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Erklärvideo aus einem Text zu starten", "Eine Vorlage mit eigenem Material zu füllen"], True)
add("Synthesia", "https://www.synthesia.io/", "synthesia.io", "paid", "proprietary", ["videogenerierung"],
    "Synthesia erzeugt Erklärvideos mit Avatar und gesprochenem Skript.",
    "Synthesia nimmt ein Skript und lässt es von einem Avatar vor der Kamera sprechen. Folien und Sprachen lassen sich im Projekt tauschen. Die Tarife sind kostenpflichtig. Die öffentliche Partnerseite ist geprüft und wird nicht als eigener Link gespeichert.",
    ["Avatar spricht ein Skript", "Folien und Sprachen im Projekt", "Kostenpflichtige Tarife"],
    ["Ein Schulungsvideo ohne Dreh zu erstellen", "Dasselbe Skript in einer anderen Sprache auszugeben"], False,
    None, ("direct", "https://www.synthesia.io/partners"))
add("HeyGen", "https://www.heygen.com/", "heygen.com", "freemium", "proprietary", ["videogenerierung", "audio-und-sprache"],
    "HeyGen erzeugt Avatar-Videos und Übersetzungen aus einem Skript oder einer Aufnahme.",
    "HeyGen spricht Texte mit einem Avatar oder überträgt eine vorhandene Aufnahme in eine andere Sprache. Die Projekte liegen im Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen. Die öffentliche Partnerseite ist geprüft.",
    ["Avatar-Video aus einem Skript", "Übersetzung einer Aufnahme", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Ansage ohne eigenes Set zu produzieren", "Ein Video in eine andere Sprache zu übertragen"], False,
    None, ("direct", "https://www.heygen.com/affiliate"))
add("Fliki", "https://fliki.ai/", "fliki.ai", "freemium", "proprietary", ["videogenerierung", "audio-und-sprache"],
    "Fliki macht aus einem Text ein Video mit Stimme und Szenen.",
    "Fliki spricht ein Skript und legt dazu passende Szenen. Stimme und Medien lassen sich tauschen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Text zu Video mit Stimme", "Tauschbare Szenen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein kurzes Erklärvideo aus einem Text zu bauen", "Dieselbe Geschichte mit einer anderen Stimme zu hören"], True)
add("Runway", "https://runwayml.com/", "runwayml.com", "freemium", "proprietary", ["videogenerierung", "bildgenerierung"],
    "Runway erzeugt und bearbeitet Videoclips aus Text, Bild oder vorhandenem Material.",
    "Runway bietet Werkzeuge, die aus einer Beschreibung oder einem Bild einen Clip machen und bestehendes Video verändern. Die Ergebnisse liegen im Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Clips aus Text oder Bild", "Bearbeitung vorhandenen Videos", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen kurzen Clip aus einer Beschreibung zu erzeugen", "Ein vorhandenes Video stilistisch zu verändern"], False)
add("Captions", "https://captions.ai/", "captions.ai", "freemium", "proprietary", ["videoschnitt"],
    "Captions setzt Untertitel und schneidet gesprochene Videos.",
    "Captions erkennt Sprache in einem Clip, legt Untertitel darüber und bietet Schnitt an der gesprochenen Spur. Die Arbeit läuft in der App. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Automatische Untertitel", "Schnitt an der Sprachspur", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein gesprochenes Video zu untertiteln", "Pausen aus einer Aufnahme zu entfernen"], True)
add("Descript", "https://www.descript.com/", "descript.com", "freemium", "proprietary", ["videoschnitt", "audio-und-sprache"],
    "Descript schneidet Video und Audio, indem man das Transkript bearbeitet.",
    "Descript schreibt die gesprochene Spur mit und lässt Schnitte über den Text zu. Overdub und Untertitel sitzen im selben Projekt. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Schnitt über das Transkript", "Untertitel im selben Projekt", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Podcast anhand des Textes zu kürzen", "Füllwörter aus einer Aufnahme zu entfernen"], False)
add("Dify", "https://dify.ai/", "dify.ai", "freemium", "unknown", ["ki-chatbots", "automatisierung"],
    "Dify baut Assistenten und Abläufe über angebundene Sprachmodelle.",
    "Dify verbindet ein Modell mit Wissen, Werkzeugen und einem Chat. Die Anwendung lässt sich selbst betreiben, daneben gibt es eine Cloud. Eine OSI-Kennung wurde hier nicht bestätigt, der Lizenztyp bleibt Unbekannt.",
    ["Assistenten mit Wissen und Werkzeugen", "Cloud und Selbstbetrieb", "Lizenztyp nicht als OSI bestätigt"],
    ["Einen internen Assistenten über eigene Dokumente zu legen", "Einen Modell-Ablauf selbst zu hosten"], False)
add("Flowise", "https://flowiseai.com/", "flowiseai.com", "free", "unknown", ["ki-chatbots", "programmierung"],
    "Flowise verbindet Sprachmodelle und Werkzeuge in einem visuellen Ablauf.",
    "Flowise setzt Bausteine für Modelle, Speicher und Werkzeuge auf eine Fläche und führt den Ablauf auf dem eigenen Server aus. Eine OSI-Kennung wurde hier nicht bestätigt. Die Software ist ohne Pflichtabo erhältlich.",
    ["Visuelle Modell-Abläufe", "Betrieb auf dem eigenen Server", "Lizenztyp nicht als OSI bestätigt"],
    ["Einen Chatfluss ohne eigene Oberfläche zu bauen", "Ein Modell mit einem Werkzeug zu verbinden"], False)
add("Langflow", "https://langflow.org/", "langflow.org", "free", "open_source", ["ki-chatbots", "programmierung"],
    "Langflow baut Modell-Abläufe visuell und steht unter MIT.",
    "Langflow verbindet Eingaben, Modelle und Werkzeuge auf einer Fläche. Der Ablauf läuft auf dem eigenen Server. Die SPDX-Kennung des Repositories ist MIT. Die Software ist ohne Pflichtabo nutzbar.",
    ["Visuelle Abläufe für Modelle", "Betrieb auf dem eigenen Server", "Lizenz MIT"],
    ["Einen Prototyp für einen Assistenten zu zeichnen", "Einen Ablauf lokal auszuprobieren"], False,
    oss("https://github.com/langflow-ai/langflow", "MIT", "https://langflow.org/"))
add("CrewAI", "https://www.crewai.com/", "crewai.com", "freemium", "open_source", ["ki-chatbots", "programmierung"],
    "CrewAI lässt mehrere Agenten eine Aufgabe in Rollen bearbeiten.",
    "CrewAI beschreibt Agenten mit Rollen und Werkzeugen, die eine Aufgabe nacheinander oder gemeinsam bearbeiten. Die Bibliothek steht unter MIT. Daneben gibt es eine bezahlte Plattform.",
    ["Agenten mit Rollen", "Bibliothek unter MIT", "Bezahlte Plattform daneben"],
    ["Eine Recherche auf mehrere Rollen zu verteilen", "Einen Agentenablauf im eigenen Code zu starten"], False,
    oss("https://github.com/crewAIInc/crewAI", "MIT", "https://www.crewai.com/"))
add("MindStudio", "https://mindstudio.ai/", "mindstudio.ai", "freemium", "proprietary", ["automatisierung", "ki-chatbots"],
    "MindStudio baut kleine Assistenten aus Anweisungen und angebundenen Diensten.",
    "MindStudio legt einen Assistenten mit Schritten an und stellt ihn als App oder Ablauf bereit. Die Logik bleibt im Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Assistenten aus Schritten", "Bereitstellung als App", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen wiederkehrenden Assistenten ohne eigenen Server zu bauen", "Einen Ablauf für ein Team bereitzustellen"], False)
add("Relevance AI", "https://relevanceai.com/", "relevanceai.com", "freemium", "proprietary", ["ki-chatbots", "automatisierung"],
    "Relevance AI baut Agenten, die Aufgaben über angebundene Werkzeuge erledigen.",
    "Relevance AI verbindet ein Modell mit Werkzeugen und Daten und lässt den Agenten eine Aufgabe abarbeiten. Die Einrichtung läuft im Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Agenten mit Werkzeugen", "Aufgaben im Konto", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Agenten an interne Daten zu hängen", "Eine wiederkehrende Aufgabe abgeben zu lassen"], False)
add("Stack AI", "https://www.stack-ai.com/", "stack-ai.com", "freemium", "proprietary", ["ki-chatbots", "automatisierung"],
    "Stack AI verbindet Modelle, Daten und Schnittstellen zu einem Ablauf.",
    "Stack AI setzt Bausteine für Eingaben, Modelle und Ziele auf eine Fläche. Den Ablauf kann ein Team im Konto nutzen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Abläufe aus Modell-Bausteinen", "Nutzung im Teamkonto", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen internen Wissensassistenten zu schalten", "Eine Schnittstelle an ein Modell zu hängen"], False)
add("Bardeen", "https://www.bardeen.ai/", "bardeen.ai", "freemium", "proprietary", ["automatisierung"],
    "Bardeen führt wiederkehrende Schritte im Browser zwischen Webseiten und Konten aus.",
    "Bardeen startet eine Abfolge, wenn eine Seite oder ein Knopfdruck das Signal gibt, und trägt Daten in ein anderes Werkzeug ein. Die Einrichtung läuft als Browser-Erweiterung. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Abläufe im Browser", "Übertrag in andere Werkzeuge", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Daten von einer Seite in eine Tabelle zu übernehmen", "Einen wiederkehrenden Klickpfad zu speichern"], False)
add("Dust", "https://dust.tt/", "dust.tt", "freemium", "proprietary", ["ki-chatbots"],
    "Dust baut Assistenten für ein Team auf internen Dokumenten und Werkzeugen.",
    "Dust verbindet ein Modell mit dem Wissen eines Teams und stellt den Assistenten im Arbeitsalltag bereit. Zugriffe bleiben im Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Team-Assistenten", "Anbindung interner Dokumente", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Fragen an das eigene Handbuch zu stellen", "Einen Assistenten für ein Team freizugeben"], False)
add("Lindy", "https://www.lindy.ai/", "lindy.ai", "freemium", "proprietary", ["automatisierung", "ki-chatbots"],
    "Lindy übernimmt wiederkehrende Büroaufgaben als Assistent.",
    "Lindy verbindet Postfach, Kalender und andere Dienste und führt daraus kleine Aufgaben aus. Die Regeln legt man im Konto fest. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Assistent für Postfach und Kalender", "Regeln im Konto", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine wiederkehrende E-Mail vorbereiten zu lassen", "Termine und Nachrichten zu sortieren"], False)
add("GnuCash", "https://www.gnucash.org/", "gnucash.org", "free", "unknown", ["finanzen"],
    "GnuCash führt doppelte Buchführung auf dem eigenen Rechner.",
    "GnuCash erfasst Konten, Buchungen und Berichte in einer lokalen Datei. Eine Cloud ist nicht erforderlich. Eine OSI-Kennung wurde in diesem Durchgang nicht bestätigt, der Lizenztyp bleibt Unbekannt.",
    ["Konten und Buchungen", "Berichte aus der lokalen Datei", "Betrieb ohne Cloud-Pflicht"],
    ["Eine kleine Buchhaltung lokal zu führen", "Einnahmen und Ausgaben auf Konten zu buchen"], False)
add("KMyMoney", "https://kmymoney.org/", "kmymoney.org", "free", "unknown", ["finanzen"],
    "KMyMoney führt Konten, Budgets und Buchungen auf dem eigenen Rechner.",
    "KMyMoney importiert Umsätze und ordnet sie Kategorien und Konten zu. Die Datei bleibt lokal. Eine OSI-Kennung wurde hier nicht bestätigt.",
    ["Konten, Budgets und Buchungen", "Import von Umsätzen", "Lokale Datei"],
    ["Ein Haushaltsbuch auf dem eigenen Rechner zu führen", "Umsätze Kategorien zuzuordnen"], False)
add("YNAB", "https://www.youneedabudget.com/", "youneedabudget.com", "paid", "proprietary", ["finanzen"],
    "YNAB plant Geld in Kategorien, bevor es ausgegeben wird.",
    "YNAB teilt verfügbares Geld auf Kategorien und zieht Ausgaben davon ab. Konten lassen sich anbinden. Die Nutzung ist kostenpflichtig.",
    ["Kategorien vor der Ausgabe", "Anbindung von Konten", "Kostenpflichtige Nutzung"],
    ["Ein Monatsbudget nach verfügbarem Geld zu planen", "Ausgaben einer Kategorie gegenüberzustellen"], True)
add("Monarch Money", "https://www.monarchmoney.com/", "monarchmoney.com", "paid", "proprietary", ["finanzen"],
    "Monarch Money bündelt Konten, Budgets und Vermögen in einer Übersicht.",
    "Monarch liest angebundene Konten ein und zeigt Budgets, Ziele und Vermögen. Die Planung bleibt im Konto. Die Nutzung ist kostenpflichtig.",
    ["Konten, Budgets und Vermögen", "Übersicht im Konto", "Kostenpflichtige Nutzung"],
    ["Mehrere Konten an einem Ort zu sehen", "Ein Budget gegen echte Umsätze zu halten"], False)
add("Wave", "https://www.waveapps.com/", "waveapps.com", "freemium", "proprietary", ["finanzen"],
    "Wave schreibt Rechnungen und führt eine einfache Buchhaltung für kleine Betriebe.",
    "Wave legt Kunden, Rechnungen und Zahlungen an und zeigt eine grundlegende Buchhaltung. Der Einstieg für Rechnungen ist ohne Monatsabo möglich, Zahlungsabwicklung und Zusatzfunktionen sind bezahlt.",
    ["Rechnungen und Kunden", "Einfache Buchhaltung", "Einstieg ohne Monatsabo, Zusatzfunktionen bezahlt"],
    ["Eine Rechnung an einen Kunden zu schicken", "Einnahmen eines kleinen Betriebs zu erfassen"], True)
add("Ghostfolio", "https://ghostfol.io/", "ghostfol.io", "free", "open_source", ["finanzen"],
    "Ghostfolio verfolgt ein Depot und lässt sich selbst betreiben.",
    "Ghostfolio erfasst Käufe, Positionen und Wertentwicklung eines Depots. Die Daten können auf dem eigenen Server liegen. Die SPDX-Kennung ist AGPL-3.0.",
    ["Positionen und Wertentwicklung", "Selbstbetrieb", "Lizenz AGPL-3.0"],
    ["Ein Depot selbst zu erfassen", "Die Wertentwicklung nicht nur bei einem Broker zu sehen"], False,
    oss("https://github.com/ghostfolio/ghostfolio", "AGPL-3.0", "https://ghostfol.io/"))
add("Portfolio Performance", "https://www.portfolio-performance.info/", "portfolio-performance.info", "free", "open_source", ["finanzen"],
    "Portfolio Performance rechnet Depots und Rendite auf dem eigenen Rechner.",
    "Portfolio Performance importiert Buchungen und zeigt Rendite, Risiko und Vermögensaufstellung. Die Datei bleibt lokal. Die SPDX-Kennung des Repositories ist EPL-1.0.",
    ["Rendite und Vermögensaufstellung", "Lokale Datei", "Lizenz EPL-1.0"],
    ["Die Rendite eines Depots nachzurechnen", "Buchungen eines Brokers lokal auszuwerten"], False,
    oss("https://github.com/buchen/portfolio", "EPL-1.0", "https://www.portfolio-performance.info/"))
add("hledger", "https://hledger.org/", "hledger.org", "free", "open_source", ["finanzen"],
    "hledger führt eine Textdatei-Buchhaltung in der Kommandozeile.",
    "hledger liest Buchungen aus einer Textdatei und erstellt Berichte, Bilanzen und Register. Die Daten bleiben im eigenen Format. Die SPDX-Kennung ist GPL-3.0.",
    ["Buchungen als Text", "Berichte und Bilanzen", "Lizenz GPL-3.0"],
    ["Eine Buchhaltung in einer Textdatei zu führen", "Einen Bericht aus denselben Buchungen zu erzeugen"], False,
    oss("https://github.com/simonmichael/hledger", "GPL-3.0", "https://hledger.org/"))
add("Beancount", "https://beancount.github.io/docs/", "beancount.github.io", "free", "open_source", ["finanzen"],
    "Beancount bucht in einer Textdatei mit doppelter Buchführung.",
    "Beancount prüft eine Buchungsdatei und erzeugt Bilanzen und Auswertungen. Die Datei lässt sich mit Versionsverwaltung ablegen. Die SPDX-Kennung ist GPL-2.0.",
    ["Doppelte Buchführung als Text", "Bilanzen aus der Datei", "Lizenz GPL-2.0"],
    ["Buchungen versioniert abzulegen", "Eine Bilanz aus einer Textdatei zu rechnen"], False,
    oss("https://github.com/beancount/beancount", "GPL-2.0", "https://beancount.github.io/docs/"))
add("Copilot Money", "https://copilot.money/", "copilot.money", "paid", "proprietary", ["finanzen"],
    "Copilot Money sortiert Kontoumsätze und Budgets auf dem Handy.",
    "Copilot Money liest angebundene Konten und ordnet Umsätze Kategorien zu. Budgets und Rückblicke bleiben in der App. Die Nutzung ist kostenpflichtig.",
    ["Umsätze und Kategorien", "Budgets in der App", "Kostenpflichtige Nutzung"],
    ["Monatsausgaben auf dem Handy zu sehen", "Umsätze automatisch zu kategorisieren"], False)

add("Cronometer", "https://cronometer.com/", "cronometer.com", "freemium", "proprietary", ["gesundheit"],
    "Cronometer zählt Kalorien und Nährstoffe aus Mahlzeiten und Lebensmitteln.",
    "Cronometer führt ein Tagebuch für Essen und zeigt Nährstoffe über die Kalorien hinaus. Ziele lassen sich setzen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Ernährungstagebuch", "Nährstoffe neben Kalorien", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Mahlzeit auf Nährstoffe zu prüfen", "Ein Tagesziel für Ernährung zu halten"], True)
add("MyFitnessPal", "https://www.myfitnesspal.com/", "myfitnesspal.com", "freemium", "proprietary", ["gesundheit"],
    "MyFitnessPal protokolliert Essen, Bewegung und ein Kalorienziel.",
    "MyFitnessPal sucht Lebensmittel und trägt sie in ein Tagebuch ein. Bewegung kann das Tagesziel verändern. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Lebensmittel-Tagebuch", "Kalorienziel und Bewegung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Mahlzeiten eines Tages zu erfassen", "Ein Kalorienziel zu verfolgen"], True)
add("Strava", "https://www.strava.com/", "strava.com", "freemium", "proprietary", ["gesundheit"],
    "Strava zeichnet Läufe, Fahrten und andere Aktivitäten auf und zeigt Strecken.",
    "Strava speichert Aktivitäten mit Strecke, Zeit und Höhe und kann sie mit anderen teilen. Segmente vergleichen Abschnitte. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Aktivitäten mit Strecke und Zeit", "Teilen und Segmente", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Lauf oder eine Fahrt aufzuzeichnen", "Dieselbe Strecke mit früheren Fahrten zu vergleichen"], True)
add("Hevy", "https://www.hevyapp.com/", "hevyapp.com", "freemium", "proprietary", ["gesundheit"],
    "Hevy protokolliert Krafttraining mit Sätzen, Wiederholungen und Gewichten.",
    "Hevy führt Trainingspläne und trägt jede Einheit mit Sätzen ein. Frühere Werte bleiben zum Vergleich. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Sätze, Wiederholungen und Gewicht", "Trainingspläne", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Krafttraining mitzuschreiben", "Ein Gewicht mit der letzten Einheit zu vergleichen"], True)
add("wger", "https://wger.de/", "wger.de", "free", "open_source", ["gesundheit"],
    "wger verwaltet Trainingspläne und Übungen und lässt sich selbst betreiben.",
    "wger speichert Übungen, Pläne und Körperwerte. Eine öffentliche Instanz und der Selbstbetrieb stehen bereit. Die SPDX-Kennung ist AGPL-3.0.",
    ["Übungen und Trainingspläne", "Öffentliche Instanz und Selbstbetrieb", "Lizenz AGPL-3.0"],
    ["Einen Trainingsplan selbst zu hosten", "Übungen einer Einheit festzuhalten"], False,
    oss("https://github.com/wger-project/wger", "AGPL-3.0", "https://wger.de/"))
add("Headspace", "https://www.headspace.com/", "headspace.com", "freemium", "proprietary", ["gesundheit"],
    "Headspace führt durch kurze Meditationen und Schlafübungen.",
    "Headspace spielt angeleitete Sitzungen für Aufmerksamkeit, Schlaf und Alltag. Die Länge einer Sitzung ist wählbar. Es gibt einen begrenzten kostenlosen Einstieg und bezahlte Stufen.",
    ["Angeleitete Meditationen", "Sitzungen für Schlaf und Alltag", "Begrenzter kostenloser Einstieg und bezahlte Stufen"],
    ["Eine kurze Atempause anzuleiten", "Eine Schlafübung abzuspielen"], True)
add("Insight Timer", "https://insighttimer.com/", "insighttimer.com", "freemium", "proprietary", ["gesundheit"],
    "Insight Timer spielt Meditationen, Musik und Kurse von vielen Anleitenden.",
    "Insight Timer bietet eine große Bibliothek angeleiteter Sitzungen und einen einfachen Timer. Ein Teil ist ohne Abo hörbar, Kurse und weitere Titel liegen in bezahlten Stufen.",
    ["Meditationsbibliothek und Timer", "Viele Anleitende", "Kostenloser Anteil und bezahlte Stufen"],
    ["Eine geführte Meditation zu starten", "Einen stillen Timer für eine eigene Sitzung zu nutzen"], True)
add("Lose It", "https://www.loseit.com/", "loseit.com", "freemium", "proprietary", ["gesundheit"],
    "Lose It führt ein Kalorientagebuch mit einem Tagesbudget.",
    "Lose It trägt Lebensmittel und Bewegung gegen ein Tagesbudget. Barcodes beschleunigen die Erfassung. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Kalorien gegen ein Tagesbudget", "Erfassung per Barcode", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Tagesbudget für Essen zu halten", "Ein Lebensmittel schnell einzutragen"], True)
add("OpenEMR", "https://www.open-emr.org/", "open-emr.org", "free", "open_source", ["gesundheit"],
    "OpenEMR führt Patientenakten und Praxisabläufe auf dem eigenen Server.",
    "OpenEMR bündelt Akten, Termine und Abrechnung für eine Praxis, die den Server selbst betreibt. Die SPDX-Kennung ist GPL-3.0. Die Einrichtung richtet sich an Praxen mit eigener Administration.",
    ["Akten, Termine und Abrechnung", "Betrieb auf dem eigenen Server", "Lizenz GPL-3.0"],
    ["Eine Praxisakte selbst zu hosten", "Termine und Akten in einem System zu halten"], False,
    oss("https://github.com/openemr/openemr", "GPL-3.0", "https://www.open-emr.org/"))
add("TripIt", "https://www.tripit.com/", "tripit.com", "freemium", "proprietary", ["reisen"],
    "TripIt sammelt Buchungen einer Reise in einen Plan.",
    "TripIt liest Weiterleitungen von Buchungen und baut daraus einen Ablauf mit Flügen, Hotels und Zeiten. Der Plan ist unterwegs abrufbar. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Reiseplan aus Buchungen", "Flüge, Hotels und Zeiten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Mehrere Buchungen einer Reise zu bündeln", "Einen Tagesablauf unterwegs zu öffnen"], True)
add("Wanderlog", "https://wanderlog.com/", "wanderlog.com", "freemium", "proprietary", ["reisen"],
    "Wanderlog plant Reiserouten mit Orten, Notizen und Tagen.",
    "Wanderlog legt Tage, Orte und Notizen auf eine Karte und eine Liste. Mehrere Personen können denselben Plan sehen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Tage und Orte auf einer Karte", "Gemeinsame Pläne", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Route für mehrere Tage zu skizzieren", "Einen Reiseplan mit anderen zu teilen"], True)
add("Polarsteps", "https://www.polarsteps.com/", "polarsteps.com", "freemium", "proprietary", ["reisen"],
    "Polarsteps zeichnet eine Reise als Route mit Fotos und Tagen auf.",
    "Polarsteps speichert den Weg einer Reise und hängt Fotos und Notizen an die Stationen. Das Reisetagebuch lässt sich teilen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Route mit Fotos und Notizen", "Teilbares Reisetagebuch", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Reise als Tagebuch festzuhalten", "Den zurückgelegten Weg später anzusehen"], True)
add("Komoot", "https://www.komoot.com/", "komoot.com", "freemium", "proprietary", ["reisen", "gesundheit"],
    "Komoot plant Wander- und Radrouten und führt darunter entlang.",
    "Komoot berechnet eine Route nach Sportart und Wegart und zeigt sie auf der Karte. Regionen lassen sich freischalten. Es gibt einen kostenlosen Einstieg und bezahlte Kartenpakete.",
    ["Routen für Wandern und Rad", "Navigation auf der Karte", "Kostenloser Einstieg und bezahlte Kartenpakete"],
    ["Eine Tageswanderung zu planen", "Eine Radroute nach Wegart zu wählen"], True)
add("Organic Maps", "https://organicmaps.app/", "organicmaps.app", "free", "unknown", ["reisen"],
    "Organic Maps navigiert offline mit OpenStreetMap-Karten.",
    "Organic Maps lädt Karten auf das Gerät und führt ohne laufende Verbindung. Die Suche umfasst Orte und Kategorien. Eine OSI-Kennung wurde hier nicht bestätigt. Die App ist ohne Pflichtabo nutzbar.",
    ["Offline-Karten", "Suche nach Orten", "Nutzung ohne Pflichtabo"],
    ["Eine Stadt ohne Mobilfunkkarte zu navigieren", "Einen Weg offline zu planen"], True)
add("OsmAnd", "https://osmand.net/", "osmand.net", "freemium", "unknown", ["reisen"],
    "OsmAnd navigiert mit Offline-Karten aus OpenStreetMap.",
    "OsmAnd speichert Karten auf dem Gerät und führt zu Fuß, mit dem Rad oder im Auto. Zusatzkarten und Funktionen liegen in bezahlten Stufen. Eine OSI-Kennung wurde hier nicht bestätigt.",
    ["Offline-Navigation", "Profile für Fuß, Rad und Auto", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Region offline zu speichern", "Dieselbe Karte für Wanderung und Fahrt zu nutzen"], False)
add("KAYAK", "https://www.kayak.com/", "kayak.com", "free", "proprietary", ["reisen"],
    "KAYAK vergleicht Flüge, Hotels und Mietwagen aus mehreren Angeboten.",
    "KAYAK sucht Reisetermine über mehrere Anbieter und zeigt Preise nebeneinander. Ein Konto ist für die Suche nicht nötig. Die Buchung selbst liegt beim jeweiligen Anbieter.",
    ["Vergleich von Flügen und Hotels", "Preise mehrerer Anbieter", "Suche ohne Pflichtkonto"],
    ["Einen Flugtermin preislich zu vergleichen", "Hotel und Flug für dieselben Tage zu suchen"], True)
add("Booking.com", "https://www.booking.com/", "booking.com", "freemium", "proprietary", ["reisen"],
    "Booking.com sucht Unterkünfte und zeigt Preise, Lagen und Bewertungen.",
    "Booking.com listet Unterkünfte zu einem Ort und einem Zeitraum und filtert nach Lage und Ausstattung. Die Buchung läuft über die Plattform. Ein Konto ist für viele Suchen nicht nötig, Treuefunktionen sind an ein Konto gebunden.",
    ["Suche nach Unterkünften", "Filter nach Lage und Ausstattung", "Buchung über die Plattform"],
    ["Eine Unterkunft für bestimmte Nächte zu suchen", "Lagen innerhalb eines Orts zu vergleichen"], True)
add("Juro", "https://www.juro.com/", "juro.com", "paid", "proprietary", ["recht"],
    "Juro führt Verträge von der Vorlage bis zur Unterschrift in einem Arbeitsbereich.",
    "Juro speichert Vertragsvorlagen, Verhandlungen und den Status bis zur Signatur. Der Ablauf richtet sich an Teams. Die Nutzung ist kostenpflichtig.",
    ["Vorlagen und Verhandlung", "Status bis zur Signatur", "Kostenpflichtige Nutzung"],
    ["Einen Vertragsentwurf im Team zu prüfen", "Den Stand eines Vertrags zu sehen"], False)
add("iubenda", "https://www.iubenda.com/", "iubenda.com", "freemium", "proprietary", ["recht"],
    "iubenda erzeugt Datenschutzerklärungen und Einwilligungsbanner für Websites.",
    "iubenda stellt aus Angaben zur Website Texte und ein Banner zusammen und bindet sie ein. Rechtstexte bleiben im Konto pflegbar. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Datenschutztexte und Banner", "Einbindung in die Website", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Datenschutzerklärung für eine Website zu erzeugen", "Ein Einwilligungsbanner einzubinden"], False)
add("Termly", "https://termly.io/", "termly.io", "freemium", "proprietary", ["recht"],
    "Termly erstellt Datenschutz-, Cookie- und Nutzungsbedingungen für Websites.",
    "Termly führt durch Fragen zur Website und liefert Texte plus ein Cookie-Banner. Die Einbindung erfolgt über einen Ausschnitt. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Rechtstexte aus einem Fragebogen", "Cookie-Banner", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Nutzungsbedingungen für eine kleine Website zu starten", "Ein Cookie-Banner einzubauen"], True)
add("DocuSign", "https://www.docusign.com/", "docusign.com", "freemium", "proprietary", ["recht"],
    "DocuSign lässt Dokumente digital unterschreiben und verschickt sie an die Beteiligten.",
    "DocuSign legt Felder für Unterschrift und Datum auf ein Dokument und schickt es der Reihe nach an Personen. Der Status bleibt im Konto sichtbar. Es gibt einen begrenzten Einstieg und bezahlte Stufen.",
    ["Unterschriftfelder auf Dokumenten", "Versand an Beteiligte", "Begrenzter Einstieg und bezahlte Stufen"],
    ["Einen Vertrag zur Unterschrift zu schicken", "Den Status einer Signatur zu prüfen"], True)
add("DoNotPay", "https://donotpay.com/", "donotpay.com", "paid", "proprietary", ["recht"],
    "DoNotPay führt durch Schreiben für Verbraucheranliegen wie Gebühren und Kündigungen.",
    "DoNotPay stellt Assistenten bereit, die aus Angaben ein Schreiben oder einen Antrag erzeugen. Die Fälle bleiben im Konto. Die Nutzung ist kostenpflichtig.",
    ["Assistenten für Verbraucherschreiben", "Fälle im Konto", "Kostenpflichtige Nutzung"],
    ["Ein Widerspruchsschreiben zu beginnen", "Ein wiederkehrendes Formular auszufüllen"], False)
add("OrangeHRM", "https://www.orangehrm.com/", "orangehrm.com", "freemium", "open_source", ["personal"],
    "OrangeHRM führt Personalakten, Abwesenheiten und Bewerbungen.",
    "OrangeHRM speichert Mitarbeitende, Urlaub und offene Stellen. Die Software lässt sich selbst betreiben, die Cloud ist ein bezahltes Angebot. Die SPDX-Kennung des genannten Repositories ist GPL-3.0.",
    ["Personalakten und Urlaub", "Stellen und Bewerbungen", "Selbstbetrieb unter GPL-3.0 und bezahlte Cloud"],
    ["Urlaubsanträge in einer eigenen Installation zu führen", "Eine Personalakte selbst zu hosten"], False,
    oss("https://github.com/orangehrm/orangehrm", "GPL-3.0", "https://www.orangehrm.com/"))
add("Horilla", "https://horilla.com/", "horilla.com", "freemium", "open_source", ["personal"],
    "Horilla führt Personal, Anwesenheit und Recruiting und lässt sich selbst betreiben.",
    "Horilla bündelt Mitarbeitendendaten, Anwesenheit und Bewerbungen in einer Installation. Die SPDX-Kennung des genannten Repositories ist LGPL-2.1. Daneben gibt es bezahlte Angebote.",
    ["Personal und Anwesenheit", "Bewerbungen", "Lizenz LGPL-2.1"],
    ["Eine Personalverwaltung selbst zu hosten", "Bewerbungen und Anwesenheit in einem System zu sehen"], False,
    oss("https://github.com/horilla-opensource/horilla", "LGPL-2.1", "https://horilla.com/"))
add("BambooHR", "https://www.bamboohr.com/", "bamboohr.com", "paid", "proprietary", ["personal"],
    "BambooHR führt Personalakten, Urlaub und das Einarbeiten neuer Leute.",
    "BambooHR speichert Stammdaten, Abwesenheiten und Unterlagen zu Mitarbeitenden. Bewerbungen können in denselben Ablauf münden. Die Nutzung ist kostenpflichtig.",
    ["Stammdaten und Abwesenheiten", "Unterlagen und Einarbeitung", "Kostenpflichtige Nutzung"],
    ["Eine Personalakte in der Cloud zu führen", "Urlaubsanträge eines Teams zu sammeln"], False)
add("Greenhouse", "https://www.greenhouse.com/", "greenhouse.com", "paid", "proprietary", ["personal"],
    "Greenhouse organisiert Bewerbungen, Interviews und Zusagen.",
    "Greenhouse legt Stellen aus, sammelt Bewerbungen und führt Interviews mit Bewertungen. Berichte zeigen den Stand der Pipeline. Die Nutzung ist kostenpflichtig.",
    ["Stellen und Bewerbungen", "Interviews und Bewertungen", "Kostenpflichtige Nutzung"],
    ["Eine Stelle mit mehreren Interviewenden zu besetzen", "Den Stand aller Bewerbungen zu sehen"], False)
add("Lever", "https://www.lever.co/", "lever.co", "paid", "proprietary", ["personal"],
    "Lever führt Kandidatinnen und Kandidaten von der Quelle bis zur Zusage.",
    "Lever sammelt Profile, Nachrichten und Interviewrückmeldungen an einer Stelle. Die Pipeline zeigt, wo eine Bewerbung steht. Die Nutzung ist kostenpflichtig.",
    ["Profile, Nachrichten und Interviews", "Pipeline je Bewerbung", "Kostenpflichtige Nutzung"],
    ["Bewerbungen aus mehreren Quellen zu sammeln", "Rückmeldungen aus Interviews zu bündeln"], False)
add("Ashby", "https://www.ashbyhq.com/", "ashbyhq.com", "paid", "proprietary", ["personal"],
    "Ashby plant Recruiting mit Stellen, Interviews und Auswertungen.",
    "Ashby führt Bewerbungen, Terminplanung für Interviews und Berichte zum Recruiting. Der Ablauf ist für wachsende Teams gedacht. Die Nutzung ist kostenpflichtig.",
    ["Bewerbungen und Interviewtermine", "Berichte zum Recruiting", "Kostenpflichtige Nutzung"],
    ["Interviews für eine Stelle zu planen", "Die Herkunft von Bewerbungen auszuwerten"], False)
add("Workable", "https://www.workable.com/", "workable.com", "freemium", "proprietary", ["personal"],
    "Workable veröffentlicht Stellen und sammelt Bewerbungen an einem Ort.",
    "Workable schaltet eine Stelle auf mehreren Kanälen und legt eingehende Bewerbungen in eine Pipeline. Nachrichten und Bewertungen bleiben am Profil. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Stellen auf mehreren Kanälen", "Pipeline für Bewerbungen", "Einstieg und bezahlte Stufen"],
    ["Eine Stelle auszuschreiben", "Bewerbungen in Stufen zu sortieren"], False)
add("Recruitee", "https://recruitee.com/", "recruitee.com", "freemium", "proprietary", ["personal"],
    "Recruitee führt Karriereseiten, Stellen und Bewerbungen.",
    "Recruitee baut eine Karriereseite und sammelt Bewerbungen in einem gemeinsamen Posteingang. Das Team bewertet Profile dort. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Karriereseite und Stellen", "Gemeinsamer Posteingang", "Einstieg und bezahlte Stufen"],
    ["Eine Karriereseite mit offenen Stellen zu betreiben", "Bewerbungen im Team zu bewerten"], False)
add("Zendesk", "https://www.zendesk.com/", "zendesk.com", "paid", "proprietary", ["kundenservice"],
    "Zendesk sammelt Kundenanfragen aus Mail, Chat und Formularen in Tickets.",
    "Zendesk macht aus einer Anfrage ein Ticket mit Verlauf, Zuständigkeit und Status. Hilfecenter können dieselben Themen öffentlich erklären. Die Nutzung ist kostenpflichtig.",
    ["Tickets aus mehreren Kanälen", "Zuständigkeit und Status", "Kostenpflichtige Nutzung"],
    ["Kundenanfragen in einer Warteschlange zu führen", "Ein Hilfecenter zu denselben Themen anzubieten"], False)
add("Freshdesk", "https://www.freshworks.com/freshdesk/", "freshworks.com", "freemium", "proprietary", ["kundenservice"],
    "Freshdesk verwandelt Kundenmails und Chats in Tickets für ein Team.",
    "Freshdesk legt Anfragen in einer gemeinsamen Warteschlange ab und verteilt sie auf Personen. Antworten und interne Notizen bleiben am Ticket. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Gemeinsame Ticket-Warteschlange", "Antworten und interne Notizen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Support-Mails im Team zu verteilen", "Den Verlauf einer Kundenanfrage zu behalten"], False)
add("Help Scout", "https://www.helpscout.com/", "helpscout.com", "freemium", "proprietary", ["kundenservice"],
    "Help Scout beantwortet Kundenmail in einem gemeinsamen Postfach.",
    "Help Scout legt E-Mails in einem gemeinsamen Posteingang ab, mit Zuweisung und internen Notizen. Ein Hilfecenter kann dieselben Antworten veröffentlichen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Gemeinsames Postfach", "Zuweisung und Notizen", "Hilfecenter neben dem Postfach"],
    ["Support-Mail ohne ein privates Postfach zu beantworten", "Häufige Antworten in einem Hilfecenter abzulegen"], False)
add("Tidio", "https://www.tidio.com/", "tidio.com", "freemium", "proprietary", ["kundenservice"],
    "Tidio setzt einen Chat auf eine Website und sammelt die Gespräche.",
    "Tidio zeigt ein Chatfenster und kann einfache Fragen automatisch beantworten, bevor ein Mensch übernimmt. Die Verläufe bleiben im Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Chatfenster auf der Website", "Automatische erste Antworten", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Besucherfragen auf der eigenen Seite anzunehmen", "Einfache Fragen vor dem Team abzufangen"], True)
add("Intercom", "https://www.intercom.com/", "intercom.com", "paid", "proprietary", ["kundenservice"],
    "Intercom führt Chat, Hilfeartikel und Nachrichten an Nutzer in einem Konto.",
    "Intercom legt Gespräche mit Nutzerinnen und Nutzern an und kann Hilfeartikel dazu zeigen. Nachrichten lassen sich an Gruppen senden. Die Nutzung ist kostenpflichtig.",
    ["Chat und Hilfeartikel", "Nachrichten an Gruppen", "Kostenpflichtige Nutzung"],
    ["Ein Gespräch aus der eigenen App anzunehmen", "Einen Hilfeartikel zum selben Thema zu zeigen"], False)
add("Crisp", "https://crisp.chat/", "crisp.chat", "freemium", "proprietary", ["kundenservice"],
    "Crisp bündelt Chat, Mail und einen gemeinsamen Posteingang für Kundenfragen.",
    "Crisp setzt einen Chat auf die Website und sammelt auch andere Kanäle in einem Posteingang. Das Team antwortet von dort. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Chat auf der Website", "Gemeinsamer Posteingang", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Kundenchat auf einer Website anzubieten", "Mehrere Kanäle in einem Posteingang zu lesen"], True)
add("Zammad", "https://zammad.com/", "zammad.com", "freemium", "open_source", ["kundenservice"],
    "Zammad führt Tickets aus Mail, Chat und Telefon und lässt sich selbst betreiben.",
    "Zammad sammelt Anfragen in Tickets mit Gruppen und Vorlagen. Die Software steht unter AGPL-3.0 und kann auf dem eigenen Server laufen. Daneben gibt es eine bezahlte gehostete Fassung.",
    ["Tickets aus mehreren Kanälen", "Selbstbetrieb unter AGPL-3.0", "Bezahltes Hosting daneben"],
    ["Einen Support-Desk selbst zu hosten", "Anfragen einer Gruppe zuzuweisen"], False,
    oss("https://github.com/zammad/zammad", "AGPL-3.0", "https://zammad.com/"))
add("FreeScout", "https://freescout.net/", "freescout.net", "free", "open_source", ["kundenservice"],
    "FreeScout ist ein gemeinsames Postfach für Support-Mail auf dem eigenen Server.",
    "FreeScout legt E-Mails in gemeinsamen Postfächern ab und merkt sich Zuweisung und Notizen. Die SPDX-Kennung ist AGPL-3.0. Die Software ist ohne Pflichtabo nutzbar.",
    ["Gemeinsame Support-Postfächer", "Zuweisung und Notizen", "Lizenz AGPL-3.0"],
    ["Support-Mail selbst zu hosten", "Eine Anfrage einer Person zuzuweisen"], False,
    oss("https://github.com/freescout-help-desk/freescout", "AGPL-3.0", "https://freescout.net/"))
add("osTicket", "https://osticket.com/", "osticket.com", "free", "open_source", ["kundenservice"],
    "osTicket macht aus Kundenanfragen Tickets auf dem eigenen Server.",
    "osTicket nimmt Anfragen über Mail und Formular entgegen und führt sie als Tickets mit Status. Die SPDX-Kennung ist GPL-2.0. Die Software ist ohne Pflichtabo nutzbar.",
    ["Tickets aus Mail und Formular", "Status je Anfrage", "Lizenz GPL-2.0"],
    ["Ein Hilfeformular selbst zu betreiben", "Offene Anfragen nach Status zu filtern"], False,
    oss("https://github.com/osTicket/osTicket", "GPL-2.0", "https://osticket.com/"))
add("Ahrefs", "https://ahrefs.com/", "ahrefs.com", "paid", "proprietary", ["seo"],
    "Ahrefs untersucht Backlinks, Keywords und Seiten einer Website.",
    "Ahrefs zeigt, welche Seiten auf eine Domain verweisen, zu welchen Begriffen sie sichtbar ist und welche Seiten mitziehen. Berichte bleiben im Konto. Die Nutzung ist kostenpflichtig. Eine öffentliche Anmeldeseite für ein Partnerprogramm hat diese Prüfung nicht bestätigt.",
    ["Backlinks und Keywords", "Seitenberichte im Konto", "Kostenpflichtige Nutzung"],
    ["Die Backlinks einer Domain zu sichten", "Begriffe zu finden, zu denen eine Seite sichtbar ist"], False)
add("Semrush", "https://www.semrush.com/", "semrush.com", "freemium", "proprietary", ["seo", "marketing"],
    "Semrush prüft Keywords, Sichtbarkeit und Wettbewerber in der Suche.",
    "Semrush liefert Keyword-Ideen, Ranglisten und Hinweise zu Seiten. Ein Teil der Auswertungen ist im Einstieg sichtbar, der volle Umfang ist bezahlt. Eine weiterleitende Partneradresse landete bei dieser Prüfung nicht auf einer Anmeldeseite und wird nicht gespeichert.",
    ["Keywords und Sichtbarkeit", "Hinweise zu Seiten", "Einstieg und bezahlter Umfang"],
    ["Begriffe für eine Seite zu sammeln", "Die Sichtbarkeit einer Domain grob zu prüfen"], False)
add("Moz", "https://moz.com/", "moz.com", "freemium", "proprietary", ["seo"],
    "Moz bewertet Domains und sucht Keywords für die organische Suche.",
    "Moz zeigt Kennzahlen zu einer Domain und Vorschläge für Begriffe. Pro-Auswertungen liegen in bezahlten Stufen. Es gibt einen begrenzten kostenlosen Einstieg.",
    ["Domain-Kennzahlen", "Keyword-Vorschläge", "Begrenzter Einstieg und bezahlte Stufen"],
    ["Eine Domain grob einzuordnen", "Begriffe rund um ein Thema zu sammeln"], False)
add("Screaming Frog", "https://www.screamingfrog.co.uk/seo-spider/", "screamingfrog.co.uk", "freemium", "proprietary", ["seo"],
    "Screaming Frog crawlt eine Website und listet technische SEO-Befunde.",
    "Der SEO Spider lädt Seiten einer Domain und zeigt Titel, Statuscodes, Weiterleitungen und fehlende Angaben. Die kostenlose Fassung ist in der Zahl der URLs begrenzt, die volle Lizenz ist bezahlt.",
    ["Crawl von Titeln und Statuscodes", "Weiterleitungen und fehlende Angaben", "Begrenzte kostenlose Fassung und bezahlte Lizenz"],
    ["Fehlerhafte Seiten einer Website zu finden", "Titel und Weiterleitungen zu exportieren"], False)
add("Google Search Console", "https://search.google.com/search-console", "search.google.com", "free", "proprietary", ["seo"],
    "Die Search Console zeigt, wie Google eine eigene Website crawlt und ausspielt.",
    "Die Search Console listet Suchanfragen, Indexierung und technische Hinweise für eine bestätigte Website. Die Nutzung für die eigene Property ist ohne Abo möglich.",
    ["Suchanfragen und Indexierung", "Technische Hinweise zur eigenen Website", "Nutzung ohne Abo"],
    ["Zu sehen, zu welchen Anfragen die eigene Seite erscheint", "Indexierungsfehler zu prüfen"], True)
add("AnswerThePublic", "https://answerthepublic.com/", "answerthepublic.com", "freemium", "proprietary", ["seo", "recherche"],
    "AnswerThePublic sammelt Fragen, die Menschen zu einem Begriff suchen.",
    "AnswerThePublic gruppiert Suchformulierungen rund um ein Wort in Fragen, Vergleiche und Präpositionen. Die kostenlose Nutzung ist begrenzt, weitere Suchen sind bezahlt.",
    ["Fragen rund um einen Begriff", "Gruppierte Suchformulierungen", "Begrenzte kostenlose Nutzung und bezahlte Suchen"],
    ["Themen für einen Text zu sammeln", "Fragen zu einem Produktbegriff zu sehen"], True)
add("SISTRIX", "https://www.sistrix.com/", "sistrix.com", "paid", "proprietary", ["seo"],
    "SISTRIX bewertet Sichtbarkeit und Keywords, mit Schwerpunkt auf dem deutschsprachigen Markt.",
    "SISTRIX zeigt einen Sichtbarkeitsindex, Keywords und Wettbewerbsvergleiche. Die Auswertungen liegen im Konto. Die Nutzung ist kostenpflichtig.",
    ["Sichtbarkeitsindex", "Keywords und Wettbewerbsvergleich", "Kostenpflichtige Nutzung"],
    ["Die Sichtbarkeit einer deutschen Domain zu verfolgen", "Keywords eines Wettbewerbers zu sichten"], False)
add("Surfer", "https://surferseo.com/", "surferseo.com", "freemium", "proprietary", ["seo", "textgenerierung"],
    "Surfer vergleicht einen Text mit Seiten, die zu einem Begriff bereits ranken.",
    "Surfer zeigt Begriffe und Strukturen, die in sichtbaren Seiten vorkommen, und legt sie neben den eigenen Entwurf. Es gibt einen Einstieg und bezahlte Stufen. Die öffentliche Partnerseite ist geprüft und wird nicht als eigener Link gespeichert.",
    ["Vergleich mit rankenden Seiten", "Begriffe neben dem eigenen Text", "Einstieg und bezahlte Stufen"],
    ["Einen Text an sichtbare Seiten anzunähern", "Fehlende Begriffe in einem Entwurf zu sehen"], False,
    None, ("direct", "https://surfer.ai/affiliate-program/"))
add("Coda", "https://coda.io/", "coda.io", "freemium", "proprietary", ["daten", "produktivitaet"],
    "Coda verbindet Dokumente mit Tabellen, Schaltflächen und kleinen Abläufen.",
    "Coda legt Seiten an, in denen Text, Tabellen und Aktionen zusammenstehen. Ein Knopf kann eine Zeile ändern oder eine Benachrichtigung auslösen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Dokumente mit Tabellen", "Schaltflächen und kleine Abläufe", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Arbeitsseite mit Daten und Text zu bauen", "Einen Knopf an eine Tabellenzeile zu hängen"], False)
add("Rows", "https://rows.com/", "rows.com", "freemium", "proprietary", ["daten"],
    "Rows ist eine Tabelle, die Daten aus anderen Diensten in Zellen holt.",
    "Rows rechnet wie eine Tabellenkalkulation und kann Schnittstellen in Zellen abfragen. Ergebnisse bleiben im Dokument. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Tabelle mit Schnittstellen in Zellen", "Rechnen und Abfragen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Kennzahlen aus einem Dienst in eine Tabelle zu holen", "Eine kleine Auswertung ohne eigenes Skript zu bauen"], False)
add("Smartsheet", "https://www.smartsheet.com/", "smartsheet.com", "paid", "proprietary", ["daten", "produktivitaet"],
    "Smartsheet führt Tabellen, die wie Projektpläne mit Status und Daten arbeiten.",
    "Smartsheet legt Zeilen mit Verantwortlichen, Daten und Status an und kann daraus Berichte bauen. Die Nutzung richtet sich an Teams. Sie ist kostenpflichtig.",
    ["Tabellen mit Status und Verantwortlichen", "Berichte aus den Zeilen", "Kostenpflichtige Nutzung"],
    ["Einen Projektplan als Tabelle zu führen", "Den Status vieler Zeilen zu berichten"], False)
add("DuckDB", "https://duckdb.org/", "duckdb.org", "free", "open_source", ["daten", "programmierung"],
    "DuckDB fragt lokale Dateien mit SQL ab, ohne einen Server zu starten.",
    "DuckDB liest CSV, Parquet und andere Dateien und beantwortet SQL direkt auf dem Rechner. Die SPDX-Kennung ist MIT. Ein Pflichtabo gibt es nicht.",
    ["SQL auf lokalen Dateien", "Kein eigener Server nötig", "Lizenz MIT"],
    ["Eine CSV-Datei mit SQL auszuwerten", "Eine Abfrage ohne Datenbankserver zu fahren"], False,
    oss("https://github.com/duckdb/duckdb", "MIT", "https://duckdb.org/"))
add("SQLite", "https://sqlite.org/index.html", "sqlite.org", "free", "unknown", ["daten", "programmierung"],
    "SQLite speichert eine Datenbank in einer einzelnen Datei.",
    "SQLite führt SQL in einer Datei aus, die eine Anwendung mitliefern kann. Einen separaten Datenbankserver braucht es dafür nicht. Die Website beschreibt die Nutzungsbedingungen selbst. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["SQL in einer Datei", "Kein separater Server", "Nutzungsbedingungen auf der Projektwebsite"],
    ["Eine Anwendung mit einer lokalen Datenbank auszustatten", "Eine kleine Datenbankdatei abzufragen"], False)
add("Datasette", "https://datasette.io/", "datasette.io", "free", "open_source", ["daten"],
    "Datasette veröffentlicht eine SQLite-Datei als durchsuchbare Website.",
    "Datasette liest eine SQLite-Datenbank und bietet Tabellen, Filter und eine API. Die SPDX-Kennung ist Apache-2.0. Der Betrieb liegt auf dem eigenen Rechner oder Server.",
    ["Tabellen und Filter aus SQLite", "API zur selben Datei", "Lizenz Apache-2.0"],
    ["Eine Datendatei im Browser zu durchsuchen", "Eine kleine Daten-API aus SQLite zu starten"], False,
    oss("https://github.com/simonw/datasette", "Apache-2.0", "https://datasette.io/"))
add("EtherCalc", "https://ethercalc.net/", "ethercalc.net", "free", "unknown", ["daten"],
    "EtherCalc ist eine Tabelle im Browser, die mehrere Personen gleichzeitig bearbeiten.",
    "EtherCalc öffnet ein Rechenblatt unter einer Adresse, ohne ein Konto zu verlangen. Formeln rechnen im Blatt. Eine OSI-Kennung wurde hier nicht bestätigt. Die öffentliche Instanz ist ohne Abo nutzbar.",
    ["Tabelle im Browser", "Gleichzeitiges Bearbeiten", "Nutzung ohne Abo"],
    ["Eine Liste schnell mit anderen zu rechnen", "Ein Blatt ohne Konto zu teilen"], True)
add("Microsoft Excel", "https://www.microsoft.com/en-us/microsoft-365/excel", "microsoft.com", "paid", "proprietary", ["daten"],
    "Excel rechnet in Tabellenblättern mit Formeln, Diagrammen und Pivot-Auswertungen.",
    "Excel öffnet Arbeitsmappen auf dem Rechner und in Microsoft 365. Formeln, Diagramme und Pivot-Tabellen werten Zeilen aus. Die Desktop- und Cloud-Nutzung ist über Microsoft 365 kostenpflichtig.",
    ["Formeln, Diagramme und Pivot", "Arbeitsmappen lokal und in Microsoft 365", "Kostenpflichtige Nutzung"],
    ["Eine größere Tabelle mit Formeln auszuwerten", "Eine Pivot-Ansicht über viele Zeilen zu bauen"], True)
add("Pitch", "https://pitch.com/", "pitch.com", "freemium", "proprietary", ["praesentationen"],
    "Pitch baut Folien im Browser und lässt ein Team gleichzeitig daran arbeiten.",
    "Pitch legt Folien mit Vorlagen, Markenfarben und Kommentaren an. Die Präsentation bleibt im Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Folien mit Vorlagen", "Kommentare im Team", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Präsentation mit anderen zu bauen", "Folien in den Farben einer Marke anzulegen"], True)
add("Beautiful.ai", "https://www.beautiful.ai/", "beautiful.ai", "freemium", "proprietary", ["praesentationen"],
    "Beautiful.ai setzt Folien aus Inhaltsbausteinen, die das Layout mitziehen.",
    "Beautiful.ai passt Abstände und Anordnung an, wenn man Text oder ein Diagramm ergänzt. Vorlagen geben den Rahmen vor. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Folien aus Inhaltsbausteinen", "Layout passt sich dem Inhalt an", "Einstieg und bezahlte Stufen"],
    ["Eine Folie zu bauen, ohne Abstände von Hand zu setzen", "Ein Diagramm in eine bestehende Folie zu setzen"], True)
add("Slidev", "https://sli.dev/", "sli.dev", "free", "open_source", ["praesentationen", "programmierung"],
    "Slidev schreibt Folien in Markdown und zeigt sie als Webpräsentation.",
    "Slidev rendert Markdown-Dateien zu Folien mit Code-Hervorhebung. Die Präsentation läuft im Browser und bleibt im eigenen Projekt. Die SPDX-Kennung ist MIT.",
    ["Folien aus Markdown", "Code-Hervorhebung", "Lizenz MIT"],
    ["Einen Vortrag neben dem Code zu versionieren", "Folien für eine technische Demo zu schreiben"], False,
    oss("https://github.com/slidevjs/slidev", "MIT", "https://sli.dev/"))
add("reveal.js", "https://revealjs.com/", "revealjs.com", "free", "open_source", ["praesentationen"],
    "reveal.js zeigt HTML-Folien im Browser und steht unter MIT.",
    "reveal.js baut eine Präsentation aus HTML-Abschnitten und spielt sie im Browser ab. Die Dateien liegen im eigenen Projekt. Die SPDX-Kennung ist MIT.",
    ["Folien aus HTML", "Wiedergabe im Browser", "Lizenz MIT"],
    ["Eine Präsentation ohne einen Folien-Dienst zu halten", "Folien mit der eigenen Website zu stylen"], False,
    oss("https://github.com/hakimel/reveal.js", "MIT", "https://revealjs.com/"))
add("Marp", "https://marp.app/", "marp.app", "free", "open_source", ["praesentationen"],
    "Marp macht aus Markdown Folien und exportiert sie als PDF oder HTML.",
    "Marp trennt Folien im Markdown mit Trennlinien und exportiert das Ergebnis. Die Arbeit bleibt in einer Textdatei. Die SPDX-Kennung des genannten Repositories ist MIT.",
    ["Folien aus Markdown", "Export als PDF oder HTML", "Lizenz MIT"],
    ["Einen Vortrag in einer Textdatei zu schreiben", "Folien als PDF zu exportieren"], False,
    oss("https://github.com/marp-team/marp", "MIT", "https://marp.app/"))
add("SketchUp", "https://www.sketchup.com/", "sketchup.com", "freemium", "proprietary", ["dreid", "design"],
    "SketchUp modelliert Räume und Körper aus Flächen und Kanten.",
    "SketchUp zieht Wände, Möbel und einfache Körper im dreidimensionalen Raum. Eine Fassung für den Browser und Desktop-Ausgaben teilen sich das Modell. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Modelle aus Flächen und Kanten", "Browser und Desktop", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Raum grob zu modellieren", "Ein einfaches Möbelstück in 3D zu zeichnen"], True)
add("Tinkercad", "https://www.tinkercad.com/", "tinkercad.com", "free", "proprietary", ["dreid", "bildung"],
    "Tinkercad baut einfache 3D-Modelle im Browser aus Grundformen.",
    "Tinkercad setzt Quader, Zylinder und andere Formen zusammen und exportiert sie für den Druck oder für weitere Programme. Ein Konto ist nötig. Die Modellierung im Browser ist ohne Abo nutzbar.",
    ["3D aus Grundformen", "Export für den Druck", "Nutzung ohne Abo"],
    ["Ein erstes 3D-Modell im Unterricht zu bauen", "Eine einfache Form für den Druck zu exportieren"], True)
add("Meshy", "https://www.meshy.ai/", "meshy.ai", "freemium", "proprietary", ["dreid", "bildgenerierung"],
    "Meshy erzeugt 3D-Modelle aus Text oder einem Bild.",
    "Meshy liefert ein dreidimensionales Modell zu einer Beschreibung oder einer Vorlage und erlaubt weitere Bearbeitung. Die Datei lässt sich exportieren. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["3D aus Text oder Bild", "Export des Modells", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein Spielfigur-Modell aus einer Beschreibung zu starten", "Ein Bild in ein einfaches 3D-Objekt zu überführen"], False)
add("FreeCAD", "https://www.freecad.org/", "freecad.org", "free", "open_source", ["dreid"],
    "FreeCAD konstruiert parametrische 3D-Modelle auf dem eigenen Rechner.",
    "FreeCAD zeichnet Bauteile mit Maßen, die sich nachträglich ändern lassen, und exportiert sie für Fertigung oder Druck. Die SPDX-Kennung ist LGPL-2.1. Die Software ist ohne Pflichtabo nutzbar.",
    ["Parametrische Bauteile", "Export für Fertigung und Druck", "Lizenz LGPL-2.1"],
    ["Ein Bauteil mit änderbaren Maßen zu zeichnen", "Ein Modell für den 3D-Druck zu exportieren"], False,
    oss("https://github.com/FreeCAD/FreeCAD", "LGPL-2.1", "https://www.freecad.org/"))
add("OpenSCAD", "https://openscad.org/", "openscad.org", "free", "unknown", ["dreid", "programmierung"],
    "OpenSCAD beschreibt 3D-Modelle als Skript statt als Zeichnung.",
    "OpenSCAD baut Körper aus Programmzeilen und rendert daraus ein Modell. Maße stehen als Variablen im Skript. Eine OSI-Kennung wurde hier nicht bestätigt. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["3D aus einem Skript", "Maße als Variablen", "Betrieb ohne Pflichtabo"],
    ["Ein parametrisches Teil als Code zu beschreiben", "Ein Modell aus Maßen erneut zu rendern"], False)
add("Sweet Home 3D", "https://www.sweethome3d.com/", "sweethome3d.com", "free", "unknown", ["dreid", "design"],
    "Sweet Home 3D zeichnet Grundrisse und zeigt sie als begehbare Räume.",
    "Sweet Home 3D legt Wände, Möbel und Öffnungen auf einen Grundriss und erzeugt dazu eine 3D-Ansicht. Die Datei bleibt lokal. Eine OSI-Kennung wurde hier nicht bestätigt. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Grundriss mit Möbeln", "3D-Ansicht des Raums", "Betrieb ohne Pflichtabo"],
    ["Eine Wohnung grob einzurichten", "Einen Grundriss mit Möbelmaßen zu prüfen"], True)
add("Polycam", "https://poly.cam/", "poly.cam", "freemium", "proprietary", ["dreid"],
    "Polycam scannt Räume und Gegenstände mit dem Handy zu einem 3D-Modell.",
    "Polycam nimmt Fotos oder einen Lidar-Scan und rechnet daraus ein Modell oder eine Punktwolke. Der Export hängt von der Stufe ab. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Scan von Räumen und Gegenständen", "Modell oder Punktwolke", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Raum mit dem Handy zu erfassen", "Einen Gegenstand als 3D-Modell zu sichern"], True)
add("Godot", "https://godotengine.org/", "godotengine.org", "free", "open_source", ["gaming"],
    "Godot ist eine Spiel-Engine für 2D und 3D unter der MIT-Lizenz.",
    "Godot bringt Editor, Szenen und Skripte mit, um ein Spiel zu bauen und zu exportieren. Die SPDX-Kennung ist MIT. Eine Lizenzgebühr an die Engine gibt es nicht.",
    ["Editor für 2D und 3D", "Export des Spiels", "Lizenz MIT"],
    ["Ein kleines Spiel ohne Engine-Gebühr zu bauen", "Eine Szene mit Skripten zu testen"], False,
    oss("https://github.com/godotengine/godot", "MIT", "https://godotengine.org/"))
add("Unity", "https://unity.com/", "unity.com", "freemium", "proprietary", ["gaming"],
    "Unity ist eine Spiel- und 3D-Engine mit Editor, Assets und Export.",
    "Unity baut Szenen, Physik und Oberflächen im Editor und exportiert sie auf mehrere Plattformen. Für kleinere Umsätze gibt es einen kostenlosen Einstieg, darüber liegen bezahlte Pläne.",
    ["Szenen, Physik und Export", "Mehrere Zielplattformen", "Kostenloser Einstieg und bezahlte Pläne"],
    ["Einen Prototyp eines Spiels zu bauen", "Eine 3D-Szene auf eine Plattform zu exportieren"], False)
add("LÖVE", "https://love2d.org/", "love2d.org", "free", "unknown", ["gaming", "programmierung"],
    "LÖVE führt 2D-Spiele aus, die in Lua geschrieben sind.",
    "LÖVE ist eine Laufzeitumgebung: Spielcode in Lua zeichnet, spielt Ton und liest Eingaben. Eine OSI-Kennung wurde hier nicht bestätigt. Die Engine ist ohne Pflichtabo erhältlich.",
    ["2D-Spiele in Lua", "Zeichnen, Ton und Eingabe", "Betrieb ohne Pflichtabo"],
    ["Ein kleines 2D-Spiel in Lua zu schreiben", "Einen Prototyp ohne große Engine zu starten"], False)
add("Ren'Py", "https://www.renpy.org/", "renpy.org", "free", "unknown", ["gaming"],
    "Ren'Py baut visuelle Romane mit Text, Bildern und Entscheidungen.",
    "Ren'Py schreibt Dialoge als Skript und zeigt sie mit Hintergründen und Auswahlmöglichkeiten. Das Spiel lässt sich als Anwendung exportieren. Eine OSI-Kennung wurde hier nicht bestätigt. Die Engine ist ohne Pflichtabo erhältlich.",
    ["Dialoge als Skript", "Bilder und Entscheidungen", "Export als Anwendung"],
    ["Eine visuelle Geschichte zu schreiben", "Eine Entscheidung in einem Dialog anzubieten"], True)
add("GDevelop", "https://gdevelop.io/", "gdevelop.io", "freemium", "unknown", ["gaming", "bildung"],
    "GDevelop baut 2D-Spiele aus Ereignissen, ohne dass jede Zeile Code sein muss.",
    "GDevelop setzt Szenen, Objekte und Wenn-dann-Ereignisse im Editor zusammen und exportiert das Spiel. Eine OSI-Kennung wurde hier nicht bestätigt. Es gibt einen kostenlosen Einstieg und bezahlte Angebote.",
    ["Szenen und Ereignisse", "Export des Spiels", "Kostenloser Einstieg und bezahlte Angebote"],
    ["Ein erstes 2D-Spiel ohne viel Code zu bauen", "Eine Spielidee im Unterricht auszuprobieren"], True)
add("Aseprite", "https://www.aseprite.org/", "aseprite.org", "paid", "proprietary", ["gaming", "design"],
    "Aseprite zeichnet Pixelgrafik und Animationen für Spiele.",
    "Aseprite arbeitet mit Ebenen, Paletten und Einzelbildern einer Animation. Der Export zielt auf Spiele-Grafik. Die Anwendung ist kostenpflichtig. Der Quelltext ist nicht als OSI-Open-Source eingeordnet.",
    ["Pixelgrafik und Animation", "Ebenen und Paletten", "Kostenpflichtige Anwendung"],
    ["Ein Sprite für ein Spiel zu zeichnen", "Eine kurze Pixelanimation zu exportieren"], False)
add("itch.io", "https://itch.io/", "itch.io", "free", "proprietary", ["gaming"],
    "itch.io veröffentlicht und lädt unabhängige Spiele, Werkzeuge und Assets.",
    "itch.io ist ein Marktplatz und eine Bibliothek für unabhängige Spiele. Entwicklerinnen und Entwickler legen eine Seite an, Spielende laden oder spielen im Browser. Das Anlegen einer Seite ist ohne Monatsabo möglich, Verkäufe haben eigene Konditionen.",
    ["Seiten für unabhängige Spiele", "Download und Browser-Spiel", "Seiten ohne Monatsabo, Verkäufe mit eigenen Konditionen"],
    ["Ein eigenes Spiel zu veröffentlichen", "Unabhängige Spiele zu finden und zu laden"], True)
add("Inworld", "https://www.inworld.ai/", "inworld.ai", "freemium", "proprietary", ["gaming", "ki-chatbots"],
    "Inworld baut Spielfiguren, die im Dialog auf Spielende reagieren.",
    "Inworld beschreibt eine Figur mit Wissen und Persönlichkeit und bindet den Dialog in ein Spiel ein. Die Nutzung läuft über ein Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Figuren mit Wissen und Persönlichkeit", "Dialog für Spiele", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen NPC mit eigenem Dialog zu entwerfen", "Eine Figur in einem Prototyp sprechen zu lassen"], False)
add("Convai", "https://convai.com/", "convai.com", "freemium", "proprietary", ["gaming", "ki-chatbots"],
    "Convai lässt Spielfiguren sprechen und auf Fragen im Spiel reagieren.",
    "Convai verbindet eine Figur mit Sprache und Wissen und liefert den Dialog an eine Spiel-Engine. Die Einrichtung bleibt im Konto. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Sprechende Spielfiguren", "Anbindung an eine Engine", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Charakter im Spiel antworten zu lassen", "Einen Dialogprototyp an eine Engine zu hängen"], False)
add("Have I Been Pwned", "https://haveibeenpwned.com/", "haveibeenpwned.com", "free", "proprietary", ["recherche"],
    "Have I Been Pwned prüft, ob eine E-Mail-Adresse in bekannten Datenlecks auftaucht.",
    "Have I Been Pwned sucht eine Adresse in veröffentlichten Leak-Daten und zeigt, in welchen Vorfällen sie vorkam. Die einzelne Suche ist ohne Abo möglich. Die Seite speichert dafür kein eigenes Passwort.",
    ["Suche einer E-Mail in Leak-Daten", "Anzeige der betroffenen Vorfälle", "Suche ohne Abo"],
    ["Zu prüfen, ob eine Adresse in einem Leak stand", "Einen Vorfall zu einer eigenen Adresse nachzulesen"], True)
add("SSL Labs", "https://www.ssllabs.com/ssltest/", "ssllabs.com", "free", "proprietary", ["programmierung"],
    "SSL Labs prüft die TLS-Konfiguration einer öffentlichen Website.",
    "Der SSL Server Test verbindet sich mit einem Host und bewertet Protokolle, Zertifikat und bekannte Schwächen. Der Bericht ist ohne Konto abrufbar. Eine OSI-Lizenz der Website ist nicht hinterlegt, der Dienst ist proprietär eingeordnet.",
    ["Prüfung von Zertifikat und Protokollen", "Bericht ohne Konto", "Öffentlicher Test"],
    ["Die TLS-Einstellung einer eigenen Website zu prüfen", "Ein Zertifikatsproblem zu sehen"], False)
add("PageSpeed Insights", "https://pagespeed.web.dev/", "pagespeed.web.dev", "free", "proprietary", ["seo", "programmierung"],
    "PageSpeed Insights misst Ladezeit und Hinweise einer öffentlichen Seite.",
    "PageSpeed Insights lädt eine URL und zeigt Messwerte plus konkrete Hinweise für Mobil und Desktop. Die Abfrage ist ohne Abo möglich.",
    ["Messwerte für Mobil und Desktop", "Konkrete Hinweise zur Seite", "Abfrage ohne Abo"],
    ["Die Ladezeit einer URL zu messen", "Hinweise zu Bildern und Skripten zu lesen"], True)
add("Can I use", "https://caniuse.com/", "caniuse.com", "free", "unknown", ["programmierung"],
    "Can I use zeigt, welche Browser eine Webfunktion unterstützen.",
    "Can I use listet eine CSS- oder HTML-Funktion und färbt die Browserversionen nach Unterstützung. Die Tabelle ist ohne Konto lesbar. Eine OSI-Lizenz der Website ist hier nicht hinterlegt.",
    ["Unterstützung je Browserversion", "Suche nach Webfunktionen", "Nutzung ohne Konto"],
    ["Vor dem Einsatz einer CSS-Funktion die Browser zu prüfen", "Eine ältere Browserversion einzuordnen"], True)
add("Coolors", "https://coolors.co/", "coolors.co", "freemium", "proprietary", ["design"],
    "Coolors erzeugt Farbpaletten und sperrt einzelne Töne fest.",
    "Coolors würfelt eine Palette und lässt einzelne Farben stehen, während der Rest neu gemischt wird. Paletten lassen sich speichern. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Paletten erzeugen und sperren", "Speichern der Farben", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Farbpalette für eine Seite zu finden", "Einen Ton festzuhalten und den Rest neu zu mischen"], True)
add("Google Fonts", "https://fonts.google.com/", "fonts.google.com", "free", "proprietary", ["design"],
    "Google Fonts stellt Schriftfamilien zum Einbinden in Websites bereit.",
    "Google Fonts zeigt Schriften mit Beispieltext und liefert einen Einbindungs-Ausschnitt für eine Website. Die Nutzung der Bibliothek ist ohne Abo möglich. Die Schriften haben eigene Lizenzen, die auf der jeweiligen Familie stehen.",
    ["Schriftfamilien mit Beispieltext", "Einbindung in eine Website", "Nutzung ohne Abo"],
    ["Eine Schrift für eine Website zu wählen", "Den Einbindungs-Ausschnitt zu kopieren"], True)
add("QR Code Generator", "https://www.qr-code-generator.com/", "qr-code-generator.com", "freemium", "proprietary", ["produktivitaet"],
    "QR Code Generator macht aus einem Text oder einer URL einen QR-Code.",
    "Die Seite erzeugt einen QR-Code aus einer Adresse oder einem kurzen Text und zeigt ihn zum Download. Erweiterte Gestaltung und dynamische Codes liegen in bezahlten Stufen. Ein einfacher Code ist ohne Abo möglich.",
    ["QR-Code aus URL oder Text", "Download des Codes", "Einfacher Code ohne Abo, Gestaltung bezahlt"],
    ["Einen QR-Code für eine Website zu erzeugen", "Einen Code auf einen Aushang zu setzen"], True)
add("SVGOMG", "https://svgomg.net/", "svgomg.net", "free", "open_source", ["design"],
    "SVGOMG verkleinert SVG-Dateien im Browser.",
    "SVGOMG nimmt eine SVG-Datei und entfernt überflüssige Angaben, ohne das Bild bewusst zu ändern. Die Bearbeitung läuft lokal im Browser. Die SPDX-Kennung des Repositories ist MIT.",
    ["SVG verkleinern", "Bearbeitung im Browser", "Lizenz MIT"],
    ["Ein Icon vor dem Einbau zu verkleinern", "Eine exportierte SVG-Datei zu bereinigen"], True,
    oss("https://github.com/jakearchibald/svgomg", "MIT", "https://svgomg.net/"))
add("Smallpdf", "https://smallpdf.com/", "smallpdf.com", "freemium", "proprietary", ["produktivitaet"],
    "Smallpdf komprimiert, verbindet und wandelt PDF-Dateien im Browser.",
    "Smallpdf bietet einzelne Werkzeuge für PDF, etwa Komprimieren, Zusammenführen und Umwandeln. Die Datei wird auf den Dienst geladen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Komprimieren und Zusammenführen", "Formatumwandlung", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Ein PDF kleiner zu machen", "Mehrere PDFs zu einer Datei zu verbinden"], True)
add("PDF24", "https://www.pdf24.org/de/", "pdf24.org", "free", "proprietary", ["produktivitaet"],
    "PDF24 bietet viele PDF-Werkzeuge im Browser und als Desktop-Programm.",
    "PDF24 Tools fügt Dateien zusammen, teilt sie, komprimiert sie und wandelt Formate. Ein großer Teil der Browser-Werkzeuge ist ohne Abo nutzbar. Die Anwendung ist proprietär.",
    ["Zusammenführen, Teilen und Komprimieren", "Browser und Desktop", "Browser-Werkzeuge ohne Abo"],
    ["Mehrere PDFs zu verbinden", "Eine Datei in PDF umzuwandeln"], True)
add("Sejda", "https://www.sejda.com/", "sejda.com", "freemium", "proprietary", ["produktivitaet"],
    "Sejda bearbeitet PDF-Dateien: zusammenfügen, teilen, Text ändern.",
    "Sejda öffnet ein PDF im Browser und bietet Werkzeuge zum Zusammenfügen, Teilen und Bearbeiten. Kostenlose Vorgänge sind begrenzt, darüber liegen bezahlte Stufen.",
    ["PDF zusammenfügen und teilen", "Text im Dokument bearbeiten", "Begrenzte kostenlose Vorgänge und bezahlte Stufen"],
    ["Seiten aus einem PDF zu lösen", "Einen Tippfehler in einem PDF zu ändern"], True)
add("WAVE Evaluation Tool", "https://wave.webaim.org/", "wave.webaim.org", "free", "unknown", ["programmierung"],
    "WAVE prüft eine Webseite auf erkennbare Barrieren.",
    "WAVE lädt eine öffentliche Adresse und markiert Fehler und Warnungen zur Zugänglichkeit direkt auf der Seite. Die einzelne Prüfung ist ohne Konto möglich. Eine OSI-Lizenz der Website ist hier nicht hinterlegt.",
    ["Prüfung einer öffentlichen URL", "Fehler und Warnungen auf der Seite", "Prüfung ohne Konto"],
    ["Eine Seite auf fehlende Alternativtexte zu prüfen", "Kontrast- und Strukturhinweise zu sehen"], True)
add("crontab.guru", "https://crontab.guru/", "crontab.guru", "free", "unknown", ["programmierung"],
    "crontab.guru übersetzt einen Cron-Ausdruck in eine lesbare Zeitangabe.",
    "Man tippt fünf Felder eines Cron-Ausdrucks und sieht, wann der Job laufen würde. Die Seite rechnet im Browser. Eine OSI-Lizenz ist hier nicht hinterlegt. Die Nutzung ist ohne Abo möglich.",
    ["Cron-Ausdruck in Klartext", "Rechnung im Browser", "Nutzung ohne Abo"],
    ["Einen Cron-Job zu verstehen, bevor er auf den Server kommt", "Einen Zeitplan für einen wiederkehrenden Lauf zu bauen"], True)
add("Bundlephobia", "https://bundlephobia.com/", "bundlephobia.com", "free", "unknown", ["programmierung"],
    "Bundlephobia zeigt, wie groß ein npm-Paket im Bundle wird.",
    "Bundlephobia sucht ein Paket und nennt die übertragene Größe samt Abhängigkeiten. Die Abfrage ist ohne Konto möglich. Eine OSI-Lizenz der Website ist hier nicht hinterlegt.",
    ["Größe eines npm-Pakets", "Abhängigkeiten in der Summe", "Abfrage ohne Konto"],
    ["Ein Paket vor dem Einbau auf die Größe zu prüfen", "Zwei Bibliotheken der Größe nach zu vergleichen"], True)
add("Cleanup.pictures", "https://cleanup.pictures/", "cleanup.pictures", "freemium", "proprietary", ["bildgenerierung", "design"],
    "Cleanup.pictures entfernt störende Objekte aus einem Foto im Browser.",
    "Man markiert einen Bereich im Bild, und die Seite füllt ihn mit der Umgebung. Die Vorschau erscheint im Browser. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Objekte aus Fotos entfernen", "Vorschau im Browser", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Person oder ein Schild aus einem Foto zu nehmen", "Einen Hintergrund zu bereinigen"], True)


def validate(entries: list[dict]) -> None:
    seen = set()
    errors = []
    allowed = {"free", "freemium", "paid"}
    licenses = {"open_source", "proprietary", "unknown"}
    for entry in entries:
        if entry["domain"] in seen:
            errors.append(f"Domain {entry['domain']} {entry['name']}")
        seen.add(entry["domain"])
        if not (10 <= len(entry["shortDescriptionDe"]) <= 280):
            errors.append(f"Kurztext {entry['name']} {len(entry['shortDescriptionDe'])}")
        if "zzgl" in (entry["shortDescriptionDe"] + entry["longDescriptionDe"]).lower():
            errors.append(f"USt {entry['name']}")
        if entry["pricingModel"] not in allowed or entry["licenseType"] not in licenses:
            errors.append(f"Feld {entry['name']}")
        if entry["licenseType"] == "open_source" and not (entry["oss"] and entry["oss"]["license"]):
            errors.append(f"OSS {entry['name']}")
        if entry["licenseType"] != "open_source" and entry["oss"] is not None:
            errors.append(f"OSS-Block {entry['name']}")
        if entry.get("programPresence") == "yes" and not str(entry.get("programInfoUrl", "")).startswith("https://"):
            errors.append(f"Programm-URL {entry['name']}")
        if entry.get("programInfoUrl") and entry.get("partnerStatus") != "found":
            errors.append(f"Status {entry['name']}")
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    validate(E)
    out = ROOT / "data" / "verified-tools-batch3.json"
    out.write_text(json.dumps(E, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(E), "->", out)

