import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { Pagination, ResultMeta, ToolGrid } from "@/components/directory";
import { publicListQuery } from "@/lib/tools/query";
import { listTools } from "@/lib/tools/repository";
import { toPublicTool } from "@/lib/tools/public";

export const revalidate = 60;

export const metadata: Metadata = {
  title: "Neu hinzugefügt",
  description: "Die zuletzt veröffentlichten Tools und Websites mit belegtem Veröffentlichungsdatum.",
  alternates: { canonical: "/neu" },
};

export default async function NewPage({
  searchParams,
}: {
  searchParams: Record<string, string | string[] | undefined>;
}) {
  const query = publicListQuery(searchParams, { sort: "newest", q: "", categorySlug: "", pricing: "", datedOnly: true });
  const result = await listTools(await getDb(), query);
  const tools = result.items.map((tool) => toPublicTool(tool));
  const safeQuery = { ...query, page: result.page };
  return (
    <div className="page-wrap py-12 sm:py-16">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">Frisch</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">Neu hinzugefügt</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">Sortiert nach dem belegten Veröffentlichungsdatum im Verzeichnis. Ein Importdatum ist kein Veröffentlichungsdatum. Einträge ohne belegtes Datum bleiben im vollständigen Verzeichnis erreichbar.</p>
      <div className="mt-8">
        <ResultMeta page={safeQuery.page} pageSize={query.pageSize} total={result.total} />
      </div>
      <div className="mt-4">
        <ToolGrid tools={tools} resetHref="/tools" />
      </div>
      <Pagination query={safeQuery} total={result.total} basePath="/neu" />
    </div>
  );
}
