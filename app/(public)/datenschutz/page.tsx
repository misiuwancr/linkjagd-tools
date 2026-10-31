import type { Metadata } from "next";
import { LegalDocument } from "@/components/legal";
import { siteConfig } from "@/site.config";

export const metadata: Metadata = {
  title: "Datenschutz",
  description: "Hinweise dazu, welche Daten Linkjagd Tools in Phase 1 verarbeitet.",
  alternates: { canonical: "/datenschutz" },
};

export default function PrivacyPage() {
  return <LegalDocument {...siteConfig.legal.datenschutz} />;
}
