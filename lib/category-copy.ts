export type CategoryCopy = {
  slug: string;
  focus: string;
  faqs: { question: string; answer: string }[];
};

const METHOD =
  "Gelistet werden nur veröffentlichte Werkzeuge. Die Texte stammen von der Redaktion und nicht aus einer Herstellerbroschüre. Auf der Karte steht das Preismodell: kostenlos, Freemium oder kostenpflichtig. Open Source steht nur bei einer bestätigten Lizenz, sonst bleibt die Lizenz unbekannt. Ob die Oberfläche auf Deutsch läuft und ob ein Konto nötig ist, bleibt unklar, bis die offizielle Seite das hergibt. Eine Empfehlung erscheint nur, wenn die Redaktion das Feld gesetzt hat. Es gibt keine Sterne und keine Stimmen. Neueste folgt dem Aufnahmedatum, Empfohlen der Markierung, Kostenlos zuerst dem Preismodell. Ein Name öffnet die Toolseite. Die offizielle Website erreichst du über die Weiterleitung, ohne dass hier ein Preis oder eine Nutzerzahl erfunden wird. Das gilt für jede einzelne Karte in dieser Ansicht ohne Ausnahme. Lies dazu die Kurzbeschreibung. Mehr steht jetzt auf der jeweiligen Toolseite.";

export function categoryIntro(name: string, focus: string) {
  return `${focus} In der Kategorie ${name} gilt: ${METHOD}`;
}

export function wordCount(text: string) {
  return text.trim().split(/\s+/).filter(Boolean).length;
}

export const CATEGORY_COPY: CategoryCopy[] = [
  { slug: "chat-assistenten", focus: "Chat und Assistenten beantworten Fragen, fassen etwas zusammen oder bleiben im Dialog. Der Unterschied liegt im Modell und darin, ob Dateien angehängt werden können. Eine Antwort ist kein Beleg.", faqs: [
    { question: "Welcher Assistent ist der beste?", answer: "Das steht hier nicht. Es gibt keine Nutzerwertung." },
    { question: "Speichert Linkjagd die Chats?", answer: "Nein. Gespräche laufen beim jeweiligen Anbieter." },
  ]},
  { slug: "text-schreiben", focus: "Textwerkzeuge entwerfen Mails, Artikel oder Umschreibungen. Der Entwurf bleibt dein Text, sobald du ihn abschickst. Die Kategorie verspricht keine Einzigartigkeit.", faqs: [
    { question: "Ist der Text einzigartig?", answer: "Das garantiert diese Seite nicht." },
    { question: "Darf ich den Text kommerziell nutzen?", answer: "Das steht in den Bedingungen des Anbieters." },
  ]},
  { slug: "bild-design", focus: "Bild- und Designwerkzeuge machen aus einer Beschreibung, einem Foto oder einem Layout ein neues Bild. Achte auf das Preismodell. Ein Entwurf ist kein Markenrecht.", faqs: [
    { question: "Sind die Bilder gemeinfrei?", answer: "Nein. Die Rechte stehen beim Anbieter." },
    { question: "Heißt kostenlos ohne Anmeldung?", answer: "Nein. Das sind zwei getrennte Angaben." },
  ]},
  { slug: "video", focus: "Videowerkzeuge erzeugen kurze Clips oder schneiden vorhandenes Material. Länge, Wasserzeichen und Export hängen vom Konto ab und stehen nicht pauschal fest.", faqs: [
    { question: "Wie lang werden die Clips?", answer: "Das legt der Anbieter fest. Hier steht keine Laufzeit." },
    { question: "Schneidet Linkjagd mein Video?", answer: "Nein." },
  ]},
  { slug: "audio-musik-stimme", focus: "Audio-Werkzeuge machen Sprache zu Text, Text zu Sprache oder schneiden Musik. Qualität hängt von der Quelle ab und wird nicht benotet. Eine Spur ist nicht automatisch KI.", faqs: [
    { question: "Darf ich Gespräche aufzeichnen?", answer: "Das klärt der Kontext, nicht das Verzeichnis." },
    { question: "Darf ich den Track verkaufen?", answer: "Das steht in der Lizenz des Anbieters." },
  ]},
  { slug: "code-entwicklung", focus: "Hier liegen Editoren, Schnittstellen, Hosting und Datenwerkzeuge. Ein Vorschlag im Editor ist kein fertiger Release und ersetzt keinen Test. Open Source steht nur bei bestätigter Lizenz.", faqs: [
    { question: "Darf ein Assistent allein mergen?", answer: "Nein, das entscheidest du im Repository." },
    { question: "Ist jedes Tool Open Source?", answer: "Nur wenn die Lizenz im Eintrag bestätigt ist." },
  ]},
  { slug: "produktivitaet", focus: "Aufgaben, Notizen, Kalender, Dokumente und Folien teilen sich diese Kategorie. Sie ist breit. Die Kurzbeschreibung sagt, welches Format ein Tool wirklich führt.", faqs: [
    { question: "Gibt es eine Rangfolge?", answer: "Nein. Sortierung ist Datum, Empfehlung oder Preis, keine Stimmen." },
    { question: "Werden meine Aufgaben hier gespeichert?", answer: "Nein. Daten liegen beim jeweiligen Tool." },
  ]},
  { slug: "recherche-suche", focus: "Recherchewerkzeuge durchsuchen Texte, Paper oder das Web und zeigen oft eine Fundstelle. Ob die Antwort stimmt, prüfst du an der Quelle. Eine Fachdatenbank ersetzt das nicht.", faqs: [
    { question: "Sind die Quellen belegt?", answer: "Nur wenn das Tool sie anzeigt." },
    { question: "Ersetzt das eine Fachdatenbank?", answer: "Nein." },
  ]},
  { slug: "marketing-social", focus: "Marketing- und Social-Werkzeuge planen Texte, Beiträge, Mails oder Auswertungen. Sie posten nichts von selbst über Linkjagd und liefern keine Reichweitenzahl.", faqs: [
    { question: "Stehen hier echte Reichweiten?", answer: "Nein. Es werden keine Nutzerzahlen erfunden." },
    { question: "Verbindet Linkjagd meine Konten?", answer: "Nein. Verbindungen richtest du im jeweiligen Tool ein." },
  ]},
  { slug: "automatisierung-agenten", focus: "Automatisierung verbindet Dienste oder wiederholt Schritte. Ein Agent startet nichts über diese Website. Ein Ablauf ist nur so zuverlässig wie die Zugänge, die du selbst einrichtest.", faqs: [
    { question: "Laufen die Abläufe auf Linkjagd?", answer: "Nein. Linkjagd startet keine Automationen." },
    { question: "Brauche ich eine API?", answer: "Nicht immer. Manche Tools klicken Seiten, andere sprechen Schnittstellen." },
  ]},
  { slug: "bildung-lernen", focus: "Bildungswerkzeuge üben Sprachen, erklären Texte oder sammeln Karten. Eine Schul- oder Hochschulfreigabe steht hier nicht. Die Prüfungsordnung gilt außerhalb dieser Kategorie.", faqs: [
    { question: "Darf ich das in der Prüfung nutzen?", answer: "Das sagt die Prüfungsordnung, nicht diese Kategorie." },
    { question: "Sind die Inhalte lehrplankonform?", answer: "Nein, das wird hier nicht geprüft." },
  ]},
  { slug: "business-finanzen", focus: "Geschäfts- und Finanzwerkzeuge schreiben Rechnungen, führen Personal oder lesen Belege. Sie beraten nicht und erstellen keinen Bescheid. Ein Ticket-System ist kein Shop.", faqs: [
    { question: "Ersetzt das eine Steuerberatung?", answer: "Nein." },
    { question: "Steht hier Umsatzsteuer extra?", answer: "Nein. Es wird kein Steuerzusatz erfunden." },
  ]},
  { slug: "e-commerce", focus: "E-Commerce ist eine Kategorie unter mehreren, nicht der Schwerpunkt des Verzeichnisses. Shop-Werkzeuge führen Produkte, Zahlungen oder Bestellungen. Ein Eintrag ist kein Shop von Linkjagd.", faqs: [
    { question: "Nimmt Linkjagd Zahlungen an?", answer: "Nein." },
    { question: "Ist jeder Eintrag ein Kassensystem?", answer: "Nein. Die Kurzbeschreibung grenzt das ein." },
  ]},
  { slug: "gesundheit", focus: "Gesundheitswerkzeuge erinnern, protokollieren oder erklären. Sie stellen keine Diagnose und ersetzen keinen Arztbesuch. Ob etwas ein Medizinprodukt ist, weist der Anbieter aus.", faqs: [
    { question: "Ist das Medizinprodukt?", answer: "Das steht hier nicht. Der Anbieter muss das selbst ausweisen." },
    { question: "Werden Gesundheitsdaten bei Linkjagd gespeichert?", answer: "Nein." },
  ]},
  { slug: "reisen", focus: "Reisewerkzeuge planen Wege, Unterkünfte oder Tickets. Preise und Verfügbarkeit kommen vom Anbieter und werden hier nicht gecacht. Linkjagd bucht keine Reise.", faqs: [
    { question: "Sind die Preise aktuell?", answer: "Nein. Es werden keine Live-Preise angezeigt." },
    { question: "Bucht Linkjagd die Reise?", answer: "Nein." },
  ]},
  { slug: "spass-sonstiges", focus: "Spaß und Sonstiges sammelt Spiele und Einträge, deren vorhandener Text in keine andere Kategorie passt. Behörden, Kassen und reine Verkäufer liegen hier zur Review, nicht als Empfehlung.", faqs: [
    { question: "Sind das die besten Spiele?", answer: "Nein. Es gibt keine Bestenliste." },
    { question: "Warum liegt ein Eintrag hier?", answer: "Weil die bisherige Kategorie oder der Text keine sichere andere Schublade hergab." },
  ]},
];

export function copyFor(slug: string) {
  return CATEGORY_COPY.find((item) => item.slug === slug) ?? null;
}

export { METHOD };
