import type { Metadata } from "next";
import Link from "next/link";
import { getDb } from "@/db/client";
import { PriceBadge } from "@/components/badges";
import { ToolLogo } from "@/components/tool-logo";
import { publicListQuery } from "@/lib/tools/query";
import { listTools } from "@/lib/tools/repository";
import { toPublicTool } from "@/lib/tools/public";

export const revalidate = 60;

export const metadata: Metadata = {
  title: "Top 20 Tools",
  description: "Zwanzig redaktionell geordnete KI-Tools. Keine Stimmen und keine erfundenen Ranglisten.",
  alternates: { canonical: "/top-20" },
};

export default async function TopPage() {
  const query = publicListQuery({}, { rankedOnly: true, sort: "featured", page: 1, pageSize: 20 });
  const result = await listTools(await getDb(), query);
  const tools = result.items.map((tool) => toPublicTool(tool));
  return (
    <div className="page-wrap py-12 sm:py-16">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-copper">Redaktion</p>
      <h1 className="mt-3 text-4xl font-semibold tracking-tight sm:text-5xl">Top 20 Tools</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Die Zahl ist eine redaktionelle Position, kein Publikumsvotum. Tools ohne gesetzte Position erscheinen hier nicht.
      </p>
      {tools.length === 0 ? (
        <p className="mt-10 text-sm text-muted-foreground">Noch keine Positionen vergeben.</p>
      ) : (
        <ol className="mt-8 divide-y divide-border rounded-3xl border border-border bg-white">
          {tools.map((tool) => (
            <li key={tool.id} className="grid grid-cols-[2.5rem_auto_1fr] items-center gap-3 px-4 py-4 sm:px-6">
              <span className="text-sm tabular-nums text-muted-foreground">{tool.editorialRank}</span>
              <ToolLogo name={tool.name} logo={tool.logo} size={44} />
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <Link href={`/tools/${tool.slug}`} className="font-semibold tracking-tight hover:underline">
                    {tool.name}
                  </Link>
                  <PriceBadge value={tool.pricingModel} />
                </div>
                <p className="mt-1 text-sm text-muted-foreground">{tool.shortDescriptionDe}</p>
              </div>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
