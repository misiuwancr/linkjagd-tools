# Verzeichnis und redaktionelle Entdeckung

Stand: 2. November 2026. Beide Folgeaufträge sind auf dem bestehenden Next.js-/Drizzle-Projekt umgesetzt. Die bestehenden rund 1.500 Tool-Datensätze, Vergleichsartikel, Tool-URLs, Rechtseiten und Produktionskorrekturen bleiben erhalten. Keine neue Datenbank, keine Migration, kein Import, keine neue Dependency und kein zweites CMS.

## Ist–Soll-Abgleich

Bereits vorhanden waren GET-Suche, Preis-/Lizenzfilter, Kategorien, mehrere Sortierungen, 24 Karten pro Seite, Preis-/Kategorie-Badges, vorhandene Video-URL-Felder, ein Empfehlungsfeld und eine geschützte Verwaltung. Die bestehende Suche behandelte mehrere Wörter als zusammenhängende Zeichenfolge. Ihr gespeicherter Index war durch die Slug-Normalisierung stark gekürzt. Mehrere Kategorien waren nicht gemeinsam auswählbar; die Hauptseite bot teils doppelte Filterbedienungen.

Die öffentliche [FutureTools-Verzeichnisseite](https://futuretools.io/tools) wurde als Referenz für zentrale Suche, kompakte Auswahlmöglichkeiten, erkennbare Empfehlungen und paginierte Karten geprüft. Linkjagd übernimmt diese Bedienprinzipien, aber keine Texte, Datensätze, Logos, Grafiken, Quelltexte oder identische Gestaltung. Linkjagd bleibt thematisch breiter als die Referenz.

## Änderungen am Verzeichnis

- Eigenständige, deutlich größere zentrale Suche. Preis, Lizenz, Kategorien, Sortierung und Zusatzfilter befinden sich in einem GET-Formular und werden gemeinsam angewendet. Keine Anfrage bei jedem Tastendruck.
- Mehrere Kategorien als ODER: mindestens eine ausgewählte Kategorie muss passen. Suchbegriffe, Preis, Lizenz und Zusatzfilter wirken zusätzlich als UND. Wiederholte `kategorie`-Parameter erhalten alte Einzelkategorie-URLs und erlauben teilbare Mehrfachauswahlen.
- Aktive Filter einzeln entfernen; alles zurücksetzen; verständlicher Nulltrefferzustand mit Link zum vollständigen Verzeichnis. Nicht zur Suche passende allgemeine Empfehlungen werden während einer gefilterten Suche ausgeblendet.
- Wortweise Suche unabhängig von Reihenfolge; vorhandene Beschreibungen werden zusätzlich durchsucht. Neue oder redaktionell gespeicherte Suchindizes dürfen länger sein; alte Produktionszeilen werden nicht massenweise neu geschrieben.
- Stabile Sortierung mit eindeutiger Zweitsortierung; paginierte Datenbankabfrage bleibt auf 24 Karten begrenzt. Erste und letzte Seite sind erreichbar, Auswahl bleibt beim Seitenwechsel erhalten.
- Einheitliche Karten mit vorhandenen Logos, Namen, bis zu drei Beschreibungszeilen, Kategorie/Preis und getrennten Detail-/Anbieter-Links. Keine neuen Preisbehauptungen oder Bewertungen.
- Normalisierte Canonicals enthalten gültige Filter und Seiten. Suchergebnisse und neue Mehrfachkategorie-Kombinationen werden nicht indexiert; der globale Produktionsstatus und bestehende Einzelkategorie-URLs werden nicht umgeschaltet.

## Redaktionelle Bedienung

1. In der vorhandenen Redaktion unter **Tools** nach dem Namen suchen. Die Liste hat jetzt Suche und Seitennavigation, damit auch Einträge hinter den früheren ersten 100 erreichbar sind.
2. Vorhandenes Tool öffnen und **Linkjagd-Empfehlung (Bereich „Unsere Empfehlungen“)** setzen oder entfernen. Speichern. Die dynamische Startseite und `/empfehlungen` verwenden ausdrücklich dieses Datenbankfeld. Die separate bestehende Top-20-Auswahl bleibt erhalten; sie wird nicht als manuell gesetztes Empfehlungs-Häkchen in das Formular geschrieben.
3. Unter **Linkjagd-Videos und Veröffentlichung** auf **Video zuordnen** klicken. Kennung und Titel angeben; Teilnummer und öffentlicher HTTPS-Link sind optional. Bis zu 20 Zuordnungen pro vorhandenem Tool; keine Tool-Kopie erforderlich. Kennungen pro Tool müssen eindeutig sein. Für dasselbe Video über mehrere Tools hinweg dieselbe Kennung und konsistente Titel/Teilnummern verwenden.
4. Speichern. Die Zuordnung erscheint unter `/linkjagd`, in Tool-Karten und auf der bestehenden Detailseite. Besucher können nach Teilnummer, Titel oder Kennung suchen, ein bestimmtes Video auswählen und zusätzlich nach Tool/Aufgabe suchen. Die Auswahl bleibt in den Pagination-URLs erhalten.
5. Eine Zuordnung kann auch ohne öffentlichen Link veröffentlicht werden. In diesem Fall gibt es keinen erfundenen Video-Link oder leeren Video-Button. Links laden keine Social-Media-API und werden nicht automatisch eingebettet.

Die vier Startbereiche **Bekannt aus Linkjagd**, **Unsere Empfehlungen**, **Neu hinzugefügt** und **Tools für Business & E-Commerce** werden aus vorhandenen veröffentlichten, nicht als Beispiel markierten Daten erzeugt. Leere Bereiche erhalten einen nutzbaren Verzeichnis-/Sammlungslink, keine fiktiven Karten. Die drei bestehenden Business-Vergleiche und die Aufgaben-Einstiege bleiben verlinkt.

## Veröffentlichungsdaten

- Die bisherige Tool-Tabelle hat kein belegtes Veröffentlichungsdatum. Das Import-/Erstellungsdatum wird daher nicht umgedeutet.
- Redaktionelle Zusatzdaten liegen validiert als JSON unter `site_settings`, Schlüssel `tool_editorial:<tool-id>`. Das vorhandene Export-/Backupverfahren umfasst diese Tabelle bereits. Keine Schemaänderung erforderlich.
- `publishedAt` wird bei erstmaliger Freigabe eines bislang unveröffentlichten Entwurfs erfasst, sowohl beim Speichern des Formulars als auch über die vorhandene Statusaktion.
- Ein Veröffentlichungsmarker verhindert, dass ein bearbeiteter oder vorübergehend zurückgezogener alter Eintrag ohne belegtes Datum nachträglich künstlich als neu erscheint. Vorhandene Daten bleiben bei Bearbeitung und erneuter Freigabe erhalten.
- Alte Veröffentlichungstage können anhand eigener Nachweise manuell ergänzt werden. Unbekannte Daten bleiben leer; Zukunftsdaten und ungültige Daten werden zurückgewiesen.
- `/neu` und der entsprechende Startbereich enthalten ausschließlich veröffentlichte Tools mit belegtem, nicht zukünftigem Datum. Im vollständigen Verzeichnis folgen Einträge ohne Datum hinter den belegten Veröffentlichungen; sie bleiben suchbar.

## Prüfungen

- 104 Tests in 51 Dateien erfolgreich; Lint ohne Warnungen/Fehler; Produktionsbuild inklusive Typprüfung erfolgreich.
- Neue Datenbanktests: kombinierte Mehrfachkategorien, Preis/Lizenz, vertauschte Suchwortfolge, lange Beschreibungen trotz Altindex, Nulltreffer, keine doppelten Karten, stabile Pagination und überhöhte Seitenzahl.
- Neue Redaktionstests: bestehende Tools zuordnen, Entwürfe ausschließen, Video-/Teilnummernsuche, Empfehlungen setzen und entfernen, automatische Erstveröffentlichung, kein falsches Datum nach Bearbeitung/Wiederfreigabe, keine neuen Tool-Zeilen, ungültige Metadaten und URLs abweisen.
- Browser: Suche „Bilder“ + Kostenlos + Open Source + zwei Kategorien + Alphabetisch; Auswahl in URL und Formular erhalten. Einzelne Kategorie entfernen, Zurücksetzen und Nulltreffer erfolgreich geprüft.
- Browser: isolierte lokale Datenbankkopie und temporäres Testkonto. Ein bestehendes Tool wurde als Empfehlung markiert und einem ausdrücklich als lokalem Test gekennzeichneten Video zugeordnet. Speichern, öffentliche Teilnummernsuche, Empfehlungsseite und Detailseite wurden geprüft. Keine Testzuordnungen oder Testkonten wurden in Produktionsdaten geschrieben oder committed.
- Beim Speichern wurde ein bestehender Fehler mit kurzzeitig undefiniertem Formularzustand gefunden und korrigiert; anschließendes Speichern zeigt wieder „Gespeichert.“.
- Mobile Prüfung bei 320 Pixeln: Verzeichnis, Startseite, Videosammlung, Empfehlungen, neue Veröffentlichungen, Tool-Detailseite und Vergleichsübersicht ohne horizontalen Seitenüberlauf. Desktop-Formular und Such-/Filterablauf ebenfalls geprüft.

## Verbleibende Grenzen

- Echte Video-Kennungen, Titel, Teilnummern und gegebenenfalls historische Veröffentlichungsdaten müssen vom Betreiber zugeordnet werden. Ohne Nachweise werden keine Inhalte vorgefüllt. Deshalb kann `/neu` zunächst wenige oder keine Treffer enthalten.
- Vorhandene Tool-Beschreibungen und Preismodelle wurden nicht in einem neuen vollständigen Produkttest verifiziert. Der neue Code erfindet oder überschreibt diese Angaben nicht.
- Suche ist eine begrenzte, parametrisierte Datenbankabfrage mit Wortteil-/Wortkombinationssuche, keine semantische KI-Suche und keine garantierte Tippfehlerkorrektur. Keine zusätzliche Infrastruktur erforderlich.
- Kategorieanzahlen beziehen sich auf alle veröffentlichten Einträge der Kategorie, nicht auf eine dynamische Facettenzählung nach jeder Auswahl.
- Die bisherigen offenen rechtlichen Angaben bleiben in `docs/RECHTLICHE-ANGABEN-OFFEN.md` dokumentiert; Newsletter und Voting werden nicht aktiviert.
- Diese beiden Folgeaufträge werden als neuer Pull Request bereitgestellt. Die frühere Produktionsfreigabe wurde nicht als automatische Freigabe aller späteren Produktänderungen behandelt.

## Abschließender Linkcheck

14 Kern-/Filteransichten und daraus 171 interne Linkziele am Produktionsbuild geprüft: alle HTTP 200. Darunter die drei vorhandenen Vergleichsseiten, kombinierte Filter, Pagination, Nulltreffer und neue Sammlungsseiten.

## Geänderte Dateien

- `app/(public)/empfehlungen/page.tsx`
- `app/(public)/linkjagd/page.tsx`
- `app/(public)/neu/page.tsx`
- `app/(public)/page.tsx`
- `app/(public)/tools/[slug]/page.tsx`
- `app/(public)/tools/page.tsx`
- `app/admin/(panel)/moderation/page.tsx`
- `app/admin/(panel)/tools/[id]/page.tsx`
- `app/admin/(panel)/tools/page.tsx`
- `app/sitemap.ts`
- `components/admin/tool-editorial-fields.tsx`
- `components/admin/tool-form.tsx`
- `components/decision-tool-page.tsx`
- `components/directory-search.tsx`
- `components/directory.tsx`
- `components/linkjagd-tool-videos.tsx`
- `components/site-footer.tsx`
- `components/site-header.tsx`
- `components/tool-card.tsx`
- `docs/VERZEICHNIS-UND-LINKJAGD-ENTDECKUNG.md`
- `lib/actions/admin.ts`
- `lib/labels.ts`
- `lib/tool-editorial.ts`
- `lib/tools/mutations.ts`
- `lib/tools/public.ts`
- `lib/tools/query.ts`
- `lib/tools/repository.ts`
- `lib/utils.ts`
- `lib/validation/tool.ts`
- `site.config.ts`
- `tests/directory-discovery.test.ts`
- `tests/tool-editorial.test.ts`
