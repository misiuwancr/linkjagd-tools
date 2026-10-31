import { readFileSync } from "fs";
import { describe, expect, it } from "vitest";

const catalog = JSON.parse(readFileSync(new URL("../data/verified-tools-batch18.json", import.meta.url), "utf8")) as Array<{
  name: string;
  originalUrl: string;
  domain: string;
  longDescriptionDe: string;
}>;

describe("achtzehnte geprüfte Liste", () => {
  it("enthält weitere Web-Apps ohne Affiliate-Link", () => {
    expect(catalog.length).toBeGreaterThanOrEqual(20);
    const domains = new Set<string>();
    for (const entry of catalog) {
      expect(domains.has(entry.domain)).toBe(false);
      domains.add(entry.domain);
      expect(entry.originalUrl.startsWith("https://")).toBe(true);
      expect(entry.longDescriptionDe.toLowerCase()).not.toContain("zzgl");
    }
  });
});
