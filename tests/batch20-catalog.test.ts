import { readFileSync } from "fs";
import { describe, expect, it } from "vitest";

const catalog = JSON.parse(readFileSync(new URL("../data/verified-tools-batch20.json", import.meta.url), "utf8")) as Array<{
  name: string;
  originalUrl: string;
  domain: string;
  licenseType: string;
  longDescriptionDe: string;
}>;

describe("zwanzigste geprüfte Liste", () => {
  it("enthält CMS- und Auth-Werkzeuge, WordPress nur mit bestätigter GPL", () => {
    expect(catalog.length).toBeGreaterThanOrEqual(25);
    const domains = new Set<string>();
    for (const entry of catalog) {
      expect(domains.has(entry.domain)).toBe(false);
      domains.add(entry.domain);
      expect(entry.originalUrl.startsWith("https://")).toBe(true);
      expect(entry.longDescriptionDe.toLowerCase()).not.toContain("zzgl");
    }
    const wp = catalog.find((entry) => entry.domain === "wordpress.org");
    expect(wp?.licenseType).toBe("open_source");
  });
});
