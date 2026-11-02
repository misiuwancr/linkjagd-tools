import { createClient } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import { describe, expect, it } from "vitest";
import * as schema from "@/db/schema";
import { applyMigrations } from "@/db/migrate";
import { directoryHref, publicListQuery } from "@/lib/tools/query";
import { buildSearchText, listTools } from "@/lib/tools/repository";

describe("Kombinierbares Verzeichnis", () => {
  it("erhält mehrere Kategorien, alle Filter und Seiten in teilbaren URLs", () => {
    const query = publicListQuery({ q: "Bilder bearbeiten", kategorie: ["design", "gaming", "design", "../admin"], preis: "kostenlos", lizenz: "open-source", sort: "alphabetisch", seite: "3", firma: "google" });
    const href = directoryHref("/tools", query);
    const params = new URL(href, "https://example.test").searchParams;
    expect(params.getAll("kategorie")).toEqual(["design", "gaming"]);
    expect(publicListQuery(Object.fromEntries([...params.keys()].map((key) => [key, params.getAll(key)])))).toEqual(query);
    const removed = new URL(directoryHref("/tools", query, { categorySlugs: ["gaming"], page: 1 }), "https://example.test");
    expect(removed.searchParams.getAll("kategorie")).toEqual(["gaming"]);
    expect(removed.searchParams.get("q")).toBe("Bilder bearbeiten");
    expect(removed.searchParams.has("seite")).toBe(false);
    expect(publicListQuery({ kategorie: ["design", "gaming"] }, { categorySlug: "produktivitaet" }).categorySlugs).toEqual(["produktivitaet"]);
  });

  it("sucht Aufgaben wortweise trotz altem Kurzindex und kombiniert Kategorien als ODER mit Preis/Lizenz als UND", async () => {
    const client = createClient({ url: ":memory:" });
    try {
      await applyMigrations(client);
      const db = drizzle(client, { schema });
      const now = new Date();
      await db.insert(schema.categories).values(["design", "gaming"].map((slug) => ({ id: slug, slug, name: slug, createdAt: now, updatedAt: now })));
      await db.insert(schema.tools).values([
        { id: "a", name: "Atelier", slug: "atelier", originalUrl: "https://atelier.example", domain: "atelier.example", shortDescriptionDe: "Eine kreative Anwendung", longDescriptionDe: "x".repeat(150) + " Bilder lassen sich damit bearbeiten und teilen.", searchText: "atelier kurz", pricingModel: "free" as const, licenseType: "open_source" as const },
        { id: "b", name: "Browser-Spiel", slug: "spiel", originalUrl: "https://spiel.example", domain: "spiel.example", shortDescriptionDe: "Bilder bearbeiten und spielen", longDescriptionDe: "", searchText: "spiel", pricingModel: "free" as const, licenseType: "proprietary" as const },
        { id: "c", name: "Studio", slug: "studio", originalUrl: "https://studio.example", domain: "studio.example", shortDescriptionDe: "Bilder bearbeiten", longDescriptionDe: "", searchText: "studio", pricingModel: "paid" as const, licenseType: "open_source" as const },
      ].map((tool) => ({ ...tool, publishStatus: "published" as const, isExample: false, featuresDe: "[]", screenshots: "[]", createdAt: now, updatedAt: now })));
      await db.insert(schema.toolCategories).values([{ toolId: "a", categoryId: "design" }, { toolId: "a", categoryId: "gaming" }, { toolId: "b", categoryId: "gaming" }, { toolId: "c", categoryId: "design" }]);
      const result = await listTools(db, publicListQuery({ q: "bearbeiten Bilder", kategorie: ["design", "gaming"], preis: "kostenlos", lizenz: "open-source" }));
      expect(result.total).toBe(1);
      expect(result.items.map((tool) => tool.slug)).toEqual(["atelier"]);
      const all = await listTools(db, publicListQuery({ kategorie: ["design", "gaming"] }));
      expect(all.total).toBe(3);
      await db.update(schema.tools).set({ createdAt: new Date("2020-01-01T00:00:00Z") }).where((await import("drizzle-orm")).eq(schema.tools.id, "c"));
      const oldestQuery = publicListQuery({ sort: "aelteste", kategorie: ["design", "gaming"] });
      expect((await listTools(db, oldestQuery)).items[0].id).toBe("c");
      expect(directoryHref("/tools", oldestQuery)).toContain("sort=aelteste"); // Multiple category membership never duplicates a card.
      expect((await listTools(db, publicListQuery({ q: "unauffindbar" }))).total).toBe(0);
      const first = await listTools(db, publicListQuery({}, { pageSize: 2 }));
      const second = await listTools(db, publicListQuery({ seite: "2" }, { pageSize: 2 }));
      expect(new Set([...first.items, ...second.items].map((tool) => tool.id)).size).toBe(3);
      expect((await listTools(db, publicListQuery({ seite: "999" }, { pageSize: 2 }))).page).toBe(2);
      expect(buildSearchText({ name: "Atelier", shortDescriptionDe: "x".repeat(150), longDescriptionDe: "Bilder bearbeiten", categories: [], tags: ["Kreativität"] })).toContain("bilder bearbeiten");
    } finally { client.close(); }
  });
});
