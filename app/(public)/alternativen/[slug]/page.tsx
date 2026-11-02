import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { JsonLd } from "@/components/json-ld";
import { ToolCard } from "@/components/tool-card";
import { alternativeIntro, isAlternativeSlug } from "@/lib/alternatives";
import { getToolBySlug, listAlternativePool } from "@/lib/tools/repository";
import { toPublicTool, type PublicTool } from "@/lib/tools/public";

export const revalidate = 60;

function split(items: PublicTool[]) {
  return {
    free: items.filter((item) => item.pricingModel === "free"),
    openSource: items.filter((item) => item.licenseType === "open_source"),
    rest: items.filter((item) => item.pricingModel !== "free" && item.licenseType !== "open_source"),
  };
}

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  if (!isAlternativeSlug(params.slug)) return { title: "Alternativen" };
  const tool = await getToolBySlug(await getDb(), params.slug);
  if (!tool || tool.publishStatus !== "published" || tool.isExample) return { title: "Alternativen" };
  const title = `Alternativen zu ${tool.name} | ${siteConfig.name}`;
  return {
    title: title.length <= 65 ? title : `Alternativen: ${tool.name}`,
    description: alternativeIntro(tool.name, tool.categories[0]?.name),
    alternates: { canonical: `/alternativen/${tool.slug}` },
  };
}

export default async function AlternativesPage({ params }: { params: { slug: string } }) {
  if (!isAlternativeSlug(params.slug)) notFound();
  const database = await getDb();
  const record = await getToolBySlug(database, params.slug);
  if (!record || record.publishStatus !== "published" || record.isExample) notFound();
  const tool = toPublicTool(record);
  const pool = (await listAlternativePool(database, record)).map((item) => toPublicTool(item));
  const groups = split(pool);
  const intro = alternativeIntro(tool.name, tool.categories[0]?.name);

  return (
    <div className="page-wrap py-10 sm:py-14">
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "CollectionPage",
          name: `Alternativen zu ${tool.name}`,
          description: intro,
          inLanguage: "de",
          url: new URL(`/alternativen/${tool.slug}`, siteConfig.url).toString(),
        }}
      />
      <nav aria-label="Brotkrumen" className="text-sm text-muted-foreground">
        <Link href="/tools" className="hover:text-foreground">Alle Tools</Link>
        <span aria-hidden="true"> / </span>
        <Link href={`/tools/${tool.slug}`} className="hover:text-foreground">{tool.name}</Link>
        <span aria-hidden="true"> / </span>
        <span className="text-foreground">Alternativen</span>
      </nav>
      <h1 className="mt-4 text-4xl font-bold tracking-tight sm:text-5xl">Alternativen zu {tool.name}</h1>
      <p className="mt-4 max-w-3xl text-base leading-7 text-muted-foreground">{intro}</p>
      <p className="mt-3 text-sm">
        <Link href={`/tools/${tool.slug}`} className="underline">Zurück zu {tool.name}</Link>
      </p>
      <Group source={"/alternativen/" + tool.slug} title="Kostenlose Alternativen" tools={groups.free} empty="In derselben Kategorie ist gerade kein kostenloses Tool veröffentlicht." />
      <Group source={"/alternativen/" + tool.slug} title="Open Source" tools={groups.openSource} empty="In derselben Kategorie ist gerade kein Open-Source-Programm veröffentlicht." />
      <Group source={"/alternativen/" + tool.slug} title="Weitere Tools aus der Kategorie" tools={groups.rest} empty="Keine weiteren veröffentlichten Tools in derselben Kategorie." />
    </div>
  );
}

function Group({ title, tools, empty, source }: { title: string; tools: PublicTool[]; empty: string; source: string }) {
  return (
    <section className="mt-12">
      <h2 className="text-2xl font-bold tracking-tight">{title}</h2>
      {tools.length === 0 ? (
        <p className="mt-3 text-sm text-muted-foreground">{empty}</p>
      ) : (
        <div className="mt-4 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {tools.map((item) => (
            <ToolCard key={item.id} tool={item} source={source} position="alternatives" />
          ))}
        </div>
      )}
    </section>
  );
}
