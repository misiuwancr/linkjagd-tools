import Link from "next/link";
import type { PublicTool } from "@/lib/tools/public";
import { comparisonsForTool, comparisonHref, decisionTools } from "@/lib/comparisons";
import { EditorialMethod, ProviderCta, SourceLinks, TextList } from "@/components/comparison-page";
import { ToolLogo } from "@/components/tool-logo";
import { BookmarkButton } from "@/components/bookmark-button";
import { VideoGate } from "@/components/video-gate";
import { JsonLd } from "@/components/json-ld";
import { LinkjagdToolVideos } from "@/components/linkjagd-tool-videos";
import { siteConfig } from "@/site.config";

export function DecisionToolPage({ tool }: { tool: PublicTool }) {
  const profile = decisionTools[tool.slug];
  return <article className="page-wrap py-10 sm:py-16">
    <JsonLd data={{ "@context": "https://schema.org", "@type": "SoftwareApplication", name: tool.name, description: profile.summary, url: new URL(`/tools/${tool.slug}`, siteConfig.url).toString(), inLanguage: "de" }} />
    <nav aria-label="Brotkrumen" className="flex gap-2 text-sm text-muted-foreground"><Link href="/">Start</Link><span>/</span><Link href="/tools">Alle Tools</Link><span>/</span><span>{tool.name}</span></nav>
    <header className="mt-7 grid gap-6 lg:grid-cols-[minmax(0,1fr)_320px]"><div><div className="flex flex-col items-start gap-4 sm:flex-row"><ToolLogo name={tool.name} logo={tool.logo} size={72} /><div className="min-w-0"><h1 className="text-4xl font-bold sm:text-5xl">{tool.name}</h1><p className="mt-4 max-w-3xl text-lg leading-8 text-muted-foreground">{profile.summary}</p></div></div><div className="mt-5 flex flex-wrap items-center gap-4"><ProviderCta slug={tool.slug} /><BookmarkButton slug={tool.slug} /></div></div>
      <aside className="rounded-2xl border border-border bg-card p-5"><h2 className="font-bold">Geeignet für</h2><p className="mt-3 text-sm leading-7 text-muted-foreground">{profile.audience}</p><p className="mt-4 text-xs leading-6 text-muted-foreground">Kosten, Lizenzbedingungen und genaue Tariffunktionen beim Anbieter prüfen. Keine pauschale Bewertung oder Datenschutz-Zusage.</p></aside></header>
    <LinkjagdToolVideos tool={tool} />
    <div className="mt-8"><EditorialMethod /></div>
    <div className="mt-10 grid gap-8 lg:grid-cols-2"><section><h2 className="text-2xl font-bold">Konkrete Einsatzfälle</h2><TextList items={profile.useCases} /><p className="mt-3 text-xs text-muted-foreground">Beispielaufgaben zur eigenen Prüfung, keine von uns durchgeführten Produkttests.</p></section><section><h2 className="text-2xl font-bold">Passender Vergleich</h2>{comparisonsForTool(tool.slug).map((item) => <Link key={item.slug} href={comparisonHref(item)} className="mt-4 block rounded-2xl border border-border bg-card p-5 font-semibold text-hunt">{item.title} →</Link>)}</section><section><h2 className="text-2xl font-bold">Stärken</h2><TextList items={profile.strengths} /></section><section><h2 className="text-2xl font-bold">Schwächen und Prüfbedarf</h2><TextList items={profile.weaknesses} /></section></div>
    <section className="mt-10"><h2 className="text-2xl font-bold">Alternativen je nach Anforderung</h2><div className="mt-4 grid gap-4 md:grid-cols-2">{profile.alternatives.map((slug) => <Link key={slug} href={`/tools/${slug}`} className="rounded-2xl border border-border bg-card p-5"><h3 className="font-bold text-hunt">{decisionTools[slug].name} →</h3><p className="mt-2 text-sm leading-7 text-muted-foreground">{decisionTools[slug].audience}</p></Link>)}</div></section>
    {tool.videos.length ? <section className="mt-10"><h2 className="text-2xl font-bold">Vorhandene Videos</h2><div className="mt-4 grid gap-4 sm:grid-cols-2">{tool.videos.map((video) => <VideoGate key={video.platform} video={video} />)}</div></section> : null}
    <section className="mt-10"><h2 className="text-2xl font-bold">Quellen und nächster Schritt</h2><SourceLinks slug={tool.slug} /><div className="mt-5"><ProviderCta slug={tool.slug} /></div></section>
  </article>;
}
