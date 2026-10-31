import type { Metadata } from "next";
import { Outfit } from "next/font/google";
import { siteConfig } from "@/site.config";
import "./globals.css";

const outfit = Outfit({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-outfit",
});

export const metadata: Metadata = {
  metadataBase: new URL(siteConfig.url),
  title: {
    default: siteConfig.seo.title,
    template: `%s · ${siteConfig.name}`,
  },
  description: siteConfig.seo.description,
  applicationName: siteConfig.name,
  openGraph: {
    type: "website",
    locale: "de_DE",
    siteName: siteConfig.name,
    title: siteConfig.seo.title,
    description: siteConfig.seo.description,
  },
  robots: { index: true, follow: true },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="de">
      <body className={`${outfit.className} min-h-screen antialiased`}>{children}</body>
    </html>
  );
}
