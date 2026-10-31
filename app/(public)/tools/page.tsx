import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { DirectoryFilters, LicenseChips, Pagination, PriceChips, ResultMeta, ToolGrid } from "@/components/directory";
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
      <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
        Das <span className="text-hunt">Verzeichnis</span>
      </h1>
      <p className="mt-3 max-w-2xl text-base leading-7 text-muted-foreground">
        Suche nach Namen oder Aufgabe. Filter und Sortierung bleiben in der Adresse, damit du die Ansicht teilen kannst.
      </p>
      <div className="mt-8 rounded-3xl border border-border bg-card/60 p-4 sm:p-5">
        <PriceChips query={safeQuery} basePath="/tools" />
        <LicenseChips query={safeQuery} basePath="/tools" />
        <div className="mt-3">
          <a
            href={safeQuery.fromVideo ? "/tools" : "/tools?video=ja"}
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
            href="/tools?deutsch=ja"
            className={
              safeQuery.germanUi === "ja"
                ? "ml-2 inline-flex h-9 items-center rounded-full bg-primary px-3 text-sm font-medium text-primary-foreground"
                : "ml-2 inline-flex h-9 items-center rounded-full border border-border bg-card px-3 text-sm font-medium"
            }
          >
            Auf Deutsch
          </a>
          <a
            href="/tools?anmeldung=ja"
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
          <DirectoryFilters query={safeQuery} categories={categories} />
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
