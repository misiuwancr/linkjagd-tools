import Link from "next/link";
import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { JsonLd } from "@/components/json-ld";
import { CategoryIcon } from "@/components/category-icon";
import { NewsletterForm } from "@/components/newsletter-form";
import { ToolCard } from "@/components/tool-card";
import { listCategories, listCompaniesInDirectory, listHomepageFresh, listTools, listTopTools, listWeeklyPopular, socialProofText } from "@/lib/tools/repository";
import { CompanyStrip } from "@/components/company-strip";
import { toPublicTool } from "@/lib/tools/public";
import { publicListQuery } from "@/lib/tools/query";
import { utcDay } from "@/lib/utils";
import { newsletterOpen } from "@/lib/newsletter";
import { AiNewsSection } from "@/components/ai-news";
import { listPublishedNews } from "@/lib/tools/repository";
import { TopToolsSidebar } from "@/components/top-tools-sidebar";
import { comparisonHref, comparisons } from "@/lib/comparisons";

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
  const [featured, newest, fromVideos, categories, popular, proof, top, companies, business] = await Promise.all([
    listTools(database, { ...base, manualRecommendationsOnly: true, sort: "alpha", pageSize: 6 }),
    listHomepageFresh(database, 6),
    listTools(database, { ...base, linkjagdOnly: true, sort: "alpha", pageSize: 6 }),
    listCategories(database),
    listWeeklyPopular(database, utcDay(since), 6),
    socialProofText(database),
    listTopTools(database, 20),
    listCompaniesInDirectory(database),
    listTools(database, publicListQuery({ kategorie: ["e-commerce", "business-finanzen", "business", "finanzen"] }, { pageSize: 6, sort: "alpha" })),
  ]);
  const siteHost = host();
  const featuredTools = featured.items.map((tool) => toPublicTool(tool, siteHost));
  const newTools = newest.map((tool) => toPublicTool(tool, siteHost));
  const videoTools = fromVideos.items.map((tool) => toPublicTool(tool, siteHost));
  const popularTools = popular.map((tool) => toPublicTool(tool, siteHost));
  const topTools = top.map((tool) => toPublicTool(tool, siteHost));
  const blog = await listPublishedNews(database, 3);

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
            Gute Websites. <span className="text-hunt">Passende Tools.</span>
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-muted-foreground">
            Entdecke interessante Websites, KI-Tools, Browser-Games und kreative Anwendungen. Für Alltag und Produktivität – und für klare Entscheidungen bei Business-Software.
          </p>
          <div className="mt-6 flex flex-wrap gap-3"><Link href="/linkjagd" className="rounded-full bg-primary px-5 py-3 font-semibold text-primary-foreground">Bekannt aus Linkjagd →</Link><Link href="/tools" className="rounded-full border border-border px-5 py-3 font-semibold">Alle Tools entdecken</Link></div>
          <nav aria-label="Was möchtest du erreichen?" className="mt-8 grid gap-4 md:grid-cols-3">
            {[
              { title: "Onlineshop aufbauen", text: "Shopify oder WooCommerce? Kläre Einrichtung, Erweiterungen und technische Betreuung.", comparison: comparisons[1], cta: "Shop-Systeme vergleichen" },
              { title: "Marketing automatisieren", text: "Wähle einen Newsletter-Dienst nach Versandaufgabe und geplanten Kontaktstrecken.", comparison: comparisons[2], cta: "Newsletter-Tools vergleichen" },
              { title: "Geschäftsprozesse automatisieren", text: "Finde den passenden Ansatz für Datenübergaben zwischen deinen Anwendungen.", comparison: comparisons[0], cta: "Zapier, Make und n8n vergleichen" },
            ].map((task) => <Link href={comparisonHref(task.comparison)} key={task.title} className="rounded-2xl border border-border bg-card p-5 transition hover:border-hunt/50"><h2 className="text-xl font-bold">{task.title}</h2><p className="mt-3 text-sm leading-7 text-muted-foreground">{task.text}</p><span className="mt-4 block text-sm font-semibold text-hunt">{task.cta} →</span></Link>)}
          </nav>
          <p className="mt-6 text-sm"><Link href="/vergleiche" className="font-semibold text-hunt underline">Alle Entscheidungshilfen</Link><span className="px-2 text-muted-foreground">·</span><Link href="/tools" className="text-muted-foreground underline">Alle Tools durchsuchen</Link></p>
          <form action="/tools" method="get" className="mt-8 flex max-w-2xl flex-col gap-2 sm:flex-row" role="search">
            <label htmlFor="start-suche" className="sr-only">
              Tools durchsuchen
            </label>
            <input id="start-suche" name="q" placeholder="Zum Beispiel Shop, Newsletter oder Automatisierung" className="field h-12" />
            <button type="submit" className="h-12 rounded-xl bg-primary px-6 text-sm font-semibold text-primary-foreground">
              Suchen
            </button>
          </form>
          <CompanyStrip companies={companies} />
        </div>
      </section>

      {videoTools.length > 0 ? (
        <section className="border-y border-border bg-card">
          <div className="page-wrap py-14">
            <SectionHead kicker="Kanal" title="Bekannt aus Linkjagd" href="/linkjagd" linkLabel="Nach Video suchen" />
            <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
              Die tatsächlich zugeordneten Tools aus unseren Videos – auffindbar nach Videotitel, Kennung und Teilnummer.
            </p>
            <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
              {videoTools.map((tool) => (
                <ToolCard key={tool.id} tool={tool} source="/" />
              ))}
            </div>
          </div>
        </section>
      ) : <section className="page-wrap py-10"><SectionHead kicker="Kanal" title="Bekannt aus Linkjagd" href="/linkjagd" linkLabel="Videos durchsuchen" /><p className="mt-3 text-muted-foreground">Du suchst eine Website aus einem unserer Videos? <Link href="/linkjagd" className="text-hunt underline">Zur Videosammlung →</Link></p></section>}

      {featuredTools.length > 0 ? (
        <section className="page-wrap py-10">
          <SectionHead kicker="Redaktion" title="Unsere Empfehlungen" href="/empfehlungen" linkLabel="Alle Empfehlungen" />
          <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {featuredTools.map((tool) => <ToolCard key={tool.id} tool={tool} source="/" />)}
          </div>
        </section>
      ) : <section className="page-wrap py-10"><SectionHead kicker="Redaktion" title="Unsere Empfehlungen" href="/empfehlungen" linkLabel="Zur Auswahl" /><p className="mt-3 text-muted-foreground">Persönliche Auswahl statt Beliebtheits-Ranking. <Link href="/tools" className="underline">Im gesamten Verzeichnis stöbern →</Link></p></section>}

      <section className="page-wrap grid gap-10 py-6 lg:grid-cols-[minmax(0,1fr)_320px]">
        <div className="min-w-0">
          <SectionHead kicker="Frisch" title="Neu hinzugefügt" href="/neu" linkLabel="Alle neuen Tools" />
          <p className="mt-3 text-sm text-muted-foreground">Nach belegtem Veröffentlichungsdatum. Import- und Änderungsdaten zählen nicht als neue Veröffentlichung.</p>
          <div className="mt-4 grid gap-3">
            {!newTools.length ? <Link href="/tools" className="rounded-2xl border border-border bg-card p-5 text-sm font-semibold text-hunt">Alle vorhandenen Tools entdecken →</Link> : null}
            {newTools.map((tool) => (
              <ToolCard key={tool.id} tool={tool} source="/" />
            ))}
          </div>
        </div>
        <TopToolsSidebar database={database} tools={topTools} />
      </section>

      {newsletterOpen() ? (
      <section className="border-t border-border">
        <div className="page-wrap py-10">
          <h2 className="text-2xl font-bold tracking-tight">Hinweise per Mail</h2>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
            Neue Hinweise von Linkjagd direkt in dein Postfach.
          </p>
          <div className="mt-6">
            <NewsletterForm notice={searchParams.hinweis} returnTo="/" open={newsletterOpen()} />
          </div>
        </div>
      </section>
      ) : null}

      <section className="page-wrap border-y border-border py-12"><SectionHead kicker="Vergleichen & entscheiden" title="Tools für Business & E-Commerce" href="/vergleiche" linkLabel="Zu den Vergleichen" /><p className="mt-3 text-sm leading-7 text-muted-foreground">Software für Shops und Unternehmensaufgaben. Unsere Vergleiche helfen bei der Auswahl; das breite Verzeichnis bleibt für alle Themen offen.</p><div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">{business.items.map((tool) => <ToolCard key={tool.id} tool={toPublicTool(tool, siteHost)} source="/" />)}</div><Link href="/tools?kategorie=e-commerce&kategorie=business-finanzen&kategorie=finanzen" className="mt-6 inline-block text-sm font-semibold text-hunt">Business-Tools durchsuchen →</Link></section>

      {popularTools.length > 0 ? (
        <section className="page-wrap py-14">
          <SectionHead kicker="Weiterleitungen" title="Beliebt diese Woche" href="/tools?sort=beliebteste" linkLabel="Nach Klicks sortieren" />
          <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
            Häufig aufgerufene Anbieter in den letzten sieben Tagen.
          </p>
          <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {popularTools.map((tool) => (
              <ToolCard key={tool.id} tool={tool} source="/" />
            ))}
          </div>
        </section>
      ) : null}

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
      <AiNewsSection />
      <section className="page-wrap border-t border-border py-14">
        <SectionHead kicker="Redaktion" title="Aus dem Blog" href="/blog" linkLabel="Alle Beiträge →" />
        {blog.length ? <div className="mt-6 grid gap-4 md:grid-cols-3">{blog.map((post) => <Link href={`/blog/${post.slug}`} key={post.id} className="rounded-2xl border border-border bg-card p-5"><h3 className="text-xl font-bold">{post.title}</h3><p className="mt-3 text-sm text-muted-foreground">{post.excerpt}</p></Link>)}</div> : <p className="mt-5 text-muted-foreground">Noch keine Beiträge veröffentlicht.</p>}
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
    <div className="flex flex-wrap items-end justify-between gap-4">
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
