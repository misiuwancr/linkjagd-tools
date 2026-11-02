import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { JsonLd } from "@/components/json-ld";
import { DirectoryFilters, LicenseChips, Pagination, PriceChips, ResultMeta, ToolGrid } from "@/components/directory";
import { categoryIntro, copyFor, wordCount } from "@/lib/category-copy";
import { getCategoryBySlug, listCategories, listTools } from "@/lib/tools/repository";
import { publicListQuery } from "@/lib/tools/query";
import { toPublicTool } from "@/lib/tools/public";

export const revalidate = 60;

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const category = await getCategoryBySlug(await getDb(), params.slug);
  if (!category) return { title: "Kategorie nicht gefunden" };
  const copy = copyFor(category.slug);
  const title = `${category.name}: Tools, Preise und Alternativen`;
  return {
    title: title.length <= 65 ? title : category.name,
    description: copy ? categoryIntro(category.name, copy.focus).slice(0, 180) : category.description || `Werkzeuge in der Kategorie ${category.name}.`,
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
  const copy = copyFor(category.slug);
  const intro = copy ? categoryIntro(category.name, copy.focus) : "";
  const recommended = await listTools(database, { ...query, featuredOnly: true, sort: "featured", page: 1, pageSize: 6 });
  const picks = recommended.items.map((tool) => toPublicTool(tool));
  return (
    <div className="page-wrap py-12 sm:py-16">
      {copy ? (
        <JsonLd
          data={{
            "@context": "https://schema.org",
            "@type": "FAQPage",
            mainEntity: copy.faqs.map((faq) => ({
              "@type": "Question",
              name: faq.question,
              acceptedAnswer: { "@type": "Answer", text: faq.answer },
            })),
          }}
        />
      ) : null}
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">Kategorie</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight">{category.name}</h1>
      {intro ? <p className="mt-4 max-w-3xl text-base leading-7 text-muted-foreground">{intro}</p> : null}
      {picks.length > 0 ? (
        <section className="mt-10">
          <h2 className="text-2xl font-bold tracking-tight">Unsere Empfehlungen</h2>
          <p className="mt-2 text-sm text-muted-foreground">Nur Tools, die die Redaktion als empfohlen markiert hat.</p>
          <div className="mt-4">
            <ToolGrid source={basePath} tools={picks} />
          </div>
        </section>
      ) : null}
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
        <ToolGrid source={basePath} tools={tools} />
      </div>
      <Pagination query={safeQuery} total={result.total} basePath={basePath} />
      {copy ? (
        <section className="mt-14 max-w-3xl">
          <h2 className="text-2xl font-bold tracking-tight">Fragen</h2>
          <div className="mt-4 space-y-4">
            {copy.faqs.map((faq) => (
              <article key={faq.question} className="rounded-2xl border border-border bg-card p-4">
                <h3 className="font-semibold">{faq.question}</h3>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">{faq.answer}</p>
              </article>
            ))}
          </div>
        </section>
      ) : null}
      <p className="sr-only">{wordCount(intro)} Wörter, {siteConfig.name}</p>
    </div>
  );
}
