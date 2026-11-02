import type { Metadata } from "next";
import { ComparisonCards, EditorialMethod } from "@/components/comparison-page";
export const metadata: Metadata = { title: "Tools vergleichen: E-Commerce, Marketing und Automatisierung", description: "Entscheidungshilfen mit gemeinsamen Kriterien, Zielgruppen und nachvollziehbaren Grenzen.", alternates: { canonical: "/vergleiche" } };
export default function ComparisonsPage() {
  return <div className="page-wrap py-12 sm:py-16"><h1 className="max-w-4xl text-4xl font-bold sm:text-6xl">Welches Tool passt zu deiner Aufgabe?</h1><p className="mt-5 max-w-3xl text-lg leading-8 text-muted-foreground">Vergleiche Lösungen für deinen Shop, dein Marketing und wiederkehrende Geschäftsprozesse. Keine pauschalen Testsieger: Entscheidend sind Anforderungen und Aufwand.</p><ComparisonCards /><div className="mt-8"><EditorialMethod /></div></div>;
}
