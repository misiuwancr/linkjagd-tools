# Linknarr: Rebranding und neue Startseite

## Umfang und Freigabe
Bestehende Codebasis, Branch feat/linknarr-rebranding von main 47bac85. Nutzerfreigabe „machen und deployen“, anschließend „beides“ für Rebranding und die Startseiten-/Verzeichnisänderungen aus dem Word-Dokument. Newsletter ohne Versanddienst ausdrücklich geschlossen. Der frühere Tool-Massenimport gehört nicht zu diesem Release.

## Änderungen nach Bereichen
- Text: site.config.ts, öffentliche Informationsseiten, Newsletter, Kategorien und Themen verwenden Linknarr. Historische Plattformnamen in DB-Inhalten werden ausschließlich für die Anzeige normalisiert (lib/branding.ts, lib/tools/public.ts, lib/content-hub.ts, Blogdetail).
- Visuell: geometrische SVG-Wortmarke linknarr., Favicon l., Acid-Lime #D0FF28, Header/Footer und Open-Graph-Bild. Heller Modus mit dunkler Wortmarke. assets: public/brand, lib/brand-assets.ts, components/brand*.tsx.
- Technik: Startseite reduziert unnötige DB-Abfragen; Newsletter-Einstieg, News mit Primärquellen, Top-20-Seitenleiste, Vergleiche und Business-Themen. Direkte Filter, sichtbare Kategorien und Sortierung vor den Ergebnissen; älteste Einträge nach Anlagezeit. Bestehende Suchparameter und fortgeschrittene Filter bleiben erhalten.
- SEO: zentrale Metadaten, strukturierte Daten und Titel auf Linknarr; doppelte Markennennung im Startseiten-/Tooltitel verhindert. Domain und Slugs bleiben erhalten.
- Affiliate: lib/affiliate/redirect.ts, go.ts, Toolkarten/-details und Admin verwenden dieselbe Gültigkeitsprüfung. Kein Original-URL-Fallback, kein Umgehen über ziel=offiziell. Fehlender Affiliate-Link wird intern gekennzeichnet. Historische Klickzählungen bleiben erhalten; gespeicherte URLs und Parameter werden nicht geändert.

## Daten und Inhalte
Keine neuen produktiven Tool-Datensätze, keine bestehenden Datensätze überschrieben oder gelöscht, keine neue Migration. Testdaten ausschließlich in isolierter lokaler DB. Drei eigenständige deutsche News-Zusammenfassungen nach geprüften Microsoft-/Anthropic-Originalmeldungen vom 22./28.10.2026; Originalquellen stehen direkt in jeder Meldung. Keine erfundenen Leserzahlen, Firmenempfehlungen oder übernommenen Fremdbilder. Linkjagd bleibt Social-Media-Marke; Route, Videozuordnungen und Navigation „Bekannt aus Linkjagd“ bleiben erhalten.

## Lokale Prüfung
- npm test: 118 Tests in 56 Dateien erfolgreich, inklusive Regressionen für fehlende/inaktive/ungültige Affiliate-Links, exakte Weiterleitungsparameter, Karten, Markenanzeige, Mail-Branding, Newsdatierung und älteste Sortierung.
- npm run lint: erfolgreich.
- npm run build: erfolgreich auf isolierter SQLite-Kopie; keine produktiven Zugangsdaten verwendet. Abschließende Darstellungsänderungen werden vor Veröffentlichung erneut gebaut.
- 14 Kern-/Asset-URLs mit HTTP 200: /, /tools, /blog, /linkjagd, /vergleiche, /kategorien, /newsletter, /news, zwei lokale Toolprofile, /robots.txt, /sitemap.xml, /icon.svg, /opengraph-image.
- Weiterleitung per HEAD: gültiger Testpartnerlink 302 mit unveränderten %2B-/Leerzeichenparametern, fehlender Partnerlink 404, ziel=offiziell 404. Profile ohne Partnerlink bleiben 200 und haben keine Anbieterlinks, auch mobil.
- Browser: Suche, Preis und Kategorie kombiniert, älteste Sortierung erhält Filter; Desktop 1440, Mobil 390 und 320 ohne horizontalen Überlauf; Menü und Escape; Dunkel-/Hellmodus. Keine JavaScript-Ausnahmen in der geprüften öffentlichen Oberfläche.

## Produktion
Vor Veröffentlichung: Vercel bestätigt linknarr.com am bestehenden Projekt, verifiziert und nicht fehlkonfiguriert. NEXT_PUBLIC_SITE_URL ist bereits https://linknarr.com. Lokaler DNS-Resolver lieferte noch 217.160.0.18 (nginx 404); HTTPS an der von Vercel bestätigten Ziel-IP 216.198.79.1 mit unverändertem Host und TLS-Namen war 200. DNS wurde nicht verändert.

Release- und abschließende Produktionsergebnisse werden nach dem Deployment ergänzt. Lokale Testprofile existieren nicht in Produktion. Newsletter-Anmeldung bleibt geschlossen; vorhandene Bestätigungs-/Versandlogik bleibt erhalten.
