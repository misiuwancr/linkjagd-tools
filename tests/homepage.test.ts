import { describe, expect, it } from "vitest";
import { siteConfig } from "@/site.config";
import { weeklyPopularVisible } from "@/lib/tools/popular";
import { categoryIconName } from "@/components/category-icon";

describe("Startseite", () => {
  it("zeigt den Markenslogan und Beliebtheit nur ab echten Klicks", () => {
    expect(siteConfig.tagline.toLowerCase()).not.toContain("besten");
    expect(siteConfig.tagline).toBe("Entdecke das Beste im Web.");
    expect(weeklyPopularVisible(2)).toBe(false);
    expect(weeklyPopularVisible(3)).toBe(true);
    expect(categoryIconName("unbekannt")).toBe("fallback");
    expect(categoryIconName("chat-assistenten")).toBe("chat-assistenten");
  });
});
