import { siteConfig } from "@/site.config";
import type { PricingModel } from "@/db/schema";

export function toolMetaTitle(name: string) {
  const full = `${name}: Was kann es? Preis, Open Source & Alternativen | ${siteConfig.name}`;
  if (full.length <= 65) return full;
  const mid = `${name}: Preis & Alternativen | ${siteConfig.name}`;
  if (mid.length <= 65) return mid;
  const short = `${name} | ${siteConfig.name}`;
  if (short.length <= 65) return short;
  return `${name.slice(0, 48).trim()} | ${siteConfig.name}`;
}

export function softwareOffer(pricing: PricingModel) {
  if (pricing !== "free") return null;
  return {
    "@type": "Offer",
    price: "0",
    priceCurrency: "EUR",
    description: "Kostenlos",
  };
}
