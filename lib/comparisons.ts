export type DecisionTool = {
  name: string; summary: string; audience: string; useCases: string[];
  strengths: string[]; weaknesses: string[]; alternatives: string[];
  providerUrl: string; sources: { title: string; url: string }[];
};
export const researchDate = "2026-11-02";
export const decisionTools: Record<string, DecisionTool> = {
  zapier: {
    name: "Zapier", summary: "Verbindet Web-Anwendungen über auslösende Ereignisse und nachfolgende Aktionen.",
    audience: "Kleine Teams, die vorhandene SaaS-Anwendungen verbinden möchten, ohne selbst einen Workflow-Server zu betreiben.",
    useCases: ["Neue Formularanfragen an ein CRM übergeben.", "Bei einer neuen Bestellung das zuständige Team benachrichtigen."],
    strengths: ["App-Verzeichnis zum Prüfen der benötigten Verbindungen.", "Ereignis und Folgeaktion bilden einen klaren Einstieg."],
    weaknesses: ["Ein vorhandener App-Connector garantiert noch nicht die benötigte Aktion.", "Verbrauch und Tarifgrenzen müssen zum tatsächlichen Ablauf passen."],
    alternatives: ["make", "n8n"], providerUrl: "https://zapier.com/",
    sources: [{ title: "App-Verzeichnis und Automatisierungsangebote", url: "https://zapier.com/apps" }],
  },
  make: {
    name: "Make", summary: "Erstellt visuelle Automatisierungen, in denen Module Daten verarbeiten und weitergeben.",
    audience: "Marketing- und Operations-Teams, die Datenflüsse und Verzweigungen auf einer Arbeitsfläche planen möchten.",
    useCases: ["Formulardaten aufbereiten und abhängig vom Inhalt weiterleiten.", "Bestellinformationen in unterschiedliche nachgelagerte Abläufe aufteilen."],
    strengths: ["Visuelle Darstellung des Datenflusses.", "Router und Filter für unterschiedliche Verarbeitungswege."],
    weaknesses: ["Verzweigte Szenarien brauchen nachvollziehbare Datenzuordnungen.", "Fehlerbehandlung und tatsächlicher Verbrauch gehören in einen Pilotlauf."],
    alternatives: ["zapier", "n8n"], providerUrl: "https://www.make.com/",
    sources: [{ title: "Visuelle Automatisierung", url: "https://www.make.com/" }, { title: "Router und Filter", url: "https://help.make.com/router" }],
  },
  n8n: {
    name: "n8n", summary: "Workflow-Plattform mit Cloud-Angebot und der Möglichkeit zum Betrieb auf eigener Infrastruktur.",
    audience: "Technische Teams mit einer verantwortlichen Person für Einrichtung, Betrieb und Fehlerbehebung.",
    useCases: ["Einen internen Datenübergabeprozess als Workflow modellieren.", "Einen Ablauf auf eigener Infrastruktur betreiben und überwachen."],
    strengths: ["Eigener Betrieb ist eine dokumentierte Option.", "Cloud und selbst betriebene Editionen lassen sich nach Betriebsbedarf abwägen."],
    weaknesses: ["Selbstbetrieb verlangt Updates, Backups und Überwachung.", "Eigener Server bedeutet weder automatisch Rechtskonformität noch, dass angebundene Dienste keine Daten erhalten."],
    alternatives: ["zapier", "make"], providerUrl: "https://n8n.io/",
    sources: [{ title: "Hosting und Editionsunterschiede", url: "https://docs.n8n.io/hosting/" }],
  },
  shopify: {
    name: "Shopify", summary: "Shop-Plattform für Produktpräsentation, Bestellungen und Verkauf mit Themes und ergänzenden Apps.",
    audience: "Shop-Gründer und kleine Handelsteams, die mit einer zusammenhängenden Verkaufsplattform beginnen möchten.",
    useCases: ["Einen Produktkatalog mit Bestellprozess veröffentlichen.", "Den Shop mit einem passenden Theme gestalten und gezielt erweitern."],
    strengths: ["Shop-Funktionen und Erweiterungsangebot in einer Plattform.", "Dokumentierter Einrichtungsablauf als Grundlage für den Shop-Start."],
    weaknesses: ["Zusatz-Apps und gewünschte Funktionen können weitere Kosten auslösen.", "Sonderanforderungen müssen gegen Plattform- und Tarifgrenzen geprüft werden."],
    alternatives: ["woocommerce"], providerUrl: "https://www.shopify.com/",
    sources: [{ title: "Funktionsüberblick", url: "https://help.shopify.com/en/manual/intro-to-shopify/overview" }, { title: "Einrichtung", url: "https://help.shopify.com/en/manual/intro-to-shopify" }],
  },
  woocommerce: {
    name: "WooCommerce", summary: "Ergänzt eine WordPress-Website um Shop-Funktionen und lässt sich über Erweiterungen anpassen.",
    audience: "Unternehmen mit WordPress-Erfahrung oder einem Dienstleister, der die technische Betreuung übernimmt.",
    useCases: ["Eine bestehende WordPress-Website um einen Shop ergänzen.", "Shop und redaktionelle Website in derselben WordPress-Umgebung betreiben."],
    strengths: ["Shop-Erweiterung für vorhandene WordPress-Projekte.", "Hosting und Erweiterungen können passend zum Projekt gewählt werden."],
    weaknesses: ["Hosting, Updates und Plugin-Zusammenspiel brauchen Betreuung.", "Ein kostenloses Kern-Plugin ist kein kostenloser Gesamtbetrieb."],
    alternatives: ["shopify"], providerUrl: "https://woocommerce.com/",
    sources: [{ title: "Shop-Aufbau und Hosting", url: "https://woocommerce.com/document/build-online-store/" }, { title: "Installation und Voraussetzungen", url: "https://woocommerce.com/document/installing-uninstalling-woocommerce/" }],
  },
  brevo: {
    name: "Brevo", summary: "Bietet Kampagnen-E-Mails, transaktionalen Versand und automatisierte E-Mail-Abläufe.",
    audience: "Kleine Unternehmen, die Newsletter und ausgelöste Service-Nachrichten getrennt planen möchten.",
    useCases: ["Einen Newsletter an dafür vorgesehene Kontakte verschicken.", "Informationsmails über eine technische Anbindung auslösen."],
    strengths: ["Unterscheidet Kampagnen, transaktionalen Versand und Automationen.", "Dokumentiert SMTP- und API-Zugänge für transaktionale Nachrichten."],
    weaknesses: ["Marketing und notwendige Service-Nachrichten müssen sauber getrennt werden.", "Versandgrenzen, Freischaltung und benötigte Funktionen vorher prüfen."],
    alternatives: ["mailchimp", "mailerlite"], providerUrl: "https://www.brevo.com/",
    sources: [{ title: "Marketing-, Transaktions- und Automations-E-Mails", url: "https://help.brevo.com/hc/en-us/articles/360021196220-What-are-the-differences-between-marketing-transactional-and-automation-emails" }],
  },
  mailchimp: {
    name: "Mailchimp", summary: "E-Mail-Marketing-Plattform mit Kampagnen, Zielgruppenfunktionen und Marketing-Automationen.",
    audience: "Marketing-Teams, die neben regelmäßigen Newslettern auch automatisierte Kontaktstrecken planen.",
    useCases: ["Eine wiederkehrende E-Mail-Kampagne erstellen.", "Eine Willkommensstrecke für neu angemeldete Kontakte planen."],
    strengths: ["Kampagnen und Automationsangebote innerhalb einer Marketing-Plattform.", "Anbieterinformationen zu Shop- und weiteren Integrationen vorhanden."],
    weaknesses: ["Benötigte Automationsschritte und Kontaktgrenzen können tarifabhängig sein.", "Die passende Integration muss mit den konkreten Shop-Ereignissen geprüft werden."],
    alternatives: ["brevo", "mailerlite"], providerUrl: "https://mailchimp.com/",
    sources: [{ title: "E-Mail-Marketing", url: "https://mailchimp.com/features/email/" }, { title: "Marketing-Automationen", url: "https://mailchimp.com/solutions/marketing-automation-tools/" }],
  },
  mailerlite: {
    name: "MailerLite", summary: "Verbindet Newsletter-Erstellung mit Anmeldeformularen, Landingpages und E-Mail-Automationen.",
    audience: "Kleine Unternehmen, die den Einstieg über Newsletter und einen überschaubaren Anmeldeprozess suchen.",
    useCases: ["Über eine Landingpage Newsletter-Anmeldungen sammeln.", "Eine anschließende E-Mail-Strecke für neue Kontakte vorbereiten."],
    strengths: ["Newsletter, Formulare und Landingpages werden zusammen angeboten.", "Automationen ergänzen den regelmäßigen Versand."],
    weaknesses: ["Spezielle Shop-Prozesse benötigen eine Prüfung der jeweiligen Integration.", "Tarifgrenzen und benötigte Auslöser vor dem Wechsel abgleichen."],
    alternatives: ["brevo", "mailchimp"], providerUrl: "https://www.mailerlite.com/",
    sources: [{ title: "E-Mail-Marketing und Formulare", url: "https://www.mailerlite.com/features/email-marketing" }, { title: "Automationsangebote", url: "https://www.mailerlite.com/features/automation" }],
  },
};

export type Comparison = {
  slug: string; title: string; topic: string; intro: string; tools: string[];
  rows: { label: string; values: string[] }[];
  recommendations: { situation: string; tool: string; reason: string }[];
  checklist: string[];
};
export const comparisons: Comparison[] = [
  {
    slug: "zapier-make-n8n-vergleich", title: "Zapier vs. Make vs. n8n", topic: "Automatisierung",
    intro: "Entscheidend ist nicht die längste Funktionsliste, sondern ob dein Ablauf mit vertretbarem Aufwand zuverlässig betreut werden kann.", tools: ["zapier", "make", "n8n"],
    rows: [
      { label: "Ansatz", values: ["Apps durch Ereignisse und Aktionen verbinden", "Datenflüsse visuell mit Modulen aufbauen", "Workflows in Cloud oder eigenem Betrieb"] },
      { label: "Passt besonders zu", values: ["Teams mit vorhandenen SaaS-Apps", "Teams, die Verzweigungen visuell planen", "Teams mit technischer Betriebsverantwortung"] },
      { label: "Zu berücksichtigen", values: ["Konkrete Connector-Aktionen abgleichen", "Datenzuordnung und Fehlerpfade planen", "Bei Selbstbetrieb: Updates, Backup und Monitoring"] },
      { label: "Budget-Prüfung", values: ["Tarif und Verbrauch des Pilotprozesses prüfen", "Szenario-Verbrauch und Tarif prüfen", "Cloud-Tarif oder vollständige Betriebskosten prüfen"] },
    ],
    recommendations: [
      { situation: "Formular → CRM mit möglichst wenig eigener Infrastruktur", tool: "zapier", reason: "Prüfe Zapier zuerst, wenn beide Anwendungen die benötigten Auslöser und Aktionen anbieten." },
      { situation: "Ein Ablauf mit mehreren Entscheidungswegen", tool: "make", reason: "Make ist eine sinnvolle Vorauswahl, wenn die visuelle Darstellung von Filtern und Routen wichtig ist." },
      { situation: "Selbstbetrieb ist eine feste Anforderung", tool: "n8n", reason: "n8n bietet diese Option. Plane dafür eine Person oder einen Dienstleister für den Betrieb ein." },
    ],
    checklist: ["Mit Testdaten denselben Prozess in den Kandidaten nachbauen; Fehler, doppelte Ereignisse und Wiederholungen prüfen.", "Tatsächlichen Verbrauch, benötigte Aktionen und aktuelle Tarifgrenzen dokumentieren.", "Bei n8n Lizenz- und Editionsbedingungen für den konkreten Einsatz prüfen; Selbstbetrieb ist keine Datenschutzgarantie."],
  },
  {
    slug: "shopify-vs-woocommerce", title: "Shopify vs. WooCommerce", topic: "E-Commerce",
    intro: "Kläre vor der Systemwahl, wer den Shop technisch betreut und welche Verkaufsprozesse bereits zum Start funktionieren müssen.", tools: ["shopify", "woocommerce"],
    rows: [
      { label: "Grundlage", values: ["Eigenständige Shop-Plattform", "Shop-Plugin für WordPress"] },
      { label: "Geeigneter Ausgangspunkt", values: ["Ein neuer Shop mit einer zusammenhängenden Plattform", "Eine bestehende WordPress-Website oder WordPress-Kompetenz"] },
      { label: "Erweiterung", values: ["Themes und Apps; Umfang vorab abgleichen", "WordPress-/WooCommerce-Erweiterungen; Zusammenspiel prüfen"] },
      { label: "Verantwortung", values: ["Shop-Konfiguration und Plattformgrenzen planen", "Zusätzlich Hosting, Updates und Plugin-Betrieb organisieren"] },
      { label: "Budget-Prüfung", values: ["Tarif, Apps, Zahlungsverarbeitung und Einrichtung zusammen betrachten", "Hosting, Erweiterungen, Wartung und Einrichtung zusammen betrachten"] },
    ],
    recommendations: [
      { situation: "Du startest ohne bestehende WordPress-Umgebung", tool: "shopify", reason: "Shopify ist eine sinnvolle Vorauswahl, wenn du den Shop um eine zusammenhängende Verkaufsplattform herum aufbauen möchtest." },
      { situation: "Du hast WordPress und verlässliche technische Betreuung", tool: "woocommerce", reason: "WooCommerce kann die bestehende Umgebung um Shop-Funktionen ergänzen; berücksichtige Wartung und Erweiterungen." },
    ],
    checklist: ["Zahlungsarten, Versandregeln, Produktvarianten und benötigte Schnittstellen mit einem Testkauf prüfen.", "Ein vollständiges Angebot inklusive Apps/Plugins, Wartung, Zahlungen und möglicher Migration einholen.", "Rechtliche Shop-Pflichten und Anbieter-Vertragsunterlagen fachlich prüfen lassen; dieses Dokument ersetzt keine Rechtsberatung."],
  },
  {
    slug: "newsletter-tools-kleine-unternehmen", title: "Newsletter-Tools für kleine Unternehmen", topic: "Marketing",
    intro: "Verglichen werden Brevo, Mailchimp und MailerLite aus dem bestehenden Verzeichnis. Entscheide nach Versandaufgabe und Arbeitsablauf, nicht nach einer pauschalen Bestenliste.", tools: ["brevo", "mailchimp", "mailerlite"],
    rows: [
      { label: "Schwerpunkt", values: ["Kampagnen, Transaktionsmails und Automationen", "E-Mail-Kampagnen und Marketing-Automation", "Newsletter, Anmeldeformulare und Landingpages"] },
      { label: "Sinnvolle Vorauswahl für", values: ["Getrennte Marketing- und Service-Nachrichten", "Teams mit geplanten Kontaktstrecken", "Newsletter-Aufbau mit Anmeldeseite"] },
      { label: "Vor dem Start", values: ["Versandarten und Kontakte klar trennen", "Benötigte Schritte und Integrationen prüfen", "Formular- und Automationsablauf prüfen"] },
      { label: "Budget-Prüfung", values: ["Versandvolumen und Funktionen im aktuellen Tarif", "Kontaktumfang und Funktionen im aktuellen Tarif", "Kontaktumfang und Funktionen im aktuellen Tarif"] },
      { label: "Nicht unabhängig geprüft", values: ["Zustellbarkeit im eigenen Verteiler", "Zustellbarkeit im eigenen Verteiler", "Zustellbarkeit im eigenen Verteiler"] },
    ],
    recommendations: [
      { situation: "Newsletter und technische Service-Mails sind beide relevant", tool: "brevo", reason: "Die dokumentierte Trennung der Versandarten ist ein guter Ausgangspunkt für deine Anforderungsprüfung." },
      { situation: "Ein Marketing-Team plant mehrere Kontaktstrecken", tool: "mailchimp", reason: "Prüfe die Automations- und Integrationsangebote anhand eurer konkreten Auslöser und Daten." },
      { situation: "Du brauchst zuerst Newsletter plus Anmeldeseite", tool: "mailerlite", reason: "Die Kombination aus Newsletter, Formularen und Landingpages passt als Vorauswahl zu dieser Aufgabe." },
    ],
    checklist: ["Einwilligung, Bestätigung, Abmeldung und Kontakt-Export mit Testkontakten prüfen.", "Authentifizierung der Versanddomain und Zustellbarkeit im eigenen Verteiler testen; keine Zustellgarantien ableiten.", "Aktuelle Tarifgrenzen, Vertragsunterlagen, Auftragsverarbeitung und Datenübermittlungen fachlich prüfen lassen."],
  },
];
export const comparisonHref = (comparison: Pick<Comparison, "slug">) => `/blog/${comparison.slug}`;
export const getComparison = (slug: string) => comparisons.find((item) => item.slug === slug);
export const comparisonsForTool = (slug: string) => comparisons.filter((item) => item.tools.includes(slug));
