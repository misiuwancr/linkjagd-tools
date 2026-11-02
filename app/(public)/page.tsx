import Link from "next/link";
import type { Metadata } from "next";
import { getDb } from "@/db/client";
import { siteConfig } from "@/site.config";
import { JsonLd } from "@/components/json-ld";
import { NewsletterForm } from "@/components/newsletter-form";
import { newsletterOpen } from "@/lib/newsletter";
import { AiNewsCards } from "@/components/ai-news";
import { publishedAiNews } from "@/lib/ai-news";
import { TopToolsSidebar } from "@/components/top-tools-sidebar";
import { listTopTools } from "@/lib/tools/repository";
import { toPublicTool } from "@/lib/tools/public";
import { comparisonHref, comparisons } from "@/lib/comparisons";

export const revalidate = 60;
export const metadata: Metadata = { title: { absolute: siteConfig.seo.title }, description: siteConfig.seo.description, alternates: { canonical: "/" } };
export default async function HomePage({ searchParams }: { searchParams: { hinweis?: string } }) {
  const database = await getDb();
  const top = (await listTopTools(database, 20)).map((tool) => toPublicTool(tool, new URL(siteConfig.url).hostname));
  const open = newsletterOpen();
  return <>
    <JsonLd data={{ "@context": "https://schema.org", "@type": "WebSite", name: siteConfig.name, url: siteConfig.url, inLanguage: "de", potentialAction: { "@type": "SearchAction", target: siteConfig.url + "/tools?q={query}", "query-input": "required name=query" } }} />
    <section className="relative overflow-hidden border-b border-border bg-[radial-gradient(ellipse_at_top_left,rgba(208,255,40,0.1),transparent_65%)]">
      <div className="page-wrap grid gap-10 py-16 sm:py-24 lg:grid-cols-[1.2fr_1fr] lg:items-center">
        <div><p className="text-xs font-semibold uppercase tracking-[0.18em] text-hunt">Der {siteConfig.name} Newsletter</p><h1 className="mt-4 max-w-3xl text-5xl font-bold tracking-tight sm:text-7xl">{siteConfig.tagline}</h1><p className="mt-6 max-w-xl text-lg leading-8 text-muted-foreground">KI-News, interessante Websites und digitale Werkzeuge. Verständlich eingeordnet, damit du schneller findest, was dir weiterhilft.</p><div className="mt-7 flex flex-wrap gap-4"><Link href="/tools" className="rounded-full bg-primary px-6 py-3 font-semibold text-primary-foreground">Alle Tools entdecken →</Link><Link href="/linkjagd" className="rounded-full border border-border px-6 py-3 font-semibold">Bekannt aus Linkjagd</Link></div></div>
        <div className="rounded-3xl border border-hunt/30 bg-card p-6 sm:p-8"><span className="text-3xl text-hunt" aria-hidden="true">✳</span><h2 className="mt-5 text-2xl font-bold">Das Web hat viel zu bieten.<br />Behalte den Überblick.</h2><p className="mt-4 text-sm leading-7 text-muted-foreground">Unser Newsletter bündelt neue Entdeckungen und Entwicklungen aus der KI-Welt – direkt in deinem Postfach.</p><div className="mt-6">{open ? <NewsletterForm open notice={searchParams.hinweis} returnTo="/" compact /> : <p className="rounded-xl border border-border bg-secondary/50 p-4 text-sm leading-6" role="status"><strong className="block">Die Anmeldung ist noch geschlossen.</strong>Bis zum Start findest du neue Meldungen hier auf der Website. Es werden keine E-Mail-Adressen erfasst.</p>}</div><Link href="/newsletter" className="mt-5 inline-block text-sm text-muted-foreground underline">Mehr zum Newsletter</Link></div>
      </div>
    </section>
    <div className="page-wrap grid gap-12 py-14 lg:grid-cols-[minmax(0,1fr)_320px]"><section aria-labelledby="ki-news-heading"><div className="flex flex-wrap items-end justify-between gap-4"><div><p className="text-xs font-semibold uppercase tracking-widest text-hunt">Wissen, was sich bewegt</p><h2 id="ki-news-heading" className="mt-2 text-3xl font-bold">Neues aus der KI-Welt</h2></div><Link href="/news" className="text-sm font-semibold text-hunt">Alle News →</Link></div><p className="mt-3 leading-7 text-muted-foreground">Redaktionell zusammengefasst. Mit Datum und direktem Link zur Originalquelle.</p><AiNewsCards news={publishedAiNews().slice(0, 6)} /></section><TopToolsSidebar database={database} tools={top} /></div>
    <section className="border-t border-border bg-secondary/20"><div className="page-wrap py-14"><p className="text-xs font-semibold uppercase tracking-widest text-hunt">Software für dein Business</p><h2 className="mt-2 text-3xl font-bold">Vergleichen &amp; Entscheiden</h2><p className="mt-4 max-w-2xl leading-7 text-muted-foreground">Welche Anwendung passt zu deinem Vorhaben? Vergleiche Funktionen, Einsatzgebiete und Grenzen, bevor du dich entscheidest.</p><div className="mt-8 grid gap-5 md:grid-cols-3">{comparisons.slice(0, 3).map((comparison) => <Link key={comparison.slug} href={comparisonHref(comparison)} className="rounded-2xl border border-border bg-card p-6 transition hover:border-hunt/60"><h3 className="text-xl font-bold">{comparison.title}</h3><span className="mt-6 block text-sm font-semibold text-hunt">Zum Vergleich →</span></Link>)}</div><Link href="/vergleiche" className="mt-6 inline-block text-sm font-semibold text-hunt">Alle Vergleiche →</Link>
      <nav aria-label="Themen für dein Business" className="mt-10 grid gap-6 md:grid-cols-3">{[
        { title: "Onlineshop aufbauen", text: "Shop-Systeme nach Einrichtung, Erweiterungen und technischer Betreuung auswählen.", comparison: comparisons[1] },
        { title: "Marketing automatisieren", text: "Newsletter und Kontaktstrecken passend zu deinem Versandvorhaben planen.", comparison: comparisons[2] },
        { title: "Geschäftsprozesse automatisieren", text: "Anwendungen verbinden und wiederkehrende Datenübergaben vereinfachen.", comparison: comparisons[0] },
      ].map((theme) => <Link href={comparisonHref(theme.comparison)} key={theme.title} className="border-l-2 border-hunt/60 pl-5"><h3 className="font-bold">{theme.title} →</h3><p className="mt-2 text-sm leading-7 text-muted-foreground">{theme.text}</p></Link>)}</nav>
    </div></section>
  </>;
}
