import { createClient } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import { describe, expect, it } from "vitest";
import * as schema from "@/db/schema";
import { applyMigrations } from "@/db/migrate";
import { listPublishedNews, publishedBlogCount, publishedBlogSlugs } from "@/lib/tools/repository";
import { directoryHref, publicListQuery } from "@/lib/tools/query";

describe("Blog-Seiten und Sitemap", () => {
  it("zeigt alle 25 veröffentlichten Beiträge auf zwei Seiten und keinen Entwurf", async () => {
    const client = createClient({ url: ":memory:" });
    try {
      await applyMigrations(client);
      const db = drizzle(client, { schema });
      for (let n = 0; n < 26; n++) await db.insert(schema.newsPosts).values({
        id: `post-${String(n).padStart(2, "0")}`, slug: `post-${n}`, title: `Beitrag ${n}`, excerpt: "Test", body: "Text",
        status: n === 25 ? "draft" : "published", publishedAt: new Date(2026, 0, 1), createdAt: new Date(), updatedAt: new Date(),
      });
      const first = await listPublishedNews(db, 24, 0);
      const second = await listPublishedNews(db, 24, 24);
      expect(first).toHaveLength(24); expect(second).toHaveLength(1);
      expect(new Set([...first, ...second].map((post) => post.id)).size).toBe(25);
      expect(await publishedBlogCount(db)).toBe(25);
      const sitemap = await publishedBlogSlugs(db);
      expect(sitemap).toHaveLength(25);
      expect(sitemap.some((post) => post.slug === "post-25")).toBe(false);
      expect(directoryHref("/blog", publicListQuery({}), { page: 2 })).toBe("/blog?seite=2");
    } finally { client.close(); }
  });
});
