import Link from "next/link";
import { JsonLd } from "@/components/json-ld";
import { siteConfig } from "@/site.config";
import { comparisonHref, comparisons, decisionTools, researchDate, type Comparison } from "@/lib/comparisons";

export function ProviderCta({ slug }: { slug: string }) {
  const tool = decisionTools[slug];
  return <a href={tool.providerUrl} rel="noopener noreferrer" target="_blank" className="inline-flex min-h-11 items-center justify-center rounded-xl bg-primary px-4 py-2 text-sm font-bold text-primary-foreground">Zu {tool.name} ↗</a>;
}

export function EditorialMethod() {
  return <div className="rounded-2xl border border-border bg-card p-5 text-sm leading-6 text-muted-foreground">
    <p><strong className="text-foreground">So ordnen wir ein:</strong> Anbieterinformationen und daraus abgeleitete redaktionelle Empfehlungen, keine eigenen Produkttests, Sterne oder bezahlte Rangfolge. Partnerstatus beeinflusst diese Einordnung nicht. Die Anbieter-CTAs hier sind direkte Links ohne Affiliate-Parameter.</p>
    <p className="mt-2">Quellenstand: <time dateTime={researchDate}>2. November 2026</time>. Konkrete Preise, Tarifgrenzen, Zustellbarkeit und rechtliche Eignung sind nicht unabhängig geprüft. Bitte vor einer Buchung beim Anbieter und für deinen Anwendungsfall klären.</p>
  </div>;
}

export function SourceLinks({ slug }: { slug: string }) {
  return <ul className="mt-2 space-y-2 text-sm leading-6">{decisionTools[slug].sources.map((source) => <li key={source.url}><a href={source.url} target="_blank" rel="noopener noreferrer" className="break-words underline underline-offset-4">{source.title} ↗</a></li>)}</ul>;
}

export function ComparisonCards() {
  return <div className="mt-5 grid gap-4 md:grid-cols-3">{comparisons.map((item) => <Link href={comparisonHref(item)} key={item.slug} className="rounded-2xl border border-border bg-card p-5 transition hover:border-hunt/50">
    <p className="text-xs font-semibold uppercase tracking-widest text-hunt">{item.topic}</p><h2 className="mt-3 text-xl font-bold">{item.title}</h2><p className="mt-3 text-sm leading-6 text-muted-foreground">{item.intro}</p><span className="mt-4 block text-sm font-semibold text-hunt">Vergleich ansehen →</span>
  </Link>)}</div>;
}

export function ComparisonPage({ comparison }: { comparison: Comparison }) {
  return <article className="page-wrap min-w-0 py-10 sm:py-16">
    <JsonLd data={{ "@context": "https://schema.org", "@type": "Article", headline: comparison.title, description: comparison.intro, inLanguage: "de", url: new URL(comparisonHref(comparison), siteConfig.url).toString(), dateModified: researchDate }} />
    <nav aria-label="Brotkrumen" className="flex flex-wrap gap-2 text-sm text-muted-foreground"><Link href="/">Start</Link><span aria-hidden="true">/</span><Link href="/vergleiche">Vergleiche</Link><span aria-hidden="true">/</span><span>{comparison.topic}</span></nav>
    <header className="mt-6 max-w-4xl"><p className="text-sm font-semibold text-hunt">Entscheidungshilfe · {comparison.topic}</p><h1 className="mt-3 text-4xl font-bold tracking-tight sm:text-6xl">{comparison.title}</h1><p className="mt-5 text-lg leading-8 text-muted-foreground">{comparison.intro}</p></header>
    <div className="mt-7"><EditorialMethod /></div>
    <section className="mt-10" aria-labelledby="zielgruppen"><h2 id="zielgruppen" className="text-2xl font-bold">Welche Lösung passt zu deiner Situation?</h2>
      <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">{comparison.recommendations.map((item) => <div className="rounded-2xl border border-border bg-card p-5" key={item.situation}>
        <h3 className="text-lg font-semibold">{item.situation}</h3><p className="mt-3 text-sm leading-6 text-muted-foreground">{item.reason}</p><div className="mt-4"><ProviderCta slug={item.tool} /></div>
      </div>)}</div>
    </section>
    <section className="mt-12" aria-labelledby="vergleich"><h2 id="vergleich" className="text-2xl font-bold">Die Unterschiede auf einen Blick</h2>
      <p id="tabellen-hinweis" className="mt-3 text-sm text-muted-foreground">Auf kleinen Bildschirmen die Tabelle seitlich wischen oder fokussieren und mit den Pfeiltasten verschieben. Ausführliche Einordnungen folgen darunter.</p>
      <div role="region" aria-label="Vergleichstabelle" aria-describedby="tabellen-hinweis" tabIndex={0} className="mt-4 max-w-full overflow-x-auto rounded-2xl border border-border focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">
        <table className="w-full min-w-[720px] table-fixed border-collapse text-left text-sm leading-6">
          <caption className="sr-only">{comparison.title}: gemeinsame Entscheidungskriterien</caption>
          <thead><tr><th scope="col" className="sticky left-0 z-10 w-36 border-b border-border bg-card p-4 sm:w-44">Kriterium</th>{comparison.tools.map((slug) => <th scope="col" key={slug} className="border-b border-border bg-card p-4"><Link href={`/tools/${slug}`} className="font-bold text-hunt underline underline-offset-4">{decisionTools[slug].name}</Link></th>)}</tr></thead>
          <tbody>{comparison.rows.map((row) => <tr key={row.label}><th scope="row" className="sticky left-0 z-10 border-b border-border bg-card p-4 align-top font-semibold">{row.label}</th>{row.values.map((value, index) => <td key={comparison.tools[index]} className="border-b border-border bg-background p-4 align-top text-muted-foreground">{value}</td>)}</tr>)}</tbody>
          <tfoot><tr><th scope="row" className="sticky left-0 bg-card p-4">Nächster Schritt</th>{comparison.tools.map((slug) => <td key={slug} className="p-4 align-top"><ProviderCta slug={slug} /><Link href={`/tools/${slug}`} className="mt-3 block underline">Tool-Profil lesen</Link></td>)}</tr></tfoot>
        </table>
      </div>
    </section>
    <section className="mt-12" aria-labelledby="abwägung"><h2 id="abwägung" className="text-2xl font-bold">Stärken und Grenzen</h2><div className="mt-5 grid gap-5 lg:grid-cols-3">{comparison.tools.map((slug) => {
      const tool = decisionTools[slug];
      return <section key={slug} className="rounded-2xl border border-border bg-card p-5"><h3 className="text-xl font-bold">{tool.name}</h3><p className="mt-3 text-sm leading-6 text-muted-foreground">{tool.summary}</p>
        <h4 className="mt-5 font-semibold">Stärken für diese Aufgabe</h4><TextList items={tool.strengths} /><h4 className="mt-5 font-semibold">Grenzen und Aufwand</h4><TextList items={tool.weaknesses} />
        <Link href={`/tools/${slug}`} className="mt-5 block font-semibold text-hunt">Einsatzfälle und Alternativen →</Link><h4 className="mt-5 text-sm font-semibold">Anbieterquellen</h4><SourceLinks slug={slug} />
      </section>;
    })}</div></section>
    <section className="mt-12 max-w-4xl rounded-2xl border border-hunt/40 bg-card p-6"><h2 className="text-2xl font-bold">Vor deiner Entscheidung selbst prüfen</h2><TextList items={comparison.checklist} /><p className="mt-4 text-sm text-muted-foreground">Diese Punkte sind noch nicht für dein Unternehmen verifiziert. Nutze eine kleine Testaufgabe, bevor du Verträge abschließt oder produktive Daten überträgst.</p></section>
    <nav aria-label="Weitere Vergleiche" className="mt-10 flex flex-wrap gap-4">{comparisons.filter((item) => item.slug !== comparison.slug).map((item) => <Link className="text-sm font-semibold text-hunt underline" href={comparisonHref(item)} key={item.slug}>{item.title} →</Link>)}<Link href="/tools" className="text-sm underline">Gesamtes Tool-Verzeichnis</Link></nav>
  </article>;
}

export function TextList({ items }: { items: string[] }) {
  return <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-7 text-muted-foreground">{items.map((item) => <li key={item}>{item}</li>)}</ul>;
}
