import { cache } from "react";
import { eq } from "drizzle-orm";
import { getDb, type AppDatabase } from "@/db/client";
import { newsPosts } from "@/db/schema";
import { comparisons, researchDate } from "@/lib/comparisons";
import { readPostEditorialBatch, type BlogTopic } from "@/lib/blog-metadata";
import { siteConfig } from "@/site.config";
export type ContentArticle = { slug: string; title: string; excerpt: string; topic: BlogTopic; toolSlugs: string[]; relatedSlugs: string[]; publishedAt: string | null; modifiedAt: string; coded: boolean };
export function linkedToolSlugs(body: string) {
  const slugs = new Set<string>();
  for (const match of body.matchAll(/\[[^\]]*\]\(([^\s)]+)\)/g)) {
    try { const url = new URL(match[1], siteConfig.url); if (url.origin !== new URL(siteConfig.url).origin) continue; const tool = url.pathname.match(/^\/(?:tools|go)\/([a-z0-9]+(?:-[a-z0-9]+)*)$/); if (tool) slugs.add(tool[1]); } catch { /* Invalid links don't create a relationship. */ }
  }
  return [...slugs];
}
export async function contentArticles(database: AppDatabase): Promise<ContentArticle[]> {
  const posts = await database.select().from(newsPosts).where(eq(newsPosts.status, "published"));
  const meta = await readPostEditorialBatch(database, posts);
  const articles = new Map<string, ContentArticle>(posts.map((post) => { const editorial = meta.get(post.id)!; return [post.slug, { slug: post.slug, title: post.title, excerpt: post.excerpt, topic: editorial.topic, toolSlugs: [...new Set([...editorial.toolSlugs, ...linkedToolSlugs(post.body)])], relatedSlugs: editorial.relatedSlugs, publishedAt: post.publishedAt?.toISOString() ?? null, modifiedAt: post.updatedAt.toISOString(), coded: false }]; }));
  for (const item of comparisons) articles.set(item.slug, { slug: item.slug, title: item.title, excerpt: item.intro, topic: "vergleiche", toolSlugs: item.tools, relatedSlugs: [], publishedAt: null, modifiedAt: researchDate, coded: true });
  return [...articles.values()].sort((a, b) => b.modifiedAt.localeCompare(a.modifiedAt) || a.slug.localeCompare(b.slug));
}
export const publicArticles = cache(async () => contentArticles(await getDb()));
export function relatedArticles(current: ContentArticle, all: ContentArticle[]) {
  const score = (post: ContentArticle) => (current.relatedSlugs.includes(post.slug) ? 100 : 0) + post.toolSlugs.filter((slug) => current.toolSlugs.includes(slug)).length * 10 + (post.topic === current.topic ? 1 : 0);
  return all.filter((post) => post.slug !== current.slug && score(post) > 0).sort((a, b) => score(b) - score(a) || a.slug.localeCompare(b.slug)).slice(0, 3);
}
