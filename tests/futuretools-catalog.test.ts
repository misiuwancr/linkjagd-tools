import { describe, expect, it } from "vitest";
import { createClient } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import { eq } from "drizzle-orm";
import * as schema from "@/db/schema";
import { categories } from "@/db/schema";
import { applyMigrations } from "@/db/migrate";
import { importDiscoveredTool } from "@/lib/import/service";
import { decideRedirect } from "@/lib/affiliate/redirect";
import { getToolBySlug } from "@/lib/tools/repository";
import catalog from "@/data/futuretools-top100.json";

describe("FutureTools-Top-100-Katalog", () => {
  it("enthält 100 eindeutige Entwurfsdatensätze ohne Tracking-Links", () => {
    expect(catalog).toHaveLength(100);
    expect(new Set(catalog.map((item) => item.domain)).size).toBe(100);
    expect(new Set(catalog.map((item) => item.rank)).size).toBe(100);
    for (const item of catalog) {
      expect(item.discoverySource).toBe("futuretools-top100");
      expect(item.originalUrl).not.toMatch(/futuretools\.|ref=|via=matt|\?via=/i);
      expect(item.shortDescriptionDe.length).toBeGreaterThanOrEqual(10);
      expect(item.longDescriptionDe).not.toMatch(/futuretools\.io\/tools\//i);
      expect(["ja", "nein", "unklar"]).toContain(item.partner);
      expect(item.partner === "ja" ? item.programUrl.startsWith("https://") : item.programUrl).toBe(
        item.partner === "ja" ? true : "",
      );
      expect(item).not.toHaveProperty("affiliateUrl");
    }
  });

  it("legt einen Katalogeintrag als Entwurf ohne Weiterleitung an", async () => {
    const client = createClient({ url: ":memory:" });
    await applyMigrations(client);
    const database = drizzle(client, { schema });
    const now = new Date();
    await database.insert(categories).values({
      id: "videogenerierung",
      name: "Videogenerierung",
      slug: "videogenerierung",
      description: "",
      sortOrder: 1,
      createdAt: now,
      updatedAt: now,
    });
    const entry = catalog[0];
    const imported = await importDiscoveredTool(database, {
      name: entry.name,
      originalUrl: entry.originalUrl,
      shortDescriptionDe: entry.shortDescriptionDe,
      longDescriptionDe: entry.longDescriptionDe,
      pricingModel: entry.pricingModel,
      categorySlugs: entry.categorySlugs,
      tags: ["Top-100"],
      discoverySource: entry.discoverySource,
    });
    expect(imported.ok).toBe(true);
    if (!imported.ok) return;
    const tool = await getToolBySlug(database, imported.slug);
    expect(tool?.publishStatus).toBe("draft");
    expect(decideRedirect(tool, []).ok).toBe(false);
    const published = { ...tool!, publishStatus: "published" as const };
    const decision = decideRedirect(published, []);
    expect(decision.ok).toBe(true);
    if (decision.ok) expect(decision.kind).toBe("official");
    expect(tool?.originalUrl).toBe(entry.originalUrl);
    const again = await importDiscoveredTool(database, {
      name: `${entry.name} Kopie`,
      originalUrl: entry.originalUrl,
      shortDescriptionDe: entry.shortDescriptionDe,
      longDescriptionDe: "",
      pricingModel: entry.pricingModel,
      categorySlugs: [],
      tags: [],
      discoverySource: "futuretools-top100",
    });
    expect(again.ok).toBe(false);
    if (!again.ok) expect(again.status).toBe(409);
    const stored = await database.select().from(schema.tools).where(eq(schema.tools.slug, imported.slug));
    expect(stored).toHaveLength(1);
  });
});
