import { readFileSync } from "fs";
import { describe, expect, it } from "vitest";

const catalog = JSON.parse(readFileSync(new URL("../data/verified-tools-batch11.json", import.meta.url), "utf8")) as Array<{
  originalUrl: string;
  domain: string;
  licenseType: string;
  longDescriptionDe: string;
  oss: { license?: string } | null;
}>;

describe("elfte geprüfte Liste", () => {
  it("enthält eigene deutsche Texte ohne gespeicherten Affiliate-Link", () => {
    expect(catalog.length).toBeGreaterThanOrEqual(50);
    const domains = new Set<string>();
    for (const entry of catalog) {
      expect(domains.has(entry.domain)).toBe(false);
      domains.add(entry.domain);
      expect(entry.originalUrl.startsWith("https://")).toBe(true);
      expect(entry.longDescriptionDe.toLowerCase()).not.toContain("zzgl");
      expect(JSON.stringify(entry)).not.toContain("affiliateUrl");
      if (entry.licenseType === "open_source") expect(entry.oss?.license).toBeTruthy();
    }
  });
});
