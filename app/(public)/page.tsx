import Link from "next/link";
import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { JsonLd } from "@/components/json-ld";
import { CategoryIcon } from "@/components/category-icon";
import { NewsletterForm } from "@/components/newsletter-form";
import { ToolCard } from "@/components/tool-card";
import { listCategories, listTools, listTopTools, listWeeklyPopular, socialProofText } from "@/lib/tools/repository";
import { toPublicTool } from "@/lib/tools/public";
import { publicListQuery } from "@/lib/tools/query";
import { utcDay } from "@/lib/utils";

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
  const since = new Date();
  since.setUTCDate(since.getUTCDate() - 6);
  const [featured, newest, fromVideos, categories, popular, proof, top] = await Promise.all([
    listTools(database, { ...base, featuredOnly: true, sort: "featured", pageSize: 6 }),
    listTools(database, { ...base, sort: "newest", pageSize: 6 }),
    listTools(database, { ...base, fromVideo: true, sort: "newest", pageSize: 6 }),
    listCategories(database),
    listWeeklyPopular(database, utcDay(since), 6),
    socialProofText(database),
    listTopTools(database, 8),
  ]);
  const siteHost = host();
  const featuredTools = featured.items.map((tool) => toPublicTool(tool, siteHost));
  const newTools = newest.items.map((tool) => toPublicTool(tool, siteHost));
  const videoTools = fromVideos.items.map((tool) => toPublicTool(tool, siteHost));
  const popularTools = popular.map((tool) => toPublicTool(tool, siteHost));
  const topTools = top.map((tool) => toPublicTool(tool, siteHost));

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
        <div className="page-wrap relative py-16 sm:py-24">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-hunt">Kuratiert von Linkjagd</p>
          <h1 className="mt-4 max-w-4xl text-5xl font-bold tracking-tight text-foreground sm:text-7xl sm:leading-[0.95]">
            Die besten Tools. <span className="text-hunt">Alle</span> an einem Ort.
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-muted-foreground">
            Bekannt aus TikTok {siteConfig.creator.channel}. Werkzeuge für Alltag, Arbeit und Projekte, auf Deutsch erklärt.
          </p>
          <div id="anmeldung" className="mt-8 scroll-mt-24">
            <NewsletterForm notice={searchParams.hinweis} returnTo="/" />
          </div>
          {proof ? <p className="mt-4 max-w-2xl text-sm text-muted-foreground">{proof}</p> : null}
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

      {featuredTools.length > 0 ? (
        <section className="page-wrap py-10">
          <SectionHead kicker="Redaktion" title="Gerade empfohlen" href="/top-20" linkLabel="Zur Top 20" />
          <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {featuredTools.map((tool) => (
              <Link key={tool.id} href={`/tools/${tool.slug}`} className="flex items-center gap-3 rounded-2xl border border-border bg-card px-3 py-3 hover:border-hunt/40">
                <CategoryIcon slug={tool.categories[0]?.slug ?? ""} />
                <span className="font-semibold">{tool.name}</span>
              </Link>
            ))}
          </div>
        </section>
      ) : null}

      <section className="page-wrap grid gap-10 py-6 lg:grid-cols-[minmax(0,1fr)_320px]">
        <div>
          <SectionHead kicker="Frisch" title="Neu hinzugefügt" href="/neu" linkLabel="Alle neuen Tools" />
          <div className="mt-4 grid gap-3">
            {newTools.map((tool) => (
              <ToolCard key={tool.id} tool={tool} />
            ))}
          </div>
        </div>
        <aside>
          <SectionHead kicker="Reihenfolge" title="Top-Tools" href="/top-20" linkLabel="Alle 20" />
          <ol className="mt-4 divide-y divide-border rounded-2xl border border-border bg-card">
            {topTools.map((tool, index) => (
              <li key={tool.id}>
                <Link href={`/tools/${tool.slug}`} className="flex items-center gap-3 px-4 py-3 hover:bg-secondary/60">
                  <span className="w-6 text-sm text-muted-foreground">{index + 1}</span>
                  <span className="font-medium">{tool.name}</span>
                </Link>
              </li>
            ))}
          </ol>
          <p className="mt-3 text-xs leading-5 text-muted-foreground">
            Zuerst gesetzte Redaktionsreihenfolge, dann Empfehlungen, dann die neuesten. Keine Stimmen.
          </p>
        </aside>
      </section>

      {videoTools.length > 0 ? (
        <section className="border-y border-border bg-card">
          <div className="page-wrap py-14">
            <SectionHead kicker="Kanal" title="Neu aus den Videos" href="/tools?video=ja" linkLabel="Alle aus den Videos" />
            <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
              Nur Tools, bei denen eine Video-Adresse von TikTok, Instagram oder YouTube hinterlegt ist.
            </p>
            <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
              {videoTools.map((tool) => (
                <ToolCard key={tool.id} tool={tool} />
              ))}
            </div>
          </div>
        </section>
      ) : null}

      {popularTools.length > 0 ? (
        <section className="page-wrap py-14">
          <SectionHead kicker="Weiterleitungen" title="Beliebt diese Woche" href="/tools?sort=beliebteste" linkLabel="Nach Klicks sortieren" />
          <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
            Reihenfolge nach echten Klicks auf /go in den letzten sieben Tagen. Ohne genug Klicks bleibt der Block leer.
          </p>
          <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {popularTools.map((tool) => (
              <ToolCard key={tool.id} tool={tool} />
            ))}
          </div>
        </section>
      ) : null}

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
                <CategoryIcon slug={category.slug} />
                <span className="mt-3 block font-semibold tracking-tight">{category.name}</span>
                <span className="mt-1 block text-sm text-muted-foreground">
                  {category.toolCount} {category.toolCount === 1 ? "Tool" : "Tools"}
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="border-t border-border bg-card">
        <div className="page-wrap py-14">
          <h2 className="text-3xl font-bold tracking-tight">Hinweise per Mail</h2>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
            Nur nach Bestätigung. Ohne Versanddienst bleibt die Adresse unbestätigt liegen, es geht keine Mail raus.
          </p>
          <div className="mt-6">
            <NewsletterForm notice={searchParams.hinweis} returnTo="/" />
          </div>
        </div>
      </section>
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
