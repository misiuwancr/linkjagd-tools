import { readFileSync } from "fs";
import { describe, expect, it } from "vitest";

const catalog = JSON.parse(readFileSync(new URL("../data/verified-tools-batch3.json", import.meta.url), "utf8")) as Array<{
  name: string;
  originalUrl: string;
  domain: string;
  licenseType: string;
  shortDescriptionDe: string;
  longDescriptionDe: string;
  partnerStatus: string;
  programPresence?: string;
  programInfoUrl?: string;
  oss: { license?: string } | null;
}>;

const programs = JSON.parse(readFileSync(new URL("../data/partner-programs.json", import.meta.url), "utf8")) as Array<{
  slug: string;
  network: string;
  programInfoUrl: string;
  affiliateUrl?: string;
}>;

describe("dritte geprüfte Liste", () => {
  it("hat mindestens 100 eigene Texte ohne Partnerlink", () => {
    expect(catalog.length).toBeGreaterThanOrEqual(100);
    const domains = new Set<string>();
    for (const entry of catalog) {
      expect(domains.has(entry.domain)).toBe(false);
      domains.add(entry.domain);
      expect(entry.originalUrl.startsWith("https://")).toBe(true);
      expect(entry.shortDescriptionDe.length).toBeGreaterThanOrEqual(10);
      expect(entry.longDescriptionDe.toLowerCase()).not.toContain("zzgl");
      expect(JSON.stringify(entry)).not.toContain("affiliateUrl");
      if (entry.programPresence === "yes") {
        expect(entry.programInfoUrl?.startsWith("https://")).toBe(true);
        expect(entry.partnerStatus).toBe("found");
      }
      if (entry.licenseType === "open_source") expect(entry.oss?.license).toBeTruthy();
    }
  });

  it("speichert Programmseiten nicht als Affiliate-Link", () => {
    expect(programs.length).toBeGreaterThan(20);
    for (const page of programs) {
      expect(page.programInfoUrl.startsWith("https://")).toBe(true);
      expect(page.affiliateUrl).toBeUndefined();
      expect(["direct", "partnerstack", "impact", "awin"]).toContain(page.network);
    }
  });
});
