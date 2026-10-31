# Top 100 aus FutureTools

Abgerufen am 31. Oktober 2026.

## Quelle und Sortierung

Liste: [futuretools.io/tools?sort=popular](https://futuretools.io/tools?sort=popular)

Das ist im Auswahlfeld der Seite der Wert `popular` mit der Beschriftung **Most Popular — All Time**. Die Seite zeigt 24 Tools je Seite, sortiert nach den dort gespeicherten Stimmen über den gesamten Zeitraum. Übernommen wurden die ersten 100 Einträge mit eindeutiger Domain. Drei spätere Treffer sind entfallen, weil dieselbe Domain schon vorkam:

- PixaMotion und Hello AI, weil `apps.apple.com` schon durch Motionleap belegt war
- QR Code AI Art Generator, weil `huggingface.co` schon durch Illusion Diffusion belegt war

Die Lücken wurden mit den nächsten Einträgen derselben Sortierung gefüllt. Die hervorgehobene Leiste „Recommended right now“ und die 30-Tage-Liste `popular_30d` wurden nicht verwendet.

## Was übernommen wurde

Nur Name, die Zieladresse ohne Tracking-Parameter (`ref`, `via`, `utm_*`), die Domain und das Preismodell (`free`, `freemium`, `paid`, `open_source`; der Wert `github` zählt als Open Source).

Texte und Logos von FutureTools sind nicht in der Datenbank. Die deutschen Beschreibungen stehen in `data/futuretools-purposes.json` und wurden anhand der eigenen Websites formuliert. War eine Seite gesperrt oder zeigte ein anderes Angebot, sagt der Text das.

`discovery_source` ist `futuretools-top100`. Alle Einträge bleiben Entwürfe. Es gibt keinen Affiliate-Link und kein aktives Programm, deshalb bleibt der öffentliche Button aus.

Partnerstatus:

- `ja`: auf der eigenen Website oder einer klaren Programmseite (zum Beispiel Partnerstack) steht ein Affiliate- oder Partnerprogramm. Die URL liegt nur in der internen Notiz des Programmdatensatzes und in der CSV.
- `nein`: Startseite erreichbar, unter `/affiliate`, `/affiliates` und `/affiliate-program` keine klar erkennbare Programmseite.
- `unklar`: Website gesperrt, leer oder nicht prüfbar.

Voice.ai stand bei FutureTools hinter einem Xsolla-Link. Gespeichert ist `https://voice.ai/`.

## Spätere Prüfung

Die Erweiterung veröffentlicht geprüfte Tools auch ohne eigenen Partnerlink. `/go/[slug]` geht zum hinterlegten Affiliate-Link, wenn einer aktiv ist, sonst zur offiziellen Website ohne Zusatzparameter. GeoSpy, Maze und Godmode sowie tote Domains bleiben archiviert. Die kuratierte Liste liegt in `data/verified-tools.json`. Die zweite Liste, `data/verified-tools-batch2.json`, ergänzt Lücken bei E-Commerce, Automatisierung, Bildung, Design, Marketing, Text, Entwicklung, Recherche und selbst betreibbaren Werkzeugen. Beschreibungen sind eigen, nicht von FutureTools übernommen. Ein Open-Source-Eintrag setzt eine gelesene OSI-Lizenzdatei voraus. `npm run import:verified` liest beide Dateien, legt neue Zeilen als Entwurf an und veröffentlicht sie, wenn sie geprüft und nicht gesperrt sind. Manuelle Admin-Speicherungen setzen `content_locked` und werden nicht überschrieben.

## Wiederholen

```bash
npm run import:futuretools
```

Das Skript nutzt dieselbe Prüfung wie `POST /api/import` (`importDiscoveredTool`). Vorhandene Entwürfe mit derselben Domain werden nicht doppelt angelegt. `SKIP_LOGOS=1` lädt keine Favicons. Logos kommen nur von der offiziellen Domain, sonst bleibt der Platzhalter.
