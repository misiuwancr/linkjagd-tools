import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { CategoryChips, DirectoryFilters, LicenseChips, Pagination, PriceChips, ResultMeta, ToolGrid } from "@/components/directory";
import { JsonLd } from "@/components/json-ld";
import { listCategories, listTools, totalClicks } from "@/lib/tools/repository";
import { weeklyPopularVisible } from "@/lib/tools/popular";
import { directoryHref, publicListQuery } from "@/lib/tools/query";
import { toPublicTool } from "@/lib/tools/public";
import { sortOptions } from "@/lib/labels";
import { companyBySlug } from "@/lib/companies";
import { indexingPolicy, robotsDirective } from "@/lib/indexing";

export const revalidate = 60;

export async function generateMetadata({
  searchParams,
}: {
  searchParams: Record<string, string | string[] | undefined>;
}): Promise<Metadata> {
  const query = publicListQuery(searchParams);
  const company = companyBySlug(query.company);
  const title = company ? `Tools von ${company.name}` : query.q ? `Suche: ${query.q}` : "Alle KI-Tools";
  const description = query.q
    ? `Suchergebnisse für „${query.q}“ im Verzeichnis ${siteConfig.name}.`
    : "Durchsuche das Verzeichnis nach Name, Beschreibung, Kategorie und Preismodell.";
  const canonical = new URL("/tools", siteConfig.url);
  if (query.categorySlug) canonical.searchParams.set("kategorie", query.categorySlug);
  if (query.pricing) canonical.searchParams.set("preis", searchParams.preis as string);
  if (query.company) canonical.searchParams.set("firma", query.company);
  if (query.sort !== "newest") {
    const sort = sortOptions.find((item) => item.value === query.sort)?.param;
    if (sort) canonical.searchParams.set("sort", sort);
  }
  return {
    title,
    description,
    alternates: { canonical: canonical.pathname + canonical.search },
    robots: robotsDirective(indexingPolicy().index && !query.q),
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
            Das <span className="text-hunt">Verzeichnis</span>
          </>
        )}
      </h1>
      <p className="mt-3 max-w-2xl text-base leading-7 text-muted-foreground">
        Suche nach Namen oder Aufgabe. Filter und Sortierung bleiben in der Adresse, damit du die Ansicht teilen kannst.
      </p>
      <div className="mt-8 rounded-3xl border border-border bg-card/60 p-4 sm:p-5">
        <CategoryChips query={safeQuery} categories={categories} basePath="/tools" />
        <div className="mt-3">
          <PriceChips query={safeQuery} basePath="/tools" />
        </div>
        <LicenseChips query={safeQuery} basePath="/tools" />
        <div className="mt-3">
          <a
            href={directoryHref("/tools", safeQuery, { fromVideo: !safeQuery.fromVideo, page: 1 })}
            className={
              safeQuery.fromVideo
                ? "inline-flex h-9 items-center rounded-full bg-primary px-3 text-sm font-medium text-primary-foreground"
                : "inline-flex h-9 items-center rounded-full border border-border bg-card px-3 text-sm font-medium"
            }
            aria-current={safeQuery.fromVideo ? "true" : undefined}
          >
            Aus meinen Videos
          </a>
          <a
            href={directoryHref("/tools", safeQuery, { germanUi: "ja", page: 1 })}
            className={
              safeQuery.germanUi === "ja"
                ? "ml-2 inline-flex h-9 items-center rounded-full bg-primary px-3 text-sm font-medium text-primary-foreground"
                : "ml-2 inline-flex h-9 items-center rounded-full border border-border bg-card px-3 text-sm font-medium"
            }
          >
            Auf Deutsch
          </a>
          <a
            href={directoryHref("/tools", safeQuery, { noSignup: "ja", page: 1 })}
            className={
              safeQuery.noSignup === "ja"
                ? "ml-2 inline-flex h-9 items-center rounded-full bg-primary px-3 text-sm font-medium text-primary-foreground"
                : "ml-2 inline-flex h-9 items-center rounded-full border border-border bg-card px-3 text-sm font-medium"
            }
          >
            Ohne Anmeldung
          </a>
        </div>
        <div className="mt-4">
          <DirectoryFilters query={safeQuery} categories={categories} showPopular={showPopular} />
        </div>
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
