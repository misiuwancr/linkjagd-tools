import { describe, expect, it } from "vitest";
import { CATEGORY_COPY, categoryIntro, wordCount } from "@/lib/category-copy";

describe("Kategorietexte", () => {
  it("liegt je Kategorie zwischen 150 und 300 Wörtern", () => {
    expect(CATEGORY_COPY.length).toBe(16);
    for (const item of CATEGORY_COPY) {
      const text = categoryIntro(item.slug, item.focus);
      const count = wordCount(text);
      expect(count).toBeGreaterThanOrEqual(150);
      expect(count).toBeLessThanOrEqual(300);
      expect(text.toLowerCase()).not.toContain("zzgl");
    }
  });
});
