import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";
import { ToolCard } from "@/components/tool-card";
import type { PublicTool } from "@/lib/tools/public";
import { affiliateTarget, decideRedirect } from "@/lib/affiliate/redirect";
import { handleGoRedirect } from "@/lib/affiliate/go";

vi.stubGlobal("React", React);
const tool = { id: "tool", name: "Testtool", slug: "testtool", domain: "vendor.example", logo: null, shortDescriptionDe: "Ein hilfreiches digitales Werkzeug.", categories: [], linkjagdVideos: [], licenseType: "unknown", pricingModel: "free", ctaEnabled: false, ctaKind: "disabled" } as unknown as PublicTool;
const record = { id: "tool", publishStatus: "published" as const, originalUrl: "https://vendor.example/" };
const stored = "https://partner.example/path?ref=Keep%2BThis&campaign=a%20b#section";
const program = { id: "partner", affiliateUrl: stored, status: "active" as const, isActive: true, priority: 1 };

describe("Affiliate-Buttons und Umgehungsschutz", () => {
  it("erhält die Detailseite auf Karten, entfernt aber den Anbieter-CTA ohne Partnerlink", () => {
    const html = renderToStaticMarkup(React.createElement(ToolCard, { tool }));
    expect(html).toContain('href="/tools/testtool"');
    expect(html).not.toContain("/go/");
    expect(html).not.toContain("Zum Anbieter");
  });
  it("zeigt bei aktivem Partnerlink einen gekennzeichneten CTA", () => {
    const html = renderToStaticMarkup(React.createElement(ToolCard, { tool: { ...tool, ctaEnabled: true, ctaKind: "affiliate" } }));
    expect(html).toContain("/go/testtool?");
    expect(html).toContain("sponsored nofollow");
    expect(html).toContain("Anzeige");
  });
  it("erhält Parameter exakt und überspringt ungültige höher priorisierte Ziele", () => {
    const programs = [{ ...program, id: "invalid", affiliateUrl: "javascript:alert(1)", priority: 20 }, program];
    expect(decideRedirect(record, programs)).toMatchObject({ ok: true, location: stored, kind: "affiliate", programId: "partner" });
    expect(programs[0].id).toBe("invalid");
    expect(affiliateTarget([program], record.originalUrl)?.location).toBe(stored);
    expect(affiliateTarget([], record.originalUrl)).toBeNull();
  });
  it("lässt den früheren Offiziell-Parameter auch mit Partnerlink nicht umgehen oder zählen", async () => {
    const load = vi.fn(async () => ({ tool: record, programs: [program] }));
    const track = vi.fn();
    expect((await handleGoRedirect("testtool", { load, track, officialOnly: true })).status).toBe(404);
    expect(load).not.toHaveBeenCalled();
    expect(track).not.toHaveBeenCalled();
  });
});
