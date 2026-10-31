import type { MetadataRoute } from "next";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { ALTERNATIVE_SLUGS } from "@/lib/alternatives";
import { USE_CASES } from "@/lib/use-cases";
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
    "/glossar",
    "/faq",
    "/newsletter",
    "/ueber-uns",
    "/kontakt",
    "/impressum",
    "/datenschutz",
    "/affiliate-hinweis",
    "/fuer",
  ];
  return [
    ...staticPaths.map((path) => ({
      url: `${base}${path || "/"}`,
      changeFrequency: "daily" as const,
      priority: path === "" ? 1 : 0.7,
    })),
    ...USE_CASES.map((item) => ({
      url: `${base}/fuer/${item.slug}`,
      changeFrequency: "weekly" as const,
      priority: 0.5,
    })),
    ...ALTERNATIVE_SLUGS.map((slug) => ({
      url: `${base}/alternativen/${slug}`,
      changeFrequency: "weekly" as const,
      priority: 0.5,
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
