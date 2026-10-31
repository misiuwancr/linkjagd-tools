import { readFileSync } from "fs";
import { describe, expect, it } from "vitest";

const catalog = JSON.parse(readFileSync(new URL("../data/verified-tools-batch2.json", import.meta.url), "utf8")) as Array<{
  name: string;
  originalUrl: string;
  domain: string;
  pricingModel: string;
  licenseType: string;
  categorySlugs: string[];
  shortDescriptionDe: string;
  longDescriptionDe: string;
  partnerStatus: string;
  verified: boolean;
  oss: { license?: string; repoUrl?: string } | null;
}>;

const categories = new Set([
  "ki-chatbots",
  "bildgenerierung",
  "videogenerierung",
  "programmierung",
  "produktivitaet",
  "automatisierung",
  "marketing",
  "social-media",
  "recherche",
  "textgenerierung",
  "audio-und-sprache",
  "design",
  "bildung",
  "e-commerce",
]);

const shared = new Set(["github.com", "gitlab.com", "huggingface.co"]);

describe("zweite geprüfte Liste", () => {
  it("enthält mehr als 100 geprüfte Einträge ohne Partnerlink", () => {
    expect(catalog.length).toBeGreaterThanOrEqual(100);
    for (const entry of catalog) {
      expect(entry.verified).toBe(true);
      expect(entry.partnerStatus).toBe("none_found");
      expect(entry.originalUrl.startsWith("https://")).toBe(true);
      expect(entry.shortDescriptionDe.length).toBeGreaterThanOrEqual(10);
      expect(entry.shortDescriptionDe.length).toBeLessThanOrEqual(280);
      expect(entry.longDescriptionDe.toLowerCase()).not.toContain("zzgl");
      expect(JSON.stringify(entry).toLowerCase()).not.toContain("affiliate_url");
      expect(["free", "freemium", "paid"]).toContain(entry.pricingModel);
      expect(["open_source", "proprietary", "unknown"]).toContain(entry.licenseType);
      expect(entry.categorySlugs.length).toBeGreaterThan(0);
      for (const slug of entry.categorySlugs) expect(categories.has(slug)).toBe(true);
      if (entry.licenseType === "open_source") {
        expect(entry.oss?.license).toBeTruthy();
        expect(entry.oss?.repoUrl).toMatch(/^https:\/\//);
      } else {
        expect(entry.oss).toBeNull();
      }
    }
  });

  it("wiederholt keine Domain außer auf gemeinsamen Hosts", () => {
    const seen = new Map<string, string>();
    for (const entry of catalog) {
      if (shared.has(entry.domain)) continue;
      expect(seen.has(entry.domain), entry.domain).toBe(false);
      seen.set(entry.domain, entry.name);
    }
  });
});
