import { eq } from "drizzle-orm";
import { categories, tools } from "@/db/schema";
import type { AppDatabase } from "@/db/client";
import { importToolSchema } from "@/lib/validation/tool";
import { domainFromUrl, slugify } from "@/lib/utils";
import {
  findByDomainOrSlug,
  refreshSearchText,
  replaceCategories,
  replaceTags,
} from "@/lib/tools/repository";

export async function importDiscoveredTool(database: AppDatabase, payload: unknown) {
  const parsed = importToolSchema.safeParse(payload);
  if (!parsed.success) {
    return {
      ok: false as const,
      status: 400,
      error: "Die Importdaten sind ungültig.",
      issues: parsed.error.issues.map((issue) => issue.message),
    };
  }
  const input = parsed.data;
  const domain = domainFromUrl(input.originalUrl);
  const slug = slugify(input.name);
  if (!slug) {
    return { ok: false as const, status: 400, error: "Aus dem Namen lässt sich kein Kurzname bilden." };
  }
  const existing = await findByDomainOrSlug(database, domain, slug);
  if (existing) {
    return {
      ok: false as const,
      status: 409,
      error: "Ein Tool mit dieser Domain oder diesem Kurznamen existiert bereits.",
      existingSlug: existing.slug,
      duplicate: existing.domain === domain ? "domain" : "slug",
    };
  }
  const now = new Date();
  const id = crypto.randomUUID();
  await database.insert(tools).values({
    id,
    name: input.name,
    slug,
    originalUrl: input.originalUrl,
    domain,
    shortDescriptionDe: input.shortDescriptionDe,
    longDescriptionDe: input.longDescriptionDe,
    featuresDe: "[]",
    screenshots: "[]",
    pricingModel: input.pricingModel,
    publishStatus: "draft",
    featured: false,
    discoverySource: input.discoverySource,
    isExample: false,
    searchText: "",
    createdAt: now,
    updatedAt: now,
  });
  if (input.categorySlugs.length > 0) {
    const matched: string[] = [];
    for (const categorySlug of input.categorySlugs) {
      const rows = await database.select().from(categories).where(eq(categories.slug, categorySlug)).limit(1);
      if (rows[0]) matched.push(rows[0].id);
    }
    await replaceCategories(database, id, matched);
  }
  await replaceTags(database, id, input.tags);
  await refreshSearchText(database, id);
  return { ok: true as const, status: 201, id, slug, publishStatus: "draft" as const };
}
