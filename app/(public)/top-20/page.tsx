import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { ToolGrid } from "@/components/directory";
import { listTopTools } from "@/lib/tools/repository";
import { toPublicTool } from "@/lib/tools/public";

export const revalidate = 60;

export const metadata: Metadata = {
  title: "Top 20 Tools",
  description: "Zwanzig veröffentlichte Tools, sortiert nach der Redaktionsreihenfolge, nicht nach Stimmen.",
  alternates: { canonical: "/top-20" },
};

export default async function Top20Page() {
  const tools = (await listTopTools(await getDb(), 20)).map((tool) => toPublicTool(tool));
  return (
    <div className="page-wrap py-12 sm:py-16">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">Auswahl</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">Top 20 Tools</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Nur veröffentlichte Tools mit einer Zahl im Feld editorial_rank. Die Redaktion setzt die Reihenfolge im Admin. Fehlt die Zahl, erscheint das Tool hier nicht. Es gibt keine Stimmen und keine aufgefüllten Plätze.
      </p>
      {tools.length === 0 ? (
        <p className="mt-8 rounded-2xl border border-dashed border-border bg-card p-6 text-sm">Noch keine Redaktionsreihenfolge gesetzt.</p>
      ) : null}
      <div className="mt-8">
        <ToolGrid tools={tools} />
      </div>
    </div>
  );
}
