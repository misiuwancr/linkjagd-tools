import { describe, expect, it } from "vitest";
import { indexingPolicy, toolIsIndexable } from "@/lib/indexing";
import { qualityIssues } from "@/lib/quality";

describe("Indexierung", () => {
  it("lässt Produktion an und schaltet Vorschau und lokal aus", () => {
    expect(indexingPolicy({ VERCEL_ENV: "production" }).index).toBe(true);
    expect(indexingPolicy({ VERCEL_ENV: "production", INDEXING_ENABLED: "false" }).index).toBe(false);
    expect(indexingPolicy({ VERCEL_ENV: "preview", INDEXING_ENABLED: "true" }).index).toBe(false);
    expect(indexingPolicy({}).index).toBe(false);
  });

  it("indexiert ein veröffentlichtes Tool nur, wenn der Schalter und die Freigabe an sind", () => {
    expect(toolIsIndexable({ globalIndex: true, allowIndex: true, published: true })).toBe(true);
    expect(toolIsIndexable({ globalIndex: true, allowIndex: false, published: true })).toBe(false);
    expect(toolIsIndexable({ globalIndex: false, allowIndex: true, published: true })).toBe(false);
    expect(toolIsIndexable({ globalIndex: true, allowIndex: true, published: false })).toBe(false);
  });

  it("meldet Platzhalter und fehlende Kategorie, ohne eine Bewertung zu erfinden", () => {
    const issues = qualityIssues({
      name: "Beispielsatz",
      shortDescriptionDe: "kurz",
      originalUrl: "http://example.com",
      pricingModel: "freemium",
      categoryCount: 0,
      publishStatus: "published",
    });
    expect(issues.join(" ")).toContain("Platzhalter");
    expect(issues.join(" ")).toContain("Kategorie");
    expect(issues.join(" ")).not.toContain("zzgl");
  });
});
