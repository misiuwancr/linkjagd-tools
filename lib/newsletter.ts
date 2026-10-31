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
  | { provider: "brevo"; key: string; from: string }
  | { provider: "none" };

export function mailConfig(env: NodeJS.ProcessEnv = process.env): MailConfig {
  const from = (env.NEWSLETTER_FROM || "").trim();
  const resend = (env.RESEND_API_KEY || "").trim();
  const brevo = (env.BREVO_API_KEY || "").trim();
  if (resend && from) return { provider: "resend", key: resend, from };
  if (brevo && from) return { provider: "brevo", key: brevo, from };
  return { provider: "none" };
}

export async function sendConfirmationMail(input: { to: string; link: string; config: MailConfig }) {
  if (input.config.provider === "none") return { sent: false as const, reason: "kein Versanddienst" };
  const subject = "Bitte bestätige deine Anmeldung bei Linkjagd Tools";
  const text = [
    "Hallo,",
    "",
    "du hast dich für Hinweise von Linkjagd Tools eingetragen. Bitte bestätige die Adresse über diesen Link:",
    input.link,
    "",
    "Ohne diese Bestätigung bleibt die Anmeldung offen und es geht keine weitere Mail raus.",
    "Wenn du das nicht warst, ignoriere diese Nachricht.",
  ].join("\n");
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
