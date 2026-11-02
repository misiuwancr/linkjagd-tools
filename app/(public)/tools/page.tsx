import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { Pagination, ResultMeta, ToolGrid } from "@/components/directory";
import { JsonLd } from "@/components/json-ld";
import { listCategories, listTools, totalClicks } from "@/lib/tools/repository";
import { weeklyPopularVisible } from "@/lib/tools/popular";
import { directoryHref, publicListQuery } from "@/lib/tools/query";
import { toPublicTool } from "@/lib/tools/public";
import { ActiveDirectoryFilters, DirectorySearch } from "@/components/directory-search";
import { companyBySlug } from "@/lib/companies";
import { indexingPolicy, robotsDirective } from "@/lib/indexing";
import Link from "next/link";
import { PartnerBanner } from "@/components/partner-banner";

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
  const hasFilters = !!(query.q || query.categorySlug || query.pricing || query.license || query.company || query.featuredOnly || query.fromVideo || query.germanUi || query.noSignup || query.linkjagdVideo || query.videoSearch);
  const [result, categories, clicks, all, recommended] = await Promise.all([
    listTools(database, query),
    listCategories(database),
    totalClicks(database),
    listTools(database, publicListQuery({}, { pageSize: 1 })),
    hasFilters ? Promise.resolve(null) : listTools(database, publicListQuery({}, { featuredOnly: true, sort: "featured", pageSize: 6 })),
  ]);
  const showPopular = weeklyPopularVisible(clicks);
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
      <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
        {companyBySlug(safeQuery.company) ? (
          <>Tools von {companyBySlug(safeQuery.company)?.name}</>
        ) : (
          <>
            <span className="text-hunt">Tools & Websites</span> entdecken
          </>
        )}
      </h1>
      <p className="mt-3 max-w-2xl text-base leading-7 text-muted-foreground">
        Interessante Websites, KI-Tools, Browser-Games und Software für Kreativität, Alltag und Business. Suche nach Namen oder Aufgabe und grenze deine Auswahl ein.
      </p>
      <div className="mt-8"><DirectorySearch key={directoryHref("/tools", safeQuery)} query={safeQuery} categories={categories.filter((category) => category.toolCount > 0 || query.categorySlugs.includes(category.slug))} showPopular={showPopular} toolCount={all.total} /></div>
      <ActiveDirectoryFilters query={safeQuery} categories={categories} />
      {recommended?.items.length ? <section className="mt-8" aria-label="Gerade empfohlen">
        <div className="flex items-center justify-between gap-3"><h2 className="text-xl font-bold">Gerade empfohlen</h2><Link href="/top-20" className="text-sm text-hunt">Zu den Top 20 →</Link></div>
        <div className="mt-3 grid gap-2 sm:grid-cols-3 xl:grid-cols-6">{recommended.items.map((tool) => <Link key={tool.id} href={`/tools/${tool.slug}`} className="rounded-xl border border-border bg-card p-4 font-semibold hover:border-hunt/40">{tool.name}</Link>)}</div>
      </section> : null}
      <PartnerBanner database={database} slot="directory" />
      <div className="mt-6 flex items-center justify-between gap-3">
        <ResultMeta page={safeQuery.page} pageSize={query.pageSize} total={result.total} />
        {tools.some((tool) => tool.isExample) ? (
          <p className="text-xs text-muted-foreground">Beispiel-Karten sind keine echten Angebote.</p>
        ) : null}
      </div>
      <div className="mt-4">
        <ToolGrid tools={tools} resetHref="/tools" />
      </div>
      <Pagination query={safeQuery} total={result.total} basePath="/tools" />
    </div>
  );
}
