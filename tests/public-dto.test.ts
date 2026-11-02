import { describe, expect, it } from "vitest";
import { toPublicTool } from "@/lib/tools/public";
import type { Tool } from "@/db/schema";

describe("öffentliche Tool-Daten", () => {
  it("enthält weder Original-URL noch Affiliate-URL", () => {
    const originalUrl = "https://nordlicht.example/geheim";
    const affiliateUrl = "https://partner.example/r/geheim?ref=test";
    const tool = {
      id: "1",
      name: "Nordlicht Chat",
      slug: "nordlicht-chat",
      originalUrl,
      domain: "nordlicht.example",
      logo: null,
      shortDescriptionDe: "Kurzbeschreibung für das Beispiel.",
      longDescriptionDe: "Lang.",
      featuresDe: "[\"Eine Funktion\"]",
      screenshots: "[]",
      pricingModel: "freemium",
      publishStatus: "published",
      featured: true,
      editorialRank: 1,
      discoverySource: "example",
      isExample: true,
      searchText: "",
      internalNotes: "intern",
      submitterEmail: "person@example.com",
      createdAt: new Date("2026-01-01T00:00:00.000Z"),
      updatedAt: new Date("2026-01-02T00:00:00.000Z"),
    } as Tool;
    const publicTool = toPublicTool({
      ...tool,
      categories: [{ name: "KI-Chatbots", slug: "ki-chatbots" }],
      tags: [],
      programs: [
        {
          id: "p",
          affiliateUrl,
          status: "active",
          isActive: true,
          priority: 1,
        },
      ],
    });
    const serialized = JSON.stringify(publicTool);
    expect(serialized).not.toContain(originalUrl);
    expect(serialized).not.toContain(affiliateUrl);
    expect(serialized).not.toContain("person@example.com");
    expect(serialized).not.toContain("intern");
    expect(publicTool.ctaEnabled).toBe(true);
    expect(publicTool.ctaKind).toBe("affiliate");
    expect(publicTool).not.toHaveProperty("originalUrl");
  });

  it("deaktiviert den Anbieter-CTA ohne Partnerlink", () => {
    const tool = {
      id: "1",
      name: "Fokusplan",
      slug: "fokusplan",
      originalUrl: "https://fokusplan.example/",
      domain: "fokusplan.example",
      logo: null,
      shortDescriptionDe: "Kurzbeschreibung für das Beispiel.",
      longDescriptionDe: "",
      featuresDe: "[]",
      screenshots: "[]",
      pricingModel: "free",
      publishStatus: "published",
      featured: false,
      editorialRank: null,
      discoverySource: "example",
      isExample: true,
      searchText: "",
      internalNotes: null,
      submitterEmail: null,
      createdAt: new Date(),
      updatedAt: new Date(),
    } as Tool;
    const publicTool = toPublicTool({ ...tool, categories: [], tags: [], programs: [] });
    expect(publicTool.ctaEnabled).toBe(false);
    expect(publicTool.ctaKind).toBe("disabled");
  });
});
