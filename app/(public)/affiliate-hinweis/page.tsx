import type { Metadata } from "next";
import { LegalDocument } from "@/components/legal";
import { siteConfig } from "@/site.config";

export const metadata: Metadata = {
  title: "Affiliate-Hinweis",
  description: "Wie Partnerlinks auf Linkjagd Tools gekennzeichnet sind.",
  alternates: { canonical: "/affiliate-hinweis" },
};

export default function AffiliatePage() {
  return <LegalDocument {...siteConfig.legal.affiliate} />;
}
