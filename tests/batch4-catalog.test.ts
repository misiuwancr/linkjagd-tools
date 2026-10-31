import { readFileSync } from "fs";
import { describe, expect, it } from "vitest";

const catalog = JSON.parse(readFileSync(new URL("../data/verified-tools-batch4.json", import.meta.url), "utf8")) as Array<{
  name: string;
  originalUrl: string;
  domain: string;
  licenseType: string;
  shortDescriptionDe: string;
  longDescriptionDe: string;
  programPresence?: string;
  programInfoUrl?: string;
  oss: { license?: string } | null;
}>;

describe("vierte geprüfte Liste", () => {
  it("enthält eigene deutsche Texte ohne gespeicherten Affiliate-Link", () => {
    expect(catalog.length).toBeGreaterThanOrEqual(50);
    const domains = new Set<string>();
    for (const entry of catalog) {
      expect(domains.has(entry.domain)).toBe(false);
      domains.add(entry.domain);
      expect(entry.originalUrl.startsWith("https://")).toBe(true);
      expect(entry.longDescriptionDe.toLowerCase()).not.toContain("zzgl");
      expect(JSON.stringify(entry)).not.toContain("affiliateUrl");
      if (entry.programPresence === "yes") expect(entry.programInfoUrl?.startsWith("https://")).toBe(true);
      if (entry.licenseType === "open_source") expect(entry.oss?.license).toBeTruthy();
    }
  });
});
