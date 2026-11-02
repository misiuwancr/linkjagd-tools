import fs from "node:fs";
import { describe, expect, it } from "vitest";
import { comparisonHref, comparisons, comparisonsForTool, decisionTools, getComparison } from "@/lib/comparisons";

describe("Entscheidungsinhalte und Verlinkung", () => {
  const exported = JSON.parse(fs.readFileSync("data/export/tools.json", "utf8")) as { slug: string; publish_status: string; is_example: boolean; original_url: string }[];
  it("nutzt die vorhandene Automatisierungs-URL und legt je Thema genau einen Vergleich an", () => {
    expect(comparisons).toHaveLength(3);
    expect(new Set(comparisons.map(comparisonHref)).size).toBe(3);
    expect(comparisonHref(getComparison("zapier-make-n8n-vergleich")!)).toBe("/blog/zapier-make-n8n-vergleich");
    expect(getComparison("unbekannt")).toBeUndefined();
  });
  it("verknüpft nur vorhandene veröffentlichte Tools, passende Alternativen und Quellen", () => {
    expect(Object.keys(decisionTools)).toHaveLength(8);
    for (const [slug, tool] of Object.entries(decisionTools)) {
      const original = exported.find((row) => row.slug === slug);
      expect(original?.publish_status).toBe("published");
      expect(original?.is_example).toBeFalsy();
      expect(tool.providerUrl).toBe(original?.original_url);
      expect(new URL(tool.providerUrl).search).toBe("");
      expect(tool.sources.length).toBeGreaterThan(0);
      for (const source of tool.sources) expect(new URL(source.url).protocol).toBe("https:");
      for (const alternative of tool.alternatives) {
        expect(alternative).not.toBe(slug);
        expect(decisionTools[alternative]).toBeDefined();
      }
      expect(comparisonsForTool(slug).length).toBeGreaterThan(0);
    }
  });
  it("ordnet jede Tabellenzelle und Empfehlung eindeutig einer Lösung zu", () => {
    for (const comparison of comparisons) {
      expect(new Set(comparison.tools).size).toBe(comparison.tools.length);
      for (const slug of comparison.tools) expect(decisionTools[slug]).toBeDefined();
      for (const row of comparison.rows) {
        expect(row.values).toHaveLength(comparison.tools.length);
        expect(row.values.every((value) => value.trim().length > 0)).toBe(true);
      }
      for (const recommendation of comparison.recommendations) expect(comparison.tools).toContain(recommendation.tool);
      expect(comparison.checklist.length).toBeGreaterThanOrEqual(3);
    }
  });
  it("trennt redaktionelle Inhalte von Partnerstatus, Scores und Preisangaben", () => {
    const content = JSON.stringify({ comparisons, decisionTools });
    expect(content).not.toMatch(/affiliateUrl|editorRating|\d+\s*€|Testsieger|DSGVO-konform/);
  });
});
