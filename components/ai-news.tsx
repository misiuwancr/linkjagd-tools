import Image from "next/image";
import Link from "next/link";
import { publishedAiNews, type AiNews } from "@/lib/ai-news";

export function AiNewsCards({ news }: { news: AiNews[] }) {
  if (!news.length) return <p className="mt-6 rounded-2xl border border-dashed border-border p-6 text-muted-foreground">Noch keine KI-News veröffentlicht. Neue Meldungen erscheinen hier nach redaktioneller Prüfung.</p>;
  return <ul className="mt-6 grid gap-5 md:grid-cols-2 xl:grid-cols-3">{news.map((item) => <li key={item.id}>
    <article className="h-full overflow-hidden rounded-2xl border border-border bg-card transition-transform duration-200 motion-safe:hover:-translate-y-1">
      <Image src={item.imageUrl || "/news-placeholder.svg"} alt="" width={640} height={360} unoptimized className="aspect-video w-full object-cover" />
      <div className="p-5"><div className="flex justify-between gap-3 text-xs text-muted-foreground"><span className="text-hunt">{item.category}</span><time dateTime={item.publishedAt}>{new Date(item.publishedAt).toLocaleDateString("de-DE", { timeZone: "Europe/Berlin" })}</time></div>
        <h3 className="mt-3 text-xl font-bold">{item.title}</h3><p className="mt-3 text-sm leading-6 text-muted-foreground">{item.summary}</p>
        <a href={item.sourceUrl} target="_blank" rel="noopener noreferrer" className="mt-5 inline-block text-sm font-semibold text-hunt">Originalquelle: {item.sourceName} ↗</a>
      </div>
    </article>
  </li>)}</ul>;
}

export function AiNewsSection() {
  const news = publishedAiNews().slice(0, 6);
  return <section className="page-wrap py-14" aria-labelledby="ki-news-heading">
    <h2 id="ki-news-heading" className="text-3xl font-bold">KI-News</h2>
    <p className="mt-3 text-muted-foreground">Die wichtigsten KI-Schlagzeilen – mit Einordnung und Originalquelle.</p>
    <AiNewsCards news={news} /><Link href="/news" className="mt-6 inline-flex rounded-full border border-border px-5 py-3 text-sm font-semibold">Alle News →</Link>
  </section>;
}
