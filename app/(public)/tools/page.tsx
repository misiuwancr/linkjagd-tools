import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { DirectoryFilters, Pagination, PriceChips, ResultMeta, ToolGrid } from "@/components/directory";
import { JsonLd } from "@/components/json-ld";
import { listCategories, listTools } from "@/lib/tools/repository";
import { publicListQuery } from "@/lib/tools/query";
import { toPublicTool } from "@/lib/tools/public";
import { sortOptions } from "@/lib/labels";

export const revalidate = 60;

export async function generateMetadata({
  searchParams,
}: {
  searchParams: Record<string, string | string[] | undefined>;
}): Promise<Metadata> {
  const query = publicListQuery(searchParams);
  const title = query.q ? `Suche: ${query.q}` : "Alle KI-Tools";
  const description = query.q
    ? `Suchergebnisse für „${query.q}“ im Verzeichnis ${siteConfig.name}.`
    : "Durchsuche das Verzeichnis nach Name, Beschreibung, Kategorie und Preismodell.";
  const canonical = new URL("/tools", siteConfig.url);
  if (query.categorySlug) canonical.searchParams.set("kategorie", query.categorySlug);
  if (query.pricing) canonical.searchParams.set("preis", searchParams.preis as string);
  if (query.sort !== "newest") {
    const sort = sortOptions.find((item) => item.value === query.sort)?.param;
    if (sort) canonical.searchParams.set("sort", sort);
  }
  return {
    title,
    description,
    alternates: { canonical: canonical.pathname + canonical.search },
    robots: query.q ? { index: false, follow: true } : { index: true, follow: true },
  };
}

export default async function ToolsPage({
  searchParams,
}: {
  searchParams: Record<string, string | string[] | undefined>;
}) {
  const query = publicListQuery(searchParams);
  const database = await getDb();
  const [result, categories] = await Promise.all([listTools(database, query), listCategories(database)]);
  const tools = result.items.map((tool) => toPublicTool(tool));
  const safeQuery = { ...query, page: result.page };

  return (
    <div className="page-wrap py-10 sm:py-14">
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "CollectionPage",
          name: "Alle KI-Tools",
          isPartOf: siteConfig.name,
          inLanguage: "de",
        }}
      />
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-copper">Verzeichnis</p>
      <h1 className="mt-3 text-4xl font-semibold tracking-tight sm:text-5xl">Alle Tools</h1>
      <p className="mt-3 max-w-2xl text-base leading-7 text-muted-foreground">
        Suche im Namen, in der Beschreibung und in der Kategorie. Filter und Sortierung stehen in der Adresse, damit du eine Ansicht teilen kannst.
      </p>
      <div className="mt-8">
        <PriceChips query={safeQuery} basePath="/tools" />
      </div>
      <div className="mt-3">
        <DirectoryFilters query={safeQuery} categories={categories} />
      </div>
      <div className="mt-6 flex items-center justify-between gap-3">
        <ResultMeta page={safeQuery.page} pageSize={query.pageSize} total={result.total} />
        {tools.some((tool) => tool.isExample) ? (
          <p className="text-xs text-muted-foreground">Beispiel-Karten sind keine echten Angebote.</p>
        ) : null}
      </div>
      <div className="mt-4">
        <ToolGrid tools={tools} />
      </div>
      <Pagination query={safeQuery} total={result.total} basePath="/tools" />
    </div>
  );
}
