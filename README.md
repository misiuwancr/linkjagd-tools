# Linkjagd Tools

Deutschsprachiges Verzeichnis für KI-Tools. Öffentliche Ausprobieren-Buttons führen nur über `/go/[slug]` und nur auf einen hinterlegten Partnerlink.

Der Projektname steht allein in [`site.config.ts`](site.config.ts). Das dunkle Erscheinungsbild ist in [`docs/MARKE.md`](docs/MARKE.md) begründet.

Grundlage ist das MIT-lizenzierte [9d8/directory](https://github.com/9d8dev/directory). Siehe `LICENSE` und `NOTICE`. Die Analyse der Vorlage steht in [`docs/ANALYSE.md`](docs/ANALYSE.md).

## Lokal starten

Voraussetzungen: Node.js 20 oder neuer.

```bash
cp .env.example .env
# JWT_SECRET und ADMIN_PASSWORD setzen (Passwort mindestens 12 Zeichen)
npm install
npm run db:setup
npm run import:verified
npm run dev
```

Die Anwendung läuft auf [http://127.0.0.1:4327](http://127.0.0.1:4327). Die Redaktion liegt unter `/admin`. Der erste Admin entsteht aus `ADMIN_EMAIL` und `ADMIN_PASSWORD`, solange noch kein Konto existiert.

```bash
npm test
npm run build
npm start
```

## Struktur

| Pfad | Inhalt |
| --- | --- |
| `app/(public)` | Startseite, Verzeichnis, Detailseiten, Kategorien, Blog, Rechtstexte |
| `app/go/[slug]` | Weiterleitung, nur bei gültigem Partnerlink |
| `app/admin` | Redaktion, serverseitig geschützt |
| `app/api/import` | Importschnittstelle, Bearer-Token |
| `db` | Drizzle-Schema, Migrationen, Seed |
| `lib/affiliate` | Redirect-Regeln, Klickzähler, Netzwerk-Registry |
| `lib/tools` | Abfragen, öffentliche Darstellung, Speichern |
| `migrations` | SQL, wird beim Start angewendet |
| `tests` | Weiterleitung, Filter, Rollen, Import |

## Datenbank

Lokale SQLite-Datei über `@libsql/client` (`DATABASE_URL=file:./data/linkjagd.db`). Dieselbe Bibliothek kann später auf Turso zeigen, nötig ist das nicht. Turso hat einen kostenlosen Tarif und wird danach nutzungsbasiert berechnet; hier entstehen keine Datenbankkosten.

| Tabelle | Zweck |
| --- | --- |
| `users` | Redaktion, Rollen `admin` und `editor` |
| `categories`, `tags` | Themen und Schlagwörter |
| `tools` | Werkzeug inklusive interner Original-URL |
| `tool_categories`, `tool_tags` | Zuordnungen |
| `affiliate_programs` | mehrere Programme je Tool, ein aktiver Link |
| `click_daily` | Tageszähler ohne IP, Cookie oder User-Agent |
| `news_posts` | spätere Meldungen |

`publish_status`: Entwurf, veröffentlicht, archiviert. Öffentlich sind nur Veröffentlichte.

Partnerstatus: Kein Partnerprogramm gefunden, Partnerprogramm gefunden, Bewerbung ausstehend, Freigeschaltet, Affiliate-Link aktiv, Affiliate-Link deaktiviert. `/go` nutzt nur ein Programm, das aktiv markiert ist und den Status „Affiliate-Link aktiv“ hat. Die URL muss `http` oder `https` sein, darf nicht die Original-URL sein und darf nicht auf diese Website oder auf lokale Netze zeigen. Es werden keine Parameter angehängt. Ohne gültigen Link antwortet `/go` mit 404.

Migrationen liegen in `migrations/` und laufen über `npm run db:migrate` oder beim Start. `npm run db:setup` migriert und legt fehlende Kategorien, Beispieldatensätze und den Admin an. Vorhandene Zeilen werden nicht überschrieben.

Beispieldatensätze bleiben in der Datenbank, werden beim Seed archiviert und erscheinen nicht in öffentlichen Listen oder Zählern. Ein erneuter Seed setzt sie wieder auf archiviert, ohne Texte gesperrter Zeilen zu ändern. Echte Affiliate-URLs gehören nicht in den Seed. Testdaten mit `example.com` existieren nur in den Tests.

`npm run import:verified` legt geprüfte Tools zuerst als Entwurf an und veröffentlicht sie danach. Die zweite Liste liegt in `data/verified-tools-batch2.json` und wird mit importiert. Ohne eigenen Partnerlink führt `/go` zur offiziellen Website. Herkunft: [`docs/FUTURETOOLS-TOP100.md`](docs/FUTURETOOLS-TOP100.md).

## Umgebung

Siehe `.env.example`.

| Variable | Bedeutung |
| --- | --- |
| `DATABASE_URL` | libSQL-URL, lokal `file:./data/linkjagd.db` |
| `JWT_SECRET` | mindestens 16 Zeichen, Cookie-Signatur |
| `ADMIN_EMAIL`, `ADMIN_PASSWORD` | erster Admin, Passwort mindestens 12 Zeichen |
| `NEXT_PUBLIC_SITE_URL` | Canonical und Sitemap |
| `IMPORT_API_TOKEN` | optional, sonst ist der Import aus |
| `NEWSLETTER_PROVIDER` | reserviert, ungenutzt; ohne Wert kein Versand und keine Speicherung |

Keine Secrets ins Repository legen.

## Deployment

Lokal bleibt SQLite. Für Vercel und Turso steht die Anleitung in [`DEPLOY.md`](DEPLOY.md). `npm run build` migriert die gerade gewählte Datenbank, seedet nur fehlende Basisdaten und baut. Ohne `TURSO_DATABASE_URL` ist das die Datei aus `DATABASE_URL`. Auf Vercel ohne Turso-Variablen bricht der Start ab.

Öffentliche Seiten nutzen ISR mit 60 Sekunden. `/go` ist dynamisch und nicht cachebar. `sitemap.xml` und `robots.txt` werden erzeugt. `/admin`, `/api` und `/go` sind von der Indexierung ausgenommen.

Rechtstexte unter Impressum, Datenschutz und Affiliate-Hinweis sind Platzhalter. Vor einem öffentlichen Start müssen sie geprüft und ergänzt werden. Es sind keine Firmenangaben erfunden. Preise und Hinweise enthalten keine Umsatzsteuer-Zusätze.

## Automatisierung

Siehe [`docs/AUTOMATISIERUNG.md`](docs/AUTOMATISIERUNG.md). Import und Netzwerk-Adapter sind Schnittstellen. Crawler, Auto-Bewerbung und KI-Agenten sind nicht implementiert und dürfen Quellen nur lesen, wenn Nutzungsbedingungen und `robots.txt` das erlauben.

## Tests

`npm test` prüft die Weiterleitung (kein Fallback auf die Original-URL), die öffentliche Darstellung ohne Original- und Partner-URL, Filter-URLs, Rollen, den Import mit Dubletten und den Klickzähler.
