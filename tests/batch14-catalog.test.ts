import { readFileSync } from "fs";
import { describe, expect, it } from "vitest";

const catalog = JSON.parse(readFileSync(new URL("../data/verified-tools-batch14.json", import.meta.url), "utf8")) as Array<{
  name: string;
  originalUrl: string;
  domain: string;
  longDescriptionDe: string;
}>;
const notTools = new Set(JSON.parse(readFileSync(new URL("../data/not-tools.json", import.meta.url), "utf8")) as string[]);

describe("vierzehnte geprüfte Liste", () => {
  it("enthält bekannte KI-Tools ohne Nachrichten oder Behörden", () => {
    expect(catalog.length).toBeGreaterThanOrEqual(40);
    const domains = new Set<string>();
    for (const entry of catalog) {
      expect(notTools.has(entry.name)).toBe(false);
      expect(domains.has(entry.domain)).toBe(false);
      domains.add(entry.domain);
      expect(entry.originalUrl.startsWith("https://")).toBe(true);
      expect(entry.longDescriptionDe.toLowerCase()).not.toContain("zzgl");
    }
  });
});
