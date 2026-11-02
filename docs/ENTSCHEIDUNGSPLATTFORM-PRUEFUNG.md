# Entscheidungshilfen – fachliche Prüfung

Stand der Recherche: 2. November 2026. Grundlage sind gelesene offizielle Anbieterinformationen; keine eigenen Produkttests und keine rechtliche oder vertragliche Zusage. Alle Quellen sind außerdem direkt an den Profilen und Vergleichen verlinkt.

## Bestandsprüfung und URLs

Die öffentliche Sitemap und beide Seiten der Blog-Liste wurden geprüft. Sie enthalten 25 Blogartikel. Der bestehende Artikel `/blog/zapier-make-n8n-vergleich` wird unter derselben URL durch das gemeinsame Vergleichstemplate verbessert. In seiner bisherigen Fassung standen konkrete Gratiskontingente, ein n8n-Preis und pauschale Aussagen wie „volle Kontrolle über deine Daten“; diese Aussagen werden in der neuen Darstellung nicht übernommen.

Für Shopify/WooCommerce und Newsletter-Tools fanden sich keine bestehenden Vergleichsartikel. Neue kanonische Artikel:
- `/blog/shopify-vs-woocommerce`
- `/blog/newsletter-tools-kleine-unternehmen`

`/vergleiche` ist die Übersicht, keine zweite Kopie der Artikel. Die Sitemap führt bestehende Blog- und neue Vergleichs-URLs zusammen und entfernt doppelte Slugs. Der globale Indexierungsstatus bleibt unverändert.

Die bestehende Sammlung `/fuer/newsletter` bleibt eine Verzeichnis-Sammlung. Sie ist kein gleichartiger Vergleich und wird nicht ersetzt. Die übrigen Blogartikel bleiben unverändert.

## Vor fachlicher Freigabe durch Michał

| Bereich | Bereits anhand offizieller Quellen eingeordnet | Noch für den konkreten Anwendungsfall zu verifizieren |
| --- | --- | --- |
| Zapier | Ereignis-/Aktionsmodell und App-Verzeichnis | Benötigte Trigger/Aktionen, Tarifgrenzen und Prozessverbrauch; Fehler, Wiederholungen und doppelte Ereignisse in einem Pilot prüfen |
| Make | Visuelle Szenarien sowie dokumentierte Router/Filter | Daten-Mapping, Fehlerpfade, Reihenfolge, notwendige Integrationen und realer Verbrauch im Pilot |
| n8n | Cloud und Selbstbetrieb; Betrieb benötigt Verantwortung | Aktuelle Lizenz-/Editionsbedingungen für den geplanten geschäftlichen Einsatz; Backup, Updates, Monitoring und Datenflüsse zu externen Diensten |
| Shopify | Shop-Plattform mit Themes, Apps und Einrichtungsdokumentation | Zahlungsarten, Gebühren, Apps, Produktvarianten, Versand und Schnittstellen; Testkauf durchführen und Gesamtangebot einholen |
| WooCommerce | WordPress-Plugin, Hosting-/Installationsanforderungen | Hosting, Wartung, Plugin-Kompatibilität, Erweiterungskosten, Zahlungs- und Versandablauf; Testkauf und Wiederherstellung prüfen |
| Brevo | Kampagnen, transaktionaler Versand und Automationsmails; SMTP/API dokumentiert | Versandarten und Einwilligung sauber trennen; genaue Grenzen, Domain-Einrichtung und benötigte Automation prüfen |
| Mailchimp | E-Mail-Marketing und Automationsangebote | Tarifabhängige Funktionen, Kontakte und Integrationsereignisse; Willkommensstrecke und Abmeldung testen |
| MailerLite | Newsletter, Formulare, Landingpages und Automationsangebote | Formular-/Bestätigungsablauf, konkrete Auslöser, Tarifgrenzen und benötigte Shop-Integration prüfen |
| Alle Anbieter | Dokumentierte Produktansätze und redaktionelle Zielgruppen-Einordnung | Aktuelle Preise und Vertragsbestandteile, Kündigung/Export/Migration sowie benötigte Rollen und Supportleistungen vor einer Buchung |
| Datenschutz/Recht | Keine Konformitätsversprechen veröffentlicht | Rechtsgrundlagen, Einwilligungen, Auftragsverarbeitung, Unterauftragnehmer, Speicherorte, Übermittlungen und Shop-Pflichten individuell fachlich prüfen lassen |
| Newsletter-Zustellbarkeit | Nicht unabhängig getestet und ausdrücklich so markiert | Eigene Versanddomain und Testverteiler verwenden; keine pauschale Zustellquote oder Rangfolge ableiten |

Die Empfehlungen sind eine begründete Vorauswahl nach Zielgruppe und Aufwand, kein empirischer Leistungsvergleich. Michał sollte die vorgeschlagenen Situationen und Gewichtungen redaktionell freigeben. Es gibt keine Gewinner-Scores. Aktiver Affiliate-Status ändert weder Inhalt noch Reihenfolge; in diesen neuen Modulen führen CTAs direkt auf die offiziellen Anbieteradressen ohne Partnerparameter. Bestehende Affiliate-Weiterleitungen im restlichen Verzeichnis bleiben erhalten.

## Technischer Umfang

- Wiederverwendbares Server-Komponenten-Template mit gemeinsamer Datenstruktur in `lib/comparisons.ts`.
- Acht bestehende Tool-URLs bekommen eine redaktionelle Detaildarstellung; alte ungeprüfte Preis-/Lizenz-/Bewertungsboxen werden dort nicht mit der neuen Einordnung vermischt.
- Inhalte bleiben als versionierter Code prüfbar. Keine produktiven Tool-Zeilen, Blog-Zeilen oder Tabellen werden verändert; kein Import und keine neue Migration.
- Der bestehende Automatisierungsartikel wird zur Laufzeit unter seiner bisherigen URL dargestellt. Sein alter Datenbanktext bleibt als Bestandsinhalt erhalten. Für diesen Slug hat das versionierte Template Vorrang; spätere Änderungen müssen daher im Code erfolgen. Gleiches gilt für die beiden neuen Artikel. Verlinkung über Startseite, Navigation, Blog-Hinweis, Übersicht, Profile und Sitemap.
- Die Tabelle hat echte Zeilen-/Spaltenüberschriften und einen benannten, tastaturbedienbaren horizontalen Scrollbereich; auf schmalen Geräten bleibt der Text in normaler Schriftgröße lesbar, nur der Tabellenbereich scrollt. Zielgruppen, Vor-/Nachteile und Anbieter-CTAs stehen zusätzlich außerhalb der Tabelle.

## Quellen

- Zapier: https://zapier.com/apps
- Make: https://www.make.com/ und https://help.make.com/router
- n8n: https://docs.n8n.io/hosting/
- Shopify: https://help.shopify.com/en/manual/intro-to-shopify/overview und https://help.shopify.com/en/manual/intro-to-shopify
- WooCommerce: https://woocommerce.com/document/build-online-store/ und https://woocommerce.com/document/installing-uninstalling-woocommerce/
- Brevo: https://help.brevo.com/hc/en-us/articles/360021196220-What-are-the-differences-between-marketing-transactional-and-automation-emails
- Mailchimp: https://mailchimp.com/features/email/ und https://mailchimp.com/solutions/marketing-automation-tools/
- MailerLite: https://www.mailerlite.com/features/email-marketing und https://www.mailerlite.com/features/automation

Anbieterinformationen können sich ändern. Das Quellen-Datum ist ein Recherchezeitpunkt und kein Nachweis eines Praxistests oder einer fortlaufenden Überwachung.

## Technische Prüfung

- Produktionsbuild erfolgreich; 98 Tests in 49 Dateien erfolgreich.
- 90 interne Linkziele aus Startseite, Übersicht, drei Vergleichen und acht Profilen geprüft: alle HTTP 200.
- Mobile Ansichten bei 320 und 390 Pixeln geprüft; keine horizontale Überbreite der Seiten. Vergleichstabellen separat horizontal scrollbar, auch per Tastatur.
- Lokaler Prüfbestand weiterhin 1.527 veröffentlichte Tools; keine produktiven Daten geändert.
