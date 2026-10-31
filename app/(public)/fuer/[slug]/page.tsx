import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { JsonLd } from "@/components/json-ld";
import { ToolGrid, ResultMeta, Pagination } from "@/components/directory";
import { getUseCase, USE_CASES } from "@/lib/use-cases";
import { listTools } from "@/lib/tools/repository";
import { publicListQuery } from "@/lib/tools/query";
import { toPublicTool } from "@/lib/tools/public";

export const revalidate = 60;

export function generateStaticParams() {
  return USE_CASES.map((item) => ({ slug: item.slug }));
}

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const useCase = getUseCase(params.slug);
  if (!useCase) return { title: "Sammlung" };
  return {
    title: useCase.title,
    description: useCase.intro.slice(0, 180),
    alternates: { canonical: `/fuer/${useCase.slug}` },
  };
}

export default async function UseCasePage({
  params,
  searchParams,
}: {
  params: { slug: string };
  searchParams: Record<string, string | string[] | undefined>;
}) {
  const useCase = getUseCase(params.slug);
  if (!useCase) notFound();
  const query = publicListQuery(searchParams, {
    categorySlug: useCase.categorySlug,
    pricing: useCase.pricing,
    license: useCase.license,
  });
  const result = await listTools(await getDb(), query);
  const tools = result.items.map((tool) => toPublicTool(tool));
  const url = new URL(`/fuer/${useCase.slug}`, siteConfig.url).toString();
  return (
    <div className="page-wrap py-10 sm:py-14">
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "FAQPage",
          mainEntity: useCase.faqs.map((faq) => ({
            "@type": "Question",
            name: faq.question,
            acceptedAnswer: { "@type": "Answer", text: faq.answer },
          })),
        }}
      />
      <nav aria-label="Brotkrumen" className="text-sm text-muted-foreground">
        <Link href="/fuer" className="hover:text-foreground">Sammlungen</Link>
        <span aria-hidden="true"> / </span>
        <span className="text-foreground">{useCase.title}</span>
      </nav>
      <h1 className="mt-4 text-4xl font-bold tracking-tight sm:text-5xl">{useCase.title}</h1>
      <p className="mt-4 max-w-3xl text-base leading-7 text-muted-foreground">{useCase.intro}</p>
      <p className="mt-6 text-sm text-muted-foreground">
        <ResultMeta page={result.page} pageSize={query.pageSize} total={result.total} />
      </p>
      <div className="mt-4">
        <ToolGrid tools={tools} />
      </div>
      <Pagination query={{ ...query, page: result.page }} total={result.total} basePath={`/fuer/${useCase.slug}`} />
      <section className="mt-14 max-w-3xl">
        <h2 className="text-2xl font-bold tracking-tight">Fragen</h2>
        <div className="mt-4 space-y-4">
          {useCase.faqs.map((faq) => (
            <article key={faq.question} className="rounded-2xl border border-border bg-card p-4">
              <h3 className="font-semibold">{faq.question}</h3>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">{faq.answer}</p>
            </article>
          ))}
        </div>
      </section>
      <p className="sr-only">{url}</p>
    </div>
  );
}
