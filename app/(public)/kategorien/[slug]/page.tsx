import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getDb } from "@/db/client";
import { DirectoryFilters, LicenseChips, Pagination, PriceChips, ResultMeta, ToolGrid } from "@/components/directory";
import { getCategoryBySlug, listCategories, listTools } from "@/lib/tools/repository";
import { publicListQuery } from "@/lib/tools/query";
import { toPublicTool } from "@/lib/tools/public";

export const revalidate = 60;

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const category = await getCategoryBySlug(await getDb(), params.slug);
  if (!category) return { title: "Kategorie nicht gefunden" };
  return {
    title: category.name,
    description: category.description || `KI-Tools in der Kategorie ${category.name}.`,
    alternates: { canonical: `/kategorien/${category.slug}` },
  };
}

export default async function CategoryPage({
  params,
  searchParams,
}: {
  params: { slug: string };
  searchParams: Record<string, string | string[] | undefined>;
}) {
  const database = await getDb();
  const category = await getCategoryBySlug(database, params.slug);
  if (!category) notFound();
  const query = publicListQuery(searchParams, { categorySlug: category.slug });
  const [result, categories] = await Promise.all([listTools(database, query), listCategories(database)]);
  const tools = result.items.map((tool) => toPublicTool(tool));
  const safeQuery = { ...query, page: result.page };
  const basePath = `/kategorien/${category.slug}`;
  return (
    <div className="page-wrap py-12 sm:py-16">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">Kategorie</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">{category.name}</h1>
      {category.description ? <p className="mt-3 max-w-2xl text-muted-foreground">{category.description}</p> : null}
      <div className="mt-8">
        <PriceChips query={safeQuery} basePath={basePath} />
        <LicenseChips query={safeQuery} basePath={basePath} />
      </div>
      <div className="mt-3">
        <DirectoryFilters query={query} categories={categories} action="/tools" />
      </div>
      <div className="mt-6">
        <ResultMeta page={safeQuery.page} pageSize={query.pageSize} total={result.total} />
      </div>
      <div className="mt-4">
        <ToolGrid tools={tools} />
      </div>
      <Pagination query={safeQuery} total={result.total} basePath={basePath} />
    </div>
  );
}
