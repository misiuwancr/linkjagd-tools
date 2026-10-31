import { and, eq, ne } from "drizzle-orm";
import { affiliatePrograms, categories, newsPosts, tools, users } from "@/db/schema";
import type { AppDatabase } from "@/db/client";
import { getAffiliateNetwork } from "@/lib/affiliate/registry";
import { validateExternalUrl, validateOutboundUrl } from "@/lib/affiliate/redirect";
import { hashPassword } from "@/lib/auth/password";
import { domainFromUrl, isSafeLocalImage, slugify } from "@/lib/utils";
import {
  affiliateInputSchema,
  categoryInputSchema,
  newsInputSchema,
  toolInputSchema,
} from "@/lib/validation/tool";
import { refreshSearchText, replaceCategories, replaceTags } from "@/lib/tools/repository";

function siteHost() {
  try {
    return new URL(process.env.NEXT_PUBLIC_SITE_URL || "http://127.0.0.1:4327").hostname;
  } catch {
    return undefined;
  }
}

export async function saveToolRecord(
  database: AppDatabase,
  raw: unknown,
  current?: { id: string; logo: string | null; screenshots: string[] },
  files?: { logo: string | null; screenshots: string[]; removeLogo: boolean; removeScreenshots: string[] },
) {
  const parsed = toolInputSchema.safeParse(raw);
  if (!parsed.success) {
    return { ok: false as const, error: parsed.error.issues[0]?.message ?? "Die Eingaben sind ungültig." };
  }
  const input = parsed.data;
  let domain = "";
  try {
    domain = domainFromUrl(input.originalUrl);
  } catch {
    return { ok: false as const, error: "Die Original-URL ist ungültig." };
  }
  const slug = slugify(input.slug || input.name);
  if (!slug) return { ok: false as const, error: "Bitte einen gültigen Kurznamen angeben." };
  const clash = await database
    .select({ id: tools.id })
    .from(tools)
    .where(current ? and(eq(tools.slug, slug), ne(tools.id, current.id)) : eq(tools.slug, slug))
    .limit(1);
  if (clash[0]) return { ok: false as const, error: "Dieser Kurzname ist bereits vergeben." };

  const knownCategories = await database.select({ id: categories.id }).from(categories);
  const allowed = new Set(knownCategories.map((category) => category.id));
  const categoryIds = input.categoryIds.filter((id) => allowed.has(id));
  const now = new Date();
  const id = current?.id ?? crypto.randomUUID();
  let logo = current?.logo ?? null;
  if (files?.removeLogo) logo = null;
  if (files?.logo) logo = files.logo;
  const screenshots = [
    ...(current?.screenshots ?? []).filter(
      (item) => isSafeLocalImage(item) && !files?.removeScreenshots.includes(item),
    ),
    ...(files?.screenshots ?? []),
  ].slice(0, 8);

  const values = {
    name: input.name,
    slug,
    originalUrl: new URL(input.originalUrl).toString(),
    domain,
    logo,
    shortDescriptionDe: input.shortDescriptionDe,
    longDescriptionDe: input.longDescriptionDe,
    featuresDe: JSON.stringify(input.featuresDe),
    screenshots: JSON.stringify(screenshots),
    pricingModel: input.pricingModel,
    licenseType: input.licenseType,
    useCasesDe: JSON.stringify(input.useCasesDe),
    beginnerFriendly: input.beginnerFriendly,
    ossProjectUrl: input.ossProjectUrl || null,
    ossRepoUrl: input.ossRepoUrl || null,
    ossLicense: input.ossLicense || null,
    ossOperatingSystems: JSON.stringify(input.ossOperatingSystems),
    ossInstallNotes: input.ossInstallNotes || null,
    tiktokUrl: input.tiktokUrl || null,
    instagramReelUrl: input.instagramReelUrl || null,
    youtubeShortUrl: input.youtubeShortUrl || null,
    editorRating: input.editorRating,
    contentLocked: true,
    publishStatus: input.publishStatus,
    featured: input.featured,
    editorialRank: input.editorialRank,
    discoverySource: input.discoverySource,
    isExample: input.isExample,
    internalNotes: input.internalNotes || null,
    updatedAt: now,
  };

  if (current) {
    await database.update(tools).set(values).where(eq(tools.id, id));
  } else {
    await database.insert(tools).values({ ...values, id, searchText: "", createdAt: now });
  }
  await replaceCategories(database, id, categoryIds);
  await replaceTags(database, id, input.tags);
  await refreshSearchText(database, id);
  return { ok: true as const, id, slug };
}

export async function removeTool(database: AppDatabase, id: string) {
  await database.delete(tools).where(eq(tools.id, id));
}

export async function setToolStatus(
  database: AppDatabase,
  id: string,
  status: "draft" | "published" | "archived",
) {
  await database.update(tools).set({ publishStatus: status, updatedAt: new Date() }).where(eq(tools.id, id));
}

export async function saveAffiliateRecord(
  database: AppDatabase,
  toolId: string,
  raw: unknown,
  programId?: string,
) {
  const tool = await database.select().from(tools).where(eq(tools.id, toolId)).limit(1);
  if (!tool[0]) return { ok: false as const, error: "Tool nicht gefunden." };
  const parsed = affiliateInputSchema.safeParse(raw);
  if (!parsed.success) {
    return { ok: false as const, error: parsed.error.issues[0]?.message ?? "Die Partnerdaten sind ungültig." };
  }
  const input = parsed.data;
  if (!getAffiliateNetwork(input.network)) {
    return { ok: false as const, error: "Unbekanntes Partnernetzwerk." };
  }
  let programInfoUrl: string | null = null;
  if (input.programInfoUrl) {
    const checked = validateExternalUrl(input.programInfoUrl, siteHost());
    if (!checked.ok) {
      return { ok: false as const, error: "Die Programmseite ist keine gültige öffentliche https-Adresse." };
    }
    programInfoUrl = checked.url;
  }
  let affiliateUrl: string | null = null;
  if (input.affiliateUrl) {
    const checked = validateOutboundUrl(input.affiliateUrl, tool[0].originalUrl, siteHost());
    if (!checked.ok) {
      const message =
        checked.reason === "matches_original"
          ? "Die Affiliate-URL darf nicht die Original-URL sein. Es wird kein Fallback eingerichtet."
          : "Die Affiliate-URL ist kein gültiges, erlaubtes Ziel.";
      return { ok: false as const, error: message };
    }
    affiliateUrl = checked.url;
  }
  if (input.isActive) {
    if (input.status !== "active" || !affiliateUrl) {
      return {
        ok: false as const,
        error: "Nur ein Programm mit Status „Affiliate-Link aktiv“ und gültiger URL kann der öffentliche Link sein.",
      };
    }
  }
  const now = new Date();
  const id = programId ?? crypto.randomUUID();
  const values = {
    affiliateUrl,
    programInfoUrl,
    programPresence: input.programPresence,
    network: input.network,
    partnerProgramId: input.partnerProgramId || null,
    status: input.status,
    priority: input.priority,
    isActive: input.isActive,
    notes: input.notes || null,
    lastCheckedAt: now,
    updatedAt: now,
  };
  if (input.isActive) {
    await database.update(affiliatePrograms).set({ isActive: false }).where(eq(affiliatePrograms.toolId, toolId));
  }
  if (programId) {
    await database.update(affiliatePrograms).set(values).where(eq(affiliatePrograms.id, programId));
  } else {
    await database.insert(affiliatePrograms).values({ ...values, id, toolId, createdAt: now });
  }
  return { ok: true as const, id };
}

export async function removeAffiliate(database: AppDatabase, id: string) {
  await database.delete(affiliatePrograms).where(eq(affiliatePrograms.id, id));
}

export async function saveCategoryRecord(database: AppDatabase, raw: unknown, id?: string) {
  const parsed = categoryInputSchema.safeParse(raw);
  if (!parsed.success) {
    return { ok: false as const, error: parsed.error.issues[0]?.message ?? "Die Kategorie ist ungültig." };
  }
  const slug = slugify(parsed.data.slug || parsed.data.name);
  if (!slug) return { ok: false as const, error: "Bitte einen gültigen Kurznamen angeben." };
  const clash = await database
    .select({ id: categories.id })
    .from(categories)
    .where(id ? and(eq(categories.slug, slug), ne(categories.id, id)) : eq(categories.slug, slug))
    .limit(1);
  if (clash[0]) return { ok: false as const, error: "Diese Kategorie gibt es schon." };
  const now = new Date();
  const values = {
    name: parsed.data.name,
    slug,
    description: parsed.data.description || null,
    sortOrder: parsed.data.sortOrder,
    updatedAt: now,
  };
  const categoryId = id ?? slug;
  if (id) {
    await database.update(categories).set(values).where(eq(categories.id, id));
  } else {
    await database.insert(categories).values({ ...values, id: categoryId, createdAt: now });
  }
  return { ok: true as const, id: categoryId };
}

export async function removeCategory(database: AppDatabase, id: string) {
  await database.delete(categories).where(eq(categories.id, id));
}

export async function saveNewsRecord(database: AppDatabase, raw: unknown) {
  const parsed = newsInputSchema.safeParse(raw);
  if (!parsed.success) {
    return { ok: false as const, error: parsed.error.issues[0]?.message ?? "Die Meldung ist ungültig." };
  }
  const slug = slugify(parsed.data.title);
  if (!slug) return { ok: false as const, error: "Aus dem Titel lässt sich kein Kurzname bilden." };
  const now = new Date();
  await database.insert(newsPosts).values({
    id: crypto.randomUUID(),
    title: parsed.data.title,
    slug,
    excerpt: parsed.data.excerpt,
    body: parsed.data.body,
    sourceName: parsed.data.sourceName || null,
    status: parsed.data.status,
    publishedAt: parsed.data.status === "published" ? now : null,
    createdAt: now,
    updatedAt: now,
  });
  return { ok: true as const };
}

export async function createEditor(database: AppDatabase, email: string, password: string) {
  const normalized = email.trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalized)) {
    return { ok: false as const, error: "Bitte eine gültige E-Mail angeben." };
  }
  if (password.length < 12) {
    return { ok: false as const, error: "Das Passwort braucht mindestens 12 Zeichen." };
  }
  const existing = await database.select().from(users).where(eq(users.email, normalized)).limit(1);
  if (existing[0]) return { ok: false as const, error: "Diese E-Mail ist schon vergeben." };
  await database.insert(users).values({
    id: crypto.randomUUID(),
    email: normalized,
    passwordHash: hashPassword(password),
    role: "editor",
    createdAt: new Date(),
  });
  return { ok: true as const };
}
