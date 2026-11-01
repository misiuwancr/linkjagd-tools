import { describe, expect, it } from "vitest";
import { aiNewsSchema, publishedAiNews } from "@/lib/ai-news";
describe("News-Quellen", () => {
  const entry = { id: "test", title: "Eigener Titel", summary: "Eigene Zusammenfassung", category: "Forschung", publishedAt: "2026-11-01T12:00:00Z", sourceName: "Originalquelle", sourceUrl: "https://example.com/news" };
  it("erfordert eine sichere Originalquelle und ein gültiges Datum", () => {
    expect(aiNewsSchema.safeParse(entry).success).toBe(true);
    expect(aiNewsSchema.safeParse({ ...entry, sourceUrl: "javascript:alert(1)" }).success).toBe(false);
    expect(aiNewsSchema.safeParse({ ...entry, publishedAt: "kein Datum" }).success).toBe(false);
    expect(aiNewsSchema.safeParse({ ...entry, imageUrl: "//tracker.example/bild" }).success).toBe(false);
    expect(aiNewsSchema.safeParse({ ...entry, imageUrl: "/news-placeholder.svg" }).success).toBe(true);
  });
  it("erfindet ohne gelieferte Datei keine Meldungen", () => {
    expect(publishedAiNews()).toEqual([]);
  });
});
