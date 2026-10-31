import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Kontakt",
  description: "Kontakt zur Redaktion von Linkjagd Tools.",
  alternates: { canonical: "/kontakt" },
};

export default function ContactPage() {
  return (
    <article className="page-wrap max-w-3xl py-12 sm:py-16">
      <h1 className="text-4xl font-semibold tracking-tight">Kontakt</h1>
      <p className="mt-4 text-muted-foreground">
        Eine erreichbare Adresse wird hier eingesetzt, sobald sie feststeht. Es ist absichtlich keine E-Mail erfunden.
      </p>
      <p className="mt-6 rounded-2xl bg-[#F8E7DC] px-4 py-3 text-sm">[PLATZHALTER: E-Mail-Adresse der Redaktion]</p>
      <p className="mt-6 text-sm leading-6">
        Tool-Vorschläge laufen über <a className="underline" href="/einreichen">Tool einreichen</a> und bleiben Entwürfe.
      </p>
    </article>
  );
}
