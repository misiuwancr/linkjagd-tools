import type { Metadata } from "next";
import { LegalDocument } from "@/components/legal";
import { siteConfig } from "@/site.config";

export const metadata: Metadata = {
  title: "Affiliate-Hinweis",
  description: `Wie Partnerlinks auf ${siteConfig.name} gekennzeichnet sind. Einzelne Angaben fehlen noch.`,
  alternates: { canonical: "/affiliate-hinweis" },
  robots: { index: false, follow: false },
};

export default function AffiliatePage() {
  return <LegalDocument {...siteConfig.legal.affiliate} />;
}
