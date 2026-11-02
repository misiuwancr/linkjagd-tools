import { describe, expect, it, vi } from "vitest";
import { platformText } from "@/lib/branding";
import { siteConfig } from "@/site.config";
import { sendConfirmationMail } from "@/lib/newsletter";

describe("Linknarr und Linkjagd", () => {
  it("trennt Plattform und Kanal und passt alte Anzeigetexte ohne Datenänderung an", () => {
    const stored = { text: "Linkjagd Tools – bekannt aus Linkjagd-Videos", url: "https://vendor.example/?ref=unchanged" };
    expect(siteConfig.name).toBe("Linknarr");
    expect(siteConfig.tagline).toBe("Entdecke das Beste im Web.");
    expect(siteConfig.creator.channel).toBe("@linkjagd");
    expect(platformText(stored.text)).toBe("Linknarr – bekannt aus Linkjagd-Videos");
    expect(platformText("LINKJAGD TOOLS / Linkjagd")).toBe("Linknarr / Linkjagd");
    expect(stored.text).toContain("Linkjagd Tools");
    expect(stored.url).toBe("https://vendor.example/?ref=unchanged");
  });

  it("verwendet die Plattformmarke auch für Bestätigungsmails", async () => {
    const mock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response("{}", { status: 200 }));
    try {
      await sendConfirmationMail({ to: "person@example.test", link: "https://linknarr.com/newsletter/bestaetigen?token=test", config: { provider: "resend", key: "test-key", from: "test@example.test" } });
      const body = JSON.parse(mock.mock.calls[0][1]!.body as string);
      expect(body.subject).toContain("Linknarr");
      expect(body.text).toContain("https://linknarr.com/newsletter/bestaetigen?token=test");
      expect(body.text).not.toContain("Linkjagd Tools");
    } finally { mock.mockRestore(); }
  });
});
