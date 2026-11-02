import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Kontakt",
  description: "Kontakt und Tool-Vorschläge für Linkjagd Tools.",
  alternates: { canonical: "/kontakt" },
  robots: { index: false, follow: false },
};

export default function ContactPage() {
  return (
    <article className="page-wrap max-w-3xl py-12 sm:py-16">
      <h1 className="text-4xl font-bold tracking-tight">Kontakt</h1>
      <p className="mt-4 text-muted-foreground">
        Eine direkte E-Mail-Kontaktadresse ist derzeit nicht veröffentlicht. Tool-Vorschläge kannst du über das Einreichungsformular senden.
      </p>
      <p className="mt-6 text-sm leading-6">
        Tool-Vorschläge laufen über <a className="underline" href="/einreichen">Tool einreichen</a> und bleiben Entwürfe.
      </p>
    </article>
  );
}
