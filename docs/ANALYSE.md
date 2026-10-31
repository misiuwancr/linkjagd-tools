# Analyse von 9d8/directory

Grundlage ist [9d8dev/directory](https://github.com/9d8dev/directory), Commit `d140b0c8089040643cfce8b6ac508998cb5ee36e` (21. Januar 2025, „feat: protect api routes“). Lizenz: MIT, Copyright (c) 2024 9d8. Die Lizenzdatei bleibt unverändert im Repository. Die MIT-Pflicht, Copyright- und Rechtehinweis mitzuführen, ist damit erfüllt. Im Footer steht zusätzlich ein Herkunftshinweis.

## Was die Vorlage mitbringt

- Next.js 14 (App Router), TypeScript, Tailwind, shadcn/ui. Die Vorlage pinnt 14.2.15; hier liegt 14.2.35, weil für 14.2.15 eine Sicherheitslücke veröffentlicht ist. Es bleibt Next 14.
- Drizzle ORM und `@libsql/client`.
- Tabellen `categories` und `bookmarks`. Eine Kategorie pro Lesezeichen, Tags als Textfeld.
- Öffentliche Startseite filtert Lesezeichen im Speicher nach Kategorie und Suchtext.
- Admin unter `/admin` mit Anlegen, Bearbeiten und Löschen von Lesezeichen und Kategorien.
- Auth über das Paket `bohoauth`: ein Passwort, JWT, Middleware für `/admin` und ein paar API-Routen. Keine Rollen, kein Benutzer in der Datenbank.
- Detailseite unter `/[slug]`.
- Sitemap aus den Lesezeichen.
- Server Actions für CRUD.

## Was nicht startklar ist

Die dokumentierten Umgebungsvariablen und der Code passen nicht zusammen. `.env.example` nennt `ADMIN_PASSWORD` und `JWT_SECRET`, `lib/boho.ts` liest `BOHO_PASSWORD` und `BOHO_SECRET`. `db/client.ts` bricht ab, wenn `TURSO_DATABASE_URL` und `TURSO_AUTH_TOKEN` fehlen. Ohne Turso-Konto lässt sich die Vorlage nicht starten.

Suche und Filter laden alle Lesezeichen und filtern in der Seite. Das trägt keine tausenden Tools. Es gibt keine Pagination und keine Filter in der URL.

## Was für Linkjagd fehlt

- Deutsch, eigener Name, eigene Informationsarchitektur (`/tools`, Top 20, Neu, Kategorien, Blog, Einreichen, Rechtstexte).
- Tool-Felder auf Deutsch, n:m-Kategorien, Preismodell, Veröffentlichungsstatus, Empfehlung, redaktionelle Position, Herkunft.
- Partnerprogramme als eigene Tabelle, genau ein öffentlicher Link über `/go/[slug]`, kein Fallback auf die Original-URL.
- Aggregierte Klicks ohne IP und ohne Cookie.
- Rollenprüfung auf allen Admin-Seiten und Aktionen.
- Importschnittstelle und eine Adapter-Registry ohne echte Netzwerk-Anbindung.
- Tests für Weiterleitung, Filter und Zugriffsschutz.

## Externe Dienste der Vorlage

| Dienst | Wofür | Kosten | Entscheidung |
| --- | --- | --- | --- |
| Turso | gehostetes libSQL | kostenloser Tarif, danach nutzungsbasiert | nicht nötig; dieselbe Bibliothek spricht eine lokale SQLite-Datei |
| Anthropic | Texte erzeugen | API, kostenpflichtig nach Verbrauch | entfernt; automatische Recherche ist in Phase 1 verboten |
| Exa | Inhalte zu URLs | API, kostenpflichtig | entfernt, gleicher Grund |
| Loops | Newsletter-Versand | kostenloser Tarif, danach Abo | nicht angebunden; Formular speichert und versendet nichts |
| Vercel Analytics | Seitenaufrufe | im Vercel-Tarif | entfernt; kein zusätzliches Tracking |

Kein weiterer kostenpflichtiger Dienst ist eingebaut. Bilder liegen lokal. Auth ist ein signiertes Cookie. Die Datenbank ist eine Datei.

## Was wiederverwendet wird

Next.js, TypeScript, Tailwind, die shadcn-Bausteine (Button, Dialog, Sheet, Tabelle, Formularfelder), Drizzle und `@libsql/client`. Die Admin-Idee (geschützter Bereich, Kategorien und Einträge pflegen) bleibt, das Datenmodell und die Oberfläche sind neu, weil aus einem englischen Lesezeichen-Board kein Affiliate-Verzeichnis wird, ohne die Tabellen zu wechseln.

`bohoauth` ist ersetzt. Es kann keine Rollen und die Variablennamen der Vorlage sind bereits inkonsistent. Die Sitzung nutzt `jose`, das vorher nur indirekt über `bohoauth` kam.

## Referenz FutureTools, ohne Übernahme

An [futuretools.io](https://futuretools.io/), [/tools](https://futuretools.io/tools) und einer Detailseite orientieren sich Aufbau und Rhythmus: schmale Kopfzeile, große Suche, dichte Karten mit Logo, Kurztext, Kategorie- und Preis-Badge, Detailseite mit Kurztext, Langtext, seitlichem Kasten und einem großen Ausprobieren-Button, dazu ähnliche Tools. Übernommen wurden keine Texte, Bilder, Logos oder Quelltexte. Keine Stimmen, keine Nutzerzahlen, keine erfundenen Testimonials. Die Marke ist Linkjagd: warmes Papier, Tinte, Kupfer, Schrift Outfit, eigenes Zeichen aus zwei Kettengliedern.
