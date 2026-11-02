# Produktionsnachtest vom 2. November 2026

## Tatsächlich bestätigte Produktionstests

Domain: https://linkjagd-tools.vercel.app. Ausgangsstand: main `523d5ae`.

1.658 unterschiedliche URLs geprüft, darunter sämtliche 1.656 Sitemap-Ziele sowie zwei zusätzliche Such-/Sortierabfragen. Sitemap und robots.txt zusätzlich jeweils HTTP 200. Zwei gleichzeitige GET-Abfragen, 300 ms Pause je Worker, höchstens 30 Sekunden je Abruf.

Erste Runde: 1.213 HTTP 200, einmal HTTP 500 (`/tools/cryptpad`), 444 Transportfehler der Prüfverbindung ohne erhaltene HTTP-Antwort. Diese 444 sind **keine nachgewiesenen HTTP-500-Fehler der Website**. Der erste unmittelbare Wiederholungslauf konnte wegen derselben Verbindungsstörung keine belastbare Antwort liefern. Ein neuer Prüfprozess hat alle 445 betroffenen URLs erneut geprüft: **445 HTTP 200, keine Transportfehler**. Anschließend CryptPad nochmals dreimal HTTP 200.

Damit für alle 1.658 URLs eine erfolgreiche Antwort bestätigt. Der einzelne 500er ist bisher nicht reproduzierbar; die Aussage „keine 500er mehr“ ist damit ausdrücklich nicht belegt. Ohne Funktionsprotokolle kann dessen Ursache nicht festgestellt werden. Die frühere Turso-/Transportcache-Hypothese ist nicht als vollständig bewiesene oder endgültig beseitigte Ursache auszugeben.

`/`, `/tools`, `/blog`, `/linkjagd`, `/vergleiche`, alle Sitemap-Kategorien und Tool-Profile erfolgreich. Alle 1.658 ausgewerteten HTML-Seiten haben einen Canonical auf der beobachteten Produktionsdomain. robots.txt erlaubt öffentliche Seiten, sperrt `/admin`, `/api/`, `/go/` und verweist auf die richtige Sitemap. Sitemap enthält ausschließlich diese Domain. Produktionsumgebungsvariablen konnten nicht direkt eingesehen werden; dies prüft die tatsächlich ausgelieferten Ergebnisse.

Suche `?q=Zapier` und Sortierung `?sort=alphabetisch`: HTTP 200. HEAD `/go/chatgpt`: HTTP 302 zum gespeicherten Anbieterziel `https://chatgpt.com/chat`, `Cache-Control: no-store`, `X-Robots-Tag: noindex, nofollow`. HEAD verhindert eine künstliche Klickzählung. Fachliche Such-/Filter-/Weiterleitungsprüfungen zusätzlich lokal durch bestehende Regressionstests.

## Analyse und kleine Korrekturen

- `db/http.ts`: bereits vorhandenes `cache: no-store` und Klonen je POST-Versuch erhalten. Höchstens drei Versuche, fünf Sekunden pro Fetch, 150/300 ms Backoff; fachliche SQL-Fehler werden nicht pauschal wiederholt. Der Timeout umfasst den Fetch bis zu den Headers, nicht das vollständige Lesen des Bodys. Transport-Retries sind keine Exactly-once-Garantie für Schreiboperationen; der neue Batch-Importer verwendet daher remote nur einen Transportversuch je Transaktion.
- Nachgewiesener zusätzlicher Fehler: `Request.signal` und bereits vor Aufruf abgebrochene Signale wurden ignoriert. Beide werden nun weitergegeben; Regressionstest belegt Abbruch ohne Wiederholung. Kein Beleg, dass dies den beobachteten 500er verursacht hat.
- `getDb` teilt die Initialisierung innerhalb eines Prozesses und setzt sie nach Fehlern zurück. Der bestehende Initialisierungspfad führt Migrationen aus; der neue Importer wird deshalb direkt mit dem bestehenden Schema verbunden und ruft weder Migration noch Seed auf.
- Öffentliche Komponenten nutzen bestehende Repository-Abfragen; keine neue breite Fehlerunterdrückung, keine leeren SEO-Seiten mit künstlichem HTTP 200 eingeführt. React.cache in `publicArticles` ist eine Deduplizierung innerhalb des Renderings. Stateful Hrana-Transportantworten werden weiterhin nicht gecacht.
- `scripts/audit-production.mjs`: wiederholbarer schonender Sitemap-Test, separater Nachlauf fehlerhafter Ziele, Abbruch nach drei aufeinanderfolgenden Transportfehlern. Status 0 bleibt ausdrücklich ein Messfehler. JSON-Berichte lokal unter `.codex/tmp`, keine Zugangsdaten.
- Windows-Testbereinigung toleriert zusätzlich `EPERM` beim Löschen noch nativerseits geöffneter temporärer SQLite-Dateien; keine Lockerung der Datenassertionen.

## Lokale Prüfung

Node 22.16.0, ausschließlich isolierte lokale SQLite-Testdatenbank; keine produktiven Zugangsdaten. `npm test`: 110 Tests in 53 Dateien erfolgreich. `npm run lint`: keine Warnungen oder Fehler. `npm run build`: erfolgreich, inklusive Typprüfung und 56 generierter Seiten. Die bestehenden Vite-CJS-/Edge-Hinweise bleiben; npm 12 meldet eine Versionswarnung zur verwendeten Node-22-Unterversion, die Befehle wurden erfolgreich abgeschlossen.

## Zugriff und Release

Vercel-Fehlerübersicht und Projektdetails verweigern Zugriff mit HTTP 403 für Team `linkjagd`. Technischen Team-Freigabelink angefordert und dem Nutzer bereitgestellt. Daher keine bestätigte Auswertung von Funktionsprotokollen, kein behauptetes Deployment dieses Branches und kein Nachweis der produktiven Umgebungsvariablen. Merge/Deployment sind vom Nutzer autorisiert; tatsächliche Durchführung und Post-Deployment-Prüfung separat nachtragen.

Nachtrag: [PR #13](https://github.com/misiuwancr/linkjagd-tools/pull/13) wurde gemergt, main `1bdce5a`. Vercels Commitstatus meldet den Produktionsbuild erfolgreich: [Deployment](https://vercel.com/linkjagd/linkjagd-tools/3ba9SKYbuHY8Pju4tfPFGrPMQVmi). Nach diesem Status acht Produktionsziele erneut abgerufen (`/`, `/tools`, `/blog`, `/linkjagd`, `/vergleiche`, `/tools/cryptpad`, `/sitemap.xml`, `/robots.txt`): achtmal HTTP 200. Keine erneute vollständige 1.658-URL-Runde nach diesem Merge behauptet. Vercel-Funktionsprotokolle weiterhin nicht zugänglich.

## Nach Aktivierung des Teamzugriffs

Der Nutzer hat den Teamzugriff erteilt; Projekt- und Protokollabfragen funktionieren. Die aggregierte Fehlerübersicht zeigt die frühere Gruppe `LibsqlError: SERVER_ERROR: Server returned HTTP status 400`, zuletzt 2. November 2026, 20:07:51 UTC, Route `/tools/[slug]`, Deployment `dpl_FGAAbHuhFMom1mnJWU1rPoBrYSEb`. Dies bestätigt den libSQL-Fehler zur Zeit des ursprünglichen Nachtests, nicht dessen genaue interne Ursache.

Gezielte Fehlerprotokollabfrage für das neue Deployment `dpl_AjfSSWY7G85HQLeQbmKF1Qo7abbX`, 20:14:13–20:44:13 UTC, Level `error`/`fatal`: keine passenden Logs. Keine nachträgliche Behauptung vollständiger Fehlerfreiheit oder einer sicheren Ursachenzuordnung allein aus dieser leeren Teilabfrage.

Nach produktivem Import der 50 neuen Tools: Deployment `dpl_AvuzxL1uFoXMLdq8H7zVxnaUVALE` READY, Produktionsdomain zugewiesen. 50 neue Profile HTTP 200 mit Beschreibung und Canonical; alle in der nun 1.706 URLs umfassenden Sitemap enthalten. Neun weitere Kern-/Such-/Filterziele HTTP 200, Anbieterweiterleitung per HEAD HTTP 302. Fehlerprotokollabfrage für dieses Deployment, 20:35:17–20:50:17 UTC, Level error/fatal: keine passenden Logs. Weitere Einzelheiten im Tool-Erweiterungsbericht; keine erneute vollständige 1.706-URL-Runde behauptet.
