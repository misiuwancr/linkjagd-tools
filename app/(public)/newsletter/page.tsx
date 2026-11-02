import Link from "next/link";
import type { Metadata } from "next";
import { NewsletterForm } from "@/components/newsletter-form";
import { newsletterOpen } from "@/lib/newsletter";

export const metadata: Metadata = {
  title: "Newsletter-Archiv",
  description: "Informationen zum Newsletter von Linkjagd Tools.",
  alternates: { canonical: "/newsletter" },
};

export default function NewsletterArchivePage({
  searchParams,
}: {
  searchParams: { hinweis?: string };
}) {
  return (
    <div className="page-wrap max-w-3xl py-12 sm:py-16">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">Mail</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">Newsletter-Archiv</h1>
      <p className="mt-3 text-muted-foreground">{newsletterOpen() ? "Eine Anmeldung gilt erst nach dem Bestätigungslink." : "Der Newsletter ist derzeit nicht verfügbar. Aktuelle Beiträge findest du im Blog."}</p>
      <Link href="/blog" className="mt-6 inline-block font-semibold text-hunt underline">Zum Blog →</Link>
      <div className="mt-8">
        <NewsletterForm notice={searchParams.hinweis} returnTo="/newsletter" open={newsletterOpen()} />
      </div>
    </div>
  );
}
