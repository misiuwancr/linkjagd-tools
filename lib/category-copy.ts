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
  { slug: "ki-chatbots", focus: "Chatbots beantworten Fragen, fassen Texte zusammen oder schreiben Code im Dialog. Der Unterschied liegt im Modell, in den Grenzen der kostenlosen Stufe und darin, ob Dateien angehängt werden können.", faqs: [
    { question: "Welcher Chatbot ist der beste?", answer: "Das steht hier nicht. Es gibt keine Nutzerwertung." },
    { question: "Speichert Linkjagd die Chats?", answer: "Nein. Gespräche laufen beim jeweiligen Anbieter." },
  ]},
  { slug: "bildgenerierung", focus: "Bildwerkzeuge machen aus einer Beschreibung oder einem Foto ein neues Bild. Achte auf das Preismodell und darauf, ob ein Stil nur in der bezahlten Stufe liegt.", faqs: [
    { question: "Sind die Bilder gemeinfrei?", answer: "Nein. Die Rechte stehen beim Anbieter, nicht in diesem Verzeichnis." },
    { question: "Heißt kostenlos ohne Anmeldung?", answer: "Nein. Das sind zwei getrennte Angaben." },
  ]},
  { slug: "videogenerierung", focus: "Videogeneratoren bauen kurze Clips aus Text, Bild oder einer Figur. Länge, Wasserzeichen und Export hängen vom Konto ab und stehen nicht pauschal fest.", faqs: [
    { question: "Wie lang werden die Clips?", answer: "Das legt der Anbieter fest. Hier steht keine Laufzeit." },
    { question: "Darf ich den Clip in Werbung nutzen?", answer: "Das regelt die Lizenz des Anbieters." },
  ]},
  { slug: "programmierung", focus: "Hier liegen Editoren, Agenten, Hosting und Schnittstellen. Ein Vorschlag im Editor ist kein fertiger Release und ersetzt keinen Test.", faqs: [
    { question: "Darf ein Agent allein mergen?", answer: "Nein, das entscheidest du im Repository." },
    { question: "Ist jedes Tool Open Source?", answer: "Nur wenn die Lizenz im Eintrag bestätigt ist." },
  ]},
  { slug: "produktivitaet", focus: "Aufgaben, Notizen, Kalender und Dokumente teilen sich diese Kategorie. Sie ist breit. Die Kurzbeschreibung sagt, welches der Formate ein Tool wirklich führt.", faqs: [
    { question: "Gibt es eine Rangfolge?", answer: "Nein. Sortierung ist Datum, Empfehlung oder Preis, keine Stimmen." },
    { question: "Werden meine Aufgaben hier gespeichert?", answer: "Nein. Daten liegen beim jeweiligen Tool." },
  ]},
  { slug: "automatisierung", focus: "Automatisierung verbindet Dienste oder wiederholt Klicks. Ein Ablauf ist nur so zuverlässig wie die Zugänge, die du selbst einrichtest.", faqs: [
    { question: "Laufen die Abläufe auf Linkjagd?", answer: "Nein. Linkjagd startet keine Automationen." },
    { question: "Brauche ich eine API?", answer: "Nicht immer. Manche Tools klicken Seiten, andere sprechen Schnittstellen." },
  ]},
  { slug: "marketing", focus: "Marketingwerkzeuge planen Texte, Mails, Anzeigen oder Auswertungen. Eine Kategorie ersetzt keine Kampagnenstrategie und keine Reichweitenzahl.", faqs: [
    { question: "Stehen hier echte Reichweiten?", answer: "Nein. Es werden keine Nutzerzahlen erfunden." },
    { question: "Ist jeder Eintrag ein Newsletter-Tool?", answer: "Nein. Lies die Kurzbeschreibung." },
  ]},
  { slug: "social-media", focus: "Diese Tools planen Beiträge oder lesen Erwähnungen. Sie posten nichts von selbst über Linkjagd und liefern keine Follower-Garantie.", faqs: [
    { question: "Verbindet Linkjagd meine Konten?", answer: "Nein. Verbindungen richtest du im jeweiligen Tool ein." },
    { question: "Welches Netz wird unterstützt?", answer: "Das steht beim Anbieter, nicht pauschal in der Kategorie." },
  ]},
  { slug: "recherche", focus: "Recherchewerkzeuge durchsuchen Texte, Paper oder das Web und zeigen oft eine Fundstelle. Ob die Antwort stimmt, prüfst du an der Quelle.", faqs: [
    { question: "Sind die Quellen belegt?", answer: "Nur wenn das Tool sie anzeigt." },
    { question: "Ersetzt das eine Fachdatenbank?", answer: "Nein." },
  ]},
  { slug: "textgenerierung", focus: "Textwerkzeuge entwerfen Mails, Artikel oder Produktbeschreibungen. Der Entwurf bleibt dein Text, sobald du ihn abschickst.", faqs: [
    { question: "Ist der Text einzigartig?", answer: "Das garantiert diese Seite nicht." },
    { question: "Darf ich den Text kommerziell nutzen?", answer: "Das steht in den Bedingungen des Anbieters." },
  ]},
  { slug: "audio-und-sprache", focus: "Sprache wird hier zu Text, Text zu Sprache oder eine Aufnahme wird bereinigt. Qualität hängt von der Quelle ab und wird nicht benotet.", faqs: [
    { question: "Darf ich Gespräche aufzeichnen?", answer: "Das klärt der Kontext, nicht das Verzeichnis." },
    { question: "Funktioniert das auf Deutsch?", answer: "Nur wenn die Faktenleiste Ja sagt. Sonst unklar." },
  ]},
  { slug: "design", focus: "Designwerkzeuge bauen Oberflächen, Grafiken oder Freisteller. Ein Entwurf ist kein fertiges Markenrecht.", faqs: [
    { question: "Welches Tool ist am schönsten?", answer: "Das bewertet die Seite nicht." },
    { question: "Liegen hier Agenturaufträge?", answer: "Nein. Es sind Programme." },
  ]},
  { slug: "bildung", focus: "Bildungswerkzeuge üben Sprachen, erklären Texte oder sammeln Karten. Eine Schul- oder Hochschulfreigabe steht hier nicht.", faqs: [
    { question: "Darf ich das in der Prüfung nutzen?", answer: "Das sagt die Prüfungsordnung, nicht diese Kategorie." },
    { question: "Sind die Inhalte lehrplankonform?", answer: "Nein, das wird hier nicht geprüft." },
  ]},
  { slug: "e-commerce", focus: "Shop-Werkzeuge führen Produkte, Zahlungen oder Bestellungen. Ein Eintrag ist kein Shop und kein Zahlungsdienst von Linkjagd.", faqs: [
    { question: "Nimmt Linkjagd Zahlungen an?", answer: "Nein." },
    { question: "Ist jeder Eintrag ein Kassensystem?", answer: "Nein. Die Kurzbeschreibung grenzt das ein." },
  ]},
  { slug: "finanzen", focus: "Finanzwerkzeuge schreiben Rechnungen, lesen Belege oder planen Zahlen. Sie beraten nicht und erstellen keinen Bescheid.", faqs: [
    { question: "Ersetzt das eine Steuerberatung?", answer: "Nein." },
    { question: "Steht hier Umsatzsteuer extra?", answer: "Nein. Es wird kein Steuerzusatz erfunden." },
  ]},
  { slug: "gesundheit", focus: "Gesundheitswerkzeuge erinnern, protokollieren oder erklären. Sie stellen keine Diagnose und ersetzen keinen Arztbesuch.", faqs: [
    { question: "Ist das Medizinprodukt?", answer: "Das steht hier nicht. Der Anbieter muss das selbst ausweisen." },
    { question: "Werden Gesundheitsdaten bei Linkjagd gespeichert?", answer: "Nein." },
  ]},
  { slug: "reisen", focus: "Reisewerkzeuge planen Wege, Unterkünfte oder Tickets. Preise und Verfügbarkeit kommen vom Anbieter und werden hier nicht gecacht.", faqs: [
    { question: "Sind die Preise aktuell?", answer: "Nein. Es werden keine Live-Preise angezeigt." },
    { question: "Bucht Linkjagd die Reise?", answer: "Nein." },
  ]},
  { slug: "recht", focus: "Rechtswerkzeuge helfen beim Lesen von Texten oder beim Strukturieren von Dokumenten. Sie sind keine Rechtsberatung.", faqs: [
    { question: "Ist das ein Anwalt?", answer: "Nein." },
    { question: "Gelten die Texte vor Gericht?", answer: "Das sagt dieses Verzeichnis nicht." },
  ]},
  { slug: "personal", focus: "Personalwerkzeuge führen Abwesenheiten, Bewerbungen oder Akten im Team. Eine Einstellung entscheiden sie nicht.", faqs: [
    { question: "Liegen Bewerberdaten bei Linkjagd?", answer: "Nein." },
    { question: "Ist das ein Arbeitsvertrag?", answer: "Nein. Verträge bleiben außerhalb der Karte." },
  ]},
  { slug: "kundenservice", focus: "Kundenservice-Werkzeuge sammeln Tickets, Chats oder Fernwartung im Alltag. Linkjagd beantwortet darüber keine Kundenanfragen.", faqs: [
    { question: "Ist der Chat auf dieser Website?", answer: "Nein. Es gibt hier keinen Support-Chat für fremde Shops." },
    { question: "Sieht die Redaktion fremde Tickets?", answer: "Nein." },
  ]},
  { slug: "seo", focus: "SEO-Werkzeuge zeigen Begriffe, Lücken oder den Aufbau eines Textes. Eine Platzierung in der Suche verspricht die Kategorie nicht.", faqs: [
    { question: "Garantiert das ein Ranking?", answer: "Nein." },
    { question: "Sind die Suchdaten live?", answer: "Nur im jeweiligen Tool, nicht auf dieser Seite." },
  ]},
  { slug: "daten", focus: "Datenwerkzeuge halten Tabellen, Banken oder Schnittstellen. Ein Eintrag ist keine Auswertung deiner Zahlen.", faqs: [
    { question: "Liegt meine Datenbank bei Linkjagd?", answer: "Nein." },
    { question: "Ist jedes Tool eine SQL-Datenbank?", answer: "Nein. Manche sind Tabellen, manche Schnittstellen." },
  ]},
  { slug: "praesentationen", focus: "Präsentationswerkzeuge setzen Folien oder klickbare Abläufe. Vorlagen gehören zum Tool, nicht zu Linkjagd.", faqs: [
    { question: "Gibt es Folien von der Redaktion?", answer: "Nein." },
    { question: "Werden Präsentationen hier gehostet?", answer: "Nein." },
  ]},
  { slug: "musik", focus: "Musikwerkzeuge erzeugen Spuren oder bearbeiten vorhandenes Audio. Veröffentlichung und Verwertungsrechte klärt der Anbieter.", faqs: [
    { question: "Ist jede Spur KI?", answer: "Nein. Manche Tools schneiden nur vorhandenes Material." },
    { question: "Darf ich den Track verkaufen?", answer: "Das steht in der Lizenz des Anbieters." },
  ]},
  { slug: "dreid", focus: "3D-Werkzeuge modellieren, rendern oder erzeugen Objekte. Dateiformate und Druckbarkeit stehen beim Anbieter.", faqs: [
    { question: "Kann ich jedes Modell drucken?", answer: "Das sagt die Kategorie nicht." },
    { question: "Sind die Modelle frei?", answer: "Nur wenn die Lizenz das ausweist." },
  ]},
  { slug: "gaming", focus: "Gaming-Werkzeuge helfen bei Assets, Servern oder dem Spiel selbst. Ein Eintrag ist kein Spieltipp und keine Wertung.", faqs: [
    { question: "Sind das die besten Spiele?", answer: "Nein. Es gibt keine Bestenliste." },
    { question: "Läuft das auf jeder Konsole?", answer: "Nur wenn das Tool die Plattform nennt." },
  ]},
  { slug: "videoschnitt", focus: "Schnittwerkzeuge legen Clips, Untertitel und Ton auf eine Zeitleiste. Exportgrenzen stehen beim Anbieter, nicht in der Karte.", faqs: [
    { question: "Schneidet Linkjagd mein Video?", answer: "Nein." },
    { question: "Sind Untertitel automatisch richtig?", answer: "Das wird hier nicht gemessen." },
  ]},
];

export function copyFor(slug: string) {
  return CATEGORY_COPY.find((item) => item.slug === slug) ?? null;
}

export { METHOD };
