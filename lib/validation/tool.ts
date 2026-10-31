import { z } from "zod";
import { affiliateStatuses, licenseTypes, pricingModels, programPresences, publishStatuses, triStates } from "@/db/schema";
import { domainFromUrl } from "@/lib/utils";
import { optionalVideoUrl } from "@/lib/videos";

z.setErrorMap((issue, ctx) => {
  if (issue.code === "invalid_type") return { message: "Bitte dieses Feld ausfüllen." };
  if (issue.code === "too_small") return { message: "Die Eingabe ist zu kurz." };
  if (issue.code === "too_big") return { message: "Die Eingabe ist zu lang." };
  if (issue.code === "invalid_enum_value") return { message: "Bitte einen der vorgegebenen Werte wählen." };
  if (issue.code === "invalid_string" && issue.validation === "email") {
    return { message: "Die E-Mail-Adresse sieht ungültig aus." };
  }
  if (issue.code === "invalid_string" && issue.validation === "url") {
    return { message: "Bitte eine gültige URL angeben." };
  }
  return { message: ctx.defaultError };
});

const httpUrl = z
  .string()
  .trim()
  .url("Bitte eine gültige URL angeben.")
  .refine((value) => {
    try {
      const url = new URL(value);
      return url.protocol === "http:" || url.protocol === "https:";
    } catch {
      return false;
    }
  }, "Nur http- und https-Adressen sind erlaubt.");

export const toolInputSchema = z.object({
  name: z.string().trim().min(2, "Der Name ist zu kurz.").max(120),
  slug: z.string().trim().max(80).optional().default(""),
  originalUrl: httpUrl,
  shortDescriptionDe: z.string().trim().min(10, "Die Kurzbeschreibung ist zu kurz.").max(280),
  longDescriptionDe: z.string().trim().max(20000).default(""),
  featuresDe: z.array(z.string().trim().min(1).max(180)).max(12),
  pricingModel: z.enum(pricingModels),
  licenseType: z.enum(licenseTypes).default("unknown"),
  useCasesDe: z.array(z.string().trim().min(1).max(180)).max(12).default([]),
  beginnerFriendly: z.boolean().default(false),
  germanUi: z.enum(triStates).default("unklar"),
  noSignup: z.enum(triStates).default("unklar"),
  ossProjectUrl: z.string().trim().max(500).default(""),
  ossRepoUrl: z.string().trim().max(500).default(""),
  ossLicense: z.string().trim().max(80).default(""),
  ossOperatingSystems: z.array(z.string().trim().min(1).max(40)).max(8).default([]),
  ossInstallNotes: z.string().trim().max(2000).default(""),
  tiktokUrl: z
    .string()
    .trim()
    .max(500)
    .default("")
    .refine((value) => optionalVideoUrl(value, "tiktok") !== null, "Nur Adressen von tiktok.com."),
  instagramReelUrl: z
    .string()
    .trim()
    .max(500)
    .default("")
    .refine((value) => optionalVideoUrl(value, "instagram") !== null, "Nur Adressen von instagram.com."),
  youtubeShortUrl: z
    .string()
    .trim()
    .max(500)
    .default("")
    .refine((value) => optionalVideoUrl(value, "youtube") !== null, "Nur Adressen von youtube.com oder youtu.be."),
  editorRating: z.number().int().min(1).max(5).nullable().default(null),
  publishStatus: z.enum(publishStatuses),
  featured: z.boolean(),
  editorialRank: z.number().int().min(1).max(20).nullable(),
  isExample: z.boolean(),
  categoryIds: z.array(z.string()).max(8),
  tags: z.array(z.string().trim().min(1).max(40)).max(12),
  internalNotes: z.string().max(5000).optional().default(""),
  discoverySource: z.string().trim().min(2).max(80).default("manual"),
});

export const affiliateInputSchema = z.object({
  affiliateUrl: z.string().trim().max(2000).optional().default(""),
  programInfoUrl: z.string().trim().max(2000).optional().default(""),
  programPresence: z.enum(programPresences).optional().default("unknown"),
  network: z.string().trim().min(2).max(40),
  partnerProgramId: z.string().trim().max(120).optional().default(""),
  status: z.enum(affiliateStatuses),
  priority: z.number().int().min(0).max(100),
  isActive: z.boolean(),
  notes: z.string().max(2000).optional().default(""),
});

export const categoryInputSchema = z.object({
  name: z.string().trim().min(2).max(80),
  slug: z.string().trim().max(80).optional().default(""),
  description: z.string().trim().max(500).optional().default(""),
  sortOrder: z.number().int().min(0).max(999),
});

export const newsInputSchema = z.object({
  title: z.string().trim().min(4).max(160),
  excerpt: z.string().trim().min(10).max(300),
  body: z.string().trim().max(20000).default(""),
  sourceName: z.string().trim().max(120).optional().default(""),
  status: z.enum(["draft", "published"]),
});

export const submissionSchema = z.object({
  name: z.string().trim().min(2).max(120),
  originalUrl: httpUrl,
  shortDescriptionDe: z.string().trim().min(10).max(280),
  categoryId: z.string().trim().optional().default(""),
  submitterEmail: z.string().trim().email("Die E-Mail-Adresse sieht ungültig aus.").optional().or(z.literal("")),
});

export const importToolSchema = z.object({
  name: z.string().trim().min(2).max(120),
  originalUrl: httpUrl,
  shortDescriptionDe: z.string().trim().min(10).max(280),
  longDescriptionDe: z.string().trim().max(20000).optional().default(""),
  pricingModel: z.enum(pricingModels).optional().default("freemium"),
  categorySlugs: z.array(z.string().trim()).max(8).optional().default([]),
  tags: z.array(z.string().trim().min(1).max(40)).max(12).optional().default([]),
  discoverySource: z.string().trim().min(2).max(80),
});

export function checkedDomain(url: string) {
  return domainFromUrl(url);
}
