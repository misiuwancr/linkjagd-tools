import { describe, expect, it } from "vitest";
import { isNewsletterEmail, mailConfig } from "@/lib/newsletter";
import { renderMarkdown } from "@/lib/markdown";
import { publicExportRow } from "@/db/transfer";

describe("Newsletter und Markdown", () => {
  it("prüft die Adresse und verschickt ohne Schlüssel nichts", () => {
    expect(isNewsletterEmail("nicht-eine-mail")).toBe(false);
    expect(isNewsletterEmail("person@example.com")).toBe(true);
    expect(mailConfig({}).provider).toBe("none");
    expect(mailConfig({ RESEND_API_KEY: "key", NEWSLETTER_FROM: "redaktion@example.com" }).provider).toBe("none");
    expect(mailConfig({ NEWSLETTER_PROVIDER: "resend", RESEND_API_KEY: "key", NEWSLETTER_FROM: "redaktion@example.com" }).provider).toBe("resend");
    expect(mailConfig({ NEWSLETTER_PROVIDER: "brevo", BREVO_API_KEY: "key", NEWSLETTER_FROM: "redaktion@example.com", BREVO_LIST_ID: "4", BREVO_DOI_TEMPLATE_ID: "9" })).toMatchObject({
      provider: "brevo",
      listId: 4,
      doiTemplateId: 9,
    });
  });

  it("exportiert keinen Bestätigungstoken und lässt kein HTML durch", () => {
    const row = publicExportRow("newsletter_subscribers", { email: "a@b.c", confirm_token: "geheim", status: "pending" });
    expect(row).not.toHaveProperty("confirm_token");
    const html = renderMarkdown("Hallo <script>alert(1)</script>\n\n- Punkt\n\n[Seite](https://example.com)");
    expect(html).not.toContain("<script>");
    expect(html).toContain("&lt;script&gt;");
    expect(html).toContain("<li>");
    expect(html).toContain('href="https://example.com"');
  });
});
