import { createClient } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import { expect, it } from "vitest";
import os from "node:os";
import path from "node:path";
import * as schema from "@/db/schema";
import { applyMigrations } from "@/db/migrate";
import { importBatchCandidate } from "@/lib/import/batch";

const candidate = {
  name: "Neues Werkzeug", originalUrl: "https://official.example/", shortDescriptionDe: "Ein Werkzeug zum Bearbeiten eigener Texte.",
  pricingModel: "free", categorySlugs: ["produktivitaet"], discoverySource: "official-research",
  evidence: { officialUrl: "https://official.example/", checkedAt: new Date().toISOString(), httpStatus: 200,
    productFacts: "Der Anbieter beschreibt die Bearbeitung eigener Texte.", pricingSource: "https://official.example/pricing", pricingFacts: "Kostenloser Zugang laut Anbieter.", reviewed: true },
};
it("prüft ohne Schreiben, importiert atomar und überspringt vorhandene Einträge beim Wiederaufnehmen", async () => {
  const client = createClient({ url: `file:${path.join(os.tmpdir(), `linkjagd-batch-${crypto.randomUUID()}.db`).replaceAll("\\", "/")}` });
  try {
    await applyMigrations(client); const db = drizzle(client, { schema });
    await db.insert(schema.categories).values({ id: "cat", slug: "produktivitaet", name: "Produktivität", createdAt: new Date(), updatedAt: new Date() });
    expect((await importBatchCandidate(db, candidate)).status).toBe("ready");
    expect(await db.select().from(schema.tools)).toHaveLength(0);
    expect((await importBatchCandidate(db, candidate, true, false)).status).toBe("published");
    const before = await db.select().from(schema.tools);
    expect((await importBatchCandidate(db, { ...candidate, shortDescriptionDe: "Dieser Text darf nichts überschreiben." }, true, false)).status).toBe("duplicate");
    expect(await db.select().from(schema.tools)).toEqual(before);
    expect((await importBatchCandidate(db, { ...candidate, name: "Andere", originalUrl: "https://other.example" })).status).toBe("invalid");
    expect((await importBatchCandidate(db, { ...candidate, name: "Neue Kategorie", originalUrl: "https://fresh.example", evidence: { ...candidate.evidence, officialUrl: "https://fresh.example" }, categorySlugs: ["unbekannt"] })).status).toBe("invalid");
    expect((await importBatchCandidate(db, { ...candidate, evidence: { ...candidate.evidence, reviewed: false } })).status).toBe("invalid");
  } finally { client.close(); }
});
