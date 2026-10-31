import { describe, expect, it } from "vitest";
import { siteConfig } from "@/site.config";
import { weeklyPopularVisible } from "@/lib/tools/popular";
import { categoryIconName } from "@/components/category-icon";

describe("Startseite", () => {
  it("verspricht keine Bestenliste und zeigt Beliebtheit nur ab echten Klicks", () => {
    expect(siteConfig.tagline.toLowerCase()).not.toContain("besten");
    expect(siteConfig.tagline).toContain("Open Source");
    expect(weeklyPopularVisible(2)).toBe(false);
    expect(weeklyPopularVisible(3)).toBe(true);
    expect(categoryIconName("unbekannt")).toBe("fallback");
    expect(categoryIconName("ki-chatbots")).toBe("ki-chatbots");
  });
});
