import type { MetadataRoute } from "next";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { listCategories, publishedSlugs } from "@/lib/tools/repository";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const database = await getDb();
  const base = siteConfig.url.replace(/\/$/, "");
  const [tools, categories] = await Promise.all([publishedSlugs(database), listCategories(database)]);
  const staticPaths = [
    "",
    "/tools",
    "/top-20",
    "/neu",
    "/kategorien",
    "/blog",
    "/einreichen",
    "/ueber-uns",
    "/kontakt",
    "/impressum",
    "/datenschutz",
    "/affiliate-hinweis",
  ];
  return [
    ...staticPaths.map((path) => ({
      url: `${base}${path || "/"}`,
      changeFrequency: "daily" as const,
      priority: path === "" ? 1 : 0.7,
    })),
    ...categories.map((category) => ({
      url: `${base}/kategorien/${category.slug}`,
      changeFrequency: "weekly" as const,
      priority: 0.6,
    })),
    ...tools.map((tool) => ({
      url: `${base}/tools/${tool.slug}`,
      lastModified: tool.updatedAt,
      changeFrequency: "weekly" as const,
      priority: 0.8,
    })),
  ];
}
