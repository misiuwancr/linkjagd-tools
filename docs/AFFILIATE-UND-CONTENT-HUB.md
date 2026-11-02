# Affiliate-Messung und Content-Hub

Stand: 2. November 2026. Erweiterung der bestehenden Weiterleitung, Auswertung und Blog-Verwaltung. Keine neue Datenbank, Migration, Dependency, Trackingplattform, Social-Media-Integration oder automatisch erzeugte Artikel. Vorherige Vergleiche und Verzeichnis-/Linkjagd-Struktur bleiben erhalten.

## Bestandsaufnahme

`/go/[slug]` nutzte bereits gespeicherte offizielle URLs bzw. aktive Partnerprogramme, URL-Prüfung und Tageszähler in `click_daily`. Parameter wurden nicht an Anbieter angehängt. Die geschützte Klickseite hatte 7-/30-Tage-Summen. Fehlend waren Quellseite und CTA-Position. Ein JOIN auf mehrere Partnerprogramme konnte Tool-Summen vervielfachen; die Auswertung verwendet jetzt unabhängige Aggregationen.

Der Blog hatte Datenbankartikel, Markdown, Entwürfe, Veröffentlichung, SEO-Felder, Canonicals, strukturierte Daten und Pagination. Drei Vergleichs-URLs haben weiterhin Vorrang durch ihre vorhandenen Code-Templates. Themenbereiche, explizite Tool-/Artikel-Verknüpfungen und gekennzeichnete Anbieterlinks fehlten. Beim Bearbeiten eines veröffentlichten Artikels wurde zuvor das Publikationsdatum überschrieben.

## Weiterleitung und Verwaltung

- Bestehende `/go`-Adressen funktionieren unverändert. Das Ziel kommt ausschließlich aus dem vorhandenen Tool bzw. einem aktiven gespeicherten Partnerprogramm. Ein übergebenes `url`-/`destination`-Feld wählt kein Ziel aus.
- `ziel=offiziell` erlaubt nur die bereits gespeicherte offizielle Adresse; keine freie Zielauswahl. Aktivierte Programme werden nach gespeicherter Priorität und bei Gleichstand deterministisch nach ID ausgewählt. Ungültige/deaktivierte Programme bleiben ausgeschlossen; ohne gültigen Partnerlink wird die geprüfte offizielle Adresse verwendet.
- Offizielle Anbieter-URL und Partnerlinks werden weiterhin im vorhandenen Toolformular gepflegt. Eine Vorschau zeigt den tatsächlich gewählten Zieltyp, die Adresse und gegebenenfalls Programmkennung.
- Affiliate-Kennzeichnung folgt dem tatsächlich ausgewählten aktiven Programm. Vergleichs-CTAs, relevante Tool-Karten und Artikel-Anbieterlinks verwenden dieselbe Weiterleitung; Partnerstatus ändert keine redaktionelle Einordnung.
- Weiterleitungen senden `Cache-Control: no-store`, `X-Robots-Tag: noindex, nofollow` und `Referrer-Policy: no-referrer`. HEAD und erkennbare Prefetch-Aufrufe werden nicht gezählt. Ein Fehler beim Zählen verhindert den bestehenden Redirect nicht.
- Bestehende eigenständige Werbebanner bleiben erhalten. Sie sind als Anzeige markiert und werden nicht fälschlich als Tool-Klick einem erfundenen Tool zugewiesen.

## Datensparsame Messung

Ein tatsächlicher GET-Aufruf des vorhandenen Endpunkts aktualisiert atomar den bestehenden Gesamttageszähler und eine dimensionierte Tagesaggregation. Dies sind zwei Ansichten desselben Aufrufs, keine zwei addierbaren Ereignisse. Die neue Dimensionierung nutzt die bereits vorhandene `site_settings`-Tabelle unter `click_context:`; keine produktive Migration nötig.

Gespeicherte Felder: Tool-ID, tatsächliche Programm-ID oder null, Zieltyp offiziell/affiliate, UTC-Tag, freigegebener Quellpfad, CTA-Positionsklasse und Anzahl. Keine IP, User-Agent, E-Mail, Personen-/Sitzungskennung, vollständige Referrer, Suchbegriffe, URL-Filter, Cookie oder Einzelereignis-Zeitstempel.

Quellen sind feste öffentliche Bereiche oder validierte veröffentlichte Tool-/Artikel-/Kategoriepfade. Unbekannte Quellen/Positionen werden zu `unbekannt`/`unknown`, nicht als beliebiger Text gespeichert. Die Quelle stammt aus einem instrumentierten Link und lässt sich technisch nachbilden; sie ist kein manipulationssicherer Herkunftsnachweis. Wiederholungen oder nicht erkannte automatische Aufrufe können enthalten sein. Es sind Anbieter-Aufrufe, keine Besucherzahlen, Käufe, Umsätze oder Conversion-Raten.

Neue Detailzuordnungen beginnen erst ab dieser Veröffentlichung. Historische Gesamtsummen bleiben erhalten; fehlende historische Quellen werden nicht erfunden. Vorhandene Daten werden nicht automatisch gelöscht. Eine rechtlich geprüfte Aufbewahrungsfrist bleibt festzulegen.

`/admin/klicks` ist sowohl über die bestehende Middleware/Layout-Anmeldung als auch explizit im Seitenhandler geschützt. Es zeigt meistgeklickte Tools, Quellen und Positionen, offizielle/Partnerziele sowie redaktionelle Artikel und Klicks aus Linkjagd/Sammlungen. Die Detailtabelle zeigt bis zu 200 Kombinationen; Bereichssummen berücksichtigen alle Gruppen. Keine öffentliche Statistik-API.

## Redaktionelle Bedienung

1. Unter **Redaktion → Blog** einen bestehenden Beitrag öffnen oder einen Entwurf anlegen. Titel, Kurzname, Teaser, Text und optionale SEO-/Quellenfelder bleiben dieselben.
2. Themenbereich **Entdecken**, **Vergleiche & Anleitungen** oder **News** wählen. Bestehende Artikel ohne zusätzliche Metadaten erhalten eine vorsichtige, anhand des Slugs vorgeschlagene Themenzuordnung; sie kann redaktionell überschrieben werden.
3. Vorhandene veröffentlichte Tool-Kurznamen sowie optional verwandte Artikel-Kurznamen eintragen. Nicht existierende Tool-Verknüpfungen, Selbstverweise und doppelte Artikel-URLs werden abgewiesen. Entwürfe werden öffentlich nicht verlinkt.
4. Im Markdown funktionieren `[Tool-Profil](/tools/zapier)` und `[Zum Anbieter](/go/zapier)`. Der zweite Link wird zur gespeicherten offiziellen oder aktiven Partneradresse aufgelöst. Nur ein tatsächlich aktiver Partnerlink erhält **Anzeige** sowie `rel="sponsored nofollow"`. Keine Partnerparameter von Hand erfinden. Unbekannte `/go`-Tools erzeugen keinen ausgehenden Link.
5. Nach fachlicher Prüfung veröffentlichen. Das Datum der ersten Veröffentlichung bleibt bei späteren Bearbeitungen erhalten; das Änderungsdatum wird separat ausgegeben. Die drei codebasierten Vergleichsseiten werden weiter im Code gepflegt und können nicht versehentlich im Blogformular überschrieben werden.

Metadaten liegen unter `post_editorial:<id>` in der vorhandenen Einstellungstabelle; der bestehende Datenexport umfasst sie. Der öffentliche Hub führt Datenbankartikel und die drei vorhandenen Vergleiche ohne doppelte Slugs zusammen, filtert nach Thema und paginiert mit 24 Artikeln. Artikel verlinken veröffentlichte Tool-Profile und verwandte Artikel, Tool-Profile verlinken zurück. Neue passende Artikel werden nicht automatisch erzeugt. Die separate vorhandene News-Route bleibt erhalten; neue redaktionelle News werden manuell als Blog-Thema veröffentlicht.

## SEO und technische Prüfung

- Globale Indexierungsregeln, robots.txt und Sitemap-Grundstruktur unverändert. Admin/API/Weiterleitungen bleiben ausgeschlossen; veröffentlichte Tool-/Kategorie-/Artikel-/Vergleichs-URLs bleiben erhalten.
- Blog-Themen und Seiten erhalten normalisierte Canonicals ohne nicht verwendete Such-/Filterparameter. Pagination behält den Themenfilter. Artikel- und Vergleichs-Canonicals bleiben bei ihren vorhandenen Slugs.
- BlogPosting enthält vorhandenes Publikationsdatum, tatsächliches Änderungsdatum, Themenbereich und zentralen Markennamen; keine erfundenen Autoren, Produkttests, Sterne oder Bewertungen.
- Markdown bleibt HTML-escaped, blockiert gefährliche Protokolle und protokollrelative Links und unterstützt sichere interne Verknüpfungen. Inhaltliche H1-Zeilen werden als H2 gerendert, damit der Seitentitel die einzige H1 bleibt.
- 108 Tests in 52 Dateien erfolgreich; Lint ohne Warnungen/Fehler; Produktionsbuild inklusive Typprüfung erfolgreich. Neue Regressionstests prüfen parallele Zähler, Mehrfachprogramme ohne Überzählung, Quellvalidierung, sichere Ziele, Head-/Prefetch-Ausnahme, datensparsame Felder, Themen-Pagination, vorhandene Tool-Verknüpfungen, Datumerhalt, geschützte Vergleichsslugs und Affiliate-Markdown.
- Lokaler End-to-End-Test in separater Datenbankkopie: Prüfartikel über vorhandene Verwaltung veröffentlicht; Profil-Rückverweis, verwandter Vergleich, instrumentierter Anbieterlink und geschützte Statistik geprüft. Zwei GET-Aufrufe ergeben zwei Klicks; zusätzlicher HEAD-Aufruf erhöht nichts. Kein Set-Cookie am Redirect. Anonyme Statistik-Anfrage wird zur Anmeldung umgeleitet.
- Mobile Browserprüfung bei 320 Pixeln: Hub, Themenfilter, normaler Artikel, bestehender Vergleich und Tool-Profil ohne horizontalen Seitenüberlauf. Keine Prüfartikel, Testpartnerschaften oder Testklicks in Produktionsdaten übertragen.

## Vom Betreiber weiter zu prüfen

- Tatsächliche Partnerprogramme und Vertragsbedingungen, erlaubte Kennzeichnung und Zieladressen bestätigen. Das System legt keine Partnerschaft an und verifiziert keinen bestehenden Vertrag automatisch.
- Rechtsgrundlage, Informationspflichten, Aufbewahrungsfrist der aggregierten Zähler und getrennte Hosting-Protokollierung fachlich prüfen. Die Datenschutzhinweise wurden sachlich ergänzt und offene Angaben gekennzeichnet; keine Rechtskonformitätszusage.
- Artikeltexte, Themenzuordnungen, Quellen, Tarife und Produktfunktionen bleiben redaktionell zu prüfen. Die Verknüpfung mit einem Tool bedeutet keinen eigenen Produkttest.
- Klickzahlen allein belegen keine Wirtschaftlichkeit oder Verkäufe. Es gibt bewusst keine Nutzerprofile oder Conversion-Verfolgung.

## Geänderte Dateien

- `app/(public)/alternativen/[slug]/page.tsx`
- `app/(public)/blog/[slug]/page.tsx`
- `app/(public)/blog/page.tsx`
- `app/(public)/empfehlungen/page.tsx`
- `app/(public)/fuer/[slug]/page.tsx`
- `app/(public)/kategorien/[slug]/page.tsx`
- `app/(public)/linkjagd/page.tsx`
- `app/(public)/neu/page.tsx`
- `app/(public)/page.tsx`
- `app/(public)/tools/[slug]/page.tsx`
- `app/(public)/top-20/page.tsx`
- `app/admin/(panel)/blog/page.tsx`
- `app/admin/(panel)/klicks/page.tsx`
- `app/admin/(panel)/tools/[id]/page.tsx`
- `app/go/[slug]/route.ts`
- `components/admin/tool-form.tsx`
- `components/article-connections.tsx`
- `components/comparison-page.tsx`
- `components/decision-tool-page.tsx`
- `components/directory.tsx`
- `components/provider-link.tsx`
- `components/tool-card.tsx`
- `docs/AFFILIATE-UND-CONTENT-HUB.md`
- `lib/actions/content.ts`
- `lib/affiliate/context.ts`
- `lib/affiliate/go.ts`
- `lib/affiliate/redirect.ts`
- `lib/blog-metadata.ts`
- `lib/content-hub.ts`
- `lib/markdown.ts`
- `lib/tools/mutations.ts`
- `lib/tools/query.ts`
- `lib/tools/repository.ts`
- `lib/validation/tool.ts`
- `site.config.ts`
- `tests/affiliate-content.test.ts`
