import fs from "node:fs";
import { createClient } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import { describe, expect, it } from "vitest";
import * as schema from "@/db/schema";
import { applyMigrations } from "@/db/migrate";
import { editorialStarterSlugs } from "@/lib/editorial-selection";
import { listTools, listTopTools } from "@/lib/tools/repository";
import { publicListQuery } from "@/lib/tools/query";
describe("redaktionelle Startauswahl", () => {
  it("verwendet 20 eindeutige, tatsächlich veröffentlichte Einträge des vorhandenen Exports", () => {
    const exported = JSON.parse(fs.readFileSync("data/export/tools.json", "utf8")) as { slug: string; publish_status: string; is_example: number }[];
    expect(new Set(editorialStarterSlugs).size).toBe(20);
    for (const slug of editorialStarterSlugs) expect(exported.some((tool) => tool.slug === slug && tool.publish_status === "published" && !tool.is_example)).toBe(true);
  });
  it("blendet Entwürfe aus, filtert Picks und bevorzugt eine gesetzte Datenbank-Rangliste", async () => {
    const client = createClient({ url: ":memory:" });
    try {
      await applyMigrations(client);
      const db = drizzle(client, { schema });
      for (const [slug, status] of [["chatgpt", "published"], ["claude", "draft"], ["gemini", "published"], ["anderes", "published"]] as const) {
        await db.insert(schema.tools).values({ id: slug, slug, name: slug, domain: "example.com", originalUrl: "https://example.com", shortDescriptionDe: "Test", publishStatus: status, createdAt: new Date(), updatedAt: new Date() });
      }
      expect((await listTopTools(db)).map((tool) => [tool.slug, tool.editorialRank])).toEqual([["chatgpt", 1], ["gemini", 3]]);
      expect((await listTools(db, publicListQuery({ picks: "ja" }, { sort: "featured" }))).items.map((tool) => tool.slug)).toEqual(["chatgpt", "gemini"]);
      await client.execute("update tools set editorial_rank=1 where slug='anderes'");
      expect((await listTopTools(db)).map((tool) => tool.slug)).toEqual(["anderes"]);
      expect((await client.execute("select editorial_rank from tools where slug='chatgpt'")).rows[0].editorial_rank).toBeNull();
    } finally { client.close(); }
  });
});
