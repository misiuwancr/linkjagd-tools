/**
 * Die öffentlichen Kategorien folgen der FutureTools-Struktur, mit eigenen deutschen Namen.
 * Die Zuordnung eines Tools kommt aus seiner bisherigen Kategorie und aus dem vorhandenen Text.
 * Unklare Institutionen und Händler ohne Werkzeugcharakter landen in Spaß & Sonstiges und in der Review-Liste.
 * Die Top 20 ist nur `editorial_rank`: eine redaktionelle Reihenfolge, keine Stimmen und keine Bewertung.
 */
export const DIRECTORY_CATEGORIES = [
  ["Chat & Assistenten", "chat-assistenten", "Dialog, Sprachmodelle und Assistenten für Fragen im Chat."],
  ["Text & Schreiben", "text-schreiben", "Entwürfe, Umschreibungen und längere Texte."],
  ["Bild & Design", "bild-design", "Bilder, Grafik, Layout und 3D-Entwürfe."],
  ["Video", "video", "Clips erzeugen und vorhandenes Material schneiden."],
  ["Audio, Musik & Stimme", "audio-musik-stimme", "Ton, Stimme, Transkript und Musik."],
  ["Code & Entwicklung", "code-entwicklung", "Editoren, Schnittstellen, Hosting und Daten."],
  ["Produktivität", "produktivitaet", "Aufgaben, Notizen, Dokumente und Folien."],
  ["Recherche & Suche", "recherche-suche", "Quellen finden, lesen und gegenüberstellen."],
  ["Marketing & Social Media", "marketing-social", "Kampagnen, SEO, Beiträge und Reichweitenwerkzeuge."],
  ["Automatisierung & Agenten", "automatisierung-agenten", "Abläufe, die Schritte zwischen Diensten abnehmen."],
  ["Bildung & Lernen", "bildung-lernen", "Üben, Erklären und Lernwege."],
  ["Business & Finanzen", "business-finanzen", "Rechnung, Personal, Recht und Kundenvorgänge."],
  ["E-Commerce", "e-commerce", "Shop, Kasse, Bestellung und Zahlungsabwicklung."],
  ["Gesundheit", "gesundheit", "Training, Ernährung und Gesundheitsverwaltung."],
  ["Reisen", "reisen", "Wege, Unterkünfte und Reisepläne."],
  ["Spaß & Sonstiges", "spass-sonstiges", "Spiele und Einträge, die in keine andere Kategorie passen."],
] as const;

export type DirectoryCategorySlug = (typeof DIRECTORY_CATEGORIES)[number][1];

/** Erste passende alte Kategorie gewinnt. E-Commerce und Finanzen stehen vor Code, damit eine Zahlungs-API nicht als Entwicklertool zählt. */
const OLD_PRIORITY: Array<[string, DirectoryCategorySlug]> = [
  ["ki-chatbots", "chat-assistenten"],
  ["videogenerierung", "video"],
  ["videoschnitt", "video"],
  ["bildgenerierung", "bild-design"],
  ["audio-und-sprache", "audio-musik-stimme"],
  ["musik", "audio-musik-stimme"],
  ["textgenerierung", "text-schreiben"],
  ["automatisierung", "automatisierung-agenten"],
  ["e-commerce", "e-commerce"],
  ["finanzen", "business-finanzen"],
  ["seo", "marketing-social"],
  ["social-media", "marketing-social"],
  ["marketing", "marketing-social"],
  ["recherche", "recherche-suche"],
  ["bildung", "bildung-lernen"],
  ["programmierung", "code-entwicklung"],
  ["daten", "code-entwicklung"],
  ["design", "bild-design"],
  ["dreid", "bild-design"],
  ["praesentationen", "produktivitaet"],
  ["produktivitaet", "produktivitaet"],
  ["kundenservice", "business-finanzen"],
  ["personal", "business-finanzen"],
  ["recht", "business-finanzen"],
  ["gesundheit", "gesundheit"],
  ["reisen", "reisen"],
  ["gaming", "spass-sonstiges"],
];

const NOT_A_TOOL = [
  "beaufsichtigt",
  "informiert zu leistungen",
  "veröffentlicht hinweise",
  "veröffentlicht standards",
  "veröffentlicht förder",
  "verkauft 3d-drucker",
  "verkauft platinen",
  "verkauft computer",
  "verkauft spiele",
];

export type CategoryChoice = {
  slug: DirectoryCategorySlug;
  review: boolean;
  reason: string;
};

export function chooseCategory(oldSlugs: string[], text: string): CategoryChoice {
  const haystack = text.toLowerCase();
  if (NOT_A_TOOL.some((phrase) => haystack.includes(phrase))) {
    return {
      slug: "spass-sonstiges",
      review: true,
      reason: "Der vorhandene Text beschreibt eine Behörde, eine Kasse oder einen Verkauf, kein Werkzeug.",
    };
  }
  const have = new Set(oldSlugs);
  for (const [oldSlug, next] of OLD_PRIORITY) {
    if (have.has(oldSlug)) {
      return { slug: next, review: false, reason: `Bisherige Kategorie ${oldSlug}.` };
    }
  }
  if (DIRECTORY_CATEGORIES.some((item) => have.has(item[1]))) {
    const slug = DIRECTORY_CATEGORIES.find((item) => have.has(item[1]))![1];
    return { slug, review: false, reason: "Bereits in der neuen Struktur." };
  }
  return {
    slug: "spass-sonstiges",
    review: true,
    reason: "Keine bisherige Kategorie ließ sich zuordnen.",
  };
}

const FRESH_CATEGORIES = new Set<DirectoryCategorySlug>([
  "chat-assistenten",
  "text-schreiben",
  "bild-design",
  "video",
  "audio-musik-stimme",
  "recherche-suche",
  "automatisierung-agenten",
]);

const FRESH_HINTS = [
  "sprachmodell",
  "chatbot",
  "assistent",
  "erzeugt",
  "generiert",
  "prompt",
  "transkrib",
  "diffusion",
  "aus einer beschreibung",
  "aus text",
  "kurze videos",
  "kurzen clip",
];

const FRESH_BLOCK = ["wordpress", "fernwartung", "vnc", "zahlung", "kasse", "shop-anwendung"];

export function isHomepageFresh(categorySlug: string, text: string) {
  if (!FRESH_CATEGORIES.has(categorySlug as DirectoryCategorySlug)) return false;
  const haystack = text.toLowerCase();
  if (FRESH_BLOCK.some((phrase) => haystack.includes(phrase))) return false;
  return FRESH_HINTS.some((phrase) => haystack.includes(phrase));
}

/**
 * Redaktionsreihenfolge für die Top 20. Nur Tools, die im Verzeichnis stehen.
 * Perplexity und Canva fehlen im Katalog und sind deshalb nicht gesetzt.
 * Notion ist der Eintrag „Notion“, nicht ein separates Produkt namens Notion AI.
 * Pflege und Änderung im Admin über das Feld editorial_rank.
 */
export const EDITORIAL_TOP: Array<{ rank: number; slug: string; name: string }> = [
  { rank: 1, slug: "chatgpt", name: "ChatGPT" },
  { rank: 2, slug: "claude", name: "Claude" },
  { rank: 3, slug: "gemini", name: "Gemini" },
  { rank: 4, slug: "midjourney", name: "Midjourney" },
  { rank: 5, slug: "eleven-labs", name: "Eleven Labs" },
  { rank: 6, slug: "runway", name: "Runway" },
  { rank: 7, slug: "capcut", name: "CapCut" },
  { rank: 8, slug: "notion", name: "Notion" },
  { rank: 9, slug: "cursor", name: "Cursor" },
  { rank: 10, slug: "github-copilot", name: "GitHub Copilot" },
  { rank: 11, slug: "microsoft-copilot", name: "Microsoft Copilot" },
  { rank: 12, slug: "suno", name: "Suno" },
  { rank: 13, slug: "leonardo-ai", name: "Leonardo AI" },
  { rank: 14, slug: "heygen", name: "HeyGen" },
  { rank: 15, slug: "adobe-firefly", name: "Adobe Firefly" },
  { rank: 16, slug: "notebooklm", name: "NotebookLM" },
  { rank: 17, slug: "mistral", name: "Mistral" },
  { rank: 18, slug: "grok", name: "Grok" },
  { rank: 19, slug: "pika-labs", name: "Pika Labs" },
  { rank: 20, slug: "luma-dream-machine", name: "Luma Dream Machine" },
];
