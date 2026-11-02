import { createClient } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import { describe, expect, it, vi } from "vitest";
import * as schema from "@/db/schema";
import { applyMigrations } from "@/db/migrate";
import { clickContext, contextClickStats, goHref } from "@/lib/affiliate/context";
import { handleGoRedirect } from "@/lib/affiliate/go";
import { recordClick, listClickStats } from "@/lib/tools/repository";
import { saveNewsRecord } from "@/lib/tools/mutations";
import { contentArticles, relatedArticles } from "@/lib/content-hub";
import { renderMarkdown } from "@/lib/markdown";
import { directoryHref, publicListQuery } from "@/lib/tools/query";

// React.cache is supplied by Next's server renderer; this suite exercises the
// repository functions directly, outside a server-component render request.
vi.mock("react", async (original) => ({ ...await original<object>(), cache: (fn: unknown) => fn }));

describe("Affiliate-Messung und Content-Hub", () => {
  it("verändert das gespeicherte Ziel nicht und zählt HEAD/Vorabrufe nicht", async () => {
    const track = vi.fn(async () => undefined);
    const deps = { load: async () => ({ tool: { id: "tool", originalUrl: "https://official.example/path", publishStatus: "published" as const }, programs: [{ id: "program", affiliateUrl: "https://partner.example/stored?ref=test", status: "active" as const, isActive: true, priority: 1 }] }), track, context: { source: "/linkjagd", position: "card" as const } };
    expect(await handleGoRedirect("tool", { ...deps, skipTracking: true })).toEqual({ status: 302, location: "https://partner.example/stored?ref=test" });
    expect(track).not.toHaveBeenCalled();
    expect(await handleGoRedirect("tool", { ...deps, officialOnly: true })).toEqual({ status: 302, location: "https://official.example/path" });
    expect(track).toHaveBeenCalledWith(expect.objectContaining({ kind: "official", programId: null, source: "/linkjagd", position: "card" }));
    expect(goHref("tool", "/blog/ratgeber", "article")).not.toContain("destination");
  });

  it("zählt atomar und vervielfacht Summen bei mehreren Partnerprogrammen nicht", async () => {
    const client = createClient({ url: ":memory:" });
    try {
      await applyMigrations(client); const db = drizzle(client, { schema });
      await db.insert(schema.tools).values({ id: "tool", slug: "tool", name: "Testtool", originalUrl: "https://official.example", domain: "official.example", shortDescriptionDe: "Nur ein lokaler Test.", publishStatus: "published", createdAt: new Date(), updatedAt: new Date() });
      await db.insert(schema.affiliatePrograms).values([{ id: "p1", toolId: "tool", createdAt: new Date(), updatedAt: new Date() }, { id: "p2", toolId: "tool", createdAt: new Date(), updatedAt: new Date() }]);
      expect(await clickContext(db, "/tools?email=privat@example.test", "private@example.test")).toEqual({ source: "unbekannt", position: "unknown" });
      expect(await clickContext(db, "/tools/tool", "hero")).toEqual({ source: "/tools/tool", position: "hero" });
      expect(await clickContext(db, "/blog/nicht-vorhanden", "article")).toEqual({ source: "unbekannt", position: "article" });
      const event = { toolId: "tool", kind: "official" as const, programId: null, day: "2026-11-02", source: "/linkjagd", position: "card" as const };
      await Promise.all(Array.from({ length: 8 }, () => recordClick(db, event)));
      expect((await listClickStats(db, "2026-10-27", "2026-10-03"))[0].days7).toBe(8);
      expect(await contextClickStats(db, "2026-10-27")).toEqual([{ source: "/linkjagd", position: "card", count: 8, official: 8, affiliate: 0 }]);
      const raw = (await client.execute("select value from site_settings where key like 'click_context:%'")).rows[0].value as string;
      expect(Object.keys(JSON.parse(raw)).sort()).toEqual(["count", "day", "kind", "position", "programId", "source", "toolId"].sort());
      expect(raw).not.toMatch(/email|ip_address|user_agent|cookie|referrer/);
    } finally { client.close(); }
  });

  it("erhält Artikel, Datierung und Vergleichs-URLs und verknüpft nur vorhandene Tools", async () => {
    const client = createClient({ url: ":memory:" });
    try {
      await applyMigrations(client); const db = drizzle(client, { schema });
      await db.insert(schema.tools).values({ id: "tool", slug: "tool", name: "Testtool", originalUrl: "https://official.example", domain: "official.example", shortDescriptionDe: "Nur ein lokaler Test.", publishStatus: "published", createdAt: new Date(), updatedAt: new Date() });
      const input = { title: "Lokaler Ratgeber", slug: "lokaler-ratgeber", excerpt: "Ein ausdrücklich lokaler Testartikel.", body: "[Tool](/tools/tool) und [Anbieter](/go/tool)", status: "published", editorial: { topic: "entdecken", toolSlugs: ["tool"], relatedSlugs: [] } };
      const saved = await saveNewsRecord(db, input); expect(saved.ok).toBe(true); if (!saved.ok) throw new Error(saved.error);
      const first = (await db.select().from(schema.newsPosts))[0];
      await saveNewsRecord(db, { ...input, id: saved.id, title: "Überarbeiteter lokaler Ratgeber" });
      expect((await db.select().from(schema.newsPosts))[0].publishedAt).toEqual(first.publishedAt);
      const bad = await saveNewsRecord(db, { ...input, slug: "falsches-tool", editorial: { ...input.editorial, toolSlugs: ["erfunden"] } }); expect(bad.ok).toBe(false);
      expect((await saveNewsRecord(db, { ...input, slug: "zapier-make-n8n-vergleich" })).ok).toBe(false);
      await saveNewsRecord(db, { ...input, slug: "entwurf", status: "draft" });
      const all = await contentArticles(db);
      expect(all.filter((post) => post.slug === "zapier-make-n8n-vergleich")).toHaveLength(1);
      expect(all.some((post) => post.slug === "entwurf")).toBe(false);
      expect(all.find((post) => post.slug === input.slug)?.toolSlugs).toEqual(["tool"]);
      expect(relatedArticles(all.find((post) => post.slug === "shopify-vs-woocommerce")!, all).some((post) => post.slug === "shopify-vs-woocommerce")).toBe(false);
      expect(directoryHref("/blog", publicListQuery({ thema: "news", seite: "2" }))).toBe("/blog?thema=news&seite=2");
    } finally { client.close(); }
  });

  it("kennzeichnet nur tatsächliche Partnerlinks und lässt kein HTML oder fremde Weiterleitungsziele einfließen", () => {
    const html = renderMarkdown('[Tool](/tools/tool) [Anbieter](/go/tool?url=https://evil.example) <script>bad</script> [Böse](javascript:alert(1)) [Extern](//evil.example)', { outbound: { tool: { href: goHref("tool", "/blog/ratgeber", "article"), affiliate: true } } });
    expect(html).toContain('href="/tools/tool"'); expect(html).toContain("sponsored nofollow"); expect(html).toContain("Anzeige");
    expect(html).not.toContain("<script>"); expect(html).not.toContain('href="//evil'); expect(html).not.toContain('href="javascript'); expect(html).not.toContain('href="/go/tool?url=');
    expect(renderMarkdown('[Anbieter](/go/tool)', { outbound: { tool: { href: "/go/tool", affiliate: false } } })).not.toContain("Anzeige");
    expect(renderMarkdown('[Unbekannt](/go/erfunden)')).not.toContain("href");
  });
});
