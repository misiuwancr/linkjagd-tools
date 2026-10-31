import type { PricingModel } from "@/db/schema";

export function toolMetaTitle(name: string) {
  const full = `${name}: Was kann es? Preis, Open Source & Alternativen | Linkjagd Tools`;
  if (full.length <= 65) return full;
  const mid = `${name}: Preis & Alternativen | Linkjagd Tools`;
  if (mid.length <= 65) return mid;
  const short = `${name} | Linkjagd Tools`;
  if (short.length <= 65) return short;
  return `${name.slice(0, 48).trim()} | Linkjagd Tools`;
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
