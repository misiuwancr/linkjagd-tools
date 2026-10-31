import Link from "next/link";
import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { JsonLd } from "@/components/json-ld";
import { Newsletter } from "@/components/newsletter";
import { PriceBadge } from "@/components/badges";
import { ToolCard } from "@/components/tool-card";
import { ToolLogo } from "@/components/tool-logo";
import { listCategories, listPublishedNews, listTools } from "@/lib/tools/repository";
import { toPublicTool } from "@/lib/tools/public";
import { publicListQuery } from "@/lib/tools/query";

export const revalidate = 60;

export const metadata: Metadata = {
  title: siteConfig.seo.title,
  description: siteConfig.seo.description,
  alternates: { canonical: "/" },
};

function host() {
  try {
    return new URL(siteConfig.url).hostname;
  } catch {
    return undefined;
  }
}

export default async function HomePage({
  searchParams,
}: {
  searchParams: { hinweis?: string };
}) {
  const database = await getDb();
  const base = publicListQuery({});
  const [featured, newest, ranked, categories, news] = await Promise.all([
    listTools(database, { ...base, featuredOnly: true, sort: "featured", pageSize: 6 }),
    listTools(database, { ...base, sort: "newest", pageSize: 6 }),
    listTools(database, { ...base, rankedOnly: true, sort: "featured", pageSize: 20 }),
    listCategories(database),
    listPublishedNews(database, 3),
  ]);
  const siteHost = host();
  const featuredTools = featured.items.map((tool) => toPublicTool(tool, siteHost));
  const newTools = newest.items.map((tool) => toPublicTool(tool, siteHost));
  const topTools = ranked.items.map((tool) => toPublicTool(tool, siteHost));

  return (
    <>
      <JsonLd
        data={{
          "@context": "https://schema.org",
          "@type": "WebSite",
          name: siteConfig.name,
          url: siteConfig.url,
          inLanguage: "de",
          potentialAction: {
            "@type": "SearchAction",
            target: `${siteConfig.url.replace(/\/$/, "")}/tools?q={query}`,
            "query-input": "required name=query",
          },
        }}
      />
      <section className="relative overflow-hidden border-b border-border">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(520px_220px_at_18%_0%,rgba(198,245,49,0.18),transparent_70%)]" />
        <div className="page-wrap relative py-14 sm:py-20">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-hunt">Verzeichnis</p>
          <h1 className="mt-4 max-w-3xl text-4xl font-bold tracking-tight text-foreground sm:text-6xl sm:leading-[1.02]">
            {siteConfig.tagline}
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-muted-foreground">{siteConfig.description}</p>
          <form action="/tools" method="get" className="mt-8 flex max-w-2xl flex-col gap-2 sm:flex-row" role="search">
            <label htmlFor="start-suche" className="sr-only">
              Tools durchsuchen
            </label>
            <input id="start-suche" name="q" placeholder="Zum Beispiel Chat, Bild oder Recherche" className="field h-12" />
            <button type="submit" className="h-12 rounded-xl bg-primary px-6 text-sm font-semibold text-primary-foreground">
              Suchen
            </button>
          </form>
        </div>
      </section>

      <section className="page-wrap py-14">
        <SectionHead kicker="Redaktion" title="Empfohlene Tools" href="/tools?sort=empfohlen" linkLabel="Alle Empfehlungen" />
        <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {featuredTools.map((tool) => (
            <ToolCard key={tool.id} tool={tool} />
          ))}
        </div>
      </section>

      <section className="border-y border-border bg-card">
        <div className="page-wrap py-14">
          <SectionHead kicker="Auswahl" title="Top 20 Tools" href="/top-20" linkLabel="Die ganze Liste" />
          <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
            Eine redaktionelle Reihenfolge. Keine Stimmen, keine erfundenen Platzierungen.
          </p>
          <ol className="mt-6 divide-y divide-border">
            {topTools.map((tool) => (
              <li key={tool.id} className="grid grid-cols-[2.5rem_auto_1fr] items-center gap-3 py-4 sm:grid-cols-[3rem_auto_1fr_auto]">
                <span className="text-sm tabular-nums text-muted-foreground">{tool.editorialRank}</span>
                <ToolLogo name={tool.name} logo={tool.logo} size={40} />
                <div className="min-w-0">
                  <Link href={`/tools/${tool.slug}`} className="font-semibold tracking-tight hover:underline">
                    {tool.name}
                  </Link>
                  <p className="truncate text-sm text-muted-foreground">{tool.shortDescriptionDe}</p>
                </div>
                <div className="col-span-3 sm:col-span-1 sm:justify-self-end">
                  <PriceBadge value={tool.pricingModel} />
                </div>
              </li>
            ))}
          </ol>
        </div>
      </section>

      <section className="page-wrap py-14">
        <SectionHead kicker="Frisch" title="Neu hinzugefügt" href="/neu" linkLabel="Alle neuen Tools" />
        <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {newTools.map((tool) => (
            <ToolCard key={tool.id} tool={tool} />
          ))}
        </div>
      </section>

      <section className="border-t border-border bg-card">
        <div className="page-wrap py-14">
          <SectionHead kicker="Themen" title="Kategorien" href="/kategorien" linkLabel="Alle Kategorien" />
          <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {categories.map((category) => (
              <Link
                key={category.id}
                href={`/kategorien/${category.slug}`}
                className="rounded-2xl border border-border bg-background px-4 py-4 hover:border-hunt/40"
              >
                <span className="block font-semibold tracking-tight">{category.name}</span>
                <span className="mt-1 block text-sm text-muted-foreground">
                  {category.toolCount} {category.toolCount === 1 ? "Tool" : "Tools"}
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="page-wrap py-14">
        <SectionHead kicker="Später automatisch" title="KI-News" href="/blog" linkLabel="Zum Bereich" />
        {news.length === 0 ? (
          <div className="mt-6 rounded-2xl border border-dashed border-border bg-card p-6 sm:p-8">
            <p className="font-medium">Hier erscheinen später Meldungen.</p>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-muted-foreground">
              In Phase 1 wird keine Nachrichtenquelle abgefragt und kein Artikel erfunden. Der Bereich ist vorbereitet und bleibt leer, bis die Redaktion etwas freigibt oder eine erlaubte Quelle angebunden wird.
            </p>
          </div>
        ) : (
          <div className="mt-6 grid gap-4 md:grid-cols-3">
            {news.map((item) => (
              <article key={item.id} className="rounded-2xl border border-border bg-card p-5">
                <h3 className="font-semibold tracking-tight">{item.title}</h3>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">{item.excerpt}</p>
              </article>
            ))}
          </div>
        )}
      </section>
      <Newsletter notice={searchParams.hinweis === "newsletter"} />
    </>
  );
}

function SectionHead({
  kicker,
  title,
  href,
  linkLabel,
}: {
  kicker: string;
  title: string;
  href: string;
  linkLabel: string;
}) {
  return (
    <div className="flex items-end justify-between gap-4">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-hunt">{kicker}</p>
        <h2 className="mt-2 text-2xl font-bold tracking-tight sm:text-3xl">{title}</h2>
      </div>
      <Link href={href} className="shrink-0 text-sm font-medium text-muted-foreground hover:text-foreground">
        {linkLabel}
      </Link>
    </div>
  );
}
