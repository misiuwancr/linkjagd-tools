import type { Metadata } from "next";
import { JsonLd } from "@/components/json-ld";

export const metadata: Metadata = {
  title: "FAQ",
  description: "Häufige Fragen zum Verzeichnis Linkjagd Tools.",
  alternates: { canonical: "/faq" },
};

const faqs = [
  ["Wer wählt die Tools aus?", "Die Redaktion von Linkjagd. Eine Markierung Empfohlen ist eine redaktionelle Entscheidung, keine Abstimmung."],
  ["Sind die Beschreibungen vom Anbieter?", "Nein. Die kurzen deutschen Texte schreibt die Redaktion. Sie sind keine Werbetexte der Firmen."],
  ["Was passiert beim Klick auf Testen?", "Der Browser geht über /go zur offiziellen Website oder, wenn ein Partnerlink aktiv ist, zu diesem Link. Anzeige steht nur im zweiten Fall."],
  ["Kostet mich ein Partnerlink extra?", "Dafür ist hier kein Aufpreis hinterlegt. Konkrete Sätze stehen nicht im Verzeichnis."],
  ["Kann ich ein Tool vorschlagen?", "Ja, über Tool einreichen. Der Vorschlag bleibt ein Entwurf, bis ihn jemand prüft."],
];

export default function FaqPage() {
  return (
    <div className="page-wrap max-w-3xl py-12 sm:py-16">
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "FAQPage",
          mainEntity: faqs.map(([question, answer]) => ({
            "@type": "Question",
            name: question,
            acceptedAnswer: { "@type": "Answer", text: answer },
          })),
        }}
      />
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">Fragen</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">FAQ</h1>
      <div className="mt-8 space-y-4">
        {faqs.map(([question, answer]) => (
          <article key={question} className="rounded-2xl border border-border bg-card p-5">
            <h2 className="text-xl font-bold">{question}</h2>
            <p className="mt-2 text-muted-foreground">{answer}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
