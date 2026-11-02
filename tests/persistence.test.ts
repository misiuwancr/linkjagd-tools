import fs from "fs";
import os from "os";
import path from "path";
import { createClient } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import { eq } from "drizzle-orm";
import { describe, expect, it } from "vitest";
import * as schema from "@/db/schema";
import { affiliatePrograms, categories, toolCategories, tools } from "@/db/schema";
import { applyMigrations } from "@/db/migrate";

function removeTemporaryDatabase(file: string) {
  try { fs.rmSync(file, { force: true }); }
  catch (error) {
    // libSQL kann unter Windows native Statements bis zum Prozessende halten.
    // Nur die Aufräumphase toleriert diesen Fall; alle Datenprüfungen bleiben strikt.
    if (process.platform !== "win32" || !["EBUSY", "EPERM"].includes((error as NodeJS.ErrnoException).code || "")) throw error;
  }
}

describe("Persistenz auf einer Datei-Kopie", () => {
  it("behält Tool, Kategorie und Partnerlink über einen neuen Verbindungsaufbau", async () => {
    const file = path.join(os.tmpdir(), `linkjagd-persist-${Date.now()}.db`);
    const clients: ReturnType<typeof createClient>[] = [];
    const open = async () => {
      const client = createClient({ url: `file:${file}` });
      clients.push(client);
      await applyMigrations(client);
      return drizzle(client, { schema });
    };
    const db = await open();
    const now = new Date();
    await db.insert(categories).values({
      id: "chat",
      name: "Chat",
      slug: "chat-assistenten",
      description: "Chat",
      sortOrder: 1,
      createdAt: now,
      updatedAt: now,
    });
    await db.insert(tools).values({
      id: "t1",
      name: "Probe",
      slug: "probe",
      originalUrl: "https://probe.example/",
      domain: "probe.example",
      shortDescriptionDe: "Ein Testwerkzeug mit einer ausreichend langen deutschen Beschreibung für die Prüfung.",
      longDescriptionDe: "",
      featuresDe: "[]",
      screenshots: "[]",
      pricingModel: "freemium",
      publishStatus: "published",
      featured: false,
      discoverySource: "test",
      isExample: false,
      searchText: "probe",
      createdAt: now,
      updatedAt: now,
    });
    await db.insert(toolCategories).values({ toolId: "t1", categoryId: "chat" });
    await db.insert(affiliatePrograms).values({
      id: "p1",
      toolId: "t1",
      affiliateUrl: "https://partner.example/probe",
      network: "manual",
      status: "active",
      priority: 1,
      isActive: true,
      createdAt: now,
      updatedAt: now,
    });
    await db.update(tools).set({ name: "Probe geändert" }).where(eq(tools.id, "t1"));

    const again = await open();
    const tool = await again.select().from(tools).where(eq(tools.slug, "probe")).limit(1);
    const link = await again.select().from(affiliatePrograms).where(eq(affiliatePrograms.toolId, "t1"));
    const category = await again.select().from(toolCategories).where(eq(toolCategories.toolId, "t1"));
    expect(tool[0]?.name).toBe("Probe geändert");
    expect(link[0]?.affiliateUrl).toBe("https://partner.example/probe");
    expect(category[0]?.categoryId).toBe("chat");
    clients.forEach((client) => client.close());
    removeTemporaryDatabase(file);
  });

  it("legt allow_index an und führt die Datei kein zweites Mal aus", async () => {
    const file = path.join(os.tmpdir(), `linkjagd-migrate-${Date.now()}.db`);
    const client = createClient({ url: `file:${file}` });
    await applyMigrations(client);
    const now = Date.now();
    await client.execute({
      sql: `insert into tools (id, name, slug, original_url, domain, short_description_de, created_at, updated_at, publish_status)
            values ('t1', 'Probe', 'probe', 'https://probe.example/', 'probe.example', 'Beschreibung lang genug für den Test der Migration.', ?, ?, 'published')`,
      args: [now, now],
    });
    const before = await client.execute("select count(*) as n from tools");
    const marked = await client.execute("select count(*) as n from schema_migrations where id = '0007_allow_index.sql'");
    await applyMigrations(client);
    const after = await client.execute("select count(*) as n from tools");
    const markedAgain = await client.execute("select count(*) as n from schema_migrations where id = '0007_allow_index.sql'");
    const column = await client.execute("select allow_index as allow_index from tools where id = 't1'");
    expect(Number(before.rows[0]?.n)).toBe(1);
    expect(Number(after.rows[0]?.n)).toBe(1);
    expect(Number(marked.rows[0]?.n)).toBe(1);
    expect(Number(markedAgain.rows[0]?.n)).toBe(1);
    expect(Number(column.rows[0]?.allow_index)).toBe(1);
    client.close();
    removeTemporaryDatabase(file);
  });
});
