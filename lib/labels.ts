import type { AffiliateStatus, PricingModel, PublishStatus } from "@/db/schema";

export const pricingOptions: { value: PricingModel; label: string; param: string }[] = [
  { value: "free", label: "Kostenlos", param: "kostenlos" },
  { value: "freemium", label: "Freemium", param: "freemium" },
  { value: "paid", label: "Kostenpflichtig", param: "kostenpflichtig" },
  { value: "open_source", label: "Open Source", param: "open-source" },
];

export const sortOptions = [
  { value: "newest", label: "Neueste", param: "neueste" },
  { value: "popular", label: "Beliebteste", param: "beliebteste" },
  { value: "alpha", label: "Alphabetisch", param: "alphabetisch" },
  { value: "featured", label: "Empfohlen", param: "empfohlen" },
] as const;

export type SortKey = (typeof sortOptions)[number]["value"];

export const publishLabels: Record<PublishStatus, string> = {
  draft: "Entwurf",
  published: "Veröffentlicht",
  archived: "Archiviert",
};

export const affiliateStatusOptions: { value: AffiliateStatus; label: string }[] = [
  { value: "none_found", label: "Kein Partnerprogramm gefunden" },
  { value: "found", label: "Partnerprogramm gefunden" },
  { value: "application_pending", label: "Bewerbung ausstehend" },
  { value: "approved", label: "Freigeschaltet" },
  { value: "active", label: "Affiliate-Link aktiv" },
  { value: "disabled", label: "Affiliate-Link deaktiviert" },
];

export function pricingLabel(value: PricingModel) {
  return pricingOptions.find((item) => item.value === value)?.label ?? value;
}

export function affiliateStatusLabel(value: AffiliateStatus) {
  return affiliateStatusOptions.find((item) => item.value === value)?.label ?? value;
}

export function pricingFromParam(param: string | undefined): PricingModel | "" {
  if (!param) return "";
  return pricingOptions.find((item) => item.param === param)?.value ?? "";
}

export function sortFromParam(param: string | undefined): SortKey {
  return sortOptions.find((item) => item.param === param)?.value ?? "newest";
}

export function pricingParam(value: PricingModel | "") {
  if (!value) return "";
  return pricingOptions.find((item) => item.value === value)?.param ?? "";
}

export function sortParam(value: SortKey) {
  return sortOptions.find((item) => item.value === value)?.param ?? "neueste";
}
