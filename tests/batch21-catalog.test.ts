import { readFileSync } from "fs";
import { describe, expect, it } from "vitest";

const catalog = JSON.parse(readFileSync(new URL("../data/verified-tools-batch21.json", import.meta.url), "utf8")) as Array<{
  name: string;
  originalUrl: string;
  domain: string;
  licenseType: string;
  longDescriptionDe: string;
}>;

describe("einundzwanzigste geprüfte Liste", () => {
  it("enthält Buchhaltung und Fernwartung, TightVNC nur mit GPL", () => {
    expect(catalog.length).toBeGreaterThanOrEqual(20);
    const domains = new Set<string>();
    for (const entry of catalog) {
      expect(domains.has(entry.domain)).toBe(false);
      domains.add(entry.domain);
      expect(entry.originalUrl.startsWith("https://")).toBe(true);
      expect(entry.longDescriptionDe.toLowerCase()).not.toContain("zzgl");
    }
    const vnc = catalog.find((entry) => entry.domain === "tightvnc.com");
    expect(vnc?.licenseType).toBe("open_source");
  });
});
