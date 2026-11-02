import { createClient } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import { describe, expect, it } from "vitest";
import * as schema from "@/db/schema";
import { applyMigrations } from "@/db/migrate";
import { listAssignedVideos, parseEditorial, readToolEditorial, saveToolEditorial, toolEditorialSchema } from "@/lib/tool-editorial";
import { getToolBySlug, listHomepageFresh, listTools } from "@/lib/tools/repository";
import { publicListQuery } from "@/lib/tools/query";
import { saveToolRecord, setToolStatus } from "@/lib/tools/mutations";

describe("Redaktionelle Entdeckungsstruktur", () => {
  it("verwirft erfundene Zukunftsdaten, doppelte Kennungen und unsichere Videolinks", () => {
    const video = { id: "lokaler-test", title: "Lokaler Test, kein echtes Video", part: 36, url: "" };
    expect(toolEditorialSchema.safeParse({ videos: [video], publishedAt: "2999-01-01T00:00:00.000Z" }).success).toBe(false);
    expect(toolEditorialSchema.safeParse({ videos: [video, video] }).success).toBe(false);
    expect(toolEditorialSchema.safeParse({ videos: [{ ...video, url: "javascript:alert(1)" }] }).success).toBe(false);
    expect(toolEditorialSchema.safeParse({ videos: [{ ...video, url: "https://127.0.0.1/video" }] }).success).toBe(false);
    expect(toolEditorialSchema.safeParse({ videos: [{ ...video, url: "http://example.com/video" }] }).success).toBe(false);
    expect(parseEditorial("kaputtes JSON")).toEqual({ videos: [], publishedAt: null, hasBeenPublished: false });
  });

  it("ordnet vorhandene Tools ohne Duplikate zu, veröffentlicht Entwürfe korrekt und erhält echte Daten beim Bearbeiten", async () => {
    const client = createClient({ url: ":memory:" });
    try {
      await applyMigrations(client);
      const db = drizzle(client, { schema });
      for (const [id, status] of [["alt", "published"], ["entwurf", "draft"], ["weiterer-entwurf", "draft"]] as const) {
        await db.insert(schema.tools).values({ id, name: id, slug: id, originalUrl: `https://${id}.example`, domain: `${id}.example`, shortDescriptionDe: "Ein klar markiertes Testwerkzeug.", publishStatus: status, createdAt: new Date("2026-01-01"), updatedAt: new Date() });
      }
      const video = { id: "lokaler-test", title: "Lokaler Test, kein echtes Video", part: 36, url: "" };
      await saveToolEditorial(db, "alt", { publishedAt: null, videos: [video] });
      await saveToolEditorial(db, "weiterer-entwurf", { publishedAt: null, videos: [{ ...video, id: "privat" }] });
      expect((await listAssignedVideos(db)).map((item) => item.id)).toEqual(["lokaler-test"]);
      expect((await listTools(db, publicListQuery({ folge: "36", q: "Testwerkzeug" }, { linkjagdOnly: true }))).items.map((tool) => tool.slug)).toEqual(["alt"]);
      expect((await listTools(db, publicListQuery({ "video-id": "lokaler-test" }, { linkjagdOnly: true }))).total).toBe(1);
      expect(await listHomepageFresh(db)).toEqual([]); // Recent edits/imports never manufacture publication dates.
      await setToolStatus(db, "entwurf", "published");
      const published = await readToolEditorial(db, "entwurf");
      expect(published.publishedAt).not.toBeNull();
      expect((await listHomepageFresh(db)).map((tool) => tool.slug)).toEqual(["entwurf"]);
      await setToolStatus(db, "entwurf", "draft");
      await setToolStatus(db, "entwurf", "published");
      expect((await readToolEditorial(db, "entwurf")).publishedAt).toBe(published.publishedAt);
      const raw = { name: "alt", slug: "alt", originalUrl: "https://alt.example", shortDescriptionDe: "Ein klar markiertes Testwerkzeug.", longDescriptionDe: "", featuresDe: [], pricingModel: "free", publishStatus: "published", featured: true, editorialRank: null, isExample: false, categoryIds: [], tags: [] };
      expect((await saveToolRecord(db, raw, { id: "alt", logo: null, screenshots: [] })).ok).toBe(true);
      expect((await getToolBySlug(db, "alt"))?.featured).toBe(true);
      expect((await readToolEditorial(db, "alt")).publishedAt).toBeNull(); // Editing an old published tool isn't publication.
      expect((await readToolEditorial(db, "alt")).videos).toEqual([video]);
      await setToolStatus(db, "alt", "draft");
      await setToolStatus(db, "alt", "published");
      expect((await readToolEditorial(db, "alt")).publishedAt).toBeNull();
      expect((await listTools(db, publicListQuery({}, { manualRecommendationsOnly: true }))).items.map((tool) => tool.slug)).toEqual(["alt"]);
      await saveToolRecord(db, { ...raw, featured: false }, { id: "alt", logo: null, screenshots: [] });
      expect((await listTools(db, publicListQuery({}, { manualRecommendationsOnly: true }))).total).toBe(0);
      expect(Number((await client.execute("select count(*) as count from tools")).rows[0].count)).toBe(3);
    } finally { client.close(); }
  });
});
