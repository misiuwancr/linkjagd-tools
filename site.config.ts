/**
 * Einzige Stelle für den Projektnamen und die sichtbaren Markentexte.
 * Rechtstexte enthalten bewusst Platzhalter und keine erfundenen Firmenangaben.
 */
export const siteConfig = {
  name: "Linkjagd Tools",
  shortName: "Linkjagd",
  locale: "de",
  tagline: "KI-Tools, kostenlose Webtools & Open Source – auf Deutsch erklärt",
  description:
    "Ein Verzeichnis für KI-Werkzeuge, Web-Apps und Open-Source-Programme. Texte auf Deutsch, ohne erfundene Platzierungen.",
  url: process.env.NEXT_PUBLIC_SITE_URL || "http://127.0.0.1:4327",
  creator: {
    name: "Michał Bohdanowicz",
    channel: "@linkjagd",
    channelUrl: "https://www.tiktok.com/@linkjagd",
  },
  nav: [
    { href: "/tools", label: "Alle Tools" },
    { href: "/tools?sort=alphabetisch", label: "Alphabetisch" },
    { href: "/neu", label: "Neu hinzugefügt" },
    { href: "/kategorien", label: "Kategorien" },
    { href: "/fuer", label: "Sammlungen" },
    { href: "/merkliste", label: "Merkliste" },
    { href: "/blog", label: "Blog" },
    { href: "/einreichen", label: "Tool einreichen" },
  ],
  footer: [
    { href: "/ueber-uns", label: "Über uns" },
    { href: "/kontakt", label: "Kontakt" },
    { href: "/impressum", label: "Impressum" },
    { href: "/datenschutz", label: "Datenschutz" },
    { href: "/affiliate-hinweis", label: "Affiliate-Hinweis" },
  ],
  seo: {
    title: "Linkjagd Tools – KI, Webtools und Open Source",
    description:
      "Deutschsprachiges Verzeichnis für KI-Tools, kostenlose Web-Apps und Open-Source-Programme.",
  },
  legal: {
    impressum: {
      title: "Impressum",
      intro:
        "Diese Seite ist ein Platzhalter. Vor einer öffentlichen Veröffentlichung müssen die Angaben von einer rechtskundigen Person ergänzt werden. Es wurden keine Firmen- oder Rechtsangaben erfunden.",
      sections: [
        {
          heading: "Anbieter",
          body: [
            "[PLATZHALTER: Vollständiger Name des Verantwortlichen]",
            "[PLATZHALTER: Anschrift – Straße, PLZ, Ort, Land]",
            "[PLATZHALTER: E-Mail-Adresse für rechtliche Anfragen]",
            "[PLATZHALTER: Telefon, falls gesetzlich anzugeben]",
          ],
        },
        {
          heading: "Umsatzsteuer",
          body: [
            "[PLATZHALTER: Hinweis nach § 19 UStG einsetzen, sofern der Kleinunternehmerstatus zutrifft. Keine Umsatzsteuer-Zusätze in Preisen oder Hinweisen formulieren.]",
          ],
        },
        {
          heading: "Verantwortlich für den Inhalt",
          body: ["[PLATZHALTER: Name und Anschrift nach § 18 Abs. 2 MStV, falls erforderlich]"],
        },
      ],
    },
    datenschutz: {
      title: "Datenschutz",
      intro:
        "Dieser Text erklärt nur, was die Anwendung in Phase 1 tatsächlich tut. Er ist kein fertiges Datenschutzerklärungsmuster und ersetzt keine rechtliche Prüfung.",
      sections: [
        {
          heading: "Verantwortlicher",
          body: ["[PLATZHALTER: Name und Kontaktdaten des Verantwortlichen]"],
        },
        {
          heading: "Hosting",
          body: [
            "[PLATZHALTER: Hoster, Serverstandort und Auftragsverarbeitung ergänzen, sobald der Betrieb feststeht.]",
            "Lokal läuft die Anwendung mit einer SQLite-Datei. Es ist kein zusätzlicher Cloud-Dienst für die Datenbank verdrahtet.",
          ],
        },
        {
          heading: "Werkzeug-Klicks",
          body: [
            "Wenn ein veröffentlichter Partnerlink über /go/[slug] aufgerufen wird, erhöht die Anwendung einen Tageszähler für dieses Tool und dieses Partnerprogramm.",
            "Gespeichert werden dabei nur Tool, Programm und das UTC-Datum sowie die Anzahl. Es werden keine IP-Adresse, kein User-Agent und kein Cookie für das Zählen geschrieben.",
            "Der Browser kann dem Ziel dennoch einen gewöhnlichen Referrer senden. Das bestimmt die verlinkte Website, nicht ein Tracking-Cookie von Linkjagd Tools.",
          ],
        },
        {
          heading: "Newsletter",
          body: [
            "Das Newsletter-Formular verschickt nichts und speichert keine E-Mail-Adresse, solange kein Anbieter in der Umgebung konfiguriert ist.",
          ],
        },
        {
          heading: "Tool-Einreichung",
          body: [
            "Angaben aus dem Formular „Tool einreichen“ werden als Entwurf in der lokalen Datenbank gespeichert, damit die Redaktion sie prüfen kann. Eine Bestätigungsmail wird nicht versendet.",
          ],
        },
        {
          heading: "Admin-Sitzung",
          body: [
            "Die Redaktion meldet sich mit einem httpOnly-Sitzungscookie an. Das Cookie dient nur der Anmeldung und nicht der öffentlichen Reichweitenmessung.",
          ],
        },
      ],
    },
    affiliate: {
      title: "Affiliate-Hinweis",
      intro:
        "Linkjagd Tools kann Vergütungen erhalten, wenn du ein Tool über einen gekennzeichneten Partnerlink öffnest. Für dich soll dadurch kein Aufpreis entstehen. Konkrete Sätze und Vertragspartner werden hier nicht erfunden.",
      sections: [
        {
          heading: "Wie Links funktionieren",
          body: [
            "Auf einer öffentlichen Tool-Seite gibt es höchstens einen ausgehenden Werkzeug-Link. Er führt über /go/[slug].",
            "Mit aktivem Partnerlink ist der Link mit rel=\"sponsored nofollow\" gekennzeichnet. Ohne Partnerlink bleibt er ein normaler Link zur offiziellen Website. Die Weiterleitung ist ein HTTP-302 auf genau die gespeicherte Adresse. Es werden keine Partnerparameter angehängt.",
            "Liegt ein gültiger eigener Partnerlink vor, führt /go/[slug] dorthin und der Button ist als Werbung gekennzeichnet. Ohne Partnerlink führt dieselbe Adresse zur offiziellen Website und wird nicht als Werbung bezeichnet. Es werden keine Empfehlungsparameter angehängt.",
          ],
        },
        {
          heading: "Kennzeichnung",
          body: [
            "Partnerlinks sind im Button-Umfeld als Werbung erkennbar. Beispieldatensätze sind archiviert und erscheinen nicht im öffentlichen Verzeichnis.",
          ],
        },
        {
          heading: "Offen zu lassen",
          body: [
            "[PLATZHALTER: Konkrete Netzwerke, Provisionshinweise und der finale Transparenztext nach rechtlicher Prüfung.]",
          ],
        },
      ],
    },
  },
} as const;

export type SiteConfig = typeof siteConfig;
