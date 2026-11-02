import { siteConfig } from "@/site.config";
import { createHash, randomBytes } from "crypto";

export function normalizeNewsletterEmail(value: string) {
  return value.trim().toLowerCase();
}

export function isNewsletterEmail(value: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalizeNewsletterEmail(value));
}

export function newConfirmToken() {
  return randomBytes(32).toString("hex");
}

export function confirmTokenHash(token: string) {
  return createHash("sha256").update(token).digest("hex");
}

export type MailConfig =
  | { provider: "resend"; key: string; from: string }
  | { provider: "brevo"; key: string; from: string; listId?: number; doiTemplateId?: number }
  | { provider: "none" };

export function mailConfig(env: { [key: string]: string | undefined } = process.env): MailConfig {
  const provider = (env.NEWSLETTER_PROVIDER || "").trim().toLowerCase();
  const from = (env.NEWSLETTER_FROM || "").trim();
  if (provider === "resend") {
    const key = (env.RESEND_API_KEY || "").trim();
    if (key && from) return { provider: "resend", key, from };
  }
  if (provider === "brevo") {
    const key = (env.BREVO_API_KEY || "").trim();
    if (key && from) {
      const listId = Number(env.BREVO_LIST_ID);
      const doiTemplateId = Number(env.BREVO_DOI_TEMPLATE_ID);
      return {
        provider: "brevo",
        key,
        from,
        ...(Number.isInteger(listId) && listId > 0 ? { listId } : {}),
        ...(Number.isInteger(doiTemplateId) && doiTemplateId > 0 ? { doiTemplateId } : {}),
      };
    }
  }
  return { provider: "none" };
}

export function newsletterOpen(env: { [key: string]: string | undefined } = process.env) {
  return mailConfig(env).provider !== "none";
}

export async function sendConfirmationMail(input: { to: string; link: string; config: MailConfig }) {
  if (input.config.provider === "none") return { sent: false as const, reason: "kein Versanddienst" };
  const subject = `Bitte bestätige deine Anmeldung bei ${siteConfig.name}`;
  const text = [
    "Hallo,",
    "",
    `du hast dich für Hinweise von ${siteConfig.name} eingetragen. Bitte bestätige die Adresse über diesen Link:`,
    input.link,
    "",
    "Ohne diese Bestätigung bleibt die Anmeldung offen und es geht keine weitere Mail raus.",
    "Wenn du das nicht warst, ignoriere diese Nachricht.",
  ].join("\n");
  if (input.config.provider === "brevo" && input.config.doiTemplateId && input.config.listId) {
    const response = await fetch("https://api.brevo.com/v3/contacts/doubleOptinRequest", {
      method: "POST",
      headers: { "api-key": input.config.key, "Content-Type": "application/json", accept: "application/json" },
      body: JSON.stringify({
        email: input.to,
        includeListIds: [input.config.listId],
        templateId: input.config.doiTemplateId,
        redirectionUrl: input.link,
      }),
    });
    return response.ok ? { sent: true as const } : { sent: false as const, reason: "Versand fehlgeschlagen" };
  }
  if (input.config.provider === "resend") {
    const response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${input.config.key}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ from: input.config.from, to: input.to, subject, text }),
    });
    return response.ok ? { sent: true as const } : { sent: false as const, reason: "Versand fehlgeschlagen" };
  }
  const response = await fetch("https://api.brevo.com/v3/smtp/email", {
    method: "POST",
    headers: { "api-key": input.config.key, "Content-Type": "application/json" },
    body: JSON.stringify({
      sender: { email: input.config.from },
      to: [{ email: input.to }],
      subject,
      textContent: text,
    }),
  });
  return response.ok ? { sent: true as const } : { sent: false as const, reason: "Versand fehlgeschlagen" };
}
