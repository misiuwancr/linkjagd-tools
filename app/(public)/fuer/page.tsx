import type { Metadata } from "next";
import Link from "next/link";
import { USE_CASES } from "@/lib/use-cases";

export const metadata: Metadata = {
  title: "Sammlungen",
  description: "Kuratierte Tool-Sammlungen für konkrete Aufgaben, ohne erfundene Ranglisten.",
  alternates: { canonical: "/fuer" },
};

export default function UseCaseIndexPage() {
  return (
    <div className="page-wrap py-12 sm:py-16">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">Sammlungen</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">Wofür ein Tool herhalten soll</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Jede Sammlung filtert veröffentlichte Einträge nach Kategorie, Preis oder Lizenz. Es gibt keine Stimmen und keine Platzierung.
      </p>
      <ul className="mt-8 grid gap-3 sm:grid-cols-2">
        {USE_CASES.map((item) => (
          <li key={item.slug}>
            <Link href={`/fuer/${item.slug}`} className="block rounded-2xl border border-border bg-card px-4 py-4 hover:border-hunt/40">
              <span className="font-semibold">{item.title}</span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
