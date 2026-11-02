import type { Metadata } from "next";
import { siteConfig } from "@/site.config";

export const metadata: Metadata = {
  title: "Über uns",
  description: `${siteConfig.name} ist das KI-Verzeichnis zum TikTok-Kanal @linkjagd.`,
  alternates: { canonical: "/ueber-uns" },
};

export default function AboutPage() {
  return (
    <article className="page-wrap max-w-3xl py-12 sm:py-16">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">{siteConfig.name}</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">Über uns</h1>
      <div className="mt-6 space-y-4 text-base leading-8">
        <p>
          {siteConfig.name} sammelt KI-Tools für Alltag, Arbeit und Projekte. Hinter dem Verzeichnis steht {siteConfig.creator.name}. Auf TikTok stellt er unter {siteConfig.creator.channel} Websites und Werkzeuge vor.
        </p>
        <p>
          Empfohlene Tools erscheinen auf der Startseite nur, wenn die Redaktion ein Tool ausdrücklich markiert. Es gibt keine erfundenen Bewertungen, Nutzerzahlen oder Testimonials. Anbieter-Buttons erscheinen nur mit gültigem aktivem Partnerlink und sind als Werbung gekennzeichnet.
        </p>
        <p>
          <a href={siteConfig.creator.channelUrl} rel="me noopener noreferrer" className="font-medium underline">
            TikTok-Kanal {siteConfig.creator.channel}
          </a>
        </p>
      </div>
    </article>
  );
}
