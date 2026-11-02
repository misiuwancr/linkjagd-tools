import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { Pagination, ResultMeta, ToolGrid } from "@/components/directory";
import { listTools } from "@/lib/tools/repository";
import { publicListQuery } from "@/lib/tools/query";
import { toPublicTool } from "@/lib/tools/public";
export const revalidate = 60;
export const metadata: Metadata = { title: "Unsere Empfehlungen", description: "Manuell von Linkjagd ausgewählte Tools und Websites, alphabetisch dargestellt.", alternates: { canonical: "/empfehlungen" } };
export default async function RecommendationsPage({ searchParams }: { searchParams: Record<string, string | string[] | undefined> }) {
  const query = publicListQuery(searchParams, { manualRecommendationsOnly: true, sort: "alpha" });
  const result = await listTools(await getDb(), query);
  return <div className="page-wrap py-12"><h1 className="text-4xl font-bold">Unsere Empfehlungen</h1><p className="mt-4 max-w-2xl leading-7 text-muted-foreground">Manuell von der Redaktion markierte Websites und Tools. Alphabetisch angeordnet, ohne Upvote-Rangliste. Ein Partnerstatus entscheidet nicht über die Auswahl.</p><div className="mt-7"><ResultMeta page={result.page} pageSize={query.pageSize} total={result.total} /></div><div className="mt-4"><ToolGrid source="/empfehlungen" tools={result.items.map((tool) => toPublicTool(tool))} resetHref="/tools" /></div><Pagination query={{ ...query, page: result.page }} total={result.total} basePath="/empfehlungen" /></div>;
}
