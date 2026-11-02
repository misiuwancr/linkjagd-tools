import { describe, expect, it, vi } from "vitest";
import { decideRedirect, sameDestination, validateOutboundUrl } from "@/lib/affiliate/redirect";
import { handleGoRedirect } from "@/lib/affiliate/go";
import type { AffiliateProgram, Tool } from "@/db/schema";

const original = "https://nordlicht.example/app";

function tool(overrides: Partial<Pick<Tool, "id" | "publishStatus" | "originalUrl">> = {}) {
  return {
    id: "tool-1",
    publishStatus: "published" as const,
    originalUrl: original,
    ...overrides,
  };
}

function program(
  overrides: Partial<Pick<AffiliateProgram, "id" | "affiliateUrl" | "status" | "isActive" | "priority">> = {},
) {
  return {
    id: "program-1",
    affiliateUrl: "https://partner.example/r/nordlicht?ref=test",
    status: "active" as const,
    isActive: true,
    priority: 1,
    ...overrides,
  };
}

describe("Weiterleitung /go", () => {
  it("leitet nur auf die gespeicherte Affiliate-URL um", () => {
    const decision = decideRedirect(tool(), [program()]);
    expect(decision.ok).toBe(true);
    if (decision.ok) {
      expect(decision.location).toBe("https://partner.example/r/nordlicht?ref=test");
      expect(decision.location).not.toBe(original);
    }
  });

  it("hängt keine Parameter an", () => {
    const stored = "https://partner.example/go";
    const decision = decideRedirect(tool(), [program({ affiliateUrl: stored })]);
    expect(decision.ok && decision.location).toBe(stored);
  });

  it("verwendet die Originaladresse niemals als Ersatz", () => {
    expect(decideRedirect(tool(), [])).toEqual({ ok: false, reason: "affiliate_missing" });
  });

  it("blendet fehlende, inaktive und ungültige Partnerlinks aus", () => {
    for (const extra of [program({ isActive: false }), program({ status: "approved" }), program({ status: "disabled" }), program({ affiliateUrl: null }), program({ affiliateUrl: "javascript:alert(1)" })]) {
      expect(decideRedirect(tool(), [extra])).toEqual({ ok: false, reason: "affiliate_missing" });
    }
  });

  it("lehnt eine als Partnerlink eingetragene Originaladresse ab", () => {
    expect(decideRedirect(tool(), [program({ affiliateUrl: original })]).ok).toBe(false);
    expect(validateOutboundUrl(original, original)).toMatchObject({ reason: "matches_original" });
  });

  it("erlaubt dieselbe Domain nur mit abweichender gespeicherter URL", () => {
    const affiliate = "https://nordlicht.example/app?ref=hinterlegt";
    const decision = decideRedirect(tool(), [program({ affiliateUrl: affiliate })]);
    expect(decision.ok).toBe(true);
    expect(sameDestination(affiliate, original)).toBe(false);
  });

  it("veröffentlicht Entwürfe und Archiv nicht", () => {
    expect(decideRedirect(tool({ publishStatus: "draft" }), [program()]).ok).toBe(false);
    expect(decideRedirect(tool({ publishStatus: "archived" }), [program()]).ok).toBe(false);
    expect(decideRedirect(null, [program()]).ok).toBe(false);
  });

  it("blockiert javascript, Zugangsdaten, lokale Hosts und die eigene Website", () => {
    expect(validateOutboundUrl("javascript:alert(1)", original).ok).toBe(false);
    expect(validateOutboundUrl("https://user:pass@partner.example/r", original).ok).toBe(false);
    expect(validateOutboundUrl("http://127.0.0.1/admin", original).ok).toBe(false);
    expect(validateOutboundUrl("https://linkjagd.test/tools/x", original, "linkjagd.test").ok).toBe(false);
  });

  it("zählt nur Tool, Programm und Tag und leitet danach weiter", async () => {
    const track = vi.fn(async () => undefined);
    const result = await handleGoRedirect("nordlicht-chat", {
      now: new Date("2026-10-31T12:00:00.000Z"),
      load: async () => ({ tool: tool(), programs: [program()] }),
      track,
    });
    expect(result).toEqual({ status: 302, location: "https://partner.example/r/nordlicht?ref=test" });
    expect(track).toHaveBeenCalledTimes(1);
    expect(track).toHaveBeenCalledWith({
      toolId: "tool-1",
      programId: "program-1",
      kind: "affiliate",
      day: "2026-10-31",
    });
  });

  it("antwortet ohne Partnerlink mit 404 und zählt keinen Klick", async () => {
    const track = vi.fn();
    const result = await handleGoRedirect("nordlicht-chat", { load: async () => ({ tool: tool(), programs: [] }), track });
    expect(result.status).toBe(404);
    expect(track).not.toHaveBeenCalled();
  });

  it("leitet auch dann weiter, wenn das Zählen scheitert", async () => {
    const result = await handleGoRedirect("nordlicht-chat", {
      load: async () => ({ tool: tool(), programs: [program()] }),
      track: async () => {
        throw new Error("Datenbank");
      },
    });
    expect(result.status).toBe(302);
  });
});
