"use server";

import { redirect } from "next/navigation";
import { categories, newsletterSubscribers, tools } from "@/db/schema";
import { getDb } from "@/db/client";
import { eq } from "drizzle-orm";
import { submissionSchema } from "@/lib/validation/tool";
import { domainFromUrl, slugify } from "@/lib/utils";
import { findByDomainOrSlug, refreshSearchText, replaceCategories } from "@/lib/tools/repository";
import { siteConfig } from "@/site.config";
import {
  confirmTokenHash,
  isNewsletterEmail,
  mailConfig,
  newConfirmToken,
  normalizeNewsletterEmail,
  sendConfirmationMail,
} from "@/lib/newsletter";

export async function subscribeNewsletter(formData: FormData) {
  const back = String(formData.get("zurueck") || "/newsletter");
  const target = back.startsWith("/") && !back.startsWith("//") ? back : "/newsletter";
  if (mailConfig().provider === "none") redirect(`${target}?hinweis=aus#anmeldung`);
  if (String(formData.get("firma") || "").trim()) redirect(`${target}?hinweis=bot#anmeldung`);
  if (formData.get("datenschutz") !== "ja") redirect(`${target}?hinweis=datenschutz#anmeldung`);
  const email = normalizeNewsletterEmail(String(formData.get("email") || ""));
  if (!isNewsletterEmail(email)) redirect(`${target}?hinweis=email#anmeldung`);
  const database = await getDb();
  const existing = await database.select().from(newsletterSubscribers).where(eq(newsletterSubscribers.email, email)).limit(1);
  if (existing[0]?.status === "confirmed") redirect(`${target}?hinweis=bereits#anmeldung`);
  const token = newConfirmToken();
  const tokenHash = confirmTokenHash(token);
  const now = new Date();
  if (existing[0]) {
    await database
      .update(newsletterSubscribers)
      .set({ confirmToken: tokenHash, status: "pending", createdAt: now, confirmedAt: null })
      .where(eq(newsletterSubscribers.id, existing[0].id));
  } else {
    await database.insert(newsletterSubscribers).values({
      id: crypto.randomUUID(),
      email,
      status: "pending",
      confirmToken: tokenHash,
      createdAt: now,
      confirmedAt: null,
    });
  }
  const link = `${siteConfig.url.replace(/\/$/, "")}/newsletter/bestaetigen?token=${token}`;
  const config = mailConfig();
  if (config.provider === "none") redirect(`${target}?hinweis=gespeichert#anmeldung`);
  const sent = await sendConfirmationMail({ to: email, link, config });
  redirect(`${target}?hinweis=${sent.sent ? "mail" : "gespeichert"}#anmeldung`);
}

export async function submitTool(formData: FormData) {
  if (String(formData.get("firma") || "").trim()) redirect("/einreichen?hinweis=danke");
  const parsed = submissionSchema.safeParse({
    name: formData.get("name"),
    originalUrl: formData.get("originalUrl"),
    shortDescriptionDe: formData.get("shortDescriptionDe"),
    categoryId: formData.get("categoryId") || "",
    submitterEmail: formData.get("submitterEmail") || "",
  });
  if (!parsed.success) {
    redirect(`/einreichen?fehler=${encodeURIComponent(parsed.error.issues[0]?.message ?? "Bitte prüfe die Eingaben.")}`);
  }
  const database = await getDb();
  const domain = domainFromUrl(parsed.data.originalUrl);
  let slug = slugify(parsed.data.name);
  if (!slug) redirect("/einreichen?fehler=Der%20Name%20ergibt%20keinen%20Kurznamen.");
  const duplicate = await findByDomainOrSlug(database, domain, slug);
  if (duplicate) redirect("/einreichen?fehler=Diese%20Domain%20oder%20dieser%20Name%20ist%20schon%20erfasst.");
  const existingSlug = await database.select({ id: tools.id }).from(tools).where(eq(tools.slug, slug)).limit(1);
  if (existingSlug[0]) slug = `${slug}-${crypto.randomUUID().slice(0, 6)}`;
  const now = new Date();
  const id = crypto.randomUUID();
  await database.insert(tools).values({
    id,
    name: parsed.data.name,
    slug,
    originalUrl: new URL(parsed.data.originalUrl).toString(),
    domain,
    shortDescriptionDe: parsed.data.shortDescriptionDe,
    longDescriptionDe: "",
    featuresDe: "[]",
    screenshots: "[]",
    pricingModel: "freemium",
    publishStatus: "draft",
    featured: false,
    discoverySource: "submission",
    isExample: false,
    submitterEmail: parsed.data.submitterEmail || null,
    searchText: "",
    createdAt: now,
    updatedAt: now,
  });
  if (parsed.data.categoryId) {
    const category = await database.select().from(categories).where(eq(categories.id, parsed.data.categoryId)).limit(1);
    if (category[0]) await replaceCategories(database, id, [category[0].id]);
  }
  await refreshSearchText(database, id);
  redirect("/einreichen?hinweis=danke");
}
