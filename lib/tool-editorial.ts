import { z } from "zod";
import { eq, inArray, sql } from "drizzle-orm";
import type { AppDatabase } from "@/db/client";
import { siteSettings, tools } from "@/db/schema";
import { validateExternalUrl } from "@/lib/affiliate/redirect";

export const linkjagdVideoSchema = z.object({
  id: z.string().trim().min(1).max(80).regex(/^[a-zA-Z0-9][a-zA-Z0-9_-]*$/, "Video-Kennung: nur Buchstaben, Ziffern, Bindestrich und Unterstrich."),
  title: z.string().trim().min(2).max(160),
  part: z.number().int().min(1).max(100000).nullable().default(null),
  url: z.string().trim().max(500).default("").refine((url) => !url || (/^https:\/\//i.test(url) && validateExternalUrl(url).ok), "Nur öffentliche HTTPS-Videolinks verwenden."),
});
export type LinkjagdVideo = z.infer<typeof linkjagdVideoSchema>;
export const toolEditorialSchema = z.object({
  hasBeenPublished: z.boolean().default(false),
  publishedAt: z.string().datetime().nullable().default(null),
  videos: z.array(linkjagdVideoSchema).max(20).default([]),
}).refine((value) => new Set(value.videos.map((video) => video.id)).size === value.videos.length, "Eine Video-Kennung pro Tool nur einmal zuordnen.")
  .refine((value) => !value.publishedAt || new Date(value.publishedAt).getTime() <= Date.now(), "Veröffentlichungsdatum darf nicht in der Zukunft liegen.");
export type ToolEditorial = z.infer<typeof toolEditorialSchema>;
export const editorialKey = (toolId: string) => `tool_editorial:${toolId}`;
export const emptyEditorial = (): ToolEditorial => ({ publishedAt: null, videos: [], hasBeenPublished: false });
export function parseEditorial(value: string | null | undefined): ToolEditorial {
  try { const parsed = toolEditorialSchema.safeParse(JSON.parse(value || "{}")); return parsed.success ? parsed.data : emptyEditorial(); } catch { return emptyEditorial(); }
}
export async function readToolEditorial(database: AppDatabase, toolId: string) {
  const [row] = await database.select().from(siteSettings).where(eq(siteSettings.key, editorialKey(toolId))).limit(1);
  return parseEditorial(row?.value);
}
export async function readEditorialBatch(database: AppDatabase, ids: string[]) {
  if (!ids.length) return new Map<string, ToolEditorial>();
  const rows = await database.select().from(siteSettings).where(inArray(siteSettings.key, ids.map(editorialKey)));
  return new Map(rows.map((row) => [row.key.slice("tool_editorial:".length), parseEditorial(row.value)]));
}
export async function saveToolEditorial(database: AppDatabase, toolId: string, value: z.input<typeof toolEditorialSchema>) {
  const parsed = toolEditorialSchema.parse(value);
  if (parsed.publishedAt && new Date(parsed.publishedAt).getTime() > Date.now()) throw new Error("Veröffentlichungsdatum darf nicht in der Zukunft liegen.");
  await database.insert(siteSettings).values({ key: editorialKey(toolId), value: JSON.stringify(parsed) }).onConflictDoUpdate({ target: siteSettings.key, set: { value: JSON.stringify(parsed) } });
}
// Only validated editorial metadata is written here. Invalid legacy settings are
// ignored by JSON expressions rather than causing public pages to fail.
export const publicationSql = sql`(select json_extract(case when json_valid(s.value) then s.value else '{}' end, '$.publishedAt') from site_settings s where s.key = 'tool_editorial:' || tools.id)`;
export function linkjagdAssignmentSql(videoId?: string, search?: string) {
  return sql`exists (select 1 from site_settings s, json_each(case when json_valid(s.value) then s.value else '{}' end, '$.videos') v where s.key = 'tool_editorial:' || tools.id ${videoId ? sql`and json_extract(v.value, '$.id') = ${videoId}` : sql``} ${search ? sql`and lower(json_extract(v.value, '$.id') || ' ' || json_extract(v.value, '$.title') || ' ' || coalesce(json_extract(v.value, '$.part'), '')) like ${`%${search.toLowerCase().replace(/[%_\\]/g, "")}%`}` : sql``})`;
}
export async function listAssignedVideos(database: AppDatabase) {
  const rows = await database.select({ value: siteSettings.value }).from(siteSettings).innerJoin(tools, sql`${siteSettings.key} = 'tool_editorial:' || ${tools.id}`).where(sql`${tools.publishStatus} = 'published' and ${tools.isExample} = 0`);
  const videos = new Map<string, LinkjagdVideo>();
  for (const row of rows) for (const video of parseEditorial(row.value).videos) if (!videos.has(video.id)) videos.set(video.id, video);
  return [...videos.values()].sort((a, b) => (a.part ?? Number.MAX_SAFE_INTEGER) - (b.part ?? Number.MAX_SAFE_INTEGER) || a.title.localeCompare(b.title, "de"));
}
