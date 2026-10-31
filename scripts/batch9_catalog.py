#!/usr/bin/env python3
"""Neunte geprüfte Liste. Nur Seiten, die unmittelbar vorher HTTP 200 geliefert haben."""

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


add("Emby", "https://emby.media/", "emby.media", "freemium", "proprietary", ["videoschnitt"],
    "Emby spielt die eigene Filmsammlung auf Fernseher und Handy.",
    "Emby streamt Filme vom eigenen Server. Es gibt eine kostenlose Ausgabe und ein bezahltes Premiere.",
    ["Eigene Filmsammlung", "Stream auf mehrere Geräte", "Kostenlose Ausgabe und bezahltes Premiere"],
    ["Einen Film vom eigenen Server zu sehen", "Dieselbe Bibliothek auf dem Fernseher zu öffnen"], True)
add("IINA", "https://iina.io/", "iina.io", "free", "unknown", ["videoschnitt"],
    "IINA spielt Videos auf dem Mac mit einer schmalen Oberfläche.",
    "IINA öffnet Dateien und Streams und setzt Untertitel. Eine OSI-Kennung wird hier nicht eingetragen. Der Player ist ohne Pflichtabo erhältlich.",
    ["Wiedergabe auf dem Mac", "Untertitel und Streams", "Nutzung ohne Pflichtabo"],
    ["Eine Videodatei auf dem Mac abzuspielen", "Einen Stream mit Untertitel zu öffnen"], True)
add("Kopia", "https://kopia.io/", "kopia.io", "free", "unknown", ["programmierung"],
    "Kopia sichert Dateien verschlüsselt auf ein eigenes Ziel.",
    "Kopia legt Schnappschüsse an und spielt einzelne Dateien zurück. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Verschlüsselte Schnappschüsse", "Rückspiel einzelner Dateien", "Nutzung ohne Pflichtabo"],
    ["Ein Verzeichnis verschlüsselt zu sichern", "Eine einzelne Datei zurückzuholen"], False)
add("Unraid", "https://unraid.net/", "unraid.net", "paid", "proprietary", ["daten"],
    "Unraid betreibt Speicher und virtuelle Maschinen auf eigener Hardware.",
    "Unraid legt Festplatten zu einem Speicher zusammen und startet VMs und Container. Die Lizenz ist kostenpflichtig.",
    ["Speicher aus mehreren Platten", "VMs und Container", "Kostenpflichtige Lizenz"],
    ["Einen Heimserver mit gemischten Platten zu betreiben", "Eine virtuelle Maschine daneben zu starten"], False)
add("NextDNS", "https://nextdns.io/", "nextdns.io", "freemium", "proprietary", ["programmierung"],
    "NextDNS filtert DNS-Anfragen und blockiert bekannte Tracker.",
    "NextDNS beantwortet Namensauflösung nach eigenen Regeln. Es gibt einen kostenlosen Einstieg und bezahlte Abfragen.",
    ["DNS mit Filterregeln", "Blockieren bekannter Tracker", "Kostenloser Einstieg und bezahlte Abfragen"],
    ["Tracker über DNS zu filtern", "Eigene Sperrlisten zu setzen"], False)
add("Alpenverein", "https://www.alpenverein.de/", "alpenverein.de", "freemium", "proprietary", ["reisen"],
    "Der Deutsche Alpenverein informiert zu Touren, Hütten und Mitgliedschaft.",
    "Die Seite beschreibt Wege, Hütten und die Mitgliedschaft. Ein Teil der Texte ist ohne Mitgliedschaft lesbar, Hütten und Versicherung hängen an der Mitgliedschaft.",
    ["Touren und Hütten", "Mitgliedschaft", "Texte frei, Leistungen über die Mitgliedschaft"],
    ["Eine Hütte nachzuschlagen", "Die Mitgliedschaft einzuordnen"], True)
add("Apache Software Foundation", "https://www.apache.org/", "apache.org", "free", "unknown", ["programmierung"],
    "Die Apache Software Foundation trägt viele freie Server- und Entwicklerprojekte.",
    "apache.org listet Projekte und ihre Downloads. Eine einzelne OSI-Kennung für die Stiftung wird hier nicht eingetragen. Die Projektseiten sind ohne Abo lesbar.",
    ["Übersicht freier Projekte", "Downloads", "Lesen ohne Abo"],
    ["Ein Apache-Projekt zu finden", "Den Download eines Projekts zu öffnen"], False)
add("BeagleBoard", "https://www.beagleboard.org/", "beagleboard.org", "free", "proprietary", ["programmierung"],
    "BeagleBoard dokumentiert Einplatinenrechner für eigene Steuerungen.",
    "Die Seite beschreibt Boards und Bilder zum Start. Die Dokumentation ist ohne Konto lesbar, die Platinen sind kostenpflichtig.",
    ["Einplatinenrechner", "Dokumentation", "Platinen kostenpflichtig"],
    ["Ein Board für ein Projekt auszuwählen", "Ein Startbild zu finden"], False)
add("CNCF", "https://www.cncf.io/", "cncf.io", "free", "unknown", ["programmierung"],
    "Die Cloud Native Computing Foundation trägt Projekte rund um Container und Orchestrierung.",
    "Die CNCF listet abgestufte Projekte und deren Status. Die Übersicht ist ohne Konto lesbar. Eine OSI-Kennung der Stiftung wird hier nicht eingetragen.",
    ["Projekte rund um Container", "Abstufung nach Reife", "Lesen ohne Konto"],
    ["Den Status eines Projekts nachzusehen", "Ein Werkzeug der Landschaft zu finden"], False)
add("Duplicati", "https://www.duplicati.com/", "duplicati.com", "free", "unknown", ["programmierung"],
    "Duplicati sichert Ordner verschlüsselt auf ein Ziel eigener Wahl.",
    "Duplicati plant Sicherungen und lädt sie zu einem Speicher hoch. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Geplante Sicherungen", "Verschlüsselter Upload", "Nutzung ohne Pflichtabo"],
    ["Einen Ordner täglich zu sichern", "Eine Datei aus einer Sicherung zu holen"], False)
add("Eclipse Foundation", "https://www.eclipse.org/", "eclipse.org", "free", "unknown", ["programmierung"],
    "Die Eclipse Foundation trägt Entwicklungswerkzeuge und Spezifikationen.",
    "eclipse.org listet Projekte und Downloads. Eine einzelne OSI-Kennung wird hier nicht eingetragen. Die Seiten sind ohne Abo lesbar.",
    ["Entwicklungswerkzeuge", "Spezifikationen und Downloads", "Lesen ohne Abo"],
    ["Ein Eclipse-Projekt zu finden", "Einen Download zu öffnen"], False)
add("Free Software Foundation", "https://www.fsf.org/", "fsf.org", "free", "unknown", ["programmierung", "recherche"],
    "Die Free Software Foundation erklärt freie Software und die Lizenzen der GNU-Familie.",
    "Die FSF veröffentlicht Texte zu Lizenzen und Freiheit der Software. Die Seiten sind ohne Konto lesbar.",
    ["Texte zu freien Lizenzen", "Erläuterung freier Software", "Lesen ohne Konto"],
    ["Eine GNU-Lizenz nachzulesen", "Den Unterschied freier Lizenzen einzuordnen"], True)
add("Funkwhale", "https://www.funkwhale.audio/", "funkwhale.audio", "free", "unknown", ["musik"],
    "Funkwhale streamt Musik auf einem eigenen Server und im Verbund.",
    "Funkwhale spielt eine eigene Sammlung und kann anderen Instanzen folgen. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Eigene Musik auf dem Server", "Verbund mehrerer Instanzen", "Nutzung ohne Pflichtabo"],
    ["Eine Musiksammlung selbst zu hosten", "Einer anderen Instanz zu folgen"], False)
add("Hardkernel", "https://www.hardkernel.com/", "hardkernel.com", "free", "proprietary", ["programmierung"],
    "Hardkernel stellt die ODROID-Einplatinenrechner her.",
    "Die Seite zeigt Boards und Zubehör. Die Dokumentation ist ohne Konto lesbar, die Platinen sind kostenpflichtig.",
    ["Einplatinenrechner", "Zubehör", "Platinen kostenpflichtig"],
    ["Ein Board für ein Projekt zu wählen", "Zubehör zu einem ODROID zu finden"], False)
add("IANA", "https://www.iana.org/", "iana.org", "free", "proprietary", ["recherche"],
    "Die IANA verwaltet Nummern und Namen, die das Internet zum Funktionieren braucht.",
    "Die IANA veröffentlicht Register zu Ports, Protokollen und der Wurzel des Namensraums. Die Register sind ohne Konto lesbar.",
    ["Register zu Ports und Protokollen", "Wurzel des Namensraums", "Lesen ohne Konto"],
    ["Einen Port nachzuschlagen", "Ein Protokoll im Register zu finden"], False)
add("ICANN", "https://www.icann.org/", "icann.org", "free", "proprietary", ["recherche"],
    "Die ICANN koordiniert Namen und Adressen im Internet.",
    "Die ICANN erklärt Domain-Endungen und veröffentlicht Beschlüsse. Die Seiten sind ohne Konto lesbar.",
    ["Namen und Adressen", "Beschlüsse zu Domain-Endungen", "Lesen ohne Konto"],
    ["Eine Domain-Endung einzuordnen", "Einen Beschluss nachzulesen"], True)
add("IETF", "https://www.ietf.org/", "ietf.org", "free", "unknown", ["recherche", "programmierung"],
    "Die IETF erarbeitet die technischen Standards des Internets.",
    "Die IETF veröffentlicht Entwürfe und Standards. Die Dokumente sind ohne Konto lesbar. Eine OSI-Kennung der Organisation wird hier nicht eingetragen.",
    ["Technische Standards", "Entwürfe und fertige Texte", "Lesen ohne Konto"],
    ["Einen Internet-Standard zu finden", "Einen Entwurf zu lesen"], False)
add("Linux Foundation", "https://www.linuxfoundation.org/", "linuxfoundation.org", "free", "unknown", ["programmierung"],
    "Die Linux Foundation trägt den Kernel und viele weitere Projekte.",
    "Die Stiftung listet Projekte und Veranstaltungen. Die Übersicht ist ohne Konto lesbar. Eine OSI-Kennung der Stiftung wird hier nicht eingetragen.",
    ["Projekte rund um Linux", "Veranstaltungen", "Lesen ohne Konto"],
    ["Ein Projekt der Stiftung zu finden", "Den Bezug zum Kernel nachzulesen"], False)
add("pfSense", "https://www.pfsense.org/", "pfsense.org", "freemium", "unknown", ["programmierung"],
    "pfSense ist eine Firewall-Distribution für eigene Hardware.",
    "pfSense filtert Verkehr und baut VPN. Es gibt eine Community-Ausgabe und eine bezahlte Plus-Ausgabe. Eine OSI-Kennung wird hier nicht eingetragen.",
    ["Firewall und VPN", "Community-Ausgabe und Plus", "Lizenz nicht eingetragen"],
    ["Einen Router selbst zu betreiben", "Ein VPN auf der Firewall einzurichten"], False)
add("Pine64", "https://www.pine64.org/", "pine64.org", "free", "proprietary", ["programmierung"],
    "Pine64 stellt günstige Einplatinenrechner und Linux-Geräte her.",
    "Die Seite zeigt Boards und den Stand der Software. Die Dokumentation ist ohne Konto lesbar, die Geräte sind kostenpflichtig.",
    ["Einplatinenrechner", "Linux-Geräte", "Geräte kostenpflichtig"],
    ["Ein Board für ein Experiment zu wählen", "Den Softwarestand eines Geräts zu lesen"], False)
add("QEMU", "https://www.qemu.org/", "qemu.org", "free", "unknown", ["programmierung"],
    "QEMU startet andere Betriebssysteme und Prozessoren in Software.",
    "QEMU emuliert Maschinen und kann als Unterbau für virtuelle Maschinen dienen. Eine OSI-Kennung wird hier nicht erneut eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Emulation und virtuelle Maschinen", "Viele Prozessoren", "Nutzung ohne Pflichtabo"],
    ["Ein anderes System zum Testen zu starten", "Eine Architektur zu emulieren"], False)
add("RFC Editor", "https://www.rfc-editor.org/", "rfc-editor.org", "free", "unknown", ["recherche", "programmierung"],
    "Der RFC Editor veröffentlicht die Standards und Notizen der IETF.",
    "Die Seite stellt RFCs im Volltext bereit. Das Lesen ist ohne Konto möglich. Eine OSI-Kennung der Texte wird hier nicht pauschal eingetragen.",
    ["Volltexte der RFCs", "Standards und Notizen", "Lesen ohne Konto"],
    ["Einen RFC im Wortlaut zu lesen", "Einen Standard nach Nummer zu finden"], False)
add("RIPE NCC", "https://www.ripe.net/", "ripe.net", "free", "proprietary", ["recherche"],
    "Das RIPE NCC verteilt IP-Adressen in Europa und veröffentlicht dazu Daten.",
    "ripe.net zeigt Statistiken und Werkzeuge zur Registrierung. Ein Teil der Seiten ist ohne Konto lesbar.",
    ["IP-Adressen in Europa", "Statistiken und Werkzeuge", "Ein Teil ohne Konto"],
    ["Eine Registrierung nachzuschlagen", "Statistiken zu Adressen zu lesen"], False)
add("RISC-V", "https://www.riscv.org/", "riscv.org", "free", "unknown", ["programmierung"],
    "RISC-V International veröffentlicht die offene Befehlssatzarchitektur RISC-V.",
    "Die Seite erklärt die Architektur und verweist auf Spezifikationen. Die Übersicht ist ohne Konto lesbar. Eine einzelne OSI-Kennung wird hier nicht eingetragen.",
    ["Befehlssatzarchitektur", "Spezifikationen", "Lesen ohne Konto"],
    ["Die Architektur einzuordnen", "Eine Spezifikation zu finden"], False)
add("Seeed Studio", "https://www.seeedstudio.com/", "seeedstudio.com", "free", "proprietary", ["programmierung"],
    "Seeed Studio verkauft Module und fertigt kleine Elektronikserien.",
    "Seeed zeigt Bauteile und einen Fertigungsservice. Die Katalogseiten sind ohne Konto lesbar, Bauteile und Fertigung sind kostenpflichtig.",
    ["Module und Fertigung", "Katalog", "Bauteile kostenpflichtig"],
    ["Ein Modul für ein Projekt zu finden", "Eine kleine Serie fertigen zu lassen"], False)
add("ToolJet", "https://www.tooljet.com/", "tooljet.com", "freemium", "unknown", ["programmierung"],
    "ToolJet baut interne Werkzeuge auf Datenquellen.",
    "ToolJet setzt Oberflächen auf Datenbanken und APIs und lässt sich selbst betreiben. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine Cloud und den Selbstbetrieb.",
    ["Oberflächen auf Datenquellen", "Cloud und Selbstbetrieb", "Lizenz nicht eingetragen"],
    ["Ein internes Werkzeug selbst zu hosten", "Eine Tabelle auf eine API zu legen"], False)
add("Veeam", "https://www.veeam.com/", "veeam.com", "freemium", "proprietary", ["daten"],
    "Veeam sichert virtuelle Maschinen, Server und Cloud-Workloads.",
    "Veeam legt Sicherungen an und spielt sie zurück. Es gibt einen Einstieg und kostenpflichtige Editionen.",
    ["Sicherung von VMs und Servern", "Rückspiel", "Einstieg und kostenpflichtige Editionen"],
    ["Eine virtuelle Maschine zu sichern", "Einen Server zurückzuspielen"], False)
add("XCP-ng", "https://www.xcp-ng.org/", "xcp-ng.org", "free", "unknown", ["programmierung"],
    "XCP-ng betreibt virtuelle Maschinen auf dem eigenen Server.",
    "XCP-ng richtet einen Hypervisor ein und verwaltet die Maschinen über eine Oberfläche. Eine OSI-Kennung wird hier nicht eingetragen. Die Software ist ohne Pflichtabo erhältlich.",
    ["Hypervisor", "Oberfläche für die Maschinen", "Nutzung ohne Pflichtabo"],
    ["Mehrere virtuelle Maschinen auf einem Server zu betreiben", "Einen Host ohne Abo zu verwalten"], False)
add("Dribbble", "https://dribbble.com/", "dribbble.com", "freemium", "proprietary", ["design"],
    "Dribbble zeigt Arbeiten von Designerinnen und Designern.",
    "Dribbble veröffentlicht kurze Arbeitsproben und Profile. Das Ansehen ist ohne Abo möglich, weitere Funktionen sind bezahlt.",
    ["Arbeitsproben", "Profile", "Ansehen ohne Abo"],
    ["Eine Gestaltungsidee zu sichten", "Ein Profil zu finden"], True)
add("Kernel.org", "https://www.kernel.org/", "kernel.org", "free", "unknown", ["programmierung"],
    "kernel.org veröffentlicht den Quelltext und die Versionen des Linux-Kernels.",
    "Die Seite stellt Tarballs und Hinweise zu den aktuellen Versionen bereit. Der Download ist ohne Konto möglich. Eine einzelne OSI-Kennung wird hier nicht erneut eingetragen.",
    ["Quelltext des Linux-Kernels", "Versionshinweise", "Download ohne Konto"],
    ["Eine Kernel-Version zu laden", "Den Stand einer Veröffentlichung zu lesen"], False)
add("MeshLab bleibt", "https://www.meshlab.net/", "meshlab.net", "free", "unknown", ["dreid"],
    "Platzhalter.", "Platzhalter.", ["x"], ["x"])


def validate(entries):
    entries[:] = [e for e in entries if not e["name"].endswith(" bleibt")]
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
        raise SystemExit("\n".join(errors))
    return entries


if __name__ == "__main__":
    rows = validate(E)
    out = ROOT / "data" / "verified-tools-batch9.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows), "->", out)
