import { describe, expect, it } from "vitest";
import { USE_CASES } from "@/lib/use-cases";

describe("Sammlungen", () => {
  it("hat eigene Texte und Fragen ohne erfundene Bestenliste", () => {
    expect(USE_CASES.length).toBeGreaterThanOrEqual(15);
    const slugs = new Set<string>();
    for (const item of USE_CASES) {
      expect(slugs.has(item.slug)).toBe(false);
      slugs.add(item.slug);
      expect(item.intro.length).toBeGreaterThan(80);
      expect(item.faqs.length).toBeGreaterThanOrEqual(2);
      expect(item.intro.toLowerCase()).not.toContain("zzgl");
      expect(item.intro.toLowerCase()).not.toContain("die besten");
    }
  });
});
