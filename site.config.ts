/**
 * Einzige Stelle für den Projektnamen und die sichtbaren Markentexte.
 * Rechtstexte enthalten bewusst Platzhalter und keine erfundenen Firmenangaben.
 */
export const siteConfig = {
  name: "Linkjagd Tools",
  shortName: "Linkjagd",
  locale: "de",
  tagline: "Websites, KI-Tools, kreative Anwendungen & Open Source entdecken",
  description:
    "Deutschsprachiges Verzeichnis für interessante Websites, KI-Tools, Browser-Games, Kreativität und Produktivität – mit Vergleichen für Business-Software.",
  url: process.env.NEXT_PUBLIC_SITE_URL || "http://127.0.0.1:4327",
  creator: {
    name: "Michał Bohdanowicz",
    channel: "@linkjagd",
    channelUrl: "https://www.tiktok.com/@linkjagd",
  },
  nav: [
    { href: "/vergleiche", label: "Tools vergleichen" },
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
    title: "Linkjagd Tools – Websites entdecken und Tools vergleichen",
    description:
      "Entdecke Websites, KI-Tools, Browser-Games und kreative Anwendungen. Finde Tools aus Linkjagd-Videos und vergleiche passende Business-Software.",
  },
  legal: {
    impressum: {
      title: "Impressum",
      intro:
        "Die Anbieterangaben sind noch unvollständig. Die fehlenden Angaben sind unten gekennzeichnet.",
      sections: [
        {
          heading: "Anbieter",
          body: [
            "[VON MICHAŁ ZU ERGÄNZEN] Vollständiger Name des Verantwortlichen",
            "[VON MICHAŁ ZU ERGÄNZEN] Anschrift – Straße, PLZ, Ort, Land",
            "[VON MICHAŁ ZU ERGÄNZEN] E-Mail-Adresse für rechtliche Anfragen",
            "[VON MICHAŁ ZU ERGÄNZEN] Telefon, falls gesetzlich anzugeben",
          ],
        },
        {
          heading: "Umsatzsteuer",
          body: [
            "[VON MICHAŁ ZU ERGÄNZEN] Hinweis nach § 19 UStG einsetzen, sofern der Kleinunternehmerstatus zutrifft. Keine Umsatzsteuer-Zusätze in Preisen oder Hinweisen formulieren.",
          ],
        },
        {
          heading: "Verantwortlich für den Inhalt",
          body: ["[VON MICHAŁ ZU ERGÄNZEN] Name und Anschrift nach § 18 Abs. 2 MStV, falls erforderlich"],
        },
      ],
    },
    datenschutz: {
      title: "Datenschutz",
      intro:
        "Diese Hinweise beschreiben die Datenverarbeitung der Website. Fehlende Angaben sind gekennzeichnet; eine vollständige rechtliche Prüfung steht noch aus.",
      sections: [
        {
          heading: "Verantwortlicher",
          body: ["[VON MICHAŁ ZU ERGÄNZEN] Name und Kontaktdaten des Verantwortlichen"],
        },
        {
          heading: "Hosting",
          body: [
            "Die öffentliche Website wird bei Vercel ausgeliefert, Funktionsregion Frankfurt (fra1). Die Datenbank der Live-Seite ist Turso, ein libSQL-Dienst, Region aws-eu-central-1. Das beschreibt den tatsächlichen Betrieb und ist kein fertiger Auftragsverarbeitungsvertrag.",
            "[VON MICHAŁ ZU ERGÄNZEN] Auftragsverarbeitung und Kontaktdaten für Datenschutzanfragen.",
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
            "Bei deaktivierter Newsletter-Anmeldung ist kein Formular sichtbar und es werden darüber keine Adressen angenommen.",
            "Ist ein Versanddienst eingerichtet und du willigst ein, speichert Linkjagd Tools E-Mail, Zeitpunkt und einen Bestätigungswert. Der Status bleibt offen, bis der Link in der Mail aufgerufen wird.",
            "Ein bestätigter Eintrag kann in der Redaktion als CSV ausgegeben werden. Der Bestätigungswert selbst steht nicht in dieser Datei.",
          ],
        },
        {
          heading: "Freiwillige Tool-Stimmen",
          body: [
            "Das anonyme Voting ist standardmäßig deaktiviert. Wenn es freigeschaltet wird, setzt eine Abstimmung ein signiertes Funktionscookie für ein Jahr. Gespeichert werden das Tool, der Zeitpunkt sowie getrennt pseudonymisierte Werte aus Cookie und IP-Adresse; die Roh-IP wird nicht in der Voting-Datenbank abgelegt.",
            "Die IP-Zuordnung verhindert wiederholte Stimmen pro Tool. Gemeinsam genutzte IP-Adressen teilen sich deshalb eine Stimme pro Tool. Versuche werden zusätzlich auf zehn pro IP und Stunde begrenzt; diese Begrenzungsdaten werden nach einem Tag bereinigt.",
            "[VON MICHAŁ VOR AKTIVIERUNG ZU PRÜFEN] Rechtsgrundlage, Speicherdauer der Stimmen und Verfahren für Betroffenenanfragen ergänzen.",
          ],
        },
        {
          heading: "Tool-Einreichung",
          body: [
            "Angaben aus dem Formular „Tool einreichen“, einschließlich einer freiwillig angegebenen E-Mail-Adresse, werden als Entwurf in der Datenbank gespeichert, damit die Redaktion sie prüfen kann. Eine Bestätigungsmail wird nicht versendet.",
          ],
        },
        {
          heading: "Merkliste und Darstellung",
          body: ["Die Merkliste und die gewählte helle oder dunkle Darstellung werden im lokalen Speicher deines Browsers abgelegt. Du kannst diese Angaben über die Website-Daten deines Browsers löschen."],
        },
        {
          heading: "Externe Videos",
          body: ["Eingebettete Videos werden erst nach Klick auf „Video laden“ vom jeweiligen Anbieter angefordert. Dabei wird eine Verbindung zu diesem Anbieter aufgebaut. Alternativ können Video-Links direkt auf dessen Website führen.", "[VON MICHAŁ ZU ERGÄNZEN] Eingesetzte Videoanbieter, Rechtsgrundlagen und gegebenenfalls Übermittlungen in Drittländer prüfen."],
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
        "Linkjagd Tools kann Vergütungen erhalten, wenn du ein Tool über einen gekennzeichneten Partnerlink öffnest. Die Preise und Vertragsbedingungen legt der jeweilige Anbieter fest.",
      sections: [
        {
          heading: "Wie Links funktionieren",
          body: [
            "Anbieterlinks führen zur offiziellen Website oder bei gekennzeichneten Partnerlinks zu einer hinterlegten Partneradresse.",
            "Mit aktivem Partnerlink ist der Link mit rel=\"sponsored nofollow\" gekennzeichnet. Ohne Partnerlink bleibt er ein normaler Link zur offiziellen Website. Die Weiterleitung ist ein HTTP-302 auf genau die gespeicherte Adresse. Es werden keine Partnerparameter angehängt.",
            "Liegt ein gültiger eigener Partnerlink vor, führt /go/[slug] dorthin und der Button ist als Werbung gekennzeichnet. Ohne Partnerlink führt dieselbe Adresse zur offiziellen Website und wird nicht als Werbung bezeichnet. Es werden keine Empfehlungsparameter angehängt.",
          ],
        },
        {
          heading: "Kennzeichnung",
          body: [
            "Partnerlinks sind im Button-Umfeld als Werbung erkennbar. Ein Partnerstatus bestimmt nicht automatisch unsere redaktionelle Einordnung.",
          ],
        },
        {
          heading: "Ergänzende Angaben",
          body: [
            "[VON MICHAŁ ZU ERGÄNZEN] Konkrete Netzwerke, Provisionshinweise und der finale Transparenztext nach rechtlicher Prüfung.",
          ],
        },
      ],
    },
  },
} as const;

export type SiteConfig = typeof siteConfig;
