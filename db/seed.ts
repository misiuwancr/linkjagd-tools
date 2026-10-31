import { eq } from "drizzle-orm";
import { categories, newsPosts, tools, users } from "@/db/schema";
import { getDb, type AppDatabase } from "@/db/client";
import { bootstrapAdminDecision } from "@/db/resolve";
import { hashPassword } from "@/lib/auth/password";
import { replaceCategories, replaceTags, refreshSearchText } from "@/lib/tools/repository";

const categorySeed = [
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
    category: "chat-assistenten",
    pricing: "freemium",
    featured: true,
    rank: 1,
    short: "Beispiel eines Chat-Werkzeugs für Alltag und kurze Arbeitsfragen.",
    tags: ["Beispiel", "Chat"],
  },
  {
    slug: "hafenbot",
    name: "Hafenbot",
    category: "chat-assistenten",
    pricing: "free",
    short: "Zweites Beispiel in derselben Kategorie, damit ähnliche Tools sichtbar sind.",
    tags: ["Beispiel", "Chat"],
  },
  {
    slug: "atelier-pixel",
    name: "Atelier Pixel",
    category: "bild-design",
    pricing: "paid",
    featured: true,
    rank: 2,
    short: "Beispiel für Bildentwürfe aus kurzen Beschreibungen.",
    tags: ["Beispiel", "Bild"],
  },
  {
    slug: "rolle-24",
    name: "Rolle 24",
    category: "video",
    pricing: "freemium",
    featured: true,
    rank: 3,
    short: "Beispiel für kurze Videoclips aus einem Stichwort.",
    tags: ["Beispiel", "Video"],
  },
  {
    slug: "klammer-code",
    name: "Klammer Code",
    category: "code-entwicklung",
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
    category: "automatisierung-agenten",
    pricing: "freemium",
    featured: true,
    rank: 6,
    short: "Beispiel für kleine Abläufe zwischen Formular und Tabelle.",
    tags: ["Beispiel"],
  },
  {
    slug: "marktfunke",
    name: "Marktfunke",
    category: "marketing-social",
    pricing: "paid",
    rank: 7,
    short: "Beispiel für Kampagnentexte und einfache Auswertungen.",
    tags: ["Beispiel"],
  },
  {
    slug: "pinnwand-social",
    name: "Pinnwand Social",
    category: "marketing-social",
    pricing: "freemium",
    rank: 8,
    short: "Beispiel, das Beitragsskizzen für soziale Netzwerke sammelt.",
    tags: ["Beispiel"],
  },
  {
    slug: "quellenkamm",
    name: "Quellenkamm",
    category: "recherche-suche",
    pricing: "free",
    short: "Beispiel, das Fundstellen nebeneinanderlegt.",
    tags: ["Beispiel"],
  },
  {
    slug: "satzwerk",
    name: "Satzwerk",
    category: "text-schreiben",
    pricing: "freemium",
    featured: true,
    short: "Beispiel für Entwürfe längerer deutscher Texte.",
    tags: ["Beispiel", "Text"],
  },
  {
    slug: "klangraum",
    name: "Klangraum",
    category: "audio-musik-stimme",
    pricing: "paid",
    short: "Beispiel für Sprache zu Ton und zurück.",
    tags: ["Beispiel"],
  },
  {
    slug: "formlinie",
    name: "Formlinie",
    category: "bild-design",
    pricing: "freemium",
    short: "Beispiel für Layoutvarianten einer einfachen Seite.",
    tags: ["Beispiel"],
  },
  {
    slug: "lernpfad",
    name: "Lernpfad",
    category: "bildung-lernen",
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
    category: "recherche-suche",
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

  const existingNews = await database.select({ id: newsPosts.id }).from(newsPosts).limit(1);
  if (!existingNews[0]) {
    const now = new Date();
    await database.insert(newsPosts).values({
      id: crypto.randomUUID(),
      title: "Woran ein Beitrag erkannt wird",
      slug: "woran-ein-beitrag-erkannt-wird",
      excerpt: "Ein Entwurf, der erklärt, wann ein Text auf dem Blog öffentlich wird.",
      body: "Dieser Text ist ein Entwurf.\n\nEr wird nicht ausgeliefert, solange der Status Entwurf bleibt.\n\n- Die Redaktion schreibt selbst.\n- Nichts davon ist eine Meldung einer Nachrichtenagentur.",
      status: "draft",
      publishedAt: null,
      createdAt: now,
      updatedAt: now,
    });
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
