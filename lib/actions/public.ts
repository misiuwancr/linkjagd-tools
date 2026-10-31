"use server";

import { redirect } from "next/navigation";
import { categories, tools } from "@/db/schema";
import { getDb } from "@/db/client";
import { eq } from "drizzle-orm";
import { submissionSchema } from "@/lib/validation/tool";
import { domainFromUrl, slugify } from "@/lib/utils";
import { findByDomainOrSlug, refreshSearchText, replaceCategories } from "@/lib/tools/repository";

export async function newsletterIntent(formData: FormData) {
  if (String(formData.get("firma") || "").trim()) redirect("/?hinweis=newsletter#newsletter");
  redirect("/?hinweis=newsletter#newsletter");
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
