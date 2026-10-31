import { createClient } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import { describe, expect, it } from "vitest";
import * as schema from "@/db/schema";
import { tools } from "@/db/schema";
import { applyMigrations } from "@/db/migrate";
import {
  COMPANY_STRIP_LABEL,
  companiesForTools,
  companyBySlug,
  toolMatchesCompany,
} from "@/lib/companies";
import { directoryHref, publicListQuery } from "@/lib/tools/query";
import { listCompaniesInDirectory, listTools } from "@/lib/tools/repository";

describe("Firmenleiste", () => {
  it("nennt das Verzeichnis und keine Leserschaft", () => {
    expect(COMPANY_STRIP_LABEL).toBe("Tools von diesen Firmen im Verzeichnis");
    expect(COMPANY_STRIP_LABEL.toLowerCase()).not.toContain("leser");
  });

  it("zählt nur eigene Hosts und blendet leere Firmen aus", () => {
    const google = companyBySlug("google");
    const meta = companyBySlug("meta");
    const github = companyBySlug("github");
    const apple = companyBySlug("apple");
    const microsoft = companyBySlug("microsoft");
    if (!google || !meta || !github || !apple || !microsoft) throw new Error("Regeln fehlen");

    expect(toolMatchesCompany(google, { slug: "gemini", domain: "gemini.google.com" })).toBe(true);
    expect(toolMatchesCompany(google, { slug: "chatgpt-file-uploader", domain: "chromewebstore.google.com" })).toBe(false);
    expect(toolMatchesCompany(meta, { slug: "animated-drawings", domain: "sketch.metademolab.com" })).toBe(true);
    expect(toolMatchesCompany(meta, { slug: "metabase", domain: "metabase.com" })).toBe(false);
    expect(toolMatchesCompany(github, { slug: "github-copilot", domain: "github.com" })).toBe(true);
    expect(toolMatchesCompany(github, { slug: "comfyui", domain: "github.com" })).toBe(false);
    expect(toolMatchesCompany(apple, { slug: "motionleap", domain: "apps.apple.com" })).toBe(false);
    expect(toolMatchesCompany(microsoft, { slug: "copilot-money", domain: "copilot.money" })).toBe(false);

    const shown = companiesForTools([
      { slug: "gemini", domain: "gemini.google.com" },
      { slug: "chatgpt-file-uploader", domain: "chromewebstore.google.com" },
      { slug: "comfyui", domain: "github.com" },
      { slug: "motionleap", domain: "apps.apple.com" },
    ]);
    expect(shown.map((company) => company.slug)).toEqual(["google"]);
    expect(shown[0]?.href).toBe("/tools?firma=google");
    expect(shown[0]?.markPath).toBeTruthy();
  });

  it("hängt den Firmenfilter an teilbare URLs", () => {
    const query = publicListQuery({ firma: "openai", seite: "2" });
    expect(query.company).toBe("openai");
    expect(directoryHref("/tools", query)).toBe("/tools?firma=openai&seite=2");
    expect(publicListQuery({ firma: "../admin" }).company).toBe("");
  });

  it("filtert veröffentlichte Tools der Firma und lässt Beispiele weg", async () => {
    const client = createClient({ url: ":memory:" });
    await applyMigrations(client);
    const db = drizzle(client, { schema });
    const now = new Date();
    const rows = [
      ["gemini", "Gemini", "gemini.google.com", "published", false],
      ["chatgpt-file-uploader", "ChatGPT File Uploader", "chromewebstore.google.com", "published", false],
      ["google-beispiel", "Google Beispiel", "gemini.google.com", "published", true],
      ["comfyui", "ComfyUI", "github.com", "published", false],
      ["google-entwurf", "Google Entwurf", "aistudio.google.com", "draft", false],
    ] as const;
    for (const [slug, name, domain, status, example] of rows) {
      await db.insert(tools).values({
        id: slug,
        name,
        slug,
        originalUrl: `https://${domain}/`,
        domain,
        shortDescriptionDe: "Kurzbeschreibung für den Test der Firmenleiste.",
        longDescriptionDe: "",
        featuresDe: "[]",
        screenshots: "[]",
        pricingModel: "freemium",
        publishStatus: status,
        featured: false,
        discoverySource: "test",
        isExample: example,
        searchText: slug,
        createdAt: now,
        updatedAt: now,
      });
    }
    const listed = await listTools(db, publicListQuery({ firma: "google" }));
    expect(listed.items.map((tool) => tool.slug)).toEqual(["gemini"]);
    const companies = await listCompaniesInDirectory(db);
    expect(companies.map((company) => company.name)).toEqual(["Google"]);
  });
});
