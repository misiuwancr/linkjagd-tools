#!/usr/bin/env python3
"""Zwanzigste Liste: bekannte CMS-, Auth- und Analyse-Werkzeuge."""

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


add("WordPress", "https://wordpress.org/", "wordpress.org", "free", "open_source", ["design"],
    "WordPress betreibt Websites und Blogs und steht unter der GPL.",
    "WordPress lässt sich selbst hosten und mit Erweiterungen ausbauen. Die Software ist quelloffen unter der GPL und ohne Lizenzgebühr nutzbar.",
    ["Selbst gehostete Websites", "Erweiterungen", "GPL, ohne Lizenzgebühr"],
    ["Einen Blog selbst zu betreiben", "Eine Website mit Erweiterungen zu bauen"], True)
add("WordPress.com", "https://wordpress.com/", "wordpress.com", "freemium", "proprietary", ["design"],
    "WordPress.com hostet eine WordPress-Website, ohne einen eigenen Server.",
    "WordPress.com veröffentlicht Seiten auf der gehosteten Plattform. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Gehostetes WordPress", "Eigene Domain in bezahlten Stufen", "Kostenloser Einstieg"],
    ["Einen Blog ohne eigenen Server zu starten", "Eine Seite zu veröffentlichen"], True)
add("Sanity", "https://www.sanity.io/", "sanity.io", "freemium", "proprietary", ["design"],
    "Sanity speichert Inhalte in einem anpassbaren Redaktionssystem.",
    "Sanity liefert Inhalte über eine Schnittstelle an die Website. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Anpassbare Redaktion", "Schnittstelle", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Texte strukturiert abzulegen", "Inhalte an eine Website zu liefern"], False)
add("Strapi", "https://www.strapi.io/", "strapi.io", "freemium", "unknown", ["design", "programmierung"],
    "Strapi ist ein Redaktionssystem, das Inhalte über eine Schnittstelle ausliefert.",
    "Strapi legt Inhaltstypen an und stellt sie per API bereit. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine selbst betriebene Fassung und eine bezahlte Cloud.",
    ["Inhaltstypen", "API", "Selbst betrieben und bezahlte Cloud"],
    ["Ein eigenes Redaktionssystem zu starten", "Inhalte an ein Frontend zu geben"], False)
add("Payload", "https://payloadcms.com/", "payloadcms.com", "freemium", "unknown", ["design"],
    "Payload ist ein Redaktionssystem, das im eigenen Code mitläuft.",
    "Payload definiert Inhaltstypen neben der Anwendung. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine selbst betriebene Fassung und eine bezahlte Cloud.",
    ["Inhaltstypen im eigenen Code", "Selbst betrieben", "Bezahlte Cloud"],
    ["Inhalte neben der App zu pflegen", "Eine Redaktion ohne separates System zu betreiben"], False)
add("Storyblok", "https://www.storyblok.com/", "storyblok.com", "freemium", "proprietary", ["design"],
    "Storyblok lässt Inhalte in Blöcken pflegen und an die Website liefern.",
    "Storyblok zeigt eine Vorschau der Seite. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Inhalte in Blöcken", "Vorschau", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Seite in Blöcken zu pflegen", "Eine Vorschau vor dem Veröffentlichen zu sehen"], False)
add("Hygraph", "https://hygraph.com/", "hygraph.com", "freemium", "proprietary", ["design"],
    "Hygraph speichert Inhalte und liefert sie über GraphQL.",
    "Hygraph modelliert Inhaltstypen und Beziehungen. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Inhalte über GraphQL", "Beziehungen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Inhalte an ein Frontend zu liefern", "Verknüpfte Inhalte zu modellieren"], False)
add("DatoCMS", "https://www.datocms.com/", "datocms.com", "freemium", "proprietary", ["design"],
    "DatoCMS pflegt Inhalte und liefert sie an die Website.",
    "DatoCMS legt Modelle an und zeigt eine Vorschau. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Inhaltsmodelle", "Vorschau", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Texte unabhängig vom Code zu pflegen", "Eine Vorschau zu prüfen"], False)
add("Prismic", "https://www.prismic.io/", "prismic.io", "freemium", "proprietary", ["design"],
    "Prismic speichert Seitenteile und liefert sie an die Website.",
    "Prismic setzt Slices und veröffentlicht sie. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Seitenteile", "Veröffentlichen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Landingpage in Teilen zu pflegen", "Inhalte ohne Deploy zu ändern"], False)
add("Builder.io", "https://www.builder.io/", "builder.io", "freemium", "proprietary", ["design"],
    "Builder.io lässt Seiten visuell bauen und an den bestehenden Code hängen.",
    "Builder.io setzt Blöcke auf eine vorhandene Website. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Visuelle Seiten", "Anbindung an vorhandenen Code", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Eine Seite ohne Deploy zu ändern", "Einen Block auf eine bestehende Seite zu setzen"], False)
add("Auth0", "https://auth0.com/", "auth0.com", "freemium", "proprietary", ["programmierung"],
    "Auth0 übernimmt Anmeldung und Konten für eine Anwendung.",
    "Auth0 stellt Login, Social-Login und Rollen bereit. Es gibt einen kostenlosen Einstieg und bezahlte Konten.",
    ["Anmeldung", "Social-Login", "Kostenloser Einstieg und bezahlte Konten"],
    ["Einen Login nicht selbst zu bauen", "Rollen an Konten zu hängen"], False)
add("Clerk", "https://clerk.com/", "clerk.com", "freemium", "proprietary", ["programmierung"],
    "Clerk baut Anmeldung, Profile und Organisationen in eine App ein.",
    "Clerk liefert fertige Anmelde-Komponenten. Es gibt einen kostenlosen Einstieg und bezahlte Konten.",
    ["Anmeldung und Profile", "Fertige Komponenten", "Kostenloser Einstieg und bezahlte Konten"],
    ["Einen Login in eine App zu setzen", "Organisationen mit Rollen zu führen"], False)
add("Stytch", "https://stytch.com/", "stytch.com", "freemium", "proprietary", ["programmierung"],
    "Stytch meldet Nutzer per Link, Code oder Passkey an.",
    "Stytch stellt passwortlose Anmeldung bereit. Es gibt einen kostenlosen Einstieg und bezahlte Konten.",
    ["Anmeldung ohne Passwort", "Passkeys", "Kostenloser Einstieg und bezahlte Konten"],
    ["Einen Login per E-Mail-Link zu bauen", "Passkeys anzubieten"], False)
add("Okta", "https://www.okta.com/", "okta.com", "paid", "proprietary", ["programmierung"],
    "Okta verwaltet Konten und Anmeldung für Belegschaften und Kunden.",
    "Okta bündelt Single Sign-on und Verzeichnisdienste. Die Nutzung ist kostenpflichtig.",
    ["Single Sign-on", "Verzeichnis", "Kostenpflichtige Nutzung"],
    ["Eine Anmeldung für viele interne Tools zu bündeln", "Konten zentral zu sperren"], False)
add("Firebase", "https://firebase.google.com/", "firebase.google.com", "freemium", "proprietary", ["programmierung"],
    "Firebase stellt Datenbank, Anmeldung und Hosting für Apps bereit.",
    "Firebase hängt Dienste an eine Anwendung. Es gibt einen kostenlosen Einstieg und bezahlte Nutzung.",
    ["Datenbank, Anmeldung, Hosting", "Dienste für Apps", "Kostenloser Einstieg und bezahlte Nutzung"],
    ["Eine App ohne eigenen Server zu starten", "Eine Anmeldung anzubinden"], False)
add("PlanetScale", "https://planetscale.com/", "planetscale.com", "freemium", "proprietary", ["daten"],
    "PlanetScale betreibt MySQL-Datenbanken mit Verzweigungen wie im Code.",
    "PlanetScale legt eine Datenbank an und trennt Schema-Änderungen. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Gehostetes MySQL", "Verzweigte Schema-Änderungen", "Einstieg und bezahlte Stufen"],
    ["Eine MySQL-Datenbank ohne eigenen Server zu betreiben", "Eine Schema-Änderung getrennt auszurollen"], False)
add("Railway", "https://railway.app/", "railway.app", "freemium", "proprietary", ["programmierung"],
    "Railway startet Anwendungen und Datenbanken aus einem Repository.",
    "Railway baut ein Projekt und stellt es bereit. Es gibt einen Einstieg und bezahlte Nutzung.",
    ["Apps aus einem Repository", "Datenbanken dazu", "Einstieg und bezahlte Nutzung"],
    ["Einen Dienst ohne eigenen Server zu starten", "Eine Datenbank daneben zu legen"], False)
add("Fly.io", "https://fly.io/", "fly.io", "freemium", "proprietary", ["programmierung"],
    "Fly.io startet Anwendungen nah an den Nutzern auf gemieteten Rechnern.",
    "Fly.io nimmt ein Image und verteilt es. Es gibt einen Einstieg und bezahlte Nutzung.",
    ["Anwendungen auf gemieteten Rechnern", "Verteilung", "Einstieg und bezahlte Nutzung"],
    ["Einen Dienst in mehreren Regionen zu starten", "Nur die Laufzeit zu bezahlen"], False)
add("LaunchDarkly", "https://www.launchdarkly.com/", "launchdarkly.com", "freemium", "proprietary", ["programmierung"],
    "LaunchDarkly schaltet Funktionen für einen Teil der Nutzer frei.",
    "LaunchDarkly legt Flags an und steuert, wer eine Funktion sieht. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Feature-Flags", "Freischaltung nach Gruppe", "Einstieg und bezahlte Stufen"],
    ["Eine Funktion erst für ein Team zu zeigen", "Einen Schalter ohne Deploy umzulegen"], False)
add("Split", "https://www.split.io/", "split.io", "freemium", "proprietary", ["programmierung"],
    "Split schaltet Funktionen frei und misst, was sich dadurch ändert.",
    "Split verbindet einen Flag mit einer Kennzahl. Es gibt einen Einstieg und bezahlte Stufen.",
    ["Flags mit Messung", "Freischaltung", "Einstieg und bezahlte Stufen"],
    ["Eine Variante nur einem Teil zu zeigen", "Zu messen, ob sich eine Kennzahl ändert"], False)
add("Statsig", "https://www.statsig.com/", "statsig.com", "freemium", "proprietary", ["programmierung"],
    "Statsig testet Funktionen und misst, welche Fassung besser ist.",
    "Statsig legt Experimente und Flags an. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Experimente", "Flags", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Zwei Fassungen einer Funktion zu vergleichen", "Einen Schalter ohne Deploy zu setzen"], False)
add("GrowthBook", "https://growthbook.io/", "growthbook.io", "freemium", "unknown", ["programmierung"],
    "GrowthBook testet Funktionen und legt Flags für eine Anwendung an.",
    "GrowthBook zeigt, welche Variante eine Kennzahl bewegt. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine selbst betriebene Fassung und eine bezahlte Cloud.",
    ["Experimente und Flags", "Selbst betrieben", "Bezahlte Cloud"],
    ["Ein Experiment zu einer Funktion zu fahren", "Einen Flag selbst zu hosten"], False)
add("Flagsmith", "https://flagsmith.com/", "flagsmith.com", "freemium", "unknown", ["programmierung"],
    "Flagsmith schaltet Funktionen über Flags frei, auch selbst gehostet.",
    "Flagsmith legt Schalter je Umgebung an. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine selbst betriebene Fassung und eine bezahlte Cloud.",
    ["Flags je Umgebung", "Selbst gehostet", "Bezahlte Cloud"],
    ["Eine Funktion schrittweise freizuschalten", "Flags auf dem eigenen Server zu halten"], False)
add("Unleash", "https://www.getunleash.io/", "getunleash.io", "freemium", "unknown", ["programmierung"],
    "Unleash schaltet Funktionen über Flags frei und lässt sich selbst betreiben.",
    "Unleash trennt den Schalter vom Deploy. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt eine selbst betriebene Fassung und eine bezahlte Cloud.",
    ["Flags", "Selbst betrieben", "Bezahlte Cloud"],
    ["Einen Schalter ohne neues Release umzulegen", "Flags im eigenen Netz zu halten"], False)
add("Prisma", "https://www.prisma.io/", "prisma.io", "freemium", "unknown", ["programmierung", "daten"],
    "Prisma beschreibt das Datenbankschema und erzeugt den Zugriff im Code.",
    "Prisma legt Modelle fest und wandelt sie in Abfragen. Eine OSI-Kennung wird hier nicht eingetragen. Es gibt einen kostenlosen Einstieg und eine bezahlte Datenplattform.",
    ["Schema im Code", "Erzeugte Abfragen", "Kostenloser Einstieg und bezahlte Plattform"],
    ["Ein Schema neben dem Code zu führen", "Abfragen aus den Modellen zu erzeugen"], False)
add("ContentSquare", "https://www.contentsquare.com/", "contentsquare.com", "paid", "proprietary", ["marketing"],
    "ContentSquare zeigt, wie Leute eine Website nutzen, und wo sie stocken.",
    "ContentSquare zeichnet Wege und Zonen auf. Die Nutzung ist kostenpflichtig.",
    ["Wege auf der Website", "Zonen", "Kostenpflichtige Nutzung"],
    ["Zu sehen, wo eine Seite nicht weiterführt", "Zonen mit vielen Abbrüchen zu finden"], False)
add("Inspectlet", "https://www.inspectlet.com/", "inspectlet.com", "freemium", "proprietary", ["marketing"],
    "Inspectlet zeichnet Besuche auf und legt Heatmaps darüber.",
    "Inspectlet spielt eine Sitzung nach. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Sitzungsaufzeichnung", "Heatmaps", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Einen Besuch mit Abbruch nachzusehen", "Klicks auf einer Seite zu sehen"], False)
add("Ptengine", "https://www.ptengine.com/", "ptengine.com", "freemium", "proprietary", ["marketing"],
    "Ptengine zeigt Heatmaps und zeichnet Sitzungen auf.",
    "Ptengine legt eine Karte der Klicks über die Seite. Es gibt einen kostenlosen Einstieg und bezahlte Stufen.",
    ["Heatmaps", "Sitzungen", "Kostenloser Einstieg und bezahlte Stufen"],
    ["Zu sehen, welche Stelle geklickt wird", "Eine Sitzung nachzuspielen"], False)
add("Glassbox", "https://www.glassbox.com/", "glassbox.com", "paid", "proprietary", ["marketing"],
    "Glassbox zeichnet Sitzungen in Web und App auf und macht sie suchbar.",
    "Glassbox filtert Besuche nach einem Fehler oder einem Schritt. Die Nutzung ist kostenpflichtig.",
    ["Sitzungen in Web und App", "Suche", "Kostenpflichtige Nutzung"],
    ["Einen Fehler mit der Sitzung zu sehen", "Besuche mit einem bestimmten Schritt zu finden"], False)
add("Quantum Metric", "https://www.quantummetric.com/", "quantummetric.com", "paid", "proprietary", ["marketing"],
    "Quantum Metric zeichnet Sitzungen auf und verbindet sie mit Kennzahlen.",
    "Quantum Metric zeigt, wo ein Ablauf abbricht. Die Nutzung ist kostenpflichtig.",
    ["Sitzungen und Kennzahlen", "Abbrüche", "Kostenpflichtige Nutzung"],
    ["Einen Abbruch im Checkout zu finden", "Eine Sitzung zu einer Kennzahl zu sehen"], False)
add("Verbformen", "https://www.verbformen.com/", "verbformen.com", "freemium", "proprietary", ["bildung"],
    "Verbformen zeigt die Konjugation deutscher Verben und Beispielsätze.",
    "Die Seite nimmt ein Verb und listet die Formen. Die Tabellen sind ohne Abo lesbar, weitere Übungen sind bezahlt.",
    ["Konjugation deutscher Verben", "Beispielsätze", "Tabellen ohne Abo"],
    ["Die Formen eines Verbs nachzuschlagen", "Einen Beispielsatz zu einer Form zu lesen"], True)
add("SpanishDict", "https://www.spanishdict.com/", "spanishdict.com", "freemium", "proprietary", ["bildung"],
    "SpanishDict übersetzt zwischen Spanisch und Englisch und zeigt die Konjugation.",
    "SpanishDict nimmt ein Wort oder einen Satz und liefert Übersetzung und Formen. Es gibt einen kostenlosen Einstieg und ein bezahltes Abo.",
    ["Übersetzung Spanisch und Englisch", "Konjugation", "Kostenloser Einstieg und bezahltes Abo"],
    ["Ein Wort nachzuschlagen", "Die Formen eines spanischen Verbs zu sehen"], True)


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
    out = ROOT / "data" / "verified-tools-batch20.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows))
