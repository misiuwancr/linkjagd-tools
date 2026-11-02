import type { Metadata } from "next";
import { LegalDocument } from "@/components/legal";
import { siteConfig } from "@/site.config";

export const metadata: Metadata = {
  title: "Impressum",
  description: `Anbieterangaben zu ${siteConfig.name}; derzeit noch unvollständig.`,
  alternates: { canonical: "/impressum" },
  robots: { index: false, follow: false },
};

export default function ImpressumPage() {
  return <LegalDocument {...siteConfig.legal.impressum} />;
}
