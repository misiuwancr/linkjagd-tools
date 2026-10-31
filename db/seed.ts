import { eq } from "drizzle-orm";
import { categories, tools, users } from "@/db/schema";
import { getDb, type AppDatabase } from "@/db/client";
import { bootstrapAdminDecision } from "@/db/resolve";
import { hashPassword } from "@/lib/auth/password";
import { replaceCategories, replaceTags, refreshSearchText } from "@/lib/tools/repository";

const categorySeed = [
  ["KI-Chatbots", "ki-chatbots", "Dialogsysteme für Fragen, Texte und Alltagsaufgaben."],
  ["Bildgenerierung", "bildgenerierung", "Werkzeuge, die aus Beschreibungen Bilder erzeugen."],
  ["Videogenerierung", "videogenerierung", "Werkzeuge für Clips, Szenen und bewegte Bilder."],
  ["Programmierung", "programmierung", "Hilfe beim Schreiben, Erklären und Prüfen von Code."],
  ["Produktivität", "produktivitaet", "Planen, Schreiben und Aufräumen im Arbeitsalltag."],
  ["Automatisierung", "automatisierung", "Abläufe, die wiederkehrende Schritte abnehmen."],
  ["Marketing", "marketing", "Texte, Kampagnen und Auswertung für Angebote."],
  ["Social Media", "social-media", "Beiträge, Formate und Planung für soziale Netzwerke."],
  ["Recherche", "recherche", "Quellen finden, lesen und gegenüberstellen."],
  ["Textgenerierung", "textgenerierung", "Entwürfe, Umschreibungen und längere Texte."],
  ["Audio und Sprache", "audio-und-sprache", "Sprache, Stimmen und Ton."],
  ["Design", "design", "Layout, Varianten und visuelle Entwürfe."],
  ["Bildung", "bildung", "Erklären, Üben und Lernwege."],
  ["E-Commerce", "e-commerce", "Produktdaten, Listings und Shop-Texte."],
  ["Finanzen", "finanzen", "Haushalt, Rechnungen und Buchhaltung."],
  ["Gesundheit", "gesundheit", "Training, Ernährung und Wohlbefinden."],
  ["Reisen", "reisen", "Wege, Unterkünfte und Reisepläne."],
  ["Recht", "recht", "Verträge, Signaturen und rechtliche Texte."],
  ["Personal", "personal", "Bewerbungen, Personal und Schichtplanung."],
  ["Kundenservice", "kundenservice", "Tickets, Chat und Hilfe für Kunden."],
  ["SEO", "seo", "Sichtbarkeit in der Suche und Seitenprüfung."],
  ["Daten", "daten", "Tabellen, Abfragen und Auswertungen."],
  ["Präsentationen", "praesentationen", "Folien und Vorträge."],
  ["Musik", "musik", "Komposition, Noten und Musikproduktion."],
  ["3D", "dreid", "Modelle, Räume und Druckvorlagen."],
  ["Gaming", "gaming", "Spiele, Engines und spielbare Geschichten."],
  ["Videoschnitt", "videoschnitt", "Schneiden, Untertitel und Schnitt am eigenen Material."],
] as const;

const exampleNote = "Beispieldatensatz für die Entwicklung. Kein reales Angebot und kein Partnerlink.";

type ExampleTool = {
  slug: string;
  name: string;
  category: string;
  pricing: "free" | "freemium" | "paid";
  featured?: boolean;
  rank?: number;
  status?: "draft" | "published" | "archived";
  source?: string;
  short: string;
  tags: string[];
};

const exampleTools: ExampleTool[] = [
  {
    slug: "nordlicht-chat",
    name: "Nordlicht Chat",
    category: "ki-chatbots",
    pricing: "freemium",
    featured: true,
    rank: 1,
    short: "Beispiel eines Chat-Werkzeugs für Alltag und kurze Arbeitsfragen.",
    tags: ["Beispiel", "Chat"],
  },
  {
    slug: "hafenbot",
    name: "Hafenbot",
    category: "ki-chatbots",
    pricing: "free",
    short: "Zweites Beispiel in derselben Kategorie, damit ähnliche Tools sichtbar sind.",
    tags: ["Beispiel", "Chat"],
  },
  {
    slug: "atelier-pixel",
    name: "Atelier Pixel",
    category: "bildgenerierung",
    pricing: "paid",
    featured: true,
    rank: 2,
    short: "Beispiel für Bildentwürfe aus kurzen Beschreibungen.",
    tags: ["Beispiel", "Bild"],
  },
  {
    slug: "rolle-24",
    name: "Rolle 24",
    category: "videogenerierung",
    pricing: "freemium",
    featured: true,
    rank: 3,
    short: "Beispiel für kurze Videoclips aus einem Stichwort.",
    tags: ["Beispiel", "Video"],
  },
  {
    slug: "klammer-code",
    name: "Klammer Code",
    category: "programmierung",
    pricing: "free",
    rank: 4,
    short: "Beispiel eines offenen Werkzeugs, das Code erklärt.",
    tags: ["Beispiel", "Code"],
  },
  {
    slug: "fokusplan",
    name: "Fokusplan",
    category: "produktivitaet",
    pricing: "free",
    rank: 5,
    short: "Beispiel, das eine Aufgabenliste in einen Tagesplan sortiert.",
    tags: ["Beispiel"],
  },
  {
    slug: "webstuhl",
    name: "Webstuhl",
    category: "automatisierung",
    pricing: "freemium",
    featured: true,
    rank: 6,
    short: "Beispiel für kleine Abläufe zwischen Formular und Tabelle.",
    tags: ["Beispiel"],
  },
  {
    slug: "marktfunke",
    name: "Marktfunke",
    category: "marketing",
    pricing: "paid",
    rank: 7,
    short: "Beispiel für Kampagnentexte und einfache Auswertungen.",
    tags: ["Beispiel"],
  },
  {
    slug: "pinnwand-social",
    name: "Pinnwand Social",
    category: "social-media",
    pricing: "freemium",
    rank: 8,
    short: "Beispiel, das Beitragsskizzen für soziale Netzwerke sammelt.",
    tags: ["Beispiel"],
  },
  {
    slug: "quellenkamm",
    name: "Quellenkamm",
    category: "recherche",
    pricing: "free",
    short: "Beispiel, das Fundstellen nebeneinanderlegt.",
    tags: ["Beispiel"],
  },
  {
    slug: "satzwerk",
    name: "Satzwerk",
    category: "textgenerierung",
    pricing: "freemium",
    featured: true,
    short: "Beispiel für Entwürfe längerer deutscher Texte.",
    tags: ["Beispiel", "Text"],
  },
  {
    slug: "klangraum",
    name: "Klangraum",
    category: "audio-und-sprache",
    pricing: "paid",
    short: "Beispiel für Sprache zu Ton und zurück.",
    tags: ["Beispiel"],
  },
  {
    slug: "formlinie",
    name: "Formlinie",
    category: "design",
    pricing: "freemium",
    short: "Beispiel für Layoutvarianten einer einfachen Seite.",
    tags: ["Beispiel"],
  },
  {
    slug: "lernpfad",
    name: "Lernpfad",
    category: "bildung",
    pricing: "free",
    short: "Beispiel, das ein Thema in kurze Übungsschritte teilt.",
    tags: ["Beispiel"],
  },
  {
    slug: "ladentheke",
    name: "Ladentheke",
    category: "e-commerce",
    pricing: "paid",
    short: "Beispiel für Produkttexte in einem kleinen Shop.",
    tags: ["Beispiel"],
  },
  {
    slug: "stilles-werkzeug",
    name: "Stilles Werkzeug",
    category: "recherche",
    pricing: "free",
    status: "draft",
    source: "import",
    short: "Beispiel eines importierten Entwurfs, der noch nicht öffentlich ist.",
    tags: ["Beispiel"],
  },
  {
    slug: "zweite-fundstelle",
    name: "Zweite Fundstelle",
    category: "produktivitaet",
    pricing: "freemium",
    status: "draft",
    source: "submission",
    short: "Beispiel einer Einreichung, die in der Moderation wartet.",
    tags: ["Beispiel"],
  },
  {
    slug: "archivregal",
    name: "Archivregal",
    category: "produktivitaet",
    pricing: "free",
    status: "archived",
    short: "Beispiel eines archivierten Eintrags, der nicht mehr gelistet wird.",
    tags: ["Beispiel"],
  },
];

async function seed() {
  const database = await getDb();
  const now = Date.now();
  for (const [index, [name, slug, description]] of categorySeed.entries()) {
    const existing = await database.select().from(categories).where(eq(categories.slug, slug)).limit(1);
    if (existing[0]) continue;
    const stamp = new Date(now);
    await database.insert(categories).values({
      id: slug,
      name,
      slug,
      description,
      sortOrder: index + 1,
      createdAt: stamp,
      updatedAt: stamp,
    });
  }

  for (const [index, example] of exampleTools.entries()) {
    const existing = await database.select().from(tools).where(eq(tools.slug, example.slug)).limit(1);
    if (existing[0]) {
      if (existing[0].isExample) {
        await database
          .update(tools)
          .set({
            publishStatus: "archived",
            featured: false,
            editorialRank: null,
            updatedAt: new Date(),
          })
          .where(eq(tools.id, existing[0].id));
      }
      continue;
    }
    const createdAt = new Date(now - (exampleTools.length - index) * 86_400_000);
    const id = crypto.randomUUID();
    const long = `${example.short} ${exampleNote} Die ausführliche Beschreibung zeigt nur, wie eine Detailseite aufgebaut ist: Wofür das Werkzeug gedacht wäre, für wen es sich eignen könnte und welche Grenze die Redaktion dazu sagen würde.`;
    const features = [
      "Beispielhafte Funktion, keine geprüfte Produkteigenschaft.",
      "Zweite Beispielzeile für die Funktionsliste.",
      "Dritte Beispielzeile, damit das Layout sichtbar wird.",
    ];
    const screenshots = example.slug === "nordlicht-chat" ? ["/examples/nordlicht-screen.svg"] : [];
    await database.insert(tools).values({
      id,
      name: example.name,
      slug: example.slug,
      originalUrl: `https://${example.slug}.example/`,
      domain: `${example.slug}.example`,
      shortDescriptionDe: example.short,
      longDescriptionDe: long,
      featuresDe: JSON.stringify(features),
      screenshots: JSON.stringify(screenshots),
      pricingModel: example.pricing,
      licenseType: example.slug === "klammer-code" ? "open_source" : "unknown",
      publishStatus: "archived",
      featured: false,
      editorialRank: null,
      discoverySource: example.source ?? "example",
      isExample: true,
      internalNotes: exampleNote,
      searchText: "",
      createdAt,
      updatedAt: createdAt,
    });
    await replaceCategories(database, id, [example.category]);
    await replaceTags(database, id, example.tags);
    await refreshSearchText(database, id);
  }

  await ensureAdmin(database);
  console.log("Seed geprüft.");
}

export async function ensureAdmin(database: AppDatabase) {
  const existingUsers = await database.select({ id: users.id }).from(users).limit(1);
  const decision = bootstrapAdminDecision(process.env, Boolean(existingUsers[0]));
  if (decision === "skip-exists") return decision;
  if (decision === "skip-config") {
    console.warn("Kein Admin angelegt. ADMIN_EMAIL und ein Passwort mit mindestens 12 Zeichen setzen.");
    return decision;
  }
  const email = (process.env.ADMIN_EMAIL || "").trim().toLowerCase();
  const password = process.env.ADMIN_PASSWORD || "";
  try {
    await database.insert(users).values({
      id: crypto.randomUUID(),
      email,
      passwordHash: hashPassword(password),
      role: "admin",
      createdAt: new Date(),
    });
  } catch {
    const again = await database.select({ id: users.id }).from(users).limit(1);
    if (again[0]) return "skip-exists" as const;
    throw new Error("Admin konnte nicht angelegt werden.");
  }
  console.log("Admin angelegt.");
  return decision;
}

if (process.argv[1]?.includes("seed.ts")) {
  import("dotenv/config").then(() => seed());
}

export { seed };
