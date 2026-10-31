import { describe, expect, it } from "vitest";
import { ALTERNATIVE_SLUGS, alternativeIntro } from "@/lib/alternatives";

describe("Alternativen", () => {
  it("nennt bekannte Tools einmal und erfindet keine Wertung", () => {
    expect(ALTERNATIVE_SLUGS.length).toBeGreaterThanOrEqual(50);
    expect(new Set(ALTERNATIVE_SLUGS).size).toBe(ALTERNATIVE_SLUGS.length);
    const text = alternativeIntro("Notion", "Produktivität");
    expect(text.toLowerCase()).not.toContain("zzgl");
    expect(text.toLowerCase()).not.toContain("beste");
    expect(text).toContain("Notion");
  });
});
