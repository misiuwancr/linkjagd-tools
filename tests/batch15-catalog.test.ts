import { readFileSync } from "fs";
import { describe, expect, it } from "vitest";

const catalog = JSON.parse(readFileSync(new URL("../data/verified-tools-batch15.json", import.meta.url), "utf8")) as Array<{
  name: string;
  originalUrl: string;
  domain: string;
  longDescriptionDe: string;
}>;

describe("fünfzehnte geprüfte Liste", () => {
  it("enthält weitere KI-Werkzeuge ohne gespeicherten Affiliate-Link", () => {
    expect(catalog.length).toBeGreaterThanOrEqual(30);
    const domains = new Set<string>();
    for (const entry of catalog) {
      expect(domains.has(entry.domain)).toBe(false);
      domains.add(entry.domain);
      expect(entry.originalUrl.startsWith("https://")).toBe(true);
      expect(entry.longDescriptionDe.toLowerCase()).not.toContain("zzgl");
      expect(JSON.stringify(entry)).not.toContain("affiliateUrl");
    }
  });
});
