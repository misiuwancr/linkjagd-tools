import type { Metadata } from "next";
import { LegalDocument } from "@/components/legal";
import { siteConfig } from "@/site.config";

export const metadata: Metadata = {
  title: "Datenschutz",
  description: "Hinweise dazu, welche Daten Linkjagd Tools verarbeitet. Der Text ist noch nicht vollständig.",
  alternates: { canonical: "/datenschutz" },
  robots: { index: false, follow: false },
};

export default function PrivacyPage() {
  return <LegalDocument {...siteConfig.legal.datenschutz} />;
}
