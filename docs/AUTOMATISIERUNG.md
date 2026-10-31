# Vorbereitete Automatisierung

Phase 1 enthält keine Crawler, keine automatische Partnerbewerbung, keine KI-Recherche und keine selbst gebauten Affiliate-Links. Zwei Schnittstellen sind so geschnitten, dass sie später dazukommen, ohne die Tabellen zu wechseln.

## A. Import

`POST /api/import` mit `Authorization: Bearer <IMPORT_API_TOKEN>`.

Ohne Token antwortet die Route mit 503. Der Körper wird mit Zod geprüft. Pflicht sind Name, `originalUrl`, deutsche Kurzbeschreibung und `discoverySource`. Das Tool wird immer als Entwurf angelegt. Domain (ohne `www`) oder Kurzname, der schon existiert, ergibt 409 und keinen zweiten Datensatz.

```json
{
  "name": "Beispiel",
  "originalUrl": "https://beispiel.example/",
  "shortDescriptionDe": "Kurzer deutscher Text mit mindestens zehn Zeichen.",
  "categorySlugs": ["recherche"],
  "tags": ["Beispiel"],
  "discoverySource": "eigener-feed",
  "pricingModel": "freemium"
}
```

Vor einem echten Feed gelten die Nutzungsbedingungen der Quelle. `robots.txt` und eventuelle AI-Trainings- oder Scraping-Hinweise sind zu lesen. Was eine Quelle nicht erlaubt, wird nicht abgeholt. Die Route nimmt nur entgegen, was ein anderer, erlaubter Prozess schickt.

## B. Partnernetzwerke

`lib/affiliate/registry.ts` definiert `AffiliateNetworkAdapter` mit `id`, `label` und `describe()`. Eingetragen sind Platzhalter für manuell, direkt, Awin, Impact, CJ und Partnerize. Keine Klasse ruft ein Netzwerk auf.

Ein späterer Adapter kann Methoden ergänzen, zum Beispiel Programme suchen. Er darf keine URL erfinden und keine Parameter an eine Original-URL hängen. Öffentlich bleibt nur, was die Redaktion als aktiven Link mit Status „Affiliate-Link aktiv“ speichert. Die Prüfung sitzt in `lib/affiliate/redirect.ts` und gilt für Admin-Speichern und für `/go/[slug]`.

Vor einer echten Anbindung: Programm-AGB, erlaubte Werbemittel, Kennzeichnungspflichten und ob automatische Bewerbungen überhaupt gestattet sind. In Phase 1 gibt es keine Auto-Bewerbung.

## C. KI-News

Die Tabelle `news_posts` und die Seite `/blog` lesen veröffentlichte Notizen. Die Redaktion kann eine Notiz von Hand anlegen. Ein späterer Job schreibt in dieselbe Tabelle. Auch hier zuerst die Quelle prüfen, nichts erfinden, nichts ungeprüft veröffentlichen.

## Was bewusst nicht gebaut ist

- Crawler und Agenten, die Tools recherchieren
- automatische Partnerbewerbung
- automatisches Erzeugen von Affiliate-Parametern
- bezahlte Platzierungen
- Newsletter-Versand
