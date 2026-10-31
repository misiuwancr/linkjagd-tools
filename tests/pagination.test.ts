import { readFileSync } from "fs";
import { describe, expect, it } from "vitest";
import { PAGE_SIZE, publicListQuery } from "@/lib/tools/query";
import { sitemapChunkCount } from "@/lib/sitemap-chunks";

describe("öffentliche Listen bleiben begrenzt", () => {
  it("liefert 24 bis 48 Karten und lässt die Seitengröße nicht aus der Adresse kommen", () => {
    expect(PAGE_SIZE).toBeGreaterThanOrEqual(24);
    expect(PAGE_SIZE).toBeLessThanOrEqual(48);
    const query = publicListQuery({ seite: "2", q: "chat", pageSize: "500" } as never);
    expect(query.page).toBe(2);
    expect(query.pageSize).toBe(PAGE_SIZE);
  });

  it("merkt Seiten, die kein Werkzeug sind", () => {
    const names = JSON.parse(readFileSync(new URL("../data/not-tools.json", import.meta.url), "utf8")) as string[];
    expect(names).toContain("dpa");
    expect(names).toContain("DFG");
    expect(names).toContain("Bundeskanzler");
    expect(names).toContain("Alpenverein Österreich");
    expect(new Set(names).size).toBe(names.length);
  });

  it("teilt die Sitemap erst ab 5000 Tool-Adressen", () => {
    expect(sitemapChunkCount(1158)).toBe(1);
    expect(sitemapChunkCount(5000)).toBe(1);
    expect(sitemapChunkCount(5001)).toBe(2);
  });
});
