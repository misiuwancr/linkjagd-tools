import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { Pagination, ResultMeta, ToolGrid } from "@/components/directory";
import { JsonLd } from "@/components/json-ld";
import { listCategories, listTools, totalClicks } from "@/lib/tools/repository";
import { weeklyPopularVisible } from "@/lib/tools/popular";
import { directoryHref, publicListQuery } from "@/lib/tools/query";
import { toPublicTool } from "@/lib/tools/public";
import { DirectorySearch } from "@/components/directory-search";
import { companyBySlug } from "@/lib/companies";
import { indexingPolicy, robotsDirective } from "@/lib/indexing";
import Link from "next/link";
import { sortOptions } from "@/lib/labels";

export const revalidate = 60;

export async function generateMetadata({
  searchParams,
}: {
  searchParams: Record<string, string | string[] | undefined>;
}): Promise<Metadata> {
  const query = publicListQuery(searchParams);
  const company = companyBySlug(query.company);
  const title = company ? `Tools von ${company.name}` : query.q ? `Suche: ${query.q}` : "Tools & Websites entdecken";
  const description = query.q
    ? `Suchergebnisse für „${query.q}“ im Verzeichnis ${siteConfig.name}.`
    : "Durchsuche das Verzeichnis nach Name, Beschreibung, Kategorie und Preismodell.";
  const canonical = directoryHref("/tools", query);
  return {
    title,
    description,
    alternates: { canonical: canonical },
    robots: robotsDirective(indexingPolicy().index && !query.q && query.categorySlugs.length <= 1),
  };
}

export default async function ToolsPage({
  searchParams,
}: {
  searchParams: Record<string, string | string[] | undefined>;
}) {
  const query = publicListQuery(searchParams);
  const database = await getDb();
  const [result, categories, clicks] = await Promise.all([
    listTools(database, query),
    listCategories(database),
    totalClicks(database),
  ]);
  const showPopular = weeklyPopularVisible(clicks);
  const tools = result.items.map((tool) => toPublicTool(tool));
  const safeQuery = { ...query, page: result.page };

  return (
    <div className="page-wrap py-4 sm:py-6">
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "CollectionPage",
          name: "Alle KI-Tools",
          isPartOf: siteConfig.name,
          inLanguage: "de",
        }}
      />
      <h1 className="sr-only">Alle Tools</h1>
      <DirectorySearch key={directoryHref("/tools", safeQuery)} query={safeQuery} categories={categories} />
      <div className="mt-6 flex items-center justify-between gap-3">
        <ResultMeta page={safeQuery.page} pageSize={query.pageSize} total={result.total} />
        {tools.some((tool) => tool.isExample) ? (
          <p className="text-xs text-muted-foreground">Beispiel-Karten sind keine echten Angebote.</p>
        ) : null}
      </div>
      <nav aria-label="Ergebnisse sortieren" className="mt-4 flex flex-wrap gap-2">{sortOptions.filter((sort) => showPopular || sort.value !== "popular").map((sort) => <Link key={sort.value} href={directoryHref("/tools", safeQuery, { sort: sort.value, page: 1 })} aria-current={safeQuery.sort === sort.value ? "true" : undefined} className={`rounded-full border px-4 py-2 text-sm ${safeQuery.sort === sort.value ? "border-hunt bg-hunt/10 text-hunt" : "border-border hover:border-hunt/50"}`}>{sort.value === "alpha" ? "A–Z" : sort.label}</Link>)}</nav>
      <div className="mt-4">
        <ToolGrid tools={tools} resetHref="/tools" />
      </div>
      <Pagination query={safeQuery} total={result.total} basePath="/tools" />
    </div>
  );
}
