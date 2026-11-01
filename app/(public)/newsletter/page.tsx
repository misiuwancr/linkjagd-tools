import type { Metadata } from "next";
import { NewsletterForm } from "@/components/newsletter-form";
import { newsletterOpen } from "@/lib/newsletter";

export const metadata: Metadata = {
  title: "Newsletter-Archiv",
  description: "Bisher verschickte Ausgaben von Linkjagd Tools. Solange keine Ausgabe existiert, bleibt die Seite leer.",
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
      <p className="mt-3 text-muted-foreground">Noch keine Ausgabe verschickt. Eine Anmeldung gilt erst nach dem Bestätigungslink.</p>
      <div className="mt-8">
        <NewsletterForm notice={searchParams.hinweis} returnTo="/newsletter" open={newsletterOpen()} />
      </div>
    </div>
  );
}
