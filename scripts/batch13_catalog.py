#!/usr/bin/env python3
"""Dreizehnte Liste: nur Software, Web-Apps und Entwicklerwerkzeuge."""

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


add("Go", "https://go.dev/", "go.dev", "free", "unknown", ["programmierung"],
    "Go ist eine Programmiersprache für Dienste und Werkzeuge auf dem Server.",
    "go.dev stellt Compiler, Module und die Dokumentation bereit. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Werkzeuge sind ohne Pflichtabo erhältlich.",
    ["Compiler und Module", "Dokumentation", "Nutzung ohne Pflichtabo"],
    ["Einen Dienst in Go zu schreiben", "Ein Modul zu beziehen"], False)
add("TypeScript", "https://www.typescriptlang.org/", "typescriptlang.org", "free", "unknown", ["programmierung"],
    "TypeScript ergänzt JavaScript um Typen und übersetzt in gewöhnliches JavaScript.",
    "Die Seite stellt den Compiler und das Handbuch bereit. Eine OSI-Kennung wird hier nicht erneut eingetragen. Der Compiler ist ohne Pflichtabo erhältlich.",
    ["Typen für JavaScript", "Compiler und Handbuch", "Nutzung ohne Pflichtabo"],
    ["Einen Typfehler vor dem Lauf zu sehen", "JavaScript aus TypeScript zu erzeugen"], False)
add("PostgreSQL", "https://www.postgresql.org/", "postgresql.org", "free", "unknown", ["daten", "programmierung"],
    "PostgreSQL ist ein relationaler Datenbankserver.",
    "PostgreSQL speichert Tabellen und beantwortet SQL. Eine OSI-Kennung wird hier nicht erneut eingetragen. Der Server ist ohne Pflichtabo nutzbar.",
    ["Relationale Tabellen", "SQL", "Nutzung ohne Pflichtabo"],
    ["Eine Anwendungsdatenbank selbst zu betreiben", "SQL auf dem eigenen Server auszuführen"], False)
add("Kubernetes", "https://kubernetes.io/", "kubernetes.io", "free", "unknown", ["programmierung"],
    "Kubernetes verteilt Container auf mehrere Rechner und startet sie neu, wenn einer ausfällt.",
    "Die Dokumentation beschreibt Cluster, Deployments und Dienste. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Container auf mehreren Rechnern", "Neustart bei Ausfall", "Nutzung ohne Pflichtabo"],
    ["Eine Anwendung auf mehrere Rechner zu verteilen", "Einen Dienst im Cluster zu beschreiben"], False)
add("Portainer", "https://www.portainer.io/", "portainer.io", "freemium", "unknown", ["programmierung"],
    "Portainer verwaltet Container über eine Weboberfläche.",
    "Portainer zeigt laufende Container und startet Stacks. Es gibt eine Community-Ausgabe und bezahlte Business-Funktionen. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Weboberfläche für Container", "Community-Ausgabe", "Bezahlte Business-Funktionen"],
    ["Container ohne nur die Kommandozeile zu starten", "Einen Stack zu überblicken"], False)
add("Elastic", "https://www.elastic.co/", "elastic.co", "freemium", "unknown", ["daten", "programmierung"],
    "Elasticsearch speichert und durchsucht große Mengen von Dokumenten und Logs.",
    "Elastic bietet Suche, Logs und Observability. Eine OSI-Kennung der aktuellen Ausgabe wird hier nicht eingetragen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Suche über Dokumente", "Logs", "Einstieg und bezahlte Stufen"],
    ["Logs einer Anwendung zu durchsuchen", "Einen Suchindex aufzubauen"], False)
add("SigNoz", "https://signoz.io/", "signoz.io", "freemium", "unknown", ["programmierung"],
    "SigNoz zeigt Traces, Metriken und Logs und lässt sich selbst betreiben.",
    "SigNoz sammelt Telemetrie einer Anwendung. Eine OSI-Kennung wird hier nicht erneut eingetragen. Es gibt den Selbstbetrieb und eine Cloud.",
    ["Traces, Metriken und Logs", "Selbstbetrieb und Cloud", "Lizenz nicht erneut eingetragen"],
    ["Eine langsame Anfrage zu verfolgen", "Die Telemetrie selbst zu hosten"], False)
add("ownCloud", "https://owncloud.com/", "owncloud.com", "freemium", "unknown", ["produktivitaet"],
    "ownCloud synchronisiert Dateien und lässt sich auf dem eigenen Server betreiben.",
    "ownCloud legt Ordner ab und teilt sie im Team. Es gibt eine selbst betreibbare Ausgabe und eine gehostete Fassung. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Dateiabgleich", "Selbstbetrieb und Hosting", "Lizenz nicht eingetragen"],
    ["Dateien eines Teams selbst zu hosten", "Einen Ordner freizugeben"], False)
add("Collabora Online", "https://www.collaboraoffice.com/", "collaboraoffice.com", "freemium", "unknown", ["produktivitaet"],
    "Collabora Online bearbeitet Textdokumente, Tabellen und Folien im Browser.",
    "Collabora setzt auf LibreOffice und lässt sich an eine eigene Cloud hängen. Es gibt eine Community-Ausgabe und bezahlte Angebote. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Dokumente im Browser", "Anbindung an eine eigene Cloud", "Community-Ausgabe und bezahlte Angebote"],
    ["Eine Datei im Browser zu bearbeiten", "Office an den eigenen Server zu hängen"], False)
add("FileZilla", "https://www.filezilla-project.org/", "filezilla-project.org", "free", "unknown", ["programmierung"],
    "FileZilla überträgt Dateien per FTP und SFTP.",
    "FileZilla Client verbindet sich mit einem Server und kopiert Dateien. Eine OSI-Kennung wird hier nicht erneut eingetragen. Der Client ist ohne Pflichtabo erhältlich.",
    ["FTP und SFTP", "Dateiübertragung", "Nutzung ohne Pflichtabo"],
    ["Eine Website auf den Server zu kopieren", "Dateien per SFTP zu holen"], True)
add("KeePass", "https://www.keepass.info/", "keepass.info", "free", "unknown", ["programmierung"],
    "KeePass speichert Passwörter in einer verschlüsselten Datei.",
    "KeePass legt Einträge lokal ab und öffnet sie mit einem Hauptschlüssel. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Verschlüsselte Passwortdatei", "Lokale Speicherung", "Nutzung ohne Pflichtabo"],
    ["Passwörter in einer Datei zu halten", "Einen Eintrag mit dem Hauptschlüssel zu öffnen"], True)
add("Magic Earth", "https://www.magic.earth/", "magic.earth", "freemium", "proprietary", ["reisen"],
    "Magic Earth navigiert offline mit Karten und zeigt Verkehr, wo eine Verbindung da ist.",
    "Die App führt zu einem Ziel und kann Karten vorausladen. Es gibt einen kostenlosen Einstieg und bezahlte Funktionen.",
    ["Navigation", "Karten zum Vorausladen", "Kostenloser Einstieg und bezahlte Funktionen"],
    ["Eine Route ohne ständige Verbindung zu fahren", "Ein Ziel in der App zu setzen"], True)
add("OpenLayers", "https://openlayers.org/", "openlayers.org", "free", "unknown", ["programmierung", "reisen"],
    "OpenLayers zeichnet Karten im Browser.",
    "OpenLayers legt Kacheln, Vektoren und Markierungen auf eine Seite. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Bibliothek ist ohne Pflichtabo erhältlich.",
    ["Karten im Browser", "Kacheln und Vektoren", "Nutzung ohne Pflichtabo"],
    ["Eine Karte in eine Website einzubauen", "Eine Markierung zu setzen"], False)
add("deck.gl", "https://deck.gl/", "deck.gl", "free", "unknown", ["daten", "programmierung"],
    "deck.gl zeichnet große Mengen von Punkten und Wegen als WebGL-Karte.",
    "deck.gl legt Ebenen über eine Grundkarte. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Bibliothek ist ohne Pflichtabo erhältlich.",
    ["WebGL-Karten", "Ebenen für Punkte und Wege", "Nutzung ohne Pflichtabo"],
    ["Viele Standorte auf einmal zu zeichnen", "Eine Datenebene über eine Karte zu legen"], False)
add("mapshaper", "https://mapshaper.org/", "mapshaper.org", "free", "unknown", ["daten"],
    "mapshaper vereinfacht und wandelt Geodaten im Browser.",
    "mapshaper öffnet Shapefiles und GeoJSON und kann sie verkleinern. Die Nutzung im Browser ist ohne Konto möglich. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Vereinfachen von Geodaten", "Shapefile und GeoJSON", "Nutzung ohne Konto"],
    ["Eine Karte fürs Web zu verkleinern", "Ein Format in ein anderes zu wandeln"], False)
add("Marble", "https://marble.kde.org/", "marble.kde.org", "free", "unknown", ["reisen"],
    "Marble ist ein virtueller Globus für den Desktop.",
    "Marble zeigt Erde und weitere Karten offline, soweit die Daten geladen sind. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Virtueller Globus", "Desktop-Anwendung", "Nutzung ohne Pflichtabo"],
    ["Einen Ort auf dem Globus zu suchen", "Eine Karte ohne Browser zu öffnen"], True)
add("uMap", "https://umap.openstreetmap.fr/", "umap.openstreetmap.fr", "free", "unknown", ["reisen", "daten"],
    "uMap zeichnet eigene Karten auf OpenStreetMap und teilt sie per Link.",
    "uMap setzt Markierungen und Flächen und bettet die Karte ein. Die Nutzung ist ohne Abo möglich. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Eigene Karten", "Markierungen und Einbettung", "Nutzung ohne Abo"],
    ["Eine Karte mit Orten zu teilen", "Eine Fläche einzuzeichnen"], True)
add("MkDocs", "https://www.mkdocs.org/", "mkdocs.org", "free", "unknown", ["programmierung"],
    "MkDocs baut eine Dokumentationswebsite aus Markdown.",
    "MkDocs erzeugt statische Seiten mit Navigation. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Dokumentation aus Markdown", "Statische Seiten", "Nutzung ohne Pflichtabo"],
    ["Eine Projektdoku zu erzeugen", "Markdown in eine Website zu bauen"], False)
add("VitePress", "https://vitepress.dev/", "vitepress.dev", "free", "unknown", ["programmierung"],
    "VitePress baut Dokumentationsseiten mit Vite aus Markdown.",
    "VitePress erzeugt eine schnelle statische Doku. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Dokumentation mit Vite", "Markdown", "Nutzung ohne Pflichtabo"],
    ["Eine Dokumentation zu veröffentlichen", "Eine Seite lokal vorzuschauen"], False)
add("Sphinx", "https://www.sphinx-doc.org/", "sphinx-doc.org", "free", "unknown", ["programmierung"],
    "Sphinx erzeugt Dokumentation, besonders für Python-Projekte.",
    "Sphinx baut aus reStructuredText oder Markdown HTML und PDF. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Dokumentation als HTML und PDF", "Python-Projekte", "Nutzung ohne Pflichtabo"],
    ["Eine API-Dokumentation zu bauen", "Ein Handbuch zu erzeugen"], False)
add("TiddlyWiki", "https://tiddlywiki.com/", "tiddlywiki.com", "free", "unknown", ["produktivitaet"],
    "TiddlyWiki hält Notizen in einer einzigen HTML-Datei.",
    "TiddlyWiki speichert kurze Einträge, die sich gegenseitig verlinken. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Anwendung ist ohne Pflichtabo erhältlich.",
    ["Notizen in einer HTML-Datei", "Verlinkte Einträge", "Nutzung ohne Pflichtabo"],
    ["Ein Notizbuch als eine Datei zu führen", "Einträge miteinander zu verlinken"], True)
add("HedgeDoc fehlt", "https://hedgedoc.org/", "hedgedoc.org", "free", "unknown", ["produktivitaet"],
    "Platzhalter.", "Platzhalter.", ["x"], ["x"])
add("BorgBackup", "https://www.borgbackup.org/", "borgbackup.org", "free", "unknown", ["programmierung"],
    "BorgBackup sichert Verzeichnisse dedupliziert und verschlüsselt.",
    "Borg speichert nur geänderte Blöcke und kann einzelne Dateien zurückspielen. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Deduplizierte Sicherungen", "Verschlüsselung", "Nutzung ohne Pflichtabo"],
    ["Ein Verzeichnis regelmäßig zu sichern", "Eine einzelne Datei zurückzuholen"], False)
add("restic", "https://restic.net/", "restic.net", "free", "unknown", ["programmierung"],
    "restic sichert Dateien verschlüsselt auf ein Ziel eigener Wahl.",
    "restic legt Schnappschüsse an und spielt sie zurück. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Verschlüsselte Schnappschüsse", "Viele Speicherziele", "Nutzung ohne Pflichtabo"],
    ["Ein Backup auf einen eigenen Speicher zu legen", "Einen Schnappschuss zurückzuspielen"], False)
add("Cloudron", "https://www.cloudron.io/", "cloudron.io", "freemium", "proprietary", ["programmierung"],
    "Cloudron installiert Webanwendungen auf dem eigenen Server über eine Oberfläche.",
    "Cloudron richtet Apps, Updates und Mail ein. Es gibt einen kostenlosen Umfang und bezahlte Pläne.",
    ["Apps auf dem eigenen Server", "Updates über die Oberfläche", "Kostenloser Umfang und bezahlte Pläne"],
    ["Mehrere Webapps ohne einzelne Einrichtung zu starten", "Updates zentral zu spielen"], False)
add("Magit", "https://magit.vc/", "magit.vc", "free", "unknown", ["programmierung"],
    "Magit bedient Git aus Emacs.",
    "Magit zeigt Status, Diffs und Commits in Emacs. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Paket ist ohne Pflichtabo erhältlich.",
    ["Git in Emacs", "Status, Diff und Commit", "Nutzung ohne Pflichtabo"],
    ["Änderungen in Emacs zu committen", "Einen Diff zu lesen"], False)
add("micro", "https://micro-editor.github.io/", "micro-editor.github.io", "free", "unknown", ["programmierung"],
    "micro ist ein Terminal-Editor, der sich mit der Maus und üblichen Tasten bedienen lässt.",
    "micro öffnet Textdateien im Terminal und hebt Syntax hervor. Eine OSI-Kennung wird hier nicht eingetragen. Der Editor ist ohne Pflichtabo erhältlich.",
    ["Editor im Terminal", "Syntax-Hervorhebung", "Nutzung ohne Pflichtabo"],
    ["Eine Datei auf einem Server zu bearbeiten", "Einen Text ohne vim-Befehle zu ändern"], True)
add("Poetry", "https://python-poetry.org/", "python-poetry.org", "free", "unknown", ["programmierung"],
    "Poetry verwaltet Abhängigkeiten und Pakete eines Python-Projekts.",
    "Poetry legt eine Lock-Datei an und installiert die genannten Versionen. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Abhängigkeiten für Python", "Lock-Datei", "Nutzung ohne Pflichtabo"],
    ["Die Pakete eines Projekts festzuschreiben", "Eine Bibliothek zu veröffentlichen"], False)
add("uv", "https://docs.astral.sh/uv/", "docs.astral.sh", "free", "unknown", ["programmierung"],
    "uv installiert Python-Pakete und legt Umgebungen an.",
    "uv ersetzt mehrere Werkzeuge rund um pip durch ein Programm. Eine OSI-Kennung wird hier nicht erneut eingetragen. Das Werkzeug ist ohne Pflichtabo erhältlich.",
    ["Schnelle Paketinstallation", "Umgebungen", "Nutzung ohne Pflichtabo"],
    ["Abhängigkeiten eines Python-Projekts zu installieren", "Eine Umgebung anzulegen"], False)
add("Astral", "https://astral.sh/", "astral.sh", "free", "unknown", ["programmierung"],
    "Astral entwickelt uv und den Linter Ruff für Python.",
    "Die Seite stellt die Werkzeuge vor. Ruff prüft Python-Code, uv installiert Pakete. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Werkzeuge sind ohne Pflichtabo erhältlich.",
    ["Ruff und uv", "Python-Werkzeuge", "Nutzung ohne Pflichtabo"],
    ["Den Linter und den Installer einzuordnen", "Zur Dokumentation zu wechseln"], False)
add("Ruby", "https://www.ruby-lang.org/", "ruby-lang.org", "free", "unknown", ["programmierung"],
    "Ruby ist eine Programmiersprache, oft für Webanwendungen.",
    "ruby-lang.org stellt die Sprache und die Dokumentation bereit. Eine OSI-Kennung wird hier nicht erneut eingetragen. Der Interpreter ist ohne Pflichtabo erhältlich.",
    ["Programmiersprache", "Dokumentation", "Nutzung ohne Pflichtabo"],
    ["Ein Skript in Ruby zu schreiben", "Die Dokumentation einer Klasse zu lesen"], False)
add("Elixir", "https://elixir-lang.org/", "elixir-lang.org", "free", "unknown", ["programmierung"],
    "Elixir ist eine Programmiersprache für nebenläufige Dienste auf der Erlang-VM.",
    "elixir-lang.org stellt Compiler und Dokumentation bereit. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Werkzeuge sind ohne Pflichtabo erhältlich.",
    ["Nebenläufige Dienste", "Erlang-VM", "Nutzung ohne Pflichtabo"],
    ["Einen Dienst in Elixir zu schreiben", "Die Dokumentation zu lesen"], False)
add("Haskell", "https://www.haskell.org/", "haskell.org", "free", "unknown", ["programmierung"],
    "Haskell ist eine funktionale Programmiersprache mit starkem Typsystem.",
    "haskell.org stellt Compiler und Dokumentation bereit. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Werkzeuge sind ohne Pflichtabo erhältlich.",
    ["Funktionale Sprache", "Starkes Typsystem", "Nutzung ohne Pflichtabo"],
    ["Ein Programm in Haskell zu schreiben", "Den Compiler zu finden"], False)
add("OCaml", "https://ocaml.org/", "ocaml.org", "free", "unknown", ["programmierung"],
    "OCaml ist eine funktionale Programmiersprache mit einem nativen Compiler.",
    "ocaml.org stellt Werkzeuge und Dokumentation bereit. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Werkzeuge sind ohne Pflichtabo erhältlich.",
    ["Funktionale Sprache", "Nativer Compiler", "Nutzung ohne Pflichtabo"],
    ["Ein Programm in OCaml zu bauen", "Die Dokumentation zu lesen"], False)
add("Scala", "https://www.scala-lang.org/", "scala-lang.org", "free", "unknown", ["programmierung"],
    "Scala verbindet funktionale und objektorientierte Programmierung auf der JVM.",
    "scala-lang.org stellt Compiler und Dokumentation bereit. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Werkzeuge sind ohne Pflichtabo erhältlich.",
    ["Sprache auf der JVM", "Dokumentation", "Nutzung ohne Pflichtabo"],
    ["Ein Programm in Scala zu schreiben", "Den Compiler zu finden"], False)
add("Swift", "https://www.swift.org/", "swift.org", "free", "unknown", ["programmierung"],
    "Swift ist eine Programmiersprache für Apple-Plattformen und Server.",
    "swift.org stellt die Sprache und den Compiler außerhalb des App Stores vor. Eine OSI-Kennung wird hier nicht erneut eingetragen. Der Compiler ist ohne Pflichtabo erhältlich.",
    ["Sprache für Apple-Plattformen und Server", "Compiler", "Nutzung ohne Pflichtabo"],
    ["Ein Programm in Swift zu bauen", "Die Sprachdokumentation zu lesen"], False)
add("Zig", "https://ziglang.org/", "ziglang.org", "free", "unknown", ["programmierung"],
    "Zig ist eine Systemsprache mit manuellem Speicher und einem eigenen Build-System.",
    "ziglang.org stellt Compiler und Dokumentation bereit. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Werkzeuge sind ohne Pflichtabo erhältlich.",
    ["Systemsprache", "Eigenes Build-System", "Nutzung ohne Pflichtabo"],
    ["Ein Programm in Zig zu schreiben", "Den Compiler zu laden"], False)
add("Julia", "https://julialang.org/", "julialang.org", "free", "unknown", ["programmierung", "daten"],
    "Julia ist eine Sprache für numerische Arbeit und wissenschaftliche Programme.",
    "julialang.org stellt die Sprache und Pakete vor. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Laufzeit ist ohne Pflichtabo erhältlich.",
    ["Numerische Sprache", "Pakete", "Nutzung ohne Pflichtabo"],
    ["Eine Berechnung in Julia zu schreiben", "Ein Paket zu finden"], False)
add("Hex", "https://hex.pm/", "hex.pm", "free", "unknown", ["programmierung"],
    "Hex verteilt Pakete für Elixir und Erlang.",
    "Hex zeigt Bibliotheken und Versionen. Die Suche ist ohne Konto möglich. Eine OSI-Kennung des Index wird hier nicht eingetragen.",
    ["Pakete für Elixir und Erlang", "Versionen", "Suche ohne Konto"],
    ["Eine Bibliothek zu finden", "Die aktuelle Version nachzusehen"], True)
add("pub.dev", "https://pub.dev/", "pub.dev", "free", "unknown", ["programmierung"],
    "pub.dev verteilt Pakete für Dart und Flutter.",
    "Die Seite zeigt Pakete, Versionen und Beispielcode. Die Suche ist ohne Konto möglich. Eine OSI-Kennung des Index wird hier nicht eingetragen.",
    ["Pakete für Dart und Flutter", "Beispielcode", "Suche ohne Konto"],
    ["Ein Flutter-Paket zu finden", "Die API eines Pakets zu lesen"], True)


def validate(entries):
    entries[:] = [e for e in entries if "fehlt" not in e["name"]]
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
    out = ROOT / "data" / "verified-tools-batch13.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows))
