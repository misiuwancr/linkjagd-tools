import { createClient } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import { describe, expect, it } from "vitest";
import * as schema from "@/db/schema";
import { eq } from "drizzle-orm";
import { tools } from "@/db/schema";
import { applyMigrations } from "@/db/migrate";
import { importDiscoveredTool } from "@/lib/import/service";
import { publicListQuery } from "@/lib/tools/query";
import { listTools, recordClick } from "@/lib/tools/repository";
import { saveAffiliateRecord } from "@/lib/tools/mutations";
import { decideRedirect } from "@/lib/affiliate/redirect";

async function database() {
  const client = createClient({ url: ":memory:" });
  await applyMigrations(client);
  return drizzle(client, { schema });
}

describe("Datenbankfilter und Import", () => {
  it("filtert veröffentlichte Tools nach Text, Kategorie und Preis", async () => {
    const db = await database();
    const now = new Date();
    await db.insert(schema.categories).values({
      id: "ki-chatbots",
      name: "KI-Chatbots",
      slug: "ki-chatbots",
      description: "Chat",
      sortOrder: 1,
      createdAt: now,
      updatedAt: now,
    });
    await db.insert(schema.categories).values({
      id: "design",
      name: "Design",
      slug: "design",
      description: "Design",
      sortOrder: 2,
      createdAt: now,
      updatedAt: now,
    });
    const imported = await importDiscoveredTool(db, {
      name: "Nordlicht Chat",
      originalUrl: "https://nordlicht.example/",
      shortDescriptionDe: "Ein Chat für den Alltag und kurze Fragen.",
      categorySlugs: ["ki-chatbots"],
      tags: ["Gespräch"],
      discoverySource: "import",
      pricingModel: "free",
    });
    expect(imported.ok).toBe(true);
    await db.update(tools).set({ publishStatus: "published" }).where(eq(tools.slug, "nordlicht-chat"));

    const again = await importDiscoveredTool(db, {
      name: "Anderes Werkzeug",
      originalUrl: "https://nordlicht.example/anders",
      shortDescriptionDe: "Dieselbe Domain darf kein zweites Tool werden.",
      discoverySource: "import",
    });
    expect(again.ok).toBe(false);
    if (!again.ok) expect(again.status).toBe(409);

    const byText = await listTools(db, publicListQuery({ q: "Alltag" }));
    expect(byText.total).toBe(1);
    expect(byText.items[0]?.slug).toBe("nordlicht-chat");

    const byCategory = await listTools(db, publicListQuery({ kategorie: "design" }));
    expect(byCategory.total).toBe(0);

    const byPrice = await listTools(db, publicListQuery({ preis: "kostenlos" }));
    expect(byPrice.total).toBe(1);
    const otherPrice = await listTools(db, publicListQuery({ preis: "kostenpflichtig" }));
    expect(otherPrice.total).toBe(0);

    const drafts = await listTools(db, { ...publicListQuery({}), status: "draft" });
    expect(drafts.total).toBe(0);
  });

  it("speichert einen Test-Partnerlink und leitet nicht auf die Original-URL", async () => {
    const db = await database();
    const now = new Date();
    await db.insert(tools).values({
      id: "t1",
      name: "Testwerkzeug",
      slug: "testwerkzeug",
      originalUrl: "https://testwerkzeug.example/",
      domain: "testwerkzeug.example",
      shortDescriptionDe: "Nur für den Test gedacht und klar markiert.",
      longDescriptionDe: "",
      featuresDe: "[]",
      screenshots: "[]",
      pricingModel: "freemium",
      publishStatus: "published",
      featured: false,
      discoverySource: "test",
      isExample: false,
      searchText: "testwerkzeug",
      createdAt: now,
      updatedAt: now,
    });
    const saved = await saveAffiliateRecord(db, "t1", {
      affiliateUrl: "https://example.com/affiliate/testwerkzeug?ref=test",
      network: "manual",
      partnerProgramId: "test-only",
      status: "active",
      priority: 2,
      isActive: true,
      notes: "Testfixture, keine echte Partnerschaft.",
    });
    expect(saved.ok).toBe(true);
    const blocked = await saveAffiliateRecord(db, "t1", {
      affiliateUrl: "https://testwerkzeug.example/",
      network: "manual",
      status: "active",
      priority: 1,
      isActive: true,
    });
    expect(blocked.ok).toBe(false);

    await db.insert(tools).values({
      id: "example-hidden",
      name: "Verstecktes Beispiel",
      slug: "verstecktes-beispiel",
      originalUrl: "https://verstecktes-beispiel.example/",
      domain: "verstecktes-beispiel.example",
      shortDescriptionDe: "Ein Beispieldatensatz, der öffentlich nicht mitgezählt wird.",
      longDescriptionDe: "",
      featuresDe: "[]",
      screenshots: "[]",
      pricingModel: "free",
      publishStatus: "published",
      featured: true,
      editorialRank: 1,
      discoverySource: "example",
      isExample: true,
      searchText: "verstecktes beispiel",
      createdAt: now,
      updatedAt: now,
    });

    const loaded = await listTools(db, publicListQuery({}));
    expect(loaded.items.some((item) => item.isExample)).toBe(false);
    const decision = decideRedirect(loaded.items[0], loaded.items[0].programs);
    expect(decision.ok).toBe(true);
    if (decision.ok) {
      expect(decision.location).toContain("example.com/affiliate/testwerkzeug");
      expect(decision.location).not.toContain("testwerkzeug.example");
      await recordClick(db, { toolId: decision.toolId, programId: decision.programId, kind: "affiliate", day: "2026-10-31" });
      await recordClick(db, { toolId: decision.toolId, programId: decision.programId, kind: "affiliate", day: "2026-10-31" });
    }
    const popular = await listTools(db, publicListQuery({ sort: "beliebteste" }));
    expect(popular.items[0]?.slug).toBe("testwerkzeug");
  });
});
