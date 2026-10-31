import type { LicenseType, PricingModel } from "@/db/schema";

export type UseCase = {
  slug: string;
  title: string;
  intro: string;
  categorySlug: string;
  pricing: PricingModel | "";
  license: LicenseType | "";
  faqs: { question: string; answer: string }[];
};

export const USE_CASES: UseCase[] = [
  {
    slug: "lehrer",
    title: "Tools für Lehrerinnen und Lehrer",
    intro: "Unterricht braucht Material, das sich in einer Stunde vorbereiten lässt. In dieser Sammlung stehen veröffentlichte Werkzeuge aus Bildung und Text, die beim Erklären, Üben oder Zusammenfassen helfen. Es ist keine amtliche Empfehlungsliste und keine Aussage darüber, ob ein Tool in der Schule erlaubt ist. Das klärt die eigene Schule.",
    categorySlug: "bildung",
    pricing: "",
    license: "",
    faqs: [
      { question: "Sind das geprüfte Schulprogramme?", answer: "Nein. Es sind Einträge aus dem Verzeichnis in der Kategorie Bildung. Eine Freigabe für den Unterricht steht hier nicht." },
      { question: "Kostet jedes Tool etwas?", answer: "Nein. Das Preismodell steht an der Karte: kostenlos, Freemium oder kostenpflichtig. Ein genauer Preis steht nur auf der Website des Anbieters." },
    ],
  },
  {
    slug: "studierende",
    title: "Tools für Studierende",
    intro: "Für Hausarbeiten zählen Lesen, Zitieren und eine ruhige Aufgabenliste. Hier liegen veröffentlichte Recherche- und Bildungswerkzeuge nebeneinander. Die Seite ersetzt keine Bibliothek und prüft nicht, ob eine Hochschule ein Werkzeug für Prüfungen zulässt.",
    categorySlug: "recherche",
    pricing: "",
    license: "",
    faqs: [
      { question: "Darf ich damit eine Prüfung schreiben?", answer: "Das steht hier nicht. Die Prüfungsordnung deiner Hochschule gilt, nicht dieses Verzeichnis." },
      { question: "Sind die Texte der Tools zitierfähig?", answer: "Ein Tooltext ist keine Quelle. Zitate gehören zur Fachliteratur, die du selbst prüfst." },
    ],
  },
  {
    slug: "tiktok-creator",
    title: "Tools für TikTok-Creator",
    intro: "Kurze Videos brauchen Schnitt, Untertitel, Ton und manchmal ein Bild. Diese Seite sammelt veröffentlichte Werkzeuge aus Videoschnitt, Videogenerierung und Audio. Sie sagt nicht, welches Format gerade Reichweite bringt.",
    categorySlug: "videoschnitt",
    pricing: "",
    license: "",
    faqs: [
      { question: "Sind das die Tools aus den Linkjagd-Videos?", answer: "Nur wenn beim Tool eine Video-Adresse hinterlegt ist. Diese Sammlung folgt der Kategorie, nicht dem Kanal." },
      { question: "Darf ich die Musik kommerziell nutzen?", answer: "Das steht in den Bedingungen des jeweiligen Anbieters. Das Verzeichnis vergibt keine Nutzungsrechte." },
    ],
  },
  {
    slug: "bewerbungen",
    title: "Tools für Bewerbungen",
    intro: "Ein Lebenslauf und ein Anschreiben sind Texte mit einem klaren Empfänger. Hier stehen veröffentlichte Schreibwerkzeuge. Sie formulieren Vorschläge, sie ersetzen nicht deine eigenen Angaben zu Beruf und Werdegang.",
    categorySlug: "textgenerierung",
    pricing: "",
    license: "",
    faqs: [
      { question: "Schreibt das Tool die Bewerbung für mich?", answer: "Es kann einen Entwurf liefern. Für den Inhalt bleibst du verantwortlich." },
      { question: "Werden meine Unterlagen hier gespeichert?", answer: "Linkjagd Tools speichert keine Bewerbungsunterlagen. Was ein externes Tool speichert, steht in dessen Datenschutzerklärung." },
    ],
  },
  {
    slug: "etsy-shops",
    title: "Tools für Etsy-Shops",
    intro: "Ein kleiner Shop braucht Produktbilder, Texte und einen Überblick über Bestellungen. Diese Seite zeigt veröffentlichte Werkzeuge aus E-Commerce und Bild. Sie ist kein Ratgeber für Etsy-Regeln und keine Umsatzgarantie.",
    categorySlug: "e-commerce",
    pricing: "",
    license: "",
    faqs: [
      { question: "Verbindet sich das mit meinem Etsy-Konto?", answer: "Nur wenn der Anbieter das anbietet. Im Verzeichnis steht das nicht pauschal." },
      { question: "Sind die Bilder frei von Rechten Dritter?", answer: "Das musst du beim jeweiligen Bildwerkzeug und bei deinen Vorlagen prüfen." },
    ],
  },
  {
    slug: "kleinunternehmen",
    title: "Tools für Kleinunternehmen",
    intro: "Rechnung, Termin und eine einfache Website reichen oft weiter als eine große Suite. Hier liegen veröffentlichte Werkzeuge aus Produktivität, Finanzen und Design. Steuern und Verträge klärt das nicht.",
    categorySlug: "produktivitaet",
    pricing: "",
    license: "",
    faqs: [
      { question: "Ersetzt das eine Steuerberatung?", answer: "Nein. Buchhaltungsprogramme rechnen, sie beraten nicht." },
      { question: "Gibt es nur kostenpflichtige Tools?", answer: "Nein. Die Karte zeigt das hinterlegte Preismodell." },
    ],
  },
  {
    slug: "kostenlose-ki-bilder",
    title: "Kostenlose KI-Bildgeneratoren",
    intro: "Diese Seite zeigt veröffentlichte Bildwerkzeuge mit dem Preismodell kostenlos. Ob ein Konto nötig ist, steht nur dann auf Ja oder Nein, wenn das in der Faktenleiste geprüft wurde. Sonst bleibt es unklar. Ein kostenloses Modell ist kein Versprechen, dass jede Funktion ohne Bezahlung bleibt.",
    categorySlug: "bildgenerierung",
    pricing: "free",
    license: "",
    faqs: [
      { question: "Heißt kostenlos auch ohne Anmeldung?", answer: "Nein. Ohne Anmeldung ist ein eigenes Feld und meist noch unklar." },
      { question: "Darf ich die Bilder verkaufen?", answer: "Das regelt der Anbieter. Hier steht nur das Preismodell." },
    ],
  },
  {
    slug: "meetings",
    title: "Tools für Meetings",
    intro: "Wer Gespräche mitschreibt, sucht Transkript, Zusammenfassung oder eine Aufnahme. In dieser Sammlung stehen veröffentlichte Audio-Werkzeuge. Eine Einwilligung der Teilnehmenden ist davon unabhängig und hier nicht geprüft.",
    categorySlug: "audio-und-sprache",
    pricing: "",
    license: "",
    faqs: [
      { question: "Darf ich jedes Meeting aufzeichnen?", answer: "Das hängt von den Personen und vom Kontext ab. Das Verzeichnis erlaubt keine Aufnahmen." },
      { question: "Sind die Zusammenfassungen vollständig?", answer: "Nein. Ein Transkript kann danebenliegen. Die Aufnahme bleibt die Quelle." },
    ],
  },
  {
    slug: "open-source-buero",
    title: "Open Source fürs Büro",
    intro: "Wer Dokumente ohne Abo bearbeiten will, findet hier veröffentlichte Programme mit bestätigter Open-Source-Lizenz in Produktivität und Design. Eine Lizenz ist nur dann Open Source, wenn sie im Eintrag so steht. Unbekannt heißt nicht offen.",
    categorySlug: "produktivitaet",
    pricing: "",
    license: "open_source",
    faqs: [
      { question: "Ist jedes kostenlose Tool Open Source?", answer: "Nein. Kostenlos und Open Source sind zwei verschiedene Angaben." },
      { question: "Wo liegt der Quelltext?", answer: "Wenn ein Repository hinterlegt ist, steht der Link auf der Toolseite." },
    ],
  },
  {
    slug: "recherche",
    title: "Tools für Recherche",
    intro: "Recherchewerkzeuge helfen, eine Frage an Texte oder Paper zu stellen. Diese Seite listet veröffentlichte Einträge aus der Kategorie Recherche. Sie prüft nicht, ob eine Antwort fachlich stimmt.",
    categorySlug: "recherche",
    pricing: "",
    license: "",
    faqs: [
      { question: "Sind die Quellen belegt?", answer: "Nur wenn das jeweilige Tool sie zeigt. Das Verzeichnis hängt keine Quellen an." },
      { question: "Ersetzt das eine Datenbank der Bibliothek?", answer: "Nein. Fachdatenbanken bleiben eigene Zugänge." },
    ],
  },
  {
    slug: "untertitel",
    title: "Tools für Untertitel",
    intro: "Untertitel entstehen aus Sprache. Hier stehen veröffentlichte Werkzeuge aus Videoschnitt und Audio, die Sprache in Text oder Text ins Bild bringen können. Die Genauigkeit hängt von der Aufnahme ab und wird hier nicht gemessen.",
    categorySlug: "videoschnitt",
    pricing: "",
    license: "",
    faqs: [
      { question: "Sind die Untertitel barrierefrei?", answer: "Das bewertet diese Seite nicht. Ob Kontrast und Timing reichen, siehst du im jeweiligen Tool." },
      { question: "Funktioniert das auf Deutsch?", answer: "Nur wenn in der Faktenleiste Auf Deutsch nutzbar auf Ja steht. Sonst ist es unklar." },
    ],
  },
  {
    slug: "passwoerter",
    title: "Tools für Passwörter",
    intro: "Ein Passwortmanager speichert Zugänge an einem Ort. Diese Sammlung zeigt veröffentlichte Programme, deren Beschreibung das nahelegt, über die Kategorie Programmierung und Produktivität ist das zu grob. Deshalb bleibt die Liste bei Produktivität und du liest auf der Toolseite, ob es wirklich ein Tresor ist.",
    categorySlug: "produktivitaet",
    pricing: "",
    license: "",
    faqs: [
      { question: "Empfiehlt Linkjagd einen bestimmten Tresor?", answer: "Nein. Es gibt keine Rangfolge." },
      { question: "Liegen meine Passwörter bei Linkjagd?", answer: "Nein. Das Verzeichnis speichert keine Zugangsdaten." },
    ],
  },
  {
    slug: "newsletter",
    title: "Tools für Newsletter",
    intro: "Wer eine Liste selbst verschickt, braucht einen Versanddienst. Hier stehen veröffentlichte Marketing-Werkzeuge. Linkjagd Tools selbst verschickt keinen Newsletter und speichert dafür keine Adressen.",
    categorySlug: "marketing",
    pricing: "",
    license: "",
    faqs: [
      { question: "Kann ich den Versand über diese Website starten?", answer: "Nein. Es ist kein Versanddienst angebunden." },
      { question: "Ist jeder Eintrag ein Newsletter-Tool?", answer: "Die Kategorie Marketing ist breiter. Lies die Kurzbeschreibung auf der Karte." },
    ],
  },
  {
    slug: "programmieren",
    title: "Tools zum Programmieren",
    intro: "Editoren, Agenten und Hosting stehen in der Kategorie Programmierung. Diese Seite zeigt die veröffentlichten Einträge daraus. Sie ist keine Rangliste und kein Ersatz für eine Code-Review.",
    categorySlug: "programmierung",
    pricing: "",
    license: "",
    faqs: [
      { question: "Darf der Assistent allein mergen?", answer: "Das entscheidest du im Repository. Das Verzeichnis schaltet nichts frei." },
      { question: "Sind die Vorschläge korrekt?", answer: "Das steht hier nicht. Tests bleiben bei dir." },
    ],
  },
  {
    slug: "praesentationen",
    title: "Tools für Präsentationen",
    intro: "Folien und Prototypen entstehen in eigenen Programmen. Diese Sammlung nimmt die veröffentlichte Kategorie Präsentationen. Wenn sie bei dir leer wirkt, liegt das an der Zahl der Einträge, nicht an einer ausgeblendeten Bestenliste.",
    categorySlug: "praesentationen",
    pricing: "",
    license: "",
    faqs: [
      { question: "Gibt es Vorlagen von Linkjagd?", answer: "Nein. Vorlagen gehören zum jeweiligen Tool." },
      { question: "Werden Folien hier gehostet?", answer: "Nein. Die Seite verlinkt nur." },
    ],
  },
  {
    slug: "buchhaltung",
    title: "Tools für Buchhaltung",
    intro: "Rechnungen und Belege sind eigene Programme. Diese Seite zeigt veröffentlichte Finanzwerkzeuge. Sie erstellt keine Buchung und keinen Steuerbescheid.",
    categorySlug: "finanzen",
    pricing: "",
    license: "",
    faqs: [
      { question: "Ist das eine DATEV-Schnittstelle?", answer: "Nur wenn der Anbieter das auf seiner Seite schreibt. Hier steht es nicht pauschal." },
      { question: "Gilt das für Kleinunternehmer?", answer: "Das Programm rechnet nicht mit einem Umsatzsteuer-Zusatz, den wir uns ausdenken. Die steuerliche Einordnung bleibt bei dir." },
    ],
  },
  {
    slug: "musik",
    title: "Tools für Musik",
    intro: "Wer einen Jingle oder eine Spur braucht, findet hier veröffentlichte Musik- und Audio-Werkzeuge. Die Seite sagt nichts über Chart-Tauglichkeit und nichts über GEMA-Pflichten.",
    categorySlug: "musik",
    pricing: "",
    license: "",
    faqs: [
      { question: "Darf ich den Track veröffentlichen?", answer: "Das steht in der Lizenz des Anbieters, nicht in diesem Verzeichnis." },
      { question: "Ist jede Spur KI?", answer: "Nein. In der Kategorie liegen auch Programme, die vorhandenes Audio bearbeiten." },
    ],
  },
  {
    slug: "design",
    title: "Tools für Design",
    intro: "Oberflächen, Logos und Freisteller liegen in der Kategorie Design. Diese Sammlung zeigt die veröffentlichten Einträge. Geschmack und Markenrechte bleiben außerhalb der Karte.",
    categorySlug: "design",
    pricing: "",
    license: "",
    faqs: [
      { question: "Ist das eine Agentur?", answer: "Nein. Es sind Werkzeuge, keine Auftragsarbeiten." },
      { question: "Welches Tool ist das schönste?", answer: "Das bewertet die Seite nicht." },
    ],
  },
];

export function getUseCase(slug: string) {
  return USE_CASES.find((item) => item.slug === slug) ?? null;
}
