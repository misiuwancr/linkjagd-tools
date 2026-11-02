import { eq } from "drizzle-orm";
import { z } from "zod";
import type { AppDatabase } from "@/db/client";
import { categories, tools } from "@/db/schema";
import { importToolSchema } from "@/lib/validation/tool";
import { domainFromUrl, slugify } from "@/lib/utils";
import { findDuplicateTool } from "@/lib/tools/repository";
import { importDiscoveredTool } from "./service";

export const batchCandidateSchema = importToolSchema.extend({
  pricingModel: z.enum(["free", "freemium", "paid"]),
  evidence: z.object({
    officialUrl: z.string().url(),
    checkedAt: z.string().datetime(),
    httpStatus: z.number().int().min(200).max(299),
    productFacts: z.string().trim().min(20),
    pricingSource: z.string().url(),
    pricingFacts: z.string().trim().min(10),
    reviewed: z.literal(true),
  }),
});

/** Insert-only, atomic per candidate. Database deduplication is also the resume checkpoint. */
export async function importBatchCandidate(db: AppDatabase, raw: unknown, publish = false, dryRun = true) {
  const parsed = batchCandidateSchema.safeParse(raw);
  if (!parsed.success) return { status: "invalid", issues: parsed.error.issues.map(i => `${i.path.join(".")}: ${i.message}`) };
  const input = parsed.data;
  const age = Date.now() - Date.parse(input.evidence.checkedAt);
  if (age < -300000 || age > 30 * 86400000) return { status: "invalid", issues: ["Prüfbeleg ist nicht aktuell."] };
  if (domainFromUrl(input.originalUrl) !== domainFromUrl(input.evidence.officialUrl)) return { status: "invalid", issues: ["Anbieter und Prüfbeleg stimmen nicht überein."] };
  const check = async (database: AppDatabase) => {
    const duplicate = await findDuplicateTool(database, domainFromUrl(input.originalUrl), slugify(input.name), input.originalUrl);
    if (duplicate) return { status: "duplicate", slug: duplicate.slug };
    if (!input.categorySlugs.length) return { status: "invalid", issues: ["Kategorie fehlt."] };
    for (const slug of input.categorySlugs) {
      if (!(await database.select().from(categories).where(eq(categories.slug, slug)).limit(1)).length) return { status: "invalid", issues: [`Unbekannte Kategorie: ${slug}`] };
    }
    if (dryRun) return { status: "ready", slug: slugify(input.name) };
    const result = await importDiscoveredTool(database, input);
    if (!result.ok) throw new Error(result.error);
    await database.update(tools).set({
      publishStatus: publish ? "published" : "draft",
      lastCheckedAt: new Date(input.evidence.checkedAt),
      internalNotes: JSON.stringify({ batchEvidence: input.evidence }),
    }).where(eq(tools.id, result.id));
    return { status: publish ? "published" : "draft", slug: result.slug };
  };
  if (dryRun) return check(db);
  // Repository helpers use only select/insert/update/delete, all supplied by tx.
  return db.transaction(tx => check(tx as unknown as AppDatabase));
}
