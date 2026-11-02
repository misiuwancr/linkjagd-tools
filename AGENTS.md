# Linknarr – Projektregeln

Linknarr ist ein deutsches Verzeichnis für KI-Tools (Alternative zu futuretools.io).
Live: https://linknarr.com.
Stack: Next.js 14, Drizzle ORM, Turso/libSQL; Hosting auf Vercel.
Die Seite ist ausschließlich auf Deutsch; keine englische Version bauen.
Der Markenname steht zentral in `site.config.ts` und soll an einer Stelle austauschbar bleiben.

## Befehle

Node.js 22 verwenden. Die vorhandene `package-lock.json` mit `npm ci` installieren.
- Entwicklung: `npm run dev`
- Build: `npm run build` (führt auch `tsx db/setup.ts` aus; ausschließlich eine isolierte Testdatenbank verwenden)
- Lint: `npm run lint`
- Tests: `npm test`

## Verbindliche Regeln
- Keine erfundenen Referral-Links verwenden. Niemals eigenmächtig Affiliate-Parameter an URLs anhängen.
- Lege keine Zugangsdaten im Repository ab. Verwende Umgebungsvariablen für Geheimnisse.
- Keine produktive Migration ohne ausdrückliche Freigabe von Michał durchführen. Neue Tabellen/Spalten zuerst nur als Migrationsdatei + Test auf der Vorschau-Datenbank.
- Keine Secrets in den Quellcode oder in Logs schreiben.
- Keinen kostenpflichtigen Dienst ohne Michałs Zustimmung einbinden.
- Keine rechtlichen Angaben erfinden (Impressum, Datenschutz: Platzhalter markieren).
- Den globalen Indexierungsstatus der öffentlichen Produktionsdomain nicht unbemerkt ändern (robots, noindex).
- Keine riskanten Änderungen an produktiven Daten ohne vorherige Freigabe.
- Aufgaben nur als abgeschlossen bezeichnen, wenn sie tatsächlich implementiert und geprüft wurden (Build + Tests grün).
- Michał ist Kleinunternehmer nach § 19 UStG: niemals „zzgl. USt“ oder „netto“ schreiben.
- Layout darf sich an futuretools.io orientieren, aber keine fremden Texte, Bilder oder Logos kopieren.
- Keine erfundenen Zahlen oder Fakten (z. B. Leserzahlen, Votes, Bewertungen).
