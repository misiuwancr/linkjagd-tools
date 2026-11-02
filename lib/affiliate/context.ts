import type { AppDatabase } from "@/db/client";
import { siteSettings, tools, newsPosts, categories } from "@/db/schema";
import { eq, sql } from "drizzle-orm";
import { getComparison } from "@/lib/comparisons";
import { getUseCase } from "@/lib/use-cases";
import { isAlternativeSlug } from "@/lib/alternatives";

export const ctaPositions = ["card", "hero", "table", "recommendation", "article", "sidebar", "sticky", "alternatives", "unknown"] as const;
export type CtaPosition = typeof ctaPositions[number];
export function goHref(slug: string, source: string, position: CtaPosition, official = false) {
  const params = new URLSearchParams({ quelle: source, position });
  if (official) params.set("ziel", "offiziell");
  return `/go/${encodeURIComponent(slug)}?${params.toString()}`;
}
export async function clickContext(database: AppDatabase, rawSource: string | null, rawPosition: string | null) {
  const position: CtaPosition = ctaPositions.includes(rawPosition as CtaPosition) ? rawPosition as CtaPosition : "unknown";
  let source = "unbekannt";
  const value = rawSource ?? "";
  if (["/", "/tools", "/neu", "/top-20", "/linkjagd", "/empfehlungen", "/vergleiche"].includes(value)) source = value;
  const match = value.match(/^\/(blog|tools|kategorien|fuer|alternativen)\/([a-z0-9]+(?:-[a-z0-9]+)*)$/);
  if (match) {
    const [, kind, slug] = match;
    if (kind === "blog") { const post = getComparison(slug) || (await database.select().from(newsPosts).where(eq(newsPosts.slug, slug)).limit(1))[0]; if (post && (!("status" in post) || post.status === "published")) source = value; }
    if (kind === "tools") { const tool = (await database.select().from(tools).where(eq(tools.slug, slug)).limit(1))[0]; if (tool?.publishStatus === "published" && !tool.isExample) source = value; }
    if (kind === "kategorien" && (await database.select({ id: categories.id }).from(categories).where(eq(categories.slug, slug)).limit(1))[0]) source = value;
    if (kind === "fuer" && getUseCase(slug)) source = value;
    if (kind === "alternativen" && isAlternativeSlug(slug)) source = value;
  }
  return { source, position };
}
export type ContextClick = { toolId: string; programId: string | null; kind: "affiliate" | "official"; day: string; source: string; position: CtaPosition };
export function contextClickInsert(database: AppDatabase, input: ContextClick) {
  const key = "click_context:" + [input.day, input.toolId, input.kind, input.programId ?? "", input.source, input.position].map(encodeURIComponent).join(":");
  const value = JSON.stringify({ ...input, count: 1 });
  return database.insert(siteSettings).values({ key, value }).onConflictDoUpdate({ target: siteSettings.key, set: { value: sql`json_set(${siteSettings.value}, '$.count', cast(json_extract(${siteSettings.value}, '$.count') as integer) + 1)` } });
}
export async function contextClickStats(database: AppDatabase, since: string) {
  const rows = await database.all<{ source: string; position: string; count: number; affiliate: number; official: number }>(sql`select json_extract(value, '$.source') as source, json_extract(value, '$.position') as position, sum(cast(json_extract(value, '$.count') as integer)) as count, sum(case when json_extract(value, '$.kind') = 'affiliate' then cast(json_extract(value, '$.count') as integer) else 0 end) as affiliate, sum(case when json_extract(value, '$.kind') = 'official' then cast(json_extract(value, '$.count') as integer) else 0 end) as official from site_settings where key like 'click_context:%' and json_valid(value) and json_extract(value, '$.day') >= ${since} group by source, position order by count desc, source asc`);
  return rows.map((row) => ({ ...row, count: Number(row.count), affiliate: Number(row.affiliate), official: Number(row.official) }));
}
