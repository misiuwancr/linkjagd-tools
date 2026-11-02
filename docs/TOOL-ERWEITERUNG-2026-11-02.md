# Erweiterung des Verzeichnisses – Stand 2. November 2026

Der Nutzer hat Veröffentlichung und Deployment ausdrücklich freigegeben und den Vercel-Teamzugriff anschließend aktiviert. **50 neue Tools sind in der Produktionsdatenbank veröffentlicht**. Das Gesamtziel von 1.000 veröffentlichten neuen Tools ist noch nicht erreicht.

## Tatsächliche Zahlen

| Prüfschritt | Anzahl |
| --- | ---: |
| Recherchierte Kandidaten aus offener Entdeckungsquelle | 1.200 |
| Bereits vorhandene Tools in lokaler Bestandskopie | 1.626 |
| Davon veröffentlicht / Entwürfe / archiviert | 1.527 / 8 / 91 |
| Zusätzlich vorhandene Importdatensätze geprüft | 1.587 |
| Erkannte Überschneidungen im Kandidatenpool | 158 |
| Potenziell neue Kandidaten | 1.042 |
| Offizielle Zielseite erreichbar | 712 |
| Inhaltlich geprüft, deutsche Beschreibung und Preis-/Lizenzbeleg vorbereitet | 50 |
| Erreichbar, aber noch nicht vollständig redaktionell geprüft | 662 |
| Technisch problematisch oder automatisierte Prüfung zurückgestellt | 330 |
| Lokal freigabe-/importbereit | 50 |
| Tatsächlich neu in Produktion importiert | **50** |

Die 158 Überschneidungen umfassen Produktnamen, Domains, vorhandene Importdateien und Wiederholungen innerhalb der Quelle. Sie sind nicht zusätzlich zu den 1.626 Bestandsdatensätzen zu addieren. Abgleich basiert auf einer lokalen Bestandskopie; die verbindliche erneute Duplikaterkennung gegen die produktive Datenbank erfolgt direkt vor jedem Import. „Erreichbar“ ist keine vollständige Produktprüfung und keine automatische Veröffentlichungsfreigabe.

## Quellen und Grenzen

FutureTools wurde als gewünschte Referenz untersucht. Die [Nutzungsbedingungen](https://app.termly.io/document/terms-of-use-for-website/e9e30fa0-42fc-4d01-8def-22f74cf7096f) untersagen systematische Entnahme für ein eigenes Verzeichnis ohne schriftliche Erlaubnis. Eine zunächst begonnene Entdeckung wurde gestoppt; daraus entstandene Zwischenliste verworfen. Keine FutureTools-Beschreibungen, Bewertungen, Bilder oder Logos übernommen.

Die finale Kandidatenliste enthält Produktnamen und offizielle Links aus [Awesome-Selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted), Stand 2. November 2026. Die daraus abgeleitete Kandidatenliste wird unter derselben [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) bereitgestellt; Urheber: Awesome-Selfhosted-Mitwirkende. Änderungen: Extraktion von Namen/Links, Abgleich, Statusfelder. Keine Übernahme der englischen Verzeichnisbeschreibungen in öffentliche Tooltexte. Die 50 deutschen Kurzbeschreibungen sind eigenständig auf Grundlage der jeweiligen offiziellen Produktseiten formuliert. Hersteller-Metadaten in der Prüfdatei dienen ausschließlich als nachvollziehbare Recherchebelege.

Diese erste Quelle enthält überdurchschnittlich viele selbst betriebene Anwendungen. Die 50 fertigen Einträge sind kein Nachweis, dass die gesamte strategische Breite des gewünschten Verzeichnisses bereits abgedeckt oder das Ziel von 1.000 neuen geprüften Tools erreicht ist.

Drei Worker, kurze Pausen, maximal ein robots.txt-Abruf und ein Seitenabruf je Kandidat. Bei unklaren robots-Regeln konservativ zurückgestellt; diese Einordnung ist kein Nachweis, dass der Anbieter tatsächlich offline oder für jeden Agenten gesperrt ist. 308 solche Fälle, sieben robots-HTTP-403, ein robots-HTTP-503, sechs Timeouts, drei Transportfehler, vier Zielseiten mit HTTP 403 und eine mit HTTP 503. Keine Sperren umgangen. Weitere gezielte Abrufe für die 50 überprüften Einträge.

Preise nur als belegtes Modell, keine dauerhaft gültigen Zahlen zugesichert. Bei freien selbst betriebenen Ausgaben bezieht sich „kostenlos“ auf die Software, nicht auf Hosting oder Betrieb. Kostenpflichtige Cloudprodukte und freie Ausgaben werden in den deutschen Beschreibungen unterschieden. Unklare Lizenzen werden nicht pauschal als geprüftes Open Source ausgezeichnet. Bei Healthchecks und SimpleLogin die separate offizielle Preisseite als Preisbeleg hinterlegt.

## Dateien und sicherer Import

- `data/expansion-candidates-2026-11-02.json`: Entdeckung und Duplikatstatus.
- `data/expansion-checks-2026-11-02.json`: technische Ergebnisse und Anbieter-Metadaten; kein automatischer Import dieser Liste.
- `data/expansion-reviewed-2026-11-02.json`: 50 redaktionell vorbereitete Einträge mit Prüfdatum und Quellen.
- `lib/import/batch.ts`, `scripts/import-batch.ts`: nutzen die vorhandene Importvalidierung, Taxonomie, Repository-Helfer und Tabellen. Nur neue Einträge, eine Transaktion pro Kandidat. Bestehende Datensätze werden ausnahmslos übersprungen, auch wenn sie nicht redaktionell gesperrt sind. Kein Archivieren, kein Seed, keine Migration.

Standard ist Dry-Run. Fehler/Status pro Kandidat werden in JSONL protokolliert; ungültige Kandidaten/Fehler führen zu einem Fehler-Exitcode. Wiederaufnahme prüft die Datenbank erneut; bereits importierte Einträge werden übersprungen. Duplikate innerhalb der Eingabedatei werden auch im Dry-Run erkannt. Remote-Schreiben braucht zusätzlich `--remote`, Veröffentlichung zusätzlich `--publish`; dies sind technische Schutzschalter, keine erneute Nutzerfreigabe.

```text
npm run import:batch -- data/expansion-reviewed-2026-11-02.json --report=PFAD/dryrun.jsonl
npm run import:batch -- data/expansion-reviewed-2026-11-02.json --apply --publish --remote --report=PFAD/import.jsonl
```

Der Zielzugriff erfolgt über die bestehenden Umgebungsvariablen. Produktionszugangsdaten gehören nicht in Repository oder Berichte. Der Remote-Importer wiederholt schreibende Transportanfragen nicht automatisch; ein unterbrochener Lauf wird durch erneuten Bestandsabgleich fortgesetzt.

## Lokal bestätigt

Dry-Run auf isolierter Bestandskopie: **50 ready**, keine Schreibänderungen, Bestand weiter 1.626 Tools. Anschließender lokaler Import: **50 published**, Bestand 1.676. Wiederholung: **50 duplicate**, keine weiteren Einträge. Vollständiger Vorher-/Nachher-Vergleich aller 1.626 bestehenden Tool-Datensätze: **0 geändert**. Das ist ausdrücklich keine produktive Veröffentlichung.

Regressionstest deckt Dry-Run ohne Schreiben, atomaren Import auf dateibasierter SQLite, Wiederaufnahme, unveränderte vorhandene Einträge, unbekannte Kategorien und fehlende/falsche Prüfbelege ab. Tests, Lint und Build werden vor Release ausgeführt. Kein neuer Datenbankdienst, keine zusätzliche Trackingplattform, keine Migration und keine kostenpflichtigen Dienste eingeführt.

Abschließend bestätigt: `npm test` 110 Tests in 53 Dateien erfolgreich; `npm run lint` ohne Warnungen/Fehler; `npm run build` einschließlich Typprüfung erfolgreich, Node 22.16.0 mit isolierter Testdatenbank. Zusätzlicher CLI-Dry-Run mit doppelter Eingabe liefert einmal `ready`, einmal `duplicate-input`.

## Noch offen

662 erreichbare Kandidaten brauchen individuelle inhaltliche Prüfung, deutsche Beschreibung und belastbare Preis-/Lizenzinformationen. 330 Fälle bleiben zurückgestellt. Für das Ziel von 1.000 **veröffentlichten** neuen Tools sind weitere Belege und gegebenenfalls weitere erlaubte Entdeckungsquellen nötig. Fehlende Daten werden nicht erfunden, unvollständige Kandidaten nicht veröffentlicht.

Der frühere HTTP-403-Zugriffsblock ist aufgehoben. Die Produktions-Zugangsdaten sind als nicht auslesbare Vercel-Geheimnisse hinterlegt. Der Import wurde deshalb innerhalb der bestehenden Vercel-Buildumgebung mit deren vorhandenen Zugangsdaten ausgeführt; keine Geheimnisse ausgelesen, exportiert oder in Logs geschrieben, keine Geheimnis-Einstellungen geändert.

## Tatsächlich bestätigter Produktionsimport

Gepinnter Stand: main `5c012c6e0e713e5a30c6a99471bd0504fde87815`, bestehendes Projekt und bestehende Produktionsdatenbank. Einmalige Build-Befehle je Deployment, kein zusätzlicher Dienst und kein öffentlicher Import-Endpunkt.

- Live-Dry-Run [Deployment E2oSgxTQPegcNUHBdFgZ5guEARop](https://vercel.com/linkjagd/linkjagd-tools/E2oSgxTQPegcNUHBdFgZ5guEARop): 50 `ready`, keine Duplikate, keine Validierungsfehler. Anschließender regulärer Build erfolgreich.
- Produktiver Import [Deployment AvuzxL1uFoXMLdq8H7zVxnaUVALE](https://vercel.com/linkjagd/linkjagd-tools/AvuzxL1uFoXMLdq8H7zVxnaUVALE): sämtliche Positionen 1–50 als `published` bestätigt, keine Fehler und keine übersprungenen Einträge. Bestehender Importpfad mit `--apply --publish --remote`, jeweils einzelne Transaktion. Vorhandene Datensätze werden vom Importer übersprungen; der vollständige Vorher-/Nachher-Vergleich mit 0 Änderungen ist lokal bestätigt und wird nicht als separate Messung der Live-Datenbank ausgegeben.
- AWStats nach dem Import auf der öffentlichen Produktionsdomain: HTTP 200 mit der vorbereiteten deutschen Beschreibung.

Das Import-Deployment ist **READY** und der öffentlichen Domain `linkjagd-tools.vercel.app` zugewiesen. Anschließende tatsächliche Produktionstests: sämtliche **50 neuen Profile HTTP 200**, jeweils mit erwarteter deutscher Beschreibung und korrektem Canonical. Sitemap HTTP 200 mit **1.706 URLs** (vorher 1.656), alle 50 neuen Profile enthalten. Zusätzlich `/`, `/tools`, `/blog`, `/linkjagd`, `/vergleiche`, `/tools/cryptpad`, `/robots.txt`, Suche nach AWStats und kombinierter Kategorie-/Kostenlos-Filter: neunmal HTTP 200; AWStats in Suche und Filterergebnis enthalten. HEAD `/go/awstats`: HTTP 302 auf `https://www.awstats.org/`, ohne künstliche Klickzählung.

Vercel-Funktionsprotokolle für dieses Import-Deployment, 20:35:17–20:50:17 UTC, Level `error`/`fatal`: keine passenden Logs. Dies ist eine abgegrenzte Beobachtung, keine unbegrenzte Stabilitätsgarantie. Keine erneute vollständige Prüfung aller 1.706 URLs behauptet; der große initiale Produktionslauf ist im separaten Stabilitätsbericht dokumentiert.

Der Build-Befehl dieses Import-Deployments besteht aus dem geprüften Batch-Importer und dem bestehenden regulären Website-Build. Bei gewöhnlichen späteren Git-Deployments bleibt der normale Paket-Build maßgeblich; es wurde kein automatischer Import in `package.json` ergänzt. Ein erneuter Batch-Aufruf würde die bereits vorhandenen 50 Einträge überspringen.
