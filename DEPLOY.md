# Deploy vorbereiten (Turso und Vercel)

Noch nichts ist deployed. Die Accounts legst du selbst an. Zugangsdaten bleiben außerhalb des Repos.

## Umgebungsvariablen in Vercel

| Variable | Pflicht | Bedeutung |
| --- | --- | --- |
| `TURSO_DATABASE_URL` | ja | `libsql://…turso.io` aus `turso db show` |
| `TURSO_AUTH_TOKEN` | ja | Token nur für diese Datenbank, nicht ins Repo |
| `JWT_SECRET` | ja | mindestens 16 Zeichen, kein Text aus `.env.example` |
| `ADMIN_EMAIL` | ja | E-Mail des ersten Admins, falls die Remote-Datenbank noch keinen Benutzer hat |
| `ADMIN_PASSWORD` | ja | mindestens 12 Zeichen; legt den Admin nur an, wenn noch keiner existiert |
| `NEXT_PUBLIC_SITE_URL` | ja | öffentliche Basis-URL, zuerst die Vercel-URL, später die eigene Domain |
| `IMPORT_API_TOKEN` | nein | ohne Wert ist `POST /api/import` aus |
| `DATABASE_URL` | nein | auf Vercel weglassen; lokal `file:./data/linkjagd.db` |

Ohne `JWT_SECRET` zeigt `/admin/login` kein Formular. Ist die Tabelle `users` leer, legt die Anmeldung genau einen Admin aus `ADMIN_EMAIL` und `ADMIN_PASSWORD` an. Der Serverstart selbst öffnet dafür keine Datenbank. Ein vorhandenes Konto wird nicht überschrieben. Node auf Vercel ist `22.x` über `engines` in `package.json`.

`INDEXING_ENABLED` bleibt auf Produktion leer, sonst ändert sich die Google-Freigabe. Vorschau (`VERCEL_ENV=preview`) und der lokale Rechner setzen noindex von selbst. Die Vorschau nutzt derzeit dieselben Turso-Variablen wie die Produktion. Dafür eine eigene kostenlose Turso-Datenbank anlegen und die beiden Turso-Variablen nur in der Vorschau darauf zeigen lassen. Die Datei `db/pending/0007_allow_index.sql` wird nicht automatisch ausgeführt.

## Turso anlegen

[Turso CLI](https://docs.turso.tech/cli/installation) installieren und einloggen:

```bash
turso auth login
turso db create linkjagd-tools
turso db show linkjagd-tools --url
turso db tokens create linkjagd-tools
```

Die URL und den Token lokal in `.env` setzen (Datei ist in `.gitignore`):

```bash
TURSO_DATABASE_URL=libsql://…
TURSO_AUTH_TOKEN=…
```

`DATABASE_URL` bleibt `file:./data/linkjagd.db`.

## Daten übertragen

Der Dump ohne Passwort-Hashes liegt in `data/export/`. Alternativen (`/alternativen`), Sammlungen (`/fuer`) und Kategorietexte stehen im Code und wandern mit dem Deploy, nicht mit der Datenbank.

```bash
npm run db:export
npm run db:push-remote
```

`db:push-remote` schreibt den Dump neu, wendet `migrations/*.sql` auf Turso an und ersetzt dort die Inhalts-Tabellen durch die lokale Datei. Der Admin-Hash wird mitkopiert, aber nicht ausgegeben und nicht ins Repo geschrieben. Ein zweiter Lauf macht dasselbe noch einmal.

Ohne die beiden Turso-Variablen endet `db:push-remote` nach dem Export mit einem Hinweis und Code 1.

## Vercel

Projekt mit diesem Repo verbinden. Dieselben Variablen wie oben eintragen. Build-Befehl bleibt `npm run build`. Erst übertragen, dann das erste Deployment auslösen.

`NEXT_PUBLIC_SITE_URL` nach dem ersten Deployment auf die echte Adresse setzen und erneut bauen, damit Sitemap und Canonicals stimmen.
