import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Glossar",
  description: "Kurze Erklärungen der Wörter, die Linkjagd Tools auf den Karten verwendet.",
  alternates: { canonical: "/glossar" },
};

const entries = [
  ["Freemium", "Es gibt einen kostenlosen Einstieg. Weitere Funktionen können Geld kosten. Der genaue Preis steht beim Anbieter."],
  ["Kostenlos", "Im Verzeichnis ist das Preismodell als kostenlos hinterlegt. Das ist keine Garantie, dass jede Funktion dauerhaft ohne Bezahlung bleibt."],
  ["Open Source", "Die Lizenz ist als OSI-konform bestätigt. Steht dort unbekannt, ist die Lizenz nicht geprüft."],
  ["Partnerlink", "Ein gekennzeichneter Link über /go, nur wenn ein Affiliate-Link aktiv ist. Sonst führt /go zur offiziellen Website."],
  ["Empfohlen", "Die Redaktion hat das Tool markiert. Das ist keine Nutzerwertung."],
  ["Unklar", "Deutsch oder Anmeldung sind noch nicht an der offiziellen Seite belegt."],
];

export default function GlossaryPage() {
  return (
    <div className="page-wrap max-w-3xl py-12 sm:py-16">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">Wörter</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">Glossar</h1>
      <dl className="mt-8 space-y-6">
        {entries.map(([term, text]) => (
          <div key={term}>
            <dt className="text-xl font-bold">{term}</dt>
            <dd className="mt-2 text-muted-foreground">{text}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
