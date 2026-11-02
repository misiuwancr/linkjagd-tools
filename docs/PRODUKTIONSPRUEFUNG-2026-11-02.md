# Produktionsprüfung Linkjagd Tools

Stand: 2. November 2026. Umfang: öffentliche Navigation, öffentliche Routen, Kernfunktionen, mobile Darstellung, Rechtstexte und die bereits vorbereiteten Vergleichsseiten. Keine neue Produktfunktion, kein Redesign, kein Datenimport und keine neue Migration.

## Nachgewiesene Befunde und Korrekturen

| Datei | Änderung und Anlass |
| --- | --- |
| `db/http.ts` | Zustandsbehaftete Hrana-Datenbankantworten ausdrücklich mit `cache: "no-store"` abfragen; verhindert Wiederverwendung von Stream-/Sitzungsantworten durch Next.js. |
| `tests/db-retry.test.ts` | Regressionstest für frische Datenbankantworten, auch bei übergebenem `force-cache`. |
| `components/site-header.tsx` | Keine Anmeldung verlinken, wenn der Versanddienst fehlt; leeres Newsletter-Archiv aus Navigation entfernt; KI-News nur bei vorhandenen Meldungen; mobiles Menü mit voller dynamischer Viewport-Höhe und eigenem Scrollbereich. |
| `app/(public)/layout.tsx` | Tatsächliche Newsletter-/News-Verfügbarkeit serverseitig an Navigation übergeben; keine Zugangsdaten an Client übergeben. |
| `components/site-footer.tsx` | Leeres Newsletter-Archiv entfernt; Entwicklungs-/Qualitätsbehauptung durch Link zur Partnertransparenz ersetzt. |
| `components/newsletter-form.tsx` | Geschlossene Anmeldung rendert kein unfertiges Formular und keine Entwicklungsinformation. Versandfunktion selbst erhalten. |
| `components/vote-button.tsx` | Deaktiviertes oder nicht erreichbar gemeldetes Voting rendert keine deaktivierte Schaltfläche und keinen unfertigen Hinweis. Funktionierendes Voting bleibt verfügbar. |
| `components/ai-news.tsx` | Leerer News-Block auf Startseite ausgeblendet; bestehende Route erhalten. |
| `app/(public)/newsletter/page.tsx` | Bestehende URL erhalten, verständlicher Verfügbarkeitshinweis und funktionierender Blog-Link. Keine Anmeldung ohne Versanddienst. |
| `app/(public)/page.tsx` | Newsletter-Block bedingt anzeigen; interne Implementierungshinweise entfernen; Abschnittsköpfe auf schmalen Displays umbrechen lassen; Grid-Inhalt kann schrumpfen. |
| `components/legal.tsx` | Allgemeines „Platzhalter“-Etikett durch „Rechtliche Informationen“ ersetzt; konkrete offene Angaben bewusst erhalten. |
| `site.config.ts` | Arbeitsphasen-/lokale Datenbankinformationen entfernt; Affiliate-Beschreibung an mehrere direkte Anbieterlinks angepasst, unbelegte Aufpreis-Zusage entfernt; tatsächliche lokale Speicherung, Videoaktivierung und freiwillige Einreichungsadresse beschrieben. Keine Betreiberangaben erfunden. |
| `app/(public)/impressum/page.tsx` | Metabeschreibung als unvollständige Anbieterangaben formuliert. |
| `app/(public)/kontakt/page.tsx` | Öffentliche Arbeitsanweisung entfernt; fehlende E-Mail transparent und vorhandenes Einreichungsformular verlinkt. |
| `app/(public)/einreichen/page.tsx` | Datenschutzhinweise unmittelbar am funktionierenden Einreichungsformular ergänzt. |
| `docs/RECHTLICHE-ANGABEN-OFFEN.md` | Separate Betreiber-Prüfliste für Impressum, Datenschutz, Affiliate und Aktivierung ruhender Funktionen. |
| `docs/PRODUKTIONSPRUEFUNG-2026-11-02.md` | Dieser Ergebnis- und Dateibericht. |

Die früher vorbereiteten Vergleichsänderungen stehen ebenfalls in PR #10. Deren Inhalt, betroffene Dateien und Quellen sind im PR-Diff und in `docs/ENTSCHEIDUNGSPLATTFORM-PRUEFUNG.md` dokumentiert.

## Nachweise

- `npm test`: 99 Tests in 49 Dateien erfolgreich.
- `npm run lint`: keine ESLint-Warnungen oder -Fehler.
- Abschließender `npm run build`: erfolgreich, einschließlich Typprüfung. Node 22; ausschließlich isolierte lokale SQLite-Prüfdatenbank, keine Remote-Zugangsdaten.
- 17 öffentliche Kernseiten inklusive Recht, Kontakt, Newsletter, Merkliste, Einreichung und allen drei Vergleichen: HTTP 200. Daraus 175 interne Linkziele: kein fehlerhafter Status. Keine sichtbaren untersuchten Entwicklungs-/Voting-/Versanddienst-Fehlermarker.
- Mobil bei 320 Pixeln: Startseite, Verzeichnis, ChatGPT- und WooCommerce-Profil, Blog, Vergleichsübersicht und alle drei Vergleiche ohne horizontalen Seitenüberlauf. Tabellen 720 Pixel breit innerhalb eigener Scrollbereiche.
- Zusätzlich 390 Pixel: Startseite, Verzeichnis, Detailseite, Blog und Shopify-Vergleich ohne horizontalen Seitenüberlauf; keine Browser-Fehler in der Prüfsitzung.
- Mobiles Menü bei 320 × 740: eigener Scrollbereich, volle Höhe, alle Links erreichbar. Newsletter und leere News fehlen in der Navigation.
- Suche „Zapier“ über Startseitenformular liefert das vorhandene Tool; Merken → Merkliste zeigt ChatGPT nach Seitenwechsel. Funktionierende Kernfunktionen erhalten.

## Grenzen und verbleibende Probleme

- Rechtliche Vollständigkeit ist nicht erreicht: Anbieteranschrift, bestätigter Kontakt und die weiteren Punkte der separaten Prüfliste fehlen. Veröffentlichung dieser technischen Korrekturen ersetzt deren Ergänzung nicht.
- Der lokale Datenbestand enthält 1.527 veröffentlichte Tools, aber nicht sämtliche produktiven Blog-/Kategoriezuordnungen und Redaktionseinstellungen. Deshalb werden lokale Inhaltshäufigkeit oder Reihenfolge nicht als Beleg für Produktionsdaten verwendet; bestehende Daten werden nicht überschrieben.
- Newsletter ist in der geprüften Produktion geschlossen, Voting deaktiviert, KI-News ohne Einträge. Direkte URLs bleiben erhalten. Vor Aktivierung müssen Versand, Abmeldung, Speicherfristen und Rechtsgrundlagen fachlich abgeschlossen werden.
- Kein vollständiger manueller Produkttest aller rund 1.500 Anbieter. Anbieterpreise, Erreichbarkeit externer Websites und bestehende redaktionelle Prüfnotizen bleiben Gegenstand laufender Inhaltsprüfung; keine Datenbereinigung auf Verdacht.
- Bestehende Hinweise zur Vite-CJS-API beim Testlauf und zur Edge-Runtime bei der Next-Generierung bleiben ohne neuen Build-Fehler bestehen.
- Öffentliche Sitemap vor Veröffentlichung: 1.651 URLs geprüft, 21 zeitweise HTTP 500. Beim gezielten GET-Nachtest waren 19 wieder HTTP 200, zwei Sammlungen weiterhin HTTP 500. Vercel-Protokolle belegen Turso/libSQL HTTP 400. Lokal waren beide Sammlungen HTTP 200. Der Transportcache wurde als plausible Ursache korrigiert; der Produktionsnachtest entscheidet über die Wirksamkeit.
- Grundlage der Transportkorrektur: [Next.js 14 dokumentiert auch POST-Caching und no-store](https://nextjs.org/docs/14/app/building-your-application/data-fetching/fetching-caching-and-revalidating). Ein HTTP-Erreichbarkeitstest ersetzt keine fachliche Inhaltsprüfung aller Tools.

Es folgen nach der Veröffentlichung keine weiteren Produktänderungen ohne neuen Auftrag.
