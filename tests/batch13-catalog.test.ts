import { readFileSync } from "fs";
import { describe, expect, it } from "vitest";

const catalog = JSON.parse(readFileSync(new URL("../data/verified-tools-batch13.json", import.meta.url), "utf8")) as Array<{
  originalUrl: string;
  domain: string;
  longDescriptionDe: string;
}>;
const notTools = new Set(JSON.parse(readFileSync(new URL("../data/not-tools.json", import.meta.url), "utf8")) as string[]);

describe("dreizehnte geprüfte Liste", () => {
  it("enthält nur Werkzeuge und keine archivierten Nachrichtenseiten", () => {
    expect(catalog.length).toBeGreaterThanOrEqual(20);
    const domains = new Set<string>();
    for (const entry of catalog) {
      expect(domains.has(entry.domain)).toBe(false);
      domains.add(entry.domain);
      expect(entry.originalUrl.startsWith("https://")).toBe(true);
      expect(entry.longDescriptionDe.toLowerCase()).not.toContain("zzgl");
      expect(notTools.has((entry as { name?: string }).name ?? "")).toBe(false);
    }
  });
});
