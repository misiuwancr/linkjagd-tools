import { z } from "zod";
import { eq, inArray } from "drizzle-orm";
import type { AppDatabase } from "@/db/client";
import { siteSettings } from "@/db/schema";
export const blogTopics = [{ value: "entdecken", label: "Entdecken" }, { value: "vergleiche", label: "Vergleiche & Anleitungen" }, { value: "news", label: "News" }] as const;
export type BlogTopic = typeof blogTopics[number]["value"];
const slug = z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/).max(80);
export const postEditorialSchema = z.object({ topic: z.enum(["entdecken", "vergleiche", "news"]), toolSlugs: z.array(slug).max(30).default([]), relatedSlugs: z.array(slug).max(12).default([]) });
export type PostEditorial = z.infer<typeof postEditorialSchema>;
export function defaultPostEditorial(slug: string): PostEditorial { return { topic: /vergleich|anleitung|automatisier|workflow|e-commerce|shopify|woocommerce/.test(slug) ? "vergleiche" : "entdecken", toolSlugs: [], relatedSlugs: [] }; }
export function parsePostEditorial(value: string | undefined, slug: string) { try { const parsed = postEditorialSchema.safeParse(JSON.parse(value || "")); return parsed.success ? parsed.data : defaultPostEditorial(slug); } catch { return defaultPostEditorial(slug); } }
export async function readPostEditorial(database: AppDatabase, id: string, slug: string) { const [row] = await database.select().from(siteSettings).where(eq(siteSettings.key, "post_editorial:" + id)).limit(1); return parsePostEditorial(row?.value, slug); }
export async function readPostEditorialBatch(database: AppDatabase, posts: { id: string; slug: string }[]) { if (!posts.length) return new Map<string, PostEditorial>(); const rows = await database.select().from(siteSettings).where(inArray(siteSettings.key, posts.map((post) => "post_editorial:" + post.id))); const values = new Map(rows.map((row) => [row.key, row.value])); return new Map(posts.map((post) => [post.id, parsePostEditorial(values.get("post_editorial:" + post.id), post.slug)])); }
export async function savePostEditorial(database: AppDatabase, id: string, input: PostEditorial) { const value = JSON.stringify(postEditorialSchema.parse(input)); await database.insert(siteSettings).values({ key: "post_editorial:" + id, value }).onConflictDoUpdate({ target: siteSettings.key, set: { value } }); }
